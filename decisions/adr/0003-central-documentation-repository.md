# ADR 0003: repositorio documental central

- Estado: aceptada
- Fecha: 2026-08-25
- Reemplaza la distribución documental definida implícitamente por ADR 0002.

## Contexto

El corpus funcional y las guías de entrega estaban copiados en frontend, backend e IA. Aunque las copias nacieron idénticas, cada cambio exigía tres PR y podía producir versiones incompatibles para personas y agentes.

## Decisión

Mantener toda documentación compartida y específica del sistema en `proyecto-gimnasio-documentacion`, sin duplicados entre repositorios. Cada repositorio de código conserva solamente:

- `README.md`, como entrada operativa y enlace a la fuente canónica;
- `AGENTS.md`, con instrucciones locales y la ruta de lectura del corpus central.

El repositorio documental publica `manifest.json` como mapa determinista para agentes. Toda pieza canónica tiene un identificador, una ruta única, un alcance y condiciones explícitas de carga.

## Consecuencias

- Un cambio documental se revisa y versiona una sola vez.
- Los cambios de código y documentación que dependan entre sí usan PR relacionados.
- Trabajar sin acceso al repositorio documental no autoriza a reconstruir reglas por memoria ni a copiar documentos al repositorio de código.
- La validación automática rechaza enlaces rotos, documentos no registrados y contenido Markdown duplicado.
