# ADR 0009: servicio generativo online en el Polo

- Estado: aceptada
- Fecha: 2026-08-29 (renumerada el 2026-09-01)

## Nota de renumeración

Esta ADR se emitió con el número 0004, ya ocupado por [ADR 0004: LLM autohospedado sobre infraestructura del Polo Educativo](0004-self-hosted-llm-server.md). Eran dos decisiones distintas con el mismo identificador. Se renumera a **0009** conservando su fecha y su contenido. Relación con las otras dos ADR del mismo dominio:

- **ADR 0004 (LLM autohospedado)** sigue vigente y es complementaria: decide *dónde corre el modelo* —infraestructura del Polo, no un proveedor externo—. Esta ADR decide *qué proceso lo orquesta y dónde vive ese proceso*.
- **[ADR 0005 (AI Gateway como módulo interno del backend)](0005-ai-gateway-in-process-module.md) queda reemplazada en su parte de ubicación de despliegue.** Aquella descartó explícitamente la opción «(c) AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server», que es exactamente lo que esta ADR decide. La contradicción existió con ambas en estado «aceptada» desde el 2026-08-29; se resuelve a favor de esta.

### Por qué prevalece esta ADR sobre la 0005

El fundamento de la ADR 0005 es un presupuesto de esfuerzo: no hay capacidad para operar un tercer servicio. El de esta ADR es una restricción física: un intento de generación puede durar hasta 120 segundos y Vercel no sostiene una petición de esa duración, de modo que hace falta un proceso durable fuera de la función serverless. Un presupuesto se renegocia; la restricción no.

**Lo que de la ADR 0005 sigue vigente y se adopta aquí:** el patrón puerto y adaptador. Timeout, reintento, límite por usuario, validación de esquema, redacción de registros y versionado de prompt viven en un único punto —ahora dentro del servicio Python, no del backend— y el conector hacia el modelo es un adaptador reemplazable sin tocar el resto.

**Lo que la ADR 0005 advertía y sigue siendo cierto:** operar API, worker, modelo y agente ngrok en el Polo es trabajo de operación que la capacidad de construcción del proyecto no contabiliza. Ver los puntos operativos pendientes al final de este documento.

## Contexto

El alcance generativo v2.1 asigna a un LLM la interpretación de pedidos, la selección del tipo de rutina, la construcción de una rutina completa, la explicación y la oferta de alternativas. El LLM ya se ejecuta en infraestructura del Polo. Por políticas de red, el código Python también puede desplegarse allí, pero su API debe exponerse mediante ngrok.

La arquitectura anterior describía `proyecto-gimnasio-ia` únicamente como motor batch, sin HTTP, y exigía una construcción determinística cuando el proveedor generativo fallaba. Esas dos restricciones son incompatibles con el alcance confirmado.

## Decisión

`proyecto-gimnasio-ia` tendrá dos límites ejecutables independientes:

1. un **servicio generativo online** Python, con API HTTP versionada y worker asíncrono, desplegado en el Polo;
2. trabajos analíticos y predictivos batch, fuera del camino de las peticiones.

El servicio Python orquesta el LLM del Polo; el LLM no es el servicio de orquestación ni accede a PostgreSQL. Ngrok publica únicamente la API Python mediante un dominio HTTPS estable.

```text
React -> Express/Vercel -> ngrok -> API Python/Polo -> LLM/Polo
              |                       |
              +------ Neon <----------+
```

### Flujo asíncrono

1. El frontend solicita la generación al backend.
2. El backend autoriza, minimiza el contexto y persiste una solicitud con identificador idempotente.
3. El backend llama al servicio Python, que acepta con `202` sin esperar al LLM.
4. Un worker reclama la solicitud persistida, llama al LLM y escribe el resultado en estructuras de integración designadas.
5. El frontend consulta el estado exclusivamente al backend.
6. El backend valida esquema, catálogo, compatibilidad y rangos; sólo entonces crea un candidato.
7. Ninguna rutina entra en vigencia sin revisión favorable de un entrenador.

Cada intento puede durar como máximo 120 segundos. Una salida inválida o un fallo técnico admite un único reintento. Tras el segundo fallo la generación queda `NO_DISPONIBLE`; no se construye una rutina determinística. El resto del sistema y la creación manual por entrenadores continúan. Los presets quedan como alcance opcional y no son una dependencia de esta contingencia.

### Contratos y autoridad

- IA es dueña del OpenAPI del servicio de orquestación y del conector privado hacia el LLM.
- Backend genera o valida su cliente desde una versión explícita de ese OpenAPI.
- Backend es dueño de Prisma, las migraciones, las estructuras de integración y todas las reglas de negocio.
- El servicio IA sólo accede a estructuras de integración expresamente autorizadas; no crea, aprueba, asigna ni activa rutinas.
- Backend e IA se despliegan independientemente. Los cambios incompatibles usan una versión nueva y compatibilidad temporal.

### Datos y credenciales

El Polo recibe únicamente el contexto necesario: identificador técnico, objetivo, nivel, frecuencia, condiciones físicas pertinentes, equipamiento, catálogo permitido y preferencias confirmadas. No recibe nombre, correo, teléfono, documento ni credenciales, y los logs no guardan prompts completos ni datos de salud.

Una única API y configuración del modelo atienden inicialmente test y producción. Credenciales de consumo diferentes seleccionan conexiones PostgreSQL diferentes, configuradas en el servidor; ninguna petición suministra una URL de base. El authtoken de ngrok, las credenciales backend–IA y las credenciales IA–LLM son secretos distintos.

Los resultados aceptados conservan contexto mínimo y versiones para auditoría. Solicitudes abandonadas, respuestas inválidas y fallos se eliminan a los 30 días. Los casos de regresión se anonimizan antes de conservarse.

### Ambientes

- Frontend y backend locales usan Neon Test y la credencial test del servicio IA.
- No se implementa un adaptador `fake` ejecutable. Los tests pueden reemplazar el transporte HTTP o el conector LLM con dobles de prueba.
- `test` despliega el ambiente estable de prueba; `main`, producción.
- Neon Test y Neon Producción no comparten base ni credenciales.

## Consecuencias

- Se reemplazan las restricciones batch-only de ADR 0002 para el repositorio IA; el pipeline analítico batch permanece vigente.
- DD-31 deja de asignar la construcción inicial de rutinas a una tabla determinística: RN-39a y la compatibilidad pasan a ser barreras de validación, no el generador principal.
- RF-058, RF-113, RNF-04, RNF-11 y RNF-18 dejan de exigir fallback determinístico para generación.
- Ngrok y la disponibilidad de la máquina del Polo pasan a ser dependencias operativas. Un dominio estable, reinicio automático y monitoreo son requisitos de producción.
- El servicio online exige un proceso API y un worker durable; no se ejecuta el LLM dentro de una petición de Vercel ni como tarea de fondo no durable.
- Un cambio de modelo, prompt o parámetros requiere evaluación de regresión y validación de al menos un entrenador antes de producción.

## Puntos operativos pendientes

Antes del primer despliegue real deben confirmarse el contrato y autenticación del LLM, la capacidad de ejecutar servicios permanentes en el Polo, el plan de ngrok con dominio estable y el mecanismo de instalación y rollback del código Python. Estos puntos no cambian la frontera decidida.
