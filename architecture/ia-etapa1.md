# Documentación de IA — Etapa 1 (Vivaz Adaptive)

|                |                                                                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Versión**    | 1.0                                                                                                                                                      |
| **Fecha**      | 2026-09-08                                                                                               |
| **Estado**     | Propuesto                                                                                                                                                |
| **Depende de** | [D5](../domain/business-rules.md), [D8](../requirements/functional-requirements.md), [baseline](../planning/baseline-alcance-2026-09.md), [generative-ai](generative-ai.md), [generative-ai-integration](generative-ai-integration.md), [ai-model-selection](ai-model-selection.md), [predictive-ai](predictive-ai.md) |

Ficha operativa de la inteligencia en la Etapa 1. El diseño completo vive en [generative-ai](generative-ai.md), [generative-ai-integration](generative-ai-integration.md) y [predictive-ai](predictive-ai.md); aquí sólo el recorte vigente, los contratos en uso, las garantías exigibles y los puntos abiertos.

## 1. Alcance vigente: qué corre y qué no

| Corre en Etapa 1 | RF | Banda | No corre en Etapa 1 |
| ---------------- | -- | ----- | ------------------- |
| `interpretarPedido` (NL → parámetros) | RF-053 | N2 | `resumirProgreso` (RF-056, diferido) |
| `generarRutina` (estructura, sin candidato ajustable) | RF-054, RF-087 | N1 | `describirPerfil` (RF-064, N3) |
| `explicarCriterios` (justificación) | RF-055 | N1 | Predictiva RF-121/RF-122 (propuestas no validadas, diferidas) |
| `sugerirAlternativas` (+ exclusión dura) | RF-059 | N1 | Riesgo de abandono (WON'T), RAG, clustering |

**Consecuencia central:** al diferirse plantillas y presets (RF-019 a RF-021 como `COULD`), `generarRutina` es la **única vía** de prescripción automática en la Etapa 1. Ver [DD-35](../decisions/design-decisions.md).

## 2. Reparto de autoridad: quién decide qué

| Capa | Responsabilidad | Dónde vive |
| ---- | --------------- | ---------- |
| LLM (propone) | Interpreta NL, construye la estructura inicial, ordena alternativas sobre subconjunto prefiltrado, redacta justificación | Servicio Python en el Polo |
| Reglas (disponen) | RN-39a (rangos por tipo), RN-44a–44d + D5/§6 (compatibilidad), RN-79a (diagnóstico), RN-89a (ajustes) | Backend, código determinista |
| Humano (autoriza) | Revisión de rutina y resolución de propuestas | Entrenador, sin excepciones (RN-35, RA-07) |

El diagnóstico y los ajustes **no** son modelos aprendidos: son tablas explícitas y auditables. Ningún componente narrativo introduce valores ausentes de su entrada (RN-94, exigible al 100 %).

## 3. Contratos en uso

Flujo: solicitud idempotente → `202` aceptado → worker + LLM (límite 120 s por intento) → validación en backend → PROPUESTA → revisión. Frontend hace polling sólo contra el backend; el LLM nunca toca PostgreSQL.

| Método | Entrada | Salida y validación |
| ------ | ------- | ------------------- |
| `interpretarPedido` | Texto libre + contexto mínimo | JSON de enumeraciones cerradas; se confirma con el usuario antes de usarse |
| `generarRutina` | Parámetros + contexto del alumno + catálogo prescribible | Estructura días→ejercicios→series con ids del catálogo; valida RN-39a + §6, 1 reintento (RN-95b, RF-113) |
| `explicarCriterios` | Estructura validada | Texto + `valores_citados`; cada número debe existir en la entrada (RNF-24) |
| `sugerirAlternativas` | Ejercicio + subconjunto prefiltrado (mismo patrón, compatibles) | Hasta 5 ids **de la lista de entrada**; fuera de lista se descarta; fallback a orden RN-49a |

**Privacidad del prompt:** objetivo, nivel, condiciones por zona/severidad (sin descripción libre), inventario, prescribible e indicadores agregados. Nunca: credenciales, correo, texto libre de salud, datos de otro alumno u otro gimnasio. Sin prompts completos ni salud en logs persistentes (RNF-19).

## 4. Guardrails exigibles

1. Salida inválida → 1 reintento → indisponibilidad declarada; jamás se presenta una propuesta inválida ni un error técnico (RN-95b, RNF-11).
2. Cero valores numéricos inventados en texto narrativo, verificado automáticamente (RN-94, RNF-24, criterio E10).
3. Sin indicaciones médicas, diagnósticos clínicos ni recomendaciones de tratamiento (RN-96, RF-057).
4. Sin contexto suficiente no se decide: se declara qué falta (RN-97b, RF-111).
5. Toda salida registra versión de componente/modelo/prompt, contexto e instante (RN-98, RF-072).
6. Inyección de prompt confinada: ninguna regla de negocio depende de que el modelo la respete; la barrera es la validación determinística (RNF-41).

## 5. Evaluación

Casos y métricas canónicos en [generative-ai §10](generative-ai.md) (conjunto fijo versionado con los prompts; CI automática: valores no verificables al 0 %, fallos de schema, reintentos, p95 vs 120 s). Cambio de prompt/modelo/parámetros exige regresión verde + validación de un entrenador; el modelo nuevo debe igualar o superar al vigente (RF-073). Criterio E9: cada componente se compara contra su referencia simple y ambas métricas se conservan.

## 6. Modelo, runtime y operación

Qwen3.5-9B-Instruct (GGUF `Q4_K_M`, ~6 GB sobre 48 GB VRAM verificados → perfil A confirmado, margen para `num_ctx` amplio y concurrencia) sobre Ollama **con soporte Qwen3.5** (arquitectura híbrida: congelar versión mínima al desplegar), detrás de `GenerativeAiPort` (`OllamaAdapter`); vLLM documentado como ruta de escalamiento. Configuración del Gateway: `think: false`, temperatura 0,1–0,3. **Tools: sí, restringido** a `verificarCompatibilidad` y sólo tras pasar el conjunto de casos de [generative-ai §10](generative-ai.md) (mismatch XML/Hermes en Ollama); hasta entonces single-shot JSON + validación determinística posterior. Topología, operación y ambientes en [generative-ai-integration](generative-ai-integration.md); métricas por método en [generative-ai §14](generative-ai.md).

## 7. Puntos abiertos y deuda (no ocultar)

1. **Hardware del Polo verificado (VRAM): 48 GB** `[F: dato del equipo, 2026-09-08]` → perfil A confirmado con amplio margen. Pendiente: versión de Ollama con soporte Qwen3.5 en el Polo y medición del p95 contra RNF-04 con el conjunto de §10.
2. **ADR-0004 vs ADR-0005**: dos decisiones «aceptadas» incompatibles sobre la ubicación del Gateway; resolver antes de integrar (recomendación del baseline §H.4: prevalece ADR-0004, conservar puerto+adaptador).
3. **Sin plantillas ni presets obligatorios**: plantillas y presets son alcance opcional (`COULD`), por lo que no forman parte del piso obligatorio de disponibilidad.
4. Deuda documental del baseline §O: alinear RF-058/RN-95b/ADR-0004 considerando plantillas y presets como alcance COULD.
