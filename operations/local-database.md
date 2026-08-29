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

## Crear migraciones · punto abierto I-07

`prisma migrate dev` no debe ejecutarse contra Neon Test compartida. Antes de la primera modificación de esquema se debe elegir una alternativa:

1. PostgreSQL efímero local, usado sólo por quien crea la migración; o
2. una base shadow separada dentro del recurso Neon Test.

La elección no cambia la base utilizada por la aplicación local. El PR incluye `schema.prisma`, SQL generado y pruebas. Nunca se edita una migración ya integrada.

## Promoción

- Merge a `test`: CI ejecuta `npm run db:deploy` contra Neon Test antes del despliegue compatible.
- Merge a `main`: CI ejecuta el mismo comando contra Neon Producción con aprobación del dueño.
- Los cambios incompatibles usan expansión, migración de consumidores y contracción posterior para permitir rollback.
