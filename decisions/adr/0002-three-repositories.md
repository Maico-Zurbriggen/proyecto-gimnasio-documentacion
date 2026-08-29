# ADR 0002: separación en tres repositorios

- Estado: aceptada, parcialmente reemplazada por ADR 0003 y ADR 0004
- Fecha: 2026-08-24

## Contexto

El equipo decidió asignar frontend, backend y análisis/IA a repositorios independientes. La frontera de despliegue y la responsabilidad de cada grupo pesan más que la navegación conjunta del monorepo.

## Decisión

Mantener tres repositorios:

- `proyecto-gimnasio`: SPA React;
- `proyecto-gimnasio-back`: API Express, Prisma y PostgreSQL;
- `proyecto-gimnasio-ia`: servicio generativo online y procesos batch Python.

El backend publica OpenAPI para frontend. IA publica OpenAPI para su servicio de orquestación; backend genera o valida su cliente desde una versión explícita. La analítica batch se integra por estructuras persistidas o snapshots acordados. Nunca hay imports entre repositorios.

El corpus funcional y técnico vive exclusivamente en `proyecto-gimnasio-documentacion` según ADR 0003. Los repositorios de código conservan sólo README y AGENTS locales y enlazan la fuente canónica.

## Consecuencias

- Cada repositorio instala, prueba, versiona y despliega de manera autónoma.
- Se eliminan workspaces y dependencias por ruta local.
- Los cambios transversales requieren coordinación y PR relacionados.
- La documentación compartida no se copia; cada cambio indica los repositorios afectados.
- ADR 0004 agrega un servicio generativo online al repositorio IA sin alterar la frontera de los jobs batch.
