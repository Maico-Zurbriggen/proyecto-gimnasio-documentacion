# IA generativa — LLM autohospedado

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto, pendiente de verificación de hardware    |
| **Depende de** | [D2](../product/glossary.md), [D5](../domain/business-rules.md), [D8](../requirements/functional-requirements.md), [D9](../requirements/non-functional-requirements.md), [D11/DD-14, DD-15, DD-31, DD-34](../decisions/design-decisions.md), [system-overview.md](system-overview.md) |

## 1. Qué resuelve y qué no resuelve

La capa generativa cubre exclusivamente **componentes narrativos y de interpretación de lenguaje**, nunca prescripción (D11/DD-14):

| Requerimiento | Función | Tipo de componente |
| --- | --- | --- |
| RF-053 | Traducir una descripción en lenguaje natural a parámetros estructurados, presentados para confirmación antes de usarse | Interpretación |
| RF-054 | Construir la rutina a partir de esos parámetros y el contexto del alumno, sobre el catálogo prescribible del gimnasio | HYBRID: el LLM redacta la estructura candidata, pero **RN-39a, RN-44a-d y D5/§6 la validan de forma determinística antes de mostrarla** (RF-113) |
| RF-055 | Justificar en lenguaje natural los criterios aplicados a una rutina generada | Narrativo |
| RF-056 | Resumir la evolución de un alumno en un período, exclusivamente sobre indicadores ya calculados | Narrativo |
| RF-059 / RF-060 | Ordenar las alternativas de sustitución de un ejercicio (ejercicios parecidos) sobre el subconjunto del catálogo prescribible ya prefiltrado de forma determinista por patrón y compatibilidad | Selección sobre catálogo prefiltrado, con revalidación determinista posterior (RF-113) |
| RF-064 | Describir en lenguaje natural el perfil de comportamiento de un alumno a partir de sus indicadores ya calculados (frecuencia, volumen, intensidad relativos) y su objetivo — **efímero, no se persiste** | Narrativo sobre indicadores ya calculados |
| RF-075 / RF-108 | Redactar la pauta nutricional orientativa (energía y proteína por comida, sin nombrar alimentos) | Narrativo sobre valores ya calculados |

**Lo que el LLM nunca hace:** calcular compatibilidad, decidir qué ejercicios entran en una rutina más allá de proponer una estructura candidata sujeta a validación, incluir en una sustitución un ejercicio fuera del subconjunto prefiltrado que recibe como entrada, calcular indicadores, aprobar una rutina, ni emitir indicaciones médicas (RF-057). RN-44a-d, RN-39a, RN-79a y RN-89a son código determinista, no prompts. Ver [D11/DD-31 y DD-34](../decisions/design-decisions.md).

## 2. Dónde corre

El runtime de inferencia corre en un servidor administrado por el Polo Educativo de la Universidad, autohospedado, sin salir a un proveedor externo (ver [ADR-0004](../decisions/adr/0004-self-hosted-llm-server.md)).

**Hardware disponible: `NO VERIFICADO`.** No hay documentación de CPU, GPU, VRAM, RAM ni almacenamiento del servidor institucional en ningún repositorio del proyecto. La arquitectura se diseña para no depender de un tamaño de modelo fijo, exactamente por esta razón: el modelo y su cuantización son **configuración** (variable de entorno leída por el runtime), no una decisión hardcodeada en el backend.

Dos perfiles de despliegue, a confirmar contra el hardware real antes de congelar el tamaño de modelo:

