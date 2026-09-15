# Despliegue del servicio IA e integración con backend

## Resultado esperado

```text
Backend/Vercel -> FastAPI/Vercel -> Vercel Queues -> consumidor Python
                                                        |
                                                        v
                                              ngrok -> Ollama/Polo
```

Un único proyecto Vercel del repositorio IA produce Preview para `test` y Production para `main`. Los ambientes no comparten URL, claves de servicio ni conexión Neon. La decisión está registrada en [ADR 0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md).

## 1. Preparar el Polo

1. Instalar Ollama y descargar el modelo configurado:

   ```bash
   ollama pull qwen2.5:7b-instruct
   ```

2. Mantener Ollama escuchando sólo en la interfaz local y comprobar `http://127.0.0.1:11434/api/tags` desde el Polo.
3. Reservar un dominio HTTPS estable en ngrok.
4. Crear una credencial Basic Auth larga y aleatoria para cada ambiente. Guardarla en el vault de ngrok; no escribirla en Git.
5. Aplicar una Traffic Policy equivalente a:

   ```yaml
   on_http_request:
     - actions:
         - type: basic-auth
           config:
             credentials:
               - vercel-test:${secrets.get('gym-llm', 'test-password')}
               - vercel-production:${secrets.get('gym-llm', 'production-password')}
   ```

6. Iniciar el agente contra Ollama con el dominio y la policy configurados. Administrar Ollama y ngrok como servicios con reinicio automático según el sistema operativo del Polo.
7. Verificar desde una red externa:

   ```bash
   curl -u "vercel-test:REEMPLAZAR" https://DOMINIO-ESTABLE.ngrok.app/api/tags
   ```

No publicar el puerto de Ollama directamente ni usar la clave de la API administrativa de ngrok como credencial de inferencia.

## 2. Crear el proyecto IA en Vercel

1. En **Add New → Project**, importar `Maico-Zurbriggen/proyecto-gimnasio-ia`.
2. Dejar la raíz del repositorio como Root Directory. Vercel detecta FastAPI desde `app.py`; no establecer Build Command ni Output Directory.
3. En Git, establecer `main` como Production Branch. La rama `test` genera el Preview estable de validación.
4. Desactivar Vercel Authentication para este proyecto: backend debe poder llegar a la API sin una sesión Vercel. Los endpoints privados ya exigen su propio Bearer y el consumidor de Queue no tiene URL pública.
5. Realizar el primer deploy. Vercel crea el consumidor privado declarado en `pyproject.toml`; el SDK usa OIDC automáticamente dentro del deployment.

Las llamadas locales a Vercel Queues sí necesitan `vercel link` y `vercel env pull`; el despliegue no requiere guardar un token OIDC manual.

## 3. Variables del proyecto IA

Configurar valores diferentes en **Preview** y **Production** y volver a desplegar después de cambiarlos:

| Variable | Preview (`test`) | Production (`main`) |
| --- | --- | --- |
| `APP_ENV` | `test` | `production` |
| `DATABASE_URL` | Neon Test, rol runtime IA, pooler | Neon Producción, rol runtime IA, pooler |
| `AI_SERVICE_API_KEY` | secreto backend–IA test | secreto backend–IA producción |
| `QUEUE_REGION` | `gru1` | `gru1` |
| `LLM_API_URL` | dominio HTTPS estable ngrok | dominio HTTPS estable ngrok |
| `LLM_MODEL` | `qwen2.5:7b-instruct` | `qwen2.5:7b-instruct` |
| `LLM_BASIC_AUTH_USERNAME` | `vercel-test` | `vercel-production` |
| `LLM_BASIC_AUTH_PASSWORD` | contraseña test | contraseña producción |
| `LLM_CONFIGURATION_VERSION` | `generative/generar-rutina@1` | igual, salvo promoción versionada |
| `GENERATION_TIMEOUT_SECONDS` | `120` | `120` |
| `GENERATION_MAX_RETRIES` | `1` | `1` |

Todas las ramas Preview comparten el conjunto Preview de variables. Sólo `test` se considera el ambiente integrado estable; los Preview de features no deben tratarse como ambientes aislados.

## 4. Verificar IA

Con la URL del deployment correspondiente:

```bash
curl https://URL-IA/health
curl -H "Authorization: Bearer AI_SERVICE_API_KEY" https://URL-IA/ready
```

`/health` debe devolver `200` aunque una dependencia esté caída. `/ready` devuelve `200` únicamente si puede consultar Neon y `/api/tags` de Ollama; un `503` se investiga en Vercel Logs, ngrok y el proceso Ollama.

## 5. Conectar backend

En el proyecto Vercel del backend configurar y volver a desplegar:

| Variable | Preview (`test`) | Production (`main`) |
| --- | --- | --- |
| `AI_SERVICE_URL` | URL estable del Preview IA de `test` | URL Production del servicio IA |
| `AI_SERVICE_API_KEY` | mismo secreto test configurado en IA | mismo secreto producción configurado en IA |
| `AI_SERVICE_REQUEST_TIMEOUT_MS` | `10000` | `10000` |

Backend crea primero la fila idempotente en `ai_integration.ai_generation_requests`. Luego su adaptador ejecuta:

```text
POST {AI_SERVICE_URL}/v1/generation-requests/{requestId}/dispatch
Authorization: Bearer {AI_SERVICE_API_KEY}
```

IA verifica que la solicitud exista, publica su UUID y responde `202`. El frontend nunca llama a IA ni conoce sus URLs.

## 6. Prueba integrada y promoción

1. Promover los cambios relacionados de backend e IA a `test`.
2. Confirmar `/health` y `/ready` en ambos servicios.
3. Crear una solicitud desde el caso de uso backend y comprobar la secuencia `PENDIENTE → PROCESANDO → COMPLETADA` o, ante dos fallos, `NO_DISPONIBLE`.
4. Comprobar en Neon que hay como máximo dos intentos y un único resultado por intento.
5. Simular caída de Ollama o ngrok y verificar timeout, reintento y que el resto del backend continúa disponible.
6. Validar salida y aprobación con un entrenador antes de promover a `main`.
7. Repetir smoke tests sobre Production sin reutilizar secretos ni datos de Test.

El despliegue del transporte no reemplaza el caso de uso backend que minimiza contexto, crea la solicitud y convierte un resultado válido en rutina `PROPUESTA`; esos pasos deben entrar juntos en una historia vertical antes de habilitar el botón del frontend.
