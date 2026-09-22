# Secuencias de la implementación actual

```yaml
document_id: ARCH-IMPLEMENTED-SEQUENCES
status: as-built-reference
snapshot_date: 2026-09-21
branches_reviewed:
  frontend: develop
  backend: develop
  ai: develop
normative: false
contains_future_design: false
```

## Propósito y regla de lectura

Este documento permite construir o renderizar diagramas de secuencia de lo que existe en el código actual. No sustituye los flujos funcionales normativos de [functional-flows.md](../flows/functional-flows.md) ni afirma que una tabla existente equivalga a una funcionalidad implementada.

Clasificación usada:

- `E2E`: existe recorrido frontend → backend → PostgreSQL y está expuesto en una pantalla funcional.
- `API`: existe en backend pero frontend no lo consume.
- `COMPONENTE`: existe de forma aislada, pero no completa un recorrido entre repositorios.
- `ROTO`: los componentes existen, pero sus contratos actuales no son compatibles.
- No se documentan como implementadas las pantallas `PlaceholderPage`, los datos visuales hardcodeados ni las tablas sin endpoint/caso de uso.

## Participantes comunes

```text
Usuario        persona que opera la SPA o un cliente HTTP
Frontend       React + TanStack Query + Zod
API            Express; controllers y middleware HTTP
Auth           sesión propia mediante cookie httpOnly y roles persistidos
UseCase        caso de uso de aplicación del backend
Repository     adaptador Prisma del backend
DB             Neon PostgreSQL; schemas app y ai_integration
AI API         FastAPI desplegada en Vercel
Queue          Vercel Queues
Worker         consumidor Python de generación
LLM            Ollama en el Polo mediante Cloudflare Tunnel
LocalStorage   estado local del navegador; no es fuente de verdad de negocio
```

La autenticación pública usa sesiones propias. El frontend nunca elige ni simula una identidad: inicia sesión, conserva sólo la identidad pública en TanStack Query y envía la cookie `httpOnly` mediante `credentials: include`. Backend resuelve usuario, gimnasio y roles desde `auth_sessions`; las cabeceras `x-user-*` quedan limitadas al proceso de pruebas automatizadas (`NODE_ENV=test`). La autenticación backend–IA usa un secreto de servicio independiente y nunca debe originarse en frontend.

## Matriz de cobertura

| ID | Secuencia | Estado | Entrada frontend |
| --- | --- | --- | --- |
| SEQ-00 | Iniciar, recuperar y cerrar sesión | E2E | `/ingresar` y guardas de rutas |
| SEQ-01 | Consultar rutina vigente y aviso de renovación | E2E | `/alumno` |
| SEQ-02 | Consultar cartera priorizada del entrenador | E2E | `/entrenador`, `/entrenador/alumnos`, `/entrenador/rutinas` |
| SEQ-03 | Consultar ficha y rutina resumida de un alumno | E2E | `/entrenador/alumnos/:studentId` |
| SEQ-04 | Desbloquear alumno con medición adeudada | E2E | ficha del alumno bloqueado |
| SEQ-05 | Listar y abrir propuestas de adaptación | E2E | `/entrenador/rutinas/revisar` |
| SEQ-06 | Resolver propuesta de adaptación | E2E | `/entrenador/rutinas/revisar/:proposalId` |
| SEQ-07 | Evaluar y aplicar bloqueo por inactividad | API | sin pantalla |
| SEQ-08 | Consultar y finalizar una generación | E2E | ficha del alumno del entrenador |
| SEQ-09 | Solicitar generación desde backend | E2E | ficha del alumno del entrenador |
| SEQ-10 | Despachar y procesar generación dentro de IA | COMPONENTE | no accesible desde frontend |
| SEQ-11 | Reintentar o agotar una generación IA | COMPONENTE | no accesible desde frontend |
| SEQ-12 | Comprobar salud y dependencias | API/COMPONENTE | sin pantalla |

## SEQ-00 — Inicio de sesión, recuperación y autorización de área

