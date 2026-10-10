# D8 — Especificación de requerimientos funcionales

**Actualización 2026-10-05:** [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) reemplaza el prefiltrado y la validación determinista de entrenamiento. RF-018 entra en alcance por decisión directa para curar fichas propias; la votación histórica se conserva. RF-101 sigue diferido en su sustitución automática. RF-118 incluye las habilitaciones y avisos de disponibilidad.

|                |            |
| -------------- | ---------- |
| **Versión**    | 4.1        |
| **Fecha**      | 2026-09-28 |
| **Estado**     | Normativo en cuanto al enunciado de cada requisito. **La clasificación de alcance de la Etapa 1 es propuesta**: depende de PD-01 y PD-00 del [baseline de alcance](../planning/baseline-alcance-2026-09.md) |
| **Depende de** | D1 a D7    |

**Identificadores estables.** Ningún identificador se reutiliza, se renumera ni se borra. RF-001 a RF-124 conservan su numeración aunque su enunciado, tipo, prioridad o alcance hayan cambiado. Renumerarlos rompería veinte documentos del corpus y los `AGENTS.md` de los tres repositorios de código, a cambio de nada.

**Cambios de la v4.1:** RF-123 y RF-124 incorporan el bloqueo por tres ciclos consecutivos sin peso y altura, la regularización personal del alumno y la aprobación posterior del entrenador.

### Cambios de la v3.3 → v4.0

La v4.0 incorpora tres fuentes que la v3.3 no tenía: la **votación del equipo** sobre RF-001 a RF-081 (8 de 9 integrantes), las **respuestas registradas del equipo** a las decisiones del Acta de Redefinición, y la **verificación del estado real de los tres repositorios de código**. El análisis completo está en el [baseline de alcance](../planning/baseline-alcance-2026-09.md); aquí se registran sus efectos sobre los requisitos.

**1 · Aparece la dimensión de alcance, separada de la prioridad.** Un requisito puede ser MUST y estar fuera de esta etapa: la prioridad dice cuánto importa al producto, el alcance dice si se construye ahora. Estaban confundidos en una sola columna.

| Marca          | Significado                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **N1**         | Núcleo de la Etapa 1. No se recorta                                                                                  |
| N2             | Comprometido en la Etapa 1                                                                                           |
| N3             | Condicionado al hito del Sprint 3                                                                                    |
| **⏸ DIFERIDO** | Fuera de la Etapa 1, **no del producto**. Conserva su enunciado y su prioridad. Distinto de WON'T, que significa nunca |
| ⊂ RF-xxx       | Absorbido por fusión en otro requisito, que conserva su contenido íntegro                                            |
| → regla        | Degradado: no era un requisito funcional sino una regla, una restricción o un criterio de aceptación                  |
| `n/8`          | Votos obtenidos. Sin marca: no fue votado (RF-082 en adelante son posteriores a la votación)                          |

**2 · Cinco fusiones**, con el contenido de los absorbidos conservado íntegro en el resultante: RF-032 ⊕ RF-033 → **RF-027** (ciclo de vida de la sesión; fusión sugerida por el equipo y ampliada) · RF-023 → **RF-038** · RF-060 → **RF-059** · RF-107 → **RF-036** · RF-004 → **RF-065**.

**3 · Cuatro fusiones sugeridas se rechazan, con fundamento**: RF-054 ⊕ RF-055 borraría la frontera entre componente de decisión y componente narrativo, y dejaría sin sujeto a RNF-24 · RF-005 dentro de RF-065 haría desaparecer la verificación por recurso, que es RA-01, R-11 y RNF-14 · RF-088 ⊕ RF-089 obligaría a inventar una «propuesta vacía», cuando un diagnóstico sin propuesta es un resultado válido.

**4 · Cuatro degradaciones**: RF-098, RF-102, RF-103 y RF-104 no eran requisitos funcionales. Su contenido se conserva como restricción de integridad, convención transversal o criterio de aceptación.

**5 · Enunciados que cambian**, todos por consecuencia del alcance y no por revisión del diseño:

- **RF-058** ya no puede apoyar la continuidad en «presets publicados del gimnasio»: RF-021 quedó diferido. La vía manual pasa a ser la plantilla del entrenador (RF-019). Ver [D11/DD-35](../decisions/design-decisions.md).
- **RF-059** absorbe RF-060; desde ADR 0013 la adecuación se evalúa con IA, sin exclusión de entrenamiento en código.
- **RF-036** absorbe el criterio de urgencia de RF-107, que existía sólo porque RF-036 no era verificable sin él.
- **RF-027** absorbe la reanudación y la finalización: son tres transiciones del mismo autómata de D6/§4.

**6 · Lo que la votación confirmó.** RF-061 a RF-063 obtuvieron 1, 0 y 0 votos: la votación respalda el WON'T de la v3.3. El ciclo central —contexto, catálogo, prescripción, ejecución, indicadores y adaptación— obtuvo mayorías amplias sin excepción.

**7 · RF-053 se conserva pese a no alcanzar el corte.** Obtuvo 3 votos de 8, pero está comprometido por escrito ante el Product Owner en `deliverable PO/alcance-ia-generativa.md` v2.1. Una votación interna no revoca un compromiso ya asumido: queda en alcance, en banda N2, hasta que el Product Owner lo libere (PD-07).

**8 · El estado real del código.** Al 2026-09-01 los tres repositorios contienen andamiaje y **ninguna funcionalidad de dominio**: Express con `/health` y `/ready`, `schema.prisma` sin modelos, una SPA con una pantalla de bienvenida y un paquete Python vacío. Ningún requisito de este documento está implementado ni parcialmente implementado. No hay funcionalidad implementada sin documentar.

### Cambios anteriores, conservados

**v2.0:** alta por invitación (RF-116) y aprovisionamiento (RF-115) · inventario del gimnasio (RF-114) y catálogo prescribible (RF-118) · desbloqueo de sesión (RF-117) · tres ciclos de dependencias eliminados · nutrición cerrada como pauta orientativa.
**v3.0:** el candidato de rutina ajustable (RF-119) y la diferencia visible para el revisor (RF-120).
**v3.1 → v3.2:** sugerencia de carga de sesión (RF-121) y proyección de trayectoria (RF-122), **no provenientes de un pedido del cliente** y pendientes de confirmación.
**v3.3 (replanteo de IA, [D11/DD-34](../decisions/design-decisions.md), ya redactada):** RF-059, RF-060 y RF-064 pasan de `ML` a `AI` · RF-061 a RF-063 pasan a WON'T · RF-122 sube a SHOULD.

