# ADR 0012: API autenticada del Polo mediante ngrok

- Estado: aceptada
- Fecha: 2026-09-29
- Reemplaza parcialmente: [ADR 0011](0011-cloudflare-tunnel-para-el-llm.md), sólo para transporte y autenticación IA–LLM
- Evidencia de endpoints: [API_ENDPOINTS_VIVAZ.pdf](../../architecture/API_ENDPOINTS_VIVAZ.pdf)

## Contexto

La guía vigente de la API del Polo documenta un dominio ngrok estable compartido por Vivaz y Polo. Vivaz usa la raíz; Polo publica el proxy autenticado de Ollama bajo `/polo`. Las rutas conservan el contrato nativo de Ollama y el token de Polo es distinto de la clave de Vivaz. Esto contradice la decisión de Cloudflare Tunnel de ADR 0011 y coincide con la alternativa ngrok ya prevista por ADR 0010.

## Decisión

1. Vercel, Vercel Queues, Neon y el despacho por UUID de ADR 0010 permanecen vigentes.
2. `LLM_API_URL` contiene `https://yen-entrench-grader.ngrok-free.dev/polo`; el conector añade `/api/tags` y `/api/chat`.
3. El conector conserva el formato nativo de Ollama. No usa el endpoint OpenAI-compatible de Vivaz.
4. `LLM_API_TOKEN` contiene el secreto `POLO_API_TOKEN`. No se reutiliza `VIVAZ_API_KEY` ni `AI_SERVICE_API_KEY`.
5. Cada llamada al Polo envía `Authorization: Bearer …` y `ngrok-skip-browser-warning: 1`. El segundo encabezado omite la pantalla intermedia de ngrok y no reemplaza la autenticación.
6. Ollama permanece detrás del router autenticado del Polo; el puerto local de Ollama no se publica directamente.
7. La generación usa `format: "json"` y `think: false`; el esquema de salida se incluye en el prompt y Pydantic valida la respuesta antes de persistirla. En el servidor vigente, enviar el JSON Schema directamente en `format` devolvió `400 Failed to initialize samplers: failed to parse grammar`.

## Consecuencias

- La prueba de disponibilidad del LLM consulta `{LLM_API_URL}/api/tags`; la generación usa `{LLM_API_URL}/api/chat`.
- Un `401` indica un `POLO_API_TOKEN` ausente o incorrecto. Un `503` o `ERR_NGROK_3200` indica que el router, el servidor o el agente ngrok no está disponible.
- La guía del Polo indica que systemd inicia el router y ngrok con el servidor. La operación y recuperación de esos procesos sigue siendo responsabilidad del Polo.
- El token continúa fuera de Git, logs, cuerpos de solicitud y documentación. Test y Production comparten inicialmente el endpoint y el token de Polo; mantienen separadas sus claves backend–IA y bases de datos.

## Relación con decisiones anteriores

- [ADR 0010](0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) sigue vigente para la API FastAPI, la cola, el worker y la persistencia.
- [ADR 0011](0011-cloudflare-tunnel-para-el-llm.md) queda como antecedente histórico del transporte Bearer; su referencia a Cloudflare está reemplazada por esta decisión.
- [ADR 0004](0004-self-hosted-llm-server.md) sigue vigente: Ollama y el modelo permanecen autohospedados en el Polo.
