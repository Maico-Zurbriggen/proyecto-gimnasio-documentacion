# ADR 0013: RepDB, habilitación por gimnasio y selección por IA

- Estado: aceptada; implementación pendiente
- Fecha: 2026-10-05
- Fuente: decisión explícita del usuario en la sesión de diseño del catálogo

## Contexto

El diseño anterior derivaba disponibilidad del inventario y prefiltraba por compatibilidad antes del LLM. El usuario eligió RepDB, habilitación explícita de ejercicios por gimnasio y decisiones de entrenamiento a cargo de IA.

## Decisión

Adoptar el recorrido de [catálogo e importación](../../architecture/exercise-catalog.md), con vocabulario y reglas actualizados en D2–D6. La habilitación es una relación N:M y no una copia del ejercicio ni un cambio de su propietario. El backend entrega toda la disponibilidad declarada y mantiene autorización, integridad, contexto vigente y persistencia; IA decide selección, adecuación y prescripción, y el entrenador conserva la aprobación.

Esta decisión reemplaza DD-31 y las partes de DD-26, DD-34, ADR 0007 y ADR 0008 que imponían prefiltrado, ranking, comprobación determinística de compatibilidad o restricciones de entrenamiento al generador. No adopta RAG ni herramientas de compatibilidad en código. Los cálculos de indicadores y el diagnóstico batch quedan fuera de este cambio.

## Consecuencias

La validación técnica no garantiza que una rutina sea adecuada al alumno. Se evalúan errores de la IA y correcciones del entrenador. El catálogo completo exige medir contexto y latencia; no se acepta truncarlo para conservar el límite anterior. El código actual todavía usa prefiltrado, selección de 32 y validadores de entrenamiento: actualizarlo requiere migración y cambios coordinados de backend, frontend e IA, sin modificar migraciones aplicadas.

El contrato de la nueva generación se define en [data-interface.md](../../architecture/data-interface.md). La [referencia física](../../architecture/database-schema-reference.md) y los [diagramas implementados](../../architecture/implemented-sequence-diagrams.md) continúan describiendo el software existente hasta que se implemente la migración.