**Cambios de la v3.3 → v3.4:** los presets pasan de requisito obligatorio a alcance opcional. La primera entrega conserva plantillas privadas de entrenadores y generación; si no se implementan presets, la indisponibilidad generativa deshabilita esa capacidad sin afectar el diseño manual.

**Tipos:** WEB · AI · ML · DATA · HYBRID **Prioridad:** MUST · SHOULD · COULD · WON'T
**Marcas de historial:** 🆕 nuevo · ✎ enunciado modificado · ⬆⬇ cambio de prioridad · ⛔ derogado
**Marcas de alcance (v4.0):** **N1** · N2 · N3 · ⏸ DIFERIDO · ⊂ absorbido · → degradado a regla · `n/8` votos

---

## Módulo 0 · Afiliación y alta

| ID     | Requerimiento                                                                                                                                                                                                                                                                      | Tipo | Prior.  | Depende        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | -------------- |
| RF-115 | Disponer de una operación de aprovisionamiento, **externa a la aplicación**, que cree un gimnasio afiliado con su zona horaria y su primer usuario con rol administrador, de forma atómica                                                                                         | WEB  | MUST 🆕 **N1** | —              |
| RF-116 | Permitir el alta de usuarios **exclusivamente mediante invitación** nominal emitida por un administrador —para cualquier rol— o por un entrenador —sólo con rol alumno—, de un solo uso, con vencimiento y revocable, que determina el gimnasio y los roles del usuario resultante | WEB  | MUST 🆕 **N1** | RF-115         |
| RF-098 | Vincular todo usuario a exactamente un gimnasio en el momento de su alta, sin posibilidad de cambio posterior                                                                                                                                                                      | WEB  | MUST → regla | RF-116         |
| RF-114 | Permitir al administrador mantener el inventario real de equipamiento como contexto de IA y revisar las habilitaciones relacionadas cuando lo modifica, sin cambios automáticos del catálogo | WEB | MUST **N1** | RF-115 |
| RF-118 | Permitir al administrador habilitar y deshabilitar por lote ejercicios base o propios aprobados de su gimnasio, sin duplicar fichas, y usar toda esa lista como catálogo prescribible. Conservar historial y señalar bajas en rutinas y plantillas existentes | DATA/WEB | MUST **N1** · decisión 2026-10-05 | RF-114, RF-013, RF-100 |

## Módulo 1 · Cuentas y acceso

| ID     | Requerimiento                                                                                                                                                                                                                             | Tipo | Prior. | Depende             |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ------------------- |
| RF-001 | Permitir a una persona invitada completar su cuenta con nombre y contraseña                                                                                                                                                               | WEB  | MUST ✎ **N1** · 8/8 | RF-116              |
| RF-002 | Autenticar, mantener la sesión, cerrarla explícitamente y expirarla por inactividad                                                                                                                                                       | WEB  | MUST **N1** · 8/8 | RF-001              |
| RF-003 | Recuperar el acceso mediante verificación por correo con validez limitada, y cambiar la contraseña estando autenticado                                                                                                                    | WEB  | MUST N2 · 8/8 | RF-001              |
| RF-004 | ~~Registro abierto con rol alumno predeterminado~~                                                                                                                                                                                        | —    | **⛔** | Derogado por RF-116 |
| RF-005 | Autorizar cada operación verificando el rol **y** la relación del actor con el recurso concreto                                                                                                                                           | WEB  | MUST **N1** · 2/8 | RF-116, RF-066      |
| RF-006 | Permitir solicitar la baja de la cuenta y obtener una copia estructurada de los datos propios                                                                                                                                             | WEB  | MUST ⏸ DIFERIDO · 0/8 | RF-001              |
| RF-096 | Requerir consentimiento explícito y separado para el tratamiento de condiciones físicas, aptitud y mediciones corporales, y conservar el texto aceptado                                                                                   | WEB  | MUST N2 | RF-001              |
| RF-097 | Registrar en auditoría toda operación sensible: invitaciones, cambios de rol, asignaciones, cambios de inventario, puesta en vigencia y modificación de rutinas, resolución de propuestas, desbloqueo de sesiones y curación del catálogo | WEB  | SHOULD ⏸ DIFERIDO | RF-005              |

## Módulo 2 · Perfil, objetivos y condiciones

| ID     | Requerimiento                                                                                                                                                                                                                                                                            | Tipo | Prior.  | Depende                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | ---------------------- |
| RF-007 | Registrar y mantener el perfil del alumno: edad, sexo, altura, nivel de experiencia y días semanales disponibles                                                                                                                                                                         | WEB  | MUST **N1** · 8/8 | RF-001                 |
| RF-008 | Declarar un objetivo vigente de la enumeración cerrada y modificarlo, conservando el historial y sus períodos de vigencia                                                                                                                                                                | WEB  | MUST **N1** · 8/8 | RF-007                 |
| RF-009 | Declarar las condiciones físicas que limitan la ejecución de ejercicios, **cada una con su zona corporal y su severidad tipadas**, y utilizarlas para condicionar prescripciones y recomendaciones. El alumno **no** declara equipamiento: el disponible es el inventario de su gimnasio | WEB  | MUST ✎ **N1** · 8/8 | RF-007, RF-114         |
| RF-010 | Registrar mediciones corporales fechadas, un máximo de un registro por tipo y fecha, corregibles y eliminables                                                                                                                                                                           | WEB  | MUST **N1** · 8/8 | RF-007                 |
| RF-011 | Mantener el perfil profesional del entrenador, visible para sus alumnos asignados                                                                                                                                                                                                        | WEB  | SHOULD ⏸ DIFERIDO · 4/8 | RF-116                 |
| RF-012 | Presentar una estimación orientativa del gasto energético diario y del rango de ingesta proteica de referencia, con su fórmula declarada, indicando explícitamente que no es una indicación nutricional profesional                                                                      | WEB  | COULD ✎ ⏸ DIFERIDO · 2/8 | RF-007, RF-010         |
| RF-084 | Registrar la aptitud con fecha de emisión y de vencimiento, cargada por el alumno o por un administrador, y **advertir de forma destacada** su ausencia o vencimiento al poner una rutina en vigencia y al iniciar una sesión, sin impedir ninguna operación                             | WEB  | MUST ✎ N2 | RF-007                 |
| RF-085 | Conservar el historial de condiciones físicas con sus fechas de inicio y fin, de modo que sea determinable qué condiciones estaban vigentes en una fecha dada                                                                                                                            | WEB  | MUST **N1** | RF-009                 |
| RF-111 | Determinar y exponer si un alumno tiene contexto suficiente para que se produzcan decisiones automáticas sobre él, e indicar qué falta cuando no lo tiene                                                                                                                                | DATA | MUST N2 | RF-007, RF-008, RF-009 |
| RF-123 | Evaluar diariamente los ciclos de 60 días ya cerrados de cada rutina vigente, persistir un único control por ciclo y restringir las capacidades del rol ALUMNO al alcanzar tres faltas consecutivas de peso y altura, sin contar faltas aisladas separadas por un ciclo cumplido y sin suspender la cuenta | WEB | MUST 🆕 **N1** · decisión cliente | RF-007, RF-010, RF-026 |
| RF-124 | Permitir al alumno restringido cargar personalmente el peso y la altura adeudados y, sólo después, permitir al entrenador con asignación vigente aprobar el desbloqueo en una operación atómica que revalide la asignación, resuelva el bloqueo y establezca una nueva línea de base | WEB | MUST 🆕 **N1** · decisión cliente | RF-123, RF-066, RF-010 |

