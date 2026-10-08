# Arquitectura de prompts y orquestación

**Actualización 2026-10-05:** [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) sustituye filtros, restricciones de prescripción y herramienta de compatibilidad. Diseño pendiente de implementación; contrato en [data-interface.md](data-interface.md).

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
- Texto libre y preferencias son datos para IA; la aplicación elige la capacidad por acción de interfaz. Esa orquestación no decide ejercicios ni entrenamiento.

**Reapertura:** si aparece conversación abierta multi-turno real (hoy fuera de alcance), reevaluar un clasificador LLM solo para esa rama. No antes.

## 2. Estructura: 1 base compartida + 7 plantillas especializadas

Ningún megaprompt único y ningún prompt por botón. Cada llamada compone 5 secciones, en este orden:

1. **Base system (común):** idioma, schema y ausencia de consejo médico. El overlay narrativo exige cifras respaldadas; el de generación permite decidir valores de prescripción.
2. **Overlay por capacidad:** lo específico de esa tarea y nada más.
3. **Schema de salida literal** (más `response_format`/`format` cuando el runtime lo soporta).
4. **Contexto dinámico como JSON:** datos pertinentes del alumno y, para generación/alternativas, todo el catálogo habilitado, sin URLs de imágenes ni recorte por alumno.
5. **Instrucción concreta** de una línea.

La base cambia poco; cada overlay se versiona por separado como `generative/<capacidad>@<n>` con su changelog. Un cambio de schema exige versión nueva de ambos. Detalle del versionado y de lo que se registra por resultado en [generative-ai.md §15](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md).

## 3. Inventario

| Plantilla | Disparo (código, no LLM) | Entrada | Salida | Validación |
| --- | --- | --- | --- | --- |
| `interpretarPedido` (RF-053) | FL-04 paso 1, solo si hay texto libre | texto + contexto mínimo | objetivo, frecuencia 1-7, restricciones, duración, confianza | schema + enumeraciones de [D2](../product/glossary.md) + confirmación humana antes de propagarse |
| `generarRutina` (RF-054) | FL-01, FL-04 | Pedido + contexto del alumno + inventario + catálogo habilitado completo | Prescripción justificada o imposibilidad explicada | Schema, IDs, disponibilidad y contexto vigente; evaluación de entrenamiento por IA y entrenador |
| `sugerirAlternativas` (RF-059, absorbe RF-060) | FL-06; RF-119 si se incorpora | Ejercicio original + catálogo habilitado completo + contexto del alumno | Hasta 5 IDs con motivo, o insuficiencia | IDs y disponibilidad; sin filtro ni ranking en código |
| `justificarRutina` (RF-055) | FL-04 paso 5, vista de revisión FL-02 | estructura validada | texto + `valores_citados` | cada valor citado debe existir en la entrada (RNF-24); si no, descarte + reintento/fallback |
| `resumirProgreso` (RF-056, diferido) | panel de progreso | indicadores ya calculados | texto + `valores_citados` | igual que arriba |
| `describirPerfil` (RF-064, banda N3) | vista entrenador/administrador | frecuencia, volumen e intensidad relativos + objetivo | etiqueta + texto efímero, no persistido | igual que arriba; sin clustering |
| `generarPautaNutricional` (RF-075/RF-108, diferido) | nutrición | energía/proteína ya calculadas | texto por comida, sin alimentos | igual que arriba + declaración orientativa/no profesional + revisión humana |

Una nueva solicitud usa `generarRutina` y una instantánea nueva. La edición/regeneración de un candidato ajustable conserva diferidos RF-119/RF-120; no agrega otra plantilla.

## 4. Reglas

- Elegir una alternativa conserva la decisión del usuario y registra el ejercicio ejecutado; el adaptador no modifica selecciones ni prescribe valores. El candidato ajustable continúa diferido.
- Indicadores, diagnóstico batch y su tabla de adaptación quedan fuera de este cambio. Adecuación, selección, tipo y prescripción de la generación corresponden al LLM; RN-39a es referencia, no validación en código.
- No se requiere `verificarCompatibilidad` ni otra herramienta de filtrado; esta entrega incluye todos los candidatos en el contexto (ADR 0013).
- **Crear una plantilla nueva solo si** cambian a la vez schema de salida, validación y set de datos de entrada. Si solo cambia la frase de la tarea, es nueva **versión** de la misma plantilla.

## 5. Evaluación y operación (remisión)

Casos fijos, métricas automáticas (factualidad, formato, adherencia, latencia, reintentos, validez repetida) y política de reintento/fallback en [generative-ai.md §9-§10 y §13](generative-ai.md). Aislamiento de datos, qué entra al prompt y qué se registra en [generative-ai.md §11](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md). Criterios de verificación aplicables: RNF-04, RNF-11, RNF-18, RNF-19, RNF-24, RNF-25, RNF-27, RNF-41.
