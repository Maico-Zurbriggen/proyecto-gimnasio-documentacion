# Base de datos compartida de desarrollo

## Estrategia

El desarrollo independiente usa PostgreSQL 17 local mediante `compose.local.yaml` del backend. El ambiente integrado del equipo conserva **Neon Test**; Producción usa otro proyecto o base, otras conexiones y otros roles. Ningún desarrollador recibe credenciales productivas.

Frontend no accede a PostgreSQL. Backend y servicio IA locales comparten `gym_local`; IA usa el rol `gym_ai_local`, restringido a solicitudes, intentos y resultados de integración.

### Base local independiente

1. Ejecutar `docker compose -f compose.local.yaml up -d --wait` desde backend. El puerto sólo se publica en `127.0.0.1:55432` y el volumen conserva los datos.
2. Usar `postgresql://gym_migrator@127.0.0.1:55432/gym_local?schema=public` en la configuración local del backend y aplicar `npm run db:deploy`.
3. Aplicar `prisma/local-ai-role.sql` y los seeds ficticios desde backend según su README.
4. IA usa `postgresql://gym_ai_local@127.0.0.1:55432/gym_local`, sin `schema`, junto con `APP_ENV=local` y `GENERATION_QUEUE_MODE=local`. Este ambiente rechaza bases remotas.

La autenticación sin contraseña del contenedor queda limitada al desarrollo local con datos ficticios. Los deployments conservan roles y credenciales propios.

### Puertos reservados por Windows

Si Docker no puede publicar `55432` y muestra `An attempt was made to access a socket in a way forbidden by its access permissions`, consultar `netsh interface ipv4 show excludedportrange protocol=tcp`. Elegir un puerto libre fuera de esos intervalos, por ejemplo `65432`, y configurar `LOCAL_DATABASE_PORT=65432` en `.env` del backend. Actualizar el puerto de `DATABASE_URL` tanto en backend como en `.env.local` de IA. Ejecutar nuevamente `docker compose -f compose.local.yaml up -d --wait` y reiniciar ambos servicios. Compose conserva el volumen existente; no se borran datos. El valor por defecto sigue siendo `55432`.

Backend y frontend activos no alcanzan para generar: el servicio de IA y su worker también deben permanecer activos. Desde `AI` en Windows, ejecutar `.\.venv-win\Scripts\python.exe dev_server.py`. Comprobar `/ready` del backend y `/ready` autenticado de IA antes de solicitar otra rutina; el segundo verifica la base local y el Polo.

### Regeneración para pruebas locales

El frontend de desarrollo ofrece **Regenerar**, que permite cambiar el prompt y crea otra clave de solicitud. Backend admite `regenerar: true` en `POST /students/:studentId/routine-generations` sólo con `LOCAL_GENERATION_TESTING=true`, `NODE_ENV=development` y `gym_local` en un host de loopback y el puerto indicado por `LOCAL_DATABASE_PORT` (por defecto `55432`). Los mismos permisos de alumno y propiedad siguen vigentes.

La solicitud captura el identificador de la propuesta actual en `preferences.local_test_regeneration.replaces_proposed_routine_id`; este dato de control no se envía al LLM. Al finalizar una salida válida, backend bloquea la fila del alumno, descarta únicamente esa propuesta con auditoría y crea la nueva `PROPUESTA` en la misma transacción. Si la generación o validación falla, la propuesta anterior se conserva. Una propuesta distinta aparecida mientras se genera no se descarta. La rutina vigente y la aprobación del entrenador conservan su ciclo normal.

Esta capacidad de prueba no implementa el candidato ajustable ni su límite de regeneraciones: esas funcionalidades mantienen el alcance definido en RF-119 y RN-127.

## Configuración de la base compartida

```bash
npm ci
cp .env.example .env
npm run db:generate
npm run db:status
npm run dev
```

En PowerShell, usar `Copy-Item .env.example .env`. La persona responsable entrega la conexión Neon Test por un canal seguro; nunca se copia una credencial real en `.env.example`, GitHub, issues o documentación.

## Reglas sobre la base compartida

- No ejecutar `prisma migrate reset`, `prisma db push` ni seeds destructivos.
- No ejecutar migraciones automáticamente al iniciar la aplicación.
- Cada prueba o desarrollador identifica sus datos y elimina sólo lo que creó.
- Las pruebas destructivas o de integración compartida se serializan.
- Los tests unitarios no dependen de Neon.
- CI aplica migraciones una sola vez por ambiente mediante `prisma migrate deploy` y un rol `migrator` separado.

## Crear migraciones · decisión I-07 resuelta