## Módulo 3 · Catálogo de ejercicios

| ID     | Requerimiento                                                                                                                                                                                                  | Tipo | Prior. | Depende        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | -------------- |
| RF-099 | Mantener taxonomías de músculos, articulaciones, patrones y equipamiento; revisar los mapeos de RepDB y completar la clasificación pendiente antes de aprobar fichas importadas | DATA | MUST **N1** | — |
| RF-013 | Mantener un catálogo base consultable por usuarios autenticados y fichas propias visibles sólo en su gimnasio, mostrando cuáles están habilitadas allí | WEB | MUST **N1** · 8/8 | — |
| RF-014 | Localizar ejercicios por nombre, grupo muscular, equipamiento requerido, patrón de movimiento y nivel de dificultad                                                                                            | WEB  | MUST N2 · 8/8 | RF-013         |
| RF-015 | Presentar instrucciones, equipamiento, patrón, dificultad, articulaciones y recursos visuales por ejercicio. La importación inicial de RepDB usa imágenes estáticas y crédito visible de la fuente | WEB | MUST N2 · 8/8 | RF-013 |
| RF-016 | Asociar a cada ejercicio los grupos musculares que involucra, diferenciando participación primaria de secundaria, y las articulaciones que exige                                                               | WEB  | MUST ✎ **N1** · 8/8 | RF-013, RF-099 |
| RF-017 | Permitir a los entrenadores incorporar ejercicios propios con la misma información descriptiva y de clasificación exigida al resto                                                                             | WEB  | SHOULD N3 · 5/8 | RF-013, RF-016 |
| RF-018 | Permitir al administrador revisar, aprobar y retirar fichas propias de su gimnasio; aprobación y habilitación son independientes. La baja impide nuevas incorporaciones y conserva las referencias históricas | WEB | MUST **N1** · decisión 2026-10-05 (voto histórico 0/8) | RF-017, RF-118 |
| RF-100 | Distinguir el catálogo base, común a todos los gimnasios y no editable, del catálogo propio de cada gimnasio, visible sólo dentro de él                                                                        | WEB  | MUST N2 | RF-013, RF-069 |
| RF-101 | Señalar en toda rutina vigente los ejercicios desactivados, permitir su ejecución y generar una propuesta de sustitución                                                                                       | WEB  | SHOULD ⏸ DIFERIDO | RF-018, RF-089 |

## Módulo 4 · Diseño y solicitud de rutinas

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                                                                       | Tipo | Prior.  | Depende                |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | ---------------------- |
| RF-019 | Crear plantillas estructuradas en días ordenados, cada uno con una secuencia ordenada de ejercicios del catálogo                                                                                                                                                                                                                                                                                    | WEB  | MUST **N1** · 8/8 | RF-013                 |
| RF-020 | Definir para cada ejercicio la cantidad de series y, por serie, el rango de repeticiones objetivo, la carga sugerida, el descanso y su carácter de calentamiento o de trabajo                                                                                                                                                                                                                       | WEB  | MUST **N1** · 6/8 | RF-019                 |
| RF-021 | Publicar **opcionalmente** una plantilla como preset dentro del gimnasio y utilizar cualquier preset como punto de partida                                                                                                                                                                                                                                                                                            | WEB  | COULD ⬇ ⏸ DIFERIDO · 1/8 | RF-019                 |
| RF-022 | Generar, al solicitarse una rutina a partir de una plantilla, una copia completa e independiente de su estructura, conservando la referencia al origen                                                                                                                                                                                                                                              | WEB  | MUST ✎ **N1** · 0/8 | RF-019                 |
| RF-023 | Modificar ejercicios, series, repeticiones, cargas y descansos de la rutina de un alumno concreto sin afectar la plantilla ni las rutinas de otros                                                                                                                                                                                                                                                  | WEB  | MUST ⊂ RF-038 · 1/8 | RF-022                 |
| RF-024 | Requerir que toda rutina declare las sesiones esperadas por semana, dentro del rango que admite su tipo                                                                                                                                                                                                                                                                                             | WEB  | MUST ✎ **N1** · 2/8 | RF-022, RF-082         |
| RF-025 | Permitir exclusivamente al alumno autenticado solicitar para sí una rutina generada; una salida válida crea una rutina `PROPUESTA` que no rige hasta la revisión y aprobación del entrenador asignado                                                                                                                                                                              | WEB  | MUST ✎ **N1** · decisión PO | RF-054, RF-110         |
| RF-026 | Mantener como máximo una rutina vigente y una propuesta por alumno, archivando la vigente anterior al entrar otra en vigencia y descartando la propuesta anterior al solicitarse otra, preservando la consulta de lo archivado                                                                                                                                                                      | WEB  | MUST ✎ **N1** · 6/8 | RF-022                 |
| RF-082 | Clasificar cada plantilla y cada rutina según un tipo de la enumeración cerrada, y **derivar de él, mediante una tabla explícita, la frecuencia semanal admisible, la estructura de días, los esquemas de series y repeticiones, los rangos de descanso y la cobertura mínima de patrones de movimiento**                                                                                           | WEB  | MUST ✎ **N1** | RF-019                 |
| RF-083 | Evaluar mediante IA y revisión del entrenador la coherencia del tipo de rutina con objetivos y contexto, justificando el criterio sin comparación automática de etiquetas | HYBRID | MUST **N1** · decisión 2026-10-05 | RF-008, RF-082 |
| RF-110 | Exigir la revisión y la aprobación explícita de un entrenador con asignación vigente antes de que **cualquier** rutina entre en vigencia, cualquiera sea su origen                                                                                                                                                                                                                                  | WEB  | MUST **N1** | RF-022, RF-066         |
| RF-109 | Transferir al entrenador entrante todas las rutinas propuestas y propuestas de adaptación pendientes del alumno al establecerse una asignación                                                                                                                                                                                                                                                      | WEB  | MUST N2 | RF-066                 |
| RF-112 | Señalar al administrador los alumnos sin entrenador vigente y mantener bloqueadas sus rutinas propuestas y sus propuestas de adaptación hasta su reasignación                                                                                                                                                                                                                                       | WEB  | MUST N2 | RF-066, RF-110         |
| RF-119 | Presentar toda rutina generada o copiada de un preset como **candidato ajustable por el solicitante** antes de enviarla a revisión, admitiendo sustituir, agregar, quitar y reordenar ejercicios, pedir alternativas admisibles para uno puntual y regenerar desde parámetros corregidos, revalidando cada ajuste y **sin crear la rutina propuesta ni avisar al entrenador hasta la confirmación** | WEB  | MUST 🆕 ⏸ DIFERIDO | RF-025, RF-054, RF-086 |
| RF-120 | Registrar y presentar al entrenador revisor la diferencia entre la rutina propuesta y la salida original del componente, o la plantilla de origen                                                                                                                                                                                                                                                   | WEB  | MUST 🆕 ⏸ DIFERIDO | RF-119, RF-110         |

