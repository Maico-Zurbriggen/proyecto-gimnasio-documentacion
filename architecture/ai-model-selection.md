# Selección de modelo y runtime para la IA generativa

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto, sujeto a revalidación cuando el hardware del servidor institucional esté verificado |
| **Depende de** | [generative-ai.md](generative-ai.md), [ADR-0006](../decisions/adr/0006-llm-model-and-runtime-selection.md) |

Este documento separa dos decisiones distintas que suelen confundirse: **qué modelo** correr y **qué runtime** usar para servirlo. Cambiar una no obliga a cambiar la otra.

## 1. Modelo

No se asumió de antemano que Llama o Qwen fueran la mejor opción. Se evaluaron cuatro familias con pesos abiertos, self-hostable, en el rango de tamaño realista para un servidor institucional de uso compartido (7B-14B parámetros, cuantizado).

| Familia | Licencia | Español / multilingüe | Tool calling / structured output | Ecosistema | Riesgo específico |
| --- | --- | --- | --- | --- | --- |
| **Qwen2.5 / Qwen3 (7B-14B)** | Apache 2.0 en los tamaños ≤32B, sin tope de uso | Mejor que Llama 3.1 en benchmarks multilingües/no-inglés a tamaño equivalente | Maduro, bien documentado | Amplio soporte GGUF/Ollama/vLLM | Ninguno relevante encontrado |
| **Llama 3.1 / 3.3 (8B)** | Licencia propia Meta: tope de 700M usuarios activos mensuales (no aplica a este proyecto), exige atribución "Built with Llama" | Soporta español, algo por detrás de Qwen en benchmarks no-inglés al mismo tamaño | Maduro | El más amplio de los cuatro: mayor cantidad de tutoriales, fine-tunes e integraciones | Licencia menos permisiva que Apache 2.0; restricciones de campo de uso a revisar si el proyecto cambia de naturaleza (académico → comercial) |
| **Gemma 2 / 3 (9B-12B)** | Licencia propia Google, sin tope de escala de usuarios | Buena calidad general | Buena | Eficiente en RAM, apta para hardware modesto | La licencia incorpora una **política de uso prohibido que restringe la generación de contenido en áreas médicas/de salud**, y Google se reserva el derecho de restringir remotamente un uso que la viole. Este proyecto redacta sobre condiciones físicas y pautas nutricionales — zona gris real, no descartable sin revisión legal |
| **Mistral 7B / Small** | Apache 2.0, sin restricciones | Aceptable, sin evidencia de liderazgo frente a Qwen en español | Soporte nativo de JSON mode y tool calling | Buen soporte en Ollama/vLLM | Ninguno relevante; queda como alternativa de respaldo |

**Fuentes consultadas** (documentación oficial y análisis de licencia, no rankings aislados): repositorios y model cards de Hugging Face para las licencias de Qwen2.5 por tamaño; análisis de la licencia de Gemma en TechCrunch y WCR.LEGAL sobre restricciones de uso; comparativas de rendimiento multilingüe y de soporte de runtime publicadas en 2025-2026 (ComputingForGeeks, benchmarks de tool calling en producción). Búsquedas realizadas en agosto de 2026; **revalidar antes de desplegar**, dado el ritmo de estas familias.

### Decisión

**Qwen2.5-7B-Instruct** como modelo primario (o Qwen2.5-14B-Instruct si el hardware verificado lo permite con margen sobre RNF-04). Motivos, en orden de peso para este proyecto:

1. **Licencia**: Apache 2.0 sin tope de uso ni política de contenido restringido — es la única de las cuatro sin una zona de riesgo legal identificada para este dominio específico (salud/condición física).
2. **Español/multilingüe**: mejor evidencia relativa a tamaño equivalente que Llama 3.1, que es el candidato con el que más se lo compara por defecto.
3. **Structured output / tool calling**: maduro, necesario para RF-053/RF-054/RF-113 (validación de JSON Schema, reintento).
4. **Ecosistema de despliegue**: soporte GGUF amplio, compatible con Ollama de forma directa.

