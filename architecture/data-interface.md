# Interfaz de datos con el backend

## Principio

PostgreSQL contiene dos interfaces diferentes para IA: estructuras operativas de generación online y datasets versionados para analítica batch. Backend es dueño de ambas definiciones y de sus migraciones.

## Generación online

**Contrato `2.0` implementado localmente el 2026-10-07.** [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) sustituye el prefiltrado, el máximo de 32 y las restricciones deterministas de entrenamiento. Todas las solicitudes nuevas usan `2.0`; se mantiene el camino `1.0` únicamente para solicitudes anteriores durante la transición. El despliegue requiere promoción coordinada; no reinterpretar solicitudes históricas.

Backend persiste idempotentemente solicitud y contexto en `ai_integration.ai_generation_requests`, y registra el ownership alumno–solicitante en `app.routine_generation_ownership`. El servicio IA recibe sólo el UUID, comprueba que siga procesable y lo encola. Lee la instantánea con su rol restringido y escribe únicamente estados y resultados técnicos; backend crea la PROPUESTA al finalizar. Preview y Production usan conexiones fijas distintas; el cliente no elige base o ambiente.

La instantánea versionada contiene:

| Campo lógico | Contenido |
| --- | --- |
| Perfil mínimo | Experiencia, disponibilidad, objetivo vigente, condiciones activas por zona y severidad, estado de aptitud; edad u otros datos sólo si aportan a la tarea |
| Historial disponible | Rutina vigente e indicadores recientes, con período e instante: volumen, frecuencia, adherencia y esfuerzo registrado. Si no hay datos, declararlo; no convertir ausencia en cero |
| Pedido y preferencias | Texto original y parámetros declarados; IA interpreta prioridades y cantidades, sin extracción mediante regex ni selección del backend |
| Equipamiento | Inventario real del gimnasio como contexto; no intersección automática de candidatos |
| `allowed_catalog` completo | Todos los ejercicios aprobados y habilitados del gimnasio: UUID, revisión, nombre, instrucciones completas, descripción, consejos, patrón, dificultad, unilateralidad, músculos primarios/secundarios, equipamiento y articulaciones |
| Trazabilidad | Versión de contrato, instante de captura y versiones o hashes del contexto y las fichas; prompt, modelo e intento en el resultado |

Comparar por separado versiones del perfil/inventario y revisiones de las fichas seleccionadas. El hash de toda la instantánea sirve para trazabilidad; una habilitación nueva, por sí sola, no vuelve desactualizado un resultado (RN-141).

No enviar imágenes, URLs de media, nombres de personas, correo, credenciales o descripciones médicas libres. Orden y alias por índice sólo compactan el transporte; IA puede expandir índices y grupos de series sin cambiar selecciones o cantidades.

La salida estructurada conserva tipo, frecuencia, días ordenados, UUID de ejercicios, series, repeticiones, carga opcional, descanso, calentamiento y justificación. El contrato distingue `PROPOSED` con `explanation`/`warnings` y `UNABLE` con `reason`/`missing_information`; esta última no crea una rutina vacía. `suggested_load: null` significa sin especificar; cero mantiene su significado propio (RN-43). Las versiones creadas siguen con `current: false` hasta aprobación.

El validador sólo comprueba schema, tipos, referencias, pertenencia a la instantánea, disponibilidad actual y contexto vigente (RN-141). Límites de tamaño protegen transporte y recursos; no codifican rangos de entrenamiento, cantidades por músculo, cobertura de patrones ni compatibilidad. La estructura no puede referenciar otro gimnasio ni ejercicios no enviados. La adecuación de la prescripción se decide con IA y revisión del entrenador.

La expansión y persistencia admiten hasta 500 series totales por respuesta como protección de memoria, tamaño y duración transaccional; no se recorta una respuesta que exceda esa capacidad. No es una recomendación de volumen de entrenamiento.

Si el resultado no pasa controles técnicos, admite un reintento; si el contexto cambió, se pide una solicitud nueva. El catálogo vacío o un presupuesto de tokens insuficiente se informan antes de inferir, sin truncamiento. Detalle en [catálogo y disponibilidad](exercise-catalog.md). Solicitudes abandonadas y fallos se eliminan a los 30 días; resultados aceptados conservan contexto mínimo y versiones con acceso restringido según auditoría.

## Analítica batch


Cada job declara:

- nombre y versión del dataset de entrada;
- columnas, tipos, nulabilidad y unidades;
- instante de corte y zona horaria;
- claves de idempotencia;
- tabla o artefacto de salida;
- versión del componente y parámetros.

El motor batch sólo escribe salidas designadas y no actualiza sesiones, rutinas, usuarios ni otras fuentes transaccionales.

## Desarrollo y pruebas

Backend e IA pueden usar PostgreSQL local persistente para desarrollo; IA conserva su rol restringido. El ambiente integrado usa Neon Test. Nunca copiar datos reales de alumnos ni el dataset licenciado al repositorio. Las pruebas usan fixtures sintéticos y comprueban lista completa, aislamiento, contrato, concurrencia e idempotencia; la adecuación se evalúa con casos revisados por entrenador.

## Cambios

El schema publicado por IA es `openapi/routine-generation-v2.schema.json`; se genera con `scripts/export_generation_contract.py`. Backend valida la unión versionada y existen fixtures en ambos repositorios. Las solicitudes nuevas no incluyen `prescription_constraints`, `muscle_counts_per_day`, combinaciones prefijadas y selección top 32. No usar esos campos históricos como reglas sobre solicitudes nuevas.

Un cambio incompatible requiere versión nueva, migración o adaptación preparada por backend, compatibilidad temporal, PR relacionados y despliegue por etapas. La implementación de ambos consumidores está preparada; verificar el runtime y revisar casos de entrenamiento antes de promover. El resumen de historial cubre 28 fechas locales, sesiones ya completadas y medias por ejercicio; ausencia de carga o esfuerzo se conserva como `null`. Las referencias del historial y catálogo comparten índices sólo durante transporte al LLM. `profile_hash` incorpora perfil, inventario y contexto; las fichas seleccionadas se comprueban por revisión material y de habilitación.
