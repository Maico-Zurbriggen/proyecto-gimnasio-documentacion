# ADR 0005: AI Gateway como módulo interno del backend

- Estado: **parcialmente reemplazada** por [ADR 0009](0009-servicio-generativo-online-en-el-polo.md) el 2026-09-01
- Fecha: 2026-08-25

> **Qué queda reemplazado y qué no.** La **ubicación de despliegue** decidida aquí —opción (b), módulo dentro del monolito del backend— queda reemplazada: la ADR 0009 despliega el servicio generativo como un proceso Python propio con worker durable en el Polo, es decir la opción (c) que esta ADR descarta. El motivo es una restricción física que esta ADR no consideró: un intento de generación puede durar hasta 120 segundos y Vercel no sostiene una petición de esa duración.
>
> **El patrón sigue vigente:** puerto estable más adaptador reemplazable, con timeout, reintento, límite por usuario, validación de esquema, redacción de registros y versionado de prompt concentrados en un único punto. Lo que cambia es dónde vive ese punto, no que exista.
>
> **La advertencia de coste operativo sigue vigente y sin resolver:** operar un proceso adicional es trabajo que la capacidad de construcción del proyecto no contabiliza. Ver ADR 0009, «Puntos operativos pendientes».

## Contexto

`Backend/AGENTS.md` ya instruye "encapsular LLM y recomendadores detrás de puertos/adaptadores", pero no especifica si ese puerto vive dentro del backend o como un servicio propio desplegado entre el backend y el LLM Server. Hace falta decidirlo antes de implementar RF-053 a RF-058.

## Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | El backend llama al LLM Server directamente, sin capa intermedia | Timeout, reintento, límite, redacción de logs y validación de schema se dispersan en cada punto de llamada del backend, contradiciendo la instrucción ya vigente en `AGENTS.md` de encapsular esto |
| (b) | **AI Gateway como módulo interno del backend** (puerto + adaptador, dentro del mismo monolito modular) | Un único punto donde viven timeout, reintento, límite, validación de schema, redacción de logs y versionado de prompt. No agrega un servicio para desplegar ni operar |
| (c) | AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server | Mismas ventajas de encapsulamiento que (b), más la posibilidad de que otros consumidores (además del backend) lo usen — pero agrega un tercer proceso a desplegar, versionar y operar |

## Decisión

(b). El AI Gateway es un módulo interno del backend (puerto `GenerativeAiPort` + adaptador `OllamaAdapter`), no un servicio desplegado por separado.

## Fundamento

[D12/§3](../../planning/risks-and-assumptions.md) ya muestra una capacidad de construcción de ~504 h contra un trabajo estimado de ~900 h — no hay margen para operar un tercer servicio (build, deploy, monitoreo, actualizaciones) sin sustento real de necesidad. ADR-0001 y ADR-0002 ya fijan la convención de monolito modular con un solo despliegue de backend, evitando microservicios que el presupuesto no justifica; agregar un Gateway desplegado aparte repite ese error que el propio proyecto ya evitó una vez para el backend en general. (a) se descarta porque ya existe la instrucción explícita de encapsular, y no seguirla dispersaría lógica transversal (timeout, rate limit, redacción, versión de prompt) en cada punto de llamada, dificultando tanto el cambio de modelo como la auditoría de RNF-19.

Ningún consumidor además del propio backend necesita al AI Gateway hoy: no hay integración con Telegram, WhatsApp ni ningún otro canal en el alcance de este proyecto (verificado contra D1-D13, sin resultados). Si eso cambiara, sería el disparador real para reconsiderar (c).

## Consecuencias

- El AI Gateway comparte el ciclo de despliegue del backend: una actualización del Gateway es una actualización del backend, con el mismo `npm run check` y el mismo pipeline de PR.
- El puerto (`GenerativeAiPort`) es la interfaz estable; el adaptador (`OllamaAdapter`) es lo único que cambia si cambia el runtime o el modelo (ver [ADR-0006](0006-llm-model-and-runtime-selection.md)).
- **Camino de evolución declarado, no implementado ahora**: si en el futuro aparece un segundo consumidor del LLM (por ejemplo, una herramienta interna del Polo Educativo, o un canal de mensajería), o si la concurrencia real supera lo que el backend puede sostener llamando directo al LLM Server, se promueve el módulo a servicio desplegado sin cambiar el contrato del puerto — sólo su ubicación de despliegue.