```mermaid
sequenceDiagram
    autonumber
    actor Usuario
    participant FE as Frontend React
    participant API as Backend Express
    participant Auth as Login/ResolveSession
    participant Repo as PrismaAuthRepository
    participant DB as PostgreSQL app
    participant Browser as Cookie jar

    Usuario->>FE: Abre la aplicación
    FE->>API: GET /auth/me<br/>credentials: include
    alt no existe sesión válida
        API-->>FE: 401 unauthorized
        FE-->>Usuario: Muestra /ingresar
        Usuario->>FE: Correo + contraseña
        FE->>API: POST /auth/login<br/>credentials: include
        API->>Auth: Normalizar correo y verificar bcrypt
        Auth->>Repo: Buscar credenciales y roles
        Repo->>DB: users + user_roles
        alt credenciales inválidas o cuenta no ACTIVO
            API-->>FE: 401 invalid_credentials
            FE-->>Usuario: Error genérico
        else credenciales válidas
            Auth->>Repo: Crear auth_session con hash del token
            Repo->>DB: INSERT auth_sessions
            API-->>Browser: Set-Cookie gym_session<br/>HttpOnly; Secure; SameSite=None en Vercel
            API-->>FE: 200 user {id, gymId, roles} + expiresAt
            FE->>FE: Cachear identidad y elegir área concedida
            FE-->>Usuario: Alumno, entrenador o admin según roles
        end
    else sesión válida
        API->>Auth: Resolver hash, vigencia, revocación y usuario ACTIVO
        API-->>FE: 200 user {id, gymId, roles}
        FE-->>Usuario: Restaurar área autorizada
    end

    note over FE: El selector muestra sólo roles presentes en la sesión.<br/>Las guardas impiden abrir un área no concedida.
    note over API: Cada endpoint vuelve a autorizar rol y recurso;<br/>la guarda frontend no es una frontera de seguridad.
```

El cierre ejecuta `POST /auth/logout`, revoca el hash de sesión, elimina la cookie con los mismos atributos con que fue emitida y limpia la caché del frontend incluso si la petición falla.

## SEQ-01 — Rutina vigente y aviso de renovación

Alcance real: devuelve metadatos y renovación. No devuelve días, ejercicios ni series; por eso `/alumno/rutina` no puede mostrar la prescripción completa.

```mermaid
sequenceDiagram
    autonumber
    actor Alumno
    participant FE as Frontend React
    participant Auth as Sesión y autorización
    participant API as Backend Express
    participant UC as GetActiveRoutineUseCase
    participant Repo as PrismaRoutinesRepository
    participant DB as PostgreSQL app
    participant LS as LocalStorage

    Alumno->>FE: Abre /alumno
    FE->>API: GET /routines/active<br/>cookie gym_session
    API->>Auth: authenticate + requireAuth + requireRoles(ALUMNO)
    alt identidad ausente o rol inválido
        Auth-->>FE: 401 unauthorized o 403 forbidden_role
    else identidad aceptada
        API->>UC: execute(studentId = req.user.id)
        UC->>Repo: findActiveByStudentId(studentId)
        Repo->>DB: Buscar routine state=VIGENTE<br/>última revisión favorable<br/>versión current
        DB-->>Repo: rutina o vacío
        alt no existe rutina vigente
            Repo-->>UC: null
            UC-->>FE: 404 active_routine_not_found
            FE-->>Alumno: Banner "Todavía no tenés una rutina vigente"
        else existe
            Repo-->>UC: rutina + fecha de inicio + versión
            UC->>UC: vencimiento = inicio + 60 días<br/>días restantes y estado
            UC-->>FE: 200 ActiveRoutineResponse
            FE->>FE: Zod valida respuesta
            FE->>LS: Leer descarte por alumno y fecha
            alt faltan más de 7 días
                FE-->>Alumno: No muestra aviso
            else quedan 7 días o menos
                FE-->>Alumno: Banner pendiente / vence hoy / vencido
                opt alumno descarta aviso no vencido
                    FE->>LS: Guardar descarte del día
                end
            end
        end
    end
```

Variante entrenador/administrador: `GET /students/:studentId/routines/active` agrega validación de propiedad y, para entrenador, asignación vigente. Frontend la utiliza en la tarjeta resumida de la ficha del alumno.

## SEQ-02 — Cartera priorizada del entrenador