## Módulo 5 · Ejecución y registro

| ID     | Requerimiento                                                                                                                                                                                                                                                                | Tipo | Prior.    | Depende        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | --------- | -------------- |
| RF-027 | **Ciclo de vida completo de la sesión** ✎ v4.0 (absorbe RF-032 y RF-033): iniciarla seleccionando un día de la rutina vigente, proponiendo por defecto el siguiente del ciclo e impidiendo más de una en curso por alumno; conservar su estado y permitir la reanudación; cerrarla automáticamente tras el período de inactividad definido; y finalizarla registrando su duración, incorporándola al historial y habilitándola para el cálculo de indicadores. Las cuatro transiciones son criterios de aceptación separados de D6/§4                                                                                                             | WEB  | MUST **N1** · 8/8 | RF-022         |
| RF-028 | Copiar, al iniciarse la sesión, la prescripción vigente del día dentro de la propia sesión, de modo que las modificaciones posteriores no la alteren                                                                                                                         | WEB  | MUST **N1** · 5/8 | RF-027, RF-020 |
| RF-029 | Registrar por serie la carga, las repeticiones realizadas, opcionalmente el esfuerzo percibido y si fue completada, conservando de forma conjunta lo prescripto y lo ejecutado, y requiriendo confirmación explícita ante un valor atípico respecto del histórico del alumno | WEB  | MUST ✎ **N1** · 8/8 | RF-028         |
| RF-030 | Presentar cada serie precargada con los valores de la última ejecución del alumno en ese ejercicio                                                                                                                                                                           | WEB  | MUST **N1** · 1/8 | RF-029, RF-035 |
| RF-031 | Permitir durante la sesión agregar series, omitir series prescriptas y sustituir un ejercicio, imputando el trabajo al ejercicio ejecutado                                                                                                                                   | WEB  | MUST N2 · 6/8 | RF-029, RF-059 |
| RF-032 | Conservar el estado de una sesión en curso, permitir su reanudación y cerrarla automáticamente tras el período de inactividad definido                                                                                                                                       | WEB  | MUST ⊂ RF-027 · 3/8 | RF-027         |
| RF-033 | Finalizar una sesión registrando su duración, incorporándola al historial y habilitándola para el cálculo de indicadores                                                                                                                                                     | WEB  | MUST ⊂ RF-027 · 7/8 | RF-029         |
| RF-034 | Registrar una sesión de fecha anterior, **imputándola a la rutina y a la versión vigentes en esa fecha aunque hoy estén archivadas**, y corregir una sesión finalizada dentro del plazo                                                                                      | WEB  | SHOULD ✎ ⏸ DIFERIDO · 2/8 | RF-033         |
| RF-117 | Permitir a un entrenador con asignación vigente reabrir por tiempo acotado y una sola vez una sesión bloqueada, a pedido del alumno y con registro del motivo                                                                                                                | WEB  | SHOULD 🆕 ⏸ DIFERIDO | RF-034         |
| RF-035 | Consultar el historial de sesiones ordenado cronológicamente y el detalle de cualquiera, incluida la comparación entre lo prescripto y lo ejecutado                                                                                                                          | WEB  | MUST **N1** · 8/8 | RF-033         |
| RF-104 | Garantizar que el envío repetido de una misma serie produzca un único registro                                                                                                                                                                                               | WEB  | MUST → regla | RF-029         |
| RF-102 | Aplicar unidades y precisión únicas en todo el sistema, y rechazar del lado del servidor los valores fuera de los rangos admitidos                                                                                                                                           | WEB  | MUST → regla | RF-029, RF-010 |
| RF-103 | Almacenar todo instante en tiempo universal coordinado, presentarlo en la zona horaria del gimnasio, y usar una definición única de semana para toda agregación                                                                                                              | WEB  | MUST → regla | RF-033         |

## Módulo 6 · Seguimiento entrenador–alumno

