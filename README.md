# Proyecto Gimnasio — Documentación

Fuente única de verdad funcional, técnica y operativa de la plataforma de entrenamiento asistido.

## Entrada rápida

- Agentes de IA: leer primero [AGENTS.md](AGENTS.md) y después [manifest.json](manifest.json).
- Personas que conocen por primera vez el proyecto: comenzar por [la guía del corpus](corpus-guide.md).
- Arquitectura general: [architecture/system-overview.md](architecture/system-overview.md).
- Implementación de una funcionalidad: consultar el conjunto indicado por `load_when` en el manifiesto, no un documento aislado.

## Organización

```text
product/       visión y lenguaje normativo
domain/        permisos, entidades, reglas, estados y casos borde
flows/         recorridos funcionales completos
requirements/ alcance, calidad y trazabilidad
architecture/ sistema y fronteras entre repositorios
decisions/     decisiones de diseño y ADR
planning/      supuestos, riesgos y capacidad
operations/    desarrollo y operación local
delivery/      GitHub, ramas, revisiones y permisos
tools/         validación automática del corpus
```

No se mantienen copias del corpus en los repositorios de código. Sus `README.md` y `AGENTS.md` enlazan esta fuente canónica.

## Validación

```bash
python tools/check_docs.py
```