```mermaid
sequenceDiagram
    autonumber
    actor Entrenador
    participant FE as Frontend React
    participant Auth as Sesión y autorización
    participant API as Backend Express
    participant UC as ListTrainerStudentsUseCase
    participant Repo as PrismaStudentsRepository
    participant DB as PostgreSQL app

    Entrenador->>FE: Abre cartera, alumnos o rutinas
    FE->>API: GET /trainers/me/students<br/>rol ENTRENADOR
    API->>Auth: authenticate + requireAuth + requireRoles
    alt no autorizado
        Auth-->>FE: 401 o 403
        FE-->>Entrenador: Error y opción Reintentar
    else autorizado
        API->>UC: execute(trainerId)
        UC->>Repo: findAssignedToTrainer(trainerId)
        Repo->>DB: Alumnos con asignación ends_at IS NULL<br/>perfil + última medición + objetivo vigente<br/>rutina VIGENTE + propuesta PENDIENTE
        DB-->>Repo: registros de cartera
        Repo-->>UC: AssignedStudentRecord[]
        UC->>UC: Calcular faltas/bloqueo y renovación<br/>ordenar: bloqueado, propuestas, nombre
        UC-->>FE: 200 TrainerStudentDto[]
        FE->>FE: Zod valida y TanStack Query cachea
        FE-->>Entrenador: Cartera, señales, rutinas y pendientes
    end
```

Las cajas de búsqueda y orden visibles en `/entrenador/alumnos` no participan: actualmente son sólo visuales.

## SEQ-03 — Ficha de alumno y rutina resumida

```mermaid
sequenceDiagram
    autonumber
    actor Entrenador
    participant FE as Frontend React
    participant API as Backend Express
    participant Auth as Sesión y autorización
    participant Assign as TrainerAssignments
    participant StudentUC as GetStudentStatusUseCase
    participant RoutineUC as GetActiveRoutineUseCase
    participant DB as PostgreSQL app

    Entrenador->>FE: Abre /entrenador/alumnos/:studentId
    par Estado del alumno
        FE->>API: GET /students/:studentId/status
        API->>Auth: Exigir ENTRENADOR
        API->>StudentUC: execute(trainerId, studentId)
        StudentUC->>Assign: isActive(trainerId, studentId)
        Assign->>DB: Buscar asignación vigente
        alt no asignado
            StudentUC-->>FE: 403 forbidden_not_assigned
        else asignado
            StudentUC->>DB: Perfil, usuario y última medición
            StudentUC-->>FE: Estado, motivo, faltas, altura y fecha
        end
    and Rutina resumida
        FE->>API: GET /students/:studentId/routines/active
        API->>Auth: Rol + propiedad + asignación
        API->>RoutineUC: execute(studentId)
        RoutineUC->>DB: Rutina VIGENTE, revisión y versión current
        RoutineUC-->>FE: Resumen de rutina o 404
    end
    FE-->>Entrenador: Ficha, bloqueo y tarjeta de rutina
```

Las pestañas `Rutina` y `Mediciones` cambian la URL pero renderizan la misma ficha; no cargan estructura de rutina ni historial de mediciones.

## SEQ-04 — Desbloqueo con medición adeudada

```mermaid
sequenceDiagram
    autonumber
    actor Entrenador
    participant FE as Frontend React
    participant API as Backend Express
    participant Auth as Sesión y autorización
    participant UC as UnlockStudentUseCase
    participant Assign as TrainerAssignments
    participant Repo as PrismaStudentsRepository
    participant DB as PostgreSQL app

    Entrenador->>FE: Ingresa peso y altura
    FE->>FE: Validar peso 20..250 y altura 100..250
    Entrenador->>FE: Presiona Desbloquear alumno
    FE->>API: POST /students/:studentId/unlock<br/>{weightKg, heightCm}
    API->>Auth: Exigir ENTRENADOR
    API->>API: Zod valida UUID y body
    API->>UC: execute(trainerId, studentId, valores)
    UC->>Assign: isActive(trainerId, studentId)
    alt entrenador no asignado
        UC-->>FE: 403 forbidden_not_assigned
    else asignado
        UC->>Repo: findById(studentId)
        Repo->>DB: Consultar usuario y perfil
        alt alumno inexistente
            UC-->>FE: 404 student_not_found
        else alumno no está SUSPENDIDO
            UC-->>FE: 409 student_not_blocked
        else suspendido
            UC->>Repo: unlock(...)
            Repo->>DB: BEGIN
            Repo->>DB: users.state = ACTIVO si sigue SUSPENDIDO
            Repo->>DB: Upsert PESO_CORPORAL del día
            Repo->>DB: Actualizar student_profiles.height_cm
            Repo->>DB: Insertar audit_logs DESBLOQUEO_ALUMNO
            Repo->>DB: COMMIT
            Repo-->>UC: true
            UC-->>FE: 200 StudentStatusDto activo
            FE->>FE: Invalidar status y cartera en TanStack Query
            FE-->>Entrenador: Confirmación de desbloqueo
        end
    end
```

