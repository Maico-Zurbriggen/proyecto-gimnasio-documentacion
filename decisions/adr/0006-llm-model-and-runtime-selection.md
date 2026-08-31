# ADR 0006: modelo Qwen2.5-7B-Instruct sobre runtime Ollama

- Estado: aceptada, sujeta a revalidación cuando el hardware del servidor institucional esté verificado
- Fecha: 2026-08-25

## Contexto

RF-053 a RF-058 necesitan un modelo de lenguaje self-hostable y un runtime que lo sirva. No se debía asumir de antemano que Llama o Qwen fueran la mejor opción; había que reunir evidencia sobre licencia, calidad en español, soporte de salida estructurada/tool calling y ecosistema de despliegue antes de elegir. La comparación completa está en [ai-model-selection.md](../../architecture/ai-model-selection.md); este ADR registra la decisión y su fundamento.

## Opciones de modelo

Qwen2.5/3 (7B-14B), Llama 3.1/3.3 (8B), Gemma 2/3 (9B-12B), Mistral 7B/Small. Comparadas en licencia, calidad en español/multilingüe, soporte de structured output/tool calling y ecosistema — ver tabla completa en [ai-model-selection.md §1](../../architecture/ai-model-selection.md).

## Opciones de runtime

Ollama, vLLM, llama.cpp. Comparadas en operación, uso de GPU, concurrencia y madurez de structured output/tool calling — ver tabla completa en [ai-model-selection.md §2](../../architecture/ai-model-selection.md).

## Decisión

**Modelo: Qwen2.5-7B-Instruct** (o 14B si el hardware verificado lo permite dentro del presupuesto de RNF-04), cuantizado GGUF.
**Runtime: Ollama.**

## Fundamento

**Modelo.** Qwen2.5 en los tamaños ≤32B tiene licencia Apache 2.0 sin tope de uso ni política de contenido restringido; es la única de las cuatro familias evaluadas sin una zona de riesgo legal identificada para el contenido real que este sistema genera (condiciones físicas, pauta nutricional orientativa). Gemma, en cambio, incorpora una política de uso prohibido que restringe explícitamente la generación de contenido médico/de salud, con derecho de Google a restringir remotamente un uso que la viole — un riesgo real y no descartable sin revisión legal para este dominio, dado RF-057 y RF-075/RF-108. Llama 3.1 tiene una licencia utilizable para este proyecto (el tope de 700M MAU no aplica) pero es menos permisiva que Apache 2.0 y, según la evidencia relevada, rinde algo por detrás de Qwen en tareas no inglesas al mismo tamaño — un factor decisivo dado que este es un producto en español. Mistral queda como alternativa de respaldo con la misma licencia permisiva, sin evidencia de ventaja sobre Qwen en español.

**Runtime.** La carga esperada (estimada en [generative-ai.md §16](../../architecture/generative-ai.md): del orden de cientos de llamadas por día) está muy por debajo del umbral donde, según la evidencia relevada, Ollama empieza a degradarse frente a vLLM (~5 usuarios concurrentes). Ollama resuelve mejor la restricción real de este proyecto: un equipo sin especialización en operación de modelos, sobre un hardware `NO VERIFICADO` que puede terminar siendo sólo CPU — Ollama corre en ambos casos con la misma integración, mientras que vLLM está pensado para GPU dedicada y agrega complejidad de configuración que no se traduce en beneficio a esta escala.

## Consecuencias

- El modelo y su cuantización quedan fijados en configuración del AI Gateway ([ADR-0005](0005-ai-gateway-in-process-module.md)), no hardcodeados, porque el hardware real del servidor institucional todavía no está verificado.
- Llama 3.1-8B queda documentado como segunda preferencia si la evaluación empírica sobre el conjunto de casos de [generative-ai.md §9](../../architecture/generative-ai.md) lo justifica.
- Gemma no se adopta sin que antes exista una revisión legal explícita de su política de uso frente al contenido real generado por este sistema.
- Si la concurrencia real supera lo que Ollama sostiene bien, se reemplaza `OllamaAdapter` por `VllmAdapter` detrás del mismo puerto, sin tocar el resto del backend (ver [generative-ai.md §15](../../architecture/generative-ai.md)).
- Esta decisión debe revisarse cuando el hardware del servidor del Polo Educativo se confirme, y periódicamente, dado el ritmo de publicación de estas familias de modelos.
