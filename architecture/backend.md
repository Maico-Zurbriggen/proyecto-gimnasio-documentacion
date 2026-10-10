# Arquitectura del backend

**Catálogo objetivo:** [habilitaciones por gimnasio](exercise-catalog.md) y [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md), pendientes de implementación.

## Distribución

```text
React SPA -> Express + TypeScript -> Neon PostgreSQL
                 |
                 | HTTPS / OpenAPI IA (Vercel)
                 v
             FastAPI / Vercel -> Vercel Queues -> worker Python
                                                    |
                                                    v
                              Polo API (ngrok) -> Ollama / Polo
```

El backend es un monolito modular desplegado en Vercel y dueño del OpenAPI público, las invariantes transaccionales, la autorización, Prisma y las migraciones.

## Responsabilidad

Los módulos previstos son identidad, catálogo, rutinas, entrenamiento, métricas, seguimiento, administración e integración IA. Se crean al implementar historias verticales. Los routers sólo traducen HTTP; reglas y autorización viven en servicios o funciones de dominio y Prisma queda detrás de adaptadores de persistencia.

## Fronteras

- OpenAPI del backend es la fuente de verdad para frontend.
- Prisma no se expone como contrato HTTP.
- PostgreSQL es la única fuente de verdad transaccional.
- Backend autoriza, minimiza el contexto e invoca idempotentemente a IA; IA persiste la solicitud técnica y backend registra su ownership local antes de responder al frontend.
- Sólo el alumno autenticado puede iniciar, consultar y finalizar técnicamente una generación, y únicamente para su propio `studentId`; entrenador y administrador no originan solicitudes.
- El cliente del servicio IA se genera o valida desde el OpenAPI versionado por ese repositorio.
- El backend nunca espera al LLM: la API IA acepta con `202` y frontend consulta estado al backend.
- IA puede escribir sólo estados y resultados en estructuras de integración; backend es el único que crea la rutina `PROPUESTA` después de una finalización `POST` explícita y de validar la salida.
- La finalización técnica no aprueba la rutina ni la pone en vigencia; la revisión explícita del entrenador asignado sigue siendo obligatoria.
- Entrenamiento y scoring predictivo siguen fuera del camino de las peticiones.

## Fallos y seguridad

- La autenticación usa sesiones propias persistidas como hash. En Vercel la cookie es `HttpOnly; Secure; SameSite=None` por el despliegue cross-site; en local es `HttpOnly; SameSite=Lax`. La eliminación conserva los mismos atributos.
- Los headers `x-user-*` existen sólo como soporte interno de tests con `NODE_ENV=test`; desarrollo local, Test y Producción autentican exclusivamente mediante sesión.
- Cada intento generativo vence inicialmente a los 120 segundos y admite un único reintento.
- Una salida inválida nunca se presenta. Tras el segundo fallo la capacidad queda no disponible; no existe fallback determinístico de generación.
- El resto del sistema continúa y las plantillas privadas del entrenador y su creación manual permanecen disponibles (RF-019). ✎ El preset publicado (RF-021) pasa a alcance opcional y **no es la contingencia**: ver [D11/DD-35](../decisions/design-decisions.md).
- Credenciales y conexiones test/producción son distintas; ninguna URL de base se recibe desde una petición.
- El Polo recibe sólo contexto necesario y un identificador técnico, nunca credenciales ni identificadores personales innecesarios.

## Invariantes

1. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
2. Al comenzar una sesión se congela lo prescripto junto a lo realmente ejecutado.
3. Historial e indicadores derivados no son fuentes de verdad editables.
4. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
5. La autorización combina rol y propiedad o asignación del recurso.
6. Ningún resultado IA evita permisos, schema, referencias a la instantánea ni disponibilidad vigente. La selección y prescripción son decisiones de IA; el entrenador evalúa y aprueba (ADR 0013).

## Contrato objetivo: bloqueo por mediciones

Este contrato implementa RF-123, RF-124 y FL-22. El bloqueo funcional es independiente de `users.state`.

### Alumno

`GET /students/me/measurement-block`

