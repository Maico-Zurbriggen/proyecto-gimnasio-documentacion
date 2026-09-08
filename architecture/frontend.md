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
- Frontend no consume el OpenAPI de IA ni conoce ngrok, el LLM o PostgreSQL.
- Los cambios incompatibles se coordinan mediante versionado y PR relacionados.

## Responsabilidad

- Presentación, accesibilidad y estado de interacción.
- Estado remoto mediante TanStack Query.
- Polling de una generación asíncrona sólo contra backend, detenido en un estado terminal.
- Conservación local del identificador de una generación activa y del borrador de sesión cuando corresponda.
- Estados de carga, reintento e indisponibilidad. ✎ No se ofrece un preset como salida alternativa: RF-021 es alcance opcional. Ante indisponibilidad generativa el alumno ve el estado, no una acción que puede no existir.
- Validaciones de experiencia de usuario que la API vuelve a comprobar.

## Invariantes

1. El frontend nunca accede directamente a PostgreSQL, Prisma, IA, ngrok ni proveedores externos.
2. Una rutina asignada es independiente de su origen; cambios posteriores no reescriben versiones existentes.
3. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
4. La indisponibilidad de IA deshabilita la generación, no el resto del producto. Presets y plantillas son alcance opcional `COULD` diferido ([DD-35](../decisions/design-decisions.md)).
5. Ninguna lógica de autorización o compatibilidad se confía sólo al cliente.
