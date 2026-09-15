# ADR 0010: servicio de IA en Vercel y LLM en el Polo

- Estado: aceptada
- Fecha: 2026-09-15
- Reemplaza parcialmente: [ADR 0009](0009-servicio-generativo-online-en-el-polo.md)
- Reemplazada parcialmente por: [ADR 0011](0011-cloudflare-tunnel-para-el-llm.md), para transporte y autenticación IA–LLM

## Contexto

La ADR 0009 ubicó la API Python y un worker residente en el Polo porque una petición HTTP no debía permanecer abierta durante la inferencia. El equipo decidió desplegar el código del repositorio IA en Vercel y conservar únicamente el runtime Ollama y el LLM en el Polo.

Vercel dispone de runtime FastAPI y consumidores Python de Vercel Queues. Esto permite mantener la aceptación rápida con `202`, reintentos y entrega durable sin un proceso Python residente en el Polo.

## Decisión

1. La API FastAPI y su consumidor de generación se despliegan desde `proyecto-gimnasio-ia` en Vercel.
2. La API autentica al backend, verifica el UUID de una solicitud ya creada y publica un mensaje idempotente en Vercel Queues. No recibe perfiles, URLs de base ni credenciales en el cuerpo.
3. Un consumidor privado de la cola reclama la solicitud en `ai_integration`, llama al LLM y persiste intentos, estados y salida estructurada.
4. Ollama y el modelo continúan en el Polo. Un dominio HTTPS estable de ngrok expone sólo la API de inferencia necesaria y exige autenticación de servicio en el borde; Ollama no se publica sin protección.
5. Un único proyecto de Vercel usa el deployment Preview estable de `test` con Neon Test y el deployment Production de `main` con Neon Producción. Cada ambiente tiene URL, clave backend–IA, conexión Neon y credenciales IA–ngrok distintas.
6. La cola usa entrega al menos una vez. El consumidor es idempotente, conserva el lease PostgreSQL recuperable y limita inicialmente la concurrencia a uno para proteger el LLM del Polo.
7. Cada intento conserva el límite de 120 segundos y existe un único reintento. Tras el segundo fallo se registra `NO_DISPONIBLE`.

## Consecuencias

- Backend deja de llamar a ngrok: sólo conoce la URL Vercel del servicio IA correspondiente a su ambiente.
- El Polo opera Ollama y el agente ngrok; ya no opera API ni worker Python.
- Vercel Queues resuelve el desacople durable. No se usa `fire-and-forget`, `waitUntil` ni un cron como sustituto de la cola.
- PostgreSQL continúa siendo la fuente de verdad del estado. La cola transporta únicamente el UUID técnico y puede redeliverlo sin duplicar resultados.
- El runtime Python y Vercel Queues están en beta al tomar esta decisión. Se agrega como riesgo operativo y se conserva el puerto del conector para poder cambiar proveedor sin alterar dominio ni contratos.
- El endpoint ngrok debe tener dominio estable, TLS y autenticación no interactiva. La URL y las credenciales son secretos de Vercel, no archivos del repositorio.

## Relación con decisiones anteriores

- [ADR 0004](0004-self-hosted-llm-server.md) sigue vigente: el modelo permanece autohospedado en el Polo.
- ADR 0009 queda reemplazada sólo en la ubicación de API/worker y en el esquema de una API compartida que seleccionaba base por credencial. Su política de asincronía, timeout, reintento e indisponibilidad continúa vigente aquí.
- [ADR 0005](0005-ai-gateway-in-process-module.md) continúa vigente como patrón de puerto y adaptador, no como ubicación física.
