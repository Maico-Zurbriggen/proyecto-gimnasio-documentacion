# IA predictiva

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto                                            |
| **Depende de** | [D5](../domain/business-rules.md), [D8](../requirements/functional-requirements.md), [D9](../requirements/non-functional-requirements.md), [D11/DD-15, DD-31, DD-34](../decisions/design-decisions.md), [analytics-engine.md](analytics-engine.md), [generative-ai.md](generative-ai.md) |

Este documento cubre los **objetivos, features, evaluación y ciclo de vida** de los componentes aprendidos. La mecánica del pipeline batch (extracción, validación, features point-in-time, entrenamiento, persistencia) ya está definida en [analytics-engine.md](analytics-engine.md) y no se repite acá.

## 1. Qué es predictivo y qué no

Por [D11/DD-31](../decisions/design-decisions.md), el diagnóstico (RN-79a), los ajustes (RN-89a), la compatibilidad (RN-44a-d) y la derivación del tipo de rutina (RN-39a) son **tablas deterministas**, no modelos aprendidos — están escritas, son auditables y no entran en este documento. Lo que sigue son **dos componentes** donde sí hay aprendizaje automático, ambos sobre series temporales, ninguno generativo, ninguno con respaldo directo del cliente (son propuestas de esta ronda de diseño — RF-121 y RF-122, ver el aviso en cada uno):

| Objetivo | Requerimiento | Tipo de tarea |
| --- | --- | --- |
| Sugerencia de carga de sesión `[propuesta 🆕, no validada con el cliente]` | RF-121 | Regresión sobre la tendencia reciente del alumno |
| Proyección de fuerza y mediciones corporales `[propuesta 🆕, no validada con el cliente]` | RF-122 | Proyección de serie temporal |

Ninguno de los dos usa un LLM para el cómputo: son problemas de serie temporal, no de lenguaje. Uno de ellos (RF-121) se **invoca** de forma síncrona desde el flujo de registro de sesión (FL-05), pero eso no cambia qué técnica lo resuelve.

**RF-121 y RF-122 no tienen pedido explícito del cliente detrás** (a diferencia del resto del corpus, evidenciado en RF-086 a RF-094 y decisiones del cliente — ver [D11/DD-01](../decisions/design-decisions.md)). Surgieron de dos preguntas concretas planteadas durante el diseño de esta arquitectura: qué pasa entre sesión y sesión dentro del mismo ciclo de dos semanas (nada, hoy — hueco real entre RF-030 y RN-89a), y cómo dar una proyección de progreso sin inventar una cifra que el sistema no puede sostener. Quedan documentadas con prioridad SHOULD, marcadas `[S-11]` en [D12](../planning/risks-and-assumptions.md), y primeras en el orden de recorte — deben confirmarse con el cliente antes de construirse.

### 1.1 Qué se movió fuera de este documento y por qué

Hasta el replanteo de IA del 2026-08-28 este documento describía cinco componentes aprendidos. Tres se reubicaron ([D11/DD-34](../decisions/design-decisions.md)):

| Antes | Ahora |
| --- | --- |
| **Ranking de alternativas de sustitución (RF-059, RF-060)** — modelo clásico de similitud sobre atributos estructurados | Lo produce la **capa generativa** al pedírsele ejercicios parecidos, sobre el subconjunto del catálogo prescribible ya prefiltrado de forma determinista por patrón de movimiento y compatibilidad (RN-44a-d). Ver [generative-ai.md §7](generative-ai.md). El orden alfabético por participación muscular de RN-49a queda como **fallback determinista** cuando el LLM no responde. |
| **Riesgo de abandono (RF-061 a RF-063)** — clasificación binaria / score de riesgo | **Descartado.** RF-061 a RF-063 pasan a WON'T por costo y esfuerzo relativos al valor esperado con los datos disponibles (S-03 `NO VERIFICADO`). No se degrada a una regla simple: se retira. El criterio de urgencia de la cartera (RF-107) deja de incluir el riesgo de abandono. Ver [D12/§4](../planning/risks-and-assumptions.md). |
| **Segmentación de perfiles (RF-064)** — clustering no supervisado sobre la base del gimnasio | La **descripción de perfil** la produce la capa generativa a partir de los indicadores ya calculados (frecuencia, volumen, intensidad relativos) y el objetivo del alumno, sin clustering. Es **efímera** — se genera al abrir la vista, no se persiste. Ver [generative-ai.md §1](generative-ai.md). |

