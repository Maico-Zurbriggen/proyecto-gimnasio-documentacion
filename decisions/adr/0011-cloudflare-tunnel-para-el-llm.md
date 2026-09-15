# ADR 0011: Cloudflare Tunnel para acceder al LLM del Polo

- Estado: aceptada
- Fecha: 2026-09-15
- Reemplaza parcialmente: [ADR 0010](0010-servicio-ia-en-vercel-y-llm-en-el-polo.md)

## Contexto

ADR 0010 estableció que el servicio IA desplegado en Vercel accede al LLM del Polo mediante un dominio HTTPS estable y supuso ngrok con Basic Auth. La infraestructura disponible usa Cloudflare Tunnel y entrega una URL junto con un token de acceso.

## Decisión

1. Cloudflare Tunnel publica exclusivamente la API de inferencia de Ollama que necesita el servicio IA.
2. `LLM_API_URL` contiene el dominio HTTPS estable del túnel.
3. `LLM_API_TOKEN` contiene el token de consumo y el cliente lo envía como `Authorization: Bearer <token>`.
4. `AI_SERVICE_API_KEY` permanece separado: autentica backend hacia el servicio IA y nunca se reutiliza para llamar al LLM.
5. Test y producción comparten inicialmente el mismo LLM, URL y token. Conservan claves backend–IA y conexiones PostgreSQL diferentes.
6. Ollama no se publica directamente y el token nunca se guarda en Git, logs, cuerpos de solicitud ni documentación.

## Consecuencias

- Desaparecen `LLM_BASIC_AUTH_USERNAME` y `LLM_BASIC_AUTH_PASSWORD`.
- El Polo opera Ollama y el agente `cloudflared`; ambos deben iniciar con la máquina y reiniciarse ante fallos.
- La rotación de `LLM_API_TOKEN` afecta inicialmente a Preview y Production y debe coordinarse en ambos ambientes.
- El conector conserva su frontera HTTP, por lo que cambiar el mecanismo de autenticación no modifica los contratos backend–IA ni el dominio.

## Relación con decisiones anteriores

- ADR 0010 sigue vigente para Vercel, Vercel Queues, Neon y la ubicación del servicio IA; queda reemplazada sólo en el transporte y autenticación IA–LLM.
- [ADR 0004](0004-self-hosted-llm-server.md) sigue vigente: Ollama y el modelo permanecen autohospedados en el Polo.
