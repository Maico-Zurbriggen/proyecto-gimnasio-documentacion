# Arquitectura del repositorio de IA

## Dos límites ejecutables

`proyecto-gimnasio-ia` contiene componentes separados:

1. **Servicio generativo online:** API FastAPI y consumidor asíncrono desplegados en Vercel.
2. **Analítica batch:** extracción, features, entrenamiento, evaluación y scoring predictivo futuros.

Compartir repositorio no permite que un componente use la frontera del otro ni que el trabajo batch entre en una petición.

## Servicio generativo

```text
Express/Vercel -> FastAPI/Vercel -> Vercel Queues -> worker Python
                         |                              |
                         +---------- Neon --------------+
                                                        |
                                                        v
                                  Cloudflare Tunnel -> Ollama/Polo
```

- Expone HTTP versionado para backend; nunca para frontend.
- Acepta una solicitud idempotente con `202` y la delega a un worker durable.
- Orquesta el LLM mediante un conector privado y valida el esquema de su respuesta.
- Usa únicamente contexto minimizado y estructuras de integración autorizadas.
- Escribe estados y resultados técnicos; no crea, aprueba ni activa rutinas.
- Preview de `test` y Production de `main` usan URL, credencial y conexión aisladas.
- El mensaje de cola contiene únicamente el UUID de la solicitud y el consumidor es idempotente ante redelivery.
- No existe modo fake ejecutable; los tests sí pueden usar dobles internos.

## Analítica batch

- Lee vistas o snapshots versionados acordados con backend.
- Escribe resultados precalculados con versión, instante y explicación.
- No modifica fuentes transaccionales.
- Ejecuta extracción, validación, features point-in-time, entrenamiento, evaluación y persistencia idempotente.
- Si un modelo no supera un criterio simple, se conserva el criterio simple.

## Operación

Vercel opera la API FastAPI, la cola y el consumidor. En el Polo sólo Ollama y el agente `cloudflared` deben arrancar con la máquina y reiniciarse ante fallos. Cloudflare Tunnel publica mediante un dominio estable únicamente los endpoints de inferencia necesarios; el servicio IA envía `LLM_API_TOKEN` como Bearer.

## Invariantes

- Ningún dato identificatorio innecesario llega al LLM.
- Ninguna salida se publica sin modelo, configuración, instante y contexto mínimo reproducible.
- El rol PostgreSQL de IA no accede a identidad ni modifica entidades de dominio.
- Ninguna feature batch usa información posterior al instante predicho.
- Falta de datos no equivale a cero.
- Los datos simulados se identifican y no se presentan como reales.