## SEQ-05 — Listado y apertura de propuestas de adaptación

```mermaid
sequenceDiagram
    autonumber
    actor Entrenador
    participant FE as Frontend React
    participant API as Backend Express
    participant Auth as Sesión y autorización
    participant ListUC as ListTrainerProposalsUseCase
    participant ReviewUC as GetProposalReviewUseCase
    participant Assign as TrainerAssignments
    participant Repo as PrismaProposalsRepository
    participant DB as PostgreSQL app

    Entrenador->>FE: Abre /entrenador/rutinas/revisar
    FE->>API: GET /trainers/me/proposals
    API->>Auth: Exigir ENTRENADOR
    API->>ListUC: execute(trainerId)
    ListUC->>Repo: findPendingForTrainer(trainerId)
    Repo->>DB: Propuestas PENDIENTES de alumnos asignados
    DB-->>Repo: resumen, alumno, diagnóstico y cantidad de ajustes
    ListUC-->>FE: 200 ProposalSummaryDto[]
    FE-->>Entrenador: Lista de propuestas pendientes

    Entrenador->>FE: Selecciona una propuesta
    FE->>API: GET /proposals/:proposalId
    API->>ReviewUC: execute(trainerId, proposalId)
    ReviewUC->>Repo: findById(proposalId)
    Repo->>DB: Propuesta + alumno + diagnóstico<br/>rutina + ajustes + evidencia
    ReviewUC->>Assign: isActive(trainerId, studentId)
    alt propuesta inexistente
        ReviewUC-->>FE: 404 proposal_not_found
    else alumno no asignado
        ReviewUC-->>FE: 403 forbidden_not_assigned
    else permitido
        ReviewUC-->>FE: 200 ProposalReviewDto
        FE-->>Entrenador: Advertencia de datos y ajustes seleccionables
    end
```

La creación automática de `evolution_diagnostics` y `adaptation_proposals` no está implementada. Este recorrido opera sobre propuestas ya existentes en PostgreSQL, incluidas las cargadas por seed de Test.

## SEQ-06 — Resolución de propuesta de adaptación

```mermaid
sequenceDiagram
    autonumber
    actor Entrenador
    participant FE as Frontend React
    participant API as Backend Express
    participant UC as ResolveProposalUseCase
    participant Assign as TrainerAssignments
    participant Domain as planResolution + applyAdjustments
    participant Repo as PrismaProposalsRepository
    participant DB as PostgreSQL app

    Entrenador->>FE: Aprobar, aprobar parcialmente o rechazar
    FE->>API: POST /proposals/:id/resolution<br/>{decision, acceptedAdjustmentIds?, reason?}
    API->>API: Validar body y rol ENTRENADOR
    API->>UC: execute(...)
    UC->>Repo: findById(proposalId)
    UC->>Assign: isActive(trainerId, studentId)
    alt no existe / no asignado / ya resuelta
        UC-->>FE: 404 / 403 / 409
    else pendiente
        UC->>Domain: planResolution(decisión, ids, motivo)
        alt decisión RECHAZADA
            Domain-->>UC: Estado RECHAZADA, sin nueva versión
        else aceptación total o parcial
            UC->>Repo: findCurrentVersion(routineId)
            Repo->>DB: Leer versión actual completa
            UC->>Domain: applyAdjustments(copia de días, aceptados)
            alt ajuste ESTRUCTURA o valor no aplicable
                Domain-->>FE: 422 adjustment_not_applicable
            else ajustes aplicables
                Domain-->>UC: Copia ajustada
            end
        end
        UC->>Repo: persistResolution(...)
        Repo->>DB: BEGIN + SELECT propuesta FOR UPDATE
        alt otra petición ya la resolvió
            Repo->>DB: ROLLBACK/fin sin cambios
            Repo-->>FE: 409 proposal_not_pending
        else mantiene PENDIENTE
            opt aceptación
                Repo->>DB: Marcar versión anterior current=false
                Repo->>DB: Crear versión nueva current=true
                Repo->>DB: Copiar días, ejercicios y series ajustados
                Repo->>DB: Crear routine_review favorable<br/>reinicia ciclo de renovación
            end
            Repo->>DB: Marcar ajustes ACEPTADO/RECHAZADO
            Repo->>DB: Resolver adaptation_proposal
            Repo->>DB: Crear audit_log
            opt se creó versión
                Repo->>DB: Crear notice RUTINA_AJUSTADA para alumno
            end
            Repo->>DB: COMMIT
            Repo-->>UC: estado y versión resultante
            UC-->>FE: 200 ProposalResolutionDto
            FE->>FE: Invalidar propuesta, listado, cartera y alumnos
            FE-->>Entrenador: Confirmación de resolución
        end
    end
```

