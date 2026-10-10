# Arquitectura de prompts y orquestación

**Actualización 2026-10-10:** [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) sustituye filtros, restricciones de prescripción y herramienta de compatibilidad. La organización de `generarRutina` está implementada localmente con variantes por tarea; las demás capacidades conservan su alcance indicado en el inventario. Contrato en [data-interface.md](data-interface.md).

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
2. **Overlay por capacidad y tarea:** lo específico de esa acción, seleccionado en código.
3. **Schema de salida literal** (más `response_format`/`format` cuando el runtime lo soporta).
4. **Contexto dinámico como JSON:** datos pertinentes del alumno y, para generación/alternativas, todo el catálogo habilitado, sin URLs de imágenes ni recorte por alumno.
5. **Instrucción concreta** de una línea.

La base cambia poco; cada capacidad se versiona como `generative/<capacidad>@<n>`. Las variantes de tarea de una misma capacidad participan de su firma y configuración; un cambio de base, overlay o schema exige versión nueva. Detalle del versionado y de lo que se registra por resultado en [generative-ai.md §15](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md).

### 2.1 Generación de rutinas implementada

El módulo `generation_prompts.py` del servicio IA compone una base compartida y tres overlays de la misma capacidad `generarRutina`: `INITIAL`, `AUTOMATIC_RENEWAL` y `TRAINER_REGENERATION`. Backend elige `preferences.generation_task.kind` desde el flujo; el texto del alumno o entrenador no selecciona la tarea. La configuración `generative/generar-rutina@26` registra la firma de la base, overlays, schemas y parámetros técnicos. El transporte adjunta el schema literal y la instrucción concreta a la entrada JSON.

La base define autoridad, catálogo, adecuación, alcance de parámetros, interpretación de preferencias, comprobaciones y salida. El foco en un músculo es una prioridad dentro de una rutina completa, sin inferir exclusividad ni mínimos por músculo. `minExercisesPerDay` cuenta todos los ejercicios del día. La selección, organización y volumen siguen siendo decisiones de IA revisadas por el entrenador.

El contexto separa parámetros actuales del gimnasio, versión vigente, evidencia congelada del ciclo, comentario del entrenador y candidato anterior. Este último contiene sólo la planilla y sus referencias mapeadas al catálogo actual; no lleva su configuración administrativa vieja ni instrucciones concatenadas. Una proyección de nombres, patrones y músculos de **todos** los ejercicios facilita consultar el catálogo sin filtrar, ordenar por preferencia ni reemplazar las fichas completas.

Las variantes de renovación declaran el vencimiento como motivo suficiente y conservan RN-89a. La regeneración atiende el comentario y permite conservar partes adecuadas del candidato, sin devolverlo idéntico. Solicitudes históricas sin `generation_task` se enrutan por sus flags persistidos; la distribución restringida al origen se mantiene exclusivamente para solicitudes anteriores sin `routine_renewal_full_catalog`.

El schema separa grupos de trabajo y calentamiento mediante flags y límites tomados exclusivamente de la configuración vigente. La expansión comprueba las cantidades totales por ejercicio. Si esa validación falla, el intento registra un código técnico específico; el siguiente worker lo recupera y agrega la corrección pertinente al prompt. Se conserva el máximo de dos intentos y la ausencia de fallback.

En regeneración, IA compara la prescripción expandida con `previous_candidate` antes de completar el intento. La misma selección, orden por día y valores de series se rechazan con `routine_regeneration_candidate_unchanged`, aunque cambien nombres, notas, explicación o agrupación compacta de series. El segundo intento recibe ese motivo para corregir la planilla; backend mantiene la misma comprobación al finalizar como defensa adicional. Mientras se reintenta se conserva el candidato anterior, y al agotar intentos se alerta una vez sin exigir otro comentario del entrenador. La comparación no decide ejercicios ni evalúa automáticamente la calidad del énfasis muscular.

La verificación de capacidad usa primero una cota conservadora por bytes. Si esa cota no entra, para GGUF BPE `qwen35` reconstruye el tokenizador con el vocabulario y las fusiones del modelo instalado, obtenidos por `/api/show` privado. La dependencia `tokenizers` permite contar sin estimaciones por caracteres ni recortar fichas; no descarga modelos de Hugging Face. La caché en memoria está limitada a dos revisiones, identificadas por servidor, modelo y digest; no interviene en la cola durable. Un tokenizador desconocido o una entrada que realmente supera la ventana se rechazan antes de inferencia. Se reservan tokens para schema, plantilla, encapsulado y respuesta, y se verifican capacidad nativa, ventana asignada y digest al completar. La ventana configurada debe admitir todo el catálogo: la prueba local con 425 ejercicios requiere una cota de entrada de aproximadamente 146.000 tokens más la reserva de salida (16.384 en la prueba local con razonamiento) y usa 196.608, dentro de los 262.144 del modelo instalado. El valor por defecto sigue en 131.072 y requiere ajuste explícito para catálogos de ese tamaño.

