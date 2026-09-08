# Arquitectura general del sistema

## Topología

```text
proyecto-gimnasio (React SPA / Vercel)
              |
              | REST/JSON + cookie httpOnly
              v
proyecto-gimnasio-back (Express / Vercel) ------> Neon PostgreSQL
              |                                      ^
              | HTTPS                                |
              v                                      |
        ngrok estable                                |
              |                                      |
              v                                      |
proyecto-gimnasio-ia (API + worker Python / Polo) ---+
              |
              | API privada/local
              v
           LLM / Polo
```

Los trabajos analíticos y predictivos futuros comparten el repositorio IA, pero son procesos batch separados del servicio generativo online. La documentación común vive en `proyecto-gimnasio-documentacion`; los cuatro repositorios se versionan de manera independiente y no comparten código fuente.

## Propiedad de contratos

- Backend es dueño del OpenAPI público, del esquema transaccional, de las estructuras de integración y de las migraciones.
- Frontend genera tipos y cliente desde una versión explícita del OpenAPI del backend.
- IA es dueña del OpenAPI de su servicio de orquestación; backend genera o valida el cliente desde una versión explícita.
- El conector IA–LLM es privado del repositorio IA.
- Los jobs batch usan datasets versionados mediante vistas o snapshots descritos en [data-interface.md](data-interface.md).
- Un cambio incompatible conserva compatibilidad temporal y coordina PR relacionados.

## Invariantes transversales

1. El historial ejecutado y las versiones congeladas nunca se reescriben.
2. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
3. PostgreSQL es la fuente de verdad transaccional; el LLM no accede a ella.
4. Toda salida inteligente registra versión, instante y contexto mínimo reproducible.
5. Backend mantiene autorización y validaciones de negocio; IA sólo persiste estados y resultados en estructuras designadas.
6. La indisponibilidad generativa no produce una rutina insegura ni degrada el resto del sistema: se deshabilita esa capacidad temporalmente y permanecen las operaciones manuales. Presets y plantillas quedan unificados bajo alcance opcional `COULD` diferido (ver [D11/DD-35](../decisions/design-decisions.md)).
7. Test y producción no comparten base ni credenciales, aunque inicialmente compartan API y configuración del modelo.

## Detalle por componente

- [Frontend](frontend.md)
- [Backend](backend.md)
- [Servicio IA y analítica](analytics-engine.md)
- [Interfaz de datos backend–IA](data-interface.md)
- [Integración generativa](generative-ai-integration.md)
