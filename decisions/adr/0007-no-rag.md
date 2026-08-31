# ADR 0007: sin RAG semántico, con prefiltrado determinista del catálogo

- Estado: aceptada, revisada
- Fecha: 2026-08-25 (revisión: mismo día, tras objeción sobre el tamaño del catálogo)

## Contexto

RAG (indexar un corpus, recuperarlo por similitud semántica y dárselo al LLM como contexto) es una técnica habitual cuando un componente generativo necesita consultar conocimiento dinámico que no cabe ni conviene fijar en el prompt. Antes de descartarla o adoptarla había que determinar si alguno de los componentes generativos de este proyecto (RF-053 a RF-058, RF-075, RF-108, RF-119) tiene esa necesidad.

**Revisión de esta ADR**: la primera versión concluyó "no RAG" apoyándose sólo en que las enumeraciones cerradas de [D2 §4](../../product/glossary.md) son chicas, sin analizar el tamaño del catálogo de ejercicios — el otro conocimiento que el LLM necesita para RF-054/RF-119. Un catálogo prescribible de gimnasio (base + propio, filtrado por equipamiento) puede tener perfectamente decenas a un par de cientos de ejercicios, no es automáticamente "chico". Esta versión corrige ese análisis incompleto.

## Análisis

Qué conocimiento necesita cada componente generativo, y de qué tamaño es:

| Componente | Conocimiento que necesita | Tamaño | ¿Es candidato a RAG semántico? |
| --- | --- | --- | --- |
| RF-053 · interpretación de NL | Las 12 enumeraciones cerradas de [D2 §4](../../product/glossary.md) | Fijo y pequeño (cientos de tokens) | No: entra completo en el prompt |
| RF-054/RF-119 · generación de rutina y candidato | El catálogo prescribible del gimnasio, y dentro de él las alternativas de un patrón de movimiento puntual | Variable, potencialmente no chico (decenas a cientos de ejercicios por gimnasio) | **No, pero por una razón distinta a "es chico"**: ver más abajo |
| RF-055, RF-056, RF-075/RF-108 · narrativos | Estructuras y valores ya calculados por el backend o el motor batch | Acotado por alumno | No: la entrada es exactamente el dato que hay que redactar, no algo que buscar |

**Por qué el catálogo tampoco necesita RAG semántico, a pesar de no ser trivialmente chico.** El problema de "qué ejercicios son válidos para esta rutina/este ejercicio a sustituir" no es un problema de búsqueda por similitud difusa — es un filtro **exacto** sobre atributos estructurados que el sistema ya calcula en código: patrón de movimiento pedido, compatibilidad con las condiciones del alumno (RN-44a-d), equipamiento presente en el inventario (RN-45). RN-46 exige que una incompatibilidad **impida** poner la rutina en vigencia — es una regla dura, no una preferencia. Un vector store resuelve por similitud aproximada, que es la herramienta equivocada para una condición que tiene que ser exacta y auditable.

La solución correcta no es "no hace falta ningún tipo de recuperación": es que el **backend prefiltra el catálogo de forma determinista antes de construir el prompt**, con el mismo código que ya exige RN-44a-d/RN-45 para la validación posterior. El LLM nunca ve el catálogo completo; ve el subconjunto ya compatible y ya acotado por patrón, que en la práctica queda en el orden de decenas de ejercicios por llamada — dentro del presupuesto de contexto de cualquiera de los modelos evaluados en [ai-model-selection.md](../../architecture/ai-model-selection.md) sin dificultad.

## Decisión

No se implementa RAG semántico (embeddings + vector store). El conocimiento que cada componente generativo necesita se entrega como contexto estructurado directo (JSON armado por el backend), y en el caso del catálogo, **prefiltrado de forma determinista** por el mismo código que ya hace cumplir RN-44a-d/RN-45, antes de construir el prompt — no el catálogo completo, no una búsqueda por similitud.

## Fundamento

Adoptar RAG semántico sin necesidad real agrega un almacén vectorial, un pipeline de ingesta/chunking/embeddings y una etapa de recuperación (con su propio re-ranking, actualización y trazabilidad) a un proyecto con capacidad de construcción ya ajustada ([D12/§3](../../planning/risks-and-assumptions.md)), para resolver un problema que un filtro SQL con `WHERE` ya resuelve de forma exacta, auditable y más barata de mantener — y que además hay que ejecutar de todas formas como validación determinista (RF-113), así que no ejecutarlo también como filtro previo sería trabajo duplicado, no ahorro. El prefiltrado determinista no es una alternativa más liviana a RAG: es la herramienta correcta para un problema de filtro exacto, mientras que RAG semántico está pensado para un problema de similitud aproximada que este proyecto no tiene.

## Consecuencias

- El contexto de cada llamada generativa se arma en el backend con acceso directo a los datos transaccionales, no en una capa de recuperación separada.
- El catálogo que llega al prompt de `generarRutina`/`sugerirAlternativas` (ver [generative-ai.md §7](../../architecture/generative-ai.md)) es siempre el subconjunto ya filtrado por patrón + compatibilidad + inventario, nunca el catálogo completo del gimnasio.
- **Umbral explícito de reapertura**: si el catálogo prescribible filtrado de un gimnasio (ya acotado, no el catálogo entero) creciera lo suficiente como para no entrar cómodo en el presupuesto de contexto del modelo elegido, corresponde reabrir esta decisión y evaluar recuperación semántica o paginación — no se espera que esto ocurra con equipamiento típico de gimnasio (22 valores de equipamiento, 9 patrones de movimiento — [D2 §4](../../product/glossary.md)), pero queda como condición de disparo explícita en vez de un "algún día" vago.
- Si en el futuro el sistema incorpora una base de conocimiento grande y no estructurada (por ejemplo, una biblioteca de metodología de entrenamiento en texto libre que el LLM deba consultar), esta decisión debe reabrirse explícitamente con su propio ADR — no debe agregarse RAG por extensión silenciosa de este diseño.