**Llama 3.1-8B-Instruct** queda documentado como alternativa de segunda preferencia: si la evaluación empírica sobre el conjunto de casos de [generative-ai.md §9](generative-ai.md) muestra que Llama supera a Qwen en el dominio real del proyecto, o si el ecosistema de soporte comunitario resulta determinante para el equipo, se promueve sin cambiar nada fuera del AI Gateway (ver §15 de [generative-ai.md](generative-ai.md)).

**Gemma queda deprioritizada**, no descartada de forma absoluta: si Qwen y Llama no cumplen calidad o rendimiento, Gemma es la siguiente opción a evaluar, pero requiere antes una revisión legal explícita de la política de uso prohibido contra el contenido real que este sistema genera (condiciones físicas, pauta nutricional).

**Mistral** queda como plan de respaldo con la misma licencia permisiva que Qwen, útil si Qwen no rinde bien en las pruebas iniciales.

## 2. Runtime de inferencia

No confundir con el modelo: el runtime es el proceso que sirve el modelo, no el modelo en sí.

| Runtime | Operación | Uso de GPU | Batching/concurrencia | Structured output / tool calling | Observabilidad | Compatibilidad con hardware desconocido |
| --- | --- | --- | --- | --- | --- | --- |
| **Ollama** | Muy simple: un binario, un comando para cambiar de modelo (`ollama pull`) | Automática si hay GPU disponible, con fallback a CPU | Se degrada notablemente por encima de ~5 usuarios concurrentes según pruebas publicadas en 2025-2026 | API compatible con OpenAI, structured outputs y tool calling ya maduros, compatible de inmediato con clientes HTTP estándar | Básica (logs, métricas limitadas) | Alta: mismo binario corre en CPU o GPU sin cambiar la integración |
| **vLLM** | Requiere más configuración y tuning | Explícito, orientado a GPU | Excelente: PagedAttention sostiene alta concurrencia, ~6x el throughput de Ollama medido a 50 usuarios concurrentes en benchmarks publicados | Nativo y sólido | Mejor soporte de métricas de producción | Media: pensado para GPU dedicada, menos cómodo si el servidor termina siendo CPU-only |
| **llama.cpp** | Motor subyacente de Ollama; usarlo de forma directa agrega trabajo de integración sin ganancia si ya se usa Ollama | Sí, eficiente en CPU también | Limitada | Incompleto en la API directa (depende de la envoltura que se use) | Mínima sin envoltura adicional | Alta, pero redundante con Ollama para este proyecto |

### Decisión

**Ollama** como runtime primario. Con la carga esperada de este proyecto (estimada en [generative-ai.md §16](generative-ai.md): del orden de cientos de llamadas/día, muy por debajo del umbral de degradación observado en Ollama), la ventaja operativa —un equipo sin especialización en MLOps, sin GPU garantizada, necesitando cambiar de modelo sin fricción— pesa más que el throughput de producción de vLLM, que este proyecto no necesita todavía.

**vLLM queda documentado como ruta de escalamiento**, no como plan B inmediato: si el uso real supera el umbral de concurrencia donde Ollama se degrada (evidencia: a partir de ~5 usuarios simultáneos), se reemplaza el adaptador (`OllamaAdapter` → `VllmAdapter`) detrás del mismo puerto (`GenerativeAiPort`), sin cambios en el resto del backend.

**llama.cpp no se adopta como runtime directo**: ya es el motor detrás de Ollama para los formatos GGUF; adoptarlo por separado sólo agregaría una integración a mantener sin resolver nada que Ollama no resuelva ya para este proyecto.

## 3. Resumen de la decisión

```text
Modelo:   Qwen2.5-7B-Instruct (GGUF, Q4_K_M/Q5_K_M según hardware verificado)
Runtime:  Ollama
Gateway:  puerto + adaptador dentro del servicio Python del Polo
          (patrón de ADR-0005; despliegue según ADR-0009)
```

Justificación completa y consecuencias en [ADR-0006](../decisions/adr/0006-llm-model-and-runtime-selection.md).
