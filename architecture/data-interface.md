# Interfaz de datos con el backend

## Principio

PostgreSQL contiene dos interfaces diferentes para IA: estructuras operativas de generación online y datasets versionados para analítica batch. Backend es dueño de ambas definiciones y de sus migraciones.

## Generación online

- Backend persiste de forma idempotente la solicitud, el contexto minimizado y el catálogo prescribible prefiltrado en `ai_integration.ai_generation_requests`; nunca guarda PII innecesaria ni una URL de base en ese contexto.
- Backend registra en `app.routine_generation_ownership` la relación entre solicitud, alumno y usuario solicitante; en esta etapa el solicitante es siempre ese mismo alumno.
- La API IA sólo recibe el UUID técnico de una solicitud ya persistida, verifica que siga procesable y publica ese identificador de forma idempotente en Vercel Queues.
- El servicio IA reclama trabajos y escribe estados o resultados sólo en estructuras designadas.
- El resultado registra identificador, intento, modelo, configuración, contrato e instante.
- Al finalizar explícitamente, backend valida y convierte una salida válida en rutina `PROPUESTA`; IA no escribe rutinas ni aprobaciones.
- El rol IA recibe privilegios mínimos y separados para Neon Test y Neon Producción.
- Cada deployment IA tiene una única conexión fija: Preview usa Test y Production usa Producción. El cliente nunca envía una URL de base ni un selector de ambiente.

Las solicitudes abandonadas, respuestas inválidas y fallos se eliminan a los 30 días. Los resultados aceptados conservan contexto mínimo y versiones según la política de auditoría.

El resultado público de IA usa `schema_version: "1.0"`, `routine_type`, `target_weekly_frequency` y `days`, con ejercicios y series en snake_case. El adaptador del backend valida ese contrato y lo traduce a los campos que consume su validador de dominio (`tipo_rutina`, `frecuencia_semanal`, `dias`); conserva compatibilidad con resultados históricos en español sin versión declarada. El catálogo y las reglas se revalidan antes de crear la propuesta. `suggested_load: null` conserva una carga sin especificar según RN-43; se persiste y se presenta como tal, distinta de cero (peso corporal). La versión creada por generación permanece con `current: false` hasta su aprobación.

Los elementos del catálogo permitido incluyen `primary_muscles` obtenidos de `app.exercise_muscles` con participación `PRIMARIA`. Las preferencias pueden incluir `muscle_counts_per_day: [{"muscle":"TRICEPS","count":3}]`. Backend extrae cantidades literales de pedidos como «3 ejercicios de tríceps por día» (también números escritos del uno al diez, acentos y «cada sesión»); conserva el texto original y valida disponibilidad antes del despacho. IA verifica en cada día la cantidad exacta de IDs distintos con ese músculo primario. Backend vuelve a comprobarlo con el catálogo real al finalizar; la participación secundaria y los IDs repetidos no cuentan como ejercicios distintos. Una salida que incumpla no crea ni reemplaza una propuesta. Un pedido imposible devuelve `422 generation_preferences_unsatisfiable` con `violations` explicativas.

Esta extracción acotada no implementa la interpretación completa ni la confirmación de RF-053: otras indicaciones siguen como texto al LLM y quedan sujetas a revisión del entrenador. No se cambia RN-39a ni la compatibilidad para satisfacer una preferencia.

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

Backend e IA pueden usar PostgreSQL local persistente para desarrollo independiente; IA conserva un rol restringido a integración. El ambiente integrado usa Neon Test. Las preferencias de generación incluyen opcionalmente `prescription_constraints`, calculadas por backend desde las mismas reglas que validan la rutina: rangos por propósito y grupos de patrones requeridos. Esto conserva compatibilidad con solicitudes anteriores. Nunca se copian datos personales reales al repositorio, fixtures o datasets de regresión. Las pruebas unitarias y de contrato usan datos sintéticos y PostgreSQL efímero en CI cuando necesitan modificar el esquema.

## Cambios

Para catálogos grandes, backend selecciona de manera determinista hasta 32 ejercicios antes de persistir la solicitud: reserva las cantidades pedidas por músculo, la cobertura mínima de patrones, variantes de los músculos mencionados en el texto y diversidad del resto. La disponibilidad se comprueba contra todo el catálogo compatible. `allowed_catalog` guarda completo el subconjunto seleccionado, con IDs reales, y es el único que recibe IA. Este límite protege el contexto configurado del modelo; no limita los ejercicios almacenados ni altera compatibilidad o aprobación.

Un cambio incompatible requiere:

1. nueva versión del contrato;
2. migración o vista preparada por backend;
3. compatibilidad temporal;
4. PR relacionados en backend e IA;
5. fixtures y tests de contrato actualizados;
6. despliegue por etapas antes de retirar la versión anterior.