## 2. Objetivo 1 — Sugerencia de carga de sesión (RF-121) `[propuesta, no validada con el cliente]`

| | |
| --- | --- |
| **Variable objetivo** | Carga y repeticiones sugeridas para la próxima serie de un ejercicio, dentro de la sesión de hoy |
| **Qué cubre hoy sin esto** | RF-030 precarga con el valor de la **última ejecución**, sin ajuste. RN-89a ajusta la prescripción cada dos semanas, a nivel de rutina, no de sesión. Entre ambos hay un hueco: de una sesión a la siguiente, dentro del mismo ciclo, nada sugiere progresión — el alumno decide solo si sube el peso (FL-05, paso 6) |
| **Features** | Tendencia de carga máxima estimada (e1RM) de las últimas sesiones en ese ejercicio, tendencia de esfuerzo percibido, cumplimiento de repeticiones reciente, si la última serie fue registrada como atípica (RN-55a) |
| **Datos históricos necesarios** | `RegistroSerie` del propio alumno en ese ejercicio — **no necesita datos de otros alumnos**: es un modelo por alumno-ejercicio, o una regla aplicada sobre la serie temporal individual. Esto lo hace viable incluso sin una base grande de usuarios (mitiga parcialmente S-03) |
| **Frecuencia de entrenamiento** | No aplica si se implementa como regla de progresión (p. ej. doble progresión: sube carga cuando se cumple el techo de repeticiones N sesiones seguidas); mensual si se implementa como modelo aprendido por segmento de alumnos |
| **Frecuencia de inferencia** | En el momento de precargar la serie (FL-05, paso 5), síncrono con la carga de la sesión — presupuesto de latencia acotado por RNF-06/RNF-07 (usabilidad de la pantalla de sesión), no por RNF-04 (que es del flujo generativo) |
| **Horizonte temporal** | Una sesión hacia adelante |
| **Criterio de referencia (baseline, RF-073)** | **RF-030 tal como existe hoy**: repetir el valor de la última ejecución. Es un baseline inusualmente fuerte y ya construido — cualquier sugerencia aprendida debe demostrar que mueve el cumplimiento o el esfuerzo percibido en una dirección mejor, no sólo que "parece razonable" |
| **Riesgo de leakage** | Bajo relativo al objetivo 2 (es intra-alumno, intra-ejercicio), pero la evaluación igual debe respetar el orden temporal: no usar sesiones futuras para sugerir una sesión pasada |
| **Piso de seguridad** | La sugerencia nunca reemplaza el mínimo de RF-030; si no hay tendencia suficiente (pocas sesiones registradas, datos contradictorios), se muestra exclusivamente el valor de RF-030. El alumno siempre confirma o corrige (FL-05, paso 6) — esto nunca se convierte en una prescripción automática |

## 3. Objetivo 2 — Proyección de fuerza y mediciones corporales (RF-122) `[propuesta, no validada con el cliente]`

| | |
| --- | --- |
| **Variable objetivo** | Trayectoria proyectada de la carga máxima estimada por ejercicio y de las mediciones corporales (`MedicionCorporal`: peso, perímetros) si el alumno continúa con un patrón de entrenamiento similar al de las últimas semanas |
| **Por qué no es "predicción de músculo ganado"** | El sistema no mide composición corporal: la enumeración cerrada de [D2 §4.11](../product/glossary.md) tiene 6 valores (peso y 4 perímetros), sin masa muscular ni porcentaje de grasa, y no hay instrumento (bioimpedancia, pliegues) que los capture. [D2 §2 — Términos prohibidos](../product/glossary.md) ya excluye "calorías quemadas" y "puntaje de fitness" por no ser estimables con la información disponible; la misma razón aplica a una cifra de músculo ganado. Este objetivo proyecta **exactamente lo que el sistema ya deriva o registra** (e1RM, perímetros) y se presenta con esos nombres, nunca como composición corporal |
| **Features** | Serie temporal de carga máxima estimada por ejercicio; serie temporal de cada tipo de medición corporal registrada; adherencia del período (una proyección sobre una tendencia inestable es menos confiable y debe decirlo) |
| **Datos históricos necesarios** | `RegistroSerie` (para e1RM) y `MedicionCorporal` del propio alumno — igual que el objetivo 1, es por alumno, no depende de una base grande de usuarios |
| **Frecuencia de entrenamiento/inferencia** | A demanda, cuando el alumno consulta su panel de progreso (RNF-02) |
| **Horizonte temporal** | Semanas, a definir junto con el criterio de "patrón similar" — `NO VERIFICADO`, requiere acuerdo con el cliente sobre qué horizonte es útil sin volverse una promesa poco creíble |
| **Criterio de referencia (baseline)** | Extrapolación lineal simple de la tendencia reciente (regresión lineal sobre las últimas N semanas). Un modelo más complejo debe superar esto antes de promoverse (RF-073) |
| **Guardrail obligatorio** | Toda proyección se presenta con su incertidumbre (banda, no un único número) y con la declaración explícita de que es una proyección bajo continuidad de patrón, no una promesa de resultado — mismo principio que RF-012 y RF-108. Si el componente narrativo (capa generativa) redacta esta proyección en texto, se le aplica exactamente la misma verificación de valores citados que a RF-055/RF-056 (ver [generative-ai.md §9](generative-ai.md)): el número proyectado tiene que provenir literalmente de este cálculo, nunca inventarse en la redacción |
| **Riesgo de leakage** | Igual que el objetivo 1: intra-alumno, pero respetar el orden temporal en la evaluación |

