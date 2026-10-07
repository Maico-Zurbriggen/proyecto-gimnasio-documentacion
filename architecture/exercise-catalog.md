# Catálogo RepDB y disponibilidad por gimnasio

**Estado:** implementación local en backend, frontend e IA, 2026-10-07; publicación del catálogo real y despliegue pendientes. [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md).

El vocabulario, las entidades, los permisos y las reglas viven en [D2](../product/glossary.md), [D4](../domain/domain-model.md), [D3](../domain/actors-roles-permissions.md) y [D5](../domain/business-rules.md). Este documento define la importación y el recorrido operativo.

## 1. Importar el catálogo principal

La fuente inicial es [RepDB Free](https://github.com/RepDB/exercise-dataset): JSON en español e ilustraciones estáticas. La carga se ejecuta como operación del proveedor del sistema; ningún usuario modifica las fichas del catálogo base.

1. Descargar una versión identificable del JSON y sus imágenes; conservar revisión o hash del paquete y licencia. La app consulta nuestra DB y almacenamiento, sin depender de RepDB en cada petición.
2. Validar el paquete completo en un área privada de preparación antes de publicarlo. Mapear dificultad, equipamiento y músculos al glosario; conservar todos los músculos primarios y secundarios, sin elegir uno arbitrariamente.
3. Usar un UUID interno estable y la clave única `(source, source_id)` para repetir la carga sin duplicados. Un cambio de nombre no cambia el UUID. Ejercicios propios y fixtures existentes conservan sus referencias; coincidencias entre fuentes requieren revisión, no fusión por nombre.
4. Conservar nombres, instrucciones y consejos en español, unilateralidad y metadatos útiles. RepDB no aporta directamente nuestra clasificación de articulaciones y patrones: completar y revisar esos datos, así como equipamiento auxiliar omitido. Un valor desconocido queda pendiente; no se rellena con un supuesto.
5. Publicar únicamente fichas completas y revisadas. Un fallo mantiene la versión anterior disponible; el informe cuenta altas, cambios y pendientes. Reimportar no habilita ejercicios en ningún gimnasio ni reactiva fichas retiradas. Cambios materiales requieren revisión antes de reemplazar la ficha publicada; una ausencia en la nueva fuente no borra el ejercicio.

Las ilustraciones se almacenan con rutas propias versionadas. Se admiten las poses de inicio/final o una sola imagen; compartir imagen no convierte dos ejercicios en uno. La ficha mantiene un recurso visual principal y sus recursos adicionales. Las ilustraciones generadas con IA necesitan revisión de postura; las etiquetas de la fuente, como `knee_safe`, no son garantías de compatibilidad.

La [licencia de datos](https://github.com/RepDB/exercise-dataset/blob/main/LICENSE-DATA.md) permite uso dentro de la aplicación con el crédito visible «Exercise data by RepDB (repdb.co)». No publicar el dataset, sus derivados o imágenes en nuestros repositorios ni ofrecer una API de redistribución. Los endpoints autenticados sirven al producto. Las animaciones de muestra pagas quedan fuera de la importación y las imágenes no se envían al LLM ni se usan para derivación generativa.

## 2. Habilitar ejercicios en un gimnasio

El administrador consulta el catálogo base y los ejercicios propios aprobados de su gimnasio, busca por atributos y habilita o deshabilita los que realmente ofrece. Puede editar varias habilitaciones en una operación atómica e idempotente. El gimnasio se obtiene de la sesión, no de un identificador elegible por el cliente.

La habilitación referencia la ficha original. No cambia su propietario ni copia instrucciones, músculos o imágenes. Aprobar un ejercicio propio permite habilitarlo, pero no lo habilita automáticamente. El administrador puede aprobar y habilitar en la misma operación. Alumnos y entrenadores consultan la disponibilidad; sólo el administrador la modifica, y el entrenador sigue creando ejercicios propios.

Un gimnasio nuevo empieza sin ejercicios habilitados. Tampoco se habilitan automáticamente los de peso corporal. Si su catálogo está vacío, la solicitud de generación explica que el administrador debe configurarlo y no consume una llamada al LLM. Una baja local afecta únicamente a ese gimnasio; una desactivación global impide nuevas incorporaciones en todos.

El inventario continúa describiendo equipamiento real y se entrega como contexto. Al cambiarlo, se muestran al administrador las habilitaciones relacionadas para que las revise. El cambio no habilita ni deshabilita ejercicios automáticamente ni reconstruye el catálogo por intersección con equipamiento.

## 3. Generar con la lista completa del gimnasio

```text
RepDB → importación y revisión → catálogo base
                                      ↓ habilitación del administrador
                               catálogo del gimnasio
                                      ↓ + contexto del alumno
                           solicitud persistida → IA → PROPUESTA
```

Backend autoriza la solicitud y toma una instantánea de todos los ejercicios aprobados y habilitados del gimnasio, incluidos los propios. Persiste esa lista completa y el contexto conforme a [data-interface.md](data-interface.md); IA recibe sólo el UUID de la solicitud. No elimina candidatos por nivel, condiciones, objetivo, músculo o patrón, ni limita la lista a 32.

La IA interpreta el pedido, evalúa la adecuación al alumno, selecciona ejercicios y decide días, series, repeticiones, descansos y justificación. Backend comprueba formato, referencias, pertenencia al catálogo enviado y disponibilidad vigente; no calcula compatibilidad ni corrige o rechaza la prescripción mediante tablas de entrenamiento. La propuesta requiere revisión del entrenador.

El catálogo se serializa compacto, sin imágenes ni URLs de media. Los índices se usan también en las referencias del historial; las referencias históricas fuera del catálogo se señalan como tales. Son operaciones de transporte, no selección. El conector usa una cota conservadora de bytes UTF-8 para entrada, prompt, schema y template, más reserva de respuesta; no es un conteo exacto del tokenizer. Comprueba capacidad declarada del modelo, ventana efectivamente asignada por Ollama y fin explícito del stream. Si no cabe, declara generación no disponible sin truncar ni introducir filtros. Una estrategia adicional requiere una decisión posterior.

## 4. Cambios durante y después de la generación

- Si un ejercicio elegido se deshabilita o desactiva mientras IA procesa, el resultado no crea una propuesta. Se conserva el motivo técnico y se permite una nueva solicitud con una instantánea nueva; no se sustituye el ejercicio en código.
- Si cambia un dato del alumno o del inventario utilizado en el contexto, el resultado queda desactualizado. Tampoco se finaliza con el contexto anterior. La comprobación compara versiones o hashes de datos, no decide entrenamiento.
- Una habilitación nueva no invalida por sí sola un resultado cuyos ejercicios siguen disponibles. Las actualizaciones materiales de fichas utilizadas sí requieren renovar el contexto.
- Antes de aprobar o incorporar ejercicios a una nueva versión se comprueba la disponibilidad actual. Deshabilitar no borra rutinas, plantillas, fichas ni sesiones: señala las referencias afectadas para revisión del entrenador, conservando la prescripción congelada de sesiones iniciadas. Reactivar no cambia versiones ni cierra advertencias de entrenamiento automáticamente.

Las fichas, habilitaciones e inventario tienen revisiones crecientes. Las escrituras reciben la revisión leída; una escritura obsoleta devuelve `409`, y repetir el mismo estado es idempotente. La aprobación de una rutina exige el `reviewToken` recibido al leerla, ligado al perfil, versión y ejercicios. La finalización bloquea gimnasio, alumno y fichas seleccionadas; reintenta únicamente conflictos de serialización, sin regenerar ni modificar decisiones de entrenamiento.

## 5. Entrega y verificación

Hay cuatro migraciones nuevas: catálogo/habilitaciones/media, revisiones optimistas, retirada de restricciones SQL de entrenamiento y carga prescripta nullable en la copia de sesión. No modifican migraciones anteriores ni habilitan automáticamente fichas existentes. La API del catálogo publica `openapi/catalog.openapi.json`; frontend regenera su cliente con `npm run catalog:generate`. El contrato de generación es `2.0`; se conserva lectura de solicitudes anteriores `1.0` durante la transición.

CI ejecuta también las pruebas de persistencia e importación con PostgreSQL 17 temporal. Para reproducirlas, aplicar las migraciones a `gym_catalog_test` en `127.0.0.1:55434`, definir `CATALOG_TEST_DATABASE_URL` y ejecutar `npm test -- --no-file-parallelism test/database`. La comprobación de destino rechaza bases compartidas; los datos de prueba son sintéticos.

Comprobar carga repetida sin duplicados, paquete inválido sin publicación parcial, mapeos pendientes, múltiples músculos primarios, recursos visuales y atribución; aislamiento y permisos entre gimnasios; habilitación repetida y baja sin pérdida de historial; lista completa enviada, resultado fuera de la instantánea, cambios concurrentes y presupuesto de tokens. La calidad de las decisiones de entrenamiento se evalúa con casos revisados por un entrenador, no se garantiza por la validación técnica.

## 6. Preparación y publicación

Desde backend, con las migraciones aplicadas a la base elegida:

```bash
npm run catalog:import -- download
npm run catalog:import -- publish <ruta-privada-del-review.json>
```

`download` guarda JSON, licencia, procedencia, hash, imágenes y `review.json` en `.catalog-private/`, excluido de Git. Completar allí únicamente las fichas revisadas: patrón, dificultad, músculos, articulaciones, equipamiento, revisor y fecha. `publish` valida el manifiesto contra el hash descargado y publica las entradas `reviewed: true` en una transacción; genera un informe privado. Los hashes materiales se calculan por ficha para que un cambio ajeno no invalide todas las revisiones. No marcar como revisada una clasificación inferida sin revisión profesional.

La descarga verificada contiene 609 ejercicios y 1.056 imágenes referenciadas disponibles. El ZIP publicado por el proveedor no coincide con el JSON: faltan 26 rutas que afectan a 14 fichas. `missing-media.json` las identifica; esas fichas no pueden publicarse mientras falten sus recursos. La preparación no equivale a catálogo aprobado: aún resta la curación de los atributos que RepDB no aporta.

En local, `CATALOG_ASSETS_DIR` apunta al almacenamiento privado de imágenes; el endpoint autenticado `/catalog/media/:revision/:filename` sirve sólo recursos publicados. En Vercel hace falta almacenamiento persistente propio: subir las mismas imágenes versionadas y definir `CATALOG_MEDIA_BASE_URL` HTTPS antes de publicar. El importador no realiza ese despliegue ni crea un CDN.

IA configura `LLM_CONTEXT_TOKENS` y `LLM_RESPONSE_TOKENS` según el modelo y hardware. Los valores iniciales son 32.768 y 4.096; no garantizan que entre el catálogo de cualquier gimnasio. El proxy debe permitir `/api/show`, `/api/tags`, `/api/chat` y `/api/ps`. Se conserva el digest del modelo y una firma del prompt, schema y parámetros. Para promoción siguen vigentes los checks y la evaluación del entrenador de [integración generativa](generative-ai-integration.md).

Verificación local: 412 pruebas de backend con PostgreSQL aislado, 129 de frontend y 45 de IA; formato, lint, tipos y build. Una llamada real con perfil y catálogo sintéticos produjo salida `2.0` válida. El navegador verificó habilitación, aprobación explícita, consulta por alumno y ficha accesible por teclado a 360 px y escritorio. Esto valida el recorrido técnico; no sustituye curación del dataset ni evaluación profesional de prescripciones.