| Perfil | Hardware asumido | Modelo/cuantización | Riesgo |
| --- | --- | --- | --- |
| **A — con GPU** | GPU única, 8-16 GB VRAM `[S]` supuesto de trabajo | Qwen2.5-7B-Instruct o Qwen2.5-14B-Instruct, cuantización Q4_K_M/Q5_K_M (GGUF) o AWQ | Bajo: el presupuesto de 20 s de RNF-04 se cumple con margen |
| **B — solo CPU** | Sin GPU dedicada, RAM ≥ 16 GB `[S]` supuesto de trabajo | Qwen2.5-7B-Instruct, cuantización Q4_K_M | **Alto**: la latencia por token en CPU puede acercarse o superar el presupuesto de RNF-04 para rutinas largas, lo que empujaría el sistema a la vía determinística (RF-113) con más frecuencia de la prevista. Si se confirma este perfil, evaluar un modelo menor (Qwen2.5-3B) o degradar RF-053/RF-055 según el orden de recorte de [D12/§4, ítem 16](../planning/risks-and-assumptions.md) |

Selección de modelo y runtime justificada en [ai-model-selection.md](ai-model-selection.md) y [ADR-0006](../decisions/adr/0006-llm-model-and-runtime-selection.md).

## 3. Componentes y comunicación

Dos capas separadas, que no deben confundirse (ver §5 de la tarea de origen: modelo ≠ runtime):

```text
Backend (Express, monolito modular)
   |
   |  llamada de función in-process
   v
AI Gateway  ── módulo interno, puerto + adaptador ──
   |             (src/modules/ai-gateway en el backend)
   |  HTTP interno, red privada del servidor institucional
   v
LLM Server  ── runtime de inferencia (Ollama) sirviendo el modelo elegido ──
```