## 4. Ciclo de vida (referencia)

El pipeline mecánico (extracción de snapshot, validación de esquema, features point-in-time, entrenamiento, evaluación contra el criterio de referencia, persistencia idempotente) está descrito en [analytics-engine.md §Pipeline](analytics-engine.md). Lo que agrega este documento:

```text
Datos (PostgreSQL, snapshot versionado)
 ↓
Preparación + features point-in-time (motor Python)
 ↓
Training  ──sólo si hay volumen suficiente; si no, se usa el criterio de referencia──
 ↓
Evaluación contra criterio de referencia (RF-073, obligatoria, no opcional)
 ↓
¿Supera al criterio de referencia?
 ├─ No → se conserva el criterio de referencia, se documenta el resultado (E9)
 └─ Sí → Model registry mínimo: un identificador de versión + métricas, persistido junto al resultado (RF-072)
 ↓
Inferencia (batch/a demanda para el objetivo 2; síncrona por alumno-ejercicio para el objetivo 1)
 ↓
Monitoreo (§7)
 ↓
Reentrenamiento (mensual o a demanda)
```

**No se implementa un model registry ni feature store como los de un equipo de MLOps de producto**: dado el tamaño del proyecto (equipo universitario, capacidad de construcción de 504 h — [D12/§3](../planning/risks-and-assumptions.md)), el "registro" es la tabla `EvaluacionComponente` ya prevista en el [modelo de dominio](../domain/domain-model.md) (componente, versión, dataset, tamaño de muestra, métricas obtenidas, métricas del criterio de referencia, fecha) más el archivo serializado del modelo versionado por nombre de archivo. Es proporcional al tamaño real del proyecto (no sobreingeniería, §29 de la tarea de origen).

**El objetivo 1 (§2, RF-121) no es batch.** Es una computación liviana por alumno-ejercicio (no poblacional), invocada de forma síncrona al precargar una serie (FL-05, paso 5). No entrena un modelo poblacional ni tiene ciclo de reentrenamiento mensual en el mismo sentido que el objetivo 2; su "entrenamiento" es, en el caso más simple, recalcular una tendencia sobre la serie temporal del propio alumno en el momento de la consulta. Se documenta la excepción para que no se le exija un pipeline batch que no necesita.

## 5. Evaluación

| Objetivo | Métrica principal | Por qué |
| --- | --- | --- |
| Sugerencia de carga de sesión | Comparación contra RF-030: ¿la serie sugerida se completa con mejor cumplimiento o esfuerzo percibido más estable que repetir el último valor? | Mide si la sugerencia mejora sobre el baseline ya construido, no si "parece razonable" |
| Proyección de fuerza/mediciones | Error absoluto entre la proyección hecha en la semana N y el valor efectivamente observado en la semana N+k, contra el mismo error de la extrapolación lineal simple | Es forecasting: se evalúa contra lo que realmente pasó después, igual que cualquier proyección de serie temporal |

Sobre ambos: split train/validation/test respetando el orden temporal (nunca aleatorio — evitaría el leakage), y comparación obligatoria contra el criterio de referencia de cada objetivo (RF-073, RNF-26). Que el criterio simple gane es un resultado válido y debe informarse, no ocultarse — es la postura ya adoptada en D11/DD-31 y el propio D12/R-16.

**Detección de sobreajuste**: la métrica de validación y la de test deben mantenerse dentro de un margen declarado (a definir en la implementación); una brecha grande entre ambas invalida la promoción del modelo, con independencia de si superó al criterio de referencia en validación.

