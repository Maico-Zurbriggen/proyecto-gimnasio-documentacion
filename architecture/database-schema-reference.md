# Referencia física de la base de datos

**Referencia de implementación local, 2026-10-10:** incluye [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md). No afirma despliegue ni publicación del dataset real; operación y pendientes en [catálogo](exercise-catalog.md).

```yaml
document_id: ARCH-DATABASE-SCHEMA
status: implementation-reference
snapshot_date: 2026-10-10
source_of_structure: proyecto-gimnasio-back/prisma/schema.prisma
database: PostgreSQL
schemas: [app, ai_integration]
contains_row_values: false
contains_credentials: false
```

## Extensión física de renovación automática, 2026-10-09

La migración `20261009180000_automatic_routine_renewal` agrega `app.routine_renewal_cycles`. Contrato de comportamiento: [D5/§9.3](../domain/business-rules.md#93-renovación-automática-de-ciclo--hu03).

| Columna | Tipo y restricciones |
| --- | --- |
| id | uuid PK, DEFAULT gen_random_uuid() |
| routine_version_id | uuid, FK app.routine_versions.id, ON DELETE RESTRICT |
| cycle_starts_on / due_on | date; due_on > cycle_starts_on; UQ (routine_version_id, due_on) |
| evaluation | jsonb; evidencia capturada al cerrar el ciclo |
| request_id | uuid NULL UQ, FK ai_integration.ai_generation_requests.id, ON DELETE RESTRICT |
| proposal_id | uuid NULL UQ, FK app.adaptation_proposals.id, ON DELETE RESTRICT |
| state | text DEFAULT PENDIENTE; CHECK PENDIENTE, GENERADA, NO_DISPONIBLE, OMITIDA |
| lease_until | timestamptz NULL; expiración del lease y orden de atención de ciclos pendientes |
| alerted_at | timestamptz NULL; evita repetir la alerta |
| last_error | text NULL |
| created_at | timestamptz DEFAULT CURRENT_TIMESTAMP |

Índice adicional: (state, lease_until). La tabla pertenece al backend: el rol IA no recibe acceso a `app`. El contexto y los resultados generativos siguen en las tablas de integración existentes.

## Extensión física de parámetros y regeneración, 2026-10-10

Las migraciones `20261010120000_generation_settings_and_trainer_regeneration` y `20261010121000_regeneration_sequence` agregan `app.gyms.generation_settings` (jsonb NULL) y `generation_settings_revision` (integer NOT NULL DEFAULT 0), y la tabla `app.routine_proposal_regenerations`. Comportamiento: [D5/§9.4](../domain/business-rules.md#94-parámetros-del-gimnasio-y-regeneración-por-entrenador).

| Columna | Tipo y restricciones |
| --- | --- |
| id | uuid PK, DEFAULT gen_random_uuid() |
| proposal_id | uuid, FK app.adaptation_proposals.id |
| trainer_id | uuid, FK app.users.id |
| sequence | integer DEFAULT 1; UQ (proposal_id, sequence) |
| idempotency_key | text UQ |
| feedback | text |
| candidate_request_id | uuid, FK ai_integration.ai_generation_requests.id |
| request_id | uuid NULL UQ, FK ai_integration.ai_generation_requests.id |
| state | text DEFAULT PENDIENTE; estados usados: PENDIENTE, COMPLETADA, NO_DISPONIBLE |
| error | text NULL |
| created_at / finished_at | timestamptz; created_at DEFAULT now(), finished_at NULL |

Las cuatro FK usan `NO ACTION` para borrado y actualización. Índice (proposal_id, created_at) e índice único parcial sobre proposal_id cuando state = PENDIENTE. La secuencia se asigna al reservar bajo bloqueo de la propuesta y define el orden aun si coinciden los instantes de creación. La tabla pertenece al backend y no concede acceso al rol IA.

## Uso por agentes

Este archivo es una proyección del esquema físico actual para implementar persistencia, DTO, validaciones y pantallas. No describe filas existentes, datos de seed, UUID concretos, credenciales ni URLs. Para reglas e invariantes usar [database-relational-model.md](database-relational-model.md), [domain-model.md](../domain/domain-model.md) y [business-rules.md](../domain/business-rules.md). Ante discrepancias, `prisma/schema.prisma` y las migraciones aplicadas determinan la estructura física; los documentos normativos determinan el comportamiento permitido.

Notación:

- `PK`: clave primaria.
- `FK target`: clave foránea al campo indicado.
- `NULL`: campo opcional; los demás campos son `NOT NULL`.
- `UQ`: restricción única.
- `DEFAULT x`: valor generado por la base o Prisma.
- `ON DELETE`: acción referencial.
- Los nombres son los nombres físicos PostgreSQL, no los nombres de modelos Prisma.
- `jsonb` exige un contrato validado por la aplicación; no implica contenido libre.

## Tipos enumerados

```yaml
app.GymAffiliationStatus: [AFFILIATED]
app.InvitationStatus: [VIGENTE, USADA, REVOCADA, CADUCADA]
app.UserRole: [ALUMNO, ENTRENADOR, ADMINISTRADOR]
app.UserState: [ACTIVO, SUSPENDIDO]
app.ConsentType: [DATOS_SALUD]
app.ExperienceLevel: [PRINCIPIANTE, INTERMEDIO, AVANZADO]
app.TrainingPurpose: [FUERZA, HIPERTROFIA, RESISTENCIA_MUSCULAR, ACONDICIONAMIENTO_GENERAL]
app.ConditionSeverity: [LEVE, MODERADA, SEVERA]
app.BodyMeasurementType: [PESO_CORPORAL, PERIMETRO_CINTURA, PERIMETRO_CADERA, PERIMETRO_BRAZO, PERIMETRO_MUSLO, PERIMETRO_PECHO]
app.MeasurementCheckpointResult: [CUMPLIDO, FALTA]
app.MeasurementBlockState: [PENDIENTE_MEDICION, PENDIENTE_APROBACION, RESUELTO]
app.MeasurementBlockReason: [TRES_FALTAS_CONSECUTIVAS]
app.MovementPattern: [EMPUJE_HORIZONTAL, EMPUJE_VERTICAL, TRACCION_HORIZONTAL, TRACCION_VERTICAL, DOMINANTE_RODILLA, DOMINANTE_CADERA, CORE, AISLAMIENTO_SUPERIOR, AISLAMIENTO_INFERIOR]
app.ExerciseOrigin: [CATALOGO_BASE, GIMNASIO]
app.ExerciseState: [PROPUESTO, APROBADO, RECHAZADO, DESACTIVADO]
app.ExerciseMediaPose: [INICIO, FINAL, PRINCIPAL]
app.MuscleParticipation: [PRIMARIA, SECUNDARIA]
app.RoutineOrigin: [PLANTILLA_ENTRENADOR, GENERADA]
app.RoutineState: [PROPUESTA, BLOQUEADA, VIGENTE, RECHAZADA, DESCARTADA, ARCHIVADA]
app.RoutineReviewResult: [APROBADA, APROBADA_CON_CAMBIOS, RECHAZADA]
app.CompatibilityState: [COMPATIBLE, ADVERTIDO, INCOMPATIBLE, EJERCICIO_DESACTIVADO]
app.TrainingSessionState: [EN_CURSO, COMPLETADA, ABANDONADA, BLOQUEADA]
app.NoticeType: [RUTINA_PROPUESTA_PENDIENTE, RUTINA_EN_VIGENCIA, RUTINA_RECHAZADA, RUTINA_AJUSTADA, PROPUESTA_PENDIENTE, RECORD_ALCANZADO, SENAL_DETECTADA, INCOMPATIBILIDAD_SOBREVENIDA, APTITUD_POR_VENCER]
app.EvolutionSituation: [DATOS_INSUFICIENTES, SOBREEXIGENCIA, PROGRESION_ADECUADA, ESTIMULO_INSUFICIENTE, ESTANCAMIENTO]
app.AdaptationProposalState: [PENDIENTE, BLOQUEADA, ACEPTADA_TOTAL, ACEPTADA_PARCIAL, RECHAZADA, INVALIDADA, CADUCADA]
app.AdjustmentType: [CARGA, VOLUMEN, ESQUEMA, SUSTITUCION, ESTRUCTURA]
app.ProposedAdjustmentState: [PENDIENTE, ACEPTADO, RECHAZADO]
app.PersonalRecordType: [CARGA_MAXIMA_ESTIMADA, CARGA_MOVILIZADA, REPETICIONES]
ai_integration.AiGenerationRequestState: [PENDIENTE, PROCESANDO, COMPLETADA, NO_DISPONIBLE, CANCELADA]
ai_integration.AiGenerationAttemptState: [PENDIENTE, PROCESANDO, COMPLETADO, FALLIDO, AGOTADO_POR_TIEMPO, SALIDA_INVALIDA]
```

## Esquema `app`

### Identidad, acceso y gimnasio

#### `app.gyms`

Propósito: organización que aísla usuarios, inventario, ejercicios propios y plantillas.

| Atributo | Tipo | Restricciones / semántica |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `name` | `text` | nombre del gimnasio |
| `timezone` | `text` | zona horaria IANA usada por reglas temporales |
| `affiliation_status` | `GymAffiliationStatus` | DEFAULT `AFFILIATED` |
| `inventory_revision` | `integer` | DEFAULT `0`; no negativa; cambia con el inventario |
| `active` | `boolean` | DEFAULT `true` |

#### `app.invitations`

Propósito: invitación nominal y temporal para crear un usuario con uno o más roles.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `gym_id` | `uuid` | FK `app.gyms.id`, ON DELETE RESTRICT |
| `issued_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `email_normalized` | `text` | correo normalizado; dato personal |
| `status` | `InvitationStatus` | DEFAULT `VIGENTE` |
| `issued_at` | `timestamptz(6)` | DEFAULT `now()` |
| `expires_at` | `timestamptz(6)` | vencimiento |

Índices: `(gym_id, status)`, `(email_normalized)`.

#### `app.invitation_roles`

Propósito: roles autorizados por una invitación.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `invitation_id` | `uuid` | PK parcial, FK `app.invitations.id`, ON DELETE CASCADE |
| `role` | `UserRole` | PK parcial |

PK compuesta: `(invitation_id, role)`.

#### `app.users`

Propósito: identidad local de una persona dentro de un gimnasio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `gym_id` | `uuid` | FK `app.gyms.id`, ON DELETE RESTRICT |
| `invitation_id` | `uuid` | NULL, UQ, FK `app.invitations.id`, ON DELETE RESTRICT |
| `email_normalized` | `text` | dato personal; UQ junto con `gym_id` |
| `display_name` | `text` | dato personal visible |
| `password_hash` | `text` | credencial derivada; nunca exponer en API, logs o frontend |
| `state` | `UserState` | DEFAULT `ACTIVO` |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |

Único: `(gym_id, email_normalized)`. Índice: `(gym_id, state)`.

#### `app.user_roles`

Propósito: roles vigentes de un usuario; un usuario puede tener más de uno.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `user_id` | `uuid` | PK parcial, FK `app.users.id`, ON DELETE CASCADE |
| `role` | `UserRole` | PK parcial |

PK compuesta: `(user_id, role)`.

#### `app.consents`

Propósito: historial de aceptación o rechazo de consentimientos versionado por texto.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `type` | `ConsentType` | tipo de consentimiento |
| `granted` | `boolean` | decisión registrada |
| `accepted_text` | `text` | texto exacto presentado al usuario |
| `recorded_at` | `timestamptz(6)` | DEFAULT `now()` |

Índice: `(user_id, type, recorded_at)`.

#### `app.auth_sessions`

Propósito: sesiones propias de autenticación.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `user_id` | `uuid` | FK `app.users.id`, ON DELETE CASCADE |
| `token_hash` | `text` | UQ; secreto derivado, nunca exponer |
| `last_activity_at` | `timestamptz(6)` | DEFAULT `now()` |
| `expires_at` | `timestamptz(6)` | vencimiento absoluto |
| `revoked_at` | `timestamptz(6)` | NULL; revocación lógica |

Índice: `(user_id, expires_at)`.

#### `app.password_reset_tokens`

Propósito: tokens de recuperación de contraseña de un solo uso.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `user_id` | `uuid` | FK `app.users.id`, ON DELETE CASCADE |
| `token_hash` | `text` | UQ; secreto derivado, nunca exponer |
| `expires_at` | `timestamptz(6)` | vencimiento |
| `used_at` | `timestamptz(6)` | NULL; consumo del token |

Índice: `(user_id, expires_at)`.

### Perfiles y estado del alumno

#### `app.student_profiles`

Propósito: atributos del alumno que condicionan la prescripción.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `user_id` | `uuid` | PK, FK `app.users.id`, ON DELETE RESTRICT |
| `birth_date` | `date` | dato personal |
| `sex` | `text` | dato personal usado por perfil |
| `height_cm` | `decimal(5,2)` | altura en centímetros |
| `height_updated_at` | `timestamptz(6)` | DEFAULT `now()`; instante de la última confirmación de altura |
| `experience_level` | `ExperienceLevel` | nivel vigente |
| `available_days_per_week` | `integer` | disponibilidad semanal |

Relación `users 1 — 0..1 student_profiles`.

#### `app.trainer_profiles`

Propósito: información profesional del usuario entrenador.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `user_id` | `uuid` | PK, FK `app.users.id`, ON DELETE RESTRICT |
| `specialty` | `text` | especialidad declarada |
| `experience_years` | `integer` | años de experiencia |
| `presentation` | `text` | descripción pública |

Relación `users 1 — 0..1 trainer_profiles`.

#### `app.goals`

Propósito: períodos de objetivos de entrenamiento de un alumno.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `type` | `TrainingPurpose` | objetivo |
| `starts_on` | `date` | inicio inclusivo |
| `ends_on` | `date` | NULL; fin del objetivo |

Índice: `(student_id, starts_on)`. La base restringe a un objetivo vigente por alumno mediante índice parcial.

#### `app.physical_conditions`

Propósito: limitaciones físicas declaradas para una zona corporal y período.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `body_zone_code` | `text` | código del vocabulario de zonas corporales; no tiene FK física |
| `severity` | `ConditionSeverity` | severidad |
| `description` | `text` | NULL; dato de salud sensible |
| `starts_on` | `date` | inicio inclusivo |
| `ends_on` | `date` | NULL; fin de vigencia |

Índice: `(student_id, starts_on)`.

#### `app.fitness_clearances`

Propósito: constancias de aptitud física registradas para un alumno.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `recorded_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `issued_on` | `date` | fecha de emisión |
| `expires_on` | `date` | fecha de vencimiento |
| `observation` | `text` | NULL; dato de salud sensible |

Índice: `(student_id, expires_on)`.

#### `app.body_measurements`

Propósito: serie temporal de mediciones corporales.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `type` | `BodyMeasurementType` | magnitud medida |
| `value` | `decimal(10,2)` | valor numérico |
| `measured_on` | `date` | fecha de medición |

Único: `(student_id, type, measured_on)`.

#### `app.student_measurement_checkpoints`

Propósito: resultado inmutable del control de peso y altura al cerrar cada ciclo de 60 días.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `routine_id` | `uuid` | FK `app.routines.id`, ON DELETE RESTRICT |
| `routine_version_id` | `uuid` | FK `app.routine_versions.id`, ON DELETE RESTRICT |
| `cycle_starts_on` | `date` | inicio exclusivo para la evidencia del ciclo |
| `due_on` | `date` | vencimiento inclusivo; debe ser inicio + 60 días |
| `result` | `MeasurementCheckpointResult` | `CUMPLIDO` exige ambas evidencias; `FALTA` exige que falte al menos una |
| `weight_measurement_id` | `uuid` | NULL, UQ, FK `app.body_measurements.id`, ON DELETE RESTRICT |
| `height_confirmed_at` | `timestamptz(6)` | NULL; confirmación dentro del ciclo |
| `evaluated_at` | `timestamptz(6)` | DEFAULT `now()` |

Único: `(student_id, due_on)`. Índices: `(student_id, evaluated_at)`, `(result, due_on)`. Triggers validan alumno, rutina, versión y evidencia del ciclo, y rechazan toda actualización o eliminación.

#### `app.student_measurement_blocks`

Propósito: historial del bloqueo funcional causado por tres faltas consecutivas y de su regularización.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `state` | `MeasurementBlockState` | DEFAULT `PENDIENTE_MEDICION` |
| `reason` | `MeasurementBlockReason` | DEFAULT `TRES_FALTAS_CONSECUTIVAS` |
| `consecutive_misses_at_block` | `integer` | mínimo 3 |
| `triggering_checkpoint_id` | `uuid` | UQ, FK `app.student_measurement_checkpoints.id`, ON DELETE RESTRICT |
| `blocked_at` | `timestamptz(6)` | DEFAULT `now()` |
| `regularization_weight_measurement_id` | `uuid` | NULL, UQ, FK `app.body_measurements.id`, ON DELETE RESTRICT |
| `regularization_height_confirmed_at` | `timestamptz(6)` | NULL; posterior al bloqueo |
| `submitted_at` | `timestamptz(6)` | NULL |
| `approved_by_trainer_id` | `uuid` | NULL, FK `app.trainer_profiles.user_id`, ON DELETE RESTRICT |
| `approved_at` | `timestamptz(6)` | NULL; nueva línea de base al resolver |

Índices: `(student_id, state)`, `(approved_by_trainer_id, approved_at)`. Un índice parcial admite como máximo un bloqueo no resuelto por alumno. Checks y trigger exigen los datos correspondientes a cada estado, transiciones hacia adelante y asignación vigente al aprobar.

#### `app.trainer_student_assignments`

Propósito: historial de asignaciones entre entrenador y alumno.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `trainer_id` | `uuid` | FK `app.trainer_profiles.user_id`, ON DELETE RESTRICT |
| `starts_at` | `timestamptz(6)` | inicio |
| `ends_at` | `timestamptz(6)` | NULL; fin; NULL significa vigente |
| `started_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `ended_by_user_id` | `uuid` | NULL, FK `app.users.id`, ON DELETE RESTRICT |

Índices: `(student_id, starts_at)`, `(trainer_id, starts_at)`. La base restringe a una asignación vigente por alumno mediante índice parcial.

### Inventario y catálogo

#### `app.equipment`

Propósito: catálogo de tipos de equipamiento.

| Atributo | Tipo | Restricciones / semántica |
| --- | --- | --- |
| `code` | `text` | PK; código estable |
| `name` | `text` | UQ; etiqueta visible |
| `display_order` | `integer` | UQ; orden de presentación |

#### `app.muscle_groups`

Propósito: taxonomía canónica de grupos musculares.

| Atributo | Tipo | Restricciones / semántica |
| --- | --- | --- |
| `code` | `text` | PK; código estable |
| `name` | `text` | UQ; etiqueta visible |
| `region` | `text` | región corporal |
| `display_order` | `integer` | UQ; orden de presentación |

#### `app.joints`

Propósito: taxonomía canónica de articulaciones.

| Atributo | Tipo | Restricciones / semántica |
| --- | --- | --- |
| `code` | `text` | PK; código estable |
| `name` | `text` | UQ; etiqueta visible |
| `region` | `text` | región corporal |
| `display_order` | `integer` | UQ; orden de presentación |

#### `app.gym_equipment`

Propósito: inventario declarado por cada gimnasio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `gym_id` | `uuid` | PK parcial, FK `app.gyms.id`, ON DELETE RESTRICT |
| `equipment_code` | `text` | PK parcial, FK `app.equipment.code`, ON DELETE RESTRICT |
| `present` | `boolean` | DEFAULT `true` |
| `updated_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `updated_at` | `timestamptz(6)` | actualizado automáticamente |

PK compuesta: `(gym_id, equipment_code)`.

#### `app.exercises`

Propósito: catálogo base compartido y catálogo propio de cada gimnasio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `gym_id` | `uuid` | NULL, FK `app.gyms.id`, ON DELETE RESTRICT; NULL para catálogo base |
| `author_user_id` | `uuid` | NULL, FK `app.users.id`, ON DELETE RESTRICT |
| `name` | `text` | nombre visible |
| `instructions` | `text` | instrucciones de ejecución |
| `movement_pattern` | `MovementPattern` | patrón mecánico |
| `difficulty_level` | `ExperienceLevel` | dificultad mínima |
| `unilateral` | `boolean` | DEFAULT `false` |
| `visual_resource_url` | `text` | referencia al recurso visual |
| `origin` | `ExerciseOrigin` | catálogo base o gimnasio |
| `state` | `ExerciseState` | DEFAULT `APROBADO` para filas existentes; las altas propias usan `PROPUESTO` |
| `revision` | `integer` | DEFAULT `1`; positiva |
| `source`, `source_id` | `text` | NULL; ambos presentes o ambos ausentes; UQ del par |
| `source_revision` | `text` | NULL; hash material de la ficha importada |
| `description` | `text` | NULL; descripción |
| `tips` | `text[]` | DEFAULT `[]` |
| `reviewed_by_user_id` | `uuid` | NULL, FK `app.users.id`, ON DELETE RESTRICT |
| `reviewed_at` | `timestamptz(6)` | NULL; instante de revisión |
| `review_observation` | `text` | NULL; decisión o procedencia de revisión |
| `created_at`, `updated_at` | `timestamptz(6)` | creación y actualización |

Índices: `(gym_id)`, `(movement_pattern, difficulty_level)`, `(state, origin)`. La base conserva unicidad de nombre normalizado sólo para ejercicios propios del mismo gimnasio. El catálogo importado usa identidad `(source, source_id)`.

#### `app.gym_exercises`

Propósito: disponibilidad explícita por gimnasio; no implica compatibilidad con un alumno.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `gym_id`, `exercise_id` | `uuid` | PK compuesta; FK a `app.gyms.id` y `app.exercises.id`, ON DELETE RESTRICT |
| `enabled` | `boolean` | DEFAULT `false` |
| `revision` | `integer` | DEFAULT `1`; positiva |
| `updated_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `updated_at` | `timestamptz(6)` | actualización |

Índice `(gym_id, enabled)`. Triggers validan actor del gimnasio, ámbito de la ficha y estado aprobado al habilitar. Las revisiones se incrementan sin eliminar la fila al deshabilitar.

#### `app.exercise_media`

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE CASCADE |
| `position` | `integer` | positiva; UQ `(exercise_id, position)` |
| `pose` | `ExerciseMediaPose` | inicio, final o principal |
| `url` | `text` | ubicación propia versionada o HTTPS de ficha propia |

#### `app.exercise_equipment`

Propósito: equipamiento requerido por un ejercicio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `exercise_id` | `uuid` | PK parcial, FK `app.exercises.id`, ON DELETE CASCADE |
| `equipment_code` | `text` | PK parcial, FK `app.equipment.code`, ON DELETE RESTRICT |

PK compuesta: `(exercise_id, equipment_code)`.

#### `app.exercise_muscles`

Propósito: participación muscular primaria o secundaria de un ejercicio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `exercise_id` | `uuid` | PK parcial, FK `app.exercises.id`, ON DELETE CASCADE |
| `muscle_code` | `text` | PK parcial, FK `app.muscle_groups.code`, ON DELETE RESTRICT |
| `participation` | `MuscleParticipation` | clasificación |

PK compuesta: `(exercise_id, muscle_code)`. Admite varios músculos primarios; un mismo músculo sólo tiene una participación por ficha.

#### `app.exercise_joints`

Propósito: articulaciones exigidas por un ejercicio.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `exercise_id` | `uuid` | PK parcial, FK `app.exercises.id`, ON DELETE CASCADE |
| `joint_code` | `text` | PK parcial, FK `app.joints.code`, ON DELETE RESTRICT |

PK compuesta: `(exercise_id, joint_code)`.

### Plantillas y rutinas

#### `app.routine_templates`

Propósito: estructura reutilizable privada creada por un entrenador.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `gym_id` | `uuid` | FK `app.gyms.id`, ON DELETE RESTRICT |
| `author_trainer_id` | `uuid` | FK `app.trainer_profiles.user_id`, ON DELETE RESTRICT |
| `name` | `text` | nombre visible |
| `routine_type` | `TrainingPurpose` | tipo de entrenamiento |
| `active` | `boolean` | DEFAULT `true`; baja lógica |

Índices: `(gym_id, active)`, `(author_trainer_id)`.

#### `app.template_days`

Propósito: días ordenados de una plantilla; no representan fechas calendario.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `template_id` | `uuid` | FK `app.routine_templates.id`, ON DELETE CASCADE |
| `position` | `integer` | UQ junto con `template_id` |
| `name` | `text` | etiqueta visible |

Único: `(template_id, position)`.

#### `app.template_exercises`

Propósito: ejercicios ordenados de un día de plantilla.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `template_day_id` | `uuid` | FK `app.template_days.id`, ON DELETE CASCADE |
| `exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE RESTRICT |
| `position` | `integer` | UQ junto con `template_day_id` |
| `note` | `text` | NULL; indicación opcional |

Único: `(template_day_id, position)`. Índice: `(exercise_id)`.

#### `app.template_sets`

Propósito: series prescriptas dentro de un ejercicio de plantilla.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `template_exercise_id` | `uuid` | FK `app.template_exercises.id`, ON DELETE CASCADE |
| `position` | `integer` | UQ junto con `template_exercise_id` |
| `min_repetitions` | `integer` | límite inferior |
| `max_repetitions` | `integer` | límite superior |
| `suggested_load` | `decimal(10,2)` | NULL; carga sugerida opcional (RN-43) |
| `rest_seconds` | `integer` | descanso |
| `warmup` | `boolean` | DEFAULT `false` |

Único: `(template_exercise_id, position)`.

#### `app.routines`

Propósito: prescripción asociada a un alumno, con procedencia y estado de aprobación.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `source_template_id` | `uuid` | NULL, FK `app.routine_templates.id`, ON DELETE RESTRICT |
| `source_generation_result_id` | `uuid` | NULL, UQ, FK `ai_integration.ai_generation_results.id`, ON DELETE RESTRICT |
| `routine_type` | `TrainingPurpose` | tipo de entrenamiento |
| `target_weekly_frequency` | `integer` | sesiones objetivo por semana |
| `state` | `RoutineState` | ciclo de vida de la rutina |
| `origin` | `RoutineOrigin` | determina qué fuente debe existir |
| `requested_by_user_id` | `uuid` | NULL, FK `app.users.id`, ON DELETE RESTRICT |
| `requested_at` | `timestamptz(6)` | DEFAULT `now()` |

Índices: `(student_id, state)`, `(source_template_id)`. La base restringe a una rutina `PROPUESTA` y una `VIGENTE` por alumno mediante índices parciales independientes.

#### `app.routine_reviews`

Propósito: decisión de un entrenador sobre una versión de rutina propuesta.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `routine_id` | `uuid` | FK `app.routines.id`, ON DELETE RESTRICT |
| `reviewed_version_id` | `uuid` | FK `app.routine_versions.id`, ON DELETE RESTRICT |
| `reviewer_trainer_id` | `uuid` | FK `app.trainer_profiles.user_id`, ON DELETE RESTRICT |
| `result` | `RoutineReviewResult` | resultado |
| `observation` | `text` | NULL |
| `reviewed_at` | `timestamptz(6)` | DEFAULT `now()` |

Índices: `(routine_id, reviewed_at)`, `(reviewer_trainer_id, reviewed_at)`.

#### `app.routine_versions`

Propósito: copia inmutable de la estructura completa de una rutina.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `routine_id` | `uuid` | FK `app.routines.id`, ON DELETE RESTRICT |
| `version_number` | `integer` | número secuencial dentro de la rutina |
| `current` | `boolean` | DEFAULT `false` |
| `created_by_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `adaptation_proposal_id` | `uuid` | NULL, UQ, FK `app.adaptation_proposals.id`, ON DELETE RESTRICT |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |

Único: `(routine_id, version_number)`. La base restringe a una versión actual por rutina mediante índice parcial.

#### `app.routine_days`

Propósito: días ordenados de una versión de rutina.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `routine_version_id` | `uuid` | FK `app.routine_versions.id`, ON DELETE CASCADE |
| `position` | `integer` | posición dentro de la versión |
| `name` | `text` | etiqueta visible |
| `dominant_pattern` | `MovementPattern` | patrón dominante |

Único: `(routine_version_id, position)`.

#### `app.routine_exercises`

Propósito: ejercicios ordenados de un día y resultado de compatibilidad al prescribir.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `routine_day_id` | `uuid` | FK `app.routine_days.id`, ON DELETE CASCADE |
| `exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE RESTRICT |
| `position` | `integer` | posición dentro del día |
| `note` | `text` | NULL |
| `compatibility_state` | `CompatibilityState` | DEFAULT `COMPATIBLE` |
| `compatibility_reason` | `text` | NULL; justificación de advertencia o incompatibilidad |

Único: `(routine_day_id, position)`. Índice: `(exercise_id)`.

#### `app.prescribed_sets`

Propósito: series prescriptas de un ejercicio en una versión de rutina.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `routine_exercise_id` | `uuid` | FK `app.routine_exercises.id`, ON DELETE CASCADE |
| `position` | `integer` | posición dentro del ejercicio |
| `min_repetitions` | `integer` | límite inferior |
| `max_repetitions` | `integer` | límite superior |
| `suggested_load` | `decimal(10,2)` | NULL; carga sugerida opcional (RN-43) |
| `rest_seconds` | `integer` | descanso |
| `warmup` | `boolean` | DEFAULT `false` |

Único: `(routine_exercise_id, position)`.

### Ejecución de entrenamiento

#### `app.training_sessions`

Propósito: ocurrencia concreta de un entrenamiento sobre una versión y día determinados.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `routine_id` | `uuid` | FK `app.routines.id`, ON DELETE RESTRICT |
| `routine_version_id` | `uuid` | FK `app.routine_versions.id`, ON DELETE RESTRICT |
| `routine_day_id` | `uuid` | FK `app.routine_days.id`, ON DELETE RESTRICT |
| `state` | `TrainingSessionState` | DEFAULT `EN_CURSO` |
| `started_at` | `timestamptz(6)` | DEFAULT `now()` |
| `completed_at` | `timestamptz(6)` | NULL |
| `occurred_on` | `date` | fecha local del entrenamiento |
| `simulated` | `boolean` | DEFAULT `false`; identifica datos no reales de prueba |

Índices: `(student_id, occurred_on)`, `(routine_id)`, `(routine_version_id)`. La base restringe a una sesión `EN_CURSO` por alumno mediante índice parcial.

#### `app.session_set_records`

Propósito: prescripción congelada y ejecución real de cada serie de una sesión.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `session_id` | `uuid` | FK `app.training_sessions.id`, ON DELETE CASCADE |
| `position` | `integer` | orden global dentro de la sesión |
| `prescribed_exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE RESTRICT |
| `performed_exercise_id` | `uuid` | NULL, FK `app.exercises.id`, ON DELETE RESTRICT; sustitución efectiva |
| `prescribed_min_repetitions` | `integer` | snapshot del mínimo |
| `prescribed_max_repetitions` | `integer` | snapshot del máximo |
| `prescribed_load` | `decimal(10,2)` | NULL; snapshot de carga; no especificada es diferente de cero |
| `warmup` | `boolean` | DEFAULT `false` |
| `performed_load` | `decimal(10,2)` | NULL; carga ejecutada |
| `performed_repetitions` | `integer` | NULL; repeticiones ejecutadas |
| `perceived_effort` | `integer` | NULL; escala 1–10 |
| `completed` | `boolean` | DEFAULT `false` |
| `additional` | `boolean` | DEFAULT `false`; serie no prescripta originalmente |
| `omission_reason` | `text` | NULL |
| `atypical_confirmed` | `boolean` | DEFAULT `false` |

Único: `(session_id, position)`. Índices: `(prescribed_exercise_id)`, `(performed_exercise_id)`.

### Avisos y auditoría

#### `app.notices`

Propósito: avisos persistentes dirigidos a un usuario.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `recipient_user_id` | `uuid` | FK `app.users.id`, ON DELETE CASCADE |
| `type` | `NoticeType` | tipo funcional |
| `reference_type` | `text` | discriminador de referencia polimórfica; sin FK física |
| `reference_id` | `uuid` | identificador de referencia polimórfica; sin FK física |
| `text` | `text` | contenido mostrado |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |
| `read_at` | `timestamptz(6)` | NULL |
| `expired` | `boolean` | DEFAULT `false` |

Índices: `(recipient_user_id, expired, created_at)`, `(reference_type, reference_id)`.

#### `app.audit_logs`

Propósito: auditoría append-only de operaciones sensibles.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `actor_user_id` | `uuid` | FK `app.users.id`, ON DELETE RESTRICT |
| `operation` | `text` | operación auditada |
| `entity_type` | `text` | discriminador polimórfico; sin FK física |
| `entity_id` | `uuid` | entidad afectada; sin FK física |
| `previous_value` | `jsonb` | NULL; snapshot previo sanitizado |
| `new_value` | `jsonb` | NULL; snapshot posterior sanitizado |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |

Índices: `(entity_type, entity_id, created_at)`, `(actor_user_id, created_at)`.

### Evolución, adaptación y récords

#### `app.evolution_diagnostics`

Propósito: diagnóstico versionado del desempeño de un alumno en un período.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `routine_version_id` | `uuid` | FK `app.routine_versions.id`, ON DELETE RESTRICT |
| `period_start` | `date` | inicio del período |
| `period_end` | `date` | fin del período |
| `global_situation` | `EvolutionSituation` | clasificación global |
| `adherence` | `decimal(5,2)` | NULL; porcentaje calculado |
| `component_version` | `text` | versión del componente que calculó el diagnóstico |
| `criteria_not_evaluated` | `jsonb` | criterios omitidos y motivos; contrato de aplicación |
| `calculated_at` | `timestamptz(6)` | DEFAULT `now()` |

Índices: `(student_id, period_end)`, `(routine_version_id, calculated_at)`.

#### `app.exercise_diagnostics`

Propósito: detalle por ejercicio de un diagnóstico de evolución.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `diagnostic_id` | `uuid` | FK `app.evolution_diagnostics.id`, ON DELETE RESTRICT |
| `exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE RESTRICT |
| `situation` | `EvolutionSituation` | clasificación del ejercicio |
| `metrics` | `jsonb` | métricas calculadas; contrato de aplicación |

Único: `(diagnostic_id, exercise_id)`. Índice: `(exercise_id)`.

#### `app.adaptation_proposals`

Propósito: propuesta de cambio derivada de un diagnóstico y resuelta por un entrenador.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `diagnostic_id` | `uuid` | UQ, FK `app.evolution_diagnostics.id`, ON DELETE RESTRICT |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `state` | `AdaptationProposalState` | DEFAULT `PENDIENTE` |
| `resolved_by_trainer_id` | `uuid` | NULL, FK `app.trainer_profiles.user_id`, ON DELETE RESTRICT |
| `resulting_version_id` | `uuid` | NULL, UQ, FK `app.routine_versions.id`, ON DELETE RESTRICT |
| `resolution_reason` | `text` | NULL |
| `component_version` | `text` | versión del componente proponente |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |
| `resolved_at` | `timestamptz(6)` | NULL |

Índices: `(student_id, state, created_at)`, `(resolved_by_trainer_id)`.

#### `app.proposed_adjustments`

Propósito: cambio atómico incluido en una propuesta de adaptación.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `proposal_id` | `uuid` | FK `app.adaptation_proposals.id`, ON DELETE RESTRICT |
| `routine_exercise_id` | `uuid` | NULL, FK `app.routine_exercises.id`, ON DELETE RESTRICT |
| `type` | `AdjustmentType` | clase de cambio |
| `previous_value` | `jsonb` | valor estructurado anterior |
| `proposed_value` | `jsonb` | valor estructurado propuesto |
| `criterion` | `text` | criterio que justifica el cambio |
| `supporting_data` | `jsonb` | evidencia estructurada |
| `state` | `ProposedAdjustmentState` | DEFAULT `PENDIENTE` |

Índices: `(proposal_id, state)`, `(routine_exercise_id)`.

#### `app.personal_records`

Propósito: historial de récords personales derivados de sesiones.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `student_id` | `uuid` | FK `app.student_profiles.user_id`, ON DELETE RESTRICT |
| `exercise_id` | `uuid` | FK `app.exercises.id`, ON DELETE RESTRICT |
| `session_id` | `uuid` | FK `app.training_sessions.id`, ON DELETE RESTRICT |
| `type` | `PersonalRecordType` | métrica del récord |
| `value` | `decimal(12,2)` | valor calculado |
| `achieved_on` | `date` | fecha de logro |
| `current` | `boolean` | DEFAULT `true` |

Índices: `(student_id, exercise_id, type, achieved_on)`, `(session_id)`.

## Esquema `ai_integration`

Este esquema es la interfaz durable entre backend y servicio IA. No contiene usuarios ni datos identificatorios. El frontend no lo consulta directamente.

#### `ai_integration.ai_generation_requests`

Propósito: trabajo asíncrono e idempotente solicitado por backend.

| Atributo | Tipo | Restricciones / semántica |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `idempotency_key` | `text` | UQ |
| `state` | `AiGenerationRequestState` | DEFAULT `PENDIENTE` |
| `minimized_context` | `jsonb` | contexto versionado y sin datos identificatorios |
| `preferences` | `jsonb` | preferencias versionadas y sanitizadas |
| `context_hash` | `text` | integridad/deduplicación del contexto |
| `available_at` | `timestamptz(6)` | DEFAULT `now()`; elegibilidad para procesamiento |
| `lease_owner` | `text` | NULL; worker que reclamó el trabajo |
| `lease_until` | `timestamptz(6)` | NULL; vencimiento del lease |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |
| `finished_at` | `timestamptz(6)` | NULL |
| `retention_until` | `timestamptz(6)` | fecha de purga |

Índices: `(state, available_at)`, `(retention_until)`.

#### `ai_integration.ai_generation_attempts`

Propósito: cada intento de procesamiento de una solicitud.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `request_id` | `uuid` | FK `ai_integration.ai_generation_requests.id`, ON DELETE CASCADE |
| `attempt_number` | `integer` | secuencia dentro de la solicitud |
| `state` | `AiGenerationAttemptState` | DEFAULT `PENDIENTE` |
| `started_at` | `timestamptz(6)` | NULL |
| `finished_at` | `timestamptz(6)` | NULL |
| `error_code` | `text` | NULL; código técnico no sensible |
| `model_version` | `text` | NULL; versión del LLM |
| `configuration_version` | `text` | NULL; versión de configuración |
| `contract_version` | `text` | versión del contrato JSON |
| `input_hash` | `text` | hash de entrada |

Único: `(request_id, attempt_number)`. Índice: `(state, started_at)`.

#### `ai_integration.ai_generation_results`

Propósito: salida estructurada producida por un intento.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `attempt_id` | `uuid` | UQ, FK `ai_integration.ai_generation_attempts.id`, ON DELETE CASCADE |
| `structured_output` | `jsonb` | salida versionada; debe validarse antes de crear una rutina |
| `output_hash` | `text` | hash de salida |
| `structurally_valid` | `boolean` | resultado de validación estructural inicial |
| `created_at` | `timestamptz(6)` | DEFAULT `now()` |
| `retention_until` | `timestamptz(6)` | fecha de purga |

Índice: `(retention_until)`. Relación inversa opcional 1:1 con `app.routines.source_generation_result_id`.

#### `ai_integration.ai_result_validations`

Propósito: historial de validaciones determinísticas ejecutadas por backend sobre un resultado.

| Atributo | Tipo | Restricciones / relación |
| --- | --- | --- |
| `id` | `uuid` | PK, generado |
| `result_id` | `uuid` | FK `ai_integration.ai_generation_results.id`, ON DELETE CASCADE |
| `validator_version` | `text` | versión del validador |
| `valid` | `boolean` | resultado |
| `violations` | `jsonb` | lista estructurada de incumplimientos |
| `validated_at` | `timestamptz(6)` | DEFAULT `now()` |

Índice: `(result_id, validated_at)`.

## Grafo de relaciones para joins

```text
app.gyms
  -> app.invitations, app.users, app.gym_equipment, app.exercises, app.routine_templates
app.invitations
  -> app.invitation_roles
  -> app.users (users.invitation_id, opcional 1:1)
app.users
  -> app.user_roles, app.consents, app.auth_sessions, app.password_reset_tokens
  -> app.student_profiles (opcional 1:1), app.trainer_profiles (opcional 1:1)
app.student_profiles
  -> app.goals, app.physical_conditions, app.fitness_clearances, app.body_measurements
  -> app.student_measurement_checkpoints, app.student_measurement_blocks
  -> app.trainer_student_assignments, app.routines, app.training_sessions
  -> app.evolution_diagnostics, app.adaptation_proposals, app.personal_records
app.trainer_profiles
  -> app.trainer_student_assignments, app.routine_templates, app.routine_reviews
  -> app.adaptation_proposals (resolved_by_trainer_id)
app.equipment <-> app.exercises through app.exercise_equipment
app.muscle_groups <-> app.exercises through app.exercise_muscles
app.joints <-> app.exercises through app.exercise_joints
app.routine_templates
  -> app.template_days -> app.template_exercises -> app.template_sets
app.routine_templates -> app.routines (source_template_id, opcional)
app.routines
  -> app.routine_versions -> app.routine_days -> app.routine_exercises -> app.prescribed_sets
  -> app.routine_reviews, app.training_sessions
app.training_sessions -> app.session_set_records, app.personal_records
app.evolution_diagnostics -> app.exercise_diagnostics
app.evolution_diagnostics -> app.adaptation_proposals (opcional 1:1)
app.adaptation_proposals -> app.proposed_adjustments
app.adaptation_proposals <-> app.routine_versions through resulting_version_id/adaptation_proposal_id
ai_integration.ai_generation_requests
  -> ai_integration.ai_generation_attempts
  -> ai_integration.ai_generation_results
  -> ai_integration.ai_result_validations
ai_integration.ai_generation_results -> app.routines (opcional 1:1 de procedencia)
```

## Límites de consumo

- Frontend consume DTO del backend; nunca consulta PostgreSQL, Prisma ni `ai_integration`.
- Backend es propietario de `app` y de la creación/validación de solicitudes y resultados IA.
- Servicio IA accede sólo a las operaciones autorizadas de `ai_integration`; no recibe acceso general a `app`.
- `password_hash`, `token_hash`, datos personales, datos de salud y JSON de auditoría nunca se incluyen automáticamente en DTO.
- Relaciones polimórficas (`notices.reference_*`, `audit_logs.entity_*`) requieren validación de aplicación porque no poseen FK física.
- Toda consulta de dominio debe aplicar aislamiento por gimnasio mediante la relación con `users.gym_id` o `gyms.id`, aunque una tabla hija no repita `gym_id`.

## Migraciones del catálogo, 2026-10-07

`20261006010000_exercise_catalog_availability` agrega campos, habilitaciones, media y validación de ámbito; retira unicidad de nombre base y el índice de un único primario. `20261006010100_catalog_optimistic_revisions` agrega revisiones de inventario y habilitaciones. `20261006010200_ai_prescription_storage_constraints` retira frecuencia dependiente del tipo, máximo de carga 1.000 y máximo de repeticiones ejecutadas 100. Conserva frecuencia de calendario 1–7, valores no negativos/positivos, intervalos ordenados y capacidad física de `integer`/`numeric(10,2)`. No se modificaron migraciones anteriores ni se habilitaron filas automáticamente.

`20261007010000_optional_session_prescribed_load` conserva la carga prescripta no especificada al copiarla a `session_set_records.prescribed_load`: columna nullable, sin transformar valores históricos.