- **AI Gateway** vive **dentro del backend**, como un módulo más del monolito modular (no un servicio desplegado aparte). Expone un puerto (`GenerativeAiPort`) con un método por capacidad (`interpretarSolicitud`, `generarRutina`, `justificarRutina`, `resumirEvolucion`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil`) y una única implementación (`OllamaAdapter`) que habla el protocolo HTTP compatible con OpenAI que expone Ollama.
- **LLM Server** es el proceso de Ollama corriendo en el servidor del Polo, sirviendo el modelo configurado. No expone ningún endpoint de negocio: sólo inferencia de texto.
- El backend **nunca** ejecuta el motor Python de IA predictiva ni el runtime del LLM dentro del proceso de una petición HTTP entrante del frontend; sólo hace una llamada saliente al LLM Server y espera su respuesta dentro del presupuesto de RNF-04.

Por qué el Gateway es un puerto con adaptador reemplazable y no lógica dispersa por cada punto de llamada: ver [ADR-0005](../decisions/adr/0005-ai-gateway-in-process-module.md). Su **ubicación de despliegue** quedó reemplazada por [ADR-0009](../decisions/adr/0009-servicio-generativo-online-en-el-polo.md): el Gateway vive dentro del servicio Python del Polo, no dentro del monolito del backend.

## 4. Flujo generativo (mapea FL-04)

```text
Alumno/Entrenador
   │  1. describe en lenguaje natural, o completa formulario
   ▼
Backend (router de rutinas)
   │  2. AI Gateway.interpretarSolicitud(texto)
   ▼
AI Gateway ──prompt versionado + schema──▶ LLM Server
   │  3. respuesta JSON candidata
   ▼
AI Gateway  4. valida contra JSON Schema; si falla, reintenta 1 vez (RF-113)
   │
   ▼
Backend  5. presenta parámetros para CONFIRMACIÓN del usuario (RF-053, paso 2 de FL-04)
   │
   ▼
Backend  6. AI Gateway.generarRutina(parámetros, contexto del alumno)
   │
   ▼
AI Gateway ──prompt + catálogo prescribible + contexto──▶ LLM Server
   │  7. estructura candidata de rutina (JSON)
   ▼
Backend  8. VALIDACIÓN DETERMINÍSTICA: RN-39a, RN-44a-d, D5/§6 (código, no LLM)
   │
   ├─ inválida → 1 reintento del paso 6 → si vuelve a fallar, vía determinística (RN-95b)
   │
   ▼
Backend  9. AI Gateway.justificarRutina(estructura validada) → texto (RF-055)
   │
   ▼
Frontend  10. candidato (RN-124): estructura + estado de compatibilidad + justificación
```

Cada llamada a `AI Gateway` se resuelve con timeout, y si el LLM Server no responde o el resultado no valida tras el reintento, el flujo continúa por la alternativa determinística (RF-058, RF-113, RN-99): entrada por formulario estructurado, justificación tabulada, generación por reglas simples. **Nunca se presenta un error al usuario por esta causa** (RNF-11).

## 5. Contrato interno del AI Gateway

Cada método del puerto recibe y devuelve una estructura tipada; el backend nunca pasa texto libre del LLM directamente a una vista o a persistencia sin haber pasado por validación de schema.

### 5.1 `interpretarSolicitud` (RF-053)

Entrada: texto libre del usuario, contexto mínimo (gimnasio, alumno).

Salida (JSON Schema, ejemplo):

```json
{
  "objetivo": "HIPERTROFIA",
  "frecuencia_semanal": 4,
  "restricciones": ["evitar sentadilla con barra"],
  "duracion_sesion_minutos": 60,
  "confianza": 0.86
}
```

`objetivo` restringido a la enumeración de [D2 §4.5](../product/glossary.md); `frecuencia_semanal` restringido al rango de RN-38 (1-7). Un valor fuera de la enumeración es un fallo de validación, no un dato a persistir.

### 5.2 `generarRutina` (RF-054)

Entrada: parámetros confirmados + contexto del alumno ([D2 §1.9](../product/glossary.md): perfil, nivel, objetivo vigente, condiciones vigentes, aptitud, inventario del gimnasio, catálogo prescribible).

Salida: estructura completa de días → ejercicios → series prescriptas, usando exclusivamente identificadores del catálogo prescribible recibido como entrada (nunca nombres inventados). Se valida contra RN-39a y D5/§6 en código antes de mostrarse.

### 5.3 `justificarRutina` / `resumirEvolucion` / `generarPautaNutricional` (RF-055, RF-056, RF-075/108)

Entrada: la estructura o los indicadores ya calculados (nunca datos crudos que el modelo deba resumir por su cuenta).

Salida:

```json
{
  "texto": "string",
  "valores_citados": [12.5, 4, "HIPERTROFIA"],
  "version_prompt": "generative/justificar-rutina@3",
  "version_modelo": "qwen2.5-7b-instruct-q4_k_m"
}
```

`valores_citados` es la lista de valores numéricos/categóricos que el texto menciona; el backend verifica que cada uno provenga literalmente de la entrada (RNF-24, RF-057) antes de mostrar el texto. Un valor no verificable descarta la respuesta y dispara el reintento/fallback.

### 5.4 `sugerirAlternativas` (RF-059, RF-060)

Entrada: el ejercicio a sustituir, el contexto del alumno y **la lista de ejercicios candidatos ya prefiltrada de forma determinista** por el backend (mismo código de RN-44a-d y RN-45: mismo patrón de movimiento dominante, estado COMPATIBLE para ese alumno, equipamiento presente en el inventario). El LLM nunca recibe el catálogo completo ni ids fuera de esa lista.

Salida (JSON Schema): lista ordenada de hasta 5 ids, **todos pertenecientes a la lista de entrada**, con un motivo breve por ítem. El backend descarta cualquier id que no esté en la entrada y revalida el estado de compatibilidad de cada uno (RF-113) antes de mostrarlo. Si el LLM no responde o la salida no valida tras el reintento, se usa el orden determinista de RN-49a (coincidencia de participación muscular primaria y luego secundaria) sobre la misma lista prefiltrada.

La lista devuelta se persiste junto con `version_modelo` y `version_prompt` (RF-072); no se recalcula al reproducir un resultado pasado (ver §15 y el encuadre de RNF-27 en [DD-34](../decisions/design-decisions.md)).

### 5.5 `describirPerfil` (RF-064)

Entrada: los indicadores de comportamiento ya calculados del alumno (frecuencia, volumen e intensidad relativos) y su objetivo vigente.

Salida: una etiqueta corta y un texto legible ("alta frecuencia, bajo volumen", en vez de un identificador de clúster). Se aplican las mismas restricciones de `valores_citados` de §5.3: el texto no introduce ninguna cifra ausente de la entrada. **El resultado es efímero** — se genera al abrir la vista del entrenador o del administrador y no se persiste. No hay clustering ni un modelo poblacional detrás.

## 6. Prompting

Separación estricta de secciones dentro de cada prompt, versionadas de forma independiente (`generative/<capacidad>@<versión>`):

1. **System prompt** — rol, restricciones permanentes ("nunca inventes valores numéricos ausentes de la entrada", "nunca emitas indicaciones médicas", "responde únicamente en el JSON Schema dado"). Fijo por capacidad, cambia poco.
2. **Schema de salida** — el JSON Schema exacto que se va a validar, incluido literalmente en el prompt para modelos sin API nativa de structured output, u ofrecido como `response_format`/`format` cuando el runtime lo soporta (Ollama lo soporta desde su API de generación estructurada).
3. **Contexto dinámico** — el contexto del alumno o los indicadores ya calculados, siempre como JSON serializado, nunca como prosa que el modelo deba reinterpretar.
4. **Instrucción de la tarea** — la petición concreta ("generá la justificación de esta rutina").
5. **Restricciones de negocio que NO van en el prompt**: la enumeración cerrada de equipamiento, patrones de movimiento y objetivos ([D2 §4](../product/glossary.md)) se valida en código después de la respuesta, no se le pide "por favor" al modelo que la respete — el modelo puede proponer, el código dispone (RN-95b, RF-113).

Las plantillas de prompt viven versionadas en el repositorio del backend (no en el LLM Server), como archivos de texto bajo control de versión, con su propio changelog. Un cambio de prompt es un cambio de código: pasa por PR y por los casos de prueba de §10.

## 7. Tool calling: herramientas invocables desde el LLM

RF-054 y RF-119 necesitan que, mientras arma el candidato de rutina (FL-04), el modelo pueda pedir alternativas de sustitución para un ejercicio puntual (RF-059, A4 de FL-04). Tras el replanteo de IA del 2026-08-28 ([DD-34](../decisions/design-decisions.md)), ese orden **lo produce la propia capa generativa** (`sugerirAlternativas`, §5.4) sobre el subconjunto del catálogo ya prefiltrado de forma determinista — ya no hay un modelo clásico de ranking. Lo que **sí** se mantiene como herramienta determinista es la verificación de compatibilidad. Fundamento en [ADR-0008 (revisada)](../decisions/adr/0008-tool-calling-for-ml-components.md).

**Herramientas expuestas por el AI Gateway al modelo:**

| Herramienta | Envuelve | Devuelve |
| --- | --- | --- |
| `verificarCompatibilidad(estructura_candidata, alumno_context)` | RN-44a-d (código determinista) | Estado de compatibilidad por ejercicio — el mismo cálculo que corre igual como validación posterior (§5, RF-113); exponerlo como herramienta le permite al modelo autocorregirse antes de terminar, no reemplaza la validación final |

El ordenamiento de alternativas de sustitución **no se expone como herramienta**: el modelo que ya está orquestando FL-04 recibe el subconjunto prefiltrado como parte del contexto y produce el orden inline, o el backend llama a `sugerirAlternativas` directamente (A4 de FL-04, FL-06). En ambos casos la salida sólo puede contener ids del subconjunto de entrada y se revalida por RN-44a-d antes de mostrarse (RF-113).

**Por qué el LLM ordena las alternativas pero no "razona sobre el catálogo entero".** El LLM recibe únicamente el subconjunto ya filtrado por patrón de movimiento, compatibilidad y equipamiento (mismo código que RN-44a-d y RN-45); no ve el catálogo completo ni puede inventar ids. La exclusión dura de lo contraindicado y la verificación final siguen siendo deterministas y son la barrera real (RF-113, RN-95b). Lo que se acepta a cambio: el orden de las alternativas ya no es exactamente reproducible entre corridas, sino "válido de forma repetida" — el mismo estándar de §10 para el resto de la capa generativa; la lista producida se persiste para RF-072 (ver el encuadre de RNF-27 en [DD-34](../decisions/design-decisions.md)).

**Requisito sobre el modelo/runtime elegido**: esto es la razón por la que el soporte de tool calling en [ai-model-selection.md §1](ai-model-selection.md) dejó de ser un "nice to have" y pasa a ser un requisito de peso — Qwen2.5 y Ollama lo soportan de forma madura, lo que valida la elección hecha en [ADR-0006](../decisions/adr/0006-llm-model-and-runtime-selection.md) también por este motivo, no sólo por licencia y calidad en español.

## 8. RAG — no se usa (retrieval semántico), pero sí prefiltrado determinista

Ver justificación completa y el umbral de reapertura en [ADR-0007](../decisions/adr/0007-no-rag.md). Resumen actualizado, con la parte de tamaño explícita:

- Las 12 enumeraciones cerradas de [D2 §4](../product/glossary.md) entran completas en el prompt: son chicas y fijas, no necesitan recuperación.
- El **catálogo prescribible de un gimnasio no siempre es chico** (puede tener decenas a un par de cientos de ejercicios) y no se vuelca completo al prompt en cada llamada. El backend lo **prefiltra de forma determinista** — mismo código que ya exige RN-44a-d y RN-45 para la validación — por patrón de movimiento pedido, compatibilidad con el alumno y equipamiento del inventario, **antes** de construir el prompt. Sólo ese subconjunto ya válido entra al contexto, típicamente acotado a decenas de ejercicios por llamada, no al catálogo entero.
- Esto no es RAG semántico porque la necesidad no es de similitud aproximada: es un filtro **exacto** sobre atributos estructurados (RN-44a-d es una regla dura, no una preferencia difusa). Un vector store resolvería esto de forma aproximada, que es peor para una condición que tiene que ser exacta (RN-46: una incompatibilidad impide poner la rutina en vigencia).
- El resto del contexto del alumno (perfil, condiciones, indicadores) se arma con una consulta directa a PostgreSQL, acotada por alumno — no hay un corpus grande, no estructurado y cambiante (políticas, FAQ, documentación interna) que el LLM deba buscar semánticamente.

**Umbral de reapertura explícito**: si el catálogo prescribible filtrado de un gimnasio (ya acotado por patrón y compatibilidad, no el catálogo completo) empezara a superar un tamaño que ya no entra cómodo en el presupuesto de contexto del modelo elegido — algo que no se espera con equipamiento típico de gimnasio, dado el techo de 22 valores de equipamiento y 9 patrones de movimiento de [D2 §4](../product/glossary.md) — ahí sí corresponde reabrir esta decisión y evaluar RAG semántico o paginación. No antes.

## 9. Guardrails

| Riesgo | Mitigación |
| --- | --- |
| Alucinación de valores numéricos en texto narrativo | Verificación de `valores_citados` contra la entrada (RNF-24); descarte automático si no coincide |
| Alternativa de sustitución con un id inventado o fuera del subconjunto prefiltrado | El backend descarta todo id que no esté en la lista de entrada y revalida compatibilidad (RF-113); si no queda ninguno válido, se aplica el orden determinista de RN-49a |
| Salida fuera del schema | Validación de JSON Schema; 1 reintento; luego vía determinística (RF-113) |
| Indicación médica | Prohibición explícita en el system prompt + filtro de patrones (palabras clave clínicas) sobre la salida antes de mostrarla; RF-057 lo exige como requisito, no como buena práctica |
| Inyección de instrucciones en el texto libre del usuario ("ignorá las reglas anteriores y...") | El contexto dinámico y la instrucción de tarea van en secciones separadas y delimitadas del prompt; ninguna instrucción de negocio depende de que el modelo la respete — la validación determinística (RN-39a, RN-44a-d) es la barrera real, no el prompt |
| Uso indebido de datos del alumno | Ver §11 — el AI Gateway decide qué campos del contexto se serializan hacia el prompt; un campo nuevo en el modelo de datos no llega al LLM automáticamente |
| Mensaje comercial/narrativo incorrecto que llega al alumno | El sistema decide si el texto se envía: la salida del LLM es siempre una propuesta que pasa por la validación de §9 antes de presentarse; ninguna redacción se entrega directo desde el modelo |

## 10. Evaluación de la IA generativa

Conjunto de casos de prueba representativo, fijo y versionado junto con los prompts (no exhaustivo, pero cubre los siete métodos del Gateway):

| Caso | Verifica |
| --- | --- |
| Interpretación con objetivo ambiguo ("quiero ponerme fuerte") | Mapea a un valor válido de la enumeración o pide aclaración, nunca inventa un valor fuera de ella |
| Interpretación con restricción de equipamiento mencionada en el texto | El equipamiento no se toma como parámetro (sale del inventario, RF-053) — el Gateway lo descarta si el modelo lo intenta incluir |
| Generación con inventario mínimo (sólo `PESO_CORPORAL`) | La estructura resultante no referencia equipamiento ausente; si no cubre los patrones mínimos, lo declara (E3 de FL-04) |
| Justificación sobre una rutina con un ajuste de `SUSTITUCION` | El texto no inventa una carga o repetición ausente del ajuste de entrada |
| Resumen de evolución con `DATOS_INSUFICIENTES` | El texto declara la insuficiencia, no la disimula con una afirmación genérica |
| Pauta nutricional sin datos suficientes | El Gateway no genera texto (RF-108) |
| Sugerencia de alternativas con un candidato contraindicado en la lista de entrada | La salida no lo incluye; ningún id fuera de la lista prefiltrada aparece en el resultado |
| Sugerencia de alternativas con el LLM no disponible | Se devuelve el orden determinista de RN-49a sobre la misma lista, sin error visible |
| Descripción de perfil con indicadores dados | El texto no introduce ninguna cifra ausente de la entrada; no se persiste |

Métricas sobre este conjunto y sobre una muestra ampliada (alineado con RNF-24/RNF-25):

- **Corrección factual**: tasa de `valores_citados` no verificables — objetivo 0% (RNF-24, sobre 50 textos por tipo).
- **Formato**: tasa de respuestas que no validan contra el JSON Schema en el primer intento.
- **Adherencia a instrucciones**: tasa de rutinas generadas que requieren el reintento de RF-113.
- **Latencia**: percentil 95 de cada método, contra el presupuesto de RNF-04 (20 s incluida validación).
- **Tasa de error/timeout**: proporción de llamadas que terminan en la vía determinística por indisponibilidad o timeout del LLM Server.
- **Consistencia**: misma entrada, incluida la temperatura configurada, produce estructuras dentro del mismo rango de validación en ejecuciones repetidas (no se exige determinismo exacto, se exige validez repetida).

No se usa únicamente evaluación subjetiva: las primeras cuatro métricas son automáticas y se ejecutan en CI sobre el conjunto de casos fijo antes de cambiar un prompt o un modelo.

## 11. Privacidad y seguridad específicas del LLM

**Qué llega al prompt:** objetivo, nivel, condiciones físicas por zona/severidad (sin descripción libre — RN-10a ya excluye la descripción libre de todo cálculo, y por la misma razón no se serializa al prompt), inventario del gimnasio, catálogo prescribible, indicadores agregados ya calculados (volumen, adherencia, e1RM). Ningún dato de contacto, credencial ni identificador más allá del necesario para trazabilidad interna (id de contexto, no nombre ni correo).

**Qué nunca llega al prompt:** contraseñas, tokens de sesión, correo electrónico, teléfono, descripción libre de una condición física, historial de otro alumno, dato de un gimnasio distinto al del alumno en contexto.

**Qué se registra:** versión de prompt, versión de modelo, hash del contexto de entrada (no el contexto completo en texto plano en logs de aplicación de larga retención), latencia, resultado de validación. **Nunca** se registra el texto de una condición física ni el contenido completo del prompt en un log persistente de nivel INFO — esto es RNF-19 aplicado a la capa generativa, no una elección adicional. Un registro de auditoría completo (para depuración de una respuesta puntual) puede existir con retención corta y acceso restringido a quien opere el LLM Server, nunca en logs de acceso general.

**Ventaja de ser autohospedado**: ningún dato de alumnos (condición física, historial) sale de la infraestructura de la Universidad hacia un tercero. **Riesgo nuevo que introduce**: la Universidad pasa a ser responsable de operar, parchear y asegurar un servicio con datos potencialmente sensibles — sin esto, el riesgo estaba tercerizado a un proveedor con su propio cumplimiento; con esto, el equipo del proyecto y el Polo Educativo lo asumen directamente. Debe documentarse como parte del acuerdo operativo con la institución.

## 12. Seguridad del servidor LLM

- El LLM Server **no se expone a Internet**. Sólo es alcanzable desde la red interna donde corre el backend (o mediante VPN/túnel si el backend no corre en la misma red del Polo). No hay razón declarada en este proyecto para exponerlo públicamente.
- Autenticación entre el AI Gateway y el LLM Server mediante un token compartido en variable de entorno (no en código), rotable sin redeploy del backend.
- TLS si el tráfico atraviesa un segmento de red no confiable; en red interna aislada, evaluado según lo que el Polo Educativo provea — `NO VERIFICADO`.
- Límite de recursos del proceso de inferencia (memoria, concurrencia máxima) configurado en el runtime, para que una petición no degrade el resto del servidor si es compartido con otros servicios del Polo.
- Rate limiting por usuario y por período en el backend, antes de llegar al Gateway (RNF-18) — protege al LLM Server de un solo usuario agotando la capacidad.
- Actualizaciones del runtime y del modelo son un cambio de versión documentado (§16), nunca un reemplazo silencioso.

## 13. Fallback

> ⚠️ **v4.0 del alcance.** Donde este documento dice «presets publicados del gimnasio», léase **«plantillas del entrenador» (RF-019)**: RF-021 quedó diferido en la Etapa 1 y con él la publicación de presets. El objeto subyacente es el mismo —una plantilla de rutina—; lo que no existe es compartirla dentro del gimnasio. **El fallback deja de ser automático: requiere que exista al menos una plantilla cargada y que un entrenador la asigne.** Ver [DD-35](../decisions/design-decisions.md), RN-95b y D12/R-17.

| Falla | Comportamiento |
| --- | --- |
| LLM no responde / timeout | Vía determinística: formulario estructurado en vez de NL, generación por reglas simples si corresponde, justificación tabulada (RF-058, A1 de FL-04) |
| LLM no responde al pedir alternativas de sustitución (FL-04/A4, FL-06) | Orden determinista de RN-49a sobre el subconjunto ya prefiltrado (coincidencia de participación muscular primaria y luego secundaria); el flujo de sustitución no se interrumpe (RN-99) |
| LLM no responde al pedir la descripción de perfil (RF-064) | La vista muestra los indicadores numéricos sin el texto descriptivo; nada más se degrada |
| Salida inválida (no pasa el JSON Schema o la validación de negocio) | 1 reintento; si vuelve a fallar, vía determinística (RF-113, E1 de FL-04). Nunca se presenta una propuesta inválida ni un error |
| GPU/recursos agotados en el LLM Server | El timeout de la llamada lo captura igual que una indisponibilidad; mismo camino que la fila anterior |
| Servicio completo fuera de línea | El resto del sistema sigue operando: registro de sesiones, revisión de rutinas, consulta de indicadores — nada de esto depende del LLM (RNF-11, RNF-12) |

## 14. Observabilidad

Métricas por método del Gateway (`interpretarSolicitud`, `generarRutina`, `justificarRutina`, `resumirEvolucion`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil`):

