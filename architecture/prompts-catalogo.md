# Catálogo de prompts del sistema — jerarquía y pasos

|                |                                                                                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Versión**    | 1.0                                                                                                                                                                                                              |
| **Fecha**      | 2026-09-08                                                                                                                                                                                                       |
| **Estado**     | Propuesto                                                                                                                                                                                                        |
| **Depende de** | [D2](../product/glossary.md), [D5](../domain/business-rules.md), [D7](../flows/functional-flows.md), [D8](../requirements/functional-requirements.md), [D9](../requirements/non-functional-requirements.md), [generative-ai](generative-ai.md), [ia-etapa1](ia-etapa1.md), [D14](../domain/contexto-alumno.md) |

Inventario operativo de **cada llamada al LLM en cada flujo de la app**: qué prompt, con qué entrada, en qué paso, con qué validación y qué pasa si falla. No redefine comportamiento: lo canónico son los RF/RN citados; el diseño vive en [generative-ai](generative-ai.md) y el recorte vigente en [ia-etapa1](ia-etapa1.md). Donde ambos difieren (candidato, vía determinística, ubicación del Gateway), **vale la columna Etapa 1**.

Convenciones: cada prompt se versiona como `generative/<capacidad>@<n>` con changelog propio; un cambio de prompt es un cambio de código (PR + regresión §10 de generative-ai). Todo prompt separa secciones delimitadas: system, schema de salida, contexto dinámico (JSON, nunca prosa a reinterpretar), tarea. Límite 120 s por intento, 1 reintento, luego indisponibilidad declarada sin error técnico (RN-95b, RF-113, RNF-11).

## Nivel 0 — Reglas transversales a todo prompt

| # | Regla | Origen |
| - | ----- | ------ |
| P0.1 | Ningún prompt recibe texto libre salvo P1. P2–P4 reciben sólo parámetros tipados y estructuras validadas | RNF-41 |
| P0.2 | Ninguna regla de negocio depende de que el modelo la respete: RN-39a y D5/§6 validan en código toda salida de decisión | RN-95, RF-113 |
| P0.3 | Ningún narrativo introduce valores ausentes de su entrada (`valores_citados`, verificación automática, objetivo 0 %) | RN-94, RNF-24 |
| P0.4 | Ningún componente emite indicaciones médicas ni diagnósticos clínicos (prohibición en system + filtro de patrones clínicos) | RN-96, RF-057 |
| P0.5 | Sin prompts completos ni salud en logs persistentes; sólo versión de prompt/modelo, hash de entrada, latencia y resultado de validación | RNF-19 |
| P0.6 | Rate limiting por usuario antes del Gateway; métricas por método sin contenido sensible | RNF-18, generative-ai §14 |

## Nivel 1 — Prompts activos en Etapa 1

### P1 · `interpretarPedido` — NL a parámetros (RF-053, N2)

Única puerta del texto libre (observaciones generales D14/§2.7, observaciones del pedido y foco D14/§6, o descripción del solicitante FL-04/paso 1).

1. System: rol intérprete + prohibiciones P0.3/P0.4 + "respondé sólo el schema".
2. Entrada: texto libre + contexto mínimo (gimnasio, alumno) + observaciones generales vigentes.
3. Salida JSON: `objetivo` (D2/§4.5) · `frecuencia_semanal` (1–7, RN-38) · `exclusiones_texto` (ejercicios a excluir, en palabras del usuario) · `foco` (grupos/patrones) · `duracion_sesion_minutos` · `confianza`. El equipamiento mencionado se descarta: sale del inventario (caso §10 de generative-ai).
4. Backend valida enums y rangos; un valor fuera es fallo de validación, no dato. Las exclusiones en texto **no se mapean a ids por código difuso**: se muestran en la confirmación para que el usuario las resuelva a selección sobre el catálogo.
5. **Confirmación del usuario antes de propagarse** (FL-04/paso 2). Si corrige, no se reinterpreta: se editan los parámetros, incluida la resolución de exclusiones a ids.
6. Fallo de schema → 1 reintento → se pide completar el formulario estructurado (vía manual, no error).

