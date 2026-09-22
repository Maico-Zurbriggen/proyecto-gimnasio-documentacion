# Arquitectura del frontend

## Distribución

```text
proyecto-gimnasio (React SPA)
              |
              | REST/JSON + cookie httpOnly
              v
proyecto-gimnasio-back (Express)
              |
              +----> Neon PostgreSQL
              |
              +----> servicio IA Python -> LLM del Polo
```

## Contratos

- Backend es dueño de su OpenAPI y de toda estructura persistida.
- Frontend genera tipos y cliente desde una versión explícita de ese OpenAPI; no comparte código con backend.
- La identidad se obtiene de `POST /auth/login` y `GET /auth/me`; todas las consultas usan `credentials: include`. Frontend no envía identificadores ni roles simulados.
- Frontend no consume el OpenAPI de IA ni conoce Cloudflare Tunnel, el LLM o PostgreSQL.
- Los cambios incompatibles se coordinan mediante versionado y PR relacionados.

## Responsabilidad

- Presentación, accesibilidad y estado de interacción.
- Estado remoto mediante TanStack Query.
- Polling de una generación asíncrona sólo contra backend, detenido en un estado terminal.
- La generación se solicita exclusivamente desde el área del alumno y para el `studentId` de su sesión; las áreas de entrenador y administrador no presentan esa acción.
- Finalización explícita contra backend cuando la generación queda `COMPLETADA`; la consulta de estado nunca materializa una rutina por sí sola.
- Conservación local del identificador de una generación activa y del borrador de sesión cuando corresponda.
- Estados de carga, reintento e indisponibilidad. ✎ No se ofrece un preset como salida alternativa: RF-021 es alcance opcional. Ante indisponibilidad generativa el alumno ve el estado, no una acción que puede no existir.
- Validaciones de experiencia de usuario que la API vuelve a comprobar.
- Guardas y navegación por los roles de la sesión: un área sólo se muestra si el backend devolvió su rol; los usuarios multirrol pueden alternar únicamente entre sus áreas concedidas.

## Invariantes

1. El frontend nunca accede directamente a PostgreSQL, Prisma, IA, Cloudflare Tunnel ni proveedores externos.
2. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
3. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
4. La indisponibilidad de IA deshabilita la generación, no el resto del producto. ✎ Lo que permanece es la creación y asignación manual de plantillas por el entrenador (RF-019); los presets, sólo si se implementa RF-021 ([DD-35](../decisions/design-decisions.md)).
5. Ninguna lógica de autorización o compatibilidad se confía sólo al cliente.
6. El frontend no guarda tokens ni determina roles: la cookie es `httpOnly` y backend vuelve a autorizar cada petición.
