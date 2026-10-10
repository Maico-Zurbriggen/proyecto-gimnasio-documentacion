# IA generativa — LLM autohospedado

**Actualizado 2026-10-07:** generación `2.0` implementada localmente según [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md). Generación recibe el catálogo habilitado completo; IA toma las decisiones de entrenamiento. Las demás capacidades generativas conservan su alcance de diseño. Las solicitudes históricas `1.0` mantienen su adaptador anterior durante la transición.

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado** | Generación implementada localmente; pendiente curación del catálogo real, promoción y evaluación de entrenamiento |
| **Depende de** | [D2](../product/glossary.md), [D5](../domain/business-rules.md), [D8](../requirements/functional-requirements.md), [D9](../requirements/non-functional-requirements.md), [D11/DD-14, DD-15, DD-31, DD-34](../decisions/design-decisions.md), [system-overview.md](system-overview.md) |

## 1. Qué resuelve y qué no resuelve

La capa generativa interpreta, selecciona ejercicios, evalúa adecuación y prescribe para RF-054/RF-059. Los componentes narrativos explican datos existentes; diagnóstico batch e indicadores mantienen su alcance independiente.

| Requerimiento | Función | Tipo de componente |
| --- | --- | --- |
| RF-053 | Traducir una descripción en lenguaje natural a parámetros estructurados, presentados para confirmación antes de usarse | Interpretación |
| RF-054 | Decidir tipo, ejercicios y prescripción a partir del contexto del alumno y todo el catálogo habilitado | IA + controles técnicos + aprobación del entrenador |
| RF-055 | Justificar en lenguaje natural los criterios aplicados a una rutina generada | Narrativo |
| RF-056 | Resumir la evolución de un alumno en un período, exclusivamente sobre indicadores ya calculados | Narrativo |
| RF-059 / RF-060 | Evaluar y ordenar alternativas con todo el catálogo habilitado y contexto del alumno | IA + controles de IDs y disponibilidad |
| RF-064 | Describir en lenguaje natural el perfil de comportamiento de un alumno a partir de sus indicadores ya calculados (frecuencia, volumen, intensidad relativos) y su objetivo — **efímero, no se persiste** | Narrativo sobre indicadores ya calculados |
| RF-075 / RF-108 | Redactar la pauta nutricional orientativa (energía y proteína por comida, sin nombrar alimentos) | Narrativo sobre valores ya calculados |

IA no aprueba ni activa rutinas, no escribe tablas de dominio ni reemplaza los cálculos de indicadores. No emite indicaciones médicas. Backend controla permisos, estructura, pertenencia y disponibilidad; las tablas de entrenamiento dejan de validar generación en código (ADR 0013).

## 2. Dónde corre

El runtime de inferencia corre en un servidor administrado por el Polo Educativo de la Universidad, autohospedado, sin salir a un proveedor externo (ver [ADR-0004](../decisions/adr/0004-self-hosted-llm-server.md)).

**Hardware disponible: `NO VERIFICADO`.** No hay documentación de CPU, GPU, VRAM, RAM ni almacenamiento del servidor institucional en ningún repositorio del proyecto. La arquitectura se diseña para no depender de un tamaño de modelo fijo, exactamente por esta razón: el modelo y su cuantización son **configuración** (variable de entorno leída por el runtime), no una decisión hardcodeada en el backend.

Dos perfiles de despliegue, a confirmar contra el hardware real antes de congelar el tamaño de modelo:

| Perfil | Hardware asumido | Modelo/cuantización | Riesgo |
| --- | --- | --- | --- |
| **A — con GPU** | GPU única, 8–16 GB VRAM `[S]` | Modelo y cuantización configurables; selección en ADR 0006 | Capacidad y latencia con catálogo completo todavía no medidas |
| **B — solo CPU** | Sin GPU dedicada, RAM ≥ 16 GB `[S]` | Modelo y cuantización configurables | Puede exceder los 120 s por intento; no existe generación determinista alternativa |

Selección de modelo y runtime justificada en [ai-model-selection.md](ai-model-selection.md) y [ADR-0006](../decisions/adr/0006-llm-model-and-runtime-selection.md).

## 3. Componentes y comunicación

Tres capas separadas, que no deben confundirse (modelo ≠ orquestador ≠ runtime):

```text
Backend / Vercel
   |
   | HTTPS; sólo UUID de solicitud
   v
Servicio IA / Vercel ── FastAPI -> Vercel Queues -> consumidor Python
   |
   | HTTPS + autenticación de servicio
   v
ngrok -> Polo API -> LLM Server / Polo ── Ollama sirviendo el modelo elegido
```