- latencia (p50/p95/p99);
- tokens de entrada y salida;
- throughput (llamadas/minuto);
- tasa de error y de timeout;
- tasa de reintento (RF-113);
- tasa de fallback a vía determinística;
- versión de modelo y de prompt activas.

Nunca se registra información sensible del alumno en estas métricas (RNF-19) — son agregados numéricos y etiquetas de versión, no contenido.

## 15. Versionado

- **Modelo**: identificador completo (`qwen2.5-7b-instruct-q4_k_m`) fijado en configuración del AI Gateway, no en el LLM Server únicamente — el backend registra qué versión produjo cada resultado (RF-072).
- **Prompt**: `generative/<capacidad>@<n>`, incrementado en cada cambio de contenido, con changelog en el propio archivo de plantilla.
- **Schema de salida**: versionado junto al prompt que lo referencia; un cambio de schema es incompatible por definición y requiere versión nueva de ambos.
- Cada resultado narrativo persistido conserva `version_modelo` y `version_prompt` (§5.3), cumpliendo RF-072 también para narrativos, aunque no sean "componentes de decisión" en el sentido de DD-14.
- La lista de alternativas de sustitución que se incorpora a un candidato de rutina se persiste con `version_modelo` y `version_prompt` (§5.4). Como el orden generativo no es exactamente reproducible, RF-072/RNF-27 se cumplen guardando la salida, no reejecutándola (ver [DD-34](../decisions/design-decisions.md)). La descripción de perfil (§5.5) es efímera y no se persiste.

