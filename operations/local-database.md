# Base de datos compartida de desarrollo

## Estrategia

El trabajo local ordinario usa **Neon Test**, compartida por el equipo. Producción usa otro proyecto o base, otras conexiones y otros roles. Ningún desarrollador recibe credenciales productivas.

Frontend no accede a PostgreSQL. Backend local usa un rol personal o de aplicación test; el servicio IA usa un rol restringido a estructuras de integración.

## Primera configuración

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

El PR incluye `schema.prisma`, el directorio nuevo de `prisma/migrations`, pruebas y una explicación de compatibilidad. Nunca se edita una migración ya integrada. La aplicación local continúa usando Neon Test con el rol runtime y no usa Docker salvo al crear migraciones.

CI también aplica el historial completo sobre PostgreSQL 17 limpio dentro del check `quality`. No usa secretos ni Neon para esta validación.

## Promoción

- Merge a `test`: CI ejecuta `npm run db:deploy` contra Neon Test antes del despliegue compatible.
- Merge a `main`: CI ejecuta el mismo comando contra Neon Producción con aprobación del dueño.
- Los cambios incompatibles usan expansión, migración de consumidores y contracción posterior para permitir rollback.

Los environments de GitHub `test` y `Production` contienen un secret homónimo `MIGRATION_DATABASE_URL`, con URL directa y rol migrador propio de cada ambiente. Estas credenciales no se guardan en Vercel ni se entregan a desarrolladores. El workflow las expone a Prisma como `DATABASE_URL` sólo durante el job.
