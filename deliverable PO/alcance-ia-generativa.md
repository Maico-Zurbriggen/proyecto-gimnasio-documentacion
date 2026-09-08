# Alcance de la IA — capa generativa

|             |                                          |
| ----------- | ---------------------------------------- |
| **Para**    | Product Owner                            |
| **Versión** | 2.1                                     |
| **Fecha**   | 2026-08-28                              |
| **Alcance** | Sólo la IA generativa. La parte predictiva (sugerir carga sesión a sesión, proyectar progreso a futuro) no entra en este entregable. |

Este documento resume qué resuelve la IA del sistema, cómo funciona a grandes rasgos y qué nos comprometemos a entregar. **El alcance comprometido es un piso: puede ensancharse hacia el final del proyecto.**

> **Vigencia (2026-09-08, baseline v4.1):** el compromiso funcional (§1–§3) sigue vigente. Quedaron desactualizados dos detalles de implementación de §4: el servicio corre como proceso Python propio en el Polo con worker durable ([ADR-0009](../decisions/adr/0009-servicio-generativo-online-en-el-polo.md)), no dentro del backend; y plantillas/presets son alcance opcional `COULD` (RF-019 a RF-021), por lo que ante indisponibilidad no hay vía manual de contingencia ([DD-35](../decisions/design-decisions.md)). Ver §3.1.

---

## 1. Qué resuelve la IA

Toda la capacidad de decisión del sistema la resuelve un modelo de lenguaje (IA generativa). A partir del contexto del alumno —perfil, objetivo, condiciones físicas, nivel, equipamiento del gimnasio e historial de entrenamiento— el sistema:

- **Entiende un pedido en lenguaje natural.** El entrenador o el alumno describen lo que necesitan con sus palabras y el sistema lo traduce a parámetros concretos, que se muestran para confirmar antes de usarlos.
- **Determina el tipo de rutina** adecuado según el perfil y el objetivo.
- **Arma la rutina completa** sobre los ejercicios que el gimnasio efectivamente tiene disponibles.
- **Verifica la compatibilidad:** revisa que ningún ejercicio choque con una condición física del alumno, supere su nivel o requiera equipamiento que el gimnasio no tiene.
- **Explica en lenguaje claro** los criterios con los que se armó o ajustó una rutina.
- **Ofrece alternativas** cuando un ejercicio no se puede hacer, dentro de lo compatible con el alumno.

---

## 2. Qué garantiza el sistema alrededor del modelo

El modelo no decide solo. Cuatro garantías lo rodean, y ninguna depende de que el modelo se comporte bien:

- **La revisión del entrenador.** Ninguna rutina llega vigente a un alumno sin que un entrenador con asignación vigente la haya aprobado. Sin excepciones, cualquiera sea el origen de la rutina.
- **La compatibilidad se verifica en código, no en el modelo.** Que un ejercicio esté contraindicado por una condición física, exceda el nivel del alumno o requiera equipamiento que el gimnasio no tiene, lo determina una regla escrita y auditable, antes de construir la propuesta y otra vez antes de presentarla.
- **Los textos no inventan números.** Un texto generado no puede contener un valor numérico que no esté en los datos que recibió. Es exigible al 100 % y se verifica de forma automática.
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
- Corre **como parte del backend del sistema**.
- El modelo se puede cambiar o actualizar sin tocar el resto del sistema.
- Cada respuesta del modelo se **valida en formato** antes de usarse; si no cumple, se reintenta una vez.
- **Ninguna rutina llega al alumno sin que el entrenador la revise y la apruebe.** Esa revisión humana es la garantía del sistema, cualquiera sea el origen de la rutina.
- El modelo **nunca** pone una rutina en vigencia por su cuenta y no da indicaciones médicas.
- Si el modelo no está disponible en un momento dado, la creación y adaptación de rutinas queda temporalmente fuera de servicio y el sistema lo informa; todo lo demás —registro de sesiones, consulta de rutinas e indicadores, revisión del entrenador— sigue funcionando con normalidad. Los mismos parámetros se pueden cargar por formulario mientras tanto.

---

## 5. Cómo se verifica

- Un conjunto fijo de casos de prueba que se corre antes de cambiar cualquier configuración del modelo.
- Se mide: que los textos nunca mencionen un número que no esté en los datos de origen y que las respuestas tengan el formato esperado.

---

## 6. Riesgos y supuestos

- **En hardware modesto, la respuesta puede tardar más de lo previsto**, sobre todo para rutinas largas. Alternativas: usar un modelo más chico o ampliar el tiempo aceptable para generar una rutina.
- **Mantener ese servidor** (actualizaciones, monitoreo) hay que acordarlo con el Polo Educativo. Caso de un servidor en la nube hay que evaluar costos y monitorearlo.
- **El modelo puede proponer una rutina con errores o incompatibilidades.** Lo cubre la revisión obligatoria del entrenador; medimos la tasa de rechazo para detectarlo temprano.