- **El adaptador del backend** sólo crea y despacha una solicitud idempotente hacia el OpenAPI del servicio IA.
- **El servicio IA** concentra autenticación, contrato, prompts, validación estructural, cola, persistencia técnica y el adaptador Ollama.
- **LLM Server** es el proceso de Ollama corriendo en el servidor del Polo, sirviendo el modelo configurado. No expone ningún endpoint de negocio: sólo inferencia de texto.
- El backend nunca llama al LLM ni espera su respuesta. FastAPI responde `202` después de encolar y el frontend consulta el estado sólo al backend.

Por qué el Gateway es un puerto con adaptador reemplazable y no lógica dispersa por cada punto de llamada: ver [ADR-0005](../decisions/adr/0005-ai-gateway-in-process-module.md). Su ubicación vigente está en [ADR-0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md).

## 4. Flujo generativo (mapea FL-04)

```text
Alumno
   │  1. describe en lenguaje natural, o completa formulario
   ▼
Backend 2. autoriza y persiste contexto mínimo + catálogo habilitado completo
   │
   ▼
FastAPI  3. crea/recupera solicitud, encola su UUID y responde 202/200
   │
   ▼
Vercel Queues  4. entrega al consumidor privado
   │
   ▼
Servicio IA ──prompt versionado + schema──▶ ngrok -> Polo API ──▶ Ollama/Polo
   │  5. valida la respuesta y registra intento/resultado
   ▼
Backend 6. comprueba formato, IDs, disponibilidad actual y contexto vigente
   │
   ├─ inválida/fallo → un reintento; segundo fallo → NO_DISPONIBLE
   │
   ▼
Backend  7. crea directamente la rutina PROPUESTA y notifica al entrenador
```

Cada intento vence a los 120 segundos. Si el LLM no responde o el resultado no valida tras el único reintento, la generación queda `NO_DISPONIBLE`; no existe un generador determinístico alternativo. Las plantillas privadas y la creación manual del entrenador continúan operativas.

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

Salida: días → ejercicios → series y justificación, con IDs de la instantánea. IA evalúa la adecuación; backend valida sólo estructura, referencias, disponibilidad y vigencia del contexto. Puede declarar imposibilidad con motivo, sin crear rutina (data-interface.md).

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

Entrada: ejercicio original, contexto del alumno y todo el catálogo habilitado del gimnasio. IA evalúa efecto equivalente, patrón, nivel, condiciones y equipamiento, y propone hasta cinco alternativas justificadas.

Backend verifica IDs y disponibilidad, sin prefiltrado ni ranking alternativo. Si no hay opciones adecuadas, IA declara el motivo; si falla, se informa indisponibilidad y continúa la vía manual. La lista producida y las versiones se conservan para RF-072; no se reconstruye un orden pasado al reejecutar.

### 5.5 `describirPerfil` (RF-064)

Entrada: los indicadores de comportamiento ya calculados del alumno (frecuencia, volumen e intensidad relativos) y su objetivo vigente.

Salida: una etiqueta corta y un texto legible ("alta frecuencia, bajo volumen", en vez de un identificador de clúster). Se aplican las mismas restricciones de `valores_citados` de §5.3: el texto no introduce ninguna cifra ausente de la entrada. **El resultado es efímero** — se genera al abrir la vista del entrenador o del administrador y no se persiste. No hay clustering ni un modelo poblacional detrás.

## 6. Prompting

Cada capacidad usa system, schema, contexto JSON e instrucción de tarea separados y versionados. Los datos del alumno y de la fuente son contexto, nunca instrucciones. La prohibición de inventar cifras aplica a narrativos; el generador sí decide valores nuevos de prescripción.

`generarRutina` y `sugerirAlternativas` reciben el catálogo habilitado completo y el perfil de [data-interface.md](data-interface.md). El prompt pide evaluar objetivos, preferencias, disponibilidad, condiciones y equipamiento, justificar elecciones y declarar imposibilidad cuando corresponda. No recibe una lista reducida por alumno ni un conjunto de combinaciones o rangos calculados en código.