- Requiere sesión y rol `ALUMNO`.
- Devuelve `200` con `measurementBlockState: NORMAL | PENDIENTE_MEDICION | PENDIENTE_APROBACION`, motivo, racha, fechas de bloqueo y envío, altura y fecha de la última medición.
- No expone datos de otro alumno ni acepta un identificador en la URL.

`POST /students/:studentId/measurements`

- Conserva el contrato existente `{ weightKg, heightCm }` y la verificación de propiedad.
- Siempre registra el peso y actualiza altura y `height_updated_at` atómicamente.
- Si hay un bloqueo `PENDIENTE_MEDICION`, la misma transacción vincula la medición al bloqueo y lo lleva a `PENDIENTE_APROBACION`.
- Si está `PENDIENTE_APROBACION`, responde `409 measurement_regularization_already_submitted` para no reemplazar silenciosamente la evidencia que revisa el entrenador.
- Responde `201` con la medición y `measurementBlockState`.

### Entrenador

`GET /students/:studentId/status`

- Conserva la verificación de asignación vigente.
- Reemplaza el booleano derivado de `users.state` por `measurementBlockState`, `motivoBloqueo`, `faltasConsecutivas`, `blockedAt`, `submittedAt` y la fecha de la última medición.
- No devuelve el detalle de la evidencia si el actor ya no tiene asignación vigente.

`POST /students/:studentId/unlock`

- Conserva la URL para reducir el cambio en frontend, pero pasa a ser una aprobación sin body.
- Requiere rol `ENTRENADOR`, asignación vigente y bloqueo `PENDIENTE_APROBACION`.
- En una única transacción vuelve a comprobar asignación y evidencia, cambia a `RESUELTO`, registra aprobador y fecha, crea auditoría y toma ese instante como inicio del ciclo nuevo.
- Responde `200` con el estado actualizado; `409 pending_measurement_required` si falta la carga; `409 measurement_block_already_resolved` si otra operación ya lo resolvió; `403` si no existe asignación vigente.

### Proceso interno

`GET /internal/jobs/measurement-blocks`

- No usa sesión de usuario. Exige `Authorization: Bearer ${CRON_SECRET}` con comparación segura.
- Evalúa ciclos cerrados en la zona horaria de cada gimnasio, crea controles faltantes en orden y bloquea al alcanzar tres faltas consecutivas.
- Es idempotente por `(student_id, due_on)`, por el control disparador y por el índice de un único bloqueo activo.
- Responde `200` con contadores agregados, sin datos personales: `{ checkpointsCreated, blocksCreated, skippedConcurrentRun }`.
- Producción se programa diariamente mediante Vercel Cron. El ambiente Preview/Test lo invoca manualmente o mediante un workflow programado de GitHub.

### Restricción transversal

Después de autenticar y resolver el rol activo, un middleware consulta el bloqueo vigente. Para operaciones como `ALUMNO`, sólo permite identidad propia, cierre de sesión, consulta del bloqueo y, en `PENDIENTE_MEDICION`, la carga de mediciones. No impide operar con roles `ENTRENADOR` o `ADMINISTRADOR` del mismo usuario.

## Renovación automática de rutina HU03

`GET /internal/jobs/routine-renewals` usa el mismo `CRON_SECRET` que el control de mediciones. Su OpenAPI está en `Backend/openapi/renewals.openapi.json`. El cron configurado corre cada hora, detecta cierres de ciclo y finaliza resultados ya completados; Preview/Test necesita un scheduler externo o invocación autenticada, igual que el control de mediciones. La generación asíncrona no requiere una petición abierta al LLM ni una acción del alumno.

Primero evalúa los controles de mediciones. Si otro proceso los está evaluando, omite esta ejecución para no capturar una racha incompleta. Después captura evidencia y crea ciclos únicos en `app.routine_renewal_cycles`. Un lote de hasta cinco ciclos obtiene leases de cinco minutos; las ejecuciones siguientes priorizan ciclos nuevos o menos recientemente procesados, para que fallos repetidos no impidan atender a otros alumnos.

El job usa la creación de solicitudes IA 2.0 existente, registra el vínculo durable antes del despacho y consulta estados/resultados en base. Comparte la validación técnica de generación y disponibilidad del catálogo. Compara el contexto material vigente y conserva la historia y evidencia del instante capturado; no recalcula el diagnóstico RN-79a. Las solicitudes de renovación no pueden finalizarse mediante el endpoint del alumno para crear una rutina inicial.

