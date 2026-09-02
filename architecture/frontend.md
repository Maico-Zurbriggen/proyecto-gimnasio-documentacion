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
2. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
3. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
4. La indisponibilidad de IA deshabilita la generación, no el resto del producto. ✎ Lo que permanece es la creación y asignación manual de plantillas por el entrenador (RF-019); los presets, sólo si se implementa RF-021 ([DD-35](../decisions/design-decisions.md)).
5. Ninguna lógica de autorización o compatibilidad se confía sólo al cliente.
