# Despliegue del servicio IA e integración con backend

## Resultado esperado

```text
Backend/Vercel -> FastAPI/Vercel -> Vercel Queues -> consumidor Python
                                                        |
                                                        v
                                      ngrok -> Polo API -> Ollama
```

Un único proyecto Vercel del repositorio IA produce Preview para `test` y Production para `main`. Los ambientes no comparten URL de servicio IA, clave backend–IA ni conexión Neon; inicialmente comparten el mismo LLM, URL y token. Las decisiones están registradas en [ADR 0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) y [ADR 0012](../decisions/adr/0012-api-polo-ngrok.md), con la [gu?a de endpoints](../architecture/API_ENDPOINTS_VIVAZ.pdf).

## 1. Preparar el Polo

1. Instalar Ollama y descargar el modelo configurado:

   ```bash
   ollama pull qwen3.5:9b
   ```

2. Mantener Ollama escuchando sólo en la interfaz local y comprobar `http://127.0.0.1:11434/api/tags` desde el Polo.
3. Configurar el router autenticado del Polo para que `https://yen-entrench-grader.ngrok-free.dev/polo` reenv?e las rutas nativas de Ollama.
4. Guardar el secreto `POLO_API_TOKEN` en el router y en el servicio IA. No reutilizar `VIVAZ_API_KEY` ni `AI_SERVICE_API_KEY`.
5. Administrar el router y el agente ngrok con reinicio autom?tico. La gu?a del Polo indica que systemd inicia ambos cuando arranca el servidor.
6. Verificar desde una red externa:

   ```bash
   export POLO_BASE_URL="https://yen-entrench-grader.ngrok-free.dev/polo"
   curl -sS -H 'ngrok-skip-browser-warning: 1' \
     -H "Authorization: Bearer ${POLO_API_TOKEN}" \
     "$POLO_BASE_URL/api/tags"
   ```

No publicar el puerto de Ollama directamente ni guardar tokens en Git, logs o cuerpos de solicitud.

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
| `GENERATION_QUEUE_MODE` | `vercel` | `vercel` |
| `QUEUE_REGION` | `gru1` | `gru1` |
| `LLM_API_URL` | `https://yen-entrench-grader.ngrok-free.dev/polo` | mismo endpoint del Polo |
| `LLM_API_TOKEN` | secreto `POLO_API_TOKEN` | mismo token inicial del Polo |
| `LLM_MODEL` | `qwen3.5:9b` | `qwen3.5:9b` |
| `LLM_CONFIGURATION_VERSION` | `generative/generar-rutina@10` | igual, salvo promoción versionada |
| `GENERATION_TIMEOUT_SECONDS` | `120` | `120` |
| `GENERATION_MAX_RETRIES` | `1` | `1` |

Todas las ramas Preview comparten el conjunto Preview de variables. Sólo `test` se considera el ambiente integrado estable; los Preview de features no deben tratarse como ambientes aislados.

## 4. Verificar IA

Con la URL del deployment correspondiente:

```bash
curl https://URL-IA/health
curl -H "Authorization: Bearer AI_SERVICE_API_KEY" https://URL-IA/ready
```

`/health` debe devolver `200` aunque una dependencia esté caída. `/ready` devuelve `200` únicamente si puede consultar Neon y `GET /polo/api/tags`; un `503` se investiga en Vercel Logs, el router ngrok y el proceso Ollama. `ERR_NGROK_3200` indica que el servidor o el túnel del Polo está desconectado.

## 5. Conectar backend

En el proyecto Vercel del backend configurar y volver a desplegar:

| Variable | Preview (`test`) | Production (`main`) |
| --- | --- | --- |
| `AI_SERVICE_URL` | URL estable del Preview IA de `test` | URL Production del servicio IA |
| `AI_SERVICE_API_KEY` | mismo secreto test configurado en IA | mismo secreto producción configurado en IA |
| `AI_SERVICE_REQUEST_TIMEOUT_MS` | `10000` | `10000` |

Backend crea primero la fila idempotente en `ai_integration.ai_generation_requests` con el contexto minimizado y el catálogo prefiltrado, y registra su ownership. Luego su adaptador envía exclusivamente el UUID a IA:

```text
POST {AI_SERVICE_URL}/v1/generation-requests/{requestId}/dispatch
Authorization: Bearer {AI_SERVICE_API_KEY}
```

IA verifica que la solicitud exista y siga procesable, publica su UUID en Vercel Queues y responde `202`. El endpoint no recibe perfil, catálogo ni credenciales en el cuerpo. El frontend nunca llama a IA ni conoce sus URLs.

## 6. Prueba integrada y promoción

1. Promover los cambios relacionados de backend e IA a `test`.
2. Confirmar `/health` y `/ready` en ambos servicios.
3. Crear una solicitud desde el caso de uso backend y comprobar la secuencia `PENDIENTE → PROCESANDO → COMPLETADA` o, ante dos fallos, `NO_DISPONIBLE`.
4. Comprobar en Neon que hay como máximo dos intentos y un único resultado por intento.
5. Verificar una generación sintética mediante `/api/chat` con `format: "json"`, `think: false` y validación Pydantic; luego simular caída de Ollama o del router ngrok y comprobar timeout, reintento y disponibilidad del backend.
6. Validar salida y aprobación con un entrenador antes de promover a `main`.
7. Repetir smoke tests sobre Production sin reutilizar secretos ni datos de Test.

El despliegue del transporte no reemplaza el caso de uso backend que minimiza contexto, crea la solicitud y convierte un resultado válido en rutina `PROPUESTA`; esos pasos deben entrar juntos en una historia vertical antes de habilitar el botón del frontend.