| ID     | Requerimiento                                                                                                                                                                          | Tipo   | Prior. | Depende                |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | ---------------------- |
| RF-107 | Definir un criterio único y ordenado de urgencia para la cartera: pendientes de revisión, incompatibilidad sobrevenida, estancamiento, caída de adherencia, sin señal ✎ (v3.3: se retira "riesgo alto" al pasar RF-061 a WON'T)  | DATA   | MUST ✎ ⊂ RF-036 | RF-042, RF-046 |
| RF-036 | Presentar la cartera del entrenador ordenada según un **criterio único y ordenado de urgencia** ✎ v4.0 (absorbe RF-107) —pendientes de revisión, incompatibilidad sobrevenida, estancamiento, caída de adherencia, sin señal—, con fecha de última sesión, adherencia reciente y señales detectadas                                                  | DATA   | MUST **N1** · 5/8 | RF-107, RF-066         |
| RF-037 | Acceder a una vista consolidada del alumno: perfil, objetivos, condiciones, rutina vigente, historial, indicadores y mediciones                                                        | HYBRID | MUST **N1** · 8/8 | RF-035, RF-040, RF-005 |
| RF-038 | Modificar ejercicios, series, repeticiones, cargas y descansos de la rutina de un alumno asignado ✎ v4.0 (absorbe RF-023), **sin afectar la plantilla de origen ni las rutinas de otros alumnos**, registrando autor e instante, avisando al alumno y sin alterar las sesiones ejecutadas                                                       | WEB    | MUST **N1** · 7/8 | RF-023, RF-028         |
| RF-039 | Intercambiar comentarios asincrónicos entre entrenador y alumno asociados a una sesión o a una rutina                                                                                  | WEB    | SHOULD ⏸ DIFERIDO · 1/8 | RF-066                 |
| RF-095 | Entregar al usuario, dentro de la aplicación, los avisos de la enumeración cerrada de tipos, con reglas explícitas de no repetición, caducidad y reasignación al cambiar de entrenador | WEB    | MUST ✎ N2 | RF-038, RF-044, RF-046 |

## Módulo 7 · Indicadores

| ID     | Requerimiento                                                                                                                                                                                                                   | Tipo | Prior. | Depende                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ---------------------- |
| RF-040 | Calcular el volumen y la frecuencia por grupo muscular para un alumno y período, considerando sólo series de trabajo completadas y ponderando participación primaria y secundaria                                               | DATA | MUST **N1** · 8/8 | RF-016, RF-029         |
| RF-041 | Estimar la capacidad máxima por ejercicio a partir de carga y repeticiones registradas, dentro del rango de repeticiones en que la estimación es válida, y mantener su evolución                                                | DATA | MUST ✎ **N1** · 8/8 | RF-029                 |
| RF-042 | Calcular la adherencia sobre una ventana móvil de cuatro semanas, ponderando la frecuencia objetivo vigente en cada semana, **sin reiniciarse al cambiar de rutina**                                                            | DATA | MUST ✎ **N1** · 5/8 | RF-024, RF-033         |
| RF-043 | Calcular el cumplimiento de series y el cumplimiento de repeticiones, por sesión y por períodos agregados                                                                                                                       | DATA | MUST ✎ **N1** · 0/8 | RF-028, RF-029         |
| RF-044 | Identificar y registrar los récords personales por ejercicio en cada uno de los tres tipos definidos, notificarlos al producirse, y recalcularlos sobre el histórico completo si se corrige o elimina la sesión que los produjo | DATA | MUST ✎ N2 · 6/8 | RF-041                 |
| RF-045 | Presentar la evolución temporal de las mediciones corporales con media móvil de siete días                                                                                                                                      | DATA | MUST ✎ N2 · 8/8 | RF-010                 |
| RF-046 | Detectar y señalar estancamiento en un ejercicio, caída significativa de la adherencia y desbalance de volumen, con umbrales explícitos                                                                                         | DATA | MUST **N1** · 7/8 | RF-040, RF-041, RF-042 |
| RF-047 | Permitir configurar las ponderaciones, rangos de referencia y ventanas temporales sin modificar los datos históricos                                                                                                            | WEB  | COULD ⏸ DIFERIDO · 3/8 | RF-040                 |

## Módulo 8 · Visualización

| ID     | Requerimiento                                                                                                                                                                                                                                                                             | Tipo | Prior. | Depende                                        |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ---------------------------------------------- |
| RF-048 | Presentar al alumno un panel con su actividad reciente, adherencia, récords, evolución de sus indicadores de fuerza y evolución de sus mediciones                                                                                                                                         | DATA | MUST N2 · 8/8 | RF-040, RF-041, RF-042, RF-043, RF-044, RF-045 |
| RF-049 | Representar sobre un esquema bidimensional del cuerpo la intensidad del trabajo por grupo muscular en un período seleccionable, con detalle numérico y ejercicios que aportaron, distinguiendo los grupos sin información de los de volumen nulo, y sin depender exclusivamente del color | DATA | MUST ✎ ⏸ DIFERIDO · 4/8 | RF-040, RF-099                                 |
| RF-050 | Consultar por ejercicio la evolución temporal de la carga, el volumen y la capacidad máxima estimada, con los récords identificados                                                                                                                                                       | DATA | MUST N2 · 8/8 | RF-041                                         |
| RF-051 | Informar explícitamente cuando no haya información suficiente para calcular o representar un indicador, en lugar de presentar valores nulos, vacíos o engañosos                                                                                                                           | WEB  | MUST **N1** · 7/8 | RF-048                                         |
| RF-052 | Presentar al entrenador indicadores agregados de su cartera: adherencia media, distribución de señales y evolución de la actividad                                                                                                                                                        | DATA | SHOULD N3 · 8/8 | RF-036                                         |

## Módulo 9 · Inteligencia artificial generativa

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                      | Tipo   | Prior. | Depende                                |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | -------------------------------------- |
| RF-053 | Interpretar una descripción en lenguaje natural y traducirla a parámetros estructurados, sometidos a validación y a confirmación del usuario antes de utilizarse                                                                                                                                                                                   | AI     | MUST N2 · 3/8 | RF-009                                 |
| RF-054 | Generar asíncronamente una rutina mediante IA con todos los ejercicios habilitados y el contexto del alumno. IA evalúa adecuación, selecciona y prescribe; backend verifica formato, IDs, permisos, disponibilidad y vigencia del contexto. Una salida válida crea PROPUESTA para revisión del entrenador, sin candidato ajustable | HYBRID | MUST **N1** · 8/8 | RF-053, RF-082, RF-086, RF-118 |
| RF-055 | Acompañar toda rutina generada con una explicación en lenguaje natural de los criterios aplicados                                                                                                                                                                                                                                                  | AI     | MUST **N1** · 8/8 | RF-054                                 |
| RF-056 | Generar un resumen redactado de la evolución de un alumno en un período, elaborado exclusivamente a partir de indicadores previamente calculados                                                                                                                                                                                                   | HYBRID | SHOULD ⏸ DIFERIDO · 4/8 | RF-040, RF-041, RF-042, RF-043, RF-044 |
| RF-057 | Impedir cifras inventadas en componentes narrativos e indicaciones médicas. Para generación y alternativas, IA decide valores de entrenamiento y explica su adecuación; la revisión del entrenador evalúa esa decisión, sin reglas deterministas de prescripción | AI | MUST **N1** · 0/8 | RF-054, RF-056 |
| RF-058 | Mantener el resto del sistema operativo ante la indisponibilidad de la generación, informar esa condición sin detalles técnicos y conservar operativas **las plantillas privadas del entrenador y su creación manual** (RF-019) como vía disponible, siempre sujeta a revisión. ✎ v4.0: sustituye a los presets publicados, que pasan a alcance opcional (RF-021, COULD) — ver [D11/DD-35](../decisions/design-decisions.md). **Deja de existir una vía automática de prescripción cuando la generación no responde**                                                                                              | HYBRID | MUST ✎ **N1** · 1/8 | RF-021, RF-022, RF-054                 |
| RF-113 | Descartar toda salida generativa que no supere la validación, reintentar una sola vez y, tras el segundo fallo o 120 segundos por intento, declarar la generación no disponible sin presentar una propuesta inválida; no se construye una rutina determinística alternativa                                                                          | HYBRID | MUST ✎ **N1** | RF-054, RF-058                         |

## Módulo 10 · Aprendizaje automático

Tras el replanteo de IA de la v3.3 ([D11/DD-34](../decisions/design-decisions.md)), sólo RF-121 y RF-122 son componentes aprendidos. RF-059/RF-060 (alternativas de sustitución) y RF-064 (descripción de perfil) pasaron a la capa generativa — ver [generative-ai.md](../architecture/generative-ai.md). RF-061 a RF-063 pasan a WON'T.

| ID     | Requerimiento                                                                                                                                                                        | Tipo   | Prior. | Depende        |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ------ | -------------- |
| RF-059 | Proponer alternativas ordenadas y justificadas mediante IA a partir del ejercicio original, todo el catálogo habilitado y el contexto del alumno. IA evalúa equivalencia y adecuación; backend comprueba referencias y disponibilidad, sin prefiltrado ni ranking alternativo en código | AI | MUST **N1** · 8/8 | RF-016, RF-118 |
| RF-060 | Evaluar mediante IA las condiciones y experiencia del alumno al sugerir alternativas; contenido absorbido por RF-059 según ADR 0013 | AI | MUST ⊂ RF-059 · 2/8 | RF-059, RF-009 |
| RF-061 | **WON'T (v3.3)** ⬇. Estimar para cada alumno el nivel de riesgo de que interrumpa su actividad — retirado del alcance en el replanteo de IA por costo/esfuerzo frente al valor esperado con los datos disponibles (S-03) | ML     | WON'T ⬇ | —              |
| RF-062 | **WON'T (v3.3)** ⬇. Presentar la estimación de riesgo con sus factores y su fecha, restringida a entrenadores y administradores — sin efecto al retirarse RF-061                     | HYBRID | WON'T ⬇ | —              |
| RF-063 | **WON'T (v3.3)** ⬇. Actualizar las estimaciones de riesgo con periodicidad definida y a demanda — sin efecto al retirarse RF-061                                                     | ML     | WON'T ⬇ | —              |
| RF-064 | Presentar a entrenadores y administradores una descripción del perfil de comportamiento del alumno (frecuencia, volumen e intensidad relativos), redactada por la capa generativa a partir de los indicadores ya calculados y el objetivo vigente, **sin clustering y sin persistirse** | AI     | SHOULD ✎ N3 · 6/8 | RF-040, RF-042 |
| RF-121 | Sugerir la carga y las repeticiones de la próxima serie de un ejercicio a partir de la tendencia reciente del alumno en ese ejercicio (carga máxima estimada, cumplimiento, esfuerzo percibido), presentada como valor precargado adicional a —nunca en reemplazo de— el mínimo de RF-030; sin tendencia suficiente, se conserva exclusivamente RF-030                                                          | ML     | SHOULD 🆕 ⏸ DIFERIDO | RF-030, RF-071 |
| RF-122 | Proyectar, a partir de la tendencia de las últimas semanas, la carga máxima estimada por ejercicio y las mediciones corporales del alumno bajo el supuesto de que continúa con un patrón de entrenamiento similar, presentando la proyección junto con su incertidumbre y **sin emplear términos de composición corporal (masa muscular, grasa corporal) que el sistema no mide**                              | ML     | SHOULD 🆕⬆ ⏸ DIFERIDO | RF-010, RF-071 |

**Por qué RF-121 y RF-122 no reemplazan nada existente.** RF-030 sigue siendo el mínimo garantizado (última ejecución, MUST); RF-121 es una sugerencia adicional que se descarta ante indisponibilidad o tendencia insuficiente, igual que cualquier otra capacidad inteligente (RNF-11, RNF-12). RN-89a sigue siendo la única vía que modifica la prescripción vigente; RF-121 no prescribe, sólo precarga un valor que el alumno confirma o corrige (FL-05, paso 6). RF-122 no estima composición corporal: proyecta exclusivamente indicadores que el sistema ya deriva o registra (carga máxima estimada, perímetros), y su presentación debe declarar que es una proyección bajo continuidad de patrón, no una promesa de resultado — mismo principio que ya rige RF-012 y RF-108.

## Módulo 11 · Administración y analítica

| ID     | Requerimiento                                                                                                                                                                                                  | Tipo | Prior.   | Depende        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | -------- | -------------- |
| RF-065 | Emitir y revocar invitaciones, asignar y revocar roles, y suspender o reactivar cuentas dentro del gimnasio, sin poder dejarlo sin ningún administrador activo                                                 | WEB  | MUST ✎ **N1** · 6/8 | RF-116         |
| RF-066 | Establecer, finalizar y reasignar la relación entrenador–alumno conservando el historial completo y revocando de forma inmediata el acceso del entrenador saliente                                             | WEB  | MUST **N1** · 2/8 | RF-065         |
| RF-067 | Registrar y actualizar el estado de membresía con carácter exclusivamente informativo, sin condicionar el acceso a ninguna funcionalidad                                                                       | WEB  | COULD N3 · 8/8 | RF-065         |
| RF-068 | Presentar indicadores agregados del gimnasio: retención por cohorte, distribución de la actividad por día y franja horaria, adherencia media, carga de alumnos por entrenador y alumnos sin entrenador vigente | DATA | SHOULD ✎ ⏸ DIFERIDO · 2/8 | RF-042, RF-033 |
| RF-069 | Circunscribir toda la información al gimnasio al que pertenece, impidiendo el acceso a datos de otro gimnasio                                                                                                  | WEB  | MUST **N1** · 4/8 | RF-005         |

## Módulo 12 · Datos y evaluación de los componentes

| ID     | Requerimiento                                                                                                                                                                                                                                                                      | Tipo   | Prior. | Depende                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | ---------------------- |
| RF-070 | Importar RepDB Free de forma repetible mediante preparación privada, identidad externa estable, revisión de mapeos e imágenes y publicación atómica. Informar pendientes sin habilitarlos ni publicarlos como aprobados; conservar licencia y atribución, sin redistribuir el dataset | DATA | MUST **N1** · 8/8 | RF-013, RF-016, RF-099 |
| RF-071 | Disponer de un mecanismo para generar información histórica simulada, e identificar de manera inequívoca los registros simulados frente a los reales                                                                                                                               | DATA   | MUST **N1** · 3/8 | RF-029, RF-033         |
| RF-072 | Registrar para cada resultado de un componente inteligente la versión que lo generó, el contexto de entrada considerado y el instante de cálculo, de modo que sea reproducible; para el orden generativo de RF-059 se conserva la salida producida, no se reejecuta ✎             | HYBRID | MUST ✎ N2 · 0/8 | RF-059, RF-121         |
| RF-073 | Disponer de un procedimiento reproducible de evaluación de los componentes de recomendación y estimación sobre un conjunto reservado de tamaño declarado, que incluya la comparación contra un criterio de referencia simple, y conservar ambas métricas                           | HYBRID | MUST ✎ N2 · 0/8 | RF-121, RF-122, RF-071 |
| RF-105 | Anonimizar los datos personales del usuario dado de baja dentro del plazo establecido, conservando las sesiones y series desvinculadas de la identidad                                                                                                                             | WEB    | MUST ⏸ DIFERIDO | RF-006                 |
| RF-106 | Excluir los registros simulados de toda analítica presentada como real, y señalar cuándo una presentación se basa en datos simulados                                                                                                                                               | DATA   | MUST **N1** | RF-071                 |

## Módulo 13 · Pauta nutricional orientativa

| ID     | Requerimiento                                                                                                                                                                                                                                                                        | Tipo   | Prior.    | Depende |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | --------- | ------- |
| RF-075 | Producir una **pauta nutricional orientativa**: la distribución de la estimación energética y del rango proteico entre las comidas del día, en función del objetivo y las características del alumno. **No nombra alimentos, no compone comidas y no registra ingesta**              | HYBRID | COULD ✎ ⏸ DIFERIDO | RF-012  |
| RF-108 | Acompañar toda pauta nutricional de la declaración de que es orientativa y no profesional, exigir revisión humana antes de entregarla al alumno, e impedir su producción cuando falten los datos necesarios o el alumno haya declarado una condición que el sistema no puede evaluar | HYBRID | COULD ✎ ⏸ DIFERIDO | RF-075  |
| RF-074 | Registrar diariamente un indicador nutricional de referencia y visualizar su evolución junto al peso corporal y al volumen                                                                                                                                                           | WEB    | COULD ⏸ DIFERIDO · 1/8 | RF-010  |
| RF-076 | Base de alimentos y composición de comidas                                                                                                                                                                                                                                           | WEB    | **WON'T** | —       |

## Módulo 14 · Excluidos

| ID     | Requerimiento                                  | Prior. | Motivo                                                                          |
| ------ | ---------------------------------------------- | ------ | ------------------------------------------------------------------------------- |
| RF-077 | Mensajería en tiempo real                      | WON'T  | Coste desproporcionado frente a RF-039; compite con herramientas ya usadas      |
| RF-078 | Pagos, cuotas y facturación                    | WON'T  | Sin relación con el ciclo de datos; sustituido por RF-067                       |
| RF-079 | Alojamiento de contenido audiovisual propio    | WON'T  | Resuelto por recursos referenciados en RF-015                                   |
| RF-080 | Representación tridimensional del cuerpo       | WON'T  | Coste y riesgo desproporcionados frente a RF-049                                |
| RF-081 | Integración con dispositivos de monitorización | WON'T  | Habilitación de terceros incompatible con el plazo; duplica la fuente de verdad |

## Módulo 15 · Prescripción adaptativa

Núcleo del producto. Pedido directo del cliente.

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Tipo   | Prior. | Depende                                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ------ | -------------------------------------- |
| RF-086 | Evaluar la adecuación de ejercicios a condiciones, nivel y equipamiento mediante IA y revisión del entrenador. Antes de aprobar o modificar una versión, comprobar técnicamente que las incorporaciones siguen habilitadas; no implementar correspondencias ni rangos deterministas de entrenamiento | HYBRID | MUST **N1** · decisión 2026-10-05 | RF-009, RF-016, RF-085, RF-118 |
| RF-087 | Generar para un alumno sin historial usando perfil, objetivos, disponibilidad, condiciones y catálogo habilitado completo. Si el catálogo está vacío, no cabe en contexto o IA no puede construir una propuesta adecuada, explicar el motivo y derivar al entrenador, sin inventar una rutina | HYBRID | MUST **N1** | RF-007, RF-008, RF-009, RF-082, RF-086 |
| RF-088 | Evaluar periódicamente la evolución de cada alumno sobre su rutina vigente y producir un diagnóstico que asigne, **por criterios explícitos y con un orden de precedencia definido**, una de cinco situaciones a cada ejercicio y al conjunto: datos insuficientes, sobreexigencia, progresión adecuada, estímulo insuficiente o estancamiento                                                                                                                                 | DATA   | MUST ✎ **N1** | RF-041, RF-042, RF-043, RF-046         |
| RF-089 | Elaborar, a partir del diagnóstico y **mediante una tabla explícita que asocia cada situación con un tipo de ajuste y su magnitud**, una propuesta de modificación de la rutina vigente que puede comprender ajuste de cargas y volumen, sustitución de ejercicios, modificación de esquemas y reestructuración de días o frecuencia, garantizando que la propuesta resultante cumpla las condiciones de compatibilidad y los rangos de su tipo                                | HYBRID | MUST ✎ **N1** | RF-088, RF-059, RF-086, RF-082         |
| RF-090 | Registrar y presentar, para cada ajuste propuesto, el criterio que lo motiva y los datos de evolución que lo sustentan                                                                                                                                                                                                                                                                                                                                                         | HYBRID | MUST **N1** | RF-089                                 |
| RF-091 | Requerir la aprobación explícita de la propuesta antes de aplicarla, correspondiendo **siempre** al entrenador con asignación vigente, y permitir aceptarla total o parcialmente o rechazarla                                                                                                                                                                                                                                                                                  | WEB    | MUST ✎ **N1** | RF-089, RF-066, RF-110                 |
| RF-092 | Generar, al aplicarse una adaptación, una nueva versión de la rutina, conservando las anteriores y manteniendo inalteradas las sesiones ejecutadas bajo cada una, sin requerir una segunda revisión                                                                                                                                                                                                                                                                            | WEB    | MUST ✎ **N1** | RF-091, RF-028                         |
| RF-093 | Consultar la secuencia completa de adaptaciones aplicadas sobre la rutina de un alumno, con sus fechas, criterios y relación con la evolución del período                                                                                                                                                                                                                                                                                                                      | DATA   | SHOULD N2 | RF-092, RF-090                         |
| RF-094 | Señalar revisión pendiente cuando cambien objetivo, condiciones, aptitud, inventario o habilitaciones. Conservar rutinas y sesiones; evaluar adecuación con IA y entrenador, sin recalcular compatibilidad ni sustituir ejercicios automáticamente por disponibilidad | HYBRID | MUST **N1** | RF-084, RF-085, RF-086, RF-089, RF-114, RF-118 |

---

### HU03 · Renovación automática de ciclos cumplidos

Extensión solicitada el 2026-10-10: la revisión permite regenerar con comentario del entrenador y el administrador configura los parámetros de generación de su gimnasio, según [D5/§9.4](../domain/business-rules.md#94-parámetros-del-gimnasio-y-regeneración-por-entrenador). No depende de plantillas ni del candidato ajustable RF-119.

Extiende el circuito RF-088 a RF-092 con un job independiente del diagnóstico quincenal. La renovación por vencimiento, con o sin mediciones nuevas, su evidencia, el bloqueo y la alerta por indisponibilidad siguen [D5/§9.3](../domain/business-rules.md#93-renovación-automática-de-ciclo--hu03). La propuesta usa `ESTRUCTURA` y requiere la misma revisión del entrenador de RF-091.

## Distribución

### Por prioridad y tipo — el producto completo

| Prioridad      | Cantidad |     | Tipo                 | Cantidad |
| -------------- | -------- | --- | -------------------- | -------- |
| MUST           | 81       |     | WEB                  | 65       |
| SHOULD         | 13       |     | DATA                 | 24       |
| COULD          | 5        |     | HYBRID               | 16       |
| WON'T          | 9        |     | ML                   | 3        |
| Derogado       | 1        |     | AI                   | 7        |
| **En el producto** | **99** |   | **Total**            | **99**   |

La prioridad no cambió en la v4.0: sigue expresando cuánto importa cada requisito **al producto**. Lo que se agrega es la segunda dimensión.

### Por alcance — la Etapa 1

| Alcance                                     | Cantidad | Qué significa                                                                    |
| ------------------------------------------- | -------- | ---------------------------------------------------------------------------------- |
| **N1** · núcleo, no se recorta              | **59**   | Sin esto el producto no cumple lo que el cliente declaró condición de aprobación |
| N2 · comprometido                           | 19       | Se construye en la Etapa 1                                                       |
| N3 · condicionado al hito del Sprint 3      | 4        | Se construye si el circuito de prescripción cerró a tiempo                        |
| **En alcance — Etapa 1**                    | **82**   |                                                                                    |
| ⏸ DIFERIDO                                  | 23       | Fuera de la Etapa 1, dentro del producto                                         |
| ⊂ absorbido por fusión                      | 6        | RF-004, RF-023, RF-032, RF-033, RF-060, RF-107                                    |
| → degradado a regla                         | 4        | RF-098, RF-102, RF-103, RF-104                                                   |
| WON'T                                       | 9        | Fuera del producto                                                                |

*Los 23 diferidos incluyen RF-075 y RF-108, que ya eran COULD y caen con la nutrición, y RF-105, que cae con RF-006.*

### El alcance sigue por encima de la capacidad

| Conjunto     | Requisitos | Optimista (8 h) | Realista (10–12 h) | Frente a ~504 h |
| ------------ | ---------- | --------------- | ------------------ | --------------- |
| N1           | 59         | ~472 h          | 590 – 708 h        | 0,9 × a 1,4 ×   |
| N1 + N2      | 78         | ~624 h          | 780 – 936 h        | 1,2 × a 1,9 ×   |
| N1 + N2 + N3 | 82         | ~656 h          | 820 – 984 h        | 1,3 × a 2,0 ×   |

**El recorte redujo el alcance un 18 %, no lo que hacía falta.** Lo que la votación retiró —nutrición, comentarios, paneles agregados, parametrización, mapa muscular— es barato; lo que confirmó por mayoría amplia es el ciclo central, que es donde está el trabajo. **El núcleo solo cabe si todo sale bien y nada más se construye.**

Y el denominador de esa cuenta está en duda: las ~504 h de [D12/§3](../planning/risks-and-assumptions.md) suponen que tres de las nueve personas no construyen software, mientras que el Documento de Planificación afirma lo contrario de forma explícita. Ver la inconsistencia **I-09** del [baseline de alcance](../planning/baseline-alcance-2026-09.md). Conviene resolver el denominador antes de discutir el numerador.

### Verificación de dependencias

Los tres ciclos de la versión anterior siguen eliminados. **Cinco fusiones de la v4.0 retiran además tres dependencias que existían sólo para unir un requisito con el que lo completaba**: RF-107 → RF-036 (que además era la dependencia invertida señalada en la v3.3), RF-060 → RF-059 y RF-023 → RF-038.

Ningún requisito de banda N1 depende de uno diferido. Dos comprobaciones que hubo que hacer y conviene dejar escritas:

- **RF-031** (sustituir un ejercicio durante la sesión, banda N2) depende de RF-059, que es N1. Correcto.
- **RF-089** (propuesta de adaptación, N1) depende de RF-059 para el ajuste de sustitución. RF-059 es N1. Correcto.
- **RF-101** conserva diferida la sustitución automática; RF-018 entra en alcance por la decisión 2026-10-05. RF-117, RF-119 y RF-120 permanecen diferidos. Solicitar generación no habilita un candidato editable.

### Qué está implementado

**Nada.** Verificado sobre los tres repositorios el 2026-09-01. `proyecto-gimnasio-back` tiene Express, CORS, `/health`, `/ready`, cliente Prisma y pipeline de migraciones, con `schema.prisma` **sin un solo modelo**. `proyecto-gimnasio` tiene el andamiaje de Vite y React con una pantalla de bienvenida. `proyecto-gimnasio-ia` tiene un paquete Python vacío con sus dependencias declaradas. Las ramas `develop` y `test` son idénticas a `main` en los tres.

Esto es una ventaja mientras dure: **todas las decisiones de esquema de este documento pueden tomarse sin coste de migración, pero sólo hasta la primera migración de Prisma.**