`prisma migrate dev` no se ejecuta contra Neon Test compartida. El autor de una migración usa exclusivamente PostgreSQL 17 efímero mediante `compose.migrations.yaml` del backend. El contenedor usa `tmpfs`, no conserva datos y no levanta la aplicación.

Flujo del autor:

1. Partir de `develop` actualizado y levantar el contenedor con `docker compose -f compose.migrations.yaml up -d --wait`.
2. Definir temporalmente `DATABASE_URL=postgresql://gym_migrator@localhost:55432/gym_migrations?schema=public` en esa terminal. El contenedor acepta conexiones sin contraseña únicamente porque es efímero y publica el puerto sólo sobre `127.0.0.1`.
3. Modificar `schema.prisma` y ejecutar `npm run db:migrate -- --name <nombre_descriptivo>`.
4. Revisar el SQL generado, ejecutar `npm run db:status` y `npm run check`.
5. Destruir y recrear el contenedor, y ejecutar `npm run db:deploy` para verificar todo el historial desde una base vacía.
6. Detener el contenedor y restaurar la variable de entorno anterior.

El PR incluye `schema.prisma`, el directorio nuevo de `prisma/migrations`, pruebas y una explicación de compatibilidad. Nunca se edita una migración ya integrada. `compose.local.yaml` y `compose.migrations.yaml` usan el mismo puerto: detener el contenedor local antes de crear una migración y volver a iniciarlo al terminar, conservando su volumen.

CI también aplica el historial completo sobre PostgreSQL 17 limpio dentro del check `quality`. No usa secretos ni Neon para esta validación.

## Promoción

- Merge a `test`: CI ejecuta `npm run db:deploy` contra Neon Test antes del despliegue compatible.
- Merge a `main`: CI ejecuta el mismo comando contra Neon Producción con aprobación del dueño.
- Los cambios incompatibles usan expansión, migración de consumidores y contracción posterior para permitir rollback.

Los environments de GitHub `test` y `Production` contienen un secret homónimo `MIGRATION_DATABASE_URL`, con URL directa y rol migrador propio de cada ambiente. Estas credenciales no se guardan en Vercel ni se entregan a desarrolladores. El workflow las expone a Prisma como `DATABASE_URL` sólo durante el job.

## Catálogo de prueba local

El catálogo de prueba puede ampliarse con `npm run db:seed:local-generation-catalog` en backend. El dataset versionado contiene 132 ejercicios y variantes para los 17 grupos musculares, con instrucciones originales en español, nivel, equipamiento, articulaciones y participación muscular primaria y secundaria. El script evita duplicados al normalizar nombres y acentos; inserta únicamente los ejercicios faltantes y comprueba dentro de la misma transacción al menos cinco ejercicios primarios por grupo. Conserva ejercicios, rutinas e historiales existentes. Está restringido a `gym_local` en loopback y el puerto local configurado; usa el gimnasio y entrenador ficticios existentes.

La carga no modifica el perfil del alumno ni el inventario. La elegibilidad sigue dependiendo de las reglas de compatibilidad. Se usaron las bibliotecas de [ACE](https://www.acefitness.org/resources/everyone/exercise-library/) y [NASM](https://www.nasm.org/resource-center/exercise-library) como referencias de movimientos; la clasificación en la taxonomía propia y la dificultad son metadatos de desarrollo que requieren revisión de un entrenador antes de importarse en un catálogo real.

## Aplicación manual excepcional desde pgAdmin

La migración `20260928190000_student_measurement_blocking` se entrega como SQL revisable porque el responsable de la base decidió aplicarla desde pgAdmin. Este procedimiento no reemplaza el flujo normal de CI:

1. Conectarse mediante la URL directa de Neon y el rol propietario `migrator_test` o `migrator_prod`; no usar el pooler ni el rol runtime.
2. Verificar que Prisma no tenga una migración ejecutándose y que no exista un advisory lock pendiente.
3. Ejecutar completo `prisma/migrations/20260928190000_student_measurement_blocking/migration.sql`. El archivo abre y confirma una única transacción; ante un error no queda una migración parcial.
4. Verificar columna, enums, tablas, índices, triggers y permisos antes de marcarla.
5. Configurar temporalmente `DATABASE_URL` con la misma conexión directa del migrador y ejecutar:

   ```bash
   npx prisma migrate resolve --applied "20260928190000_student_measurement_blocking"
   npx prisma migrate status
   ```

Sin `migrate resolve`, el siguiente `prisma migrate deploy` intentaría ejecutar de nuevo el SQL y fallaría porque los objetos ya existen. Marcarla como aplicada antes de ejecutarla también es incorrecto: Prisma dejaría de crear objetos que todavía faltan.
