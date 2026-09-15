# Arquitectura de prompts y orquestación

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto                                           |
| **Depende de** | [generative-ai.md](generative-ai.md), [generative-ai-integration.md](generative-ai-integration.md), [D7](../flows/functional-flows.md), [D8](../requirements/functional-requirements.md), [D9](../requirements/non-functional-requirements.md), [ADR-0008](../decisions/adr/0008-tool-calling-for-ml-components.md), [ADR-0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) |

## Alcance y autoridad

Este documento es canónico para **cómo se organizan los prompts y quién decide cuál se usa**. El contrato del AI Gateway, los guardrails, la evaluación y la topología de despliegue siguen en [generative-ai.md](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md); aquí no se duplican, se enlazan.

## 1. Decisión: orquestador determinístico en código, sin router LLM ni subagentes

La pregunta "¿qué necesita el usuario?" **no la responde un LLM**. La responde el código a partir de la acción de la interfaz y el estado del flujo (qué botón, en qué paso de FL-01/FL-04/FL-06, con qué estado previo). Cada acción dispara **un solo método** del Gateway.

No hay clasificador LLM de intenciones ni subagentes autónomos que se llamen entre sí. Fundamento:

- El sistema no es un chatbot abierto: son 7 tareas cerradas con entrada/salida JSON y validación determinista posterior (RF-113).
- Un router LLM agrega latencia sobre un presupuesto ya ajustado (RNF-04: 120 s por intento), un punto de fallo más (contra RNF-11) y variabilidad donde se exige validez repetida (RNF-25, RNF-27, RF-072).
- El único texto libre del sistema vive confinado en `interpretarPedido` (RNF-41). El resto recibe parámetros tipados; ninguna regla de negocio depende de que el modelo "quiera" respetarla (RN-39a, RN-44a-d).

**Reapertura:** si aparece conversación abierta multi-turno real (hoy fuera de alcance), reevaluar un clasificador LLM solo para esa rama. No antes.

## 2. Estructura: 1 base compartida + 7 plantillas especializadas

Ningún megaprompt único y ningún prompt por botón. Cada llamada compone 5 secciones, en este orden:

1. **Base system (común):** rol, idioma, "respondé solo en el schema dado", "no inventes números ausentes de la entrada", "nada médico" (RF-057).
2. **Overlay por capacidad:** lo específico de esa tarea y nada más.
3. **Schema de salida literal** (más `response_format`/`format` cuando el runtime lo soporta).
4. **Contexto dinámico como JSON**, mínimo para esa tarea (nunca prosa a reinterpretar, nunca catálogo completo sin prefiltrar).
5. **Instrucción concreta** de una línea.

La base cambia poco; cada overlay se versiona por separado como `generative/<capacidad>@<n>` con su changelog. Un cambio de schema exige versión nueva de ambos. Detalle del versionado y de lo que se registra por resultado en [generative-ai.md §15](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md).

## 3. Inventario

| Plantilla | Disparo (código, no LLM) | Entrada | Salida | Validación |
| --- | --- | --- | --- | --- |
| `interpretarPedido` (RF-053) | FL-04 paso 1, solo si hay texto libre | texto + contexto mínimo | objetivo, frecuencia 1-7, restricciones, duración, confianza | schema + enumeraciones de [D2](../product/glossary.md) + confirmación humana antes de propagarse |
| `generarRutina` (RF-054) | FL-01, FL-04 paso 3, FL-04/A5 (regeneración) | parámetros confirmados + perfil, nivel, objetivo, condiciones, inventario, catálogo prescribible | días → ejercicios por id → series/cargas/descansos + `patrones_no_cubiertos` | RN-39a y D5/§6 en código (RF-113); 1 reintento, luego indisponibilidad |
| `sugerirAlternativas` (RF-059, absorbe RF-060) | FL-04/A4, FL-06 | ejercicio + subconjunto prefiltrado en código (mismo patrón, compatibles, con equipamiento) | hasta 5 ids de esa lista + motivo corto | descarte de ids fuera de la lista + RN-44a-d (RF-113); fallback a RN-49a |
| `justificarRutina` (RF-055) | FL-04 paso 5, vista de revisión FL-02 | estructura validada | texto + `valores_citados` | cada valor citado debe existir en la entrada (RNF-24); si no, descarte + reintento/fallback |
| `resumirProgreso` (RF-056, diferido) | panel de progreso | indicadores ya calculados | texto + `valores_citados` | igual que arriba |
| `describirPerfil` (RF-064, banda N3) | vista entrenador/administrador | frecuencia, volumen e intensidad relativos + objetivo | etiqueta + texto efímero, no persistido | igual que arriba; sin clustering |
| `generarPautaNutricional` (RF-075/RF-108, diferido) | nutrición | energía/proteína ya calculadas | texto por comida, sin alimentos | igual que arriba + declaración orientativa/no profesional + revisión humana |

**Regeneración (FL-04/A5) no es una plantilla nueva:** es `generarRutina` con dos campos extra (`intento_previo`, `que_corregir`), mismo schema y misma validación, con tope RN-127. Dos prompts casi idénticos divergen; un modo explícito no.

## 4. Reglas

- **Cambiar un ejercicio no reescribe la rutina con el LLM.** El usuario elige de `sugerirAlternativas` y el código sustituye y revalida en el acto (RN-126). Un candidato inválido nunca se confirma.
- **No son prompts:** compatibilidad (RN-44a-d), diagnóstico (RN-79a), ajustes (RN-89a), derivación del tipo (RN-39a), ajuste a mano del candidato (FL-04/A3). La adaptación quincenal (FL-09/FL-10) es tabla determinista; si necesita texto, reusa `justificarRutina` sobre ajustes + criterios (RF-090), no crea plantilla nueva.
- **Única tool del modelo:** `verificarCompatibilidad` (determinista, para autocorrección dentro de `generarRutina`); no reemplaza la validación final. Fundamento en [ADR-0008](../decisions/adr/0008-tool-calling-for-ml-components.md).
- **Crear una plantilla nueva solo si** cambian a la vez schema de salida, validación y set de datos de entrada. Si solo cambia la frase de la tarea, es nueva **versión** de la misma plantilla.

## 5. Evaluación y operación (remisión)

Casos fijos, métricas automáticas (factualidad, formato, adherencia, latencia, reintentos, validez repetida) y política de reintento/fallback en [generative-ai.md §9-§10 y §13](generative-ai.md). Aislamiento de datos, qué entra al prompt y qué se registra en [generative-ai.md §11](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md). Criterios de verificación aplicables: RNF-04, RNF-11, RNF-18, RNF-19, RNF-24, RNF-25, RNF-27, RNF-41.