## 6. Datos y calidad

- **Cantidad y representatividad**: dependen de S-03 (`NO VERIFICADO`). Si no hay historial real suficiente al momento de entrenar, se usa exclusivamente el criterio de referencia para cada objetivo y se declara explícitamente que el componente aprendido no está activo (RNF-12, DD-15: la ausencia del proceso no degrada el resto del sistema).
- **Datos simulados** (RF-071): identificados sin ambigüedad y excluidos de toda analítica presentada como real (DD-20, RNF-28). Un modelo entrenado sólo con datos simulados no debe presentarse como si generalizara a comportamiento real; se documenta esa limitación junto al resultado.
- **Datos faltantes**: ausencia de dato no equivale a cero (invariante ya declarada en [analytics-engine.md](analytics-engine.md)) — un alumno sin esfuerzo percibido registrado no cuenta como esfuerzo percibido 0, cuenta como no evaluado en ese criterio (RN-81, precedente ya establecido).
- **Privacidad**: las features usadas son indicadores agregados y de comportamiento (adherencia, volumen, frecuencia, e1RM), no descripciones libres de condiciones físicas. El motor batch no debe recibir campos de texto libre con datos de salud como feature de un modelo — sólo los campos tipados que D4/D5 ya definen como calculables.

### 6.1 Datasets externos evaluados para entrenar

Búsqueda de datasets públicos que pudieran acelerar el arranque de los objetivos 1 y 2, evitando el problema de partir de cero (S-03). Conclusión calibrada, sin sobrevender lo encontrado:

| Dataset | Contenido | Licencia | Utilidad real para este proyecto |
| --- | --- | --- | --- |
| [OpenPowerlifting](https://www.openpowerlifting.org/faq) | Resultados de competencias de powerlifting (sentadilla, banco, peso muerto) por atleta, a lo largo de años, a gran escala | Datos en dominio público (CC0) | Útil **sólo para el objetivo 2** (proyección de fuerza), y como validación de metodología, no como datos de entrenamiento directos: son atletas de competencia, no alumnos de gimnasio en general, y son intentos máximos en competencia, no series de entrenamiento |
| [free-exercise-db](https://github.com/yuhonas/free-exercise-db) | Catálogo de +800 ejercicios con clasificación muscular, equipamiento e instrucciones | Dominio público | No es un dataset de entrenamiento de modelos: es un candidato para la **carga inicial del catálogo** (RF-070, RF-099, S-09 en D12), un problema distinto y ya identificado en el corpus. Vale la pena evaluarlo para ese propósito, no para éste |
| Datasets de Kaggle de "gym workouts" (varios, ej. *Gym Members Exercise Dataset*, *721 Weight Training Workouts*) | Variado: algunos son resúmenes agregados por socio (no series temporales por sesión), otros son el registro de una sola persona durante varios años | Variable, revisar por dataset | El de una sola persona no generaliza a una población; los agregados no tienen el detalle serie-por-serie que exige `RegistroSerie`. Para los objetivos 1 y 2, al ser por alumno, el propio historial del alumno es lo que importa, no una base externa |

**Conclusión, sin dar vueltas:** no existe un dataset público que reemplace la necesidad de datos propios del sistema. Para los objetivos 1 y 2, al ser por alumno (no poblacionales), el propio historial del alumno alcanza sin necesidad de una base externa — son los objetivos menos expuestos al riesgo S-03, además de ser los menos evidenciados por el cliente (S-11). Mientras el historial real no exista, se usan datos simulados (RF-071) con la limitación siempre declarada (DD-20, RNF-28).

## 7. Monitoreo posterior

- **Latencia**: para el objetivo 2 (batch/a demanda) se mide el tiempo del job completo, no de una predicción individual. Para el objetivo 1 (síncrono, dentro de FL-05) se mide como cualquier otra respuesta del backend, contra RNF-06/RNF-07.
- **Drift**: distribución de las features de entrada de una ejecución comparada contra la anterior; un cambio abrupto (p. ej. tras una migración de datos) debe alertar antes de publicar resultados nuevos.
- **Performance**: la métrica de §5 recalculada en cada reentrenamiento, conservada junto con la del criterio de referencia (RF-073), nunca sólo la del modelo aprendido.
- **Versión del modelo**: todo resultado persistido referencia la versión del componente que lo produjo (RF-072), ya modelado en `EvaluacionComponente`.