## SEQ-07 — Bloqueo por inactividad

Estado `API`: no tiene interfaz frontend.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrador o cliente HTTP
    participant API as Backend Express
    participant Auth as Sesión y autorización
    participant UC as BlockUserOnInactivityUseCase
    participant Domain as evaluateInactivity
    participant Repo as PrismaUsersRepository
    participant DB as PostgreSQL app

    Admin->>API: POST /users/:userId/inactivity-check<br/>{consecutiveFaltas?, daysInactive?, lastDataDate?}
    API->>Auth: Exigir ADMINISTRADOR
    API->>API: Validar UUID y body
    API->>UC: execute(input)
    UC->>Repo: findById(userId)
    Repo->>DB: SELECT user
    alt usuario inexistente
        UC-->>Admin: 404 user_not_found
    else existe
        UC->>Domain: Evaluar faltas en ciclos de 60 días
        alt menos de 3 faltas
            Domain-->>UC: shouldBlock=false
            UC-->>Admin: 200, estado sin cambio
        else 3 faltas o más
            Domain-->>UC: shouldBlock=true
            UC->>Repo: save(state=SUSPENDIDO)
            Repo->>DB: UPDATE users
            UC-->>Admin: 200, blocked=true
        end
    end
```

El cálculo usa valores recibidos en el request; el endpoint no deriva por sí solo la inactividad desde sesiones o mediciones.

## SEQ-08 — Consulta y finalización de generación

Estado `FRONT→API`: el panel del alumno conserva el `requestId`
por alumno en `localStorage`, recupera el seguimiento tras recargar y consulta al
backend cada tres segundos. El polling se detiene en `COMPLETADA`,
`NO_DISPONIBLE`, `CANCELADA` o ante un error HTTP; nunca consulta directamente a
IA. Una generación completa se convierte en rutina únicamente mediante una
finalización `POST` explícita e idempotente.

```mermaid
sequenceDiagram
    autonumber
    actor Alumno
    participant FE as Frontend React
    participant LocalStorage
    participant API as Backend Express
    participant Auth as Sesión y autorización
    participant UC as GetRoutineGenerationUseCase
    participant Repo as PrismaRoutineGenerationsRepository
    participant Validator as Validador determinístico
    participant DB as PostgreSQL app + ai_integration

    Alumno->>FE: Abre su panel
    FE->>LocalStorage: Recuperar requestId del alumno
    loop cada 3 s mientras PENDIENTE/PROCESANDO
        FE->>API: GET /students/:studentId/routine-generations/:requestId
        API->>Auth: Exigir ALUMNO + studentId propio
        API->>API: Validar ambos UUID
        API->>UC: execute(requestId, studentId, alumnoId)
        UC->>Repo: findById(owner)
        Repo->>DB: Solicitud + ownership + último intento<br/>resultado + última validación
        alt solicitud inexistente o ajena
            UC-->>FE: 404 routine_generation_not_found
        else existe
            UC-->>FE: 200 {status, estructuraCandidata, violaciones, error, routineId}
            FE-->>Alumno: Estado, error o violaciones
        end
    end
    opt estado COMPLETADA y todavía sin routineId
        FE->>API: POST /students/:studentId/routine-generations/:requestId/finalize
        API->>Auth: Exigir ALUMNO + studentId propio
        API->>Repo: finalize(owner)
        Repo->>DB: Leer output, alumno, condiciones,<br/>equipamiento y ejercicios
        Repo->>Validator: Validar schema, RN-39a, catálogo,<br/>nivel, condiciones y equipamiento
        alt salida inválida
            Repo->>DB: Registrar ai_result_validation inválida
            API-->>FE: 422 invalid_generated_routine
        else ya hay otra rutina PROPUESTA
            API-->>FE: 409 proposed_routine_already_exists
        else salida válida
            Repo->>DB: BEGIN + validación válida + rutina PROPUESTA<br/>versión, días, ejercicios y series + COMMIT
            API-->>FE: 201 {routineId, status: PROPUESTA}
            FE-->>Alumno: Rutina propuesta enviada a revisión
        end
    end
