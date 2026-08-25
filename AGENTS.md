# Instrucciones del repositorio documental

## Propósito

Este repositorio es la única fuente de verdad documental del Proyecto Gimnasio. Los repositorios de frontend, backend e IA conservan solamente su `README.md` y su `AGENTS.md`; cualquier definición compartida o que afecte a más de un componente se mantiene aquí.

## Inicio obligatorio para agentes

1. Leer `manifest.json`.
2. Identificar el tipo de tarea y cargar sólo los documentos indicados por `load_when`.
3. Para cualquier cambio de dominio, leer primero `product/glossary.md` y respetar sus términos y enumeraciones cerradas.
4. Para implementar una funcionalidad, combinar como mínimo su flujo, reglas de negocio, estados, casos borde y requisitos trazados.
5. Leer también el `AGENTS.md` del repositorio de código que se modificará; sus reglas locales complementan esta documentación.

No inferir una regla ausente. Si la documentación no alcanza o se contradice, registrar el punto abierto en `planning/risks-and-assumptions.md` y resolverlo antes de codificar.

## Autoridad por tema

- Vocabulario y enumeraciones: `product/glossary.md`.
- Entidades y restricciones de integridad: `domain/domain-model.md`.
- Reglas, constantes y cálculos: `domain/business-rules.md`.
- Estados y transiciones: `domain/lifecycles-and-states.md`.
- Alcance funcional y prioridad: `requirements/functional-requirements.md`.
- Calidad y verificabilidad: `requirements/non-functional-requirements.md`.
- Topología y fronteras técnicas: `architecture/` y los ADR vigentes.
- Forma de trabajo y permisos: `delivery/`.

Cuando dos documentos parezcan incompatibles, no elegir silenciosamente: verificar sus identificadores, el estado del ADR y la trazabilidad, y documentar la resolución.

## Reglas de mantenimiento

- Una definición tiene un único documento canónico. En los demás lugares se enlaza; no se copia ni se resume como una segunda fuente normativa.
- Conservar los identificadores estables `RN-*`, `RF-*`, `RNF-*`, `RA-*`, `RI-*`, `CB-*`, `DD-*`, `PD-*` y `S-*`.
- Un cambio de regla debe actualizar en el mismo PR los requisitos, flujos, casos borde, decisiones y trazabilidad afectados.
- Un cambio de frontera entre repositorios debe incluir un ADR y PR relacionados en los repositorios de código afectados.
- Registrar todo documento nuevo en `manifest.json`, con alcance, autoridad y condiciones de carga.
- Usar enlaces relativos dentro de este repositorio y enlaces permanentes de GitHub hacia repositorios externos.
- No guardar código de aplicación, secretos, datos personales, datasets, modelos ni artefactos generados.

## Repositorios del sistema

- Frontend: `Maico-Zurbriggen/proyecto-gimnasio`.
- Backend: `Maico-Zurbriggen/proyecto-gimnasio-back`.
- Motor analítico: `Maico-Zurbriggen/proyecto-gimnasio-ia`.

## Verificación

Ejecutar antes de cerrar un cambio:

```bash
python tools/check_docs.py
```

La verificación controla el manifiesto, documentos huérfanos, contenido duplicado y enlaces relativos.
