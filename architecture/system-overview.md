# Arquitectura general del sistema

## Topología

```text
proyecto-gimnasio (React SPA)
              |
              | REST/JSON + cookie httpOnly
              v
proyecto-gimnasio-back (Express + TypeScript)
              |
              v
         PostgreSQL
              ^
              | vistas o snapshots versionados
              |
proyecto-gimnasio-ia (Python batch)
```

La documentación común vive en `proyecto-gimnasio-documentacion`. Los cuatro repositorios se versionan de manera independiente y no comparten código fuente.

## Propiedad de contratos

- El backend es dueño de OpenAPI, del esquema transaccional y de las migraciones.
- El frontend consume una versión explícita de OpenAPI y genera desde ella tipos y cliente HTTP.
- Backend e IA acuerdan datasets versionados mediante vistas o snapshots; la interfaz canónica está en [data-interface.md](data-interface.md).
- IA escribe solamente resultados precalculados designados. No modifica fuentes transaccionales ni expone HTTP.
- Un cambio incompatible requiere actualizar primero esta documentación y coordinar PR relacionados.

## Invariantes transversales

1. El historial ejecutado y las versiones congeladas nunca se reescriben.
2. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
3. PostgreSQL es la fuente de verdad transaccional; indicadores derivados no se convierten en entradas editables.
4. Toda salida analítica registra versión, instante y contexto reproducible.
5. Una capacidad inteligente o externa tiene fallback determinístico y su fallo no se transforma en un 5xx cuando el camino base puede continuar.

## Detalle por componente

- [Frontend](frontend.md)
- [Backend](backend.md)
- [Motor analítico](analytics-engine.md)
- [Interfaz de datos backend–IA](data-interface.md)