```

La consulta no materializa ni descarta rutinas. La mutación ocurre sólo en el
`POST /finalize`; una propuesta preexistente se conserva y produce conflicto.

## SEQ-09 — Solicitud de generación desde backend

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Alumno
    participant API as Backend Express
    participant Context as PrismaGenerationContextRepository
    participant DB as PostgreSQL app
    participant Gateway as HttpRoutineGenerationGateway
    participant AI as FastAPI IA

    Cliente->>API: POST /students/:studentId/routine-generations<br/>{textoLibre?, parametros?, idempotencyKey?}
    API->>API: Exigir ALUMNO + studentId propio<br/>validar input
    API->>Context: getStudentContext(studentId)
    Context->>DB: Perfil, objetivos y condiciones
    API->>Context: getPrefilteredCatalog(studentId, gymId, now)
    Context->>DB: Ejercicios, nivel, condiciones<br/>y equipamiento presente
    alt alumno inexistente / input faltante / catálogo vacío
        API-->>Cliente: 404 o 422
    else contexto disponible
        API->>Gateway: requestGeneration(contexto + catálogo)
        Gateway->>AI: POST /v1/routine-generations<br/>X-API-Key + body completo
        AI->>AI: Autenticar e idempotencia
        AI->>DB: Insert ai_generation_request + contexto minimizado
        AI->>AI: Publicar requestId en Vercel Queues
        AI-->>Gateway: 202 pending o 200 existente
        API->>DB: Upsert app.routine_generation_ownership
        API-->>Cliente: 202/200 {requestId, status}
    end
```

## SEQ-10 — Despacho y procesamiento implementados dentro de IA

Estado `COMPONENTE`: FastAPI acepta la solicitud, persiste el contexto minimizado,
publica el identificador y responde sin esperar al LLM.

```mermaid
sequenceDiagram
    autonumber
    actor Caller as Backend autorizado
    participant AI as FastAPI IA
    participant DB as PostgreSQL ai_integration
    participant Q as Vercel Queues
    participant W as Worker Python
    participant LLM as Ollama / Cloudflare Tunnel

    Caller->>AI: POST /v1/routine-generations<br/>X-API-Key + contexto y catálogo
    AI->>AI: Comparación segura de AI_SERVICE_API_KEY
    alt credencial inválida
        AI-->>Caller: 401 unauthorized
    else autorizada
        AI->>DB: Buscar idempotency_key
        alt solicitud existente
            AI-->>Caller: 200 {requestId, status}
        else nueva
            AI->>DB: INSERT request + COMMIT
            AI->>Q: send UUID con idempotency_key=requestId
            AI-->>Caller: 202 pending
            Q->>W: GenerationMessage(requestId)
            W->>DB: SELECT ... FOR UPDATE SKIP LOCKED
            W->>DB: state=PROCESANDO + lease<br/>crear attempt PROCESANDO
            W->>LLM: POST /api/generate con stream<br/>Bearer LLM_API_TOKEN<br/>schema JSON compatible + contexto minimizado
            LLM-->>W: Chunks NDJSON de salida estructurada
            W->>W: Pydantic valida RutinaEstructurada
            W->>W: Hash canónico de salida
            W->>DB: BEGIN
            W->>DB: Insert ai_generation_results<br/>contrato routine-generation@1.1
            W->>DB: attempt=COMPLETADO
            W->>DB: request=COMPLETADA y liberar lease
            W->>DB: COMMIT
        end
    end
```