La regeneración repite el comentario original como dato estructurado `task_reminder` después del contexto largo, sin cambiar su autoridad ni clasificar texto libre. El prompt exige que el cambio responda a la prioridad solicitada frente al candidato y que la explicación nombre una diferencia comprobable; pide agrupar las series del mismo ejercicio en una sola entrada diaria y elegir complementos en lugar de repetirlo para alcanzar el mínimo. Estas instrucciones orientan a IA y revisión humana; no agregan cuotas por músculo, selección determinista ni una garantía automática de calidad.

Changelog local: `@21` separa base, variantes y datos estructurados, aclara el énfasis muscular y agrega el directorio completo; `@22` explicita los grupos de calentamiento/trabajo y transmite al reintento el error de parámetros que quedó persistido; `@23` rechaza copias de candidato dentro del flujo durable de IA, habilita su corrección automática y aclara que una explicación distinta no modifica la prescripción; `@24` cuenta tokens con el vocabulario GGUF verificado cuando la cota por bytes resulta excesiva, sin filtrar el catálogo; `@25` recuerda el comentario al final de entradas largas y explicita el cambio de prioridad y la presentación sin duplicados innecesarios dentro del día; `@26` habilita razonamiento del modelo para generación con catálogo completo y repite al cierre la corrección técnica persistida del reintento.

En generación con catálogo completo se solicita `think=true` para permitir planificación y comprobación interna antes del JSON. El servicio consume únicamente `message.content`; no presenta ni persiste `message.thinking`. Razonamiento y respuesta comparten la reserva de tokens de salida, y un agotamiento o stream incompleto se rechaza. El flujo histórico de distribución por índices mantiene `think=false`. No se agregan llamadas LLM ni etapas fuera del máximo de dos intentos. En el reintento, `validation_feedback` repite al cierre del contexto el código persistido y su corrección estática, conservando el mismo mensaje en el sistema.

Prueba manual local de `@26` (2026-10-10): desde la UI del entrenador, con 425 ejercicios habilitados y el mismo comentario «Genera una rutina con enfoque en gluteos», la generación terminó en el primer intento en aproximadamente 220 segundos. La revisión confirmó 3 días de 5 ejercicios, 3 series de trabajo y 2 de calentamiento por ejercicio, sin duplicados dentro del día; el trabajo directo de glúteos pasó de 6 a 12 series semanales y el día correspondiente comenzó con hip thrust. Todos los IDs pertenecían al snapshot y se mantuvieron los parámetros administrativos. Esta muestra acredita el caso observado, sin garantizar calidad de todas las salidas. La demora supera el límite por defecto de 120 segundos de producción; la prueba local usó 600, por lo que capacidad y presupuesto de ejecución deben evaluarse antes de desplegar ese catálogo.

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

Una nueva solicitud usa `generarRutina` y una instantánea nueva. La regeneración por entrenador de una propuesta automática `ESTRUCTURA` usa el overlay de §2.1; no agrega otra capacidad. La edición del candidato por alumno de RF-119/RF-120 conserva su alcance diferido.

## 4. Reglas

- Elegir una alternativa conserva la decisión del usuario y registra el ejercicio ejecutado; el adaptador no modifica selecciones ni prescribe valores. El candidato ajustable continúa diferido.
- Indicadores, diagnóstico batch y su tabla de adaptación quedan fuera de este cambio. Adecuación, selección, tipo y prescripción de la generación corresponden al LLM; RN-39a es referencia, no validación en código.
- No se requiere `verificarCompatibilidad` ni otra herramienta de filtrado; esta entrega incluye todos los candidatos en el contexto (ADR 0013).
- **Crear una plantilla nueva solo si** cambian a la vez schema de salida, validación y set de datos de entrada. Si solo cambia la frase de la tarea, es nueva **versión** de la misma plantilla.

## 5. Evaluación y operación (remisión)

Casos fijos, métricas automáticas (factualidad, formato, adherencia, latencia, reintentos, validez repetida) y política de reintento/fallback en [generative-ai.md §9-§10 y §13](generative-ai.md). Aislamiento de datos, qué entra al prompt y qué se registra en [generative-ai.md §11](generative-ai.md) y [generative-ai-integration.md](generative-ai-integration.md). Criterios de verificación aplicables: RNF-04, RNF-11, RNF-18, RNF-19, RNF-24, RNF-25, RNF-27, RNF-41.
