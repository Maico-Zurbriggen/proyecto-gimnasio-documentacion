# ADR 0004: LLM autohospedado sobre infraestructura del Polo Educativo

- Estado: aceptada
- Fecha: 2026-08-25

## Contexto

RF-053 a RF-058, RF-075 y RF-108 requieren un servicio de generación de lenguaje. [D12/S-05](../../planning/risks-and-assumptions.md) asume "un servicio de generación gratuito o de coste muy bajo con calidad suficiente" sin especificar si es un proveedor externo (API de terceros) o un modelo propio. La Universidad ofrece un servidor administrado por el Polo Educativo para este propósito.

## Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | API de un proveedor externo (OpenAI, Anthropic, etc.) | Datos de condiciones físicas y hábitos de entrenamiento de los alumnos salen de la infraestructura de la Universidad hacia un tercero. Coste variable por token, dependiente de un servicio fuera de control del proyecto. Cumple S-05 ("servicio gratuito o de bajo coste") sólo si el proveedor ofrece nivel gratuito suficiente |
| (b) | **LLM autohospedado en el servidor del Polo Educativo** | Ningún dato de alumnos sale de la infraestructura de la Universidad. Coste de operación (no de API) asumido por la institución. Requiere que alguien administre el runtime |
| (c) | Sin componente generativo, todo por formulario estructurado | Cumple RF-058 como comportamiento normal en vez de como fallback, pero renuncia a RF-053 y RF-055 tal como están redactados, y a la propuesta de valor declarada en [D1 §3.0](../../product/vision-and-objectives.md) sobre la interpretación de lenguaje natural |

## Decisión

(b). El LLM corre autohospedado en el servidor del Polo Educativo.

## Fundamento

RNF-21 ya exige que los datos de condiciones físicas, aptitud y mediciones sólo se traten con consentimiento explícito registrado; enviarlos a un proveedor externo de generación agrega una parte procesadora adicional que complica ese consentimiento y la trazabilidad de RNF-19. El self-hosting resuelve esto de raíz: el dato no sale del perímetro de la institución. Además, (a) hace que la disponibilidad y el coste del componente generativo dependan de un tercero fuera del control del proyecto, mientras que RF-058 ya asume que ese servicio puede no estar disponible — tener el servidor bajo administración propia (institucional) da más control sobre esa disponibilidad que un proveedor externo.

## Consecuencias

- El equipo (o el Polo Educativo) debe operar, actualizar y monitorear un proceso de inferencia — trabajo no incluido en las 504 h de capacidad de construcción de [D12/§3](../../planning/risks-and-assumptions.md); debe declararse como carga adicional real, coordinada con la institución.
- El hardware disponible es `NO VERIFICADO` al momento de esta decisión — ver [generative-ai.md §2](../../architecture/generative-ai.md). El tamaño de modelo elegido debe ser configuración, no una decisión fija, hasta que se confirme.
- Se mantiene RF-058 como comportamiento de excepción (indisponibilidad puntual), no como comportamiento normal — a diferencia de la opción (c).
- Ver [ADR-0006](0006-llm-model-and-runtime-selection.md) para qué modelo y runtime corren sobre esta infraestructura.
