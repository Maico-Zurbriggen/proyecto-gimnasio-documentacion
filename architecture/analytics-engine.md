# Arquitectura del repositorio de IA

## Dos límites ejecutables

`proyecto-gimnasio-ia` contiene componentes separados:

1. **Servicio generativo online:** API Python y worker asíncrono desplegados en el Polo.
2. **Analítica batch:** extracción, features, entrenamiento, evaluación y scoring predictivo futuros.

Compartir repositorio no permite que un componente use la frontera del otro ni que el trabajo batch entre en una petición.

## Servicio generativo

Límite ejecutable del mismo repositorio: API Python + worker en el Polo detrás de ngrok. Diseño, flujo y ambientes canónicos en [generative-ai-integration.md](generative-ai-integration.md); contratos por prompt en [prompts-catalogo.md](prompts-catalogo.md). Regla de frontera (vale para ambos límites): compartir repositorio no permite usar la frontera del otro — el trabajo batch nunca entra en una petición, y el servicio online nunca escribe entidades de dominio.

## Analítica batch

- Lee vistas o snapshots versionados acordados con backend.
- Escribe resultados precalculados con versión, instante y explicación.
- No modifica fuentes transaccionales.
- Ejecuta extracción, validación, features point-in-time, entrenamiento, evaluación y persistencia idempotente.
- Si un modelo no supera un criterio simple, se conserva el criterio simple.

## Operación en el Polo

API, worker, LLM y agente ngrok son procesos distintos. Deben arrancar con la máquina, reiniciarse ante fallos y exponer salud observable. Ngrok publica sólo la API Python mediante un dominio estable; el LLM queda local o privado.

## Invariantes

- Ningún dato identificatorio innecesario llega al LLM.
- Ninguna salida se publica sin modelo, configuración, instante y contexto mínimo reproducible.
- El rol PostgreSQL de IA no accede a identidad ni modifica entidades de dominio.
- Ninguna feature batch usa información posterior al instante predicho.
- Falta de datos no equivale a cero.
- Los datos simulados se identifican y no se presentan como reales.
