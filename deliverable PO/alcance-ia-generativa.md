# Alcance de la IA — capa generativa

|             |                                          |
| ----------- | ---------------------------------------- |
| **Para**    | Product Owner                            |
| **Versión** | 2.2 |
| **Fecha** | 2026-10-05 |
| **Alcance** | Sólo la IA generativa. La parte predictiva (sugerir carga sesión a sesión, proyectar progreso a futuro) no entra en este entregable. |

Este documento resume qué resuelve la IA del sistema, cómo funciona a grandes rasgos y qué nos comprometemos a entregar. **El alcance comprometido es un piso: puede ensancharse hacia el final del proyecto.**

---

**Decisión incorporada:** [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md). El catálogo se importa de RepDB y cada gimnasio habilita su disponibilidad; IA recibe toda esa lista y el contexto del alumno. Diseño pendiente de implementación.

## 1. Qué resuelve la IA

Toda la capacidad de decisión del sistema la resuelve un modelo de lenguaje (IA generativa). A partir del contexto del alumno —perfil, objetivo, condiciones físicas, nivel, equipamiento del gimnasio e historial de entrenamiento— el sistema:

- **Entiende un pedido en lenguaje natural.** El entrenador o el alumno describen lo que necesitan con sus palabras y el sistema lo traduce a parámetros concretos, que se muestran para confirmar antes de usarlos.
- **Determina el tipo de rutina** adecuado según el perfil y el objetivo.
- **Arma la rutina completa** sobre los ejercicios que el gimnasio efectivamente tiene disponibles.
- **Evalúa la adecuación:** considera condiciones, nivel, objetivos y equipamiento, explica su criterio y puede declarar que no hay una propuesta adecuada.
- **Explica en lenguaje claro** los criterios con los que se armó o ajustó una rutina.
- **Ofrece alternativas** cuando un ejercicio no se puede hacer, dentro de lo compatible con el alumno.

---

## 2. Qué garantiza el sistema alrededor del modelo

El modelo decide selección y entrenamiento; el sistema controla lo siguiente. Esos controles técnicos no garantizan que la prescripción sea adecuada:

- **La revisión del entrenador.** Ninguna rutina llega vigente a un alumno sin que un entrenador con asignación vigente la haya aprobado. Sin excepciones, cualquiera sea el origen de la rutina.
- **Referencias y disponibilidad se verifican en código.** Sólo se admiten IDs enviados y habilitados en el gimnasio, con contexto vigente. La adecuación y los valores de entrenamiento se evalúan con IA y revisión del entrenador; no con filtros o tablas deterministas.
- **Los textos narrativos no inventan números.** Citan datos recibidos; el generador sí decide nuevos valores de prescripción que quedan sujetos a revisión.
- **Una salida inválida no se muestra.** Se reintenta una vez; si vuelve a fallar, la capacidad se declara no disponible y no se presenta nada.

---

## 3. Fuera de alcance asegurado

**IA predictiva:** sugerir la carga de la próxima serie y proyectar la trayectoria de fuerza y mediciones. Es otra técnica (modelos de series temporales) y se trataría aparte.

**Estimación de riesgo de abandono:** retirada del producto. Requiere meses de actividad sobre cientos de usuarios para tener sustento, y el proyecto no va a tener esos datos.

---

## 3.1 Qué cambió con el recorte de alcance del 2026-09-01, y qué hace falta confirmar

El equipo votó el alcance de esta etapa y el resultado toca dos cosas de este documento. Ver el [baseline de alcance](../planning/baseline-alcance-2026-09.md).

**Lo que hay que confirmar con el Product Owner:**

- **La interpretación de lenguaje natural (§1, primer punto) obtuvo 3 votos de 8.** Está comprometida en este documento y por eso se conserva en el alcance, pero el equipo no la quiere en esta etapa. La alternativa es cargar los mismos parámetros por formulario. **Es una decisión del Product Owner: o libera el compromiso, o se construye pese al voto.**

**Lo que hay que saber aunque no requiera decisión:**

- **Ya no hay rutinas predefinidas de contingencia.** El equipo resolvió generar todas las rutinas desde cero. Si el servicio del modelo no está disponible, la única vía que queda es que un entrenador arme y asigne una rutina a mano. **Un alumno nuevo en un gimnasio que todavía no tiene ninguna rutina cargada, con el servicio caído, no recibe plan.** La forma de evitarlo es operativa: cargar dos o tres rutinas base al dar de alta cada gimnasio.

---

## 4. Cómo funciona

- **Un solo modelo de lenguaje**, alojado en la infraestructura de la Universidad/Polo de San Francisco o en la nube.
- El servicio IA recibe una solicitud persistida por backend, procesa en forma asíncrona y llama al LLM del Polo; el modelo no accede a las tablas de negocio.
- El modelo se puede cambiar o actualizar sin tocar el resto del sistema.
- Cada respuesta del modelo se **valida en formato** antes de usarse; si no cumple, se reintenta una vez.
- **Ninguna rutina llega al alumno sin que el entrenador la revise y la apruebe.** Esa revisión humana es la garantía del sistema, cualquiera sea el origen de la rutina.
- El modelo **nunca** pone una rutina en vigencia por su cuenta y no da indicaciones médicas.
- Si el modelo no está disponible en un momento dado, la creación y adaptación de rutinas queda temporalmente fuera de servicio y el sistema lo informa; todo lo demás —registro de sesiones, consulta de rutinas e indicadores, revisión del entrenador— sigue funcionando con normalidad. Los mismos parámetros se pueden cargar por formulario mientras tanto.

---

## 5. Cómo se verifica

- Un conjunto fijo de casos de prueba que se corre antes de cambiar cualquier configuración del modelo.
- Se comprueban formato, referencias, contexto y capacidad. Se evalúan adecuación y cumplimiento del pedido con un entrenador, midiendo correcciones y rechazos por separado.

---

## 6. Riesgos y supuestos

- **En hardware modesto, la respuesta puede tardar más de lo previsto**, sobre todo para rutinas largas. Alternativas: usar un modelo más chico o ampliar el tiempo aceptable para generar una rutina.
- **Mantener ese servidor** (actualizaciones, monitoreo) hay que acordarlo con el Polo Educativo. Caso de un servidor en la nube hay que evaluar costos y monitorearlo.
- **El modelo puede proponer una rutina con errores o incompatibilidades.** Lo cubre la revisión obligatoria del entrenador; medimos la tasa de rechazo para detectarlo temprano.