El schema restringe estructura, tipos y referencias. Alias por índice y grupos de series compactos son admisibles si su expansión es exacta; no se modifican valores ni se eligen complementos en el adaptador. Las solicitudes nuevas usan `generar-rutina@23`, con base compartida y variantes por tarea según [prompt-architecture.md §2.1](prompt-architecture.md#21-generación-de-rutinas-implementada). Se registra el digest del modelo y una firma de system, overlays, schema y parámetros. La forma compacta usa índices del catálogo y grupos de series elegidos por IA; la expansión preserva sus valores.

Se reserva contexto para entrada completa y respuesta; no truncar catálogo. Streaming requiere final explícito y límite total por intento. Logs de fallos guardan rutas y códigos técnicos sin prompts ni datos personales. Cambios de prompt requieren evaluación técnica y revisión de calidad por entrenador.

## 7. Tool calling: herramientas invocables desde el LLM

Esta entrega pasa el catálogo completo en el contexto y no requiere herramientas de recuperación ni `verificarCompatibilidad`. La adecuación la evalúa el modelo; no se ofrece una herramienta que esconda el filtro determinista retirado. La API y cola siguen orquestadas por código. ADR 0013 reemplaza esa parte de ADR 0008; los ajustes de candidato RF-119 continúan diferidos.

## 8. Contexto completo, sin RAG

No se usa recuperación semántica ni prefiltrado por entrenamiento: el catálogo habilitado completo es la fuente de candidatos. Las enumeraciones y el contexto se leen directamente de PostgreSQL. Si la ventana no alcanza, se informa capacidad insuficiente; una estrategia de recuperación o varias etapas necesitaría una decisión posterior. [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) reemplaza la justificación anterior de ADR 0007.

## 9. Guardrails

| Riesgo | Control |
| --- | --- |
| ID inventado, ajeno o no enviado | Rechazar por pertenencia a la instantánea y disponibilidad actual |
| JSON inválido o incompleto | Schema técnico; un reintento y luego indisponibilidad |
| Prescripción inadecuada o consejo médico | Instrucciones, evaluación de casos y revisión del entrenador; el validador técnico no garantiza adecuación |
| Inyección en preferencias o datos importados | Separar contexto de instrucciones, sin credenciales ni acceso del modelo a tablas o acciones de dominio |
| Cifras inventadas en textos narrativos | Comparar `valores_citados` con la entrada (RF-057, RNF-24) |
| Datos excesivos o contexto desactualizado | Minimización explícita y control de versiones antes de crear propuesta |

Un prompt no garantiza decisiones correctas. Se mide cuánto corrige o rechaza el entrenador y se conserva la propuesta original para evaluar calidad.

## 10. Evaluación de la IA generativa

Verificación automática: schema, IDs enviados, aislamiento, lista completa, fallos, timeout, reintento, cambios concurrentes y presupuesto de tokens. Confirmar que no se aplican top 32, exclusiones por alumno, cantidades extraídas por regex ni validaciones de rangos de entrenamiento.

Evaluación revisada por entrenador: alumnos sin historial, distintas experiencias y objetivos, condiciones activas, preferencias exigentes, inventario en conflicto con una habilitación, alternativas insuficientes y prescripciones extremas. Catálogo vacío debe detenerse antes del LLM; sólo peso corporal debe funcionar si esos ejercicios fueron habilitados.

Medir formato inválido, latencia, tokens, indisponibilidad, adherencia al pedido y tasa/magnitud de corrección o rechazo del entrenador. Validez técnica repetida y calidad de entrenamiento son métricas separadas; no se exige texto idéntico ni se presenta la primera como garantía de la segunda. La prueba de capacidad usa el catálogo completo y los 120 s por intento.

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

Generación y alternativas admiten un reintento ante fallo técnico; agotado o vencido el límite de 120 s por intento, se informa indisponibilidad. No hay prescripción, selección ni ranking determinista alternativo. El entrenador conserva creación manual y plantillas privadas; los presets requieren RF-021.

Catálogo vacío, capacidad insuficiente o contexto cambiado requieren resolver el motivo antes de una nueva solicitud. El resto del sistema y las sesiones siguen operativos. En textos descriptivos opcionales se muestran los indicadores disponibles sin el texto generado.

## 14. Observabilidad

Métricas por método del Gateway (`interpretarSolicitud`, `generarRutina`, `justificarRutina`, `resumirEvolucion`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil`):

- latencia (p50/p95/p99);
- tokens de entrada y salida;
- throughput (llamadas/minuto);
- tasa de error y de timeout;
- tasa de reintento (RF-113);
- tasa de indisponibilidad y derivación a creación manual;
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

El runtime autohospedado requiere operación, recursos y una configuración de contexto medidos. La cantidad de ejercicios almacenados o de valores de equipamiento no demuestra que el prompt entre en memoria.

Antes de habilitar la nueva generación, medir catálogo completo + perfil + prompt + schema + respuesta con los gimnasios previstos, y comprobar memoria, latencia y concurrencia. Configurar modelo/ventana adecuados o informar indisponibilidad sin recortar candidatos. No afirmar capacidad de producción con estimaciones sin medición; [catálogo y disponibilidad](exercise-catalog.md) define el comportamiento ante falta de capacidad.