### P2 · `generarRutina` — estructura candidata (RF-054, RF-087, N1)

Núcleo de FL-01 (alta) y FL-04. En Etapa 1 la salida válida va **directo a rutina PROPUESTA**, sin candidato ajustable.

1. System: rol constructor + "usá sólo ids del catálogo recibido" + prohibiciones P0.3/P0.4.
2. Entrada: parámetros confirmados de P1 (o valores del perfil si no hubo pedido) + snapshot del alumno (D14/§7.1: objetivo, nivel, días, condiciones como pares zona/severidad, preferencias estables, aptitud como estado, inventario, prescribible prefiltrado por patrón/compatibilidad/equipamiento, indicadores agregados).
3. Salida JSON: días → ejercicios (**ids del catálogo de entrada**) → series prescriptas (repeticiones, carga sugerida, descanso, calentamiento).
4. Validación determinista en backend: RN-39a (estructura, series, repeticiones, descansos, cobertura de patrones) + D5/§6 (RN-44a–d) + RN-97 (sólo prescribible).
5. Inválida → 1 reintento → generación deshabilitada temporalmente (RN-95b v4.1, RN-99, RF-058): **no hay generador determinístico alternativo ni plantillas de contingencia** (RF-019 a RF-021 diferidos); sin vía alternativa de prescripción en Etapa 1 (DD-35).
6. Se registra versión de componente/modelo/prompt, contexto y hash (RN-98).
7. **Regeneración / modificación (FL-04/A5): no hay prompt separado.** Se reejecuta este mismo P2 con los parámetros corregidos + la salida anterior como contexto no autoritativo + las preferencias acumuladas como entrada (RN-128, nunca como parche sobre la salida). Validación, reintento y registro idénticos a la primera pasada. La sustitución puntual dentro del armado usa P4; la edición humana directa (FL-02 con cambios, FL-11, resolución FL-10) no usa ningún prompt.

### P3 · `explicarCriterios` — justificación (RF-055, N1)

1. Entrada: **estructura ya validada** de P2 (nunca la candidata sin validar).
2. Salida JSON: `texto` + `valores_citados` (cada número/categoría mencionada).
3. Backend verifica cada citado contra la entrada (RNF-24); un valor no verificable descarta la respuesta → 1 reintento → justificación tabulada mínima (lista de criterios aplicados, sin prosa).
4. Se muestra junto a la rutina en revisión (FL-02) y al alumno tras la vigencia.

### P4 · `sugerirAlternativas` — orden de sustitutos (RF-059, absorbe RF-060, N1)

Usado en FL-04/A4 (alternativas puntuales) y FL-06 (sustitución en sesión).

1. Entrada: ejercicio a sustituir + contexto del alumno + **lista prefiltrada determinista** (mismo patrón dominante, COMPATIBLE, equipamiento presente — RN-49a/RN-44a-d). Nunca el catálogo completo.
2. Salida JSON: hasta 5 ids **de la lista de entrada**, con motivo breve por ítem.
3. Backend descarta ids fuera de lista y revalida compatibilidad (RF-113). La lista aceptada se persiste con versiones (RF-072).
4. Fallo o LLM caído → orden determinista RN-49a (primaria, luego secundaria) sin interrumpir el flujo (RN-99).

### P5 · Herramienta `verificarCompatibilidad` — condicional

Envuelve RN-44a-d en código para que P2 se autocorrija antes de terminar. **Sólo tras pasar el conjunto de casos de ia-etapa1 §10**; hasta entonces P2 es single-shot JSON + validación posterior. No reemplaza la validación final nunca.

## Nivel 2 — Prompts diferidos (diseño congelado, no se implementan)

