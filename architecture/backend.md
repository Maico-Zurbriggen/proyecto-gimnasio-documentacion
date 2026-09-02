# Arquitectura del backend

## Distribución

```text
React SPA -> Express + TypeScript -> Neon PostgreSQL
                 |
                 | HTTPS / OpenAPI IA
                 v
             ngrok -> API Python / Polo
```

El backend es un monolito modular desplegado en Vercel y dueño del OpenAPI público, las invariantes transaccionales, la autorización, Prisma y las migraciones.

## Responsabilidad

Los módulos previstos son identidad, catálogo, rutinas, entrenamiento, métricas, seguimiento, administración e integración IA. Se crean al implementar historias verticales. Los routers sólo traducen HTTP; reglas y autorización viven en servicios o funciones de dominio y Prisma queda detrás de adaptadores de persistencia.

## Fronteras

- OpenAPI del backend es la fuente de verdad para frontend.
- Prisma no se expone como contrato HTTP.
- PostgreSQL es la única fuente de verdad transaccional.
- Backend autoriza, minimiza el contexto y crea solicitudes idempotentes antes de invocar IA.
- El cliente del servicio IA se genera o valida desde el OpenAPI versionado por ese repositorio.
- El backend nunca espera al LLM: la API IA acepta con `202` y frontend consulta estado al backend.
- IA puede escribir sólo estados y resultados en estructuras de integración; backend es el único que crea entidades de dominio.
- Entrenamiento y scoring predictivo siguen fuera del camino de las peticiones.

## Fallos y seguridad

- Cada intento generativo vence inicialmente a los 120 segundos y admite un único reintento.
- Una salida inválida nunca se presenta. Tras el segundo fallo la capacidad queda no disponible; no existe fallback determinístico de generación.
- El resto del sistema continúa y las plantillas y operaciones manuales permanecen disponibles.
- Credenciales y conexiones test/producción son distintas; ninguna URL de base se recibe desde una petición.
- El Polo recibe sólo contexto necesario y un identificador técnico, nunca credenciales ni identificadores personales innecesarios.

## Invariantes

1. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
2. Al comenzar una sesión se congela lo prescripto junto a lo realmente ejecutado.
3. Historial e indicadores derivados no son fuentes de verdad editables.
4. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
5. La autorización combina rol y propiedad o asignación del recurso.
6. Ningún resultado IA evita las validaciones de catálogo, compatibilidad, rangos y permisos.