## 16. Reemplazo del modelo en el futuro

Cambiar de Qwen a Llama, a otro modelo, o subir de tamaño no requiere tocar el backend fuera del AI Gateway:

1. El nuevo modelo se publica en el LLM Server (`ollama pull <modelo>`) y se valida con el conjunto de casos de §10.
2. Se compara contra el modelo vigente con las mismas métricas (RF-073 aplicado también acá: el modelo nuevo debe igualar o superar al vigente en el conjunto de prueba antes de promoverse).
3. Se cambia la variable de configuración del AI Gateway. El `GenerativeAiPort` no cambia; sólo cambia qué modelo atiende el `OllamaAdapter`.
4. Si el nuevo modelo requiere un runtime distinto (por ejemplo, vLLM por necesidad de concurrencia), se agrega un adaptador nuevo (`VllmAdapter`) que implementa el mismo puerto — el backend no distingue entre ellos.

## 17. Costos y capacidad

Autohospedado no es costo cero:

- **Electricidad y amortización de hardware**: a cargo del Polo Educativo, fuera del presupuesto del proyecto — `NO VERIFICADO` si existe un límite o cuota asignada al equipo.
- **Administración**: alguien del equipo o del Polo debe mantener el runtime actualizado y monitorear el proceso — no está presupuestado en las 504 h de capacidad de construcción de [D12/§3](../planning/risks-and-assumptions.md); es trabajo adicional a declarar, no a absorber en silencio.
- **Estimación de carga** (de trabajo, no verificada contra uso real): generación de rutina es un evento poco frecuente por alumno (al incorporarse, al pedir una nueva, no en cada sesión). Con 5.000 alumnos (techo de RNF-36) y una tasa optimista de una generación por alumno por semana, son ~715 llamadas/día a `generarRutina`, muy por debajo del umbral de ~5 usuarios concurrentes donde Ollama empieza a degradarse (ver [ai-model-selection.md](ai-model-selection.md)). El resumen narrado (RF-056) y la justificación (RF-055) tienen una frecuencia similar o menor. **Esta estimación es de diseño, no una medición — debe revisarse cuando haya uso real.**
- Con esta carga esperada, una sola GPU modesta (o incluso CPU con el riesgo de latencia ya señalado en §2) alcanza. No hay evidencia de que se necesite más de una instancia del LLM Server.