La finalización crea diagnóstico técnico, propuesta `ESTRUCTURA`, ajuste con evidencia y aviso en una transacción. La consulta de propuestas lee la evaluación persistida en el ciclo. La aprobación vuelve a comprobar asignación, versión de origen y catálogo, crea una versión de la rutina existente, conserva la anterior y reinicia el ciclo. Los fallos crean una alerta persistida e idempotente para el entrenador o administradores; no producen una rutina alternativa.

La generación de una planilla nueva usa el contrato generativo 2.0 con selección del catálogo completo y grupos de series. El transporte valida hasta 500 series y la política explícita capturada del gimnasio, sin decidir entrenamiento mediante tablas fijas. La IA conserva objetivo, tipo y frecuencia salvo evidencia aplicable de RN-89a, y debe cambiar la estructura. Las solicitudes históricas sin `routine_renewal_full_catalog` conservan el schema de redistribución de apariciones de origen.

Las solicitudes nuevas de renovación y regeneración entregan al modelo todo el catálogo habilitado, con sus fichas completas y una referencia por índice. La estructura vigente se conserva como contexto: la IA puede seleccionar otros ejercicios habilitados y prescribir según los parámetros explícitos del gimnasio. Las solicitudes históricas mantienen su esquema de redistribución de origen. Los nombres que muestra la propuesta proceden del catálogo capturado.

La ficha del alumno enlaza las propuestas de adaptación pendientes. Su revisión presenta la planilla completa, la distribución anterior y propuesta calculada desde los datos estructurados, el criterio y las mediciones capturadas. No utiliza el relato del modelo para reconstruir cambios: el resultado bruto permanece registrado para auditoría.

### QA reproducible

`GET/PUT /gyms/me/generation-settings` usa el gimnasio de la sesión: administrador escribe y entrenador puede consultar. `app.gyms` conserva JSON de parámetros y revisión. Las solicitudes 2.0 capturan ambos y la finalización/aprobación vuelve a verificar la revisión. El contrato se publica en `Backend/openapi/generation-management.openapi.json`; `npm run generation:openapi` lo actualiza y `npm run generation:contract` en Frontend genera sus schemas.

`POST/GET /proposals/:proposalId/regeneration` exige rol ENTRENADOR y asignación vigente. `app.routine_proposal_regenerations` conserva comentario, clave idempotente, solicitud y secuencia creciente; una restricción parcial permite una sola regeneración pendiente. El polling finaliza el reemplazo, guarda ambas planillas en auditoría y mantiene la evidencia del ciclo. Un rechazo técnico crea una alerta única por regeneración sin borrar la planilla anterior. La resolución verifica que no haya regeneración pendiente y que `candidateRequestId` coincida con la planilla revisada.

La suite `Backend/test/integration/automatic-routine-renewal.test.ts` requiere `RENEWAL_TEST_DATABASE_URL` y sólo acepta la base desechable `gym_renewal_qa`, host `127.0.0.1` y puerto `65433`. Aplica todas las migraciones con `DATABASE_URL` apuntando a esa base y ejecuta `npm run check` desde Backend con la variable de QA definida. Nunca apuntar esa suite a `gym_local`, Neon Test ni producción.

La verificación de 2026-10-09 utiliza PostgreSQL 17 en un contenedor con almacenamiento temporal. Prueba ciclos de 60 días y zona horaria, evidencia nueva/ausente/tardía, concurrencia, recuperación de leases, caída de despacho y worker, bloqueo en tercera falta, salida inválida, permisos del cron y aprobación de estructura. El transporte y los resultados de IA son dobles internos de prueba; no acreditan la disponibilidad del Polo.

La extensión de 2026-10-10 agrega pruebas de regeneración simultánea, recuperación del estado, conservación de evidencia y versión vigente, resultados repetidos/`UNABLE`, catálogo deshabilitado o externo, parámetros capturados y revisiones obsoletas. También se verificó el recorrido local con IA real: el administrador guardó los parámetros y Lucía regeneró la propuesta de Martín, sin aprobarla. La revisión muestra incorporaciones, ejercicios quitados y los parámetros con los que se produjo la planilla.
