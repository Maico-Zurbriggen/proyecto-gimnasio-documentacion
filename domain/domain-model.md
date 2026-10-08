# D4 — Modelo de dominio

|                |                                              |
| -------------- | -------------------------------------------- |
| **Versión**    | 2.4                                          |
| **Fecha**      | 2026-09-28                                   |
| **Estado**     | Normativo. Congelar antes de escribir código |
| **Depende de** | D1, D2, D3                                   |

**Cambios de la v1.0:** entidades `Invitacion` e `InventarioGimnasio` · `EquipamientoDisponible` eliminada (el equipamiento es del gimnasio) · `EjercicioArticulacion` agregada, sin la cual la compatibilidad no era calculable · `EjercicioRutina` gana el estado de compatibilidad que cuatro reglas exigían y el modelo no soportaba · `Ejercicio` gana el nivel de dificultad como atributo tipado · dos referencias cruzadas corregidas · PD-07 nuevo.

**Cambios de la v2.1 (replanteo de IA, [D11/DD-34](../decisions/design-decisions.md)):** `ScoreRiesgo` y `SegmentoPerfil` quedan **derogadas** — el riesgo de abandono se retira del alcance (RF-061 a RF-063 → WON'T) y la descripción de perfil (RF-064) la produce la capa generativa de forma efímera.

**Cambios de la v2.2 ([baseline de alcance](../planning/baseline-alcance-2026-09.md)).** El núcleo del modelo **no cambia**: el eje `RutinaAsignada → VersionRutina → DiaRutina → EjercicioRutina → SeriePrescripta`, la sesión autocontenida, `EjercicioMusculo`, `EjercicioArticulacion` y las 23 restricciones de integridad quedan intactos. Lo que cambia es lo que la Etapa 1 no necesita persistir:

| Elemento                                                              | Estado en la Etapa 1                                                                                    |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `Comentario`                                                          | ⏸ No se crea. Diferida con RF-039 (1 voto de 8)                                                          |
| `PlantillaRutina.publicada`                                           | ⏸ No se crea en la Etapa 1. RF-021 es alcance opcional (COULD, 1 voto de 8): la plantilla existe, la publicación sólo se agrega si se implementa |
| `RutinaAsignada.origen`                                               | ✎ Se reduce a `PLANTILLA_ENTRENADOR` y `GENERADA`. `PRESET_ELEGIDO_POR_ALUMNO` sólo existe si se implementa RF-021 (ver §2.4) |
| `PerfilAlumno.nivel de actividad`                                     | ⏸ No se crea. Sólo alimentaba la estimación energética de RF-012 (2/8)                                    |
| `SesionEntrenamiento.es diferida` y `.desbloqueada hasta`             | ⏸ No se crean. Diferidos con RF-034 (2/8) y RF-117                                                       |
| `RegistroAuditoria`                                                   | ✎ Se acota a las operaciones de RF-038, RF-066, RF-091 y RF-114. RF-097 general queda diferido            |
| `ScoreRiesgo`, `SegmentoPerfil`                                       | Derogadas en la v2.1; la votación lo confirma (1, 0 y 0 votos)                                            |

**Añadir una columna después es barato; quitarla después de tener datos, no.** Por eso lo diferido no se crea ahora: los repositorios están en andamiaje y ninguna migración se ejecutó todavía.

**Cambios de la v2.3 (baseline v4.0 confirmada).** Se aplican las retiradas también al detalle del modelo: desaparecen `Comentario`, `nivel de actividad`, sesión diferida y desbloqueo. `EvaluacionComponente` no se persiste: RF-121 y RF-122 están diferidos y RF-073 se resuelve con regresión generativa versionada en el repositorio de IA. Diagnóstico, propuesta, ajustes y récords pertenecen a `app` y forman parte del modelo de la Etapa 1.

**Cambios de la v2.4:** se agregan `ControlMedicionCiclo` y `BloqueoMediciones` para representar faltas consecutivas reales y el proceso de regularización. El bloqueo funcional deja de inferirse del estado administrativo del usuario.

### Índices exigidos desde la primera migración

No son optimización posterior: son lo que sostiene RNF-01 y RNF-36, y definirlos después obliga a una migración sobre tablas con datos.

| Índice                                                     | Qué sostiene                                             |
| ---------------------------------------------------------- | ---------------------------------------------------------- |
| `RegistroSerie(sesion, orden)` **único**                   | RI-10 e idempotencia del registro (RF-104, RNF-13)        |
| `RegistroSerie(ejercicio_ejecutado, sesion)`               | Volumen por grupo muscular y carga máxima estimada        |
| `SesionEntrenamiento(alumno, fecha_de_ocurrencia)`         | Adherencia, historial y diagnóstico                       |
| `RutinaAsignada(alumno, estado)` parcial sobre VIGENTE y PROPUESTA | RI-06 y la cartera priorizada                     |
| `AsignacionEntrenador(alumno)` parcial sobre `hasta IS NULL` | RI-05 y **toda decisión de autorización** (RA-01, RA-03) |
| `CondicionFisica(perfil)` parcial sobre `hasta IS NULL`    | Verificación de compatibilidad en cada puesta en vigencia |
| `Ejercicio(gimnasio)` admitiendo `NULL`                    | Catálogo base frente a catálogo propio (PD-04 del modelo) |

### Aislamiento multi-gimnasio: en el modelo, no en el motor

El ámbito por gimnasio (RF-069, RA-02) se resuelve con la columna `gimnasio` en toda entidad raíz más RI-01, **no con `row-level security` de PostgreSQL**. Una segunda fuente de autorización dentro del motor habría que mantenerla sincronizada con la de la aplicación, y el proyecto no tiene capacidad para operar dos. La compensación es RNF-14: una prueba automatizada por cada operación que reciba un identificador de alumno.

---

## 1. Estructura general

```
Gimnasio ──< InventarioGimnasio >── (equipamiento, §4.1 de D2)
 │
 ├─< Invitacion ──▶ (produce) ──▶ Usuario
 │
 ├─< Usuario ──< RolUsuario
 │     ├── PerfilAlumno ──< Objetivo(vigencia)
 │     │        ├─< CondicionFisica(vigencia, zona corporal, severidad)
 │     │        ├─< Aptitud
 │     │        ├─< MedicionCorporal
 │     │        ├─< ControlMedicionCiclo
 │     │        └─< BloqueoMediciones
 │     ├── PerfilEntrenador
 │     ├─< Consentimiento
 │     └─< AsignacionEntrenador (alumno ─ entrenador, vigencia)
 │
 ├─< PlantillaRutina ──< DiaPlantilla ──< EjercicioPlantilla ──< SeriePrescriptaPlantilla
 │        │
 │        │  (copia profunda al solicitar)
 │        ▼
 │   RutinaAsignada ──< RevisionRutina
 │        ├──< VersionRutina ──< DiaRutina ──< EjercicioRutina ──< SeriePrescripta
 │        │         ▲
 │        │         │ (una propuesta aceptada genera una versión)
 │        │   PropuestaAdaptacion ──< AjustePropuesto
 │        │         ▲
 │        │   DiagnosticoEvolucion ──< DiagnosticoEjercicio
 │        ▼
 │   SesionEntrenamiento ──< RegistroSerie   [prescripto + ejecutado en la misma fila]
 │
 └─< Ejercicio (del gimnasio)          CATÁLOGO BASE (global, gimnasio = null)
Gimnasio ──< EjercicioHabilitadoGimnasio >── Ejercicio
            └────────────── Ejercicio ──< EjercicioMusculo   >── GrupoMuscular
                                      ──< EjercicioArticulacion >── Articulacion
                                      ──< EjercicioEquipamiento

   RecordPersonal · Aviso
   RegistroAuditoria
   [derogadas v2.2: ScoreRiesgo, SegmentoPerfil]
```

## 2. Entidades

### 2.1 Ámbito, identidad y alta

| Entidad                | Atributos relevantes                                                                                          | Notas                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Gimnasio**           | nombre, zona horaria, estado de afiliación, activo                                                            | Creado por aprovisionamiento (RF-115), no por ningún rol de la aplicación. Su zona horaria define el día y la semana de todos sus usuarios |
| **InventarioGimnasio** | gimnasio, equipamiento (§4.1 de D2), presente | N:M contra la enumeración cerrada; contexto de equipamiento real. La disponibilidad se mantiene mediante EjercicioHabilitadoGimnasio |
| **Invitacion**         | gimnasio, correo destinatario, roles ofrecidos, emitida por, emitida en, vence en, estado, usuario resultante | Única vía de alta. Ver PD-08                                                                                                               |
| **Usuario**            | gimnasio, correo, nombre, estado, fecha de alta, invitación de origen                                         | El correo es único **dentro del gimnasio**: una misma persona puede ser alumna de dos gimnasios. Ver DD-24                                 |
| **RolUsuario**         | usuario, rol ∈ {ALUMNO, ENTRENADOR, ADMINISTRADOR}                                                            | Conjunto, no valor único. Un usuario tiene ≥1                                                                                              |
| **Consentimiento**     | usuario, tipo, otorgado, instante, texto aceptado                                                             | Se conserva el texto exacto que se aceptó, no una referencia a la versión actual                                                           |

### 2.2 Estado del alumno

| Entidad                  | Atributos relevantes                                                                                                                         | Cardinalidad                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **PerfilAlumno**         | usuario, fecha de nacimiento, sexo, altura, altura actualizada en, nivel de experiencia (§4.4), días semanales disponibles, estado de membresía | 1:1 con Usuario con rol ALUMNO. `altura actualizada en` permite probar que fue confirmada dentro del ciclo o después del bloqueo              |
| **Objetivo**             | perfil, tipo (§4.5), desde, hasta                                                                                                            | 1:N. **Como máximo uno** con `hasta = null`; ninguno antes de la primera declaración                                                          |
| **CondicionFisica**      | perfil, zona corporal (§4.2 ∪ §4.3), severidad (§4.6), descripción libre, desde, hasta                                                       | 1:N. Varias pueden estar vigentes a la vez. **La zona corporal y la severidad son tipadas**: son las que hacen calculable la contraindicación |
| **Aptitud**              | perfil, fecha de emisión, fecha de vencimiento, observación, cargada por                                                                     | 1:N. La vigente es la de vencimiento más lejano no superado. `cargada por` admite al alumno o a un administrador                              |
| **MedicionCorporal**     | perfil, tipo (§4.11), valor, fecha                                                                                                           | 1:N. Única por (perfil, tipo, fecha)                                                                                                          |
| **ControlMedicionCiclo** | perfil, rutina y versión de referencia, inicio, vencimiento, resultado ∈ {CUMPLIDO, FALTA}, medición de peso, confirmación de altura, evaluado en | 1:N. Único por (perfil, vencimiento). Es inmutable una vez cerrado y constituye el hecho del que se deriva la racha                            |
| **BloqueoMediciones**    | perfil, control que lo originó, estado ∈ {PENDIENTE_MEDICION, PENDIENTE_APROBACION, RESUELTO}, motivo, faltas al bloquear, bloqueado en, regularizado en, aprobado en, aprobado por | 1:N histórico. Como máximo uno activo por alumno. Conserva la evidencia, regularización y aprobación que cerraron el bloqueo |
| **PerfilEntrenador**     | usuario, especialidad, experiencia, presentación                                                                                             | 1:1 con Usuario con rol ENTRENADOR                                                                                                            |
| **AsignacionEntrenador** | alumno, entrenador, desde, hasta, autor del alta, autor de la baja                                                                           | N:M con vigencia. Como máximo una vigente por alumno, por regla RN-18 y no por estructura                                                     |

**Por qué la asignación es N:M y no un campo en el alumno.** Un campo no permite responder "¿cambió de entrenador antes de abandonar?" ni auditar quién lo asignó. La unicidad se impone por RN-18. Costo marginal: nulo.

**Por qué el alumno ya no declara equipamiento.** Ver PD-07.

### 2.3 Catálogo

| Entidad                             | Atributos relevantes                                                                                                                                                | Notas                                                                                                                                      |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Ejercicio** | gimnasio propietario (nulo para base), nombre, instrucciones, patrón, dificultad, unilateral, estado, origen, recurso visual principal; fuente, ID externo y revisión para importados | UUID interno estable. Los datos pendientes no se publican como ficha aprobada; detalle de importación en architecture/exercise-catalog.md |
| **EjercicioEquipamiento**           | ejercicio, equipamiento (§4.1)                                                                                                                                      | N:M. Un ejercicio requiere **todo** el equipamiento que declara. Un ejercicio sin filas requiere sólo `PESO_CORPORAL`                      |
| **EjercicioMusculo**                | ejercicio, grupo muscular (§4.2), participación ∈ {PRIMARIA, SECUNDARIA}                                                                                            | N:M. Sin filas, el ejercicio está **no clasificado**: no aporta volumen, y esa ausencia se distingue de aportar cero. Ver D10/CB-12        |
| **EjercicioArticulacion** | ejercicio, articulación (§4.3) | N:M. Describe el movimiento para contexto de IA; un dato faltante requiere revisión, no una contraindicación calculada por backend |
| **GrupoMuscular**, **Articulacion** | código, nombre, región                                                                                                                                              | Tablas de referencia pobladas con §4.2 y §4.3. Cerradas                                                                                    |

| **EjercicioHabilitadoGimnasio** | gimnasio, ejercicio, habilitado, revisión, actualizado por, actualizado en | N:M única por gimnasio y ejercicio. Sólo referencia base o propios del mismo gimnasio; conservar filas al deshabilitar |
| **RecursoVisualEjercicio** | ejercicio, orden, pose, URL propia versionada | Uno o varios recursos por ficha; referencia principal conservada para presentación |

### 2.4 Prescripción

| Entidad                      | Atributos relevantes                                                                                                                                                                          |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PlantillaRutina**          | gimnasio, autor, nombre, tipo de rutina (§4.5), activa; `publicada` sólo se agrega si se implementa el alcance opcional de presets                                                                                                                          |
| **DiaPlantilla**             | plantilla, orden, nombre                                                                                                                                                                      |
| **EjercicioPlantilla**       | día de plantilla, ejercicio, orden, nota                                                                                                                                                      |
| **SeriePrescriptaPlantilla** | ejercicio de plantilla, orden, repeticiones mínimas, repeticiones máximas, carga sugerida, descanso, es de calentamiento                                                                      |
| **RutinaAsignada**           | alumno, plantilla de origen, tipo de rutina, frecuencia semanal objetivo, estado (D6/§1), origen ∈ {PLANTILLA_ENTRENADOR, GENERADA}; `PRESET_ELEGIDO_POR_ALUMNO` sólo existe si se implementa RF-021, solicitada por, solicitada en                           |
| **RevisionRutina**           | rutina, entrenador revisor, resultado ∈ {APROBADA, APROBADA_CON_CAMBIOS, RECHAZADA}, observación, instante                                                                                    |
| **VersionRutina**            | rutina, número, vigente, creada en, creada por, propuesta que la originó                                                                                                                      |
| **DiaRutina**                | versión de rutina, orden, nombre, patrón dominante                                                                                                                                            |
| **EjercicioRutina**          | día de rutina, ejercicio, orden, nota, **estado de compatibilidad** ∈ {COMPATIBLE, ADVERTIDO, INCOMPATIBLE, EJERCICIO_DESACTIVADO}, **motivo de la marca**                                    |
| **SeriePrescripta**          | ejercicio de rutina, orden, repeticiones mínimas, repeticiones máximas, carga sugerida, descanso, es de calentamiento                                                                         |

**`estado de compatibilidad` en `EjercicioRutina`.** RN-29, RN-92, RN-93 y RF-101 exigen "marcar el ejercicio en la rutina vigente sin retirarlo". En la v1.0 ninguna estructura lo soportaba. Es un atributo derivado que se recalcula en cada verificación de compatibilidad y se persiste para que la marca sobreviva a la consulta y pueda mostrarse al iniciar una sesión sin recalcular.

### 2.5 Ejecución

| Entidad                 | Atributos relevantes                                                                                                                                                                                                                                                                               |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SesionEntrenamiento** | alumno, rutina, versión de rutina, día de rutina, estado (D6/§3), iniciada en, finalizada en, duración, **fecha de ocurrencia**, es simulada                                                                                                                               |
| **RegistroSerie**       | sesión, orden, ejercicio prescripto, ejercicio ejecutado, repeticiones mínimas prescriptas, repeticiones máximas prescriptas, carga prescripta, es de calentamiento, carga ejecutada, repeticiones ejecutadas, esfuerzo percibido, completada, es adicional, motivo de omisión, atípico confirmado |

**`fecha de ocurrencia` separada de `iniciada en`.** Todos los indicadores usan la fecha de ocurrencia; la auditoría usa el instante de registro.

**`ejercicio prescripto` y `ejercicio ejecutado` en la misma fila.** Cuando no hay sustitución son el mismo. El volumen se imputa al ejecutado; el cumplimiento se evalúa contra el prescripto.

### 2.6 Adaptación e inteligencia

| Entidad                  | Atributos relevantes                                                                                                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DiagnosticoEvolucion** | alumno, versión de rutina evaluada, período desde/hasta, situación global (§4.9), adherencia del período, calculado en, versión del componente, criterios no evaluados                 |
| **DiagnosticoEjercicio** | diagnóstico, ejercicio, situación (§4.9), variación de carga máxima estimada, cumplimiento de repeticiones, esfuerzo percibido medio, sesiones consideradas                            |
| **PropuestaAdaptacion**  | alumno, diagnóstico de origen, estado (D6/§4), creada en, resuelta en, resuelta por, versión resultante, versión del componente                                                        |
| **AjustePropuesto**      | propuesta, tipo (§4.10), ejercicio de rutina afectado _o_ alcance global, valor anterior, valor propuesto, criterio, datos que lo sustentan, estado ∈ {PENDIENTE, ACEPTADO, RECHAZADO} |
| **RecordPersonal**       | alumno, ejercicio, tipo (§4.8), valor, sesión que lo produjo, fecha, vigente                                                                                                           |
| ~~**ScoreRiesgo**~~      | **Derogada (v2.2)** — RF-061 a RF-063 pasan a WON'T ([D11/DD-34](../decisions/design-decisions.md)); no hay estimación de riesgo que persistir                                          |
| ~~**SegmentoPerfil**~~   | **Derogada (v2.2)** — la descripción de perfil (RF-064) la produce la capa generativa y es efímera; no se persiste ([D11/DD-34](../decisions/design-decisions.md))                       |

### 2.7 Transversales

| Entidad               | Atributos relevantes                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| **Aviso**             | destinatario, tipo (§4.12), referencia, texto, instante, leído en, vencido                        |
| **RegistroAuditoria** | actor, operación, entidad afectada, identificador afectado, valor anterior, valor nuevo, instante |

## 3. Puntos difíciles del modelo

### PD-01 — Plantilla, rutina y versión

**Problema.** ¿Qué pasa si un entrenador modifica una plantilla ya usada por doce alumnos? ¿Y qué pasa cuando se aplica una adaptación a una rutina bajo la cual ya se ejecutaron sesiones?

| Alternativa                              | Descartada porque                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| La rutina referencia a la plantilla      | Modificar la plantilla reescribe el pasado de doce alumnos; la personalización individual es imposible |
| Versionado con diferencias y propagación | Exige resolución de conflictos. Coste desproporcionado                                                 |
| **Copia + versiones completas** ✅       | —                                                                                                      |

**Elegida:** copia profunda al solicitar la rutina (RF-022) más versiones completas de la rutina (RF-092).
**Qué se sacrifica.** Los cambios de plantilla no se propagan, y hay duplicación de datos. A esta escala la duplicación es irrelevante; la no propagación es deseable.
**Por qué versiones completas y no diferencias.** Una versión de rutina es una copia profunda de una estructura pequeña: no hay diferencias que calcular ni conflictos que resolver, y RF-093 se responde comparando dos versiones.

### PD-02 — La sesión es autocontenida

Cada sesión copia su prescripción al iniciarse, en sus propios registros de serie. Aunque la rutina cambie de versión mañana, la sesión de hoy conserva lo que estaba prescripto hoy `[F: RF-028]`.

- El pasado es inmune al versionado, sin lógica adicional.
- El cumplimiento (prescripto contra ejecutado) sale gratis, por serie.
- Un ejercicio desactivado después no rompe ninguna sesión anterior.

### PD-03 — Derivado o persistido

**Regla general:** se deriva todo lo que sea función pura de los datos crudos; se persiste sólo lo que es un evento con fecha, la salida fechada de un componente, o una marca que debe sobrevivir a la consulta.

| Dato                                                                 | Decisión                           | Motivo                                                                                                                                                                                                   |
| -------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Volumen, frecuencia, carga máxima estimada, adherencia, cumplimiento | **Derivado**                       | Si se persisten y cambia la definición, hay que recalcular todo el histórico                                                                                                                             |
| **Récord personal**                                                  | **Persistido**                     | Evento con fecha que debe notificarse en el momento. Recalcularlo pierde el instante                                                                                                                     |
| **Diagnóstico y propuesta**                                          | **Persistido**                     | Salidas fechadas de un componente con versión; deben poder auditarse                                                                                                                                     |
| ~~Estimación de riesgo y segmento~~                                  | **N/A (v2.2)**                     | Riesgo de abandono retirado del alcance; la descripción de perfil (RF-064) es efímera. Ver [D11/DD-34](../decisions/design-decisions.md)                                                                  |
| **Alternativas de sustitución incorporadas a un candidato de rutina** | **Persistido**                     | Salida de la capa generativa (RF-059); se guarda la lista, no se reejecuta `[F: RF-072]`                                                                                                                  |
| **Estado de compatibilidad de un ejercicio de rutina**               | **Persistido, derivado en origen** | Es el único derivado que se persiste. Se recalcula ante cada verificación (RN-45) y se guarda para que la marca esté disponible al iniciar una sesión y en la vista de rutina sin recalcular el conjunto |
| Peso corporal y perímetros                                           | **Persistido**                     | Son el dato crudo                                                                                                                                                                                        |

### PD-04 — Ámbito del catálogo

Un ejercicio con `gimnasio = null` pertenece al catálogo base y es visible para todos; uno con gimnasio informado sólo dentro de él. Reconcilia RF-013 con RF-069 sin duplicar la carga inicial.
**Disponibilidad.** Consultar una ficha base no la hace prescribible: EjercicioHabilitadoGimnasio determina su incorporación a cada gimnasio. El campo gimnasio de Ejercicio conserva propiedad, no habilitación.
**Qué se sacrifica.** Un entrenador no puede promover su ejercicio al catálogo base.

### PD-05 — Un solo entrenador vigente sobre una relación con historial

El modelo soporta el historial completo; RN-18 impone la unicidad. Sin el historial no se puede responder qué entrenador supervisó un período ni calcular la carga por entrenador.

### PD-06 — Borrado

**Ninguna entidad referenciada por información histórica se borra físicamente.** Ejercicios, usuarios, plantillas y rutinas conservan las referencias necesarias. La baja de cuenta y su anonimización están diferidas con RF-006 y RF-105; si vuelven al alcance se incorporarán mediante una migración y reglas específicas.

### PD-07 — El equipamiento es del gimnasio, no del alumno

El inventario describe equipamiento real y lo mantiene el administrador. La disponibilidad de ejercicios se declara por separado mediante habilitaciones (RN-116); un cambio de inventario requiere revisarlas, sin selección automática. La IA recibe ambos datos y el contexto del alumno para decidir adecuación. El alumno no declara equipamiento propio. La declaración incorrecta o desactualizada queda registrada como riesgo R-15.

### PD-08 — El alta es por invitación

**Problema.** El sistema no es abierto: un gimnasio afiliado avisa a la persona para que se registre. ¿Cómo queda vinculado un usuario a su gimnasio?

**Elegida:** la invitación es la única vía de alta. Un administrador —o un entrenador, para sus futuros alumnos— emite una invitación nominal a una dirección de correo, con los roles que se le otorgarán. La persona crea su cuenta desde esa invitación y queda vinculada al gimnasio emisor `[F: decisión del cliente, 2026-08-18]`.

**Qué resuelve.** No hay autorregistro sin gimnasio; la pertenencia al gimnasio no es un dato que el usuario elige; los roles quedan determinados por quien invita y no por quien se registra; y queda auditado quién incorporó a cada persona.

**Qué se sacrifica.** No hay crecimiento espontáneo de usuarios. Es exactamente lo que el modelo de negocio pide.

**Arranque.** El primer administrador de un gimnasio no puede invitarse a sí mismo: lo crea el aprovisionamiento (RF-115), junto con el gimnasio. Es una operación del proveedor del sistema, fuera de la aplicación y de todo rol.

### PD-09 — Controles y bloqueos de mediciones son hechos persistidos

La racha actual se deriva leyendo los controles cerrados desde el más reciente hasta el primer `CUMPLIDO`; no se persiste como contador mutable. En cambio, cada `ControlMedicionCiclo` y cada `BloqueoMediciones` se persisten porque son hechos fechados que deben sobrevivir a reintentos del job, explicar por qué se restringió al alumno y evitar que los mismos tres ciclos históricos vuelvan a bloquearlo después de una aprobación.

La suspensión administrativa continúa en `Usuario.estado`. El bloqueo por mediciones es una restricción del rol ALUMNO y pertenece a `BloqueoMediciones`: un usuario con varios roles conserva las capacidades de sus otros roles.

## 4. Restricciones de integridad

| #      | Restricción                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RI-01  | Un usuario pertenece a exactamente un gimnasio                                                                                                          |
| RI-02  | El correo es único dentro de un gimnasio                                                                                                                |
| RI-03  | Un usuario tiene al menos un rol                                                                                                                        |
| RI-04  | Un alumno tiene como máximo un objetivo con `hasta = null`                                                                                              |
| RI-05  | Un alumno tiene como máximo una asignación con `hasta = null`                                                                                           |
| RI-06  | Un alumno tiene como máximo una rutina en estado VIGENTE y como máximo una en estado PROPUESTA                                                          |
| RI-06b | Una rutina sólo alcanza VIGENTE si existe una revisión favorable de un entrenador con asignación vigente sobre ese alumno en el instante de la revisión |
| RI-07  | Una rutina tiene exactamente una versión marcada como vigente                                                                                           |
| RI-08  | Una medición corporal es única por (alumno, tipo, fecha)                                                                                                |
| RI-09  | Un alumno tiene como máximo una sesión en estado EN_CURSO                                                                                               |
| RI-10  | Un registro de serie es único por (sesión, orden)                                                                                                       |
| RI-11  | Un ejercicio del catálogo base tiene `gimnasio = null`; uno del gimnasio lo tiene informado                                                             |
| RI-12  | Toda serie prescripta pertenece a un ejercicio de rutina, que pertenece a un día, que pertenece a una versión                                           |
| RI-13  | El orden es único dentro de su nivel                                                                                                                    |
| RI-14  | Una propuesta pertenece a un único diagnóstico, y ambos al mismo alumno                                                                                 |
| RI-15  | Un ajuste pertenece a una única propuesta                                                                                                               |
| RI-16  | Toda sesión referencia la versión de rutina bajo la cual se ejecutó                                                                                     |
| RI-17  | `hasta` es posterior a `desde` en toda entidad con vigencia                                                                                             |
| RI-18  | Una sesión simulada sólo contiene registros de serie simulados                                                                                          |
| RI-19  | Una invitación pertenece a un gimnasio y produce como máximo un usuario                                                                                 |
| RI-20  | Todo usuario referencia la invitación que lo originó, salvo el primer administrador de cada gimnasio, que referencia el aprovisionamiento               |
| RI-21 | Un ejercicio admite varias participaciones PRIMARIAS y SECUNDARIAS; cada grupo aparece una sola vez por ejercicio y no ocupa ambos roles |
| RI-22  | Un récord personal vigente es único por (alumno, ejercicio, tipo)                                                                                       |
| RI-23  | Un gimnasio tiene al menos un usuario con rol ADMINISTRADOR en estado activo                                                                            |
| RI-24  | Un control de mediciones es único por (alumno, vencimiento), referencia una rutina y versión del mismo alumno y no cambia después de cerrarse             |
| RI-25  | Un alumno tiene como máximo un bloqueo de mediciones cuyo estado no sea RESUELTO                                                                          |
| RI-26  | Un bloqueo sólo pasa a PENDIENTE_APROBACION con peso y confirmación de altura posteriores a `bloqueado en`, y sólo se resuelve por su entrenador vigente   |
| RI-27 | Una habilitación es única por (gimnasio, ejercicio) y sólo referencia base o una ficha propia del mismo gimnasio |
| RI-28 | La clave (fuente, identificador externo) es única; las reimportaciones conservan el UUID interno y las referencias históricas |