La validación de negocio y la materialización pertenecen a backend y ocurren en
SEQ-08, no dentro del worker IA.

## SEQ-11 — Falla y reintento del worker IA

```mermaid
sequenceDiagram
    autonumber
    participant Q as Vercel Queues
    participant W as Worker Python
    participant DB as PostgreSQL ai_integration
    participant LLM as Ollama / Cloudflare Tunnel

    Q->>W: Entregar GenerationMessage
    W->>DB: Reclamar solicitud y crear intento N
    W->>LLM: Generar rutina (timeout 120 s)
    alt timeout
        W->>DB: attempt=AGOTADO_POR_TIEMPO<br/>error_code=llm_timeout
    else salida no cumple Pydantic
        W->>DB: attempt=SALIDA_INVALIDA<br/>error_code=invalid_structured_output
    else error HTTP o envelope inválido
        W->>DB: attempt=FALLIDO<br/>error_code=llm_request_failed
    end
    alt N menor que 2
        W->>DB: request=PENDIENTE<br/>liberar lease
        W--xQ: Lanzar GenerationProcessingError
        Q->>W: Reentrega posterior
    else N igual a 2
        W->>DB: request=NO_DISPONIBLE<br/>finished_at y liberar lease
        W-->>Q: Finalizar sin nueva excepción funcional
    end
```

Vercel Queue está configurada con `max_attempts=6`, pero la persistencia de dominio agota la generación al segundo intento. Entregas posteriores no reclaman una solicitud `NO_DISPONIBLE`.

## SEQ-12 — Salud y readiness

```mermaid
sequenceDiagram
    autonumber
    actor Monitor
    participant Back as Backend Express
    participant AI as FastAPI IA
    participant DB as PostgreSQL
    participant LLM as Ollama / Cloudflare Tunnel

    Monitor->>Back: GET /health
    Back-->>Monitor: 200 {status: ok}
    Monitor->>Back: GET /ready
    Back->>DB: SELECT 1
    alt DB disponible
        Back-->>Monitor: 200 ready, database up
    else DB no disponible
        Back-->>Monitor: 503 unavailable
    end

    Monitor->>AI: GET /health
    AI-->>Monitor: 200 {status: ok}
    Monitor->>AI: GET /ready + Authorization Bearer
    AI->>DB: SELECT 1
    AI->>LLM: GET /api/tags + Bearer
    alt ambas dependencias disponibles
        AI-->>Monitor: 200 ready, database up, llm up
    else alguna dependencia falla
        AI-->>Monitor: 503 dependency_unavailable
    end
```

## Funcionalidades visibles que no deben tener diagrama de negocio todavía

```yaml
frontend_placeholders:
  alumno:
    - Mi rutina completa
    - Inicio y registro de sesión
    - Progreso
    - Historial
    - Catálogo
    - Perfil
  entrenador:
    - Plantillas
    - Catálogo
    - Perfil
    - Pestañas específicas de rutina y mediciones del alumno
  administrador:
    - Analítica real
    - Usuarios y roles
    - Asignaciones
    - Catálogo
    - Reglas
    - Configuración
missing_endpoints:
  - lectura de rutina con días, ejercicios y series
  - inicio, registro y cierre de sesión
  - historial y progreso
  - CRUD de usuarios, invitaciones, asignaciones, catálogo y plantillas
  - creación automática de diagnósticos y propuestas de adaptación
  - autenticación mediante sesiones propias
```

## Convenciones para trasladar a otra herramienta

- Línea continua: llamada síncrona HTTP, caso de uso o consulta directa.
- Línea discontinua: respuesta.
- Flecha asíncrona: publicación o entrega de Vercel Queues.
- Fragmento `alt`: respuesta alternativa o error observable.
- Fragmento `opt`: paso condicional sin cambiar el éxito principal.
- Marco transaccional: desde `BEGIN` hasta `COMMIT`; todo el bloque se revierte ante error.
- No conectar frontend con IA, Queue, LLM o PostgreSQL.
- Dibujar la cookie sólo entre navegador y backend; el token nunca se expone al código React ni se persiste en PostgreSQL en claro.
- No dibujar una rutina completa en SEQ-01: el endpoint actual sólo devuelve resumen y renovación.
- Mantener SEQ-09 como falla hasta alinear ruta, autenticación, payload y persistencia backend–IA.
