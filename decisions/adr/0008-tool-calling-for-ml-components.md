# ADR 0008: componentes clásicos expuestos como herramientas del LLM, no reimplementados en él

- Estado: **revisada** (2026-08-28) — ver la nota de revisión al final
- Fecha: 2026-08-25

## Contexto

RF-059 (ranking de alternativas de sustitución) se invoca desde dentro del flujo de creación de rutina asistido por el LLM (FL-04/A4). Esto planteó una pregunta real: si ya se está usando un LLM para interpretar, generar y justificar la rutina, ¿no debería el mismo LLM también ordenar las alternativas de sustitución, en vez de mantener un componente clásico aparte? La misma pregunta aplica, con menos fuerza, a la segmentación de perfiles (RF-064).

## Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | El LLM razona en lenguaje natural sobre el catálogo y produce el orden de alternativas él mismo | Un único componente para todo el flujo, pero pierde reproducibilidad exacta (RF-072/RNF-27), necesita de todas formas una re-validación determinista posterior (RF-060/RN-44a-d) porque no se puede confiar en que el LLM excluya correctamente lo contraindicado, y ata FL-06 (sustitución durante una sesión, sin lenguaje natural de por medio) a la disponibilidad del LLM Server sin necesidad |
| (b) | **El ranking se sigue calculando con el modelo/regla clásica ya descrita en `predictive-ai.md`, expuesto al LLM como una herramienta invocable (tool calling) durante FL-04, y llamado directamente por el backend en FL-06** | Un cálculo, dos formas de invocarlo. El LLM decide cuándo pedir alternativas; el modelo clásico calcula cuáles, de forma reproducible y ya validada |
| (c) | Dos implementaciones separadas y no relacionadas: una para el flujo generativo, otra para FL-06 | Duplica el mantenimiento de la misma lógica de negocio (RN-49a) en dos lugares, con riesgo real de que diverjan |

## Decisión (original — parcialmente reemplazada, ver nota de revisión)

(b). El ranking de RF-059 (y, del mismo modo, la verificación de compatibilidad de RN-44a-d cuando se usa dentro del flujo generativo) se mantiene como cómputo clásico, expuesto al AI Gateway como una función que el LLM puede invocar mientras arma el candidato de rutina.

## Fundamento

RF-060 exige excluir de forma dura los ejercicios contraindicados o de nivel superior — una condición que ya corre en código (RN-44a-d) y que, por RF-113, se re-valida sobre cualquier salida antes de mostrarla al usuario. Si el LLM también calculara el ranking, esa validación determinista tendría que ejecutarse de todas formas como red de seguridad — es decir, el costo del cómputo clásico ya está pagado sí o sí, y dejar que el LLM lo intente además no ahorra nada, sólo agrega una fuente más de variabilidad y una llamada más al modelo. RF-072/RNF-27 exigen reproducibilidad exacta a partir de versión y contexto guardado: un ranking por similitud sobre atributos estructurados (patrón de movimiento, participación muscular) es exactamente reproducible; un ranking producido por generación de lenguaje no lo es entre corridas ni entre versiones de modelo. Y RF-059 se usa también en FL-06 (sustitución durante una sesión en curso, sin lenguaje natural, con necesidad de responder rápido) — atarlo a la disponibilidad del LLM Server introduciría una dependencia que hoy no existe, contra RNF-11.

La pregunta que motivó esta ADR tiene una respuesta general, no sólo para RF-059: **la ubicación en el flujo (dónde se invoca) no determina la técnica que resuelve el problema (cómo se calcula)**. Un LLM con tool calling maduro (ya elegido en [ADR-0006](0006-llm-model-and-runtime-selection.md) también por esta razón) permite que ambas cosas convivan: el modelo de lenguaje orquesta la conversación y decide cuándo necesita un dato o un cálculo; los componentes especializados —deterministas o de ML clásico— siguen siendo la fuente de ese dato o cálculo.

## Consecuencias

- El AI Gateway expone `verificarCompatibilidad` como herramienta invocable además de los métodos de generación/interpretación/redacción ya descritos en `generative-ai.md §5`. Ver `generative-ai.md §7` para el contrato completo.
- Ningún componente de compatibilidad se reimplementa dentro de un prompt.

---

## Nota de revisión (2026-08-28) — replanteo de IA

Tras el replanteo de alcance de IA ([D11/DD-34](../design-decisions.md)), **la parte de esta ADR referida al ranking de RF-059 se reemplaza por la opción (a)**: el orden de las alternativas de sustitución lo produce ahora la capa generativa (`sugerirAlternativas`, `generative-ai.md §5.4`), no un modelo clásico. Motivos del cambio de contexto:

- Ya no existe un modelo/regla clásica de ranking en `predictive-ai.md` que exponer — construirlo y mantenerlo era costo que el proyecto decidió no asumir (S-03, capacidad de 504 h).
- Se acepta la pérdida de reproducibilidad **exacta**: RF-059 pasa al estándar de "validez repetida" del resto de la capa generativa (`generative-ai.md §10`), y RF-072/RNF-27 se cumplen **persistiendo la lista producida**, no reejecutándola.
- FL-06 (sustitución en sesión) pasa a invocar el LLM, con el orden determinista de RN-49a como fallback cuando el LLM no responde (RN-99). Esto amplía la superficie de dependencia del LLM Server — declarado como consecuencia asumida en DD-34 y D12/§4.

**Lo que de esta ADR sigue vigente sin cambios:** `verificarCompatibilidad` como herramienta determinista invocable, la exclusión dura de RN-44a-d en código, y el principio de que "dónde se invoca ≠ cómo se calcula" para los componentes que sí son deterministas (compatibilidad, diagnóstico, ajustes, estructura).