| # | Prompt | RF | Entrada / salida | Activación |
| - | ------ | -- | ---------------- | ---------- |
| P6 | `resumirProgreso` | RF-056 (SHOULD, diferido) | Indicadores ya calculados → texto + `valores_citados` (mismo contrato que P3) | Cuando vuelva el alcance; se muestra en FL-09 junto al diagnóstico |
| P7 | `describirPerfil` | RF-064 (N3) | Frecuencia/volumen/intensidad relativos + objetivo → etiqueta + texto; **efímero, no se persiste**; sin LLM se muestran los números | Cartera FL-13 y ficha RF-037 |
| P8 | `proyectarEvolucion` (presentación) | RF-122 (diferido) | Proyección ML ya calculada + incertidumbre → texto que declara supuesto de continuidad, sin términos de composición corporal | Ficha del alumno/entrenador |
| P9 | Sin prompt propio | RF-121 (diferido) | La sugerencia es un número ML/estadístico: se presenta con template fijo, no con LLM (P0.3: un narrativo no introduce valores) | Precarga en FL-05/paso 6 junto al mínimo RF-030 |
| P10 | `generarPautaNutricional` | RF-075/RF-108 (diferidos con nutrición) | Energía y proteína ya calculadas → distribución por comida, sin nombrar alimentos | Si vuelve §13 de D5 |

## Nivel 3 — Matriz flujo → prompts (cobertura total)

Sin LLM = el flujo es determinista o humano; se declara para que ningún flujo quede sin clasificar.

| Flujo | Prompts | Paso |
| ----- | ------- | ---- |
| FL-00 aprovisionamiento | — | — |
| FL-19 invitación y alta | — | — |
| FL-01 puesta en contexto | P1 → P2 → P3 | 1 (observaciones) → 4 (generación del alta, directo a PROPUESTA) |
| FL-02 revisión y vigencia | — (humana; muestra P3 ya generado) | — |
| FL-03 solicitud por alumno | ⏸ Diferido; si vuelve: P1 → P2 → P3 | — |
| FL-04 generación asistida | P1 → P2 → P3; P4 en A4; P5 condicional en P2 | 1–2 (P1) · 3 (P2) · 5 (P3) · A4 (P4) |
| FL-05 ejecución de sesión | — (P9 diferido) | — |
| FL-06 sustitución en sesión | P4 (con fallback RN-49a) | Curso normal |
| FL-07 reanudación | — | — |
| FL-08 diferido | — | — |
| FL-09 diagnóstico | — (determinista RN-79a; P6 diferido) | — |
| FL-10 resolución de propuesta | — (humana; ajustes RN-89a deterministas) | — |
| FL-11 intervención directa | — (humana) | — |
| FL-12 reevaluación | — (determinista RN-91/92) | — |
| FL-13 cartera priorizada | — (P7 diferido) | — |
| FL-14 mediciones | — | — |
| FL-15 asignaciones | — | — |
| FL-16 | Derogado (WON'T): sin prompt por decisión, no por olvido | — |
| FL-17 catálogo | — (curación humana) | — |
| FL-18 baja y exportación | — | — |
| FL-20 inventario | — (dispara reevaluación determinista RN-117) | — |
| FL-21 paneles | — (P6/P7 diferidos) | — |

## Nivel 4 — Trazabilidad y auditoría del catálogo

RF-053 → P1 · RF-054/RF-087 → P2 · RF-055 → P3 · RF-059/RF-060 → P4 · RF-057 → P0.3/P0.4 · RF-058/RNF-11 → P2/paso 5 · RF-072/RN-98 → P2/paso 6, P4/paso 3 · RF-111/RN-97b → precondición de P1/P2 (sin contexto suficiente no se llama) · RF-113/RN-95b → reintento único en P1–P4 · RF-056 → P6 · RF-064 → P7 · RF-121 → P9 · RF-122 → P8 · RF-075/108 → P10 · RF-061–063 → sin prompt (WON'T).

**Chequeo de completitud:** los 7 métodos del Gateway (`interpretarPedido`, `generarRutina`, `explicarCriterios`, `resumirProgreso`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil` — nombres vigentes de ia-etapa1; generative-ai.md los llama `interpretarSolicitud`/`justificarRutina`/`resumirEvolucion`) tienen prompt asignado (P1, P2, P3, P6, P10, P4, P7); los 22 flujos están clasificados; ningún prompt existe sin RF que lo pida.
