# Documentación Maestra — Proyecto Gimnasio (Vivaz Adaptive)

> **Qué es este archivo.** La compilación completa y literal de toda la documentación del proyecto:
> el corpus del repositorio documental, más los `README.md` y `AGENTS.md` de los tres repositorios de
> código, más los anexos de configuración de entrega. Reúne **60 archivos** en un solo
> documento para leer o buscar el proyecto entero sin recorrer carpeta por carpeta.
>
> **Qué NO es.** No es una fuente normativa. Cada documento conserva su archivo canónico, indicado
> bajo su título en la línea **Origen**. Ante cualquier diferencia manda el archivo original, no esta
> copia. Regla del corpus: *una definición tiene un único documento canónico* — ver
> [AGENTS del repositorio documental](#agents-documentacion) y [ADR 0003](#adr-0003).
>
> **Cómo se generó.** Concatenación mecánica: no se resumió, reescribió ni omitió texto. Los únicos
> cambios sobre el contenido original son (1) el título `#` de cada archivo pasa a ser el encabezado
> `###` de su sección y sus demás encabezados bajan dos niveles, para que el índice funcione, y
> (2) los enlaces relativos entre documentos del corpus se reescribieron como anclas internas de este
> archivo. Los enlaces externos quedaron intactos; los dos enlaces relativos heredados que ya no
> resuelven a ningún archivo (`docs/README.md` y `docs/data-interface.md`, rutas previas a la
> centralización del corpus, citadas en el README del servicio de IA) conservan su texto pero sin
> sintaxis de enlace, para no dejar vínculos rotos.
>
> **Estado del proyecto al momento de compilar.** Nada del dominio está implementado todavía: los
> tres repositorios de código contienen andamiaje. Todo este corpus es diseño, no descripción de
> software existente — ver [la guía del corpus](#guia-corpus) y el
> [baseline de alcance](#baseline).

**Compilado el** 2026-09-07 · **Versión del corpus** 3.0 (2026-09-01) · **Etapa 1**

---

## Índice general

**[Parte I — Punto de entrada del corpus](#parte-i)**

- [Guía del corpus documental](#guia-corpus)
- [README del repositorio documental](#readme-documentacion)
- [AGENTS del repositorio documental](#agents-documentacion)

**[Parte II — Producto](#parte-ii)**

- [D1 — Visión y objetivos del producto](#d1)
- [D2 — Glosario y lenguaje del dominio](#d2)
- [Entregable al Product Owner — Alcance de la IA generativa](#po-alcance-ia-generativa)

**[Parte III — Dominio](#parte-iii)**

- [D3 — Actores, roles y permisos](#d3)
- [D4 — Modelo de dominio](#d4)
- [D5 — Reglas de negocio](#d5)
- [D6 — Ciclos de vida y estados](#d6)
- [D10 — Catálogo de casos borde](#d10)

**[Parte IV — Flujos funcionales](#parte-iv)**

- [D7 — Flujos funcionales](#d7)

**[Parte V — Requerimientos](#parte-v)**

- [D8 — Especificación de requerimientos funcionales](#d8)
- [D9 — Requerimientos no funcionales](#d9)
- [D13 — Trazabilidad](#d13)

**[Parte VI — Arquitectura](#parte-vi)**

- [Arquitectura general del sistema](#arch-system)
- [Arquitectura del frontend](#arch-frontend)
- [Arquitectura del backend](#arch-backend)
- [Modelo relacional de PostgreSQL](#arch-database)
- [Interfaz de datos con el backend](#arch-data-interface)
- [Arquitectura del repositorio de IA](#arch-analytics)
- [Integración de IA generativa, ambientes y pruebas](#arch-generative-integration)
- [IA generativa — LLM autohospedado](#arch-generative)
- [Selección de modelo y runtime para la IA generativa](#arch-model-selection)
- [IA predictiva](#arch-predictive)

**[Parte VII — Decisiones y ADR](#parte-vii)**

- [D11 — Registro de decisiones de diseño](#d11)
- [ADR 0001 — Monorepo y motor analítico batch](#adr-0001)
- [ADR 0002 — Separación en tres repositorios](#adr-0002)
- [ADR 0003 — Repositorio documental central](#adr-0003)
- [ADR 0004 — LLM autohospedado sobre infraestructura del Polo](#adr-0004)
- [ADR 0005 — AI Gateway como módulo interno del backend](#adr-0005)
- [ADR 0006 — Modelo Qwen2.5-7B-Instruct sobre runtime Ollama](#adr-0006)
- [ADR 0007 — Sin RAG semántico, con prefiltrado determinista](#adr-0007)
- [ADR 0008 — Componentes clásicos como herramientas del LLM](#adr-0008)
- [ADR 0009 — Servicio generativo online en el Polo](#adr-0009)

**[Parte VIII — Planificación](#parte-viii)**

- [D12 — Riesgos y supuestos](#d12)
- [Baseline de alcance — Vivaz Adaptive · Etapa 1](#baseline)

**[Parte IX — Operación](#parte-ix)**

- [Base de datos compartida de desarrollo](#ops-local-db)

**[Parte X — Entrega y gobierno del trabajo](#parte-x)**

- [Flujo de trabajo en GitHub](#delivery-github)
- [Permisos y protección del repositorio](#delivery-permissions)

**[Parte XI — Repositorios de código](#parte-xi)**

- [Frontend — README](#repo-frontend-readme)
- [Frontend — AGENTS (instrucciones del repositorio)](#repo-frontend-agents)
- [Backend — README](#repo-backend-readme)
- [Backend — AGENTS (instrucciones del repositorio)](#repo-backend-agents)
- [Servicio de IA y analítica — README](#repo-ia-readme)
- [Servicio de IA y analítica — AGENTS (instrucciones del repositorio)](#repo-ia-agents)

**[Anexos](#anexos)**

- [Anexo A — manifest.json: mapa de enrutamiento del corpus](#anexo-manifest)
- [Anexo B — tools/check_docs.py: validador del corpus](#anexo-check-docs)
- [Anexo C — Plantilla de pull request (idéntica en los tres repositorios de código)](#anexo-pr-template)
- [Anexo D.1 — Plantilla de issue: reporte de error](#anexo-issue-bug)
- [Anexo D.2 — Plantilla de issue: funcionalidad](#anexo-issue-feature)
- [Anexo E — CODEOWNERS (idéntico en los tres repositorios de código)](#anexo-codeowners)
- [Anexo F.1 — CI del repositorio documental](#anexo-ci-docs)
- [Anexo F.2 — CI del frontend](#anexo-ci-frontend)
- [Anexo F.3 — CI del backend](#anexo-ci-backend)
- [Anexo F.4 — Workflow de migraciones del backend](#anexo-ci-migrations)
- [Anexo F.5 — CI del servicio de IA](#anexo-ci-ia)
- [Anexo G.1 — Variables de entorno del frontend](#anexo-env-frontend)
- [Anexo G.2 — Variables de entorno del backend](#anexo-env-backend)
- [Anexo G.3 — Variables de entorno del servicio de IA](#anexo-env-ia)

---

## Mapa de origen

Cada sección de este documento, con su identificador en `manifest.json` y su archivo real en el proyecto.

| Sección | ID | Archivo de origen |
| --- | --- | --- |
| [Guía del corpus documental](#guia-corpus) | `INDEX-CORPUS` | `Documentación/proyecto-gimnasio-documentacion/corpus-guide.md` |
| [README del repositorio documental](#readme-documentacion) | `—` | `Documentación/proyecto-gimnasio-documentacion/README.md` |
| [AGENTS del repositorio documental](#agents-documentacion) | `—` | `Documentación/proyecto-gimnasio-documentacion/AGENTS.md` |
| [D1 — Visión y objetivos del producto](#d1) | `D1` | `Documentación/proyecto-gimnasio-documentacion/product/vision-and-objectives.md` |
| [D2 — Glosario y lenguaje del dominio](#d2) | `D2` | `Documentación/proyecto-gimnasio-documentacion/product/glossary.md` |
| [Entregable al Product Owner — Alcance de la IA generativa](#po-alcance-ia-generativa) | `DELIVERABLE-PO-GENERATIVE-AI` | `Documentación/proyecto-gimnasio-documentacion/deliverable PO/alcance-ia-generativa.md` |
| [D3 — Actores, roles y permisos](#d3) | `D3` | `Documentación/proyecto-gimnasio-documentacion/domain/actors-roles-permissions.md` |
| [D4 — Modelo de dominio](#d4) | `D4` | `Documentación/proyecto-gimnasio-documentacion/domain/domain-model.md` |
| [D5 — Reglas de negocio](#d5) | `D5` | `Documentación/proyecto-gimnasio-documentacion/domain/business-rules.md` |
| [D6 — Ciclos de vida y estados](#d6) | `D6` | `Documentación/proyecto-gimnasio-documentacion/domain/lifecycles-and-states.md` |
| [D10 — Catálogo de casos borde](#d10) | `D10` | `Documentación/proyecto-gimnasio-documentacion/domain/edge-cases.md` |
| [D7 — Flujos funcionales](#d7) | `D7` | `Documentación/proyecto-gimnasio-documentacion/flows/functional-flows.md` |
| [D8 — Especificación de requerimientos funcionales](#d8) | `D8` | `Documentación/proyecto-gimnasio-documentacion/requirements/functional-requirements.md` |
| [D9 — Requerimientos no funcionales](#d9) | `D9` | `Documentación/proyecto-gimnasio-documentacion/requirements/non-functional-requirements.md` |
| [D13 — Trazabilidad](#d13) | `D13` | `Documentación/proyecto-gimnasio-documentacion/requirements/traceability.md` |
| [Arquitectura general del sistema](#arch-system) | `ARCH-SYSTEM` | `Documentación/proyecto-gimnasio-documentacion/architecture/system-overview.md` |
| [Arquitectura del frontend](#arch-frontend) | `ARCH-FRONTEND` | `Documentación/proyecto-gimnasio-documentacion/architecture/frontend.md` |
| [Arquitectura del backend](#arch-backend) | `ARCH-BACKEND` | `Documentación/proyecto-gimnasio-documentacion/architecture/backend.md` |
| [Modelo relacional de PostgreSQL](#arch-database) | `ARCH-DATABASE` | `Documentación/proyecto-gimnasio-documentacion/architecture/database-relational-model.md` |
| [Interfaz de datos con el backend](#arch-data-interface) | `ARCH-DATA-INTERFACE` | `Documentación/proyecto-gimnasio-documentacion/architecture/data-interface.md` |
| [Arquitectura del repositorio de IA](#arch-analytics) | `ARCH-ANALYTICS` | `Documentación/proyecto-gimnasio-documentacion/architecture/analytics-engine.md` |
| [Integración de IA generativa, ambientes y pruebas](#arch-generative-integration) | `ARCH-GENERATIVE-AI` | `Documentación/proyecto-gimnasio-documentacion/architecture/generative-ai-integration.md` |
| [IA generativa — LLM autohospedado](#arch-generative) | `ARCH-GENERATIVE-AI-SCOPE` | `Documentación/proyecto-gimnasio-documentacion/architecture/generative-ai.md` |
| [Selección de modelo y runtime para la IA generativa](#arch-model-selection) | `ARCH-AI-MODEL-SELECTION` | `Documentación/proyecto-gimnasio-documentacion/architecture/ai-model-selection.md` |
| [IA predictiva](#arch-predictive) | `ARCH-PREDICTIVE-AI` | `Documentación/proyecto-gimnasio-documentacion/architecture/predictive-ai.md` |
| [D11 — Registro de decisiones de diseño](#d11) | `D11` | `Documentación/proyecto-gimnasio-documentacion/decisions/design-decisions.md` |
| [ADR 0001 — Monorepo y motor analítico batch](#adr-0001) | `ADR-0001` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0001-monorepo-and-batch-engine.md` |
| [ADR 0002 — Separación en tres repositorios](#adr-0002) | `ADR-0002` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0002-three-repositories.md` |
| [ADR 0003 — Repositorio documental central](#adr-0003) | `ADR-0003` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0003-central-documentation-repository.md` |
| [ADR 0004 — LLM autohospedado sobre infraestructura del Polo](#adr-0004) | `ADR-0004-SELF-HOSTED-LLM` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0004-self-hosted-llm-server.md` |
| [ADR 0005 — AI Gateway como módulo interno del backend](#adr-0005) | `ADR-0005-AI-GATEWAY` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0005-ai-gateway-in-process-module.md` |
| [ADR 0006 — Modelo Qwen2.5-7B-Instruct sobre runtime Ollama](#adr-0006) | `ADR-0006-LLM-RUNTIME` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0006-llm-model-and-runtime-selection.md` |
| [ADR 0007 — Sin RAG semántico, con prefiltrado determinista](#adr-0007) | `ADR-0007-NO-RAG` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0007-no-rag.md` |
| [ADR 0008 — Componentes clásicos como herramientas del LLM](#adr-0008) | `ADR-0008-ML-TOOLS` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0008-tool-calling-for-ml-components.md` |
| [ADR 0009 — Servicio generativo online en el Polo](#adr-0009) | `ADR-0009` | `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0009-servicio-generativo-online-en-el-polo.md` |
| [D12 — Riesgos y supuestos](#d12) | `D12` | `Documentación/proyecto-gimnasio-documentacion/planning/risks-and-assumptions.md` |
| [Baseline de alcance — Vivaz Adaptive · Etapa 1](#baseline) | `PLAN-BASELINE` | `Documentación/proyecto-gimnasio-documentacion/planning/baseline-alcance-2026-09.md` |
| [Base de datos compartida de desarrollo](#ops-local-db) | `OPS-LOCAL-DB` | `Documentación/proyecto-gimnasio-documentacion/operations/local-database.md` |
| [Flujo de trabajo en GitHub](#delivery-github) | `DELIVERY-GITHUB` | `Documentación/proyecto-gimnasio-documentacion/delivery/github-workflow.md` |
| [Permisos y protección del repositorio](#delivery-permissions) | `DELIVERY-PERMISSIONS` | `Documentación/proyecto-gimnasio-documentacion/delivery/repository-permissions.md` |
| [Frontend — README](#repo-frontend-readme) | `—` | `Frontend/proyecto-gimnasio/README.md` |
| [Frontend — AGENTS (instrucciones del repositorio)](#repo-frontend-agents) | `—` | `Frontend/proyecto-gimnasio/AGENTS.md` |
| [Backend — README](#repo-backend-readme) | `—` | `Backend/proyecto-gimnasio-back/README.md` |
| [Backend — AGENTS (instrucciones del repositorio)](#repo-backend-agents) | `—` | `Backend/proyecto-gimnasio-back/AGENTS.md` |
| [Servicio de IA y analítica — README](#repo-ia-readme) | `—` | `IA/proyecto-gimnasio-ia/README.md` |
| [Servicio de IA y analítica — AGENTS (instrucciones del repositorio)](#repo-ia-agents) | `—` | `IA/proyecto-gimnasio-ia/AGENTS.md` |
| [Anexo A — manifest.json: mapa de enrutamiento del corpus](#anexo-manifest) | `—` | `Documentación/proyecto-gimnasio-documentacion/manifest.json` |
| [Anexo B — tools/check_docs.py: validador del corpus](#anexo-check-docs) | `—` | `Documentación/proyecto-gimnasio-documentacion/tools/check_docs.py` |
| [Anexo C — Plantilla de pull request (idéntica en los tres repositorios de código)](#anexo-pr-template) | `—` | `Backend/proyecto-gimnasio-back/.github/pull_request_template.md` |
| [Anexo D.1 — Plantilla de issue: reporte de error](#anexo-issue-bug) | `—` | `Backend/proyecto-gimnasio-back/.github/ISSUE_TEMPLATE/bug.yml` |
| [Anexo D.2 — Plantilla de issue: funcionalidad](#anexo-issue-feature) | `—` | `Backend/proyecto-gimnasio-back/.github/ISSUE_TEMPLATE/feature.yml` |
| [Anexo E — CODEOWNERS (idéntico en los tres repositorios de código)](#anexo-codeowners) | `—` | `Backend/proyecto-gimnasio-back/.github/CODEOWNERS` |
| [Anexo F.1 — CI del repositorio documental](#anexo-ci-docs) | `—` | `Documentación/proyecto-gimnasio-documentacion/.github/workflows/quality.yml` |
| [Anexo F.2 — CI del frontend](#anexo-ci-frontend) | `—` | `Frontend/proyecto-gimnasio/.github/workflows/ci.yml` |
| [Anexo F.3 — CI del backend](#anexo-ci-backend) | `—` | `Backend/proyecto-gimnasio-back/.github/workflows/ci.yml` |
| [Anexo F.4 — Workflow de migraciones del backend](#anexo-ci-migrations) | `—` | `Backend/proyecto-gimnasio-back/.github/workflows/migrations.yml` |
| [Anexo F.5 — CI del servicio de IA](#anexo-ci-ia) | `—` | `IA/proyecto-gimnasio-ia/.github/workflows/ci.yml` |
| [Anexo G.1 — Variables de entorno del frontend](#anexo-env-frontend) | `—` | `Frontend/proyecto-gimnasio/.env.example` |
| [Anexo G.2 — Variables de entorno del backend](#anexo-env-backend) | `—` | `Backend/proyecto-gimnasio-back/.env.example` |
| [Anexo G.3 — Variables de entorno del servicio de IA](#anexo-env-ia) | `—` | `IA/proyecto-gimnasio-ia/.env.example` |

### Repositorios del sistema

| Capa | Repositorio | Carpeta local |
| --- | --- | --- |
| Frontend | `Maico-Zurbriggen/proyecto-gimnasio` | `Frontend/proyecto-gimnasio` |
| Backend | `Maico-Zurbriggen/proyecto-gimnasio-back` | `Backend/proyecto-gimnasio-back` |
| Servicio de IA y analítica | `Maico-Zurbriggen/proyecto-gimnasio-ia` | `IA/proyecto-gimnasio-ia` |
| Documentación | `Maico-Zurbriggen/proyecto-gimnasio-documentacion` | `Documentación/proyecto-gimnasio-documentacion` |

---

<a id="parte-i"></a>

## Parte I — Punto de entrada del corpus

<a id="guia-corpus"></a>

### Guía del corpus documental

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/corpus-guide.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `INDEX-CORPUS`

**Versión del corpus** 3.0 · **Fecha** 2026-09-01 · **Estado** alineado con el [baseline de alcance de la Etapa 1](#baseline), el [modelo relacional](#arch-database) y ADR 0009. Puntos abiertos en D12/§5, entre ellos **I-09**, que afecta al cálculo de capacidad

La v2.0 incorpora las 42 correcciones de la auditoría y las dos definiciones del cliente que las hicieron posibles: **el sistema no es abierto** (el gimnasio afilia e invita) y **el equipamiento es del gimnasio** (la prescripción depende de qué máquinas tiene).

La v2.1 incorpora el **candidato de rutina**: el solicitante moldea la rutina generada antes de enviarla a revisión, sin tocar la prescripción y sin mover la puerta del entrenador. Toca D3, D5, D6, D7, D8, D10, D11 y D12. Ver D11/DD-33.

La v2.2 centraliza el corpus en un repositorio documental único, organiza las rutas por responsabilidad y agrega `manifest.json` como mapa determinista para agentes. No modifica reglas funcionales.

La v2.3 incorpora una [propuesta de integración generativa](#arch-generative-integration) con ambientes, trabajo local, promoción y pruebas. Declara tres diferencias que requieren ADR antes de cambiar la arquitectura o los requisitos vigentes.

La v2.4 aceptó [ADR 0009](#adr-0009): servicio Python y worker en el Polo, ingreso por ngrok, LLM separado, generación asíncrona y Neon Test compartida. También adoptó la promoción `develop → test → main`.

**La v3.0 incorpora el [baseline de alcance de la Etapa 1](#baseline)**, que cruza la votación del equipo con el Acta de Redefinición y con el estado real de los tres repositorios de código. Tres cosas que conviene saber antes de leer el resto del corpus:

1. **Existe una dimensión de alcance separada de la prioridad.** Un requisito puede ser MUST y estar diferido: la prioridad dice cuánto importa al producto, el alcance dice si se construye ahora. D8 v4.0 marca las dos.
2. **Nada del dominio está implementado.** Los tres repositorios contienen andamiaje. Todo el corpus es diseño, no descripción de software existente.
3. **Se cerraron tres defectos estructurales del propio corpus:** DD-34 estaba citada por ocho documentos y nunca redactada · dos ADR compartían el número 0004 decidiendo cosas incompatibles · nueve documentos no estaban registrados en el manifiesto, con lo que la validación automática fallaba. Los tres están corregidos.

**Y quedan dos preguntas abiertas que condicionan la planificación**, no la documentación: cuánta capacidad de construcción hay realmente (I-09 en D12/§5) y si el Product Owner libera el compromiso sobre la interpretación de lenguaje natural (I-10).

La v2.7 incorpora el [modelo relacional PostgreSQL](#arch-database), contratos JSON versionados sin datos identificatorios, candidatos con vencimiento por inactividad y estados técnicos de generación. Los presets dejan de ser contingencia obligatoria y pasan a alcance `COULD`; la primera entrega conserva plantillas privadas y creación manual por entrenadores.

---

#### Cómo leerlo

| Doc                                       | Contenido                                                                                             | Léelo si                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [D1](#d1)                 | Visión, capacidad central, alcance y 13 criterios de éxito                                            | Es el criterio que juzga todo lo demás. **Empezá acá**                         |
| [D2](#d2)                              | Glosario normativo + **12 enumeraciones cerradas**                                                    | Vas a escribir cualquier cosa. Un término o un valor que no esté acá no se usa |
| [D3](#d3)                | Actores, matriz de permisos, 10 reglas de acceso                                                      | Trabajás en autorización                                                       |
| [D4](#d4)                            | Entidades, 8 puntos difíciles con alternativas y sacrificios, 23 restricciones                        | Vas a tocar la estructura de datos. **Congelar antes de escribir código**      |
| [D5](#d5)                          | 152 reglas verificables, **cada constante con su origen marcado**                                     | Implementás cualquier cálculo o validación                                     |
| [D6](#d6)                   | 10 ciclos de vida, con las transiciones **imposibles** y su motivo                                    | Implementás una entidad con estado                                             |
| [D7](#d7)                         | 21 flujos con cursos normales, alternativos y de excepción                                            | Implementás una funcionalidad completa                                         |
| [D8](#d8)           | RF-001 a RF-120 con tipo, prioridad y dependencias                                                    | Planificás o estimás                                                           |
| [D9](#d9)       | 40 requerimientos, todos con criterio de verificación                                                 | Definís la estrategia de pruebas                                               |
| [D10](#d10)                             | 73 casos borde en 10 categorías                                                                       | Antes de dar por terminada cualquier funcionalidad                             |
| [D11](#d11)                    | 33 decisiones con opciones, fundamento y consecuencias                                                | Querés saber por qué algo es así, o pensás cambiarlo                           |
| [D12](#d12)                | 10 supuestos, **37 constantes con su origen**, 16 riesgos, aritmética del esfuerzo y orden de recorte | Sos responsable del plan. **Leelo antes de comprometer fechas**                |
| [D13](#d13)                     | Qué requerimiento responde a qué necesidad, y qué quedó sin cubrir                                    | Preparás la defensa o discutís alcance con el cliente                          |

#### Las cuatro tablas que sostienen la prescripción

Son determinísticas, auditables y discutibles con un entrenador real. En generación inicial validan la salida del LLM; en diagnóstico y adaptación determinan el comportamiento:

| Tabla                         | Dónde              | Qué determina                                                                                  |
| ----------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| Restricciones del tipo de rutina | D5/RN-39a       | Valida frecuencia, días, series, repeticiones, descansos y cobertura mínima del tipo propuesto |
| Compatibilidad                | D5/RN-44a a RN-44d | Cuándo un ejercicio está contraindicado, excede el nivel o falta el equipamiento               |
| Criterios de diagnóstico      | D5/RN-79a          | Cuál de las cinco situaciones tiene cada ejercicio y el conjunto                               |
| Reglas de ajuste              | D5/RN-89a          | Qué ajuste, de qué tipo y de qué magnitud, corresponde a cada situación                        |

#### Convención de marcado

`[F]` lo afirma una fuente · `[I]` inferencia · `[S]` convención de este proyecto, sin fuente externa · 👁 decisión que las fuentes tomaron sin advertirlo · 🆕 nuevo · ⬆⬇ cambio de prioridad · ✎ enunciado modificado · ⛔ derogado

#### Lo que hay que resolver antes de escribir código

1. **Confirmar el tamaño del equipo** (D12/S-01). El cliente escribió "somos 3 personas" y listó 9. Se tomó la lista.
2. **Conversación de alcance.** 82 requerimientos MUST contra ~504 h de capacidad de construcción (D12/§3) — entre 1,3 y 1,8 veces lo que entra. El orden de recorte está en D12/§4.
3. **Validar las cuatro tablas con un entrenador en ejercicio.** 33 de las 37 constantes del sistema son convenciones de este proyecto, no datos del dominio (D12/§1.1). Si están mal, el sistema funciona y prescribe mal, que es peor que fallar.
4. **Congelar D4 y D5.** Un error en DD-02, DD-03, DD-04 o DD-26 se paga con un rediseño imposible a mitad del plazo.
5. **Verificar la fuente del catálogo** (D12/S-09): tiene que traer, o permitir derivar, el equipamiento requerido y las articulaciones exigidas por cada ejercicio. Sin eso, la compatibilidad se cura a mano.
6. **Verificar que existe una fuente de datos con historial por usuario y por serie** (D12/S-03). De eso depende que el aprendizaje automático predictivo, que es núcleo, tenga sustento.
7. **Cerrar los puntos de producto abiertos** de D12/§5.
8. **Resolver la creación de migraciones** sin ejecutar `migrate dev` sobre Neon Test compartida (D12/I-07).
9. **Confirmar la operación en el Polo**: contrato LLM, dominio ngrok estable, procesos permanentes y rollback (D12/I-08).


---

<a id="readme-documentacion"></a>

### README del repositorio documental

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/README.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `—`

Fuente única de verdad funcional, técnica y operativa de la plataforma de entrenamiento asistido.

#### Entrada rápida

- Agentes de IA: leer primero [AGENTS.md](#agents-documentacion) y después [manifest.json](#anexo-manifest).
- Personas que conocen por primera vez el proyecto: comenzar por [la guía del corpus](#guia-corpus).
- Arquitectura general: [architecture/system-overview.md](#arch-system).
- Integración generativa: [architecture/generative-ai-integration.md](#arch-generative-integration).
- Implementación de una funcionalidad: consultar el conjunto indicado por `load_when` en el manifiesto, no un documento aislado.

#### Organización

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

#### Validación

```bash
python tools/check_docs.py
```


---

<a id="agents-documentacion"></a>

### AGENTS del repositorio documental

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/AGENTS.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `—`

#### Propósito

Este repositorio es la única fuente de verdad documental del Proyecto Gimnasio. Los repositorios de frontend, backend e IA conservan solamente su `README.md` y su `AGENTS.md`; cualquier definición compartida o que afecte a más de un componente se mantiene aquí.

#### Inicio obligatorio para agentes

1. Leer `manifest.json`.
2. Identificar el tipo de tarea y cargar sólo los documentos indicados por `load_when`.
3. Para cualquier cambio de dominio, leer primero `product/glossary.md` y respetar sus términos y enumeraciones cerradas.
4. Para implementar una funcionalidad, combinar como mínimo su flujo, reglas de negocio, estados, casos borde y requisitos trazados.
5. Leer también el `AGENTS.md` del repositorio de código que se modificará; sus reglas locales complementan esta documentación.

No inferir una regla ausente. Si la documentación no alcanza o se contradice, registrar el punto abierto en `planning/risks-and-assumptions.md` y resolverlo antes de codificar.

#### Autoridad por tema

- Vocabulario y enumeraciones: `product/glossary.md`.
- Entidades y restricciones de integridad: `domain/domain-model.md`.
- Reglas, constantes y cálculos: `domain/business-rules.md`.
- Estados y transiciones: `domain/lifecycles-and-states.md`.
- Alcance funcional y prioridad: `requirements/functional-requirements.md`.
- Calidad y verificabilidad: `requirements/non-functional-requirements.md`.
- Topología y fronteras técnicas: `architecture/` y los ADR vigentes.
- Forma de trabajo y permisos: `delivery/`.

Cuando dos documentos parezcan incompatibles, no elegir silenciosamente: verificar sus identificadores, el estado del ADR y la trazabilidad, y documentar la resolución.

#### Reglas de mantenimiento

- Una definición tiene un único documento canónico. En los demás lugares se enlaza; no se copia ni se resume como una segunda fuente normativa.
- Conservar los identificadores estables `RN-*`, `RF-*`, `RNF-*`, `RA-*`, `RI-*`, `CB-*`, `DD-*`, `PD-*` y `S-*`.
- Un cambio de regla debe actualizar en el mismo PR los requisitos, flujos, casos borde, decisiones y trazabilidad afectados.
- Un cambio de frontera entre repositorios debe incluir un ADR y PR relacionados en los repositorios de código afectados.
- Registrar todo documento nuevo en `manifest.json`, con alcance, autoridad y condiciones de carga.
- Usar enlaces relativos dentro de este repositorio y enlaces permanentes de GitHub hacia repositorios externos.
- No guardar código de aplicación, secretos, datos personales, datasets, modelos ni artefactos generados.

#### Repositorios del sistema

- Frontend: `Maico-Zurbriggen/proyecto-gimnasio`.
- Backend: `Maico-Zurbriggen/proyecto-gimnasio-back`.
- Servicio de IA y analítica: `Maico-Zurbriggen/proyecto-gimnasio-ia`.

#### Verificación

Ejecutar antes de cerrar un cambio:

```bash
python tools/check_docs.py
```

La verificación controla el manifiesto, documentos huérfanos, contenido duplicado y enlaces relativos.


---

<a id="parte-ii"></a>

## Parte II — Producto

<a id="d1"></a>

### D1 — Visión y objetivos del producto

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/product/vision-and-objectives.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D1`

|                    |                                                         |
| ------------------ | ------------------------------------------------------- |
| **Versión**        | 2.1                                                     |
| **Fecha**          | 2026-09-01                                              |
| **Estado**         | Aprobado en Fase 1, base para el resto del corpus       |
| **Depende de**     | Nada. Es el documento raíz                              |
| **Es criterio de** | Todos. Una funcionalidad que no se conecte con §3 sobra |

**Marcas usadas en todo el corpus:** `[F]` lo afirma una fuente · `[I]` inferencia · `[S]` supuesto por ausencia de información (registrado en D12).

**Cambios de la v2.1 ([baseline de alcance](#baseline)).** La visión del producto **no cambia**: la votación del equipo confirmó el ciclo central por mayorías amplias y el cliente no movió el núcleo. Lo que cambia es qué parte de esa visión se construye en la Etapa 1 (§6.1) y una garantía de continuidad que dejó de ser cierta al retirarse los presets (§3.2).

---

#### 1. Problema

Una persona que entrena necesita que lo que hace hoy tenga en cuenta lo que le pasó hasta hoy: cómo viene respondiendo, qué le duele, qué equipamiento tiene, qué se propuso lograr. Esa adecuación permanente es un trabajo que hoy nadie hace de forma sostenida.

| Actor                      | Problema                                                                                                                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Alumno**                 | Entrena durante meses con un plan que se decidió una sola vez. Si progresa, el plan se le queda corto; si se estanca, el plan no cambia; si se lesiona o cambia de objetivo, el plan sigue igual `[I]`                                           |
| **Gimnasio (como sostén)** | Es quien tiene las máquinas, el espacio y los entrenadores. El plan de una persona sólo es realizable con lo que ese gimnasio efectivamente tiene, y hoy nadie cruza ambas cosas de forma sistemática `[F: cliente]`                             |
| **Entrenador**             | Sabe qué habría que ajustarle a cada alumno pero no puede hacerlo para todos. Revisar a fondo a veinticinco personas cada pocas semanas no entra en su jornada, así que atiende a los que preguntan y a los que ve `[F: A §2.1, autoridad baja]` |
| **Gimnasio**               | Pierde socios que se fueron apagando de a poco y se entera cuando ya se dieron de baja `[F: A §2.1, autoridad baja]`                                                                                                                             |

`[S-04]` Esta caracterización no fue contrastada con un gimnasio real: proviene de un análisis interno del equipo. Es el supuesto sobre el que se apoya todo el producto y el más barato de verificar. Ver D12.

#### 2. Situación actual y por qué no alcanza

La rutina vive en un papel, en una planilla o en la memoria del entrenador, y el seguimiento ocurre por conversación `[F: A §2.1]`. Falla por tres razones, en orden de importancia:

1. **No queda registro de lo que realmente pasó.** Se anota lo que había que hacer, no lo que se hizo. Sin esa diferencia nadie puede decir si el plan se cumplió, si funcionó, o si la persona dejó de venir.
2. **Revisar cuesta más que no revisar.** Ajustar bien una rutina exige mirar semanas de historial. Con muchos alumnos, la opción realista es no ajustar.
3. **Nada avisa.** El estancamiento, la caída de constancia y el abandono son graduales; cuando se vuelven visibles ya ocurrieron.

Una aplicación que sólo registre entrenamientos resuelve el punto 1 y ninguno de los otros dos.

#### 3. Capacidad central

> **Mantener la prescripción de cada alumno permanentemente adecuada a su estado: desde el primer día, cuando no hay ningún historial, y a lo largo del tiempo, cuando el historial dice que hay que cambiar algo — fundamentando cada cambio y sometiéndolo siempre a la revisión de su entrenador.**

Cinco componentes que sólo tienen valor juntos `[F: RF-086, RF-087, RF-088, RF-089, RF-090, RF-091, RF-094 y decisión del cliente de 2026-08-18]`:

|     | Capacidad                                                                                                                                                                          | Requerimientos         |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| C1  | **Nadie queda sin plan.** Todo alumno incorporado obtiene de inmediato una rutina propuesta, compatible con sus condiciones, aunque no tenga ningún historial                      | RF-087, RF-025         |
| C2  | **Ninguna prescripción contradice el estado de la persona**, ni al asignarla ni después, cuando cambia una condición, el objetivo o la aptitud                                     | RF-086, RF-094         |
| C3  | **La evolución se evalúa sola.** El sistema distingue periódicamente entre progresión adecuada, estancamiento y sobreexigencia                                                     | RF-088                 |
| C4  | **El cambio lo decide la inteligencia del sistema, con fundamento**, a partir del contexto completo del alumno                                                                     | RF-089, RF-090, RF-054 |
| C5  | **El entrenador es la puerta.** Ninguna rutina llega vigente a un alumno sin que un entrenador la haya revisado y aprobado. Sin excepciones, cualquiera sea el origen de la rutina | RF-091, RF-110         |

##### 3.0 Dónde está la inteligencia

**Los componentes de inteligencia artificial y de aprendizaje automático son el centro del producto, no un accesorio.** `[F: decisión del cliente, 2026-08-18]` El sistema no se limita a mostrar datos para que una persona decida: **decide**, y presenta su decisión fundamentada para que una persona la valide.

De ahí se derivan tres consecuencias que gobiernan todo el corpus:

1. **La captación de datos del alumno es infraestructura crítica, no una funcionalidad más.** Perfil, objetivo, condiciones físicas, equipamiento, aptitud, mediciones, series registradas y esfuerzo percibido no existen para llenar pantallas: son el **contexto del alumno**, la entrada de todo componente de decisión. Un dato que no se capta es una decisión que se toma a ciegas. Los requerimientos de registro tienen la misma prioridad que los de decisión.
2. **Hay dos clases de componente y no se confunden.** Los **de decisión** (generación de rutinas, ajuste de la prescripción, recomendación de sustitutos) ✎ *(v2.1: se retira la estimación de riesgo, fuera del producto desde [DD-34](#d11))* producen valores y estructuras; su salida se valida automáticamente contra las reglas de compatibilidad y siempre pasa por revisión humana. Los **narrativos** (justificación de un ajuste, resumen de progreso) sólo redactan sobre hechos ya calculados y no pueden introducir ningún valor que no esté en su entrada.
3. **La decisión automática y la revisión humana no compiten.** La primera hace que el ajuste exista; la segunda hace que sea seguro. Sin la primera, el entrenador vuelve a revisar veinticinco fichas a mano. Sin la segunda, el sistema prescribe sin responsable.

**Dónde decide una regla y dónde un modelo — dicho sin adornos.** El LLM interpreta el pedido, selecciona el tipo y construye el candidato inicial. Catálogo, compatibilidad y rangos se validan mediante reglas determinísticas y auditables; el diagnóstico y los ajustes también permanecen escritos como tablas. Los componentes aprendidos futuros actúan en alternativas, riesgo y segmentación. Esta distribución cumple el alcance generativo sin entregar al modelo la autoridad de seguridad ni la puerta del entrenador. Ver D11/DD-31, ADR 0009 y D12/R-16.

##### 3.1 El ciclo que gobierna el alcance

```
   estado del alumno ──▶ prescripción ──▶ ejecución registrada ──▶ diagnóstico
          ▲                                                             │
          │                                                             ▼
   nueva prescripción ◀── REVISIÓN DEL ENTRENADOR ◀── propuesta fundamentada
                                   ▲
                        toda rutina pasa por acá,
                  venga de una plantilla del entrenador,
                de una generación, o de un preset si se
                          implementa RF-021
```

El registro de entrenamientos, los indicadores, los tableros y la vista de cartera **son el insumo de este ciclo, no productos separados**. Existen porque sin ellos no hay diagnóstico, y sin diagnóstico no hay adaptación fundamentada.

**Criterio de corte:** si una funcionalidad no aparece en este ciclo ni lo alimenta, no entra.

##### 3.2 Qué queda en pie cuando falla un servicio externo

Siendo la inteligencia el centro, la continuidad operativa deja de ser una concesión y pasa a ser un requisito de disponibilidad del núcleo. La distinción que lo hace posible:

- **El diagnóstico y el cálculo de ajustes viven dentro del sistema.** Se resuelven con reglas propias sobre datos propios: RN-79a y RN-89a son tablas explícitas, no llamadas a un servicio. ✎ v2.1: **la generación de rutinas ya no está en esta lista.** Depende por completo del servicio del Polo, y es la corrección que se explica abajo.
- **Lo que depende de un servicio externo es la conversación**: interpretar una descripción en lenguaje natural y redactar una justificación. Si ese servicio no está disponible, la entrada se hace por formulario estructurado y la justificación se presenta en forma tabulada `[F: RF-058]`.

Es decir: si falla el servicio externo el sistema sigue decidiendo, sólo que deja de hablar. Si además se apagaran los componentes de decisión, el sistema sigue siendo usable como herramienta de prescripción y registro manual — pero deja de ser este producto.

> **Corrección de la v2.1, y es importante.** El párrafo anterior era cierto mientras la capacidad de decidir viviera dentro del sistema. En la Etapa 1 **no vive dentro del sistema**: al no construirse presets ni un generador determinístico, la construcción de una rutina la resuelve por completo el servicio generativo del Polo. Si ese servicio no responde, el sistema **no sigue decidiendo**: la única vía que queda es que un entrenador asigne a mano una plantilla suya (RF-019, RF-058, [D11/DD-35](#d11)).
>
> Un alumno nuevo en un gimnasio sin plantillas cargadas y con el servicio caído **no obtiene ninguna rutina**, y con eso la capacidad C1 deja de cumplirse. No hay mitigación técnica dentro del alcance de esta etapa; la mitigación es operativa —cargar plantillas de arranque al aprovisionar cada gimnasio— y hay que ejecutarla, no suponerla. Ver [D12/R-17](#d12) y la decisión PD-03 del baseline.

#### 4. Actores

| Actor                                                           | ¿Va?                       | Justificación                                                                                                                                                                                                                     |
| --------------------------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Proveedor del sistema                                           | Sí, fuera de la aplicación | Aprovisiona el gimnasio afiliado y su primer administrador. Sin él ningún gimnasio arranca. No es un rol, no inicia sesión. Ver D11/DD-30                                                                                         |
| Alumno                                                          | Sí                         | Actor central. Puede elegir y pedir una rutina, pero no ponerla en vigencia por sí mismo. **Sólo existe por invitación de un gimnasio afiliado**                                                                                  |
| Entrenador                                                      | Sí                         | **Actor obligatorio del ciclo.** Revisa y aprueba toda rutina antes de que rija, resuelve las propuestas de adaptación, interviene sobre las rutinas de su cartera                                                                |
| Administrador de gimnasio                                       | Sí, acotado                | Invita usuarios, gestiona roles y asignaciones, **mantiene el inventario de equipamiento** y accede a la analítica agregada. El inventario determina qué puede prescribirse en todo el gimnasio: no es un rol administrativo puro |
| Visitante no autenticado                                        | No                         | Ver D11/DD-21                                                                                                                                                                                                                     |
| Recepcionista, nutricionista, superadministrador multi-gimnasio | No                         | Dependen de funcionalidades fuera de alcance (§6)                                                                                                                                                                                 |

#### 5. Propuesta de valor

Para el **alumno**: un plan que se mantiene adecuado a lo que le está pasando, y evidencia de si progresa.
Para el **entrenador**: no tener que revisar a veinticinco personas para descubrir a cuáles hay que cambiarles algo; el sistema propone y él decide.
Para el **gimnasio**: aviso temprano de deserción y visibilidad de la actividad agregada.

#### 6. No-alcance

No porque cueste construirlo, sino porque no es este problema.

| Fuera                                               | Precisión                                                                                                                                                                                                               |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Decidir por la persona**                          | El sistema propone; el entrenador aprueba. Ninguna rutina rige ni cambia sin su autorización explícita `[F: RF-091 + decisión del cliente]`                                                                             |
| **Entrenar sin entrenador**                         | Todo alumno tiene un entrenador vigente. Un alumno sin entrenador no puede recibir ninguna rutina nueva ni ninguna adaptación —conserva la vigente— y el sistema lo señala al administrador `[F: decisión del cliente]` |
| **Usarse sin gimnasio**                             | El sistema no es abierto. Nadie se registra por su cuenta: la cuenta nace de una invitación de un gimnasio afiliado, y la prescripción depende del equipamiento que ese gimnasio tiene `[F: decisión del cliente]`      |
| **Prescribir con equipamiento propio del alumno**   | Lo disponible es el inventario del gimnasio. Un alumno que además entrena en su casa no recibe una rutina para su casa `[F: decisión del cliente]` · Ver D11/DD-26                                                      |
| **Seguimiento de comidas**                          | Sin base de alimentos, sin composición ni registro de ingesta `[F: decisión del cliente]`. Ver DD-13                                                                                                                    |
| **Salud clínica**                                   | No diagnostica, no rehabilita, no corrige técnica, no reemplaza a un profesional                                                                                                                                        |
| **Operación del gimnasio como negocio**             | Cobros, cuotas, facturación, control de acceso físico, reservas de clases                                                                                                                                               |
| **Alta y administración de gimnasios y sucursales** | El sistema sirve a varios gimnasios; no los gestiona `[F: decisión del cliente]`                                                                                                                                        |
| **Comunicación en vivo**                            | Hay comentarios asincrónicos sobre una sesión o rutina; no hay mensajería `[F: RF-077 WON'T]`                                                                                                                           |
| **Lo que el sistema no puede medir**                | Calorías quemadas, calidad de ejecución, datos de dispositivos externos `[F: RF-081 WON'T]`                                                                                                                             |
| **Alojamiento de video propio**                     | Se referencian recursos externos `[F: RF-079 WON'T]`                                                                                                                                                                    |

##### 6.1 Qué queda fuera de la Etapa 1 sin salir del producto

La distinción importa: lo de §6 no es este problema y no volverá. Lo de aquí **sí es este producto** y está diferido por capacidad y por la votación del equipo — 8 de 9 integrantes. Ver el [baseline de alcance](#baseline).

| Fuera de la Etapa 1                                         | Consecuencia para el usuario en esta etapa                                                                                                     |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Toda la nutrición, incluida la estimación energética        | El sistema no dice nada sobre alimentación `[2/8 votos]`                                                                                        |
| Presets publicados y compartidos entre entrenadores         | Cada entrenador construye y reutiliza **sus** plantillas; no se comparten dentro del gimnasio `[1/8]`                                          |
| Solicitud de rutina iniciada por el alumno, y su ajuste     | La rutina la origina el entrenador o la generación automática de la incorporación. El alumno recibe, no pide `[3/8]`                          |
| Comentarios asincrónicos                                    | No hay canal entrenador↔alumno más allá de los avisos del sistema `[1/8]`                                                                       |
| Representación muscular sobre esquema del cuerpo            | El mismo dato se presenta como barras por grupo muscular. **Es una degradación visible del diferencial declarado del producto** `[4/8]`        |
| Registro diferido de sesiones pasadas                       | Una sesión no cargada el mismo día se pierde, y **la adherencia queda sesgada a la baja**. Hay que declararlo al presentar el indicador `[2/8]` |
| Panel analítico del gimnasio                                | El administrador gestiona; no mide `[2/8]`                                                                                                     |
| Baja de cuenta, portabilidad y anonimización                | **Una persona no puede irse del sistema llevándose ni borrando sus datos de salud.** Es una decisión de exposición, no de alcance funcional `[0/8]` |
| Estimación de riesgo de abandono                            | Ya estaba fuera desde la v3.3 de D8; la votación lo confirma `[1/8]`                                                                            |

**Lo que esto le cuesta a la propuesta de valor.** Para el gimnasio, «aviso temprano de deserción» (§5) queda sin sustento en esta etapa: sin estimación de riesgo y sin panel agregado, lo único que queda es la caída de adherencia visible en la cartera del entrenador. Conviene decirlo así en la defensa en lugar de sostener una promesa que el alcance no respalda.
| **Representación tridimensional del cuerpo**        | La representación bidimensional cubre la misma necesidad `[F: RF-080 WON'T]`                                                                                                                                            |

#### 7. Criterios de éxito

No son métricas de tablero: son las preguntas que, contestadas con datos del propio sistema, dicen si esto sirvió.

| #   | Pregunta                                                                                        | Observación                                                                                                                                                                                                                       | Verificable sin usuarios reales |
| --- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| E1  | ¿Alguien se quedó sin plan?                                                                     | Todo alumno incorporado tiene una rutina propuesta el mismo día, y vigente en cuanto su entrenador la revisa. Ningún alumno queda sin entrenador vigente                                                                          | Sí                              |
| E1b | ¿Cuánto tarda la puerta?                                                                        | Días entre que una rutina se propone y su entrenador la resuelve. Si crece, el sistema deja de servir por congestión humana, no por defecto técnico                                                                               | No                              |
| E2  | ¿Alguna rutina vigente prescribe algo incompatible con las condiciones vigentes de esa persona? | Cero casos                                                                                                                                                                                                                        | Sí                              |
| E3  | ¿Cuánto tarda el sistema en reaccionar?                                                         | Días entre la aparición de un estancamiento o caída de constancia y la existencia de una propuesta                                                                                                                                | No                              |
| E4  | ¿Las propuestas se aceptan?                                                                     | Proporción aprobada total o parcialmente. Una tasa de rechazo alta significa que el diagnóstico es malo, y es más útil saberlo que no tenerlo                                                                                     | No                              |
| E5  | ¿El entrenador atiende a quien lo necesita?                                                     | Sus intervenciones se concentran en alumnos señalados                                                                                                                                                                             | No                              |
| E6  | ¿El pasado se mantuvo intacto?                                                                  | Una sesión ejecutada nunca cambia porque la rutina haya cambiado después                                                                                                                                                          | Sí                              |
| E7  | ¿Cada cambio tiene explicación?                                                                 | Toda adaptación conserva el criterio que la motivó y los datos que lo sustentan                                                                                                                                                   | Sí                              |
| E8  | ¿El alumno percibe que progresa?                                                                | Puede responder "¿estoy mejor que hace tres meses?" sin que se lo explique nadie                                                                                                                                                  | No                              |
| E9  | ¿La decisión automática es mejor que una regla trivial?                                         | Cada componente de decisión y de estimación se compara contra un criterio de referencia simple sobre un conjunto reservado, y se conservan ambas métricas. Que la regla simple gane también es un resultado, y hay que informarlo | Sí                              |
| E10 | ¿Lo narrado es cierto?                                                                          | Ningún valor numérico presente en un texto generado está ausente de sus datos de entrada. Cero excepciones                                                                                                                        | Sí                              |
| E11 | ¿El contexto está completo?                                                                     | Proporción de alumnos con contexto suficiente para decidir: objetivo, condiciones, equipamiento y nivel declarados. Un contexto pobre degrada toda decisión aguas abajo                                                           | Sí                              |

| E12 | ¿Lo que se prescribe se puede hacer en este gimnasio? | Ninguna rutina vigente contiene un ejercicio que exija equipamiento ausente del inventario. Cero casos | Sí |

**Verificables sin usuarios reales:** E1, E2, E6, E7, E9, E10, E11 y E12 — todos binarios o contables sobre la base.
**Requieren uso sostenido:** E1b, E3, E4, E5 y E8. Con datos simulados sólo se demuestra el mecanismo, no el efecto, y así deben presentarse.


---

<a id="d2"></a>

### D2 — Glosario y lenguaje del dominio

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/product/glossary.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D2`

|                |                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Versión**    | 2.1                                                                                                                             |
| **Fecha**      | 2026-09-01                                                                                                                      |
| **Estado**     | Normativo                                                                                                                       |
| **Depende de** | D1                                                                                                                              |
| **Regla**      | Todo el corpus usa exclusivamente estos términos, con esta ortografía y este significado. Un término no definido aquí no se usa |

**Cambios de la v1.0:** se define el verbo _asignar_ (colisionaba con _asignación_) · se define _progreso_ en lugar de prohibirlo · el equipamiento pasa a ser del gimnasio · se agregan _afiliación_, _invitación_, _inventario_, _articulación_, _contraindicación_ · se incorporan las siete enumeraciones cerradas de §4, que antes se presuponían sin existir.

**Cambios de la v2.1 (replanteo de IA, [D11/DD-34](#d11)):** el término "Riesgo de abandono" se retira (RF-061 a RF-063 → WON'T) y pasa a §2 como término retirado del alcance.

---

#### 1. Términos del dominio

##### 1.1 Ámbito, identidad y alta

| Término               | Definición                                                                                                                                                                                                                 | Sinónimos descartados              |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Gimnasio**          | Organización afiliada al sistema. Ámbito de aislamiento de toda la información y **origen del equipamiento disponible** para sus alumnos. No es un objeto administrable por los usuarios de la aplicación                  | Sucursal, sede, tenant, club       |
| **Afiliación**        | Acuerdo por el cual un gimnasio incorpora el sistema. Ocurre **fuera de la aplicación**; su efecto dentro del sistema es el aprovisionamiento del gimnasio y de su primer administrador                                    | Contratación, alta de cliente      |
| **Aprovisionamiento** | Operación por la que el proveedor del sistema crea un gimnasio afiliado, su zona horaria y su primer administrador. No es una funcionalidad accesible a ningún rol de la aplicación                                        | Instalación, bootstrap             |
| **Invitación**        | Autorización nominal y temporal, emitida por un administrador o por un entrenador, que habilita a una persona a crear su cuenta en un gimnasio determinado con un rol determinado. **Es la única vía de alta de usuarios** | Alta, registro abierto             |
| **Usuario**           | Persona con cuenta en un gimnasio. Posee uno o más roles                                                                                                                                                                   | Cuenta, socio, miembro             |
| **Alumno**            | Rol que recibe prescripciones y registra ejecuciones                                                                                                                                                                       | Cliente, socio, deportista, atleta |
| **Entrenador**        | Rol que diseña prescripciones, revisa toda rutina antes de que rija y resuelve las propuestas de adaptación                                                                                                                | Profesor, coach, instructor        |
| **Administrador**     | Rol que gestiona invitaciones, usuarios, roles, asignaciones y el inventario de equipamiento del gimnasio, y consulta la analítica agregada                                                                                | Admin, dueño, gerente              |
| **Asignación**        | Relación vigente entre un entrenador y un alumno. Tiene fecha de inicio y, cuando termina, fecha de fin. Determina el acceso del entrenador a la información del alumno. **Se usa exclusivamente para esta relación**      | Vinculación, cartera               |
| **Asignar** _(verbo)_ | Establecer una asignación entre un entrenador y un alumno. **Nunca se dice "asignar una rutina"**: una rutina se _solicita_, se _revisa_ y se _pone en vigencia_                                                           | Vincular                           |
| **Cartera**           | Conjunto de alumnos con asignación vigente a un entrenador determinado                                                                                                                                                     | Nómina, listado de alumnos         |

##### 1.2 Equipamiento

| Término          | Definición                                                                                                                                                           | Sinónimos descartados                       |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **Equipamiento** | Elemento de la enumeración cerrada de §4.1. Es el vocabulario común entre lo que un ejercicio requiere y lo que un gimnasio posee                                    | Material, aparato, máquina                  |
| **Inventario**   | Conjunto de equipamiento que un gimnasio declara poseer. Lo mantiene el administrador y **determina qué ejercicios son prescribibles a los alumnos de ese gimnasio** | Equipamiento disponible, parque de máquinas |

**Decisión de dominio:** el equipamiento disponible para un alumno es el inventario de su gimnasio. El alumno no declara equipamiento propio. Ver D11/DD-26.

##### 1.3 Estado del alumno

| Término                  | Definición                                                                                                                                                                                       | Sinónimos descartados                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| **Perfil**               | Datos del alumno que condicionan la prescripción: edad, sexo, altura, nivel de experiencia y días semanales disponibles                                                                          | Ficha, datos personales                   |
| **Nivel de experiencia** | Clasificación del alumno según §4.4. Limita qué ejercicios le son prescribibles                                                                                                                  | Nivel                                     |
| **Objetivo**             | Propósito de entrenamiento declarado por el alumno, tomado de §4.5, vigente durante un período. Un alumno tiene como máximo un objetivo vigente, y ninguno antes de declararlo                   | Meta, finalidad                           |
| **Condición física**     | Limitación declarada por el alumno que afecta una **zona corporal** (§4.3) con una **severidad** (§4.6). Tiene fecha de inicio y, cuando cesa, fecha de fin                                      | Lesión, restricción, patología            |
| **Zona corporal**        | Elemento de la unión de las enumeraciones de grupos musculares (§4.2) y articulaciones (§4.3). Es el vocabulario que vincula una condición física con un ejercicio                               | Parte del cuerpo, área                    |
| **Contraindicación**     | Relación calculada entre un ejercicio y una condición física vigente de un alumno, según la regla RN-44a. No es un dato que alguien cargue: es el resultado de una comparación                   | Restricción, incompatibilidad (ver abajo) |
| **Aptitud**              | Constancia de aptitud para la práctica deportiva registrada para un alumno, con fecha de emisión y de vencimiento. Su ausencia o vencimiento se advierte de forma destacada; nunca impide operar | Apto físico, certificado médico           |
| **Estado de membresía**  | Situación declarada del alumno respecto del gimnasio. Exclusivamente informativa                                                                                                                 | Cuota, suscripción                        |
| **Medición corporal**    | Valor numérico fechado de una magnitud del cuerpo del alumno. Como máximo un registro por tipo y fecha                                                                                           | Medida, antropometría                     |

##### 1.4 Catálogo

| Término                      | Definición                                                                                                                                                                                                         | Sinónimos descartados   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| **Ejercicio**                | Movimiento identificable del catálogo, con instrucciones, equipamiento requerido, patrón de movimiento (§4.7), nivel de dificultad (§4.4), articulaciones exigidas (§4.3), clasificación muscular y recurso visual | Movimiento, actividad   |
| **Catálogo base**            | Conjunto de ejercicios común a todos los gimnasios, incorporado por carga inicial y no editable por ningún usuario                                                                                                 | Semilla, biblioteca     |
| **Catálogo del gimnasio**    | Ejercicios creados por entrenadores de un gimnasio, visibles sólo dentro de él                                                                                                                                     | Ejercicios propios      |
| **Catálogo prescribible**    | Subconjunto del catálogo accesible a un gimnasio cuyos ejercicios requieren únicamente equipamiento presente en su inventario. **Es el conjunto sobre el que operan la construcción y la validación de rutinas**   | —                       |
| **Grupo muscular**           | Elemento de la taxonomía canónica de §4.2                                                                                                                                                                          | Músculo, zona, región   |
| **Articulación**             | Elemento de la enumeración de §4.3. Un ejercicio declara las articulaciones que exige                                                                                                                              | —                       |
| **Participación muscular**   | Relación entre un ejercicio y un grupo muscular, primaria o secundaria                                                                                                                                             | Implicación, activación |
| **Patrón de movimiento**     | Clasificación mecánica del ejercicio según §4.7. Base de la equivalencia entre ejercicios y de la estructura de los días de rutina                                                                                 | Tipo de movimiento      |
| **Ejercicio no clasificado** | Ejercicio sin ninguna participación muscular declarada. No aporta volumen a ningún grupo, y esa ausencia se distingue de aportar cero                                                                              | Sin datos               |

##### 1.5 Prescripción

| Término                         | Definición                                                                                                                                                                                       | Sinónimos descartados   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| **Plantilla**                   | Estructura de rutina reutilizable creada por un entrenador, no asociada a ningún alumno                                                                                                          | Modelo, template        |
| **Preset**                      | Funcionalidad opcional: plantilla publicada para uso de otros usuarios del mismo gimnasio. Es un estado de la plantilla y sólo existe si se implementa RF-021                                    | Plantilla pública       |
| **Rutina**                      | Copia independiente de una estructura de rutina, asociada a un alumno concreto                                                                                                                   | Plan, programa          |
| **Rutina propuesta**            | Rutina completa asociada a un alumno que aún no rige porque no fue revisada. El alumno la ve; no puede entrenar bajo ella                                                                        | Borrador, pendiente     |
| **Revisión**                    | Acto por el cual un entrenador examina una rutina propuesta y la aprueba, la modifica y aprueba, o la rechaza. Ninguna rutina rige sin una revisión favorable                                    | Validación, visto bueno |
| **Versión de rutina**           | Estado completo de la estructura de una rutina en un momento dado. Cada adaptación aplicada genera una versión nueva; las anteriores se conservan sin alteración                                 | Revisión, snapshot      |
| **Día de rutina**               | Agrupación ordenada de ejercicios dentro de una versión. No está asociado a un día del calendario                                                                                                | Jornada, día A/B/C      |
| **Serie prescripta**            | Unidad de prescripción: rango de repeticiones objetivo, carga sugerida, descanso y carácter de calentamiento o de trabajo                                                                        | Set planificado         |
| **Serie de trabajo**            | Serie prescripta que no es de calentamiento. Sólo las series de trabajo completadas cuentan para el volumen                                                                                      | Serie efectiva          |
| **Tipo de rutina**              | Clasificación de §4.5 que determina, según la tabla RN-39a, la estructura de días admisible, los esquemas de series y repeticiones y los rangos de descanso                                      | Modalidad, enfoque      |
| **Frecuencia semanal objetivo** | Cantidad de sesiones esperadas por semana declarada por una rutina. Referencia única para el cálculo de adherencia                                                                               | Sesiones objetivo       |
| **Incompatibilidad**            | Condición que impide poner una rutina en vigencia: un ejercicio contraindicado con severidad moderada o severa, de nivel superior al del alumno, o que exige equipamiento ausente del inventario | Conflicto               |

##### 1.6 Ejecución

| Término                    | Definición                                                                                                                                     | Sinónimos descartados  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Sesión**                 | Ocurrencia concreta de entrenamiento de un alumno correspondiente a un día de su rutina. Contiene su propia copia congelada de la prescripción | Entrenamiento, workout |
| **Registro de serie**      | Anotación de una serie dentro de una sesión, que conserva de forma conjunta lo prescripto y lo ejecutado                                       | Set, serie realizada   |
| **Prescripción congelada** | Copia de la prescripción del día realizada al iniciarse la sesión, inmune a toda modificación posterior de la rutina                           | Snapshot de sesión     |
| **Esfuerzo percibido**     | Valoración subjetiva del alumno sobre la dificultad de una serie, de 1 a 10. Opcional                                                          | RPE, RIR               |
| **Sustitución**            | Reemplazo, durante una sesión, de un ejercicio prescripto por otro efectivamente ejecutado                                                     | Cambio de ejercicio    |
| **Sesión diferida**        | Sesión registrada con posterioridad a la fecha en que ocurrió                                                                                  | Registro retroactivo   |
| **Registro atípico**       | Valor dentro del rango admisible pero muy superior al histórico del alumno en ese ejercicio, que requiere confirmación antes de aceptarse      | Outlier                |

##### 1.7 Indicadores

| Término                          | Definición                                                                                                                                                                                               | Sinónimos descartados  |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **Volumen**                      | Trabajo dirigido a un grupo muscular en un período, en **series efectivas**: cada serie de trabajo completada aporta 1,0 al grupo de participación primaria y 0,5 a cada secundario. **No es tonelaje**  | Carga total, tonelaje  |
| **Volumen por ejercicio**        | Cantidad de series de trabajo completadas de un ejercicio en un período. Unidad distinta del volumen por grupo muscular; nunca se comparan                                                               | —                      |
| **Frecuencia**                   | Cantidad de sesiones distintas de un período que estimularon un grupo muscular                                                                                                                           | —                      |
| **Carga máxima estimada**        | Estimación de la carga máxima que un alumno movilizaría una vez en un ejercicio, derivada de sus series registradas. Sinónimo técnico admitido en notas de diseño: _e1RM_                                | Fuerza máxima, 1RM     |
| **Adherencia**                   | Proporción entre las sesiones realizadas y las esperadas, sobre una ventana móvil de cuatro semanas. Mide **si vino**                                                                                    | Constancia, asistencia |
| **Cumplimiento de series**       | Series de trabajo completadas sobre series de trabajo prescriptas                                                                                                                                        | —                      |
| **Cumplimiento de repeticiones** | Repeticiones ejecutadas sobre repeticiones objetivo, en las series de trabajo prescriptas. Mide **qué hizo cuando vino**                                                                                 | Logro                  |
| **Progreso**                     | Evolución conjunta de los indicadores de un alumno en un período: carga máxima estimada por ejercicio, volumen, adherencia, cumplimiento, récords y mediciones corporales. Se usa sólo con esta acepción | Avance, mejora         |
| **Récord personal**              | Mejor marca registrada de un alumno en un ejercicio, en alguno de los tres tipos de §4.8. Es un evento con fecha                                                                                         | PR, mejor marca        |
| **Señal de seguimiento**         | Situación detectada sobre un alumno que requiere atención: estancamiento, caída de adherencia o desbalance                                                                                               | Alerta, flag           |
| **Desbalance**                   | Diferencia entre el volumen recibido por un grupo muscular y su rango de referencia                                                                                                                      | Descompensación        |

##### 1.8 Adaptación

| Término                      | Definición                                                                                                                                                             | Sinónimos descartados       |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **Situación de evolución**   | Clasificación de §4.9 aplicada a un ejercicio o al conjunto de la rutina de un alumno en un período                                                                    | Estado, diagnóstico parcial |
| **Diagnóstico de evolución** | Resultado fechado de la evaluación periódica de un alumno sobre su rutina vigente, que asigna una situación a cada ejercicio y una global                              | Evaluación, análisis        |
| **Propuesta de adaptación**  | Conjunto fechado de ajustes sugeridos sobre la rutina vigente, derivado de un diagnóstico. Nunca se aplica sin revisión                                                | Sugerencia                  |
| **Ajuste**                   | Cada modificación individual de una propuesta, de alguno de los tipos de §4.10, con su criterio motivador y los datos que lo sustentan                                 | Cambio                      |
| **Aprobador**                | Única persona facultada para poner una rutina en vigencia y resolver una propuesta: el entrenador con asignación vigente sobre el alumno. No hay aprobador alternativo | —                           |

##### 1.9 Datos y componentes

| Término                        | Definición                                                                                                                                                                                                                                                                                            |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto del alumno**        | Conjunto estructurado que se entrega como entrada a un componente de decisión: perfil, nivel, objetivo vigente, condiciones físicas vigentes, aptitud, inventario del gimnasio, rutina vigente, indicadores del período y esfuerzo percibido registrado. Se conserva junto a cada resultado producido |
| **Contexto suficiente**        | Contexto que contiene, como mínimo, nivel de experiencia, objetivo vigente y declaración de condiciones físicas (aunque sea la declaración expresa de no tener ninguna). Sin contexto suficiente no se produce ninguna decisión automática                                                            |
| **Componente de decisión**     | Componente que produce valores o estructuras que afectan la prescripción o la gestión. Su salida se valida contra las reglas de compatibilidad y de tipo de rutina, y se somete a revisión humana                                                                                                     |
| **Componente narrativo**       | Componente que sólo redacta texto sobre hechos ya calculados. No introduce valores ausentes de su entrada ni afecta ninguna prescripción                                                                                                                                                              |
| **Dato simulado**              | Registro generado con fines de desarrollo, evaluación o demostración, marcado de forma inequívoca y excluido de toda analítica presentada como real                                                                                                                                                   |
| **Criterio de referencia**     | Regla simple contra la cual se compara el resultado de un componente para determinar si aporta algo                                                                                                                                                                                                   |

##### 1.10 Términos diferidos en la Etapa 1

Estos términos siguen siendo parte del lenguaje del producto, pero **no tienen referente en la Etapa 1** ([baseline de alcance](#baseline)). No usarlos en código, contratos ni interfaz de esta etapa.

| Término                    | Por qué no tiene referente ahora                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **preset**                 | RF-021 diferido. Existe la **plantilla**, que es su objeto subyacente; lo que no existe es publicarla        |
| **candidato de rutina**    | RF-119 diferido. Una generación produce directamente una **rutina propuesta**                                |
| **estimación de riesgo**   | RF-061 a RF-063 retirados del producto ([DD-34](#d11))                            |
| **pauta nutricional**      | RF-075 y RF-108 diferidos con toda la nutrición                                                              |
| **sesión diferida**        | RF-034 diferido                                                                                              |
| **desbloqueo de sesión**   | RF-117 diferido                                                                                              |

De §4.12, los tipos de aviso que quedan sin emisor en esta etapa son los ligados a lo diferido; la enumeración **no se recorta**, porque recortarla obligaría a reabrirla cuando el alcance vuelva.

#### 2. Términos prohibidos

| Término                                       | Motivo                                                                                                                                    |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Historial** (como entidad)                  | El historial son las sesiones ordenadas por fecha                                                                                         |
| **Tonelaje**, **carga total**                 | Métrica no comparable entre ejercicios                                                                                                    |
| **Calorías quemadas**, **puntaje de fitness** | No estimables con la información disponible                                                                                               |
| **Rutina activa**                             | Se usa exclusivamente **vigente**                                                                                                         |
| **Asignar una rutina**                        | Se usa _solicitar_, _revisar_ o _poner en vigencia_. _Asignar_ queda reservado a la relación entrenador–alumno                            |
| **Preset** como entidad separada de plantilla | Es un estado de la plantilla                                                                                                              |
| **Chat**, **mensaje**                         | El sistema tiene comentarios asincrónicos                                                                                                 |
| **Dieta**, **plan alimentario**, **menú**     | El sistema produce una **pauta nutricional**: distribución orientativa de energía y macronutrientes, sin nombrar alimentos. Ver D11/DD-13 |
| **Cumplimiento** sin calificar                | Se dice _cumplimiento de series_ o _cumplimiento de repeticiones_                                                                         |
| **Riesgo de abandono**, **deserción**, **churn** | Retirados del alcance en el replanteo de IA (RF-061 a RF-063 → WON'T, [D11/DD-34](#d11)). No se reintroducen sin reabrir esa decisión |
| **Segmento**, **clúster** (de alumnos)        | El sistema no agrupa alumnos por clustering. Se dice _descripción de perfil_: un texto generado sobre los indicadores ya calculados de un alumno |

#### 3. Unidades y marco temporal

| Magnitud                       | Unidad                               | Precisión                                                                                            |
| ------------------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Carga                          | Kilogramo                            | Dos decimales, redondeo a 0,01 al ingresar. Nunca representación en coma flotante _(nota de diseño)_ |
| Incrementos de carga sugeridos | Kilogramo                            | Múltiplos de 2,50 kg                                                                                 |
| Repeticiones                   | Entero                               | —                                                                                                    |
| Descanso y duración            | Segundo                              | Entero                                                                                               |
| Esfuerzo percibido             | Entero de 1 a 10                     | —                                                                                                    |
| Peso corporal                  | Kilogramo                            | Un decimal                                                                                           |
| Perímetros                     | Centímetro                           | Un decimal                                                                                           |
| Volumen                        | Series efectivas                     | Un decimal                                                                                           |
| Energía                        | Kilocaloría                          | Entero                                                                                               |
| Proteína                       | Gramo por kilogramo de peso corporal | Un decimal                                                                                           |

- **Instante:** se almacena en tiempo universal coordinado y se presenta en la zona horaria del gimnasio.
- **Día:** delimitado por la zona horaria del gimnasio, no por la del dispositivo.
- **Semana:** de lunes a domingo inclusive. Definición única para toda agregación semanal.
- **Ventana móvil de adherencia:** cuatro semanas completas hacia atrás desde el instante de cálculo.
- **Período de diagnóstico:** seis semanas completas hacia atrás desde el instante de cálculo.

#### 4. Enumeraciones cerradas

Estas listas son el vocabulario del sistema. Ninguna admite valores fuera de ella sin modificar este documento.

##### 4.1 Equipamiento — 22 valores

`PESO_CORPORAL` · `BARRA` · `DISCOS` · `MANCUERNAS` · `PESAS_RUSAS` · `BANCO_PLANO` · `BANCO_INCLINADO` · `BANCO_DECLINADO` · `RACK_SENTADILLA` · `JAULA_POTENCIA` · `PRENSA_PIERNAS` · `POLEA_ALTA` · `POLEA_BAJA` · `MAQUINA_PECHO` · `MAQUINA_ESPALDA` · `MAQUINA_HOMBRO` · `MAQUINA_CUADRICEPS` · `MAQUINA_ISQUIOTIBIALES` · `MAQUINA_GEMELOS` · `BARRA_DOMINADAS` · `PARALELAS` · `BANDAS_ELASTICAS`

`PESO_CORPORAL` se considera presente en todo inventario y no se declara.

##### 4.2 Grupos musculares — 17 valores

**Cadena anterior:** `PECTORAL` · `DELTOIDES_ANTERIOR` · `DELTOIDES_LATERAL` · `BICEPS` · `ANTEBRAZO` · `ABDOMINALES` · `OBLICUOS` · `CUADRICEPS` · `ADUCTORES`

**Cadena posterior:** `DORSAL` · `TRAPECIO` · `DELTOIDES_POSTERIOR` · `TRICEPS` · `ERECTORES_LUMBARES` · `GLUTEO` · `ISQUIOTIBIALES` · `GEMELOS`

`[S]` La granularidad de esta lista es una convención de modelado adoptada por este proyecto, no un estándar anatómico. Es la unidad de agregación del volumen y la unidad de pintado de la representación muscular; cambiarla obliga a rehacer la curación del catálogo. Registrado en D12/§1.

##### 4.3 Articulaciones — 8 valores

`HOMBRO` · `CODO` · `MUNECA` · `COLUMNA_CERVICAL` · `COLUMNA_LUMBAR` · `CADERA` · `RODILLA` · `TOBILLO`

**Zona corporal** = unión de §4.2 y §4.3, 25 valores en total.

##### 4.4 Nivel — 3 valores, ordenados

`PRINCIPIANTE` < `INTERMEDIO` < `AVANZADO`

Se aplica tanto al nivel de experiencia del alumno como al nivel de dificultad del ejercicio, con el mismo orden.

##### 4.5 Objetivo del alumno y tipo de rutina — 4 valores comunes

`FUERZA` · `HIPERTROFIA` · `RESISTENCIA_MUSCULAR` · `ACONDICIONAMIENTO_GENERAL`

Objetivo y tipo de rutina comparten enumeración deliberadamente: hace que la verificación de correspondencia de RN-40 sea una comparación y no un juicio. `ACONDICIONAMIENTO_GENERAL` como tipo de rutina es compatible con cualquier objetivo.

`READAPTACION` fue evaluado y excluido: no tiene objetivo de alumno equivalente y arrastra implicancias clínicas que el sistema declara fuera de alcance. Ver D11/DD-27.

##### 4.6 Severidad de una condición física — 3 valores

`LEVE` — advierte, no impide · `MODERADA` — impide · `SEVERA` — impide

##### 4.7 Patrón de movimiento — 9 valores

`EMPUJE_HORIZONTAL` · `EMPUJE_VERTICAL` · `TRACCION_HORIZONTAL` · `TRACCION_VERTICAL` · `DOMINANTE_RODILLA` · `DOMINANTE_CADERA` · `CORE` · `AISLAMIENTO_SUPERIOR` · `AISLAMIENTO_INFERIOR`

##### 4.8 Tipo de récord personal — 3 valores

`CARGA_MAXIMA_ESTIMADA` — mayor carga máxima estimada alcanzada
`CARGA_MOVILIZADA` — mayor carga usada en una serie de trabajo completada
`REPETICIONES` — mayor cantidad de repeticiones en una serie de trabajo completada. **Es el único aplicable a ejercicios cuya carga ejecutada es cero**

##### 4.9 Situación de evolución — 5 valores

`DATOS_INSUFICIENTES` · `SOBREEXIGENCIA` · `PROGRESION_ADECUADA` · `ESTIMULO_INSUFICIENTE` · `ESTANCAMIENTO`

Enumerados en el orden de precedencia con que se evalúan (RN-79a).

##### 4.10 Tipo de ajuste — 5 valores

`CARGA` — modifica la carga sugerida de un ejercicio
`VOLUMEN` — modifica la cantidad de series de un ejercicio
`ESQUEMA` — modifica el rango de repeticiones o el descanso
`SUSTITUCION` — reemplaza un ejercicio por otro
`ESTRUCTURA` — modifica la composición de días o la frecuencia semanal objetivo

##### 4.11 Tipo de medición corporal — 6 valores

`PESO_CORPORAL` · `PERIMETRO_CINTURA` · `PERIMETRO_CADERA` · `PERIMETRO_BRAZO` · `PERIMETRO_MUSLO` · `PERIMETRO_PECHO`

##### 4.12 Tipo de aviso — 9 valores

`RUTINA_PROPUESTA_PENDIENTE` · `RUTINA_EN_VIGENCIA` · `RUTINA_RECHAZADA` · `RUTINA_AJUSTADA` · `PROPUESTA_PENDIENTE` · `RECORD_ALCANZADO` · `SENAL_DETECTADA` · `INCOMPATIBILIDAD_SOBREVENIDA` · `APTITUD_POR_VENCER`


---

<a id="po-alcance-ia-generativa"></a>

### Entregable al Product Owner — Alcance de la IA generativa

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/deliverable PO/alcance-ia-generativa.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `DELIVERABLE-PO-GENERATIVE-AI`

|             |                                          |
| ----------- | ---------------------------------------- |
| **Para**    | Product Owner                            |
| **Versión** | 2.1                                     |
| **Fecha**   | 2026-08-28                              |
| **Alcance** | Sólo la IA generativa. La parte predictiva (sugerir carga sesión a sesión, proyectar progreso a futuro) no entra en este entregable. |

Este documento resume qué resuelve la IA del sistema, cómo funciona a grandes rasgos y qué nos comprometemos a entregar. **El alcance comprometido es un piso: puede ensancharse hacia el final del proyecto.**

---

#### 1. Qué resuelve la IA

Toda la capacidad de decisión del sistema la resuelve un modelo de lenguaje (IA generativa). A partir del contexto del alumno —perfil, objetivo, condiciones físicas, nivel, equipamiento del gimnasio e historial de entrenamiento— el sistema:

- **Entiende un pedido en lenguaje natural.** El entrenador o el alumno describen lo que necesitan con sus palabras y el sistema lo traduce a parámetros concretos, que se muestran para confirmar antes de usarlos.
- **Determina el tipo de rutina** adecuado según el perfil y el objetivo.
- **Arma la rutina completa** sobre los ejercicios que el gimnasio efectivamente tiene disponibles.
- **Verifica la compatibilidad:** revisa que ningún ejercicio choque con una condición física del alumno, supere su nivel o requiera equipamiento que el gimnasio no tiene.
- **Explica en lenguaje claro** los criterios con los que se armó o ajustó una rutina.
- **Ofrece alternativas** cuando un ejercicio no se puede hacer, dentro de lo compatible con el alumno.

---

#### 2. Qué garantiza el sistema alrededor del modelo

El modelo no decide solo. Cuatro garantías lo rodean, y ninguna depende de que el modelo se comporte bien:

- **La revisión del entrenador.** Ninguna rutina llega vigente a un alumno sin que un entrenador con asignación vigente la haya aprobado. Sin excepciones, cualquiera sea el origen de la rutina.
- **La compatibilidad se verifica en código, no en el modelo.** Que un ejercicio esté contraindicado por una condición física, exceda el nivel del alumno o requiera equipamiento que el gimnasio no tiene, lo determina una regla escrita y auditable, antes de construir la propuesta y otra vez antes de presentarla.
- **Los textos no inventan números.** Un texto generado no puede contener un valor numérico que no esté en los datos que recibió. Es exigible al 100 % y se verifica de forma automática.
- **Una salida inválida no se muestra.** Se reintenta una vez; si vuelve a fallar, la capacidad se declara no disponible y no se presenta nada.

---

#### 3. Fuera de alcance asegurado

**IA predictiva:** sugerir la carga de la próxima serie y proyectar la trayectoria de fuerza y mediciones. Es otra técnica (modelos de series temporales) y se trataría aparte.

**Estimación de riesgo de abandono:** retirada del producto. Requiere meses de actividad sobre cientos de usuarios para tener sustento, y el proyecto no va a tener esos datos.

---

#### 3.1 Qué cambió con el recorte de alcance del 2026-09-01, y qué hace falta confirmar

El equipo votó el alcance de esta etapa y el resultado toca dos cosas de este documento. Ver el [baseline de alcance](#baseline).

**Lo que hay que confirmar con el Product Owner:**

- **La interpretación de lenguaje natural (§1, primer punto) obtuvo 3 votos de 8.** Está comprometida en este documento y por eso se conserva en el alcance, pero el equipo no la quiere en esta etapa. La alternativa es cargar los mismos parámetros por formulario. **Es una decisión del Product Owner: o libera el compromiso, o se construye pese al voto.**

**Lo que hay que saber aunque no requiera decisión:**

- **Ya no hay rutinas predefinidas de contingencia.** El equipo resolvió generar todas las rutinas desde cero. Si el servicio del modelo no está disponible, la única vía que queda es que un entrenador arme y asigne una rutina a mano. **Un alumno nuevo en un gimnasio que todavía no tiene ninguna rutina cargada, con el servicio caído, no recibe plan.** La forma de evitarlo es operativa: cargar dos o tres rutinas base al dar de alta cada gimnasio.

---

#### 4. Cómo funciona

- **Un solo modelo de lenguaje**, alojado en la infraestructura de la Universidad/Polo de San Francisco o en la nube.
- Corre **como parte del backend del sistema**.
- El modelo se puede cambiar o actualizar sin tocar el resto del sistema.
- Cada respuesta del modelo se **valida en formato** antes de usarse; si no cumple, se reintenta una vez.
- **Ninguna rutina llega al alumno sin que el entrenador la revise y la apruebe.** Esa revisión humana es la garantía del sistema, cualquiera sea el origen de la rutina.
- El modelo **nunca** pone una rutina en vigencia por su cuenta y no da indicaciones médicas.
- Si el modelo no está disponible en un momento dado, la creación y adaptación de rutinas queda temporalmente fuera de servicio y el sistema lo informa; todo lo demás —registro de sesiones, consulta de rutinas e indicadores, revisión del entrenador— sigue funcionando con normalidad. Los mismos parámetros se pueden cargar por formulario mientras tanto.

---

#### 5. Cómo se verifica

- Un conjunto fijo de casos de prueba que se corre antes de cambiar cualquier configuración del modelo.
- Se mide: que los textos nunca mencionen un número que no esté en los datos de origen y que las respuestas tengan el formato esperado.

---

#### 6. Riesgos y supuestos

- **En hardware modesto, la respuesta puede tardar más de lo previsto**, sobre todo para rutinas largas. Alternativas: usar un modelo más chico o ampliar el tiempo aceptable para generar una rutina.
- **Mantener ese servidor** (actualizaciones, monitoreo) hay que acordarlo con el Polo Educativo. Caso de un servidor en la nube hay que evaluar costos y monitorearlo.
- **El modelo puede proponer una rutina con errores o incompatibilidades.** Lo cubre la revisión obligatoria del entrenador; medimos la tasa de rechazo para detectarlo temprano.


---

<a id="parte-iii"></a>

## Parte III — Dominio

<a id="d3"></a>

### D3 — Actores, roles y permisos

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/domain/actors-roles-permissions.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D3`

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.3        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | D1, D2     |

**Cambios de la v1.0:** se agrega el proveedor del sistema como actor no aplicativo · filas de invitación, inventario, aviso, consentimiento y desbloqueo de sesión, que faltaban · se resuelve quién registra la aptitud · se elimina el equipamiento declarado por el alumno · referencia cruzada corregida (apuntaba a RN-58 en lugar de RN-106).

**Cambios de la v2.0:** el alumno gana escritura sobre el **candidato** de rutina —no sobre la rutina propuesta— dentro de las operaciones de D5/§5.2. Ver D11/DD-33.

**Cambios de la v2.2 (replanteo de IA, [D11/DD-34](#d11)):** se retiran las filas "Estimación de riesgo de abandono" (RF-061 a RF-063 → WON'T) y "Segmentación de perfiles" de la matriz de permisos; la descripción de perfil (RF-064) la produce la capa generativa de forma efímera y se muestra a entrenador y administrador junto a los indicadores.

**Cambios de la v2.3 ([baseline de alcance](#baseline)).** Las reglas de acceso RA-01 a RA-10 **no cambian**: son el núcleo de seguridad del sistema y ninguna depende de algo diferido. Quedan sin sujeto en la Etapa 1 las filas de la matriz correspondientes a comentarios (RF-039), pauta nutricional (RF-075, RF-108), panel analítico del gimnasio (RF-068) y solicitud de rutina por el alumno (RF-025).

**Dos consecuencias del recorte sobre permisos que conviene no perder de vista:**

- **RA-07b sigue intacta y ahora es más simple de verificar.** «Ningún origen exime de la revisión» tenía tres orígenes; ahora tiene dos —plantilla del entrenador y rutina generada—, porque el preset elegido por el alumno se difirió. La regla no se relaja: se reduce su superficie.
- **RF-005 y RF-069 entraron al alcance como dependencia, no por votación** (2 y 4 votos de 8). Es el resultado más delicado de la votación: la autorización por recurso y el aislamiento por gimnasio son lo que impide que cualquiera lea los datos de salud de cualquiera, y quedaron por debajo del corte. Están dentro del alcance y en banda N1 porque sin ellos el sistema no es entregable, no porque el equipo los haya priorizado.

---

#### 1. Actores

##### 1.0 Proveedor del sistema — actor no aplicativo

|                    |                                                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Qué hace**       | Aprovisiona un gimnasio afiliado: lo crea con su zona horaria y crea su primer administrador                   |
| **Dónde**          | **Fuera de la aplicación.** No es un rol, no inicia sesión, no aparece en ninguna pantalla                     |
| **Por qué existe** | Sin él ningún gimnasio puede arrancar: el alta es por invitación y nadie puede emitir la primera. Ver D4/PD-08 |

Se lo declara como actor porque ejecuta una operación indispensable. Modelarlo como rol de la aplicación reintroduciría el superadministrador multi-gimnasio, que está fuera de alcance.

##### 1.1 Alumno

|                |                                                                                                                                                                                                                                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objetivo**   | Entrenar con un plan que se mantenga adecuado a su estado, y saber si progresa                                                                                                                                                                                                                                                                         |
| **Consulta**   | Su rutina vigente y su rutina propuesta, su historial de sesiones, sus indicadores, sus mediciones, el catálogo, las propuestas de adaptación que le afectan y su estado de resolución, sus avisos                                                                                                                                                     |
| **Modifica**   | Su perfil, objetivo, condiciones físicas, aptitud, mediciones; sus sesiones dentro del plazo de corrección; comentarios propios. **Puede solicitar** una rutina generada y **moldear el candidato** antes de enviarlo a revisión, dentro de las operaciones de D5/§5.2; al confirmarlo se crea la rutina propuesta. Puede elegir un preset sólo si se implementa RF-021 |
| **Nunca hace** | Poner en vigencia una rutina, resolver una propuesta de adaptación, modificar su rutina vigente **ni su rutina propuesta una vez confirmada**, fijar series, repeticiones, descansos o cargas, declarar equipamiento                                                                                                                                   |
| **Nunca ve**   | La descripción de perfil que se presenta al entrenador y al administrador; información de otros alumnos                                                                                                                                                                                                                                                |

**Nota (v2.2):** la fila "no ve su estimación de riesgo de abandono" y la decisión asociada a DD-17 se retiran al pasar RF-061 a RF-063 a WON'T ([D11/DD-34](#d11)). El alumno sigue viendo sus indicadores objetivos de adherencia y cumplimiento.

##### 1.2 Entrenador

|                         |                                                                                                                                                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objetivo**            | Que los alumnos de su cartera entrenen con la prescripción correcta, sin tener que revisarlos uno por uno                                                                                                       |
| **Función indelegable** | Es la puerta: **ninguna rutina rige para un alumno suyo sin su revisión**, cualquiera sea su origen                                                                                                             |
| **Consulta**            | Su cartera ordenada por urgencia, la ficha integral de cada alumno asignado, lo pendiente de su revisión, sus plantillas, el catálogo, sus indicadores agregados de cartera, sus avisos                         |
| **Modifica**            | Sus plantillas; las rutinas de sus alumnos asignados; su perfil profesional; comentarios; ejercicios propios del gimnasio. Resuelve propuestas. Emite invitaciones con rol ALUMNO. Desbloquea sesiones a pedido |
| **Nunca ve**            | Alumnos sin asignación vigente con él; información de otro gimnasio                                                                                                                                             |
| **Nunca hace**          | Modificar el inventario del gimnasio, registrar la aptitud de un alumno, otorgar roles distintos de ALUMNO                                                                                                      |

Un entrenador que quiera entrenar necesita **otro** entrenador asignado: no hay excepción a la puerta ni autoasignación (RN-22, RN-22a). Si es el único entrenador del gimnasio, no puede tener rutina vigente y el sistema lo señala al administrador. Ver D11/DD-28.

##### 1.3 Administrador

|                                              |                                                                                                                                                                                     |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objetivo**                                 | Que el gimnasio tenga las personas, los roles, las asignaciones y el **inventario** correctos, y entender la salud agregada del gimnasio                                            |
| **Función con efecto sobre la prescripción** | Mantiene el inventario de equipamiento, que determina el catálogo prescribible de todo el gimnasio. No es un rol administrativo puro                                                |
| **Consulta**                                 | Usuarios, roles e invitaciones de su gimnasio, asignaciones vigentes e históricas, inventario, panel analítico agregado, registro de auditoría, catálogo del gimnasio               |
| **Modifica**                                 | Invitaciones; roles; suspensión y reactivación de cuentas; asignaciones; inventario; estado de membresía; aptitud; curación del catálogo. Solicita el recálculo de las estimaciones |
| **Nunca ve**                                 | El detalle de sesiones, mediciones corporales ni condiciones físicas de un alumno individual. Ver §4                                                                                |

#### 2. Matriz de permisos

**Convención:** `P` propio · `A` alumnos con asignación vigente · `G` todo el gimnasio · `—` sin acceso · `L` leer · `E` escribir

| Recurso / operación                              | Alumno                       | Entrenador                  | Administrador           |
| ------------------------------------------------ | ---------------------------- | --------------------------- | ----------------------- |
| **Invitación**                                   | —                            | `L/E` G, sólo rol ALUMNO    | `L/E` G                 |
| **Inventario del gimnasio**                      | `L`                          | `L`                         | `L/E` G                 |
| Consentimiento propio                            | `L/E` P                      | `L/E` P                     | `L/E` P                 |
| Perfil propio                                    | `L/E` P                      | `L/E` P                     | `L/E` P                 |
| Perfil de alumno (edad, nivel, días disponibles) | `L/E` P                      | `L` A                       | `L` G                   |
| Objetivo e historial de objetivos                | `L/E` P                      | `L` A                       | —                       |
| Condición física e historial                     | `L/E` P                      | `L` A                       | —                       |
| Aptitud                                          | `L/E` P                      | `L` A                       | `L/E` G                 |
| Medición corporal                                | `L/E` P                      | `L` A                       | —                       |
| Estado de membresía                              | `L` P                        | `L` A                       | `L/E` G                 |
| Catálogo base                                    | `L`                          | `L`                         | `L`                     |
| Catálogo del gimnasio                            | `L`                          | `L` + `E` propios           | `L` + curar G           |
| Plantilla                                        | —; `L` presets si existe RF-021 | `L/E` propias; `L` presets si existe RF-021 | `L` G      |
| Rutina propuesta y rutina vigente                | `L` P                        | `L/E` A                     | —                       |
| ~~**Candidato** de rutina~~ ⏸ diferido (RF-119)  | —                            | —                           | —                       |
| Versión histórica de rutina                      | `L` P                        | `L` A                       | —                       |
| **Solicitar** una rutina                         | `E` P                        | `E` A                       | —                       |
| **Poner en vigencia** una rutina                 | **—**                        | `E` A                       | —                       |
| Sesión y registros de serie                      | `L/E` P                      | `L` A                       | —                       |
| **Desbloquear** una sesión bloqueada             | **—**                        | `E` A                       | —                       |
| Indicadores individuales                         | `L` P                        | `L` A                       | —                       |
| Diagnóstico de evolución                         | `L` P                        | `L` A                       | —                       |
| Propuesta de adaptación: ver                     | `L` P                        | `L` A                       | —                       |
| Propuesta de adaptación: **resolver**            | **—**                        | `E` A                       | —                       |
| Historial de adaptaciones                        | `L` P                        | `L` A                       | —                       |
| Comentario sobre sesión o rutina                 | `L/E` P                      | `L/E` A                     | —                       |
| Pauta nutricional orientativa                    | `L` P                        | `L` A                       | —                       |
| **Aviso**                                        | `L/E` P                      | `L/E` P                     | `L/E` P                 |
| ~~Estimación de riesgo de abandono~~ (retirada v2.2) | —                        | —                           | —                       |
| Descripción de perfil (efímera, generativa)      | —                            | `L` A                       | `L` G                   |
| Panel agregado de cartera                        | —                            | `L` P                       | `L` G                   |
| Panel analítico del gimnasio                     | —                            | —                           | `L` G                   |
| Gestión de usuarios y roles                      | —                            | —                           | `E` G                   |
| Gestión de asignaciones                          | —                            | —                           | `E` G                   |
| Registro de auditoría                            | —                            | —                           | `L` G                   |
| Solicitar recálculo de estimaciones              | —                            | —                           | `E` G                   |
| Exportar datos propios / solicitar baja          | `E` P                        | `E` P                       | `E` P                   |
| **Aprovisionar un gimnasio**                     | —                            | —                           | **—** (proveedor, §1.0) |

#### 3. Reglas de acceso

**RA-01 — Doble filtro.** Toda operación se autoriza en dos pasos y en este orden: (1) ¿el rol admite esta operación?; (2) ¿este recurso concreto le pertenece o le está asignado? `[F: RF-005]`

**RA-02 — Alcance por gimnasio.** Ninguna operación devuelve información de un gimnasio distinto del de su actor. La única excepción es el catálogo base. `[F: RF-069, RF-100]`

**RA-03 — Vigencia de la asignación.** El acceso del entrenador existe si y sólo si hay asignación vigente en el instante de la consulta. `[F: RF-066]`

**RA-04 — Efecto inmediato del fin de la asignación.** Al finalizar, el acceso cesa en ese instante y las operaciones en curso no se completan. Ver D10/CB-31.

**RA-05 — Acumulación de roles.** Un actor con varios roles obtiene la unión de los permisos de cada uno, evaluados de forma independiente. No hay elevación: tener el rol de entrenador no otorga acceso a alumnos no asignados aunque el actor sea además administrador.

**RA-06 — El administrador no accede al detalle individual sensible.** Su acceso es de gestión y agregación. No lee sesiones, mediciones corporales ni condiciones físicas de un alumno concreto. Sí registra la aptitud, porque la constancia se presenta en el gimnasio y alguien tiene que cargarla, pero sólo su vigencia, no su contenido clínico. Ver D11/DD-22.

**RA-07 — El entrenador es la única puerta.** El facultado para poner una rutina en vigencia y para resolver una propuesta es **exclusivamente** el entrenador con asignación vigente. No hay aprobador alternativo: sin entrenador vigente, la rutina permanece propuesta y la propuesta permanece pendiente. `[F: RF-091 + decisión del cliente]` Ver D11/DD-25.

**RA-07b — Ningún origen exime de la revisión.** Plantilla del entrenador y rutina generada —y preset elegido por el alumno si se implementa RF-021— entran por la misma puerta. ✎ v2.3: eran tres orígenes garantizados; el preset pasó a alcance opcional. **La regla no se relaja: se reduce su superficie.**

**RA-08 — Datos propios siempre accesibles.** Ningún estado —membresía vencida, aptitud vencida, cuenta suspendida— priva a un usuario de leer y exportar sus propios datos.

**RA-09 — La invitación determina los roles.** Un usuario no puede otorgarse roles ni cambiar de gimnasio. Los roles del usuario creado son exactamente los de su invitación. `[F: RN-02c]`

**RA-10 — Un entrenador sólo invita alumnos.** Y el alumno resultante queda asignado a él. `[F: RN-02d]`

#### 4. Evolución de los permisos cuando cambia una relación

| Evento                                          | Efecto inmediato                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Se emite una invitación                         | No otorga ningún acceso hasta usarse. Puede revocarse mientras no se haya usado                                                                                                                                                                                                                                                                 |
| Se crea una asignación                          | El entrenador gana lectura del alumno y escritura sobre sus rutinas. Lo pendiente de revisión pasa a corresponderle. `[F: RF-109]`                                                                                                                                                                                                              |
| Finaliza la asignación                          | El entrenador pierde todo acceso al alumno, **incluido el histórico que supervisó**. La rutina vigente permanece vigente y el alumno puede seguir entrenando; lo que se detiene es la aprobación de cambios. Lo pendiente queda BLOQUEADO y el sistema lo señala al administrador. Los avisos del saliente sobre ese alumno se cierran (RN-114) |
| Se reasigna a otro entrenador                   | Equivale a finalizar la anterior e iniciar la nueva en el mismo instante. No hay intervalo con dos entrenadores vigentes ni con ninguno. Todo lo pendiente pasa al entrante                                                                                                                                                                     |
| Un alumno pierde el rol de alumno               | Sus datos permanecen; deja de poder iniciar sesiones. Sus sesiones anteriores siguen contando para la analítica agregada                                                                                                                                                                                                                        |
| Un entrenador pierde el rol de entrenador       | Sus asignaciones vigentes finalizan en ese instante. Sus plantillas publicadas permanecen utilizables. Sus alumnos conservan su rutina vigente pero no pueden recibir ninguna rutina nueva ni ninguna adaptación hasta ser reasignados                                                                                                          |
| Un administrador pierde el rol de administrador | Se rechaza si es el último administrador activo del gimnasio (RN-03a)                                                                                                                                                                                                                                                                           |
| Se suspende una cuenta                          | No puede autenticarse. Sus datos y sus asignaciones permanecen: la suspensión es reversible y no destruye relaciones                                                                                                                                                                                                                            |
| Se da de baja una cuenta                        | Anonimización, no borrado. Ver D5/RN-106 y D10/CB-38                                                                                                                                                                                                                                                                                            |
| Cambia el inventario del gimnasio               | No altera permisos, pero recalcula el catálogo prescribible y dispara la reevaluación de las rutinas vigentes afectadas (RN-117)                                                                                                                                                                                                                |

**Sobre la pérdida de acceso al histórico.** Que el entrenador pierda el acceso a los datos de un alumno que sí supervisó es incómodo y correcto: el fundamento del acceso es la relación vigente, no el mérito histórico. La consecuencia asumida es que el indicador de carga por entrenador del panel del gimnasio se calcula sobre información agregada y no requiere que el entrenador conserve visibilidad individual. Ver D11/DD-23.


---

<a id="d4"></a>

### D4 — Modelo de dominio

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/domain/domain-model.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D4`

|                |                                              |
| -------------- | -------------------------------------------- |
| **Versión**    | 2.2                                          |
| **Fecha**      | 2026-09-01                                   |
| **Estado**     | Normativo. Congelar antes de escribir código |
| **Depende de** | D1, D2, D3                                   |

**Cambios de la v1.0:** entidades `Invitacion` e `InventarioGimnasio` · `EquipamientoDisponible` eliminada (el equipamiento es del gimnasio) · `EjercicioArticulacion` agregada, sin la cual la compatibilidad no era calculable · `EjercicioRutina` gana el estado de compatibilidad que cuatro reglas exigían y el modelo no soportaba · `Ejercicio` gana el nivel de dificultad como atributo tipado · dos referencias cruzadas corregidas · PD-07 nuevo.

**Cambios de la v2.1 (replanteo de IA, [D11/DD-34](#d11)):** `ScoreRiesgo` y `SegmentoPerfil` quedan **derogadas** — el riesgo de abandono se retira del alcance (RF-061 a RF-063 → WON'T) y la descripción de perfil (RF-064) la produce la capa generativa de forma efímera. `EvaluacionComponente` se conserva (RF-121, RF-122).

**Cambios de la v2.2 ([baseline de alcance](#baseline)).** El núcleo del modelo **no cambia**: el eje `RutinaAsignada → VersionRutina → DiaRutina → EjercicioRutina → SeriePrescripta`, la sesión autocontenida, `EjercicioMusculo`, `EjercicioArticulacion` y las 23 restricciones de integridad quedan intactos. Lo que cambia es lo que la Etapa 1 no necesita persistir:

| Elemento                                                              | Estado en la Etapa 1                                                                                    |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `Comentario`                                                          | ⏸ No se crea. Diferida con RF-039 (1 voto de 8)                                                          |
| `PlantillaRutina.publicada`                                           | ⏸ No se crea en la Etapa 1. RF-021 es alcance opcional (COULD, 1 voto de 8): la plantilla existe, la publicación sólo se agrega si se implementa |
| `RutinaAsignada.origen`                                               | ✎ Se reduce a `PLANTILLA_ENTRENADOR` y `GENERADA`. `PRESET_ELEGIDO_POR_ALUMNO` sólo existe si se implementa RF-021 (ver §2.4) |
| `PerfilAlumno.nivel de actividad`                                     | ⏸ No se crea. Sólo alimentaba la estimación energética de RF-012 (2/8)                                    |
| `SesionEntrenamiento.es diferida` y `.desbloqueada hasta`             | ⏸ No se crean. Diferidos con RF-034 (2/8) y RF-117                                                       |
| `RegistroAuditoria`                                                   | ✎ Se acota a las operaciones de RF-038, RF-066, RF-091 y RF-114. RF-097 general queda diferido            |
| `ScoreRiesgo`, `SegmentoPerfil`                                       | Derogadas en la v2.1; la votación lo confirma (1, 0 y 0 votos)                                            |

**Añadir una columna después es barato; quitarla después de tener datos, no.** Por eso lo diferido no se crea ahora: los repositorios están en andamiaje y ninguna migración se ejecutó todavía.

##### Índices exigidos desde la primera migración

No son optimización posterior: son lo que sostiene RNF-01 y RNF-36, y definirlos después obliga a una migración sobre tablas con datos.

| Índice                                                     | Qué sostiene                                             |
| ---------------------------------------------------------- | ---------------------------------------------------------- |
| `RegistroSerie(sesion, orden)` **único**                   | RI-10 e idempotencia del registro (RF-104, RNF-13)        |
| `RegistroSerie(ejercicio_ejecutado, sesion)`               | Volumen por grupo muscular y carga máxima estimada        |
| `SesionEntrenamiento(alumno, fecha_de_ocurrencia)`         | Adherencia, historial y diagnóstico                       |
| `RutinaAsignada(alumno, estado)` parcial sobre VIGENTE y PROPUESTA | RI-06 y la cartera priorizada                     |
| `AsignacionEntrenador(alumno)` parcial sobre `hasta IS NULL` | RI-05 y **toda decisión de autorización** (RA-01, RA-03) |
| `CondicionFisica(perfil)` parcial sobre `hasta IS NULL`    | Verificación de compatibilidad en cada puesta en vigencia |
| `Ejercicio(gimnasio)` admitiendo `NULL`                    | Catálogo base frente a catálogo propio (PD-04 del modelo) |

##### Aislamiento multi-gimnasio: en el modelo, no en el motor

El ámbito por gimnasio (RF-069, RA-02) se resuelve con la columna `gimnasio` en toda entidad raíz más RI-01, **no con `row-level security` de PostgreSQL**. Una segunda fuente de autorización dentro del motor habría que mantenerla sincronizada con la de la aplicación, y el proyecto no tiene capacidad para operar dos. La compensación es RNF-14: una prueba automatizada por cada operación que reciba un identificador de alumno.

---

#### 1. Estructura general

```
Gimnasio ──< InventarioGimnasio >── (equipamiento, §4.1 de D2)
 │
 ├─< Invitacion ──▶ (produce) ──▶ Usuario
 │
 ├─< Usuario ──< RolUsuario
 │     ├── PerfilAlumno ──< Objetivo(vigencia)
 │     │        ├─< CondicionFisica(vigencia, zona corporal, severidad)
 │     │        ├─< Aptitud
 │     │        └─< MedicionCorporal
 │     ├── PerfilEntrenador
 │     ├─< Consentimiento
 │     └─< AsignacionEntrenador (alumno ─ entrenador, vigencia)
 │
 ├─< PlantillaRutina ──< DiaPlantilla ──< EjercicioPlantilla ──< SeriePrescriptaPlantilla
 │        │
 │        │  (copia profunda al solicitar)
 │        ▼
 │   RutinaAsignada ──< RevisionRutina
 │        ├──< VersionRutina ──< DiaRutina ──< EjercicioRutina ──< SeriePrescripta
 │        │         ▲
 │        │         │ (una propuesta aceptada genera una versión)
 │        │   PropuestaAdaptacion ──< AjustePropuesto
 │        │         ▲
 │        │   DiagnosticoEvolucion ──< DiagnosticoEjercicio
 │        ▼
 │   SesionEntrenamiento ──< RegistroSerie   [prescripto + ejecutado en la misma fila]
 │        └─< Comentario
 │
 └─< Ejercicio (del gimnasio)          CATÁLOGO BASE (global, gimnasio = null)
            └────────────── Ejercicio ──< EjercicioMusculo   >── GrupoMuscular
                                      ──< EjercicioArticulacion >── Articulacion
                                      ──< EjercicioEquipamiento

   RecordPersonal · Aviso
   RegistroAuditoria · EvaluacionComponente
   [derogadas v2.2: ScoreRiesgo, SegmentoPerfil]
```

#### 2. Entidades

##### 2.1 Ámbito, identidad y alta

| Entidad                | Atributos relevantes                                                                                          | Notas                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Gimnasio**           | nombre, zona horaria, estado de afiliación, activo                                                            | Creado por aprovisionamiento (RF-115), no por ningún rol de la aplicación. Su zona horaria define el día y la semana de todos sus usuarios |
| **InventarioGimnasio** | gimnasio, equipamiento (§4.1 de D2), presente                                                                 | N:M contra la enumeración cerrada. **Determina el catálogo prescribible del gimnasio.** Ver PD-07                                          |
| **Invitacion**         | gimnasio, correo destinatario, roles ofrecidos, emitida por, emitida en, vence en, estado, usuario resultante | Única vía de alta. Ver PD-08                                                                                                               |
| **Usuario**            | gimnasio, correo, nombre, estado, fecha de alta, invitación de origen                                         | El correo es único **dentro del gimnasio**: una misma persona puede ser alumna de dos gimnasios. Ver DD-24                                 |
| **RolUsuario**         | usuario, rol ∈ {ALUMNO, ENTRENADOR, ADMINISTRADOR}                                                            | Conjunto, no valor único. Un usuario tiene ≥1                                                                                              |
| **Consentimiento**     | usuario, tipo, otorgado, instante, texto aceptado                                                             | Se conserva el texto exacto que se aceptó, no una referencia a la versión actual                                                           |

##### 2.2 Estado del alumno

| Entidad                  | Atributos relevantes                                                                                                                         | Cardinalidad                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **PerfilAlumno**         | usuario, fecha de nacimiento, sexo, altura, nivel de experiencia (§4.4), días semanales disponibles, estado de membresía, nivel de actividad | 1:1 con Usuario con rol ALUMNO. `nivel de actividad` alimenta la estimación energética de RF-012                                              |
| **Objetivo**             | perfil, tipo (§4.5), desde, hasta                                                                                                            | 1:N. **Como máximo uno** con `hasta = null`; ninguno antes de la primera declaración                                                          |
| **CondicionFisica**      | perfil, zona corporal (§4.2 ∪ §4.3), severidad (§4.6), descripción libre, desde, hasta                                                       | 1:N. Varias pueden estar vigentes a la vez. **La zona corporal y la severidad son tipadas**: son las que hacen calculable la contraindicación |
| **Aptitud**              | perfil, fecha de emisión, fecha de vencimiento, observación, cargada por                                                                     | 1:N. La vigente es la de vencimiento más lejano no superado. `cargada por` admite al alumno o a un administrador                              |
| **MedicionCorporal**     | perfil, tipo (§4.11), valor, fecha                                                                                                           | 1:N. Única por (perfil, tipo, fecha)                                                                                                          |
| **PerfilEntrenador**     | usuario, especialidad, experiencia, presentación                                                                                             | 1:1 con Usuario con rol ENTRENADOR                                                                                                            |
| **AsignacionEntrenador** | alumno, entrenador, desde, hasta, autor del alta, autor de la baja                                                                           | N:M con vigencia. Como máximo una vigente por alumno, por regla RN-18 y no por estructura                                                     |

**Por qué la asignación es N:M y no un campo en el alumno.** Un campo no permite responder "¿cambió de entrenador antes de abandonar?" ni auditar quién lo asignó. La unicidad se impone por RN-18. Costo marginal: nulo.

**Por qué el alumno ya no declara equipamiento.** Ver PD-07.

##### 2.3 Catálogo

| Entidad                             | Atributos relevantes                                                                                                                                                | Notas                                                                                                                                      |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Ejercicio**                       | gimnasio (nulo si es del catálogo base), nombre, instrucciones, patrón de movimiento (§4.7), nivel de dificultad (§4.4), unilateral, recurso visual, estado, origen | `gimnasio = null` identifica el catálogo base                                                                                              |
| **EjercicioEquipamiento**           | ejercicio, equipamiento (§4.1)                                                                                                                                      | N:M. Un ejercicio requiere **todo** el equipamiento que declara. Un ejercicio sin filas requiere sólo `PESO_CORPORAL`                      |
| **EjercicioMusculo**                | ejercicio, grupo muscular (§4.2), participación ∈ {PRIMARIA, SECUNDARIA}                                                                                            | N:M. Sin filas, el ejercicio está **no clasificado**: no aporta volumen, y esa ausencia se distingue de aportar cero. Ver D10/CB-12        |
| **EjercicioArticulacion**           | ejercicio, articulación (§4.3)                                                                                                                                      | N:M. Articulaciones que el movimiento exige. **Sin esta tabla la contraindicación no es calculable**; era el hueco central del modelo v1.0 |
| **GrupoMuscular**, **Articulacion** | código, nombre, región                                                                                                                                              | Tablas de referencia pobladas con §4.2 y §4.3. Cerradas                                                                                    |

##### 2.4 Prescripción

| Entidad                      | Atributos relevantes                                                                                                                                                                          |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PlantillaRutina**          | gimnasio, autor, nombre, tipo de rutina (§4.5), activa; `publicada` sólo se agrega si se implementa el alcance opcional de presets                                                                                                                          |
| **DiaPlantilla**             | plantilla, orden, nombre                                                                                                                                                                      |
| **EjercicioPlantilla**       | día de plantilla, ejercicio, orden, nota                                                                                                                                                      |
| **SeriePrescriptaPlantilla** | ejercicio de plantilla, orden, repeticiones mínimas, repeticiones máximas, carga sugerida, descanso, es de calentamiento                                                                      |
| **RutinaAsignada**           | alumno, plantilla de origen, tipo de rutina, frecuencia semanal objetivo, estado (D6/§1), origen ∈ {PLANTILLA_ENTRENADOR, GENERADA}; `PRESET_ELEGIDO_POR_ALUMNO` sólo existe si se implementa RF-021, solicitada por, solicitada en                           |
| **RevisionRutina**           | rutina, entrenador revisor, resultado ∈ {APROBADA, APROBADA_CON_CAMBIOS, RECHAZADA}, observación, instante                                                                                    |
| **VersionRutina**            | rutina, número, vigente, creada en, creada por, propuesta que la originó                                                                                                                      |
| **DiaRutina**                | versión de rutina, orden, nombre, patrón dominante                                                                                                                                            |
| **EjercicioRutina**          | día de rutina, ejercicio, orden, nota, **estado de compatibilidad** ∈ {COMPATIBLE, ADVERTIDO, INCOMPATIBLE, EJERCICIO_DESACTIVADO}, **motivo de la marca**                                    |
| **SeriePrescripta**          | ejercicio de rutina, orden, repeticiones mínimas, repeticiones máximas, carga sugerida, descanso, es de calentamiento                                                                         |

**`estado de compatibilidad` en `EjercicioRutina`.** RN-29, RN-92, RN-93 y RF-101 exigen "marcar el ejercicio en la rutina vigente sin retirarlo". En la v1.0 ninguna estructura lo soportaba. Es un atributo derivado que se recalcula en cada verificación de compatibilidad y se persiste para que la marca sobreviva a la consulta y pueda mostrarse al iniciar una sesión sin recalcular.

##### 2.5 Ejecución

| Entidad                 | Atributos relevantes                                                                                                                                                                                                                                                                               |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SesionEntrenamiento** | alumno, rutina, versión de rutina, día de rutina, estado (D6/§3), iniciada en, finalizada en, duración, **fecha de ocurrencia**, es diferida, es simulada, desbloqueada hasta                                                                                                                      |
| **RegistroSerie**       | sesión, orden, ejercicio prescripto, ejercicio ejecutado, repeticiones mínimas prescriptas, repeticiones máximas prescriptas, carga prescripta, es de calentamiento, carga ejecutada, repeticiones ejecutadas, esfuerzo percibido, completada, es adicional, motivo de omisión, atípico confirmado |
| **Comentario**          | autor, sesión _o_ rutina, texto, instante                                                                                                                                                                                                                                                          |

**`fecha de ocurrencia` separada de `iniciada en`.** Todos los indicadores usan la fecha de ocurrencia; la auditoría usa el instante de registro.

**`ejercicio prescripto` y `ejercicio ejecutado` en la misma fila.** Cuando no hay sustitución son el mismo. El volumen se imputa al ejecutado; el cumplimiento se evalúa contra el prescripto.

##### 2.6 Adaptación e inteligencia

| Entidad                  | Atributos relevantes                                                                                                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DiagnosticoEvolucion** | alumno, versión de rutina evaluada, período desde/hasta, situación global (§4.9), adherencia del período, calculado en, versión del componente, criterios no evaluados                 |
| **DiagnosticoEjercicio** | diagnóstico, ejercicio, situación (§4.9), variación de carga máxima estimada, cumplimiento de repeticiones, esfuerzo percibido medio, sesiones consideradas                            |
| **PropuestaAdaptacion**  | alumno, diagnóstico de origen, estado (D6/§4), creada en, resuelta en, resuelta por, versión resultante, versión del componente                                                        |
| **AjustePropuesto**      | propuesta, tipo (§4.10), ejercicio de rutina afectado _o_ alcance global, valor anterior, valor propuesto, criterio, datos que lo sustentan, estado ∈ {PENDIENTE, ACEPTADO, RECHAZADO} |
| **RecordPersonal**       | alumno, ejercicio, tipo (§4.8), valor, sesión que lo produjo, fecha, vigente                                                                                                           |
| ~~**ScoreRiesgo**~~      | **Derogada (v2.2)** — RF-061 a RF-063 pasan a WON'T ([D11/DD-34](#d11)); no hay estimación de riesgo que persistir                                          |
| ~~**SegmentoPerfil**~~   | **Derogada (v2.2)** — la descripción de perfil (RF-064) la produce la capa generativa y es efímera; no se persiste ([D11/DD-34](#d11))                       |
| **EvaluacionComponente** | componente, versión, conjunto de datos, tamaño de la muestra, métricas obtenidas, métricas del criterio de referencia, ejecutada en                                                    |

##### 2.7 Transversales

| Entidad               | Atributos relevantes                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| **Aviso**             | destinatario, tipo (§4.12), referencia, texto, instante, leído en, vencido                        |
| **RegistroAuditoria** | actor, operación, entidad afectada, identificador afectado, valor anterior, valor nuevo, instante |

#### 3. Puntos difíciles del modelo

##### PD-01 — Plantilla, rutina y versión

**Problema.** ¿Qué pasa si un entrenador modifica una plantilla ya usada por doce alumnos? ¿Y qué pasa cuando se aplica una adaptación a una rutina bajo la cual ya se ejecutaron sesiones?

| Alternativa                              | Descartada porque                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| La rutina referencia a la plantilla      | Modificar la plantilla reescribe el pasado de doce alumnos; la personalización individual es imposible |
| Versionado con diferencias y propagación | Exige resolución de conflictos. Coste desproporcionado                                                 |
| **Copia + versiones completas** ✅       | —                                                                                                      |

**Elegida:** copia profunda al solicitar la rutina (RF-022) más versiones completas de la rutina (RF-092).
**Qué se sacrifica.** Los cambios de plantilla no se propagan, y hay duplicación de datos. A esta escala la duplicación es irrelevante; la no propagación es deseable.
**Por qué versiones completas y no diferencias.** Una versión de rutina es una copia profunda de una estructura pequeña: no hay diferencias que calcular ni conflictos que resolver, y RF-093 se responde comparando dos versiones.

##### PD-02 — La sesión es autocontenida

Cada sesión copia su prescripción al iniciarse, en sus propios registros de serie. Aunque la rutina cambie de versión mañana, la sesión de hoy conserva lo que estaba prescripto hoy `[F: RF-028]`.

- El pasado es inmune al versionado, sin lógica adicional.
- El cumplimiento (prescripto contra ejecutado) sale gratis, por serie.
- Un ejercicio desactivado después no rompe ninguna sesión anterior.

##### PD-03 — Derivado o persistido

**Regla general:** se deriva todo lo que sea función pura de los datos crudos; se persiste sólo lo que es un evento con fecha, la salida fechada de un componente, o una marca que debe sobrevivir a la consulta.

| Dato                                                                 | Decisión                           | Motivo                                                                                                                                                                                                   |
| -------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Volumen, frecuencia, carga máxima estimada, adherencia, cumplimiento | **Derivado**                       | Si se persisten y cambia la definición, hay que recalcular todo el histórico                                                                                                                             |
| **Récord personal**                                                  | **Persistido**                     | Evento con fecha que debe notificarse en el momento. Recalcularlo pierde el instante                                                                                                                     |
| **Diagnóstico y propuesta**                                          | **Persistido**                     | Salidas fechadas de un componente con versión; deben poder auditarse                                                                                                                                     |
| ~~Estimación de riesgo y segmento~~                                  | **N/A (v2.2)**                     | Riesgo de abandono retirado del alcance; la descripción de perfil (RF-064) es efímera. Ver [D11/DD-34](#d11)                                                                  |
| **Alternativas de sustitución incorporadas a un candidato de rutina** | **Persistido**                     | Salida de la capa generativa (RF-059); se guarda la lista, no se reejecuta `[F: RF-072]`                                                                                                                  |
| **Estado de compatibilidad de un ejercicio de rutina**               | **Persistido, derivado en origen** | Es el único derivado que se persiste. Se recalcula ante cada verificación (RN-45) y se guarda para que la marca esté disponible al iniciar una sesión y en la vista de rutina sin recalcular el conjunto |
| Peso corporal y perímetros                                           | **Persistido**                     | Son el dato crudo                                                                                                                                                                                        |

##### PD-04 — Ámbito del catálogo

Un ejercicio con `gimnasio = null` pertenece al catálogo base y es visible para todos; uno con gimnasio informado sólo dentro de él. Reconcilia RF-013 con RF-069 sin duplicar la carga inicial.
**Qué se sacrifica.** Un entrenador no puede promover su ejercicio al catálogo base.

##### PD-05 — Un solo entrenador vigente sobre una relación con historial

El modelo soporta el historial completo; RN-18 impone la unicidad. Sin el historial no se puede responder qué entrenador supervisó un período ni calcular la carga por entrenador.

##### PD-06 — Borrado

**Ninguna entidad referenciada por información histórica se borra físicamente.** Ejercicios, usuarios, plantillas y rutinas se desactivan. La única eliminación real es la anonimización de datos personales en la baja de cuenta (RN-106), que reemplaza los identificadores personales y conserva los registros de entrenamiento desvinculados. Ver D10/CB-38.

##### PD-07 — El equipamiento es del gimnasio, no del alumno

**Problema.** ¿Contra qué conjunto de equipamiento se valida una prescripción?

| Alternativa               | Consecuencia                                                                                                                                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lo declara el alumno      | La falta de equipamiento sólo puede advertir, porque el alumno podría tener acceso circunstancial a algo que no declaró. La validación se vuelve blanda y el generador puede proponer ejercicios imposibles |
| Lo declara el gimnasio ✅ | La falta de equipamiento **impide**: si la máquina no está en el gimnasio, el ejercicio no se puede hacer. La validación se vuelve dura y verificable                                                       |
| Ambos, con intersección   | Duplica el mantenimiento y reintroduce la ambigüedad del primer caso                                                                                                                                        |

**Elegida:** el inventario del gimnasio es la única fuente. El alumno no declara equipamiento `[F: decisión del cliente, 2026-08-18]`.

**Qué se gana.** El catálogo prescribible queda determinado por gimnasio, la incompatibilidad por equipamiento pasa de advertencia a impedimento (RN-47), la incorporación del alumno pierde un paso, y el administrador adquiere una función con efecto real sobre la prescripción en lugar de un rol puramente administrativo.

**Qué se sacrifica.** Un alumno que además entrena en su casa no puede recibir una rutina que use su propio equipamiento. Es una limitación aceptada: el sistema prescribe para el gimnasio que lo mantiene.

**Consecuencia operativa que hay que asumir.** Si el administrador declara mal el inventario, todo el catálogo prescribible del gimnasio es incorrecto y ninguna rutina generada sirve. El inventario es un dato crítico, no una configuración cosmética.

##### PD-08 — El alta es por invitación

**Problema.** El sistema no es abierto: un gimnasio afiliado avisa a la persona para que se registre. ¿Cómo queda vinculado un usuario a su gimnasio?

**Elegida:** la invitación es la única vía de alta. Un administrador —o un entrenador, para sus futuros alumnos— emite una invitación nominal a una dirección de correo, con los roles que se le otorgarán. La persona crea su cuenta desde esa invitación y queda vinculada al gimnasio emisor `[F: decisión del cliente, 2026-08-18]`.

**Qué resuelve.** No hay autorregistro sin gimnasio; la pertenencia al gimnasio no es un dato que el usuario elige; los roles quedan determinados por quien invita y no por quien se registra; y queda auditado quién incorporó a cada persona.

**Qué se sacrifica.** No hay crecimiento espontáneo de usuarios. Es exactamente lo que el modelo de negocio pide.

**Arranque.** El primer administrador de un gimnasio no puede invitarse a sí mismo: lo crea el aprovisionamiento (RF-115), junto con el gimnasio. Es una operación del proveedor del sistema, fuera de la aplicación y de todo rol.

#### 4. Restricciones de integridad

| #      | Restricción                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RI-01  | Un usuario pertenece a exactamente un gimnasio                                                                                                          |
| RI-02  | El correo es único dentro de un gimnasio                                                                                                                |
| RI-03  | Un usuario tiene al menos un rol                                                                                                                        |
| RI-04  | Un alumno tiene como máximo un objetivo con `hasta = null`                                                                                              |
| RI-05  | Un alumno tiene como máximo una asignación con `hasta = null`                                                                                           |
| RI-06  | Un alumno tiene como máximo una rutina en estado VIGENTE y como máximo una en estado PROPUESTA                                                          |
| RI-06b | Una rutina sólo alcanza VIGENTE si existe una revisión favorable de un entrenador con asignación vigente sobre ese alumno en el instante de la revisión |
| RI-07  | Una rutina tiene exactamente una versión marcada como vigente                                                                                           |
| RI-08  | Una medición corporal es única por (alumno, tipo, fecha)                                                                                                |
| RI-09  | Un alumno tiene como máximo una sesión en estado EN_CURSO                                                                                               |
| RI-10  | Un registro de serie es único por (sesión, orden)                                                                                                       |
| RI-11  | Un ejercicio del catálogo base tiene `gimnasio = null`; uno del gimnasio lo tiene informado                                                             |
| RI-12  | Toda serie prescripta pertenece a un ejercicio de rutina, que pertenece a un día, que pertenece a una versión                                           |
| RI-13  | El orden es único dentro de su nivel                                                                                                                    |
| RI-14  | Una propuesta pertenece a un único diagnóstico, y ambos al mismo alumno                                                                                 |
| RI-15  | Un ajuste pertenece a una única propuesta                                                                                                               |
| RI-16  | Toda sesión referencia la versión de rutina bajo la cual se ejecutó                                                                                     |
| RI-17  | `hasta` es posterior a `desde` en toda entidad con vigencia                                                                                             |
| RI-18  | Una sesión simulada sólo contiene registros de serie simulados                                                                                          |
| RI-19  | Una invitación pertenece a un gimnasio y produce como máximo un usuario                                                                                 |
| RI-20  | Todo usuario referencia la invitación que lo originó, salvo el primer administrador de cada gimnasio, que referencia el aprovisionamiento               |
| RI-21  | Un ejercicio tiene como máximo una participación PRIMARIA                                                                                               |
| RI-22  | Un récord personal vigente es único por (alumno, ejercicio, tipo)                                                                                       |
| RI-23  | Un gimnasio tiene al menos un usuario con rol ADMINISTRADOR en estado activo                                                                            |


---

<a id="d5"></a>

### D5 — Reglas de negocio

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/domain/business-rules.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D5`

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.2        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | D2, D3, D4 |

**Cambios de la v1.0:** se incorporan las reglas que faltaban y sin las cuales la capacidad central no era implementable — compatibilidad calculable (§6), derivación del tipo de rutina (§5.1), criterios de diagnóstico (§9.1) y **reglas de ajuste** (§9.2) — y se incorpora el marcado de origen, ausente en toda la v1.0.

**Cambios de la v2.0:** el **candidato de rutina** —RN-124 a RN-129 y §5.2—, que da al solicitante la posibilidad de moldear la rutina generada antes de enviarla a revisión, sin tocar la prescripción ni la puerta del entrenador. Ver D11/DD-33.

**Cambios de la v2.2, parte A (presets como alcance opcional).** Las reglas de publicación sólo aplican si se implementa RF-021; la generación y las plantillas privadas no dependen de ellos.

**Cambios de la v2.2, parte B ([baseline de alcance](#baseline)).** Ninguna regla se borra ni cambia de contenido. Se marcan como **⏸ diferidas** las que quedaron sin sujeto al diferirse su requisito de origen en la Etapa 1, y se corrige una que dejó de ser cierta:

| Regla                                     | Estado en la Etapa 1                                                                                                                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RN-124 a RN-129 y §5.2 · candidato        | ⏸ El ajuste por el solicitante se difiere con RF-119 y RF-025 ([DD-33](#d11) derogada para esta etapa). El **objeto** candidato subsiste como estado técnico: ver D6/§11 |
| RN-32 · publicación de una plantilla como preset | ⏸ Sin sujeto salvo que se implemente RF-021, que es alcance opcional                                                                                   |
| RN-100 · estimación de riesgo diferida    | ⏸ Sin sujeto desde [DD-34](#d11)                                                                                                |
| RN-119 a RN-123 · §13 nutricional         | ⏸ Diferidas con RF-012 y RF-075                                                                                                                             |
| **RN-95b y RN-99 · comportamiento ante fallo generativo** | **✎ Corregidas.** Ya no pueden remitir a los presets                                                                                        |

**Lo que no se toca, y conviene decirlo.** RN-39a (derivación del tipo de rutina), RN-44a a RN-44d (compatibilidad), RN-79a (criterios de diagnóstico) y RN-89a (reglas de ajuste) quedan **intactas**. Son el núcleo determinístico del producto y el recorte no las alcanza. Sus umbrales y magnitudes siguen siendo convenciones del proyecto marcadas `[S]`, discutibles con el cliente y registradas en D12/§1.1.

#### Marcado de origen

Toda constante numérica lleva su origen. `[F]` proviene de una fuente del proyecto · `[I]` se deriva de otra regla `· [S]` es una convención adoptada por este proyecto, sin fuente externa: **es discutible con el cliente y está registrada en D12/§1.1**.

---

#### 1. Identidad, afiliación y acceso

| #          | Regla                                                                                                                                                                                         | Origen          |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **RN-01**  | Un usuario pertenece a exactamente un gimnasio y no puede cambiar de gimnasio. Para operar en otro se requiere otra invitación y otra cuenta                                                  | `[F]` cliente   |
| **RN-02**  | El correo electrónico identifica de forma única a un usuario dentro de su gimnasio                                                                                                            | `[I]` de RN-01  |
| **RN-02a** | **No existe el alta espontánea.** Una persona sólo puede crear una cuenta a partir de una invitación vigente emitida por su gimnasio                                                          | `[F]` cliente   |
| **RN-02b** | Una invitación indica el gimnasio, la dirección de correo destinataria y los roles que se otorgarán. Es de un solo uso, caduca a los **14 días** de emitida y puede revocarse antes de usarse | `[S]` plazo     |
| **RN-02c** | Los roles del usuario creado son exactamente los de su invitación. El usuario no elige sus roles                                                                                              | `[I]` de RN-02a |
| **RN-02d** | Un administrador puede emitir invitaciones para cualquier rol. Un entrenador puede emitirlas únicamente con el rol ALUMNO, y el alumno resultante queda asignado a él                         | `[I]` de D3     |
| **RN-02e** | El gimnasio y su primer administrador se crean por aprovisionamiento, fuera de la aplicación. Ningún rol de la aplicación puede crear un gimnasio                                             | `[F]` cliente   |
| **RN-03**  | Todo usuario tiene al menos un rol. Quitarle el último es una operación inválida; para retirarlo se suspende o se da de baja la cuenta                                                        | `[I]` de RI-03  |
| **RN-03a** | Un gimnasio no puede quedarse sin ningún administrador activo. La operación que produciría ese estado se rechaza                                                                              | `[I]` de RN-02e |
| **RN-05**  | Toda operación se autoriza verificando el rol y, además, la relación del actor con el recurso concreto                                                                                        | `[F]` RF-005    |
| **RN-06**  | El enlace de recuperación de acceso caduca a las **2 horas** y es de un solo uso. Emitir uno nuevo invalida el anterior                                                                       | `[S]` plazo     |
| **RN-07**  | La sesión de usuario expira tras **30 días** de inactividad continuada                                                                                                                        | `[S]` plazo     |
| **RN-08**  | Ningún estado del sistema impide a un usuario leer y exportar sus propios datos                                                                                                               | `[I]` de RF-006 |

_(RN-04 —"toda cuenta creada por autorregistro nace con rol ALUMNO"— queda **derogada** por RN-02a y RN-02c. El identificador no se reutiliza.)_

#### 2. Inventario del gimnasio

| #          | Regla                                                                                                                                                                                           | Origen          |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **RN-115** | El administrador declara y mantiene el inventario de equipamiento del gimnasio sobre la enumeración cerrada de D2/§4.1. `PESO_CORPORAL` se considera siempre presente                           | `[F]` cliente   |
| **RN-116** | El **catálogo prescribible** de un gimnasio es el conjunto de ejercicios accesibles cuyo equipamiento requerido está íntegramente presente en su inventario                                     | `[I]` de RN-115 |
| **RN-117** | Retirar un equipamiento del inventario marca como INCOMPATIBLE todo ejercicio de rutina vigente que lo requiera, y dispara la reevaluación de esas rutinas. **No las invalida ni las detiene**  | `[I]` de RN-92  |
| **RN-118** | Un gimnasio cuyo catálogo prescribible no alcance para construir una rutina del tipo requerido lo declara explícitamente al administrador, indicando qué patrones de movimiento no puede cubrir | `[I]` de RN-49  |

#### 3. Perfil, condiciones y aptitud

| #          | Regla                                                                                                                                                                                           | Origen          |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **RN-09**  | Un alumno tiene **como máximo** un objetivo vigente, y ninguno antes de declararlo por primera vez. Declarar uno nuevo cierra el anterior con fecha de fin igual a la fecha de inicio del nuevo | `[I]` de RI-04  |
| **RN-10**  | Una condición física vigente es la que tiene fecha de inicio pasada y no tiene fecha de fin, o la tiene futura. Varias pueden estar vigentes simultáneamente                                    | `[F]` RF-085    |
| **RN-10a** | Toda condición física declara una zona corporal de D2/§4.2 ∪ §4.3 y una severidad de D2/§4.6. La descripción libre es complementaria y **no participa de ningún cálculo**                       | `[I]` de RN-44a |
| **RN-11**  | Las condiciones vigentes se evalúan a la fecha de la operación. Una condición cerrada deja de restringir desde su fecha de fin y no reabre retroactivamente ninguna prescripción pasada         | `[I]` de PD-02  |
| **RN-12**  | La aptitud vigente es la de fecha de vencimiento más lejana no superada. Si no hay ninguna, el alumno no tiene aptitud vigente                                                                  | `[I]`           |
| **RN-13**  | La ausencia o el vencimiento de la aptitud se advierte de forma destacada al poner una rutina en vigencia y al iniciar una sesión. **Nunca impide ninguna operación**                           | `[F]` cliente   |
| **RN-13a** | La aptitud puede registrarla el propio alumno o un administrador. El entrenador la consulta y no la modifica                                                                                    | `[F]` cliente   |
| **RN-13b** | Se emite un aviso `APTITUD_POR_VENCER` **30 días** antes del vencimiento y otro el día del vencimiento                                                                                          | `[S]` plazo     |
| **RN-14**  | El estado de membresía es informativo. Ningún valor condiciona el acceso a ninguna funcionalidad                                                                                                | `[F]` cliente   |
| **RN-15**  | Una medición corporal es única por alumno, tipo y fecha. Cargar una segunda para la misma combinación sustituye a la anterior, con registro de auditoría                                        | `[I]` de RI-08  |
| **RN-16**  | No se aceptan mediciones corporales con fecha futura                                                                                                                                            | `[I]`           |
| **RN-17**  | Rangos admisibles: peso corporal **20,0–400,0 kg**; altura **100–250 cm**; perímetros **10,0–250,0 cm**. Fuera de rango se rechaza indicando el rango                                           | `[S]` rangos    |

#### 4. Asignación entrenador–alumno

| #          | Regla                                                                                                                                                                                                                                                                                                                           | Origen                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **RN-18**  | Un alumno tiene como máximo una asignación vigente. Crear una nueva finaliza la anterior en el mismo instante                                                                                                                                                                                                                   | `[F]` RF-066           |
| **RN-19**  | El acceso del entrenador a un alumno existe si y sólo si hay asignación vigente en el instante de la consulta. No hay acceso residual                                                                                                                                                                                           | `[F]` RF-066           |
| **RN-20**  | Finalizar una asignación no altera la rutina vigente del alumno ni sus sesiones. Sólo detiene la aprobación de cambios                                                                                                                                                                                                          | `[I]`                  |
| **RN-21**  | Un alumno sin asignación vigente es una situación anómala: el sistema la señala al administrador y la cuantifica en el panel del gimnasio                                                                                                                                                                                       | `[I]` de DD-25         |
| **RN-22**  | Un entrenador no puede tener una asignación consigo mismo                                                                                                                                                                                                                                                                       | `[I]`                  |
| **RN-22a** | **Un entrenador que quiera entrenar debe tener otro entrenador asignado**, y se le aplican íntegramente las reglas del alumno. Si es el único entrenador del gimnasio, no puede tener rutina vigente: el sistema lo señala al administrador como caso a resolver incorporando otro entrenador. **No hay excepción a la puerta** | `[I]` de RN-22 y RN-35 |
| **RN-23**  | Al finalizar una asignación, la rutina propuesta y las propuestas de adaptación pendientes de ese alumno quedan BLOQUEADAS hasta la reasignación                                                                                                                                                                                | `[I]` de RA-07         |

#### 5. Catálogo y prescripción

| #          | Regla                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Origen          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **RN-24**  | Un ejercicio del catálogo base es visible para todos los gimnasios y no es editable por ningún usuario                                                                                                                                                                                                                                                                                                                                                  | `[I]` de PD-04  |
| **RN-25**  | Un ejercicio creado por un entrenador es visible sólo dentro de su gimnasio y nace en estado PROPUESTO                                                                                                                                                                                                                                                                                                                                                  | `[F]` RF-017    |
| **RN-26**  | Un ejercicio PROPUESTO puede usarse en plantillas de su autor, pero no aparece en búsquedas generales ni puede prescribirse a un alumno hasta ser aprobado                                                                                                                                                                                                                                                                                              | `[I]` de RF-018 |
| **RN-27**  | Un ejercicio nunca se borra. Se desactiva                                                                                                                                                                                                                                                                                                                                                                                                               | `[F]` RF-018    |
| **RN-28**  | Un ejercicio desactivado no puede incorporarse a nuevas prescripciones ni proponerse como sustituto                                                                                                                                                                                                                                                                                                                                                     | `[I]` de RN-27  |
| **RN-29**  | Un ejercicio desactivado presente en una rutina vigente permanece y puede ejecutarse, se marca como `EJERCICIO_DESACTIVADO` y genera una propuesta de sustitución                                                                                                                                                                                                                                                                                       | `[F]` RF-101    |
| **RN-30**  | Un ejercicio sin participación muscular declarada está **no clasificado**: no aporta volumen y esa ausencia se distingue de aportar cero                                                                                                                                                                                                                                                                                                                | `[F]` RF-099    |
| **RN-31**  | Un ejercicio tiene como máximo una participación primaria y cualquier cantidad de secundarias                                                                                                                                                                                                                                                                                                                                                           | `[I]` de RI-21  |
| **RN-32**  | Una plantilla pertenece a un gimnasio. Si se implementa la publicación opcional como preset, sólo puede publicarse y utilizarse dentro de ese gimnasio                                                                                                                                                                                                                                                                                                   | `[I]` de RN-01  |
| **RN-33**  | Solicitar una rutina a partir de una plantilla crea una copia profunda e independiente. Modificar la plantilla después no altera ninguna rutina ya creada                                                                                                                                                                                                                                                                                               | `[F]` RF-022    |
| **RN-34**  | Toda rutina conserva la referencia a la plantilla de origen                                                                                                                                                                                                                                                                                                                                                                                             | `[F]` RF-022    |
| **RN-35**  | **Ninguna rutina alcanza VIGENTE sin una revisión favorable de un entrenador con asignación vigente sobre el alumno.** Aplica a todo origen implementado: plantilla del entrenador, rutina generada y, opcionalmente, preset elegido por el alumno                                                                                                                                                                                                       | `[F]` cliente   |
| **RN-35a** | Una versión nueva generada por una propuesta aceptada **no requiere una segunda revisión**: la resolución de la propuesta por el entrenador _es_ la revisión                                                                                                                                                                                                                                                                                            | `[I]` de RN-35  |
| **RN-36**  | Un alumno tiene como máximo una rutina VIGENTE y como máximo una PROPUESTA. Poner una en vigencia archiva la anterior                                                                                                                                                                                                                                                                                                                                   | `[I]` de RI-06  |
| **RN-36a** | Solicitar una rutina cuando ya existe una PROPUESTA pasa la anterior a DESCARTADA, con registro de quién la descartó                                                                                                                                                                                                                                                                                                                                    | `[I]` de RI-06  |
| **RN-37**  | Una rutina archivada y todas sus versiones permanecen consultables junto con las sesiones ejecutadas bajo ellas                                                                                                                                                                                                                                                                                                                                         | `[I]` de PD-01  |
| **RN-38**  | Toda rutina declara su frecuencia semanal objetivo, entre **1 y 7**, dentro del rango que su tipo admite (RN-39a)                                                                                                                                                                                                                                                                                                                                       | `[F]` RF-024    |
| **RN-39**  | Toda rutina declara su tipo, del que se derivan las restricciones de RN-39a                                                                                                                                                                                                                                                                                                                                                                             | `[F]` RF-082    |
| **RN-40**  | Si el tipo de la rutina no coincide con el objetivo vigente del alumno y no es `ACONDICIONAMIENTO_GENERAL`, el sistema lo advierte y exige confirmación del entrenador. No lo impide                                                                                                                                                                                                                                                                    | `[F]` RF-083    |
| **RN-41**  | Una rutina tiene entre 1 y 7 días. Un día tiene al menos un ejercicio. Un ejercicio tiene al menos una serie prescripta                                                                                                                                                                                                                                                                                                                                 | `[S]` límites   |
| **RN-42**  | Los días de la rutina no están asociados a días del calendario. El sistema propone el siguiente día del ciclo según el historial; el alumno puede elegir otro                                                                                                                                                                                                                                                                                           | `[F]` A §5.3    |
| **RN-43**  | En una serie prescripta las repeticiones mínimas son ≤ las máximas, ambas entre **1 y 100**; el descanso entre **0 y 600 s**; la carga sugerida es opcional y no negativa                                                                                                                                                                                                                                                                               | `[S]` rangos    |
| **RN-124** | La salida de una generación se presenta primero como **candidato de rutina**: una estructura completa que **no es una `RutinaAsignada`**, no tiene estado del ciclo de D6/§1, pertenece a quien la solicitó y no se avisa a ningún entrenador. Existe hasta que el solicitante lo confirma, lo abandona o vence tras 24 horas sin actividad. Si se implementan presets, sus copias usan el mismo flujo. La generación automática del alta no produce candidato | `[I]` de RN-35  |
| **RN-125** | El solicitante ajusta el candidato antes de confirmarlo, dentro de las operaciones de §5.2. El ajuste **no altera el origen** de la rutina ni exime de la revisión del entrenador (RN-35, RA-07b)                                                                                                                                                                                                                                                       | `[S]` criterio  |
| **RN-126** | Toda operación sobre el candidato revalida en el acto contra RN-39a y §6, y el rechazo enuncia el rango o el mínimo incumplido (RN-55). Un candidato que no supere la validación no puede confirmarse                                                                                                                                                                                                                                                   | `[I]` de RN-95  |
| **RN-127** | Un candidato admite como máximo **3 regeneraciones completas**. Elegir entre alternativas admisibles ya calculadas (RN-49a) no consume el tope. Agotado el tope, el solicitante confirma el último candidato o deriva la construcción a su entrenador; nunca se presenta un error (RN-99)                                                                                                                                                               | `[S]` límite    |
| **RN-128** | Las preferencias que el solicitante declara sobre el candidato —excluir un ejercicio, preferir un patrón— se registran como **entrada** del componente, nunca como parche sobre su salida, de modo que la generación siga siendo reproducible (RN-98)                                                                                                                                                                                                   | `[I]` de RN-98  |
| **RN-129** | Confirmar el candidato crea la rutina PROPUESTA, y es el instante en que se aplica RN-36a. La diferencia entre la rutina propuesta y la salida original del componente, o la plantilla de origen, es reconstruible y **se presenta al entrenador en la revisión** (FL-02)                                                                                                                                                                               | `[I]` de RN-35  |

##### 5.1 Derivación del tipo de rutina · RN-39a

Toda rutina y toda salida de un componente de decisión se valida contra esta tabla. `[S]` **Todos estos valores son convenciones del proyecto, derivadas de práctica habitual de entrenamiento de fuerza. Son el primer candidato a revisión con un entrenador real.**

| Tipo de rutina              | Frecuencia semanal admisible | Series de trabajo por ejercicio | Repeticiones objetivo | Descanso (s) | Ejercicios por día |
| --------------------------- | ---------------------------- | ------------------------------- | --------------------- | ------------ | ------------------ |
| `FUERZA`                    | 3 – 5                        | 3 – 5                           | 3 – 6                 | 180 – 300    | 4 – 6              |
| `HIPERTROFIA`               | 3 – 6                        | 3 – 4                           | 6 – 12                | 60 – 120     | 5 – 8              |
| `RESISTENCIA_MUSCULAR`      | 2 – 4                        | 2 – 4                           | 12 – 20               | 30 – 60      | 5 – 8              |
| `ACONDICIONAMIENTO_GENERAL` | 2 – 4                        | 2 – 3                           | 8 – 15                | 45 – 90      | 5 – 8              |

**Estructura de días admisible según la frecuencia semanal objetivo** `[S]`:

| Frecuencia | Composición de los días, por patrón dominante                                |
| ---------- | ---------------------------------------------------------------------------- |
| 2          | Dos días de cuerpo completo                                                  |
| 3          | Tres días de cuerpo completo, **o** empuje / tracción / pierna               |
| 4          | Superior / inferior / superior / inferior                                    |
| 5          | Empuje / tracción / pierna / superior / inferior                             |
| 6          | Empuje / tracción / pierna, dos veces                                        |
| 7          | No admitida como estructura: 7 excede el máximo de días de rutina útil `[S]` |

**Cobertura mínima de patrones** `[S]`: toda rutina debe incluir, en el conjunto de sus días, al menos un ejercicio de `EMPUJE_HORIZONTAL`, uno de `TRACCION_HORIZONTAL` o `TRACCION_VERTICAL`, uno de `DOMINANTE_RODILLA` y uno de `DOMINANTE_CADERA`. Si el catálogo prescribible del gimnasio no lo permite, se aplica RN-118.

##### 5.2 Ajuste del candidato de rutina · RN-125 — ⏸ **diferido en la Etapa 1**

> Esta sección y las reglas RN-124 a RN-129 quedan diferidas junto con RF-119 y RF-025 ([DD-33](#d11), derogada para esta etapa). En la Etapa 1 la generación la origina el entrenador o la incorporación del alumno, y su salida se convierte directamente en rutina PROPUESTA sujeta a revisión. El texto se conserva íntegro: si vuelve la solicitud por el alumno, vuelve con estas reglas ya escritas.


Antes de confirmar, el solicitante moldea el candidato. Lo que puede tocar el **alumno** está acotado a lo que el sistema revalida sin reabrir la prescripción: `[S]`

| Admitido                                                                                     | No admitido                                                  |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Sustituir un ejercicio por una **alternativa admisible** del mismo patrón dominante (RN-49a) | Series, repeticiones, descanso y carga sugerida              |
| Agregar un ejercicio del catálogo prescribible que resulte COMPATIBLE                        | Tipo de rutina                                               |
| Quitar un ejercicio                                                                          | Frecuencia semanal objetivo                                  |
| Reordenar los ejercicios dentro de un día                                                    | Reordenar los días: su orden compone la estructura de RN-39a |
| Escribir la `nota` de un ejercicio                                                           | El estado de compatibilidad y su motivo                      |

Lo no admitido no es inaccesible: o es **parámetro**, y se cambia volviendo al paso 2 de FL-04 y regenerando, o es **prescripción**, y entonces la decide el entrenador. Un pedido numérico concreto del alumno viaja como `Comentario` sobre la propuesta y se resuelve en FL-02.

**Piso de la operación.** Quitar ejercicios no puede dejar el día por debajo del mínimo de RN-39a ni la rutina sin la cobertura mínima de patrones. El rechazo enuncia el mínimo (RN-126).

**Cuando el solicitante es el entrenador** esta restricción no se aplica: ya tiene escritura sobre las rutinas de sus alumnos asignados (D3) y su ajuste es el de FL-02/paso 2.

#### 6. Compatibilidad

| #          | Regla                                                                                                                                                                                                                                                                                          | Origen                                |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **RN-44**  | Una rutina es compatible con un alumno cuando ninguno de sus ejercicios está contraindicado con severidad impeditiva, ni excede su nivel de experiencia, ni exige equipamiento ausente del inventario del gimnasio                                                                             | `[F]` RF-086                          |
| **RN-44a** | **Contraindicación.** Un ejercicio está contraindicado por una condición física vigente si la zona corporal de la condición es (a) un grupo muscular con participación **primaria** en el ejercicio, **o** (b) una articulación que el ejercicio exige                                         | `[I]` construida sobre D2/§4.2 y §4.3 |
| **RN-44b** | **Efecto de la severidad.** `SEVERA` y `MODERADA` producen INCOMPATIBLE e impiden la puesta en vigencia. `LEVE` produce ADVERTIDO: se señala y no impide                                                                                                                                       | `[S]` correspondencia                 |
| **RN-44c** | **Nivel.** Un ejercicio cuyo nivel de dificultad es superior al nivel de experiencia del alumno, según el orden de D2/§4.4, produce INCOMPATIBLE                                                                                                                                               | `[S]` criterio                        |
| **RN-44d** | **Equipamiento.** Un ejercicio que exige equipamiento ausente del inventario del gimnasio produce INCOMPATIBLE                                                                                                                                                                                 | `[I]` de PD-07                        |
| **RN-45**  | La compatibilidad se verifica antes de poner una rutina en vigencia, ante toda modificación de una rutina vigente, ante todo cambio de objetivo, condición física o aptitud del alumno, y ante todo cambio del inventario del gimnasio                                                         | `[F]` RF-086, RF-094                  |
| **RN-46**  | Una incompatibilidad **impide** poner la rutina en vigencia. El sistema ofrece alternativas admisibles para cada ejercicio incompatible                                                                                                                                                        | `[F]` RF-086                          |
| **RN-47**  | La falta de equipamiento impide, no advierte: si el gimnasio no lo tiene, el ejercicio no se puede ejecutar                                                                                                                                                                                    | `[I]` de PD-07                        |
| **RN-48**  | La falta de aptitud vigente nunca constituye incompatibilidad. Advierte (RN-13)                                                                                                                                                                                                                | `[F]` cliente                         |
| **RN-49**  | Si para un ejercicio incompatible no existe ninguna alternativa admisible en el catálogo prescribible, el sistema lo declara explícitamente y deja la decisión al entrenador, que puede retirar el ejercicio o dejar la rutina propuesta. **No inventa una alternativa ni oculta el problema** | `[I]`                                 |
| **RN-49a** | **Alternativa admisible** de un ejercicio: ejercicio del catálogo prescribible, con el mismo patrón de movimiento, con estado de compatibilidad COMPATIBLE para ese alumno, ordenado por coincidencia de participación muscular primaria y luego secundaria                                    | `[I]` de RF-059                       |

#### 7. Ejecución

| #          | Regla                                                                                                                                                                                                                                                                          | Origen                  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| **RN-50**  | Un alumno tiene como máximo una sesión EN_CURSO                                                                                                                                                                                                                                | `[F]` RF-027            |
| **RN-51**  | Una sesión **iniciada en tiempo real** sólo puede abrirse sobre un día de la rutina VIGENTE del alumno. La sesión diferida se rige por RN-59                                                                                                                                   | `[F]` RF-027            |
| **RN-52**  | Al iniciarse, la sesión copia la prescripción vigente de ese día en sus propios registros de serie. Esa copia es inmutable                                                                                                                                                     | `[F]` RF-028            |
| **RN-53**  | Una sesión EN_CURSO sin actividad durante **8 horas** se cierra automáticamente como ABANDONADA                                                                                                                                                                                | `[F]` A §4.2            |
| **RN-54**  | Una serie sólo cuenta para el volumen si está completada y no es de calentamiento                                                                                                                                                                                              | `[F]` RF-040            |
| **RN-55**  | Rangos admisibles al registrar una serie: carga **0,00–1.000,00 kg**; repeticiones **1–100**; esfuerzo percibido **1–10**. La validación se realiza siempre del lado del sistema                                                                                               | `[S]` rangos            |
| **RN-55a** | **Registro atípico.** Una carga superior al **150%** del mejor histórico del alumno en ese ejercicio se marca como atípica y requiere confirmación explícita antes de aceptarse. Confirmada, se registra con normalidad y puede producir récord; sin confirmar, no se registra | `[S]` umbral            |
| **RN-56**  | Una serie sustituida se imputa al ejercicio ejecutado a efectos de volumen y cuenta como cumplida a efectos de cumplimiento de series, marcada como sustituida                                                                                                                 | `[I]` de DD-19          |
| **RN-57**  | Una serie omitida no cuenta para volumen ni como cumplida, y admite un motivo opcional                                                                                                                                                                                         | `[I]`                   |
| **RN-58**  | Una sesión completada puede corregirse dentro de las **48 horas** posteriores a su finalización. Después queda BLOQUEADA                                                                                                                                                       | `[F]` A §4.2            |
| **RN-58a** | **Desbloqueo excepcional.** A pedido del alumno, el entrenador con asignación vigente puede reabrir una sesión BLOQUEADA por **24 horas**, una sola vez por sesión, dejando registro de auditoría del motivo. Es la única vía de corregir un error detectado tarde             | `[S]` mecanismo y plazo |
| **RN-59**  | Una sesión diferida se registra con la fecha en que ocurrió, que no puede ser futura ni anterior a los **90 días**. Se imputa a la rutina y a la versión que estaban vigentes en esa fecha, **aunque hoy estén archivadas**                                                    | `[S]` plazo             |
| **RN-60**  | Un mismo envío de una serie, identificado por sesión y orden, produce un único registro aunque se reciba más de una vez                                                                                                                                                        | `[I]` de RI-10          |
| **RN-61**  | El registro de una serie no puede modificar la prescripción congelada de esa serie                                                                                                                                                                                             | `[I]` de PD-02          |

#### 8. Indicadores

| #          | Regla                                                                                                                                                                                                                                       | Origen                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **RN-62**  | **Volumen por grupo muscular** en un período: suma, sobre las series de trabajo completadas, de **1,0** por cada serie cuyo ejercicio ejecutado tiene participación primaria en ese grupo y **0,5** por cada secundaria                     | `[F]` A §7.1                                                                    |
| **RN-63**  | Las ponderaciones 1,0 y 0,5 son una convención documentada, no un hecho fisiológico                                                                                                                                                         | `[F]` A §7.1                                                                    |
| **RN-64**  | **Frecuencia** de un grupo muscular: cantidad de sesiones distintas del período que le aportaron volumen mayor que cero                                                                                                                     | `[I]`                                                                           |
| **RN-65**  | **Carga máxima estimada** de una serie: se calcula sobre series de trabajo completadas con carga mayor que cero y hasta **12 repeticiones**. Por encima de 12 no se calcula                                                                 | `[F]` A §6.1 fórmula; `[S]` el tope de 12                                       |
| **RN-66**  | La carga máxima estimada de un ejercicio en una sesión es la mayor de las de sus series                                                                                                                                                     | `[I]`                                                                           |
| **RN-67**  | **Adherencia** sobre la ventana de 4 semanas: sesiones completadas dividido por la suma, semana a semana, de la frecuencia semanal objetivo **vigente en cada una de esas semanas**. Se expresa en porcentaje y se acota a 100%             | `[I]` corrige el defecto de la v1.0 ante cambios de rutina dentro de la ventana |
| **RN-68**  | La adherencia se calcula desde que el alumno acumula **2 semanas con alguna rutina vigente**. **Cambiar de rutina no reinicia el cálculo.** Antes de ese umbral se informa como no disponible                                               | `[I]` corrige el defecto de la v1.0                                             |
| **RN-69**  | **Cumplimiento de series** de una sesión: series de trabajo completadas dividido por series de trabajo prescriptas                                                                                                                          | `[F]` RF-043                                                                    |
| **RN-69a** | **Cumplimiento de repeticiones** de una sesión: suma de repeticiones ejecutadas dividido por suma de repeticiones objetivo, tomando como objetivo el **tope** del rango prescripto, sobre las series de trabajo prescriptas. Acotado a 100% | `[F]` RF-043; `[S]` el uso del tope del rango                                   |
| **RN-70**  | **Récord personal**: se registra cuando una serie de trabajo completada supera el máximo histórico vigente del alumno en ese ejercicio, en cualquiera de los tres tipos de D2/§4.8. Se detecta al finalizar la sesión                       | `[F]` RF-044                                                                    |
| **RN-70a** | En ejercicios cuya carga ejecutada es cero, el único tipo aplicable es `REPETICIONES`                                                                                                                                                       | `[I]` cubre el hueco de la v1.0                                                 |
| **RN-71**  | Si se corrige o se elimina la sesión que produjo un récord, el récord de ese tipo y ejercicio se **recalcula sobre el histórico completo** del alumno. Puede restaurar el récord anterior o dejar el ejercicio sin récord                   | `[I]` cubre el hueco de la v1.0                                                 |
| **RN-72**  | Todo indicador se calcula sobre la fecha de ocurrencia de la sesión, nunca sobre la fecha de registro                                                                                                                                       | `[I]`                                                                           |
| **RN-73**  | Cuando no hay datos suficientes para calcular un indicador, el sistema lo declara explícitamente. **No devuelve cero, ni vacío, ni un valor por defecto**                                                                                   | `[F]` RF-051                                                                    |

##### 8.1 Umbrales de las señales de seguimiento

| #          | Regla                                                                                                                                                                                                                                               | Origen                                                        |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **RN-74**  | **Estancamiento** en un ejercicio: la variación de la carga máxima estimada, definida en RN-74a, es menor que **+2,5%** durante el período de diagnóstico, con al menos **4 sesiones** que incluyan ese ejercicio                                   | `[S]` umbrales                                                |
| **RN-74a** | **Variación de la carga máxima estimada** de un ejercicio en el período: `(mejor de las últimas 3 semanas − mejor de las primeras 3 semanas) / mejor de las primeras 3 semanas`. Si falta alguno de los dos extremos, la variación no es calculable | `[I]` sustituye "tendencia creciente", que no era verificable |
| **RN-75**  | **Caída de adherencia**: la adherencia de las últimas 2 semanas es al menos **25 puntos porcentuales** menor que la de las 2 semanas previas                                                                                                        | `[S]` umbral                                                  |
| **RN-76**  | **Desbalance**: un grupo muscular recibe menos de **6** o más de **22** series efectivas semanales promediadas sobre 4 semanas. Rangos orientativos de literatura de entrenamiento, **no recomendación de salud**                                   | `[F]` A §7.1                                                  |
| **RN-77**  | Ninguna señal se emite si el alumno no alcanza el mínimo de datos que la regla exige. La ausencia por falta de datos se distingue de la ausencia por normalidad                                                                                     | `[F]` RF-051                                                  |

#### 9. Diagnóstico y adaptación

| #         | Regla                                                                                                                                                                                                                                                             | Origen                 |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **RN-78** | El diagnóstico se produce sobre la rutina vigente, con periodicidad de **2 semanas**, y también a solicitud del entrenador                                                                                                                                        | `[S]` periodicidad     |
| **RN-79** | El diagnóstico asigna a cada ejercicio y al conjunto una situación de D2/§4.9                                                                                                                                                                                     | `[F]` RF-088           |
| **RN-81** | El esfuerzo percibido es opcional. Si no está registrado, el diagnóstico se produce igual sin ese criterio y **declara qué no pudo evaluar**                                                                                                                      | `[F]` RF-088           |
| **RN-82** | Un diagnóstico con situación global `DATOS_INSUFICIENTES` no genera propuesta de adaptación                                                                                                                                                                       | `[I]`                  |
| **RN-83** | Toda propuesta deriva de exactamente un diagnóstico y conserva la referencia                                                                                                                                                                                      | `[I]` de RI-14         |
| **RN-84** | Cada ajuste registra su tipo, el valor anterior, el valor propuesto, el criterio que lo motiva y los datos de evolución que lo sustentan                                                                                                                          | `[F]` RF-090           |
| **RN-85** | Toda propuesta se verifica contra §6 antes de presentarse. Una propuesta incompatible no se presenta                                                                                                                                                              | `[I]`                  |
| **RN-86** | Una propuesta se resuelve por aceptación total, aceptación parcial de ajustes individuales, o rechazo. Sólo la resuelve el entrenador con asignación vigente                                                                                                      | `[F]` RF-091 + cliente |
| **RN-87** | Una propuesta pendiente caduca a los **30 días** sin resolver, y el hecho se registra                                                                                                                                                                             | `[S]` plazo            |
| **RN-88** | Aceptar una propuesta, total o parcialmente, genera una nueva versión de la rutina. La anterior se conserva íntegra                                                                                                                                               | `[F]` RF-092           |
| **RN-89** | Al generarse una versión nueva, las sesiones ya ejecutadas conservan su referencia a la versión bajo la cual se ejecutaron y no se alteran                                                                                                                        | `[F]` RF-092           |
| **RN-90** | Una propuesta rechazada no genera versión y queda registrada con su motivo                                                                                                                                                                                        | `[I]`                  |
| **RN-91** | Un cambio de objetivo, la declaración o cierre de una condición física, un cambio de estado de la aptitud o un cambio del inventario provocan la reevaluación inmediata de la rutina vigente                                                                      | `[F]` RF-094           |
| **RN-92** | Si la reevaluación detecta una incompatibilidad sobrevenida, el sistema **marca los ejercicios afectados en la rutina vigente sin retirarlos**, lo señala al entrenador y al alumno, y genera la propuesta correspondiente. Retirarlos es decisión del entrenador | `[F]` RF-094           |
| **RN-93** | Mientras haya un ejercicio marcado como INCOMPATIBLE o ADVERTIDO, el alumno recibe la advertencia al iniciar cada sesión que lo incluya                                                                                                                           | `[I]`                  |

##### 9.1 Criterios de diagnóstico · RN-79a

Se evalúa **por ejercicio**, sobre el período de diagnóstico, en este orden de precedencia. La primera condición que se cumple determina la situación; las restantes no se evalúan. `[S]` **Todos los umbrales son convenciones del proyecto.**

| Orden | Situación               | Condición                                                                                                                                                                       |
| ----- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | `DATOS_INSUFICIENTES`   | Menos de 4 sesiones con ese ejercicio en el período, o variación de carga máxima estimada no calculable (RN-74a)                                                                |
| 2     | `SOBREEXIGENCIA`        | Cumplimiento de repeticiones < **70%** en 3 sesiones consecutivas, **o** esfuerzo percibido medio ≥ **9** en las series de trabajo de 3 sesiones consecutivas                   |
| 3     | `PROGRESION_ADECUADA`   | Variación de carga máxima estimada ≥ **+2,5%**                                                                                                                                  |
| 4     | `ESTIMULO_INSUFICIENTE` | El alumno alcanzó el tope del rango de repeticiones en **todas** las series de trabajo de las últimas 2 sesiones, y el esfuerzo percibido medio, si está registrado, es ≤ **5** |
| 5     | `ESTANCAMIENTO`         | Ninguna de las anteriores                                                                                                                                                       |

`ESTIMULO_INSUFICIENTE` es la contraparte simétrica de la sobreexigencia y cubre el caso más frecuente de estancamiento: el alumno cumple todo sin esfuerzo y la carga no sube. Sin ella ese caso caía en `ESTANCAMIENTO` y recibía el ajuste equivocado.

**Situación global**, evaluada en este orden sobre los ejercicios con situación distinta de `DATOS_INSUFICIENTES` `[S]`:

| Orden | Situación global        | Condición                                                                                                                     |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1     | `DATOS_INSUFICIENTES`   | Adherencia no disponible, **o** menos de la mitad de los ejercicios de la rutina tienen situación calculable                  |
| 2     | `SOBREEXIGENCIA`        | Al menos un tercio de los ejercicios en `SOBREEXIGENCIA`, **o** adherencia < 50% con cumplimiento de repeticiones medio < 70% |
| 3     | `ESTANCAMIENTO`         | Al menos la mitad de los ejercicios en `ESTANCAMIENTO`                                                                        |
| 4     | `ESTIMULO_INSUFICIENTE` | Al menos la mitad de los ejercicios en `ESTIMULO_INSUFICIENTE`                                                                |
| 5     | `PROGRESION_ADECUADA`   | Ninguna de las anteriores                                                                                                     |

##### 9.2 Reglas de ajuste · RN-89a

Es el núcleo del producto: convierte un diagnóstico en una propuesta concreta. Todo ajuste se somete a §6 antes de presentarse y a la revisión del entrenador antes de aplicarse. `[S]` **Todas las magnitudes son convenciones del proyecto.**

**Por ejercicio:**

| Situación del ejercicio                          | Ajuste                  | Magnitud                                                                                                                                                    |
| ------------------------------------------------ | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PROGRESION_ADECUADA`                            | Ninguno                 | —                                                                                                                                                           |
| `ESTIMULO_INSUFICIENTE`                          | `CARGA` ↑               | +2,5% de la carga sugerida, redondeado al alza al múltiplo de 2,50 kg. Incremento mínimo: 2,50 kg                                                           |
| `ESTANCAMIENTO`, primer diagnóstico consecutivo  | `ESQUEMA` + `VOLUMEN`   | Desplazar el rango de repeticiones un escalón dentro del rango que admite el tipo (RN-39a) y agregar **1 serie de trabajo**, sin superar el máximo del tipo |
| `ESTANCAMIENTO`, segundo diagnóstico consecutivo | `SUSTITUCION`           | Reemplazar por la primera alternativa admisible (RN-49a). Si no hay ninguna, se aplica RN-49 y el ajuste no se propone                                      |
| `SOBREEXIGENCIA`                                 | `CARGA` ↓ + `VOLUMEN` ↓ | −10% de la carga sugerida, redondeado a la baja al múltiplo de 2,50 kg, y quitar **1 serie de trabajo**, sin bajar del mínimo del tipo                      |
| Marcado `INCOMPATIBLE` o `EJERCICIO_DESACTIVADO` | `SUSTITUCION`           | Primera alternativa admisible (RN-49a)                                                                                                                      |
| `DATOS_INSUFICIENTES`                            | Ninguno                 | —                                                                                                                                                           |

**Globales:**

| Condición                                           | Ajuste       | Magnitud                                                                                                             |
| --------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------- |
| Adherencia < **60%** sostenida durante 4 semanas    | `ESTRUCTURA` | Reducir la frecuencia semanal objetivo en 1, sin bajar del mínimo del tipo (RN-39a)                                  |
| Situación global `SOBREEXIGENCIA`                   | `VOLUMEN`    | Aplicar la reducción de 1 serie a todos los ejercicios en sobreexigencia, además de sus ajustes individuales         |
| Desbalance por defecto en un grupo muscular (RN-76) | `ESTRUCTURA` | Agregar un ejercicio del patrón de movimiento que estimula primariamente ese grupo, tomado del catálogo prescribible |
| Desbalance por exceso en un grupo muscular (RN-76)  | `VOLUMEN`    | Quitar 1 serie de trabajo del ejercicio de ese grupo con menor variación de carga máxima estimada                    |
| Cambio de objetivo del alumno                       | `ESTRUCTURA` | Proponer el cambio de tipo de rutina al que corresponde al nuevo objetivo, con el reajuste de esquemas de RN-39a     |

**Restricciones que toda propuesta debe cumplir** `[I]`:

1. Ningún ajuste puede dejar la rutina fuera de los rangos de RN-39a.
2. Ningún ajuste puede introducir una incompatibilidad (RN-85).
3. Una propuesta no puede contener dos ajustes sobre el mismo ejercicio de rutina con tipos contradictorios.
4. Si tras aplicar las reglas no queda ningún ajuste, no se genera propuesta; el diagnóstico se registra igual.

#### 10. Componentes inteligentes

| #           | Regla                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Origen             |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| **RN-94**   | Un **componente narrativo** no introduce ningún valor numérico ausente de sus datos de entrada. Exigible al 100% y verificable de forma automática                                                                                                                                                                                                                                                                                                                                                                                                                   | `[F]` RF-057       |
| **RN-95**   | Un **componente de decisión** determina valores de prescripción a partir del contexto del alumno. Toda salida suya se valida contra §6 y contra RN-39a antes de presentarse, y nunca rige sin la revisión del entrenador                                                                                                                                                                                                                                                                                                                                             | `[F]` cliente      |
| **RN-95b**  | Una salida que no supere la validación no se presenta. El sistema reintenta una vez y, si el segundo intento falla o vence su límite de 120 segundos, declara la generación no disponible. No construye una rutina determinística alternativa ni muestra una propuesta inválida. ✎ v2.2: la vía que permanece es **la asignación de una plantilla del entrenador** (RF-019), no los presets publicados, diferidos con RF-021. **Si el gimnasio no tiene ninguna plantilla cargada, no queda ninguna vía de prescripción** — ver [DD-35](#d11) y D12/R-17                                                                                                                                                                                                                         | `[F]` ADR-0009     |
| **RN-96**   | Ningún componente emite indicaciones de carácter médico, diagnósticos clínicos ni recomendaciones de tratamiento                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `[F]` RF-057       |
| **RN-97**   | Toda rutina generada utiliza exclusivamente ejercicios del **catálogo prescribible** del gimnasio del alumno                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `[I]` de RN-116    |
| **RN-97b**  | Ningún componente de decisión se ejecuta sobre un alumno sin contexto suficiente. En ese caso el sistema declara qué falta y lo solicita, en lugar de decidir con supuestos                                                                                                                                                                                                                                                                                                                                                                                          | `[F]` cliente      |
| **RN-98**   | Toda salida de un componente registra la versión del componente, el contexto de entrada y el instante de cálculo, de modo que el resultado sea reproducible                                                                                                                                                                                                                                                                                                                                                                                                          | `[F]` RF-072       |
| **RN-99**   | La indisponibilidad de API IA, ngrok o LLM no produce un error técnico visible ni degrada otras funciones. La generación queda temporalmente deshabilitada; las plantillas privadas y la creación manual por entrenadores continúan operativas. ✎ v2.2: **los presets dejan de ser la contingencia** (RF-021, alcance opcional). Si el gimnasio no tiene ninguna plantilla cargada, no queda vía de prescripción — [DD-35](#d11), D12/R-17                                                                                                                                                                                                     | `[F]` RF-058       |
| **RN-101**  | La estimación se presenta siempre junto a su fecha de cálculo y sus factores principales, y nunca al alumno evaluado                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `[F]` RF-062       |
| **RN-102**  | Las recomendaciones de sustitución aplican los mismos filtros que §6 y se limitan al catálogo prescribible                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `[I]`              |
| **RN-103**  | Todo componente de recomendación o estimación se evalúa contra un criterio de referencia simple, y ambas métricas se conservan                                                                                                                                                                                                                                                                                                                                                                                                                                       | `[F]` RF-073       |
| **RN-103a** | **Dónde decide un componente aprendido y dónde una regla.** El componente generativo interpreta lenguaje natural, selecciona el tipo y construye el candidato inicial. RN-39a y §6 son barreras determinísticas de validación. El diagnóstico (§9.1) y los ajustes (§9.2) permanecen determinísticos; los componentes aprendidos actúan en alternativas, riesgo y segmentación. Cada capacidad se presenta según su naturaleza real                                                                                          | `[F]` ADR-0009     |

#### 11. Avisos

| #          | Regla                                                                                                                                                                                                                                                                                                       | Origen         |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **RN-111** | El sistema emite un aviso, de los tipos de D2/§4.12, al destinatario que corresponde: al alumno los que afectan su rutina, sus récords y su aptitud; al entrenador los que requieren su revisión y las señales de su cartera; al administrador los alumnos sin entrenador y los fallos de aprovisionamiento | `[F]` RF-095   |
| **RN-112** | Un aviso no leído no se repite. Un mismo hecho no genera más de un aviso                                                                                                                                                                                                                                    | `[S]` criterio |
| **RN-113** | Los avisos caducan a los **90 días** y dejan de mostrarse; el hecho que los originó permanece consultable en su entidad                                                                                                                                                                                     | `[S]` plazo    |
| **RN-114** | Al finalizar una asignación, los avisos pendientes del entrenador saliente relativos a ese alumno se cierran, y los que correspondan se re-emiten al entrenador entrante                                                                                                                                    | `[I]` de RN-23 |

#### 12. Datos, privacidad y trazabilidad

| #          | Regla                                                                                                                                                                                                                                                                             | Origen                        |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **RN-104** | El tratamiento de condiciones físicas, aptitud y mediciones corporales requiere consentimiento explícito, separado del alta, y se conserva el texto aceptado                                                                                                                      | `[F]` A §14.2                 |
| **RN-105** | El sistema no solicita documento de identidad, domicilio ni ningún dato personal que no condicione la prescripción o el cálculo de indicadores                                                                                                                                    | `[F]` A §14.2                 |
| **RN-106** | La baja de cuenta anonimiza los datos personales dentro de **7 días**. Las sesiones y series se conservan desvinculadas de la identidad, para no invalidar la analítica agregada                                                                                                  | `[F]` A §14.2; `[S]` el plazo |
| **RN-107** | Todo registro simulado está marcado de forma inequívoca y se excluye de toda analítica presentada como real                                                                                                                                                                       | `[F]` RF-071                  |
| **RN-108** | Se registra en auditoría: emisión y revocación de invitaciones, cambios de rol, altas y bajas de asignación, cambios del inventario, puesta en vigencia y modificación de rutinas, resolución de propuestas, desbloqueo de sesiones, cambios de membresía y curación del catálogo | `[F]` RF-097                  |
| **RN-109** | Los registros de auditoría no contienen credenciales ni contraseñas                                                                                                                                                                                                               | `[F]` A §14.2                 |
| **RN-110** | Los instantes se almacenan en tiempo universal coordinado y se presentan en la zona horaria del gimnasio. La semana va de lunes a domingo                                                                                                                                         | `[F]` A §5.5                  |

#### 13. Estimación energética orientativa — ⏸ **diferida en la Etapa 1**

> RN-119 a RN-123 quedan diferidas con RF-012 (2 votos de 8) y RF-075. Con ellas cae toda la cadena nutricional del producto en esta etapa, y [DD-13](#d11) queda sin efecto. El texto se conserva: la pregunta que resuelve —qué significa «generar la dieta»— volverá si vuelve la nutrición.


| #          | Regla                                                                                                                                                                                                                                                                                                                                               | Origen                |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **RN-119** | La estimación de gasto energético diario se calcula por la ecuación de **Mifflin-St Jeor** sobre sexo, edad, altura y peso corporal más reciente, multiplicada por un factor de actividad derivado de la frecuencia semanal objetivo del alumno                                                                                                     | `[F]` A §8            |
| **RN-120** | El rango orientativo de ingesta proteica es de **1,6 a 2,2 g por kg** de peso corporal                                                                                                                                                                                                                                                              | `[S]` rango           |
| **RN-121** | La **pauta nutricional** que el sistema produce se limita a la distribución de esa estimación energética y de ese rango proteico entre las comidas del día. **No nombra alimentos, no compone comidas y no registra ingesta**                                                                                                                       | `[F]` cliente + DD-13 |
| **RN-122** | Toda salida de §13 se presenta acompañada de la declaración de que es una estimación estadística orientativa y no una indicación nutricional profesional, y no se produce si el alumno declaró una condición física de severidad `MODERADA` o `SEVERA` cuya zona corporal el sistema no puede evaluar. En ese caso se remite a consulta profesional | `[I]`                 |
| **RN-123** | Si falta el peso corporal, la estimación no se calcula y se declara qué falta                                                                                                                                                                                                                                                                       | `[I]` de RN-73        |


---

<a id="d6"></a>

### D6 — Ciclos de vida y estados

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/domain/lifecycles-and-states.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D6`

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.3        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | D2, D4, D5 |

**Cambios de la v2.2:** §10 — la estimación de riesgo y la segmentación se retiran del alcance ([D11/DD-34](#d11)); la descripción de perfil (RF-064) es efímera y no genera registros.

**Cambios de la v2.3 ([baseline de alcance](#baseline)).** Ningún autómata cambia. Lo que cambia es qué transiciones existen en la Etapa 1:

- **El candidato de rutina no existe en esta etapa.** Se declaraba en §1 como objeto explícitamente fuera del ciclo de vida, para que nadie lo resolviera agregando un estado `BORRADOR`. Al diferirse RF-119 y RF-025, **la advertencia sigue valiendo con más fuerza**: la salida de una generación se convierte directamente en rutina `PROPUESTA`, y sigue sin haber un estado intermedio.
- **La sesión conserva sus cuatro transiciones** —iniciar, reanudar, cerrar por inactividad, finalizar—, ahora reunidas bajo un único requisito (RF-027 absorbe RF-032 y RF-033). El autómata de §4 es la especificación de ese requisito y no se toca.
- **La sesión pierde el desbloqueo por el entrenador** (RF-117, diferido con RF-034): el plazo de corrección vuelve a ser absoluto, con el coste que CB-70 describía.
- **`RutinaAsignada.origen` pierde `PRESET_ELEGIDO_POR_ALUMNO`**: quedan `PLANTILLA_ENTRENADOR` y `GENERADA`.

**Cambios de la v1.0:** ciclo de la invitación · estado `DESCARTADA` de rutina, que faltaba y dejaba indefinido un caso frecuente · desbloqueo excepcional de sesión · aclaración de que una versión nueva no transiciona la rutina · corrección del diagrama de rutina, cuya flecha de rechazo apuntaba al estado equivocado.

**Cambios de la v2.0:** se declara que el **candidato de rutina** (D5/RN-124) no es un estado de este ciclo, y por qué no se agrega uno.

**Cambios de la v2.1:** se incorporan los estados técnicos de solicitudes, intentos y candidatos generativos, separados del ciclo de vida de la rutina.

Las transiciones prohibidas importan tanto como las permitidas: cada una evita un defecto que de otro modo aparece en producción.

---

#### 1. Invitación

```
   emitida ──▶ VIGENTE ──┬──▶ USADA      (terminal, produce un usuario)
                         ├──▶ REVOCADA   (terminal, decisión del emisor)
                         └──▶ CADUCADA   (terminal, 14 días)
```

| Estado   | Significado                                                | Quién provoca la entrada                   |
| -------- | ---------------------------------------------------------- | ------------------------------------------ |
| VIGENTE  | Habilita a crear una cuenta en ese gimnasio con esos roles | Administrador, o entrenador con rol ALUMNO |
| USADA    | Ya produjo un usuario                                      | La persona invitada                        |
| REVOCADA | Anulada antes de usarse                                    | Administrador o el emisor                  |
| CADUCADA | Venció sin usarse                                          | Sistema, a los 14 días (RN-02b)            |

**Transiciones imposibles:** usar dos veces la misma invitación (RI-19) · revocar o caducar una invitación ya usada, porque el usuario ya existe y su alta no se deshace: para retirarlo se suspende o se da de baja la cuenta · modificar los roles de una invitación ya usada, porque cambiarían los permisos de un usuario existente sin auditarlo como cambio de rol.

#### 2. Rutina

```
   solicitud (entrenador, alumno o generación)
                  │
                  ▼
            ┌───────────┐  revisión desfavorable   ┌────────────┐
            │ PROPUESTA │ ────────────────────────▶│ RECHAZADA  │ (terminal)
            └─────┬─────┘                          └────────────┘
   revisión       │  │
   favorable      │  └── otra solicitud ──▶ ┌────────────┐
                  │                          │ DESCARTADA │ (terminal)
                  ▼                          └────────────┘
            ┌───────────┐
            │  VIGENTE  │◀── (una versión nueva NO transiciona la rutina)
            └─────┬─────┘
   otra rutina    │
   entra en       ▼
   vigencia  ┌────────────┐
             │ ARCHIVADA  │ (terminal)
             └────────────┘

            ┌────────────┐   el alumno queda sin entrenador vigente
            │ BLOQUEADA  │◀──────────── desde PROPUESTA
            └─────┬──────┘
                  └──▶ vuelve a PROPUESTA al reasignarse un entrenador
```

| Estado     | Significado                                                                           | Quién provoca la entrada                                                                                   |
| ---------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| PROPUESTA  | Rutina completa asociada al alumno, sin efecto. Visible para el alumno, no ejecutable | Entrenador, alumno al **confirmar** una rutina generada —o un preset opcional—, sistema (RF-087)            |
| BLOQUEADA  | Propuesta sin aprobador porque el alumno no tiene entrenador vigente                  | Sistema, al finalizar la asignación (RN-23)                                                                |
| VIGENTE    | Rutina bajo la cual el alumno puede iniciar sesiones                                  | Entrenador, mediante revisión favorable                                                                    |
| RECHAZADA  | Revisión desfavorable, con motivo. El alumno puede solicitar otra                     | Entrenador                                                                                                 |
| DESCARTADA | Fue sustituida por otra solicitud antes de ser revisada                               | Quien solicitó la nueva (RN-36a)                                                                           |
| ARCHIVADA  | Fue vigente y otra la sustituyó. Consultable, no ejecutable                           | Sistema                                                                                                    |

**El candidato de rutina no es un estado.** Lo que el solicitante ajusta antes de enviar a revisión (RN-124, D5/§5.2) no es una `RutinaAsignada`: no se persiste como rutina, no transiciona y desaparece si no se confirma. La rutina nace directamente en PROPUESTA, al confirmarse el candidato. **No se agrega un estado BORRADOR**: sería un estado sin efecto, sin aprobador y sin historial que preservar, y obligaría a decidir qué hacer con los borradores que nadie confirma. Ver D11/DD-33.

**Transiciones imposibles**

| Transición                                                                         | Por qué                                                                                                                             |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| PROPUESTA → VIGENTE sin revisión favorable de un entrenador con asignación vigente | RN-35. Es la regla que el cliente definió como indelegable                                                                          |
| RECHAZADA o DESCARTADA → cualquier estado                                          | Terminales. Para volver a intentarlo se solicita una rutina nueva, y así el historial muestra cada intento por separado             |
| ARCHIVADA → VIGENTE                                                                | Reactivarla reabriría el cálculo de adherencia de un período cerrado. Se solicita una nueva a partir de la misma plantilla          |
| VIGENTE → RECHAZADA o → PROPUESTA                                                  | Lo que ya rige no se rechaza ni vuelve a estar pendiente: se sustituye poniendo otra en vigencia, o se ajusta generando una versión |
| Dos rutinas VIGENTE, o dos PROPUESTA, del mismo alumno                             | RI-06                                                                                                                               |
| BLOQUEADA → VIGENTE                                                                | Requiere pasar por PROPUESTA, es decir, requiere entrenador                                                                         |

**Una adaptación aceptada no transiciona la rutina.** Genera una versión nueva (§3) y la rutina sigue VIGENTE. La resolución de la propuesta por el entrenador **es** la revisión exigida por RN-35, y no se pide una segunda (RN-35a).

#### 3. Versión de rutina

```
   puesta en vigencia ──▶ VERSIÓN 1 (vigente)
                                │
        propuesta aceptada, o   │
        intervención directa    ▼
                          VERSIÓN 2 (vigente) · VERSIÓN 1 → SUPERSEDIDA
```

| Estado      | Significado                                                 |
| ----------- | ----------------------------------------------------------- |
| VIGENTE     | Estructura que rige hoy. Exactamente una por rutina (RI-07) |
| SUPERSEDIDA | Estructura que rigió en un período. Inmutable y consultable |

**Transiciones imposibles:** modificar una versión SUPERSEDIDA, que reescribiría el pasado bajo el cual se ejecutaron sesiones · volver a marcar vigente una versión anterior, en su lugar se genera una versión nueva con el contenido anterior para que el historial sea lineal y fechado · crear una versión sin propuesta resuelta ni intervención registrada de un entrenador, porque toda versión tiene autor y motivo.

#### 4. Sesión de entrenamiento

```
   inicio                 finalización              48 h
 ──────────▶ EN_CURSO ──────────────▶ COMPLETADA ────────▶ BLOQUEADA
                 │                         ▲                   │
                 │ 8 h sin actividad       │ desbloqueo del    │
                 ▼                         │ entrenador, 24 h  │
            ABANDONADA (terminal)          └───────────────────┘
```

| Estado     | Significado                                                     | Cuenta para indicadores              |
| ---------- | --------------------------------------------------------------- | ------------------------------------ |
| EN_CURSO   | Iniciada, con prescripción congelada, admite registro de series | No                                   |
| COMPLETADA | Finalizada por el alumno. Corregible durante 48 h (RN-58)       | Sí                                   |
| ABANDONADA | Cerrada por inactividad. Conserva lo registrado                 | No, salvo como señal de interrupción |
| BLOQUEADA  | Completada y fuera del plazo de corrección                      | Sí                                   |

**Desbloqueo excepcional.** A pedido del alumno, el entrenador con asignación vigente puede devolver una sesión BLOQUEADA al estado COMPLETADA por 24 horas, **una sola vez por sesión**, con registro de auditoría del motivo (RN-58a). Es la única vía de corregir un error detectado tarde; sin ella un error de tipeo contaminaba de forma permanente la carga máxima estimada, el diagnóstico y toda la cadena de adaptación.

**Transiciones imposibles**

| Transición                                                          | Por qué                                                                                                        |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| ABANDONADA → EN_CURSO                                               | Reanudar una sesión de hace días falsearía la fecha de ocurrencia. Se registra una sesión diferida             |
| COMPLETADA → EN_CURSO                                               | El estado en curso implica una prescripción abierta; corregir no es reabrir                                    |
| BLOQUEADA → COMPLETADA sin intervención registrada de un entrenador | El plazo de corrección es lo que hace estables los indicadores; la excepción existe pero es nominal y auditada |
| Desbloquear dos veces la misma sesión                               | RN-58a. Sin el límite, el plazo de corrección no existiría                                                     |
| Dos sesiones EN_CURSO del mismo alumno                              | RN-50                                                                                                          |
| Iniciar una sesión en tiempo real sobre una rutina no VIGENTE       | RN-51                                                                                                          |
| Modificar la prescripción congelada, en cualquier estado            | RN-61                                                                                                          |

**Sobre ABANDONADA.** Sus series registradas se conservan y son visibles en el historial, marcadas como tales. Descartarlas perdería evidencia de interrupción, que es una señal de comportamiento relevante para el diagnóstico.

#### 5. Propuesta de adaptación

```
   diagnóstico ──▶ PENDIENTE ──┬──▶ ACEPTADA_TOTAL      ─▶ genera versión
                       │        ├──▶ ACEPTADA_PARCIAL    ─▶ genera versión
                       │        ├──▶ RECHAZADA           ─▶ no genera versión
                       │        └──▶ INVALIDADA          ─▶ el contexto cambió
                       │
                       ├── 30 días sin resolver ──▶ CADUCADA
                       └── alumno sin entrenador ──▶ BLOQUEADA ──▶ vuelve a PENDIENTE
```

| Estado                            | Significado                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| PENDIENTE                         | Esperando la revisión del entrenador                                                                                   |
| BLOQUEADA                         | Sin aprobador por falta de asignación vigente                                                                          |
| ACEPTADA_TOTAL / ACEPTADA_PARCIAL | Resuelta favorablemente. Generó una versión nueva                                                                      |
| RECHAZADA                         | Resuelta desfavorablemente, con motivo registrado                                                                      |
| INVALIDADA                        | El contexto del alumno cambió y la propuesta dejó de ser compatible antes de resolverse. Se genera una propuesta nueva |
| CADUCADA                          | Venció sin resolución. El hecho se registra                                                                            |

**Transiciones imposibles:** aplicarse sin resolución favorable (RN-86, el principio central del producto) · resolverla el propio alumno (RA-07) · reabrir una propuesta resuelta, caducada o invalidada, porque el historial de adaptaciones sería ininterpretable si las propuestas mutaran · generar dos versiones a partir de una misma propuesta.

#### 6. Ejercicio del catálogo

```
  carga inicial ─────────────────────────▶ APROBADO ⇄ DESACTIVADO
  creación por entrenador ──▶ PROPUESTO ───┤
                                           └──▶ RECHAZADO (terminal)
```

| Estado      | Visible en búsquedas           | Prescribible                                                       |
| ----------- | ------------------------------ | ------------------------------------------------------------------ |
| PROPUESTO   | Sólo para su autor             | No                                                                 |
| APROBADO    | Sí                             | Sí, si su equipamiento está en el inventario del gimnasio (RN-116) |
| RECHAZADO   | Sólo para su autor, con motivo | No                                                                 |
| DESACTIVADO | No                             | No, pero permanece en rutinas y sesiones existentes (RN-29)        |

**Transiciones imposibles:** borrado físico en cualquier estado (RN-27) · modificación de un ejercicio del catálogo base por cualquier usuario (RN-24) · desactivación que altere registros históricos que lo referencian.

#### 7. Estado de compatibilidad de un ejercicio dentro de una rutina

No es un ciclo de vida sino una **clasificación recalculada** en cada verificación (RN-45), persistida para que la marca esté disponible sin recalcular.

| Valor                 | Se asigna cuando                                                                                                          | Efecto                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| COMPATIBLE            | Ninguna regla de D5/§6 lo objeta                                                                                          | Ninguno                                                          |
| ADVERTIDO             | Contraindicado por una condición de severidad `LEVE`                                                                      | Se señala; no impide                                             |
| INCOMPATIBLE          | Contraindicado con severidad `MODERADA` o `SEVERA`, o nivel superior al del alumno, o equipamiento ausente del inventario | Impide poner la rutina en vigencia; genera ajuste de sustitución |
| EJERCICIO_DESACTIVADO | El ejercicio fue desactivado del catálogo                                                                                 | Se señala; puede ejecutarse; genera ajuste de sustitución        |

**Nunca se retira un ejercicio automáticamente por cambiar su estado de compatibilidad.** Retirarlo es decisión del entrenador (RN-92).

#### 8. Asignación entrenador–alumno

| Estado     | Significado                                                  |
| ---------- | ------------------------------------------------------------ |
| VIGENTE    | `hasta` sin informar. Habilita todo el acceso del entrenador |
| FINALIZADA | `hasta` informado. Terminal e inmutable                      |

**Transiciones imposibles:** reactivar una asignación finalizada, en su lugar se crea una nueva para que el historial refleje la discontinuidad · dos asignaciones vigentes del mismo alumno (RN-18) · una asignación de un entrenador consigo mismo (RN-22).

#### 9. Usuario

```
   ACTIVO ⇄ SUSPENDIDO
      │           │
      └─────┬─────┘
            ▼
      DADO_DE_BAJA (terminal, con anonimización)
```

| Estado       | Puede autenticarse | Sus datos                                                                                 |
| ------------ | ------------------ | ----------------------------------------------------------------------------------------- |
| ACTIVO       | Sí                 | Íntegros                                                                                  |
| SUSPENDIDO   | No                 | Íntegros. Las asignaciones no se alteran: la suspensión es reversible                     |
| DADO_DE_BAJA | No                 | Anonimizados dentro de 7 días. Sesiones y series conservadas sin vínculo con la identidad |

**Transiciones imposibles:** DADO_DE_BAJA → cualquier otro estado · suspender destruyendo asignaciones · dar de baja sin conservar los registros de entrenamiento desvinculados (RN-106) · suspender o dar de baja al último administrador activo del gimnasio (RN-03a, RI-23).

#### 10. Entidades sin ciclo de vida

**Aptitud.** Su condición es derivada de la fecha: vigente si su vencimiento no fue superado, vencida en caso contrario, ausente si no hay ninguna registrada. Se modela como derivada y no como estado persistido porque un estado persistido exigiría un proceso que lo actualice, y quedaría desactualizado exactamente el día que importa. **Los tres casos se distinguen siempre** y nunca se colapsan en "no tiene aptitud": ausente y vencida requieren acciones distintas.

**Diagnóstico y salidas fechadas de un componente.** Cada cálculo produce un registro nuevo, fechado y con la versión del componente. No se actualizan ni se borran. El vigente es el de fecha más reciente. **Si nunca se ejecutó ningún cálculo**, la información se presenta como no disponible y ninguna funcionalidad se degrada (RNF-12). Ése es el caso normal el primer día del sistema, no una anomalía. *(La estimación de riesgo de abandono y la segmentación se retiraron del alcance — D11/DD-34; la descripción de perfil, RF-064, es efímera y no genera registros.)*

**Récord personal.** Tiene un indicador de vigencia, no estados: un récord deja de ser vigente cuando otro lo supera, o cuando el recálculo de RN-71 lo desplaza. Los superados se conservan para poder dibujar la progresión.

#### 11. Solicitud, intento y candidato generativo

##### Solicitud generativa

```text
PENDIENTE → PROCESANDO ─┬→ COMPLETADA
     ▲                  ├→ NO_DISPONIBLE
     └─ lease vencido ──┘

PENDIENTE o PROCESANDO → CANCELADA
```

| Estado         | Significado |
| -------------- | ----------- |
| PENDIENTE      | Disponible para que un worker la reclame |
| PROCESANDO     | Reclamada mediante un lease temporal |
| COMPLETADA     | Tiene un resultado estructural que backend puede validar |
| NO_DISPONIBLE  | Agotó dos intentos sin resultado válido |
| CANCELADA      | El solicitante abandonó antes de obtener un resultado utilizable |

Un lease vencido devuelve la solicitud a `PENDIENTE` sin perder el intento registrado. `COMPLETADA`, `NO_DISPONIBLE` y `CANCELADA` son terminales.

##### Intento generativo

```text
PENDIENTE → PROCESANDO ─┬→ COMPLETADO
                        ├→ FALLIDO
                        ├→ AGOTADO_POR_TIEMPO
                        └→ SALIDA_INVALIDA
```

Cada solicitud admite como máximo dos intentos. Los cuatro estados de salida son terminales para el intento; tras el primer fallo la solicitud vuelve a `PENDIENTE`, y tras el segundo pasa a `NO_DISPONIBLE`.

##### Candidato técnico

`ACTIVO` pasa a `CONFIRMADO` cuando el backend crea la rutina `PROPUESTA`, o a `ABANDONADO` por decisión del solicitante o después de 24 horas sin actividad. Cada ajuste o regeneración renueva ese plazo. Estos valores son estados técnicos del objeto temporal y no agregan estados al ciclo de `RutinaAsignada`.


---

<a id="d10"></a>

### D10 — Catálogo de casos borde

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/domain/edge-cases.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D10`

|                |                                        |
| -------------- | -------------------------------------- |
| **Versión**    | 2.1                                    |
| **Fecha**      | 2026-08-24                             |
| **Estado**     | Normativo                              |
| **Depende de** | D5 (reglas), D6 (estados), D7 (flujos) |

**Cambios de la v1.0:** los cinco casos que remitían a reglas inexistentes ahora remiten a reglas reales (CB-13, CB-16, CB-21, CB-22, CB-32) · las dos decisiones pendientes quedan cerradas y convertidas en reglas (CB-53, CB-55) · casos nuevos de invitación, inventario, arranque, entrenador que entrena y corrección tardía.

**Cambios de la v2.0:** CB-72 y CB-73, del candidato de rutina (D5/RN-124 a RN-129).

Este documento **no reescribe** reglas ni flujos: los referencia. Si un comportamiento cambia, cambia en D5 o D7 y aquí sólo cambia la referencia.

---

#### A · Estados iniciales y vacíos

| ID    | Escenario                                                                             | Comportamiento esperado                                                                                                                                                                                          | Regla                |
| ----- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| CB-01 | Alumno recién creado, sin nada                                                        | Ve su rutina propuesta y el aviso de que espera revisión. Ninguna vista de indicadores muestra cero: todas declaran qué falta y cuánto                                                                           | RN-73, RF-051, FL-01 |
| CB-02 | Panel del alumno sin ninguna sesión                                                   | Cada bloque explica qué falta: la primera sesión habilita el volumen; hacen falta cuatro sesiones del mismo ejercicio para diagnosticar                                                                          | RN-73, RN-79a        |
| CB-03 | Representación muscular sin ninguna sesión                                            | Todos los grupos en estado "sin datos", visualmente distinto de volumen nulo                                                                                                                                     | RN-30, RF-049        |
| CB-04 | Alumno con una sola sesión                                                            | Volumen y representación muscular ya se calculan. Progresión, adherencia y diagnóstico se declaran no disponibles                                                                                                | RN-68, RN-79a        |
| CB-05 | Adherencia antes de las dos primeras semanas                                          | No se calcula. La cartera muestra "aún sin adherencia", no 0%                                                                                                                                                    | RN-68                |
| CB-06 | Mediciones con un solo registro                                                       | Se muestra el punto, no se dibuja tendencia                                                                                                                                                                      | FL-14/E1             |
| CB-07 | Cartera de entrenador sin alumnos                                                     | Estado explicativo con la acción a seguir. No una tabla vacía                                                                                                                                                    | FL-13/E2             |
| CB-08 | Gimnasio sin ninguna sesión registrada                                                | El panel declara que no hay actividad. Retención por cohorte y ocupación horaria no se dibujan vacías                                                                                                            | RN-73, FL-21/E1      |
| CB-09 | Primera ejecución de un ejercicio: no hay valores previos                             | Se precarga la carga sugerida de la prescripción, o el campo queda vacío. **Nunca cero**                                                                                                                         | FL-05/A4             |
| CB-10 | Alumno con contexto insuficiente                                                      | No se produce ninguna decisión automática. Se declara exactamente qué falta y se solicita                                                                                                                        | RN-97b, RF-111       |
| ~~CB-11~~ | ⏸ **Sin sujeto.** La estimación de riesgo se retiró del alcance ([D11/DD-34](#d11), confirmado por la votación con 1/8). Antes: estimación de riesgo nunca calculada para nadie                                       | La columna dice "no disponible" en toda la cartera; el orden se resuelve con los criterios restantes de RF-107                                                                                                   | RN-100, FL-13/E1     |
| CB-59 | **Gimnasio recién aprovisionado**: un administrador, ningún entrenador, ningún alumno | El administrador puede emitir invitaciones y declarar el inventario, y nada más. El sistema le indica los dos pasos que faltan para que alguien pueda entrenar: al menos un entrenador y un inventario declarado | FL-00, RN-115        |
| CB-60 | **Inventario vacío**                                                                  | Sólo son prescribibles los ejercicios de peso corporal. Se advierte al administrador con la lista de patrones no cubiertos                                                                                       | RN-118, FL-20/E2     |

#### B · Cambios en el tiempo

| ID    | Escenario                                                                                   | Comportamiento esperado                                                                                                                                                                                                 | Regla                         |
| ----- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| CB-13 | Se desactiva un ejercicio presente en rutinas vigentes                                      | El ejercicio permanece y puede ejecutarse; pasa a `EJERCICIO_DESACTIVADO` y genera un ajuste de sustitución. Los registros históricos no se tocan                                                                       | RN-27 a RN-29, RN-89a, RF-101 |
| CB-14 | Se crea una versión nueva mientras el alumno tiene una sesión en curso                      | La sesión conserva su prescripción congelada y se completa sin alteración. La versión nueva rige desde la sesión siguiente                                                                                              | RN-52, RN-61, RN-89           |
| CB-15 | Sesión diferida cuya fecha cae bajo una rutina archivada                                    | Se admite y se imputa a la rutina y a la versión vigentes en esa fecha. La restricción de rutina vigente rige sólo para sesiones iniciadas en tiempo real                                                               | RN-51, RN-59, FL-08           |
| CB-16 | Una propuesta pendiente deja de ser compatible porque el alumno declaró una condición nueva | La propuesta pasa a `INVALIDADA` con su motivo y se genera una nueva sobre el contexto actualizado                                                                                                                      | RN-85, RN-91, D6/§5           |
| CB-17 | El alumno cierra una condición física que restringía su rutina                              | Los ejercicios dejan de estar marcados desde la fecha de cierre. **Nada se recalcula hacia atrás**: las prescripciones y sesiones pasadas fueron correctas cuando ocurrieron                                            | RN-11                         |
| CB-18 | La aptitud vence durante un período de entrenamiento activo                                 | Aviso 30 días antes y el día del vencimiento. Desde entonces, advertencia al iniciar cada sesión. Ninguna sesión anterior se invalida y ninguna operación se impide                                                     | RN-12, RN-13, RN-13b          |
| CB-19 | Cambian las constantes de cálculo entre dos versiones del sistema                           | Los indicadores se recalculan con la definición nueva, porque son derivados. Los diagnósticos, propuestas y estimaciones ya emitidos **no** se recalculan: conservan la versión del componente con la que se produjeron | PD-03, RN-98                  |
| CB-61 | **El administrador retira del inventario un equipamiento usado por muchas rutinas**         | Los ejercicios afectados pasan a `INCOMPATIBLE` en todas las rutinas vigentes, se genera una propuesta de sustitución por alumno, y ninguna sesión ni rutina se interrumpe                                              | RN-117, FL-20/A2              |
| CB-62 | **El administrador incorpora equipamiento nuevo**                                           | El catálogo prescribible crece; los ejercicios marcados por equipamiento vuelven a `COMPATIBLE` y las propuestas abiertas por ese motivo se invalidan                                                                   | RN-117, FL-20/A1              |

#### C · Datos ausentes, degradados o sin respuesta válida

| ID    | Escenario                                                                                      | Comportamiento esperado                                                                                                                                                                                                                                                                               | Regla                    |
| ----- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| CB-12 | Un ejercicio del catálogo no tiene ninguna clasificación muscular                              | Se marca no clasificado y entra en la cola de curación. No aporta volumen, y esa ausencia se distingue de aportar cero en toda vista                                                                                                                                                                  | RN-30, RF-099, FL-17/E2  |
| CB-20 | La generación de rutina no produce salida válida                                               | Un reintento; si vuelve a fallar o vence el límite, se declara generación no disponible. No se propone una rutina inválida ni determinística. **La vía que queda es que un entrenador cree y asigne una plantilla propia** (RF-019); si el gimnasio no tiene ninguna, el alumno queda sin rutina — [DD-35](#d11), D12/R-17                                              | RN-95b, RN-99, RF-113    |
| CB-21 | Un ejercicio es incompatible y **no existe alternativa admisible** en el catálogo prescribible | Se declara explícitamente: no hay alternativa con las condiciones del alumno y el inventario del gimnasio. Se ofrece omitirlo y la decisión queda en el entrenador. El ajuste de sustitución no se propone y el hecho consta en la propuesta. **No inventa, no oculta, no propone algo incompatible** | RN-49, RN-49a, FL-09/E4  |
| CB-22 | El catálogo prescribible no cubre los patrones mínimos que exige el tipo de rutina             | Se genera la rutina posible, se declara qué patrones quedaron sin cubrir, y se avisa al administrador porque es un problema de inventario, no del alumno                                                                                                                                              | RN-118, RN-39a, FL-20/E1 |
| CB-23 | El alumno declara como motivo de sustitución una molestia física                               | El sistema **sugiere** registrarla como condición física con su zona corporal y su severidad. **No la registra por su cuenta**: una condición inferida contaminaría el contexto y todas las prescripciones futuras                                                                                    | RN-10a, FL-06/E2         |
| CB-63 | **El esfuerzo percibido no fue registrado nunca**                                              | El diagnóstico se produce igual, sin ese criterio, y declara explícitamente que no pudo evaluar sobreexigencia por esfuerzo ni estímulo insuficiente por esfuerzo                                                                                                                                     | RN-81, RN-79a            |
| CB-64 | **La condición física tiene descripción libre pero zona corporal no declarada**                | No se acepta: zona y severidad son obligatorias y tipadas. La descripción libre es complementaria y no participa de ningún cálculo                                                                                                                                                                    | RN-10a                   |

#### D · Interrupción y reanudación

| ID    | Escenario                                                                              | Comportamiento esperado                                                                                            | Regla            |
| ----- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------- |
| CB-24 | Se pierde la conexión durante el registro de series                                    | Lo ingresado se conserva localmente y se reintenta. Al recuperar, se sincroniza sin duplicar                       | RN-60, RNF-10    |
| CB-25 | El alumno cierra la aplicación a mitad de sesión y vuelve al rato                      | Retoma en el punto exacto, con las series registradas conservadas                                                  | FL-07            |
| CB-26 | Vuelve pasadas más de 8 horas                                                          | La sesión ya está abandonada, con lo registrado conservado y visible. Se le ofrece registrar una sesión diferida   | RN-53, FL-07/E1  |
| CB-27 | Abandona la puesta en contexto a mitad de camino                                       | Lo declarado se conserva. Al volver, retoma donde quedó. No se genera rutina hasta alcanzar contexto suficiente    | RN-97b, FL-01/E1 |
| CB-65 | **Una invitación queda a medio usar**: la persona abre el enlace y no completa el alta | La invitación sigue VIGENTE hasta caducar o revocarse. No hay usuario a medio crear                                | D6/§1            |
| CB-73 | **El solicitante abandona un candidato de rutina a medio ajustar**                     | No deja rutina, aviso ni propuesta descartada: lo que no se confirmó no ocurrió. Si vuelve, empieza otra solicitud | RN-124, FL-04/A6 |

#### E · Concurrencia

| ID    | Escenario                                                                           | Comportamiento esperado                                                                                                                                         | Regla           |
| ----- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| CB-28 | El entrenador modifica la rutina mientras el alumno inicia una sesión               | Ambas operaciones se completan. La sesión toma la versión vigente en el instante del inicio y la congela                                                        | RN-52           |
| CB-29 | Dos entrenadores actúan sobre el mismo alumno                                       | Imposible por construcción: sólo hay un entrenador vigente                                                                                                      | RN-18           |
| CB-30 | La misma propuesta se resuelve dos veces                                            | La segunda resolución se rechaza indicando que ya fue resuelta y por quién. No genera una segunda versión                                                       | RN-86, D6/§5    |
| CB-66 | **El administrador cambia el inventario mientras un entrenador aprueba una rutina** | La aprobación revalida contra el inventario en el instante de confirmar. Si un ejercicio pasó a incompatible, la aprobación se impide y se ofrecen alternativas | FL-02/E5, RN-45 |

#### F · Permisos en los bordes

| ID    | Escenario                                                                          | Comportamiento esperado                                                                                                                                                                                                                                                                                                                 | Regla                |
| ----- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| CB-31 | La asignación termina mientras el entrenador revisa una rutina o una propuesta     | La confirmación se rechaza en ese instante, con explicación. Lo pendiente queda BLOQUEADO y pasa al entrenador entrante                                                                                                                                                                                                                 | RA-04, RN-23         |
| CB-32 | El alumno queda sin entrenador y tiene una incompatibilidad activa                 | Sigue pudiendo entrenar y sigue recibiendo la advertencia en cada sesión. La propuesta queda BLOQUEADA. El administrador es señalado                                                                                                                                                                                                    | RN-92, RN-93, RF-112 |
| CB-33 | Un actor con rol de entrenador y de administrador consulta a un alumno no asignado | Accede sólo a lo que la matriz concede al rol de administrador. Tener dos roles no acumula accesos de forma implícita                                                                                                                                                                                                                   | RA-05                |
| CB-34 | Un usuario accede por enlace directo a un recurso de otro alumno                   | Rechazo, con mensaje genérico que no revela si el recurso existe                                                                                                                                                                                                                                                                        | RA-01, RNF-14        |
| CB-67 | **Un entrenador quiere entrenar**                                                  | Necesita que el administrador le asigne **otro** entrenador; entonces se le aplican íntegramente las reglas del alumno. No puede autoasignarse ni aprobarse a sí mismo. Si es el único entrenador del gimnasio, no puede tener rutina vigente y el sistema lo señala al administrador como caso a resolver incorporando otro entrenador | RN-22, RN-22a, DD-28 |
| CB-68 | **Un entrenador intenta invitar con rol de entrenador o administrador**            | Rechazo: sólo puede invitar con rol ALUMNO                                                                                                                                                                                                                                                                                              | RN-02d, RA-10        |

#### G · Fallos de dependencias

| ID    | Escenario                                                                      | Comportamiento esperado                                                                                                                                         | Regla          |
| ----- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| CB-35 | El proceso periódico de diagnóstico o de estimación nunca se ejecutó           | No hay diagnósticos ni estimaciones. Todas las vistas funcionan y declaran la información como no disponible. Ninguna funcionalidad se degrada                  | RN-100, RNF-12 |
| CB-36 | API IA, ngrok o LLM están caídos, lentos o devuelven algo inesperado            | Tras un reintento la generación queda no disponible, sin detalles técnicos. El resto y las operaciones manuales continúan funcionando ✎ *(los presets dejan de ser la contingencia: RF-021 es alcance opcional)*                            | RN-95b, RN-99, RF-058 |
| CB-37 | La fuente externa del catálogo cambió de estructura o no responde              | La carga falla de forma completa y verificable. **No deja un catálogo a medias**, porque un catálogo parcial produce volumen incorrecto de forma silenciosa     | FL-17/E1       |
| CB-69 | **El correo de invitación no llega**                                           | La invitación existe y sigue vigente. El emisor puede reenviarla o revocarla y emitir otra. El alta no depende de un único envío                                | D6/§1          |

#### H · Bajas y eliminaciones

| ID    | Escenario                                                                             | Comportamiento esperado                                                                                                                                 | Regla          |
| ----- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| CB-38 | Un alumno se da de baja y sus sesiones alimentan la retención por cohorte             | Se anonimizan sus datos personales; sesiones y series se conservan desvinculadas. La analítica agregada no se invalida y la identidad no es recuperable | RN-106, RF-105 |
| CB-39 | El único administrador activo del gimnasio se da de baja, se suspende o pierde el rol | Se rechaza en los tres casos hasta que exista otro administrador. Un gimnasio sin administrador es un estado del que no se puede salir                  | RN-03a, RI-23  |
| CB-40 | Se elimina un ejercicio referenciado por miles de registros                           | No se elimina. Se desactiva                                                                                                                             | RN-27          |
| CB-41 | Un entrenador se da de baja con alumnos asignados                                     | Sus asignaciones se finalizan, sus alumnos quedan señalados al administrador, sus plantillas publicadas permanecen disponibles                          | FL-18/E3       |

#### I · Límites y valores extremos

| ID    | Escenario                                                                       | Comportamiento esperado                                                                                                                                                 | Regla                   |
| ----- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| CB-42 | Carga cero en una serie                                                         | Válida: los ejercicios de peso corporal existen. Aporta volumen; no aporta carga máxima estimada; su único tipo de récord posible es por repeticiones                   | RN-55, RN-65, RN-70a    |
| CB-43 | Carga negativa, o más de 100 repeticiones                                       | Rechazo del lado del servidor con el rango admitido en el mensaje                                                                                                       | RN-55                   |
| CB-44 | Serie de 30 repeticiones                                                        | Se registra y aporta volumen. **No se calcula carga máxima estimada**: por encima de 12 repeticiones la estimación no es fiable                                         | RN-65                   |
| CB-45 | Fecha de sesión o de medición en el futuro, o anterior a 90 días                | Rechazo indicando el rango admitido                                                                                                                                     | RN-16, RN-59            |
| CB-46 | Sesión iniciada a las 23:30 y finalizada a las 00:40                            | Se imputa a la fecha de inicio en la zona horaria del gimnasio. Un entrenamiento no se parte en dos días                                                                | RN-110                  |
| CB-47 | Alumno en otra zona horaria que la del gimnasio                                 | Todo se calcula y se presenta en la zona horaria del gimnasio. Una única definición de día y de semana para todos                                                       | RN-110                  |
| CB-48 | Cargas con más de dos decimales                                                 | Se redondean a 0,01 al ingresar. El redondeo ocurre una sola vez, nunca en cada cálculo                                                                                 | D2/§3                   |
| CB-49 | Alumno con diez mil sesiones                                                    | Las vistas siguen dentro de RNF-01 y RNF-02. Los históricos se presentan por ventana                                                                                    | RNF-01                  |
| CB-50 | Rutina con siete días y treinta ejercicios por día                              | Se rechaza: excede los rangos del tipo de rutina, y la frecuencia 7 no tiene estructura admisible                                                                       | RN-39a, RN-41           |
| CB-72 | **El alumno agota el tope de regeneraciones del candidato sin quedar conforme** | Confirma el último candidato, o deriva la construcción a su entrenador adjuntando como comentario lo que no lo convence. **No se le muestra un error ni queda sin vía** | RN-127, RN-99, FL-04/E5 |

#### J · Comportamiento absurdo pero posible

| ID    | Escenario                                                                                | Comportamiento esperado                                                                                                                                                                                                                                          | Regla                   |
| ----- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| CB-51 | Un alumno nunca usa el sistema                                                           | No genera indicadores. Aparece en la cartera con "sin actividad" y días desde el alta. La estimación de riesgo lo considera si tiene antigüedad suficiente; si no, se declara sin datos                                                                          | RN-77, CB-11            |
| CB-52 | Un alumno registra ocho sesiones en un día                                               | Se admiten. La adherencia se acota al 100% y no premia el exceso. El diagnóstico puede clasificarlo como sobreexigencia                                                                                                                                          | RN-67, RN-79a           |
| CB-53 | Un alumno carga una carga muy superior a su histórico                                    | Si supera el 150% de su mejor marca en ese ejercicio, se marca como **registro atípico** y se pide confirmación explícita. Confirmado, se registra con normalidad y puede producir récord; sin confirmar, no se registra                                         | RN-55a                  |
| CB-54 | Un alumno empeora de forma sostenida                                                     | El diagnóstico lo clasifica como estancamiento o sobreexigencia y produce la propuesta correspondiente. El sistema **no** presenta el empeoramiento como progreso ni lo oculta                                                                                   | RN-79a, RN-89a          |
| CB-55 | Un alumno completa siempre el 100% de las repeticiones con esfuerzo percibido bajo       | Se clasifica como `ESTIMULO_INSUFICIENTE` y el ajuste es un aumento de carga. Sin esa situación, el caso caía en estancamiento y recibía el ajuste equivocado                                                                                                    | RN-79a, RN-89a          |
| CB-56 | Un alumno ejecuta los días de su rutina siempre en otro orden                            | Se admite: la rutina es cíclica, no un calendario. La propuesta del siguiente día es una sugerencia                                                                                                                                                              | RN-42                   |
| CB-57 | El entrenador rechaza sistemáticamente todas las propuestas                              | Se registra cada rechazo con su motivo. La proporción de rechazo es un indicador de la calidad del diagnóstico y es visible en la evaluación de componentes                                                                                                      | RN-90, D1/E4            |
| CB-58 | Un caso sin ninguna respuesta válida disponible                                          | El sistema lo declara explícitamente y transfiere la decisión a una persona, con toda la información que reunió. **Nunca produce una respuesta arbitraria para no quedarse callado**                                                                             | RN-49, CB-21            |
| CB-70 | **Un alumno detecta hace un mes un error de carga que le produjo un récord falso**       | Pide a su entrenador el desbloqueo de esa sesión. El entrenador la reabre por 24 h, una sola vez, con motivo auditado. Corregida la serie, el récord se recalcula sobre el histórico completo y puede restaurarse el anterior o quedar el ejercicio sin récord   | RN-58a, RN-71, FL-08/A2 |
| CB-71 | **Un alumno declara una condición severa que afecta a casi todos los grupos musculares** | Casi toda la rutina queda incompatible y la propuesta implica una rutina sustancialmente nueva. Si no hay alternativas suficientes, se aplica CB-21 y CB-22: el sistema lo declara y deriva al entrenador. **No construye una rutina vacía ni una incompatible** | RN-49, RN-92, FL-12/E1  |

---

#### Cierre de las decisiones pendientes de la v1.0

| ID    | Cuestión                                                      | Resolución                                                                                                                                                                                                                                                         |
| ----- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CB-53 | ¿Alertar sobre valores atípicos dentro de rango?              | **Resuelta:** confirmación explícita por encima del 150% del mejor histórico (RN-55a). No bloquea, es barata, y evita que un error de tipeo produzca un récord falso que distorsione la progresión, el diagnóstico y toda la cadena de adaptación                  |
| CB-55 | ¿"Estímulo insuficiente" es una situación diagnóstica propia? | **Resuelta:** sí, incorporada como quinta situación (D2/§4.9, RN-79a) con su regla de ajuste propia (RN-89a). Es la contraparte simétrica de la sobreexigencia; sin ella, el caso más frecuente de estancamiento por defecto de carga recibía el ajuste equivocado |


---

<a id="parte-iv"></a>

## Parte IV — Flujos funcionales

<a id="d7"></a>

### D7 — Flujos funcionales

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/flows/functional-flows.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D7`

|                |                    |
| -------------- | ------------------ |
| **Versión**    | 2.3                |
| **Fecha**      | 2026-09-01         |
| **Estado**     | Normativo          |
| **Depende de** | D2, D3, D4, D5, D6 |

**Cambios de la v1.0:** flujos nuevos FL-00 (aprovisionamiento), FL-19 (invitación), FL-20 (inventario), FL-21 (paneles agregados) · FL-01 rehecho: el alta es por invitación y el alumno ya no declara equipamiento · FL-08 corregido: la contradicción entre RN-51, RN-59 y el registro diferido bajo rutina archivada · FL-09 y FL-10 remiten a los criterios de D5/§9.1 y §9.2, que en la v1.0 no existían.

**Cambios de la v2.0:** FL-04 gana el **candidato de rutina** —el solicitante moldea la rutina generada antes de enviarla a revisión, a mano, pidiendo alternativas o volviendo al lenguaje natural (pasos 6 a 8, A3 a A7)— y FL-03 lo hereda. Ver D5/RN-124 a RN-129, D5/§5.2 y D11/DD-33.

**Cambios de la v2.3 ([baseline de alcance](#baseline)).** Ningún flujo del ciclo central cambia. Lo que cambia es qué flujos existen en la Etapa 1:

| Flujo                                          | Estado en la Etapa 1                                                                                                                                             |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **FL-03** · solicitud de rutina por el alumno  | ⏸ Diferido con RF-025 (3 votos de 8). La rutina la origina el entrenador o la incorporación del alumno                                                            |
| **FL-04** · generación asistida                | ✎ Se conserva **sin el paso de ajuste del candidato**: la salida válida se convierte directamente en rutina `PROPUESTA`. RN-124 a RN-129 quedan diferidas          |
| **FL-08** · registro diferido y desbloqueo     | ⏸ Diferido con RF-034 y RF-117                                                                                                                                    |
| **FL-21** · paneles agregados                  | ⏸ Diferido en su parte de panel del gimnasio (RF-068). El panel de cartera del entrenador (RF-052) queda en banda N3                                              |
| **FL-05** · ejecución de una sesión            | Sin cambios funcionales. Ahora es la especificación de un único requisito, RF-027, que absorbió RF-032 y RF-033                                                    |
| **FL-01, FL-02, FL-09, FL-10, FL-12** ⭐        | **Sin cambios.** Son el ciclo que el cliente declaró condición de aprobación                                                                                       |

**Y un cambio de comportamiento en FL-04 que no es de alcance sino de consecuencia:** su excepción por indisponibilidad generativa ya no puede remitir a los presets del gimnasio. La vía que queda es que el entrenador asigne una plantilla propia (RF-019, RF-058, [DD-35](#d11)). Si el gimnasio no tiene ninguna, **el flujo no tiene salida** y el alumno queda sin rutina.

**Cambios de la v2.2 (replanteo de IA, [D11/DD-34](#d11)):** FL-16 (estimación de riesgo de abandono) queda **derogado** al pasar RF-061 a RF-063 a WON'T · FL-13 pierde "riesgo de abandono alto" del orden de urgencia · el orden de las alternativas de sustitución en FL-04/A4 y FL-06 lo produce ahora la capa generativa, con el orden determinista de RN-49a como fallback.

Los cursos alternativos y de excepción no son un apéndice: son la mayor parte del trabajo.

---

#### FL-00 · Aprovisionamiento de un gimnasio afiliado

|                     |                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **Actor**           | Proveedor del sistema, fuera de la aplicación                                            |
| **Precondiciones**  | Afiliación acordada fuera del sistema                                                    |
| **Postcondiciones** | Gimnasio creado con su zona horaria, y un usuario con rol ADMINISTRADOR en estado activo |
| **Reglas**          | RN-02e, RN-03a, RI-23                                                                    |

**Curso normal.** Se crea el gimnasio con su nombre y zona horaria, y su primer administrador con una invitación de arranque que el propio aprovisionamiento marca como emitida. La persona completa su registro por FL-19.

**Excepción.** E1: un gimnasio queda creado sin administrador → estado inconsistente que el sistema debe impedir; la operación es atómica o no ocurre. E2: la dirección de correo del primer administrador ya pertenece a otro gimnasio → se admite: la unicidad del correo es por gimnasio (RN-02).

**Por qué está fuera de la aplicación.** El alta es por invitación y nadie dentro de un gimnasio nuevo puede emitir la primera. Modelarlo como funcionalidad exigiría un rol superadministrador multi-gimnasio, que está fuera de alcance. Ver D4/PD-08.

---

#### FL-19 · Invitación y alta de un usuario

|                     |                                                                              |
| ------------------- | ---------------------------------------------------------------------------- |
| **Actor**           | Administrador o entrenador · Persona invitada                                |
| **Precondiciones**  | El emisor pertenece al gimnasio y tiene el rol que lo habilita               |
| **Postcondiciones** | Usuario activo, vinculado al gimnasio emisor, con los roles de la invitación |
| **Reglas**          | RN-02a a RN-02d, RN-104, RA-09, RA-10                                        |

**Curso normal**

1. El emisor indica la dirección de correo y los roles a otorgar. Un entrenador sólo puede indicar ALUMNO.
2. El sistema crea la invitación en estado VIGENTE y la envía.
3. La persona la abre, define su contraseña y su nombre, y otorga el **consentimiento explícito y separado** para el tratamiento de datos de salud.
4. El usuario queda activo, vinculado a ese gimnasio, con exactamente los roles de la invitación. Si el emisor fue un entrenador, la asignación con él queda establecida.
5. Si tiene rol ALUMNO, continúa por FL-01.

**Cursos alternativos**

|                                               |                                                                                                                                                                                            |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A1 · El emisor revoca antes de que se use     | La invitación pasa a REVOCADA y el enlace deja de funcionar                                                                                                                                |
| A2 · La persona no otorga el consentimiento   | La cuenta se crea. No puede declarar condiciones ni mediciones y, por lo tanto, no alcanza contexto suficiente: no se le genera rutina. El sistema explica exactamente qué falta y por qué |
| A3 · El administrador invita con varios roles | Admitido. Los roles se otorgan juntos (RA-09)                                                                                                                                              |

**Cursos de excepción**

|                                                 |                                                                                               |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| E1 · La invitación caducó                       | Se informa y se ofrece solicitar una nueva al gimnasio. No se permite crear la cuenta         |
| E2 · Se intenta usar dos veces                  | Rechazo: es de un solo uso (RI-19)                                                            |
| E3 · El correo ya tiene cuenta en ese gimnasio  | Rechazo con mensaje genérico, sin revelar si el correo existe                                 |
| E4 · El correo ya tiene cuenta en otro gimnasio | Se admite: son cuentas distintas (RN-02, DD-24). El ingreso resuelve a qué cuenta corresponde |

---

#### FL-01 · Puesta en contexto del alumno

|                     |                                                                  |
| ------------------- | ---------------------------------------------------------------- |
| **Actor**           | Alumno · Sistema · Administrador (asignación)                    |
| **Precondiciones**  | Usuario creado por FL-19 con rol ALUMNO                          |
| **Postcondiciones** | Contexto suficiente y una rutina en estado PROPUESTA o BLOQUEADA |
| **Reglas**          | RN-09, RN-97b, RN-21, RF-111                                     |

**Curso normal**

1. El alumno declara su **contexto**: nivel de experiencia, objetivo y días semanales disponibles.
2. Declara sus condiciones físicas, cada una con su **zona corporal** y su **severidad**, o declara expresamente no tener ninguna.
3. Opcionalmente registra su peso actual y su aptitud.
4. El sistema comprueba contexto suficiente y genera una rutina completa sobre el **catálogo prescribible del gimnasio** (FL-04).
5. La rutina queda PROPUESTA y se avisa a su entrenador. La generación del alta **no produce candidato ajustable**: el alumno todavía no solicitó nada que moldear (RN-124). Si quiere intervenir sobre su rutina, la solicita por FL-03.

**El alumno no declara equipamiento:** el disponible es el inventario de su gimnasio (D4/PD-07).

**Cursos alternativos**

|                                                |                                                                                                                                                             |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1 · Declara no tener ninguna condición física | Es una declaración positiva, distinta de no haber contestado. Cuenta para el contexto suficiente                                                            |
| A2 · No tiene entrenador asignado              | La rutina se genera igual y queda BLOQUEADA. El sistema lo señala al administrador (RN-21) y al alumno le informa que espera la asignación de un entrenador |
| A3 · Fue invitado por un entrenador            | Ya tiene asignación desde FL-19/paso 4; la rutina queda PROPUESTA directamente                                                                              |

**Cursos de excepción**

|                                                                      |                                                                                                                                                                         |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E1 · Contexto insuficiente                                           | No se genera rutina. Se declara exactamente qué falta (RN-97b). Ver CB-10                                                                                               |
| E2 · La generación no produce salida válida                          | Ver CB-20: la tarea pasa al entrenador; nunca se presenta una rutina inválida                                                                                           |
| E3 · El catálogo prescribible no permite cubrir los patrones mínimos | Ver CB-22 y RN-118: se genera la rutina posible y se declara qué patrones quedaron sin cubrir, señalándolo también al administrador porque es un problema de inventario |

---

#### FL-02 · Revisión de una rutina y puesta en vigencia ⭐

Es la puerta del sistema. Todo lo que llega al alumno pasa por acá.

|                     |                                                                                                |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Actor**           | Entrenador                                                                                     |
| **Precondiciones**  | Rutina PROPUESTA de un alumno con asignación vigente                                           |
| **Postcondiciones** | Rutina VIGENTE o RECHAZADA; en el primer caso la anterior queda ARCHIVADA y se avisa al alumno |
| **Reglas**          | RN-35, RN-36, RN-40, D5/§6, RN-108                                                             |

**Curso normal**

1. El entrenador abre la rutina propuesta desde su cartera y ve, junto a la estructura: el origen de la rutina, el contexto del alumno con el que se construyó, el estado de compatibilidad de cada ejercicio, y **qué difiere de la salida original del componente o de la plantilla de origen** (RN-129, RF-120).
2. Revisa día por día. Puede modificar cualquier ejercicio, serie, repetición, carga o descanso antes de aprobar.
3. Aprueba. El sistema revalida compatibilidad y rangos de RN-39a sobre la versión final.
4. La rutina pasa a VIGENTE con su versión 1, la anterior queda ARCHIVADA, se registra la revisión en auditoría y se avisa al alumno.

**Cursos alternativos**

|                                                   |                                                                                                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| A1 · Aprueba con cambios                          | Idéntico. La revisión registra que hubo modificación y cuál                                                                                |
| A2 · Rechaza                                      | La rutina pasa a RECHAZADA con motivo. Se avisa al alumno, que puede solicitar otra. Su rutina vigente anterior, si existía, sigue vigente |
| A3 · El tipo de rutina no corresponde al objetivo | Advertencia y confirmación obligatoria (RN-40). No se impide                                                                               |
| A4 · Falta la aptitud o está vencida              | Advertencia destacada. No impide aprobar (RN-13)                                                                                           |
| A5 · Hay ejercicios ADVERTIDOS por condición leve | Se señalan. No impiden                                                                                                                     |

**Cursos de excepción**

|                                                                    |                                                                                                                                        |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| E1 · Hay un ejercicio INCOMPATIBLE                                 | La aprobación se impide. El sistema ofrece las alternativas admisibles de RN-49a. El entrenador sustituye o retira, y vuelve al paso 3 |
| E2 · No hay alternativa admisible                                  | Ver CB-21 y RN-49: se declara explícitamente; el entrenador retira el ejercicio o deja la rutina propuesta                             |
| E3 · La asignación termina mientras revisa                         | Ver CB-31: la confirmación se rechaza; la rutina queda BLOQUEADA                                                                       |
| E4 · Un ejercicio fue desactivado entre la propuesta y la revisión | Ver CB-13: se marca y se propone sustituto                                                                                             |
| E5 · El inventario cambió entre la propuesta y la revisión         | Los ejercicios afectados pasan a INCOMPATIBLE y se aplica E1                                                                           |

---

#### ~~FL-03 · Solicitud de rutina por el alumno~~ — ⏸ **diferido en la Etapa 1** (RF-025, 3/8)

|                     |                                                       |
| ------------------- | ----------------------------------------------------- |
| **Actor**           | Alumno                                                |
| **Precondiciones**  | Contexto suficiente                                   |
| **Postcondiciones** | Una rutina en estado PROPUESTA                        |
| **Reglas**          | RN-35, RN-36, RN-36a, RN-124 a RN-129, D5/§5.2, D5/§6 |

**Curso normal.** El alumno solicita una rutina generada. El sistema genera la estructura sobre el catálogo prescribible, verifica compatibilidad y la presenta como **candidato** (RN-124). El alumno lo ajusta si quiere, dentro de D5/§5.2, y confirma: recién entonces la rutina queda PROPUESTA y se avisa a su entrenador. Si se implementa RF-021, elegir un preset inicia el mismo flujo desde una copia.

**Alternativos.** A1: ya tiene una rutina propuesta → se le informa **al confirmar** y, si continúa, la anterior pasa a DESCARTADA (RN-36a). A2: no tiene entrenador vigente → queda BLOQUEADA (RN-23). A3: abandona el candidato sin confirmar → no queda rutina ni aviso, y su propuesta anterior sigue intacta (RN-124, CB-73).

**Excepción opcional.** E1: si se implementa RF-021 y el preset elegido contiene ejercicios incompatibles, se informa cuáles y por qué. No se propone algo que se sabe que será rechazado.

---

#### FL-04 · Generación asistida de rutina

|                     |                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **Actor**           | Entrenador · Alumno · Sistema                                                               |
| **Precondiciones**  | Contexto suficiente                                                                         |
| **Postcondiciones** | Rutina PROPUESTA con justificación asociada, o ningún efecto si el candidato no se confirma |
| **Reglas**          | RN-39a, RN-95, RN-95b, RN-96, RN-97, RN-97b, RN-98, RN-99, RN-124 a RN-129, D5/§5.2         |

**Curso normal**

1. El solicitante describe la necesidad en lenguaje natural, o completa el formulario estructurado equivalente.
2. Si la entrada fue en lenguaje natural, el sistema la traduce a parámetros estructurados —objetivo, frecuencia semanal, restricciones y duración de sesión— y **los presenta para confirmación antes de usarlos**. El equipamiento no es un parámetro: sale del inventario.
3. El componente de decisión construye la rutina a partir de esos parámetros y del contexto completo, usando exclusivamente el catálogo prescribible.
4. El sistema valida la salida contra RN-39a (estructura de días, series, repeticiones, descansos, cobertura mínima de patrones) y contra D5/§6.
5. Se produce la justificación en lenguaje natural de los criterios aplicados.
6. La rutina se presenta como **candidato**: la estructura completa, día por día, con el estado de compatibilidad de cada ejercicio y la justificación al lado. Todavía no existe como rutina y nadie fue avisado (RN-124).
7. El solicitante ajusta el candidato si quiere, por cualquiera de las tres vías de A3, A4 y A5. Cada ajuste revalida en el acto contra RN-39a y D5/§6 (RN-126).
8. Confirma. La rutina queda PROPUESTA, se registra qué difiere de la salida original del componente y se avisa a su entrenador (RN-129).

**Por qué existe el paso 7.** Si el alumno no puede moldear lo que pidió, que la solicite él o que se la genere el sistema por su cuenta son la misma funcionalidad. El paso 7 es lo que hace que la solicitud sea suya — y está acotado por D5/§5.2 para que moldear no se convierta en prescribir. Ver D11/DD-33.

**Cursos alternativos**

|                                                           |                                                                                                                                                                                                                         |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1 · Generación no disponible ✎                           | Se deshabilita temporalmente la generación y se informa sin detalles técnicos. **La vía que queda es que un entrenador cree y asigne una plantilla propia** (RF-019, RN-99, [DD-35](#d11)); el preset sólo existe si se implementa RF-021                                                       |
| A2 · La interpretación del lenguaje natural es incorrecta | El solicitante corrige los parámetros en el paso 2. Por eso el paso 2 existe                                                                                                                                            |
| ~~A3 · Ajusta el candidato **a mano**~~ ⏸ diferido        | Sustituye, agrega, quita o reordena ejercicios dentro de lo que admite D5/§5.2, sin volver a llamar al componente. No consume el tope de RN-127 ni cambia el origen de la rutina                                        |
| A4 · Pide **alternativas** para un ejercicio puntual      | El sistema ofrece las admisibles del mismo patrón dominante, del catálogo prescribible y compatibles con el alumno (RN-49a), ordenadas por la capa generativa sobre ese subconjunto ya prefiltrado (RF-059) y revalidadas por RN-44a-d (RF-113). Si el LLM no responde, se usa el orden determinista de RN-49a. El solicitante elige de esa lista; no escribe valores |
| A5 · Vuelve a **describirla en lenguaje natural**         | Regenera desde el paso 2, con los parámetros corregidos y las preferencias ya declaradas como entrada (RN-128). Consume el tope de RN-127                                                                               |
| A6 · Abandona el candidato sin confirmar                  | No queda rutina, no se avisa a nadie y la propuesta anterior, si existía, sigue intacta: RN-36a se aplica al confirmar, no al generar. Ver CB-73                                                                        |
| A7 · El solicitante es el entrenador                      | El ajuste del paso 7 no tiene las restricciones de D5/§5.2, porque ya tiene escritura sobre la rutina. Al confirmar, la rutina entra en FL-02 con él mismo como revisor                                                 |

**Cursos de excepción**

|                                                                                |                                                                                                                                                                       |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E1 · La salida no supera la validación o vence el límite                       | Un reintento; si vuelve a fallar o supera 120 segundos, la solicitud queda no disponible y se aplica A1. Nunca se presenta una propuesta inválida (RN-95b)             |
| E2 · Contexto insuficiente                                                     | No se genera. Se declara qué falta (RN-97b)                                                                                                                           |
| E3 · El catálogo prescribible no cubre los patrones mínimos de RN-39a          | Se genera la rutina posible, se declara qué patrones faltan y se avisa al administrador (RN-118)                                                                      |
| E4 · Un ajuste del paso 7 deja el candidato inválido                           | Se rechaza ese ajuste enunciando el rango o el mínimo incumplido, y el candidato queda como estaba. Un candidato inválido no se confirma nunca (RN-126)               |
| E5 · Agota el tope de regeneraciones sin quedar conforme                       | Ver CB-72: confirma el último candidato, o deriva la construcción a su entrenador adjuntando como comentario lo que no lo convence. No se le muestra un error (RN-99) |
| E6 · El inventario o una condición del alumno cambian con el candidato abierto | Los ejercicios afectados se remarcan en la revalidación del paso 7. Un candidato con un ejercicio INCOMPATIBLE no se confirma hasta sustituirlo o quitarlo            |

---

#### FL-05 · Ejecución de una sesión ⭐

|                      |                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------- |
| **Actor**            | Alumno                                                                                 |
| **Precondiciones**   | Rutina VIGENTE; ninguna sesión EN_CURSO                                                |
| **Datos de entrada** | Día elegido; por serie: carga, repeticiones, esfuerzo percibido (opcional), completada |
| **Postcondiciones**  | Sesión COMPLETADA con sus registros; récords detectados; indicadores recalculables     |
| **Reglas**           | RN-50 a RN-61, RN-70, RN-13, RN-93                                                     |

**Curso normal**

1. El sistema propone el siguiente día del ciclo según el historial. El alumno confirma o elige otro.
2. Si la aptitud está ausente o vencida, se advierte de forma destacada. La sesión se inicia igual.
3. Si algún ejercicio del día está marcado INCOMPATIBLE, ADVERTIDO o EJERCICIO_DESACTIVADO, se advierte (RN-93).
4. La sesión pasa a EN_CURSO y **congela la prescripción del día**.
5. Cada serie se presenta precargada con los valores óptimos predichos para ese ejercicio en esa sesión.
6. El alumno confirma o corrige carga y repeticiones, y opcionalmente el esfuerzo percibido.
7. Finaliza. La sesión pasa a COMPLETADA, se sella la duración, se detectan récords y se avisan.

**Cursos alternativos**

|                                           |                                                                                                                                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1 · Agrega series adicionales            | Se registran marcadas como adicionales. Cuentan para volumen, no para cumplimiento                                                                                              |
| A2 · Omite una serie prescripta           | Se marca no completada, con motivo opcional. No cuenta para volumen ni como cumplida                                                                                            |
| A3 · Sustituye un ejercicio               | FL-06                                                                                                                                                                           |
| A4 · Primera vez que ejecuta un ejercicio | Se precarga la carga sugerida de la prescripción, o el campo queda vacío o predice en base a un peso lógico para un principiante en ese ejercicio en particular. **Nunca cero** |
| A5 · Carga un valor atípico               | RN-55a: se marca y se pide confirmación. Confirmado, se registra con normalidad                                                                                                 |

**Cursos de excepción**

|                                                   |                                                                              |
| ------------------------------------------------- | ---------------------------------------------------------------------------- |
| E1 · Pérdida de conexión                          | El estado parcial se conserva localmente y se reintenta. Ver CB-24           |
| E2 · Cierra la aplicación                         | La sesión sigue EN_CURSO y se retoma (FL-07)                                 |
| E3 · Envía dos veces la misma serie               | Un único registro (RN-60)                                                    |
| E4 · Valor fuera de rango                         | Rechazo del lado del sistema con el rango en el mensaje (RN-55)              |
| E5 · Pasan 8 horas sin actividad                  | Se cierra como ABANDONADA conservando lo registrado (RN-53)                  |
| E6 · Su rutina cambia de versión mientras entrena | La sesión continúa contra la versión con la que se inició (RN-52). Ver CB-14 |

---

#### FL-06 · Sustitución de un ejercicio durante la sesión

|           |                                                                                |
| --------- | ------------------------------------------------------------------------------ |
| **Actor** | Alumno · **Precondiciones** Sesión EN_CURSO · **Reglas** RN-56, RN-102, RN-49a, RN-99 |

**Curso normal.** El alumno indica que no puede hacer un ejercicio. El sistema arma el subconjunto de alternativas admisibles (RN-49a: mismo patrón dominante, compatibles, con equipamiento presente en el inventario) y pide su orden a la capa generativa (RF-059), que devuelve hasta cinco, revalidadas por RN-44a-d antes de mostrarse (RF-113). Si el LLM no responde, se usa el orden determinista de RN-49a sobre el mismo subconjunto, sin interrumpir la sesión (RN-99). Elige una; las series restantes se registran contra el ejercicio ejecutado, marcadas como sustituidas, y cuentan como cumplidas.

**Alternativos.** A1: elige un ejercicio del catálogo prescribible por su cuenta → se admite y se registra igual. A2: declara el motivo → se conserva y alimenta el diagnóstico.

**Excepción.** E1: no hay alternativa admisible → CB-21; se ofrece omitir el ejercicio con motivo y se señala al entrenador. E2: el motivo declarado es una molestia física → el sistema **sugiere** al alumno declararla como condición física con su zona y severidad, y no la registra por su cuenta. Ver CB-23.

---

#### FL-07 · Reanudación de una sesión interrumpida

**Curso normal.** Al volver, si existe una sesión EN_CURSO, el sistema la ofrece en el punto exacto en que quedó, con las series ya registradas conservadas.

**Alternativos.** A1: el alumno prefiere descartarla → se cierra como ABANDONADA, conservando lo registrado; no se borra. A2: intenta iniciar una sesión nueva → se le presenta primero la pendiente (RN-50).

**Excepción.** E1: pasaron más de 8 horas → ya está ABANDONADA; se le ofrece registrar una sesión diferida (FL-08).

---

#### ~~FL-08 · Registro diferido, corrección y desbloqueo~~ — ⏸ **diferido en la Etapa 1** (RF-034, 2/8). *Consecuencia: una sesión no cargada el mismo día se pierde y la adherencia queda sesgada a la baja — D12/R-19*

|           |                                                                           |
| --------- | ------------------------------------------------------------------------- |
| **Actor** | Alumno · Entrenador (desbloqueo) · **Reglas** RN-58, RN-58a, RN-59, RN-71 |

**Curso normal.** El alumno registra una sesión indicando la fecha en que ocurrió y completando sus series. La sesión nace COMPLETADA, marcada como diferida, **imputada a la rutina y a la versión que estaban vigentes en esa fecha** — que pueden estar archivadas hoy. La restricción de RN-51 rige sólo para las sesiones iniciadas en tiempo real.

**Alternativos.** A1: corrige una sesión COMPLETADA dentro de las 48 h → se admite, se audita, y los récords afectados se recalculan sobre el histórico completo (RN-71). A2: pide corregir una sesión BLOQUEADA → su entrenador la desbloquea por 24 h, una sola vez, dejando el motivo en auditoría (RN-58a).

**Excepción.** E1: fecha futura, o anterior a 90 días → rechazo indicando el rango (RN-59). E2: en esa fecha el alumno no tenía ninguna rutina vigente → se rechaza y se explica; el sistema no inventa una rutina de referencia. E3: la sesión ya fue desbloqueada una vez → rechazo; el plazo de corrección dejaría de existir si el desbloqueo fuera repetible. E4: el alumno no tiene entrenador vigente que pueda desbloquear → la solicitud queda pendiente y se señala al administrador.

---

#### FL-09 · Diagnóstico periódico de evolución

|                     |                                                                     |
| ------------------- | ------------------------------------------------------------------- |
| **Actor**           | Sistema · Entrenador (a demanda)                                    |
| **Precondiciones**  | Alumno con rutina VIGENTE                                           |
| **Postcondiciones** | Diagnóstico registrado; propuesta generada si corresponde           |
| **Reglas**          | **D5/§9.1** (criterios) y **§9.2** (ajustes) · RN-78 a RN-85, RN-98 |

**Curso normal.** Cada dos semanas el sistema evalúa cada ejercicio de la rutina vigente y le asigna una situación según la tabla de precedencia de RN-79a, y determina la situación global. Si corresponde, produce una propuesta aplicando las reglas de ajuste de RN-89a, con un ajuste fundamentado por cada problema detectado. La propuesta se valida contra D5/§6 y se avisa al entrenador.

**Alternativos.** A1: situación global `PROGRESION_ADECUADA` y ningún ejercicio con ajuste → se registra el diagnóstico y no se genera propuesta. Un diagnóstico sin propuesta es un resultado, no un fallo (RN-89a/restricción 4). A2: el entrenador lo solicita antes de tiempo → se ejecuta sobre los datos disponibles.

**Excepción.** E1: `DATOS_INSUFICIENTES` → diagnóstico registrado sin propuesta (RN-82), declarando qué faltó. E2: el esfuerzo percibido no fue registrado → se diagnostica sin ese criterio y se declara (RN-81). E3: el proceso nunca se ejecutó → CB-35: no hay diagnósticos y la información se presenta como no disponible. E4: un ajuste de sustitución no encuentra alternativa admisible → ese ajuste no se propone y el hecho se declara en la propuesta (RN-49).

---

#### FL-10 · Resolución de una propuesta de adaptación ⭐

|                     |                                                                             |
| ------------------- | --------------------------------------------------------------------------- |
| **Actor**           | Entrenador                                                                  |
| **Precondiciones**  | Propuesta PENDIENTE de un alumno con asignación vigente                     |
| **Postcondiciones** | Propuesta resuelta; si fue aceptada, nueva versión vigente y alumno avisado |
| **Reglas**          | RN-35a, RN-86 a RN-92, RN-108                                               |

**Curso normal.** El entrenador ve cada ajuste con su criterio y los datos que lo sustentan, junto a la evolución del alumno en el período. Acepta la propuesta. El sistema genera una versión nueva, conserva la anterior, no altera ninguna sesión ejecutada, y avisa al alumno. **No se pide una segunda revisión: la resolución es la revisión** (RN-35a).

**Alternativos.** A1: acepta algunos ajustes y rechaza otros → se genera la versión con los aceptados. A2: rechaza todo → no se genera versión; se registra el motivo, que es información valiosa sobre la calidad del diagnóstico. A3: prefiere modificar la rutina por su cuenta → FL-11.

**Excepción.** E1: el contexto del alumno cambió y la propuesta dejó de ser compatible → pasa a INVALIDADA y se genera una nueva (CB-16). E2: caduca a los 30 días → CADUCADA registrada (RN-87). E3: la asignación termina mientras la evalúa → CB-31.

---

#### FL-11 · Intervención directa del entrenador sobre la rutina

**Curso normal.** El entrenador modifica ejercicios, series, repeticiones, cargas o descansos de la rutina vigente de un alumno asignado. El sistema verifica compatibilidad y rangos de RN-39a, genera una versión nueva, registra autor e instante, y avisa al alumno.

**Reglas.** RN-45, RN-46, RN-88, RN-89, RN-108. Las sesiones ya ejecutadas no cambian.

**Excepción.** E1: la modificación introduce una incompatibilidad → se impide y se ofrecen alternativas (RN-46). E2: la modificación deja la rutina fuera de los rangos de su tipo → se advierte y se exige confirmación; el entrenador puede apartarse de la referencia, el componente automático no. E3: hay una sesión EN_CURSO → la versión se crea igual; la sesión conserva su prescripción congelada (CB-14).

---

#### FL-12 · Reevaluación por cambio de contexto

|                |                                                                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Disparador** | Cambio de objetivo, alta o cierre de una condición física, cambio de estado de la aptitud, **o cambio del inventario del gimnasio** |
| **Reglas**     | RN-91, RN-92, RN-93, RN-11, RN-117                                                                                                  |

**Curso normal.** El sistema reevalúa la compatibilidad de la rutina vigente. Si aparece una incompatibilidad, marca los ejercicios afectados **sin retirarlos**, avisa al entrenador y al alumno, y genera la propuesta correspondiente.

**Alternativos.** A1: no aparece incompatibilidad → se registra la reevaluación y no ocurre nada más. A2: la condición se cierra → los ejercicios dejan de estar marcados desde esa fecha, sin efecto retroactivo (RN-11). A3: cambia el objetivo → se propone el cambio de tipo de rutina con el reajuste de esquemas de RN-89a. A4: el administrador retira equipamiento del inventario → todos los alumnos del gimnasio con ese ejercicio en su rutina reciben la marca y la propuesta (RN-117).

**Excepción.** E1: la condición nueva invalida la mayor parte de la rutina → la propuesta puede implicar una rutina sustancialmente nueva. E2: no hay entrenador vigente → la propuesta queda BLOQUEADA y el alumno sigue recibiendo la advertencia en cada sesión (CB-32).

---

#### FL-13 · Consulta de la cartera priorizada

**Curso normal.** El entrenador ve sus alumnos con asignación vigente, ordenados según el criterio único de urgencia (RF-107): primero los que tienen una rutina propuesta o una propuesta de adaptación pendientes de su revisión; luego incompatibilidad sobrevenida sin resolver; luego estancamiento; luego caída de adherencia; luego sin señal. Cada fila muestra fecha de la última sesión, adherencia de cuatro semanas y señales detectadas. *(El "riesgo de abandono alto" se retiró de este orden al pasar RF-061 a RF-063 a WON'T — replanteo de IA, [D11/DD-34](#d11).)*

**Alternativos.** A1: filtra por señal. A2: un alumno sin datos suficientes → aparece con "sin datos suficientes", nunca con cero.

**Excepción.** E1: cartera vacía → estado explicativo, no una tabla vacía.

---

#### FL-14 · Registro de mediciones corporales

**Curso normal.** El alumno registra un valor fechado de peso o de un perímetro. El sistema lo suma a su serie temporal y presenta la evolución con media móvil de 7 días.

**Reglas.** RN-15, RN-16, RN-17.

**Alternativos.** A1: corrige o elimina un registro → admitido, auditado. A2: carga un segundo valor del mismo tipo y fecha → sustituye al anterior.

**Excepción.** E1: menos de dos registros → no se dibuja tendencia; se declara que hacen falta más datos. E2: valor fuera de rango → rechazo con el rango admitido.

---

#### FL-15 · Gestión de asignaciones

|           |                                                                 |
| --------- | --------------------------------------------------------------- |
| **Actor** | Administrador · **Reglas** RN-18 a RN-23, RA-04, RN-108, RN-114 |

**Curso normal.** El administrador asigna un entrenador a un alumno. Si había otro, se finaliza en el mismo instante. Todo lo pendiente pasa al entrante y los avisos del saliente sobre ese alumno se cierran. El acceso del saliente cesa en ese instante.

**Alternativos.** A1: finaliza una asignación sin reemplazo → el alumno queda señalado como sin entrenador; su rutina vigente permanece; sus pendientes quedan BLOQUEADOS.

**Excepción.** E1: el destino no tiene rol de entrenador → rechazo. E2: el destino es el mismo alumno → rechazo (RN-22). E3: operaciones del saliente en curso → se rechazan al confirmarse (CB-31).

---

#### ~~FL-16 · Estimación de riesgo de abandono~~ — Derogado (replanteo de IA, 2026-08-28)

**Derogado.** RF-061 a RF-063 pasaron a WON'T en el replanteo de IA ([D11/DD-34](#d11)); RN-100 y RN-101 quedan derogadas. No hay proceso de estimación de riesgo. El texto original se conserva tachado para trazabilidad.

> ~~**Actor:** Sistema (proceso diferido semanal) · Administrador (a demanda) · **Reglas** RN-100, RN-101, RN-98, RN-103, RN-107.~~
> ~~**Curso normal.** El proceso calcula, para cada alumno con datos suficientes, una estimación con sus factores principales, y la registra con la versión del componente, el contexto y el instante. Entrenadores y administradores la ven; el alumno evaluado nunca.~~
> ~~**Excepción.** E1: nunca se ejecutó → toda la información de riesgo se presenta como no disponible y nada más se degrada. E2: historial insuficiente → no se calcula; se distingue de riesgo bajo. E3: los datos son simulados → la estimación se marca como tal y se excluye de toda presentación como real (RN-107).~~

---

#### FL-17 · Carga y curación del catálogo

**Carga inicial (sistema).** Un proceso repetible incorpora el catálogo base desde la fuente externa con su clasificación muscular, sus articulaciones exigidas, su equipamiento requerido y sus recursos visuales, y **declara qué ejercicios quedaron sin clasificación muscular**. Ejecutarlo dos veces no duplica registros.

**Curación (administrador).** Revisa los ejercicios propuestos por entrenadores, los aprueba o rechaza, y desactiva ejercicios del catálogo del gimnasio. Completa a mano la clasificación de los ejercicios no clasificados de mayor uso (RF-099).

**Excepción.** E1: la fuente cambió de estructura o no responde → la carga falla de forma completa y verificable, sin dejar un catálogo a medias. E2: un ejercicio llega sin clasificación muscular → se incorpora marcado como no clasificado, no aporta volumen y no se presenta como cero (RN-30). E3: se desactiva un ejercicio presente en rutinas vigentes → RN-29 y CB-13.

---

#### FL-18 · Baja de cuenta y exportación

**Curso normal.** El usuario solicita una copia estructurada de sus datos y de su historial, o la baja de su cuenta. La baja anonimiza sus datos personales dentro de 7 días, conservando sesiones y series desvinculadas.

**Reglas.** RN-08, RN-106, RN-03a.

**Excepción.** E1: tiene una sesión EN_CURSO → se cierra como ABANDONADA antes de procesar la baja. E2: es el único administrador activo → rechazo hasta que exista otro (RI-23, CB-39). E3: es entrenador con asignaciones vigentes → todas se finalizan y sus alumnos quedan señalados al administrador.

---

#### FL-20 · Mantenimiento del inventario del gimnasio

|                     |                                                                  |
| ------------------- | ---------------------------------------------------------------- |
| **Actor**           | Administrador                                                    |
| **Postcondiciones** | Catálogo prescribible actualizado; rutinas afectadas reevaluadas |
| **Reglas**          | RN-115 a RN-118, RN-45, RN-117, RN-108                           |

**Curso normal.** El administrador marca qué equipamiento de la enumeración cerrada posee el gimnasio. El sistema recalcula el catálogo prescribible.

**Alternativos.** A1: **incorpora** equipamiento → el catálogo prescribible crece; los ejercicios antes marcados por equipamiento vuelven a COMPATIBLE y las propuestas abiertas por ese motivo se invalidan. A2: **retira** equipamiento → todo ejercicio de rutina vigente que lo requiera pasa a INCOMPATIBLE y se genera propuesta de sustitución (RN-117), sin interrumpir ninguna sesión ni rutina.

**Excepción.** E1: tras el cambio, el catálogo prescribible no cubre los patrones mínimos de RN-39a → se declara al administrador qué patrones quedan sin cubrir y qué equipamiento los resolvería (RN-118). Es la advertencia que evita descubrirlo alumno por alumno. E2: el inventario queda vacío → sólo quedan prescribibles los ejercicios de `PESO_CORPORAL`; se advierte explícitamente.

---

#### FL-21 · Paneles agregados — ⏸ **el panel del gimnasio queda diferido** (RF-068, 2/8); el de cartera (RF-052) es banda N3

|             |                                                                                         |
| ----------- | --------------------------------------------------------------------------------------- |
| **Actores** | Entrenador (su cartera) · Administrador (el gimnasio) · **Reglas** RN-73, RN-107, RA-06 |

**Curso normal.** El entrenador consulta la adherencia media de su cartera, la distribución de señales y la evolución de su actividad. El administrador consulta la retención por cohorte de incorporación, la distribución de actividad por día y franja horaria, la adherencia media, la carga de alumnos por entrenador y la cantidad de alumnos sin entrenador vigente.

**Alternativos.** A1: se filtra por período.

**Excepción.** E1: no hay actividad suficiente para una cohorte → se declara, no se dibuja vacía (RN-73). E2: hay datos simulados en la base → se excluyen de la analítica presentada como real, y se indica que se excluyeron (RN-107). E3: el administrador intenta descender al detalle individual → no se ofrece esa navegación (RA-06).


---

<a id="parte-v"></a>

## Parte V — Requerimientos

<a id="d8"></a>

### D8 — Especificación de requerimientos funcionales

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/requirements/functional-requirements.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D8`

|                |            |
| -------------- | ---------- |
| **Versión**    | 4.0        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo en cuanto al enunciado de cada requisito. **La clasificación de alcance de la Etapa 1 es propuesta**: depende de PD-01 y PD-00 del [baseline de alcance](#baseline) |
| **Depende de** | D1 a D7    |

**Identificadores estables.** Ningún identificador se reutiliza, se renumera ni se borra. RF-001 a RF-122 conservan su numeración aunque su enunciado, tipo, prioridad o alcance hayan cambiado. Renumerarlos rompería veinte documentos del corpus y los `AGENTS.md` de los tres repositorios de código, a cambio de nada.

##### Cambios de la v3.3 → v4.0

La v4.0 incorpora tres fuentes que la v3.3 no tenía: la **votación del equipo** sobre RF-001 a RF-081 (8 de 9 integrantes), las **respuestas registradas del equipo** a las decisiones del Acta de Redefinición, y la **verificación del estado real de los tres repositorios de código**. El análisis completo está en el [baseline de alcance](#baseline); aquí se registran sus efectos sobre los requisitos.

**1 · Aparece la dimensión de alcance, separada de la prioridad.** Un requisito puede ser MUST y estar fuera de esta etapa: la prioridad dice cuánto importa al producto, el alcance dice si se construye ahora. Estaban confundidos en una sola columna.

| Marca          | Significado                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **N1**         | Núcleo de la Etapa 1. No se recorta                                                                                  |
| N2             | Comprometido en la Etapa 1                                                                                           |
| N3             | Condicionado al hito del Sprint 3                                                                                    |
| **⏸ DIFERIDO** | Fuera de la Etapa 1, **no del producto**. Conserva su enunciado y su prioridad. Distinto de WON'T, que significa nunca |
| ⊂ RF-xxx       | Absorbido por fusión en otro requisito, que conserva su contenido íntegro                                            |
| → regla        | Degradado: no era un requisito funcional sino una regla, una restricción o un criterio de aceptación                  |
| `n/8`          | Votos obtenidos. Sin marca: no fue votado (RF-082 en adelante son posteriores a la votación)                          |

**2 · Cinco fusiones**, con el contenido de los absorbidos conservado íntegro en el resultante: RF-032 ⊕ RF-033 → **RF-027** (ciclo de vida de la sesión; fusión sugerida por el equipo y ampliada) · RF-023 → **RF-038** · RF-060 → **RF-059** · RF-107 → **RF-036** · RF-004 → **RF-065**.

**3 · Cuatro fusiones sugeridas se rechazan, con fundamento**: RF-054 ⊕ RF-055 borraría la frontera entre componente de decisión y componente narrativo, y dejaría sin sujeto a RNF-24 · RF-005 dentro de RF-065 haría desaparecer la verificación por recurso, que es RA-01, R-11 y RNF-14 · RF-088 ⊕ RF-089 obligaría a inventar una «propuesta vacía», cuando un diagnóstico sin propuesta es un resultado válido.

**4 · Cuatro degradaciones**: RF-098, RF-102, RF-103 y RF-104 no eran requisitos funcionales. Su contenido se conserva como restricción de integridad, convención transversal o criterio de aceptación.

**5 · Enunciados que cambian**, todos por consecuencia del alcance y no por revisión del diseño:

- **RF-058** ya no puede apoyar la continuidad en «presets publicados del gimnasio»: RF-021 quedó diferido. La vía manual pasa a ser la plantilla del entrenador (RF-019). Ver [D11/DD-35](#d11).
- **RF-059** absorbe la exclusión dura de RF-060, que era una restricción sobre su salida, no un requisito aparte.
- **RF-036** absorbe el criterio de urgencia de RF-107, que existía sólo porque RF-036 no era verificable sin él.
- **RF-027** absorbe la reanudación y la finalización: son tres transiciones del mismo autómata de D6/§4.

**6 · Lo que la votación confirmó.** RF-061 a RF-063 obtuvieron 1, 0 y 0 votos: la votación respalda el WON'T de la v3.3. El ciclo central —contexto, catálogo, prescripción, ejecución, indicadores y adaptación— obtuvo mayorías amplias sin excepción.

**7 · RF-053 se conserva pese a no alcanzar el corte.** Obtuvo 3 votos de 8, pero está comprometido por escrito ante el Product Owner en `deliverable PO/alcance-ia-generativa.md` v2.1. Una votación interna no revoca un compromiso ya asumido: queda en alcance, en banda N2, hasta que el Product Owner lo libere (PD-07).

**8 · El estado real del código.** Al 2026-09-01 los tres repositorios contienen andamiaje y **ninguna funcionalidad de dominio**: Express con `/health` y `/ready`, `schema.prisma` sin modelos, una SPA con una pantalla de bienvenida y un paquete Python vacío. Ningún requisito de este documento está implementado ni parcialmente implementado. No hay funcionalidad implementada sin documentar.

##### Cambios anteriores, conservados

**v2.0:** alta por invitación (RF-116) y aprovisionamiento (RF-115) · inventario del gimnasio (RF-114) y catálogo prescribible (RF-118) · desbloqueo de sesión (RF-117) · tres ciclos de dependencias eliminados · nutrición cerrada como pauta orientativa.
**v3.0:** el candidato de rutina ajustable (RF-119) y la diferencia visible para el revisor (RF-120).
**v3.1 → v3.2:** sugerencia de carga de sesión (RF-121) y proyección de trayectoria (RF-122), **no provenientes de un pedido del cliente** y pendientes de confirmación.
**v3.3 (replanteo de IA, [D11/DD-34](#d11), ya redactada):** RF-059, RF-060 y RF-064 pasan de `ML` a `AI` · RF-061 a RF-063 pasan a WON'T · RF-122 sube a SHOULD.

**Cambios de la v3.3 → v3.4:** los presets pasan de requisito obligatorio a alcance opcional. La primera entrega conserva plantillas privadas de entrenadores y generación; si no se implementan presets, la indisponibilidad generativa deshabilita esa capacidad sin afectar el diseño manual.

**Tipos:** WEB · AI · ML · DATA · HYBRID **Prioridad:** MUST · SHOULD · COULD · WON'T
**Marcas de historial:** 🆕 nuevo · ✎ enunciado modificado · ⬆⬇ cambio de prioridad · ⛔ derogado
**Marcas de alcance (v4.0):** **N1** · N2 · N3 · ⏸ DIFERIDO · ⊂ absorbido · → degradado a regla · `n/8` votos

---

#### Módulo 0 · Afiliación y alta

| ID     | Requerimiento                                                                                                                                                                                                                                                                      | Tipo | Prior.  | Depende        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | -------------- |
| RF-115 | Disponer de una operación de aprovisionamiento, **externa a la aplicación**, que cree un gimnasio afiliado con su zona horaria y su primer usuario con rol administrador, de forma atómica                                                                                         | WEB  | MUST 🆕 **N1** | —              |
| RF-116 | Permitir el alta de usuarios **exclusivamente mediante invitación** nominal emitida por un administrador —para cualquier rol— o por un entrenador —sólo con rol alumno—, de un solo uso, con vencimiento y revocable, que determina el gimnasio y los roles del usuario resultante | WEB  | MUST 🆕 **N1** | RF-115         |
| RF-098 | Vincular todo usuario a exactamente un gimnasio en el momento de su alta, sin posibilidad de cambio posterior                                                                                                                                                                      | WEB  | MUST → regla | RF-116         |
| RF-114 | Permitir al administrador declarar y mantener el inventario de equipamiento del gimnasio sobre la enumeración cerrada del glosario, y advertirle cuando el inventario resultante no permita cubrir los patrones de movimiento que exige algún tipo de rutina                       | WEB  | MUST 🆕 **N1** | RF-115         |
| RF-118 | Determinar el catálogo prescribible de cada gimnasio como el subconjunto del catálogo accesible cuyo equipamiento requerido está presente en su inventario, y utilizarlo como único conjunto sobre el que se construyen y validan rutinas y recomendaciones                        | DATA | MUST 🆕 **N1** | RF-114, RF-013 |

#### Módulo 1 · Cuentas y acceso

| ID     | Requerimiento                                                                                                                                                                                                                             | Tipo | Prior. | Depende             |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ------------------- |
| RF-001 | Permitir a una persona invitada completar su cuenta con nombre y contraseña                                                                                                                                                               | WEB  | MUST ✎ **N1** · 8/8 | RF-116              |
| RF-002 | Autenticar, mantener la sesión, cerrarla explícitamente y expirarla por inactividad                                                                                                                                                       | WEB  | MUST **N1** · 8/8 | RF-001              |
| RF-003 | Recuperar el acceso mediante verificación por correo con validez limitada, y cambiar la contraseña estando autenticado                                                                                                                    | WEB  | MUST N2 · 8/8 | RF-001              |
| RF-004 | ~~Registro abierto con rol alumno predeterminado~~                                                                                                                                                                                        | —    | **⛔** | Derogado por RF-116 |
| RF-005 | Autorizar cada operación verificando el rol **y** la relación del actor con el recurso concreto                                                                                                                                           | WEB  | MUST **N1** · 2/8 | RF-116, RF-066      |
| RF-006 | Permitir solicitar la baja de la cuenta y obtener una copia estructurada de los datos propios                                                                                                                                             | WEB  | MUST ⏸ DIFERIDO · 0/8 | RF-001              |
| RF-096 | Requerir consentimiento explícito y separado para el tratamiento de condiciones físicas, aptitud y mediciones corporales, y conservar el texto aceptado                                                                                   | WEB  | MUST N2 | RF-001              |
| RF-097 | Registrar en auditoría toda operación sensible: invitaciones, cambios de rol, asignaciones, cambios de inventario, puesta en vigencia y modificación de rutinas, resolución de propuestas, desbloqueo de sesiones y curación del catálogo | WEB  | SHOULD ⏸ DIFERIDO | RF-005              |

#### Módulo 2 · Perfil, objetivos y condiciones

| ID     | Requerimiento                                                                                                                                                                                                                                                                            | Tipo | Prior.  | Depende                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | ---------------------- |
| RF-007 | Registrar y mantener el perfil del alumno: edad, sexo, altura, nivel de experiencia y días semanales disponibles                                                                                                                                                                         | WEB  | MUST **N1** · 8/8 | RF-001                 |
| RF-008 | Declarar un objetivo vigente de la enumeración cerrada y modificarlo, conservando el historial y sus períodos de vigencia                                                                                                                                                                | WEB  | MUST **N1** · 8/8 | RF-007                 |
| RF-009 | Declarar las condiciones físicas que limitan la ejecución de ejercicios, **cada una con su zona corporal y su severidad tipadas**, y utilizarlas para condicionar prescripciones y recomendaciones. El alumno **no** declara equipamiento: el disponible es el inventario de su gimnasio | WEB  | MUST ✎ **N1** · 8/8 | RF-007, RF-114         |
| RF-010 | Registrar mediciones corporales fechadas, un máximo de un registro por tipo y fecha, corregibles y eliminables                                                                                                                                                                           | WEB  | MUST **N1** · 8/8 | RF-007                 |
| RF-011 | Mantener el perfil profesional del entrenador, visible para sus alumnos asignados                                                                                                                                                                                                        | WEB  | SHOULD ⏸ DIFERIDO · 4/8 | RF-116                 |
| RF-012 | Presentar una estimación orientativa del gasto energético diario y del rango de ingesta proteica de referencia, con su fórmula declarada, indicando explícitamente que no es una indicación nutricional profesional                                                                      | WEB  | COULD ✎ ⏸ DIFERIDO · 2/8 | RF-007, RF-010         |
| RF-084 | Registrar la aptitud con fecha de emisión y de vencimiento, cargada por el alumno o por un administrador, y **advertir de forma destacada** su ausencia o vencimiento al poner una rutina en vigencia y al iniciar una sesión, sin impedir ninguna operación                             | WEB  | MUST ✎ N2 | RF-007                 |
| RF-085 | Conservar el historial de condiciones físicas con sus fechas de inicio y fin, de modo que sea determinable qué condiciones estaban vigentes en una fecha dada                                                                                                                            | WEB  | MUST **N1** | RF-009                 |
| RF-111 | Determinar y exponer si un alumno tiene contexto suficiente para que se produzcan decisiones automáticas sobre él, e indicar qué falta cuando no lo tiene                                                                                                                                | DATA | MUST N2 | RF-007, RF-008, RF-009 |

#### Módulo 3 · Catálogo de ejercicios

| ID     | Requerimiento                                                                                                                                                                                                  | Tipo | Prior. | Depende        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | -------------- |
| RF-099 | Definir la taxonomía muscular canónica cerrada y la enumeración cerrada de articulaciones, y exigir la curación manual de la clasificación de los ejercicios de mayor uso incorporados desde la fuente externa | DATA | MUST ✎ **N1** | —              |
| RF-013 | Mantener un catálogo de ejercicios accesible en consulta a todos los usuarios autenticados                                                                                                                     | WEB  | MUST **N1** · 8/8 | —              |
| RF-014 | Localizar ejercicios por nombre, grupo muscular, equipamiento requerido, patrón de movimiento y nivel de dificultad                                                                                            | WEB  | MUST N2 · 8/8 | RF-013         |
| RF-015 | Presentar por ejercicio sus instrucciones, equipamiento, patrón de movimiento, nivel, articulaciones exigidas y al menos un recurso visual                                                                     | WEB  | MUST ✎ N2 · 8/8 | RF-013         |
| RF-016 | Asociar a cada ejercicio los grupos musculares que involucra, diferenciando participación primaria de secundaria, y las articulaciones que exige                                                               | WEB  | MUST ✎ **N1** · 8/8 | RF-013, RF-099 |
| RF-017 | Permitir a los entrenadores incorporar ejercicios propios con la misma información descriptiva y de clasificación exigida al resto                                                                             | WEB  | SHOULD N3 · 5/8 | RF-013, RF-016 |
| RF-018 | Permitir a un administrador revisar, aprobar y desactivar ejercicios, garantizando que un ejercicio desactivado deje de estar disponible para nuevas prescripciones sin afectar los registros históricos       | WEB  | SHOULD ⏸ DIFERIDO · 0/8 | RF-017         |
| RF-100 | Distinguir el catálogo base, común a todos los gimnasios y no editable, del catálogo propio de cada gimnasio, visible sólo dentro de él                                                                        | WEB  | MUST N2 | RF-013, RF-069 |
| RF-101 | Señalar en toda rutina vigente los ejercicios desactivados, permitir su ejecución y generar una propuesta de sustitución                                                                                       | WEB  | SHOULD ⏸ DIFERIDO | RF-018, RF-089 |

#### Módulo 4 · Diseño y solicitud de rutinas

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                                                                       | Tipo | Prior.  | Depende                |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------- | ---------------------- |
| RF-019 | Crear plantillas estructuradas en días ordenados, cada uno con una secuencia ordenada de ejercicios del catálogo                                                                                                                                                                                                                                                                                    | WEB  | MUST **N1** · 8/8 | RF-013                 |
| RF-020 | Definir para cada ejercicio la cantidad de series y, por serie, el rango de repeticiones objetivo, la carga sugerida, el descanso y su carácter de calentamiento o de trabajo                                                                                                                                                                                                                       | WEB  | MUST **N1** · 6/8 | RF-019                 |
| RF-021 | Publicar **opcionalmente** una plantilla como preset dentro del gimnasio y utilizar cualquier preset como punto de partida                                                                                                                                                                                                                                                                                            | WEB  | COULD ⬇ ⏸ DIFERIDO · 1/8 | RF-019                 |
| RF-022 | Generar, al solicitarse una rutina a partir de una plantilla, una copia completa e independiente de su estructura, conservando la referencia al origen                                                                                                                                                                                                                                              | WEB  | MUST ✎ **N1** · 0/8 | RF-019                 |
| RF-023 | Modificar ejercicios, series, repeticiones, cargas y descansos de la rutina de un alumno concreto sin afectar la plantilla ni las rutinas de otros                                                                                                                                                                                                                                                  | WEB  | MUST ⊂ RF-038 · 1/8 | RF-022                 |
| RF-024 | Requerir que toda rutina declare las sesiones esperadas por semana, dentro del rango que admite su tipo                                                                                                                                                                                                                                                                                             | WEB  | MUST ✎ **N1** · 2/8 | RF-022, RF-082         |
| RF-025 | Permitir a un alumno **seleccionar** un preset o solicitar una rutina generada, lo que crea una rutina propuesta que no rige hasta ser revisada por un entrenador                                                                                                                                                                                                                                   | WEB  | MUST ✎ ⏸ DIFERIDO · 3/8 | RF-021, RF-110         |
| RF-026 | Mantener como máximo una rutina vigente y una propuesta por alumno, archivando la vigente anterior al entrar otra en vigencia y descartando la propuesta anterior al solicitarse otra, preservando la consulta de lo archivado                                                                                                                                                                      | WEB  | MUST ✎ **N1** · 6/8 | RF-022                 |
| RF-082 | Clasificar cada plantilla y cada rutina según un tipo de la enumeración cerrada, y **derivar de él, mediante una tabla explícita, la frecuencia semanal admisible, la estructura de días, los esquemas de series y repeticiones, los rangos de descanso y la cobertura mínima de patrones de movimiento**                                                                                           | WEB  | MUST ✎ **N1** | RF-019                 |
| RF-083 | Verificar la correspondencia entre el tipo de rutina y el objetivo del alumno, advertir explícitamente si no coinciden y requerir confirmación para continuar                                                                                                                                                                                                                                       | WEB  | MUST **N1** | RF-008, RF-082         |
| RF-110 | Exigir la revisión y la aprobación explícita de un entrenador con asignación vigente antes de que **cualquier** rutina entre en vigencia, cualquiera sea su origen                                                                                                                                                                                                                                  | WEB  | MUST **N1** | RF-022, RF-066         |
| RF-109 | Transferir al entrenador entrante todas las rutinas propuestas y propuestas de adaptación pendientes del alumno al establecerse una asignación                                                                                                                                                                                                                                                      | WEB  | MUST N2 | RF-066                 |
| RF-112 | Señalar al administrador los alumnos sin entrenador vigente y mantener bloqueadas sus rutinas propuestas y sus propuestas de adaptación hasta su reasignación                                                                                                                                                                                                                                       | WEB  | MUST N2 | RF-066, RF-110         |
| RF-119 | Presentar toda rutina generada o copiada de un preset como **candidato ajustable por el solicitante** antes de enviarla a revisión, admitiendo sustituir, agregar, quitar y reordenar ejercicios, pedir alternativas admisibles para uno puntual y regenerar desde parámetros corregidos, revalidando cada ajuste y **sin crear la rutina propuesta ni avisar al entrenador hasta la confirmación** | WEB  | MUST 🆕 ⏸ DIFERIDO | RF-025, RF-054, RF-086 |
| RF-120 | Registrar y presentar al entrenador revisor la diferencia entre la rutina propuesta y la salida original del componente, o la plantilla de origen                                                                                                                                                                                                                                                   | WEB  | MUST 🆕 ⏸ DIFERIDO | RF-119, RF-110         |

#### Módulo 5 · Ejecución y registro

| ID     | Requerimiento                                                                                                                                                                                                                                                                | Tipo | Prior.    | Depende        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | --------- | -------------- |
| RF-027 | **Ciclo de vida completo de la sesión** ✎ v4.0 (absorbe RF-032 y RF-033): iniciarla seleccionando un día de la rutina vigente, proponiendo por defecto el siguiente del ciclo e impidiendo más de una en curso por alumno; conservar su estado y permitir la reanudación; cerrarla automáticamente tras el período de inactividad definido; y finalizarla registrando su duración, incorporándola al historial y habilitándola para el cálculo de indicadores. Las cuatro transiciones son criterios de aceptación separados de D6/§4                                                                                                             | WEB  | MUST **N1** · 8/8 | RF-022         |
| RF-028 | Copiar, al iniciarse la sesión, la prescripción vigente del día dentro de la propia sesión, de modo que las modificaciones posteriores no la alteren                                                                                                                         | WEB  | MUST **N1** · 5/8 | RF-027, RF-020 |
| RF-029 | Registrar por serie la carga, las repeticiones realizadas, opcionalmente el esfuerzo percibido y si fue completada, conservando de forma conjunta lo prescripto y lo ejecutado, y requiriendo confirmación explícita ante un valor atípico respecto del histórico del alumno | WEB  | MUST ✎ **N1** · 8/8 | RF-028         |
| RF-030 | Presentar cada serie precargada con los valores de la última ejecución del alumno en ese ejercicio                                                                                                                                                                           | WEB  | MUST **N1** · 1/8 | RF-029, RF-035 |
| RF-031 | Permitir durante la sesión agregar series, omitir series prescriptas y sustituir un ejercicio, imputando el trabajo al ejercicio ejecutado                                                                                                                                   | WEB  | MUST N2 · 6/8 | RF-029, RF-059 |
| RF-032 | Conservar el estado de una sesión en curso, permitir su reanudación y cerrarla automáticamente tras el período de inactividad definido                                                                                                                                       | WEB  | MUST ⊂ RF-027 · 3/8 | RF-027         |
| RF-033 | Finalizar una sesión registrando su duración, incorporándola al historial y habilitándola para el cálculo de indicadores                                                                                                                                                     | WEB  | MUST ⊂ RF-027 · 7/8 | RF-029         |
| RF-034 | Registrar una sesión de fecha anterior, **imputándola a la rutina y a la versión vigentes en esa fecha aunque hoy estén archivadas**, y corregir una sesión finalizada dentro del plazo                                                                                      | WEB  | SHOULD ✎ ⏸ DIFERIDO · 2/8 | RF-033         |
| RF-117 | Permitir a un entrenador con asignación vigente reabrir por tiempo acotado y una sola vez una sesión bloqueada, a pedido del alumno y con registro del motivo                                                                                                                | WEB  | SHOULD 🆕 ⏸ DIFERIDO | RF-034         |
| RF-035 | Consultar el historial de sesiones ordenado cronológicamente y el detalle de cualquiera, incluida la comparación entre lo prescripto y lo ejecutado                                                                                                                          | WEB  | MUST **N1** · 8/8 | RF-033         |
| RF-104 | Garantizar que el envío repetido de una misma serie produzca un único registro                                                                                                                                                                                               | WEB  | MUST → regla | RF-029         |
| RF-102 | Aplicar unidades y precisión únicas en todo el sistema, y rechazar del lado del servidor los valores fuera de los rangos admitidos                                                                                                                                           | WEB  | MUST → regla | RF-029, RF-010 |
| RF-103 | Almacenar todo instante en tiempo universal coordinado, presentarlo en la zona horaria del gimnasio, y usar una definición única de semana para toda agregación                                                                                                              | WEB  | MUST → regla | RF-033         |

#### Módulo 6 · Seguimiento entrenador–alumno

| ID     | Requerimiento                                                                                                                                                                          | Tipo   | Prior. | Depende                |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | ---------------------- |
| RF-107 | Definir un criterio único y ordenado de urgencia para la cartera: pendientes de revisión, incompatibilidad sobrevenida, estancamiento, caída de adherencia, sin señal ✎ (v3.3: se retira "riesgo alto" al pasar RF-061 a WON'T)  | DATA   | MUST ✎ ⊂ RF-036 | RF-042, RF-046 |
| RF-036 | Presentar la cartera del entrenador ordenada según un **criterio único y ordenado de urgencia** ✎ v4.0 (absorbe RF-107) —pendientes de revisión, incompatibilidad sobrevenida, estancamiento, caída de adherencia, sin señal—, con fecha de última sesión, adherencia reciente y señales detectadas                                                  | DATA   | MUST **N1** · 5/8 | RF-107, RF-066         |
| RF-037 | Acceder a una vista consolidada del alumno: perfil, objetivos, condiciones, rutina vigente, historial, indicadores y mediciones                                                        | HYBRID | MUST **N1** · 8/8 | RF-035, RF-040, RF-005 |
| RF-038 | Modificar ejercicios, series, repeticiones, cargas y descansos de la rutina de un alumno asignado ✎ v4.0 (absorbe RF-023), **sin afectar la plantilla de origen ni las rutinas de otros alumnos**, registrando autor e instante, avisando al alumno y sin alterar las sesiones ejecutadas                                                       | WEB    | MUST **N1** · 7/8 | RF-023, RF-028         |
| RF-039 | Intercambiar comentarios asincrónicos entre entrenador y alumno asociados a una sesión o a una rutina                                                                                  | WEB    | SHOULD ⏸ DIFERIDO · 1/8 | RF-066                 |
| RF-095 | Entregar al usuario, dentro de la aplicación, los avisos de la enumeración cerrada de tipos, con reglas explícitas de no repetición, caducidad y reasignación al cambiar de entrenador | WEB    | MUST ✎ N2 | RF-038, RF-044, RF-046 |

#### Módulo 7 · Indicadores

| ID     | Requerimiento                                                                                                                                                                                                                   | Tipo | Prior. | Depende                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ---------------------- |
| RF-040 | Calcular el volumen y la frecuencia por grupo muscular para un alumno y período, considerando sólo series de trabajo completadas y ponderando participación primaria y secundaria                                               | DATA | MUST **N1** · 8/8 | RF-016, RF-029         |
| RF-041 | Estimar la capacidad máxima por ejercicio a partir de carga y repeticiones registradas, dentro del rango de repeticiones en que la estimación es válida, y mantener su evolución                                                | DATA | MUST ✎ **N1** · 8/8 | RF-029                 |
| RF-042 | Calcular la adherencia sobre una ventana móvil de cuatro semanas, ponderando la frecuencia objetivo vigente en cada semana, **sin reiniciarse al cambiar de rutina**                                                            | DATA | MUST ✎ **N1** · 5/8 | RF-024, RF-033         |
| RF-043 | Calcular el cumplimiento de series y el cumplimiento de repeticiones, por sesión y por períodos agregados                                                                                                                       | DATA | MUST ✎ **N1** · 0/8 | RF-028, RF-029         |
| RF-044 | Identificar y registrar los récords personales por ejercicio en cada uno de los tres tipos definidos, notificarlos al producirse, y recalcularlos sobre el histórico completo si se corrige o elimina la sesión que los produjo | DATA | MUST ✎ N2 · 6/8 | RF-041                 |
| RF-045 | Presentar la evolución temporal de las mediciones corporales con media móvil de siete días                                                                                                                                      | DATA | MUST ✎ N2 · 8/8 | RF-010                 |
| RF-046 | Detectar y señalar estancamiento en un ejercicio, caída significativa de la adherencia y desbalance de volumen, con umbrales explícitos                                                                                         | DATA | MUST **N1** · 7/8 | RF-040, RF-041, RF-042 |
| RF-047 | Permitir configurar las ponderaciones, rangos de referencia y ventanas temporales sin modificar los datos históricos                                                                                                            | WEB  | COULD ⏸ DIFERIDO · 3/8 | RF-040                 |

#### Módulo 8 · Visualización

| ID     | Requerimiento                                                                                                                                                                                                                                                                             | Tipo | Prior. | Depende                                        |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------ | ---------------------------------------------- |
| RF-048 | Presentar al alumno un panel con su actividad reciente, adherencia, récords, evolución de sus indicadores de fuerza y evolución de sus mediciones                                                                                                                                         | DATA | MUST N2 · 8/8 | RF-040, RF-041, RF-042, RF-043, RF-044, RF-045 |
| RF-049 | Representar sobre un esquema bidimensional del cuerpo la intensidad del trabajo por grupo muscular en un período seleccionable, con detalle numérico y ejercicios que aportaron, distinguiendo los grupos sin información de los de volumen nulo, y sin depender exclusivamente del color | DATA | MUST ✎ ⏸ DIFERIDO · 4/8 | RF-040, RF-099                                 |
| RF-050 | Consultar por ejercicio la evolución temporal de la carga, el volumen y la capacidad máxima estimada, con los récords identificados                                                                                                                                                       | DATA | MUST N2 · 8/8 | RF-041                                         |
| RF-051 | Informar explícitamente cuando no haya información suficiente para calcular o representar un indicador, en lugar de presentar valores nulos, vacíos o engañosos                                                                                                                           | WEB  | MUST **N1** · 7/8 | RF-048                                         |
| RF-052 | Presentar al entrenador indicadores agregados de su cartera: adherencia media, distribución de señales y evolución de la actividad                                                                                                                                                        | DATA | SHOULD N3 · 8/8 | RF-036                                         |

#### Módulo 9 · Inteligencia artificial generativa

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                      | Tipo   | Prior. | Depende                                |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | -------------------------------------- |
| RF-053 | Interpretar una descripción en lenguaje natural y traducirla a parámetros estructurados, sometidos a validación y a confirmación del usuario antes de utilizarse                                                                                                                                                                                   | AI     | MUST N2 · 3/8 | RF-009                                 |
| RF-054 | Generar de forma asíncrona un candidato de rutina a partir de parámetros estructurados y del contexto mínimo del alumno, usando exclusivamente el catálogo prescribible de su gimnasio y respetando condiciones y nivel; sólo al confirmarse se convierte en propuesta que requiere revisión de un entrenador                                              | HYBRID | MUST ✎ **N1** · 8/8 | RF-053, RF-082, RF-086, RF-118         |
| RF-055 | Acompañar toda rutina generada con una explicación en lenguaje natural de los criterios aplicados                                                                                                                                                                                                                                                  | AI     | MUST **N1** · 8/8 | RF-054                                 |
| RF-056 | Generar un resumen redactado de la evolución de un alumno en un período, elaborado exclusivamente a partir de indicadores previamente calculados                                                                                                                                                                                                   | HYBRID | SHOULD ⏸ DIFERIDO · 4/8 | RF-040, RF-041, RF-042, RF-043, RF-044 |
| RF-057 | Impedir que los componentes narrativos introduzcan valores numéricos ausentes de sus datos de entrada, y que cualquier componente emita indicaciones de carácter médico. Los componentes de decisión sí determinan valores de prescripción, siempre validados contra las reglas de compatibilidad y de tipo de rutina, y sujetos a revisión humana | AI     | MUST **N1** · 0/8 | RF-054, RF-056                         |
| RF-058 | Mantener el resto del sistema operativo ante la indisponibilidad de la generación, informar esa condición sin detalles técnicos y conservar operativas **las plantillas privadas del entrenador y su creación manual** (RF-019) como vía disponible, siempre sujeta a revisión. ✎ v4.0: sustituye a los presets publicados, que pasan a alcance opcional (RF-021, COULD) — ver [D11/DD-35](#d11). **Deja de existir una vía automática de prescripción cuando la generación no responde**                                                                                              | HYBRID | MUST ✎ **N1** · 1/8 | RF-021, RF-022, RF-054                 |
| RF-113 | Descartar toda salida generativa que no supere la validación, reintentar una sola vez y, tras el segundo fallo o 120 segundos por intento, declarar la generación no disponible sin presentar una propuesta inválida; no se construye una rutina determinística alternativa                                                                          | HYBRID | MUST ✎ **N1** | RF-054, RF-058                         |

#### Módulo 10 · Aprendizaje automático

Tras el replanteo de IA de la v3.3 ([D11/DD-34](#d11)), sólo RF-121 y RF-122 son componentes aprendidos. RF-059/RF-060 (alternativas de sustitución) y RF-064 (descripción de perfil) pasaron a la capa generativa — ver [generative-ai.md](#arch-generative). RF-061 a RF-063 pasan a WON'T.

| ID     | Requerimiento                                                                                                                                                                        | Tipo   | Prior. | Depende        |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ------ | -------------- |
| RF-059 | Proponer para un ejercicio un conjunto ordenado de alternativas del catálogo prescribible con el mismo patrón de movimiento y efecto de entrenamiento equivalente, mediante la capa generativa sobre el subconjunto ya prefiltrado por patrón y compatibilidad, con revalidación determinista posterior (RF-113), **excluyendo de forma dura y en código los ejercicios contraindicados por las condiciones vigentes del alumno o de nivel superior al suyo (RN-44a-d)** ✎ v4.0 (absorbe RF-060) | AI     | MUST ✎ **N1** · 8/8 | RF-016, RF-118 |
| RF-060 | Excluir de las recomendaciones los ejercicios contraindicados por las condiciones vigentes del alumno o de nivel superior al suyo (exclusión dura en código, RN-44a-d)               | AI     | MUST ✎ ⊂ RF-059 · 2/8 | RF-059, RF-009 |
| RF-061 | **WON'T (v3.3)** ⬇. Estimar para cada alumno el nivel de riesgo de que interrumpa su actividad — retirado del alcance en el replanteo de IA por costo/esfuerzo frente al valor esperado con los datos disponibles (S-03) | ML     | WON'T ⬇ | —              |
| RF-062 | **WON'T (v3.3)** ⬇. Presentar la estimación de riesgo con sus factores y su fecha, restringida a entrenadores y administradores — sin efecto al retirarse RF-061                     | HYBRID | WON'T ⬇ | —              |
| RF-063 | **WON'T (v3.3)** ⬇. Actualizar las estimaciones de riesgo con periodicidad definida y a demanda — sin efecto al retirarse RF-061                                                     | ML     | WON'T ⬇ | —              |
| RF-064 | Presentar a entrenadores y administradores una descripción del perfil de comportamiento del alumno (frecuencia, volumen e intensidad relativos), redactada por la capa generativa a partir de los indicadores ya calculados y el objetivo vigente, **sin clustering y sin persistirse** | AI     | SHOULD ✎ N3 · 6/8 | RF-040, RF-042 |
| RF-121 | Sugerir la carga y las repeticiones de la próxima serie de un ejercicio a partir de la tendencia reciente del alumno en ese ejercicio (carga máxima estimada, cumplimiento, esfuerzo percibido), presentada como valor precargado adicional a —nunca en reemplazo de— el mínimo de RF-030; sin tendencia suficiente, se conserva exclusivamente RF-030                                                          | ML     | SHOULD 🆕 ⏸ DIFERIDO | RF-030, RF-071 |
| RF-122 | Proyectar, a partir de la tendencia de las últimas semanas, la carga máxima estimada por ejercicio y las mediciones corporales del alumno bajo el supuesto de que continúa con un patrón de entrenamiento similar, presentando la proyección junto con su incertidumbre y **sin emplear términos de composición corporal (masa muscular, grasa corporal) que el sistema no mide**                              | ML     | SHOULD 🆕⬆ ⏸ DIFERIDO | RF-010, RF-071 |

**Por qué RF-121 y RF-122 no reemplazan nada existente.** RF-030 sigue siendo el mínimo garantizado (última ejecución, MUST); RF-121 es una sugerencia adicional que se descarta ante indisponibilidad o tendencia insuficiente, igual que cualquier otra capacidad inteligente (RNF-11, RNF-12). RN-89a sigue siendo la única vía que modifica la prescripción vigente; RF-121 no prescribe, sólo precarga un valor que el alumno confirma o corrige (FL-05, paso 6). RF-122 no estima composición corporal: proyecta exclusivamente indicadores que el sistema ya deriva o registra (carga máxima estimada, perímetros), y su presentación debe declarar que es una proyección bajo continuidad de patrón, no una promesa de resultado — mismo principio que ya rige RF-012 y RF-108.

#### Módulo 11 · Administración y analítica

| ID     | Requerimiento                                                                                                                                                                                                  | Tipo | Prior.   | Depende        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | -------- | -------------- |
| RF-065 | Emitir y revocar invitaciones, asignar y revocar roles, y suspender o reactivar cuentas dentro del gimnasio, sin poder dejarlo sin ningún administrador activo                                                 | WEB  | MUST ✎ **N1** · 6/8 | RF-116         |
| RF-066 | Establecer, finalizar y reasignar la relación entrenador–alumno conservando el historial completo y revocando de forma inmediata el acceso del entrenador saliente                                             | WEB  | MUST **N1** · 2/8 | RF-065         |
| RF-067 | Registrar y actualizar el estado de membresía con carácter exclusivamente informativo, sin condicionar el acceso a ninguna funcionalidad                                                                       | WEB  | COULD N3 · 8/8 | RF-065         |
| RF-068 | Presentar indicadores agregados del gimnasio: retención por cohorte, distribución de la actividad por día y franja horaria, adherencia media, carga de alumnos por entrenador y alumnos sin entrenador vigente | DATA | SHOULD ✎ ⏸ DIFERIDO · 2/8 | RF-042, RF-033 |
| RF-069 | Circunscribir toda la información al gimnasio al que pertenece, impidiendo el acceso a datos de otro gimnasio                                                                                                  | WEB  | MUST **N1** · 4/8 | RF-005         |

#### Módulo 12 · Datos y evaluación de los componentes

| ID     | Requerimiento                                                                                                                                                                                                                                                                      | Tipo   | Prior. | Depende                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | ---------------------- |
| RF-070 | Disponer de un mecanismo repetible de carga inicial del catálogo desde una fuente externa, con clasificación muscular, articulaciones, equipamiento requerido y recursos visuales, que declare qué ejercicios quedaron sin clasificar y no deje el catálogo a medias ante un fallo | DATA   | MUST ✎ **N1** · 8/8 | RF-013, RF-016, RF-099 |
| RF-071 | Disponer de un mecanismo para generar información histórica simulada, e identificar de manera inequívoca los registros simulados frente a los reales                                                                                                                               | DATA   | MUST **N1** · 3/8 | RF-029, RF-033         |
| RF-072 | Registrar para cada resultado de un componente inteligente la versión que lo generó, el contexto de entrada considerado y el instante de cálculo, de modo que sea reproducible; para el orden generativo de RF-059 se conserva la salida producida, no se reejecuta ✎             | HYBRID | MUST ✎ N2 · 0/8 | RF-059, RF-121         |
| RF-073 | Disponer de un procedimiento reproducible de evaluación de los componentes de recomendación y estimación sobre un conjunto reservado de tamaño declarado, que incluya la comparación contra un criterio de referencia simple, y conservar ambas métricas                           | HYBRID | MUST ✎ N2 · 0/8 | RF-121, RF-122, RF-071 |
| RF-105 | Anonimizar los datos personales del usuario dado de baja dentro del plazo establecido, conservando las sesiones y series desvinculadas de la identidad                                                                                                                             | WEB    | MUST ⏸ DIFERIDO | RF-006                 |
| RF-106 | Excluir los registros simulados de toda analítica presentada como real, y señalar cuándo una presentación se basa en datos simulados                                                                                                                                               | DATA   | MUST **N1** | RF-071                 |

#### Módulo 13 · Pauta nutricional orientativa

| ID     | Requerimiento                                                                                                                                                                                                                                                                        | Tipo   | Prior.    | Depende |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | --------- | ------- |
| RF-075 | Producir una **pauta nutricional orientativa**: la distribución de la estimación energética y del rango proteico entre las comidas del día, en función del objetivo y las características del alumno. **No nombra alimentos, no compone comidas y no registra ingesta**              | HYBRID | COULD ✎ ⏸ DIFERIDO | RF-012  |
| RF-108 | Acompañar toda pauta nutricional de la declaración de que es orientativa y no profesional, exigir revisión humana antes de entregarla al alumno, e impedir su producción cuando falten los datos necesarios o el alumno haya declarado una condición que el sistema no puede evaluar | HYBRID | COULD ✎ ⏸ DIFERIDO | RF-075  |
| RF-074 | Registrar diariamente un indicador nutricional de referencia y visualizar su evolución junto al peso corporal y al volumen                                                                                                                                                           | WEB    | COULD ⏸ DIFERIDO · 1/8 | RF-010  |
| RF-076 | Base de alimentos y composición de comidas                                                                                                                                                                                                                                           | WEB    | **WON'T** | —       |

#### Módulo 14 · Excluidos

| ID     | Requerimiento                                  | Prior. | Motivo                                                                          |
| ------ | ---------------------------------------------- | ------ | ------------------------------------------------------------------------------- |
| RF-077 | Mensajería en tiempo real                      | WON'T  | Coste desproporcionado frente a RF-039; compite con herramientas ya usadas      |
| RF-078 | Pagos, cuotas y facturación                    | WON'T  | Sin relación con el ciclo de datos; sustituido por RF-067                       |
| RF-079 | Alojamiento de contenido audiovisual propio    | WON'T  | Resuelto por recursos referenciados en RF-015                                   |
| RF-080 | Representación tridimensional del cuerpo       | WON'T  | Coste y riesgo desproporcionados frente a RF-049                                |
| RF-081 | Integración con dispositivos de monitorización | WON'T  | Habilitación de terceros incompatible con el plazo; duplica la fuente de verdad |

#### Módulo 15 · Prescripción adaptativa

Núcleo del producto. Pedido directo del cliente.

| ID     | Requerimiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Tipo   | Prior. | Depende                                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ------ | -------------------------------------- |
| RF-086 | Verificar, antes de poner una rutina en vigencia y ante toda modificación posterior, que ningún ejercicio esté contraindicado por una condición vigente con severidad impeditiva, exceda el nivel del alumno o exija equipamiento ausente del inventario, **mediante una regla explícita de correspondencia entre zona corporal de la condición y participación muscular o articulación del ejercicio**, impidiendo la puesta en vigencia y ofreciendo alternativas admisibles | HYBRID | MUST ✎ **N1** | RF-009, RF-016, RF-085, RF-118         |
| RF-087 | Generar una rutina completa para un alumno sin historial a partir de su perfil, objetivo, tipo de rutina, condiciones y catálogo prescribible, garantizando que todo alumno finalice su incorporación con una rutina propuesta                                                                                                                                                                                                                                                 | HYBRID | MUST ✎ **N1** | RF-007, RF-008, RF-009, RF-082, RF-086 |
| RF-088 | Evaluar periódicamente la evolución de cada alumno sobre su rutina vigente y producir un diagnóstico que asigne, **por criterios explícitos y con un orden de precedencia definido**, una de cinco situaciones a cada ejercicio y al conjunto: datos insuficientes, sobreexigencia, progresión adecuada, estímulo insuficiente o estancamiento                                                                                                                                 | DATA   | MUST ✎ **N1** | RF-041, RF-042, RF-043, RF-046         |
| RF-089 | Elaborar, a partir del diagnóstico y **mediante una tabla explícita que asocia cada situación con un tipo de ajuste y su magnitud**, una propuesta de modificación de la rutina vigente que puede comprender ajuste de cargas y volumen, sustitución de ejercicios, modificación de esquemas y reestructuración de días o frecuencia, garantizando que la propuesta resultante cumpla las condiciones de compatibilidad y los rangos de su tipo                                | HYBRID | MUST ✎ **N1** | RF-088, RF-059, RF-086, RF-082         |
| RF-090 | Registrar y presentar, para cada ajuste propuesto, el criterio que lo motiva y los datos de evolución que lo sustentan                                                                                                                                                                                                                                                                                                                                                         | HYBRID | MUST **N1** | RF-089                                 |
| RF-091 | Requerir la aprobación explícita de la propuesta antes de aplicarla, correspondiendo **siempre** al entrenador con asignación vigente, y permitir aceptarla total o parcialmente o rechazarla                                                                                                                                                                                                                                                                                  | WEB    | MUST ✎ **N1** | RF-089, RF-066, RF-110                 |
| RF-092 | Generar, al aplicarse una adaptación, una nueva versión de la rutina, conservando las anteriores y manteniendo inalteradas las sesiones ejecutadas bajo cada una, sin requerir una segunda revisión                                                                                                                                                                                                                                                                            | WEB    | MUST ✎ **N1** | RF-091, RF-028                         |
| RF-093 | Consultar la secuencia completa de adaptaciones aplicadas sobre la rutina de un alumno, con sus fechas, criterios y relación con la evolución del período                                                                                                                                                                                                                                                                                                                      | DATA   | SHOULD N2 | RF-092, RF-090                         |
| RF-094 | Reevaluar la rutina vigente cuando cambie el objetivo, se registre o cierre una condición física, se modifique el estado de la aptitud **o cambie el inventario del gimnasio**, señalando las incompatibilidades sin retirar los ejercicios y elaborando la propuesta correspondiente                                                                                                                                                                                          | HYBRID | MUST ✎ **N1** | RF-084, RF-085, RF-086, RF-089, RF-114 |

---

#### Distribución

##### Por prioridad y tipo — el producto completo

| Prioridad      | Cantidad |     | Tipo                 | Cantidad |
| -------------- | -------- | --- | -------------------- | -------- |
| MUST           | 79       |     | WEB                  | 63       |
| SHOULD         | 13       |     | DATA                 | 24       |
| COULD          | 5        |     | HYBRID               | 16       |
| WON'T          | 9        |     | ML                   | 3        |
| Derogado       | 1        |     | AI                   | 7        |
| **En el producto** | **97** |   | **Total**            | **97**   |

La prioridad no cambió en la v4.0: sigue expresando cuánto importa cada requisito **al producto**. Lo que se agrega es la segunda dimensión.

##### Por alcance — la Etapa 1

| Alcance                                     | Cantidad | Qué significa                                                                    |
| ------------------------------------------- | -------- | ---------------------------------------------------------------------------------- |
| **N1** · núcleo, no se recorta              | **57**   | Sin esto el producto no cumple lo que el cliente declaró condición de aprobación |
| N2 · comprometido                           | 19       | Se construye en la Etapa 1                                                       |
| N3 · condicionado al hito del Sprint 3      | 4        | Se construye si el circuito de prescripción cerró a tiempo                        |
| **En alcance — Etapa 1**                    | **80**   |                                                                                    |
| ⏸ DIFERIDO                                  | 23       | Fuera de la Etapa 1, dentro del producto                                         |
| ⊂ absorbido por fusión                      | 6        | RF-004, RF-023, RF-032, RF-033, RF-060, RF-107                                    |
| → degradado a regla                         | 4        | RF-098, RF-102, RF-103, RF-104                                                   |
| WON'T                                       | 9        | Fuera del producto                                                                |

*Los 23 diferidos incluyen RF-075 y RF-108, que ya eran COULD y caen con la nutrición, y RF-105, que cae con RF-006.*

##### El alcance sigue por encima de la capacidad

| Conjunto     | Requisitos | Optimista (8 h) | Realista (10–12 h) | Frente a ~504 h |
| ------------ | ---------- | --------------- | ------------------ | --------------- |
| N1           | 57         | ~456 h          | 570 – 684 h        | 0,9 × a 1,4 ×   |
| N1 + N2      | 76         | ~608 h          | 760 – 912 h        | 1,2 × a 1,8 ×   |
| N1 + N2 + N3 | 80         | ~640 h          | 800 – 960 h        | 1,3 × a 1,9 ×   |

**El recorte redujo el alcance un 18 %, no lo que hacía falta.** Lo que la votación retiró —nutrición, comentarios, paneles agregados, parametrización, mapa muscular— es barato; lo que confirmó por mayoría amplia es el ciclo central, que es donde está el trabajo. **El núcleo solo cabe si todo sale bien y nada más se construye.**

Y el denominador de esa cuenta está en duda: las ~504 h de [D12/§3](#d12) suponen que tres de las nueve personas no construyen software, mientras que el Documento de Planificación afirma lo contrario de forma explícita. Ver la inconsistencia **I-09** del [baseline de alcance](#baseline). Conviene resolver el denominador antes de discutir el numerador.

##### Verificación de dependencias

Los tres ciclos de la versión anterior siguen eliminados. **Cinco fusiones de la v4.0 retiran además tres dependencias que existían sólo para unir un requisito con el que lo completaba**: RF-107 → RF-036 (que además era la dependencia invertida señalada en la v3.3), RF-060 → RF-059 y RF-023 → RF-038.

Ningún requisito de banda N1 depende de uno diferido. Dos comprobaciones que hubo que hacer y conviene dejar escritas:

- **RF-031** (sustituir un ejercicio durante la sesión, banda N2) depende de RF-059, que es N1. Correcto.
- **RF-089** (propuesta de adaptación, N1) depende de RF-059 para el ajuste de sustitución. RF-059 es N1. Correcto.
- **RF-101** dependía de RF-018, y ambos quedan diferidos juntos. **RF-117** dependía de RF-034, y ambos quedan diferidos juntos. **RF-119 y RF-120** dependían de RF-025, y los tres quedan diferidos juntos. No hay dependencias colgadas.

##### Qué está implementado

**Nada.** Verificado sobre los tres repositorios el 2026-09-01. `proyecto-gimnasio-back` tiene Express, CORS, `/health`, `/ready`, cliente Prisma y pipeline de migraciones, con `schema.prisma` **sin un solo modelo**. `proyecto-gimnasio` tiene el andamiaje de Vite y React con una pantalla de bienvenida. `proyecto-gimnasio-ia` tiene un paquete Python vacío con sus dependencias declaradas. Las ramas `develop` y `test` son idénticas a `main` en los tres.

Esto es una ventaja mientras dure: **todas las decisiones de esquema de este documento pueden tomarse sin coste de migración, pero sólo hasta la primera migración de Prisma.**


---

<a id="d9"></a>

### D9 — Requerimientos no funcionales

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/requirements/non-functional-requirements.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D9`

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.1        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | D1, D5, D8 |

Sólo se incluyen requerimientos con criterio de verificación concreto. Un requerimiento no funcional sin forma de comprobarlo es una aspiración.

**Cambios de la v1.0:** RNF-24 y RNF-25 llevan tamaño de muestra declarado, sin el cual no eran verificables · RNF-15 fija un criterio comprobable en lugar de un adjetivo · RNF-37 a RNF-40 cubren invitación, inventario, reevaluación masiva y desbloqueo.

**Cambios de la v2.1 ([baseline de alcance](#baseline)):** se corrigen cuatro requisitos que seguían nombrando la estimación de riesgo, retirada del alcance en el replanteo de IA · RNF-11 y RNF-18 dejan de apoyarse en los presets, diferidos con RF-021 · **RNF-35 queda diferido** con RF-049 · se incorporan **RNF-41** (dónde queda confinado el texto libre del usuario) y **RNF-42** (nadie se queda sin plan), este último porque el criterio de éxito E1 dejó de estar garantizado al retirarse los presets.

---

#### 1. Rendimiento

| ID     | Requerimiento                      | Criterio de verificación                                                                                              |
| ------ | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| RNF-01 | Lectura de las vistas principales  | Percentil 95 por debajo de 500 ms con 300 alumnos y 150.000 registros de serie cargados                               |
| RNF-02 | Panel de progreso del alumno       | Carga completa en menos de 1,5 s con seis meses de historial                                                          |
| RNF-03 | Cartera del entrenador             | Se ordena y presenta en menos de 1,5 s con 50 alumnos                                                                 |
| RNF-04 | Generación de una rutina           | La solicitud se acepta sin esperar al LLM; cada intento alcanza un estado terminal en un máximo inicial configurable de 120 s, con un solo reintento antes de declarar indisponibilidad |
| RNF-05 | Diagnóstico y procesos diferidos ✎ | Se ejecutan fuera del camino de la petición del usuario. Ninguna vista queda a la espera de su cálculo. *(v2.1: se retira «estimación de riesgo», sin sujeto desde [D11/DD-34](#d11))* |

#### 2. Usabilidad

| ID     | Requerimiento                                                                                               | Criterio de verificación                                                                                                            |
| ------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| RNF-06 | La sesión de entrenamiento es plenamente usable en pantalla de 360 px de ancho                              | Recorrido completo de registro de una sesión de 5 ejercicios ejecutado en un dispositivo de ese ancho sin desplazamiento horizontal |
| RNF-07 | Registrar una serie con los valores precargados correctos requiere como máximo dos interacciones            | Medido sobre el recorrido de RNF-06                                                                                                 |
| RNF-08 | El alumno completa su incorporación en tres pasos como máximo, de los cuales sólo el primero es obligatorio | Verificado sobre FL-01                                                                                                              |
| RNF-09 | Ninguna vista presenta cero, vacío ni un valor por defecto cuando la causa es falta de datos                | Revisión sistemática de todas las vistas con un alumno sin historial. Ver D10/§A                                                    |

#### 3. Robustez y continuidad

| ID     | Requerimiento                                                                             | Criterio de verificación                                                                                                     |
| ------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| RNF-10 | La sesión en curso conserva un estado local y reintenta el envío ante pérdida de conexión | Prueba con red interrumpida durante el registro: ningún dato ingresado se pierde                                             |
| RNF-11 | Ningún fallo generativo degrada el resto del sistema ni expone un error técnico ✎          | Prueba con API IA, ngrok o LLM inaccesible: la generación se declara no disponible y **las plantillas y operaciones manuales siguen funcionando** (RF-019). *(v2.1: los presets dejan de ser la contingencia — RF-021, alcance opcional.* **Esta prueba ya no demuestra que un alumno nuevo obtenga rutina**: eso es RNF-42*)* |
| RNF-12 | La no ejecución de los procesos diferidos no degrada ninguna otra funcionalidad           | Prueba con la base sin diagnósticos ni estimaciones: todas las vistas funcionan y declaran la información como no disponible |
| RNF-13 | El envío repetido de una misma operación de registro no produce duplicados                | Envío del mismo registro de serie tres veces: un único registro resultante                                                   |

#### 4. Seguridad

| ID     | Requerimiento                                                                                                                                                                                                  | Criterio de verificación                                                                                                                                  |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-14 | Toda operación sobre un recurso de un alumno concreto rechaza a un actor no autorizado                                                                                                                         | Una prueba automatizada por cada operación con identificador de alumno, que verifica el rechazo con un actor autenticado pero sin relación con el recurso |
| RNF-15 | Las contraseñas se almacenan mediante una función de derivación de clave con sal única por usuario y coste configurable, calibrada para que una verificación tarde al menos 200 ms en el entorno de producción | Medición del tiempo de verificación e inspección del almacenamiento: ninguna contraseña recuperable, ninguna sal compartida                               |
| RNF-16 | Las credenciales de sesión no son accesibles desde el código de la página                                                                                                                                      | Inspección                                                                                                                                                |
| RNF-17 | Los intentos de autenticación están limitados por origen y por período                                                                                                                                         | Prueba: el sexto intento en un minuto desde un mismo origen es rechazado                                                                                  |
| RNF-18 | Las invocaciones a servicios externos de generación están limitadas por usuario y por período                                                                                                                  | Prueba: superado el límite, no se envía otra invocación, se informa indisponibilidad temporal y permanece disponible la creación manual de plantillas por el entrenador ✎ |
| RNF-19 | Ningún registro de diagnóstico contiene credenciales, contraseñas ni datos de salud                                                                                                                            | Inspección de los registros producidos durante el recorrido completo                                                                                      |
| RNF-20 | El acceso del entrenador cesa en el instante en que finaliza la asignación                                                                                                                                     | Prueba: operación iniciada antes y confirmada después del fin de la asignación, rechazada                                                                 |

#### 5. Privacidad

| ID     | Requerimiento                                                                                                 | Criterio de verificación                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| RNF-21 | Los datos de condiciones físicas, aptitud y mediciones sólo se tratan con consentimiento explícito registrado | Prueba: sin consentimiento registrado, las operaciones correspondientes son rechazadas                                           |
| RNF-22 | La baja de cuenta produce anonimización efectiva en 7 días o menos                                            | Prueba: tras el proceso, ningún dato identificatorio del usuario es recuperable, y sus sesiones siguen contando en los agregados |
| RNF-23 | El sistema no solicita ni almacena documento de identidad ni domicilio                                        | Inspección del modelo de datos                                                                                                   |

#### 6. Calidad de los componentes inteligentes

| ID     | Requerimiento                                                                                         | Criterio de verificación                                                                                                                                                                                                                                                                                                                                              |
| ------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-24 | Ningún texto generado contiene un valor numérico ausente de sus datos de entrada                      | Verificación automática sobre **50 textos generados** de cada tipo narrativo: tasa de valores no presentes igual a cero                                                                                                                                                                                                                                               |
| RNF-25 | Toda rutina generada es válida por construcción                                                       | Sobre **200 rutinas generadas** cubriendo los cuatro tipos y al menos tres inventarios distintos: 100% con ejercicios existentes en el catálogo prescribible, 100% sin ejercicios incompatibles, 100% dentro de los rangos de la tabla de derivación del tipo, 100% con la cobertura mínima de patrones o con la declaración explícita de qué patrón no pudo cubrirse |
| RNF-26 | La rutina generada se evalúa contra un criterio de referencia explícito ✎ | Tras [DD-34](#d11) no queda un modelo clásico contra el que comparar en la Etapa 1. El criterio de referencia pasa a ser **la rutina que un entrenador construye a mano sobre el mismo caso**, sobre un conjunto fijo de casos. Que la construida a mano resulte mejor es un resultado admisible y debe informarse |
| RNF-27 | Toda salida de un componente inteligente es reproducible a partir de lo registrado                    | Dado un resultado almacenado, su versión de componente y su contexto de entrada permiten reejecutar y obtener el mismo resultado                                                                                                                                                                                                                                      |
| RNF-28 | Todo resultado producido sobre datos simulados está identificado como tal en toda presentación ✎ | Inspección de las vistas de indicadores, diagnóstico y propuestas de adaptación. *(v2.1: se retira «vistas de riesgo», sin sujeto desde DD-34)* |

#### 7. Mantenibilidad y entrega

| ID     | Requerimiento                                                                                                              | Criterio de verificación                            |
| ------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| RNF-29 | La lógica de cálculo de indicadores y la de construcción y validación de rutinas están cubiertas por pruebas automatizadas | Cobertura igual o superior al 70% en esos módulos   |
| RNF-30 | Toda incorporación de cambios exige la ejecución exitosa de la verificación automatizada                                   | Configuración del repositorio                       |
| RNF-31 | Un integrante que clona el repositorio tiene el sistema en ejecución local en menos de 10 minutos                          | Prueba con un integrante que no lo haya hecho antes |
| RNF-32 | Los cambios de estructura de datos están versionados desde el inicio                                                       | Inspección del repositorio                          |

#### 8. Compatibilidad y accesibilidad

| ID     | Requerimiento                                                                                                          | Criterio de verificación                                                 |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| RNF-33 | Funciona en las dos últimas versiones de los navegadores mayoritarios, de escritorio y móviles                         | Recorrido de FL-05 y FL-02 en cada uno                                   |
| RNF-34 | Contraste de texto conforme al nivel AA, navegación completa por teclado y etiquetas en todos los campos de formulario | Auditoría automatizada más recorrido manual por teclado de FL-02 y FL-05 |
| RNF-35 | ⏸ **DIFERIDO** con RF-049. La presentación en barras por grupo muscular queda cubierta por RNF-34                     | —                                                                        |

#### 9. Escalabilidad

| ID     | Requerimiento                                                                                                                                              | Criterio de verificación                                                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| RNF-36 | El diseño soporta 5.000 alumnos sin rediseño estructural                                                                                                   | Prueba de carga con ese volumen sembrado, cumpliendo RNF-01             |
| RNF-39 | Un cambio del inventario del gimnasio reevalúa todas las rutinas vigentes afectadas en menos de 60 s con 500 alumnos, sin bloquear ninguna sesión en curso | Prueba: retirar un equipamiento usado por el 30% de las rutinas y medir |

#### 10. Alta y arranque

| ID     | Requerimiento                                                                                                           | Criterio de verificación                                                                                               |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| RNF-41 🆕 | El texto libre del usuario queda confinado a la interpretación de RF-053 y no alcanza a ningún otro componente generativo | Inspección del contrato del servicio IA: el único campo de texto libre del usuario es la entrada de `interpretarPedido`; su salida se valida contra las enumeraciones cerradas de D2/§4 y se confirma con el usuario antes de propagarse. `generarRutina`, `sugerirAlternativas` y los narrativos reciben sólo parámetros tipados y estructuras ya validadas |
| RNF-42 🆕 | Todo alumno con contexto suficiente tiene una rutina propuesta dentro de las 24 h de completar su incorporación         | Consulta sobre la base: cero alumnos con contexto suficiente y sin rutina propuesta ni vigente. Es el criterio de éxito E1 hecho comprobable, y **el que la indisponibilidad generativa pone en riesgo** — ver RNF-11 y D12/R-17 |
| RNF-37 | Ninguna cuenta puede crearse sin una invitación vigente                                                                 | Prueba: todo intento de alta sin invitación, con invitación caducada, revocada o ya usada, es rechazado                |
| RNF-38 | El aprovisionamiento de un gimnasio es atómico: o quedan creados el gimnasio y su primer administrador, o no queda nada | Prueba con fallo inducido a mitad del proceso: ningún gimnasio sin administrador en la base                            |
| RNF-40 | El desbloqueo de una sesión es irrepetible y siempre auditado                                                           | Prueba: el segundo desbloqueo de la misma sesión es rechazado, y el primero deja registro con actor, motivo e instante |

---

#### No incluidos deliberadamente

Se nombran para dejar constancia de que fueron considerados y descartados por alcance, lo que vale más que implementarlos a medias:

acuerdo de nivel de servicio de disponibilidad · internacionalización · funcionamiento sin conexión completo · escalado horizontal · alta disponibilidad · doble factor de autenticación · cifrado a nivel de campo · auditoría de seguridad externa · gestión centralizada de secretos.


---

<a id="d13"></a>

### D13 — Trazabilidad

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/requirements/traceability.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D13`

|                |                                              |
| -------------- | -------------------------------------------- |
| **Versión**    | 3.0                                          |
| **Fecha**      | 2026-09-01                                   |
| **Estado**     | Normativo, con la limitación declarada en §0 |
| **Depende de** | D8                                           |

---

#### 0. Limitación de este documento

**El brief original del cliente no forma parte del material recibido.** La voz del cliente disponible es:

1. La sección "Requerimientos nuevos" de la especificación funcional (RF-082 a RF-094), declarada por el cliente como propia.
2. Las decisiones expresadas durante la elaboración de este corpus (18 de agosto de 2026).
3. **El Acta de Redefinición de Alcance** (agosto de 2026), que registra la reunión de relevamiento con el cliente y las cuatro decisiones que el equipo votó en respuesta. Es la fuente de mayor autoridad disponible y la que declara la adaptación como condición de aprobación del proyecto.

**Fuente nueva en la v3.0, que no es la voz del cliente sino la del equipo:** la **votación de requerimientos**, con 8 de 9 integrantes. No decide qué necesita el cliente; decide qué construye el equipo en esta etapa. Se registra en §6 y su efecto sobre el alcance está en el [baseline](#baseline). Cuando el voto y el cliente discrepan, manda el cliente: RF-082 a RF-094 nunca se votaron y entran igual.

Todo lo anterior sólo se conoce a través de la crítica que el análisis de scope hace de él. **La trazabilidad de esa parte es una reconstrucción, no un rastreo**, y está marcada como tal en §2.

---

#### 1. Necesidades expresadas directamente por el cliente

| #    | Necesidad del cliente                                                                                                   | Cómo se recoge                                                                               | Cobertura                                                                                                                                                                                                                                                                                        |
| ---- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| N-01 | Las rutinas deben tener un tipo, y del tipo se derivan estructura, esquemas y descansos                                 | RF-082 · **tabla RN-39a**                                                                    | Total. En la v1.0 la derivación se enunciaba sin existir                                                                                                                                                                                                                                         |
| N-02 | El tipo de rutina debe ser coherente con el objetivo del alumno                                                         | RF-083 · RN-40 · enumeración común (DD-27)                                                   | Total                                                                                                                                                                                                                                                                                            |
| N-03 | Debe registrarse la aptitud, con vencimiento, y advertirse                                                              | RF-084 · RN-13, RN-13a, RN-13b · DD-06                                                       | Total. Se fijó "advierte, no bloquea" y quién la carga                                                                                                                                                                                                                                           |
| N-04 | Las condiciones físicas deben tener historial con vigencia                                                              | RF-085 · RN-10, RN-10a, RN-11 · DD-16                                                        | Total. Se tipó zona corporal y severidad, sin las cuales no eran calculables                                                                                                                                                                                                                     |
| N-05 | Ninguna rutina puede prescribir algo incompatible con el alumno                                                         | RF-086 · **RN-44a a RN-44d**                                                                 | Total. En la v1.0 no había regla que definiera "incompatible"                                                                                                                                                                                                                                    |
| N-06 | Un alumno sin historial debe recibir igual una rutina completa                                                          | RF-087 · FL-01 · FL-04                                                                       | Total, con la precisión de que queda propuesta, no vigente (N-14)                                                                                                                                                                                                                                |
| N-07 | Evaluar periódicamente y diagnosticar progresión, estancamiento y sobreexigencia                                        | RF-088 · **RN-79a** · FL-09                                                                  | Total, y ampliada: cinco situaciones, incorporando `ESTIMULO_INSUFICIENTE`                                                                                                                                                                                                                       |
| N-08 | El sistema debe proponer la adaptación de la rutina                                                                     | RF-089 · **RN-89a** · FL-09                                                                  | Total. En la v1.0 el ajuste no tenía ninguna regla                                                                                                                                                                                                                                               |
| N-09 | Cada ajuste debe estar fundamentado                                                                                     | RF-090 · RN-84                                                                               | Total                                                                                                                                                                                                                                                                                            |
| N-10 | La adaptación requiere aprobación explícita, total o parcial                                                            | RF-091 · RN-86 · FL-10                                                                       | Total, con la rama del alumno derogada por N-14                                                                                                                                                                                                                                                  |
| N-11 | Cada adaptación genera una versión nueva, conservando las anteriores                                                    | RF-092 · DD-02 · D6/§3                                                                       | Total                                                                                                                                                                                                                                                                                            |
| N-12 | Debe poder consultarse el historial de adaptaciones                                                                     | RF-093                                                                                       | Total                                                                                                                                                                                                                                                                                            |
| N-13 | Un cambio de objetivo, condición o aptitud dispara la reevaluación                                                      | RF-094 · RN-91 · FL-12                                                                       | Total, y ampliada al cambio de inventario                                                                                                                                                                                                                                                        |
| N-14 | El entrenador es intermediario: revisa toda rutina antes de que llegue al alumno                                        | RF-110 · RF-112 · RN-35 · FL-02 · DD-25                                                      | Total. **Deroga** la autoasignación de RF-025 y la rama de aprobación por el alumno de RF-091                                                                                                                                                                                                    |
| N-15 | La inteligencia artificial es el centro: debe decidir con el contexto del alumno                                        | D1/§3.0 · Módulos 9 y 10 en MUST · RN-95 · DD-14 · **DD-31** · ADR 0009                       | **Total con barreras declaradas.** El LLM interpreta, selecciona el tipo y construye el candidato inicial; catálogo, compatibilidad y rangos se validan determinísticamente y un entrenador conserva la puerta. Diagnóstico y ajustes siguen reglas auditables                              |
| N-16 | La captación de datos del alumno es primordial como contexto de la inteligencia                                         | RF-111 · RN-97b · RF-031 en MUST · D2 "contexto del alumno"                                  | Total                                                                                                                                                                                                                                                                                            |
| N-17 | El aprendizaje automático predictivo es núcleo                                                                          | RF-121, RF-122 · RF-073                                                                      | **Parcial, y la diferencia hay que declararla.** ✎ v3.0: RF-061 a RF-063 (riesgo de abandono) se retiraron en [DD-34](#d11) por costo frente al valor esperado con los datos disponibles, y la votación lo confirmó con 1, 0 y 0 votos de 8. Lo que queda de aprendizaje automático son dos componentes por alumno **que además están diferidos en la Etapa 1 por no haber sido validados con el cliente**. En esta etapa el proyecto entrega IA generativa, no predictiva |
| N-18 | El sistema debe servir a varios gimnasios                                                                               | RF-069 · RF-098 · RF-100 · DD-05 · DD-24                                                     | Total                                                                                                                                                                                                                                                                                            |
| N-19 | Gestionar gimnasios y sucursales queda fuera                                                                            | D1/§6 · ningún requerimiento de gestión de gimnasios · RF-115 fuera de la aplicación (DD-30) | Total, por exclusión                                                                                                                                                                                                                                                                             |
| N-20 | El estado de membresía informa, no condiciona                                                                           | RF-067 · RN-14 · DD-07                                                                       | Total                                                                                                                                                                                                                                                                                            |
| N-21 | El servicio de generación debe ser gratuito o muy barato                                                                | RF-058 · RNF-18 · S-05                                                                       | **Parcial.** Es una restricción de contratación, no un comportamiento. Lo que el corpus garantiza es que el sistema sigue decidiendo sin él                                                                                                                                                      |
| N-22 | La protección de datos personales de Argentina debe estar cubierta                                                      | RF-096 · RF-105 · RN-104 a RN-106 · RNF-21 a RNF-23                                          | Total en lo que un corpus de requerimientos puede cubrir. **No sustituye asesoramiento legal**                                                                                                                                                                                                   |
| N-23 | Nutrición: generar la dieta, sin seguimiento de comidas, y no como funcionalidad principal                              | RF-075 · RF-108 · **DD-13** · RF-076 WON'T                                                   | **Parcial y decidida.** El sistema produce una pauta de energía y macronutrientes por comida, **sin nombrar alimentos**. Si el cliente entiende por "generar la dieta" un menú con alimentos, hay que reabrir DD-13 antes de construir                                                           |
| N-24 | Los datos pueden provenir de un gimnasio real o de una fuente pública, empezando por la pública y dejándolo adaptable   | RF-070 · RF-071 · RF-106 · S-03                                                              | Total en especificación. La existencia de una fuente adecuada sigue sin verificar                                                                                                                                                                                                                |
| N-25 | La cátedra no impone tecnologías                                                                                        | Sin efecto sobre los requerimientos. Registrado en S-08                                      | —                                                                                                                                                                                                                                                                                                |
| N-26 | **El sistema no es abierto: el gimnasio debe estar afiliado y avisar al usuario para que se registre**                  | RF-115 · RF-116 · RF-098 · RN-02a a RN-02e · **DD-29, DD-30** · FL-00, FL-19                 | Total                                                                                                                                                                                                                                                                                            |
| N-27 | **El foco está en el usuario, pero lo mantiene el gimnasio: la prescripción depende de qué máquinas tiene el gimnasio** | RF-114 · RF-118 · RN-115 a RN-118 · RN-44d, RN-47 · **DD-26** · FL-20                        | Total. Cambió el modelo: el alumno ya no declara equipamiento y la falta de equipamiento pasó de advertir a impedir                                                                                                                                                                              |
| **N-28** 🆕 | **El usuario debe poder ver cómo se ejecuta cada ejercicio; el cliente mencionó video** (Acta de Redefinición §1.4 y §4.3/N11, prioridad SHOULD) | RF-015 exige «al menos un recurso visual» · RF-079 excluye el alojamiento propio           | **Parcial, y es un hueco que el corpus nunca registró.** RF-015 admite una imagen y da por cumplido el requisito; el cliente habló de video, y §4.3 del acta lo pedía como enlace embebido de terceros. **Nadie decidió si el enlace embebido es exigible o si la imagen alcanza.** Ver PD-10 del [baseline](#baseline) |

#### 2. Necesidades reconstruidas del pedido original

Reconstruidas a partir de la crítica del análisis de scope. **No son citas del cliente.**

| #     | Necesidad reconstruida                 | Cobertura                                                                                                                  |
| ----- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| N-R01 | Gestionar rutinas y entrenamientos     | RF-019 a RF-035                                                                                                            |
| N-R02 | Seguimiento entrenador–alumno          | RF-036 a RF-039. Resuelto como observación, intervención y comentarios asincrónicos; **no** como mensajería (RF-077 WON'T) |
| N-R03 | Estadísticas y progreso                | RF-040 a RF-052                                                                                                            |
| N-R04 | Modelo visual del cuerpo humano        | RF-049 en dos dimensiones. **RF-080 excluido** por coste y riesgo frente a la misma necesidad informativa                  |
| N-R05 | Nutrición                              | Ver N-23                                                                                                                   |
| N-R06 | Administración del gimnasio            | RF-065 a RF-069 y RF-114, orientado a analítica y a inventario, no a gestión administrativa                                |
| N-R07 | Componentes de inteligencia artificial | Módulos 9, 10 y 15                                                                                                         |
| N-R08 | Presets de rutina                      | RF-021 `COULD`: un preset es una plantilla publicada y se implementa sólo si el cronograma lo permite                     |

#### 3. Pedidos del cliente no cubiertos, y por qué

| Pedido                                              | Estado          | Motivo                                                                                                                                                                                               |
| --------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mensajería en tiempo real                           | **No cubierto** | RF-077 WON'T. Coste desproporcionado frente a RF-039, y compite con herramientas ya en uso                                                                                                           |
| Gestión de pagos, cuotas y facturación              | **No cubierto** | RF-078 WON'T. Sin relación con el ciclo central. Sustituido parcialmente por RF-067                                                                                                                  |
| Alojamiento de video propio                         | **No cubierto** | RF-079 WON'T. Sustituido por recursos referenciados en RF-015                                                                                                                                        |
| Representación tridimensional del cuerpo            | **No cubierto** | RF-080 WON'T. RF-049 cubre la misma necesidad informativa                                                                                                                                            |
| Integración con dispositivos de monitorización      | **No cubierto** | RF-081 WON'T. Duplicaría la fuente de verdad de la actividad                                                                                                                                         |
| Base de alimentos y composición de comidas          | **No cubierto** | RF-076 WON'T, confirmado por el cliente                                                                                                                                                              |
| Menú con alimentos concretos                        | **No cubierto** | DD-13: el sistema produce una pauta de energía y macronutrientes. **Es la única divergencia consciente respecto de lo que el cliente pidió con esas palabras, y está señalada para que la confirme** |
| Control de acceso o registro de entrada al gimnasio | **No cubierto** | Nunca requerido formalmente. Crearía una segunda fuente de verdad de asistencia que contradiría a las sesiones                                                                                       |
| Alta y administración de gimnasios y sucursales     | **No cubierto** | Excluido por el cliente (N-19). El gimnasio existe como ámbito, no como objeto administrable                                                                                                         |
| Recordatorios por correo o notificación externa     | **No cubierto** | Sólo avisos dentro de la aplicación (RF-095). El correo se usa únicamente para la invitación y la recuperación de acceso                                                                             |
| Entrenar sin entrenador asignado                    | **No cubierto** | Consecuencia de N-14. Un alumno sin entrenador conserva su rutina vigente pero no puede recibir ninguna nueva. Declarado en D1/§6                                                                    |
| Rutinas con equipamiento propio del alumno          | **No cubierto** | Consecuencia de N-27 y DD-26. El sistema prescribe para el gimnasio que lo mantiene                                                                                                                  |

#### 4. Requerimientos sin necesidad de origen

Requerimientos que **nadie pidió** y que existen porque sin ellos el sistema es incoherente.

| RF                                                | Por qué existe                                                                                                                           |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| RF-095 · avisos dentro de la aplicación           | RF-038, RF-044 y RF-046 prometen notificar y no había canal                                                                              |
| RF-096 · consentimiento de datos de salud         | Se registran condiciones, aptitud y mediciones sin base para tratarlos                                                                   |
| RF-097 · auditoría                                | Había trazabilidad en tres puntos y ninguna regla general                                                                                |
| RF-098 · vinculación a un gimnasio                | Sin ella, la pertenencia al gimnasio no quedaba determinada por nada                                                                     |
| RF-099 · taxonomía muscular y de articulaciones   | RF-016, RF-040, RF-049 y toda la compatibilidad dependen de listas que nadie definía                                                     |
| RF-100 · ámbito del catálogo                      | RF-013 y RF-069 eran incompatibles sin esta distinción                                                                                   |
| RF-101 · ejercicio desactivado en rutina vigente  | RF-018 protegía el historial y callaba sobre las rutinas activas                                                                         |
| RF-102, RF-103 · unidades y marco temporal        | Sin ellos ningún cálculo es verificable                                                                                                  |
| RF-104 · idempotencia                             | El registro ocurre con conexión inestable; el envío duplicado es cotidiano                                                               |
| RF-105, RF-106 · anonimización y datos simulados  | La baja de cuenta contra la analítica agregada, y los simulados contra los reales, eran conflictos sin resolver                          |
| RF-107 · criterio de urgencia                     | RF-036 pedía ordenar por urgencia sin definirla, y no era verificable                                                                    |
| RF-109, RF-110, RF-112 · la puerta del entrenador | Derivados de N-14. RF-112 evita que el alumno quede en un limbo silencioso                                                               |
| RF-111 · contexto suficiente                      | Derivado de N-15 y N-16: sin él, la inteligencia decide con huecos y nadie se entera                                                     |
| RF-113 · descarte de salidas inválidas            | Consecuencia de N-15: si la inteligencia decide, hace falta una regla sobre qué ocurre cuando decide mal                                 |
| RF-115 · aprovisionamiento                        | Derivado de N-26: si el alta es por invitación, alguien tiene que emitir la primera                                                      |
| RF-117 · desbloqueo de sesión                     | Sin él, un error detectado tarde contaminaba de forma permanente la carga máxima estimada, el diagnóstico y toda la cadena de adaptación |
| RF-118 · catálogo prescribible                    | Derivado de N-27: es el conjunto operativo sobre el que trabajan la generación, la validación y la recomendación                         |

#### 6. La votación del equipo como fuente

La votación no es la voz del cliente: es la del equipo decidiendo qué construye en esta etapa. Se registra aquí porque a partir de la v4.0 de D8 explica por qué un requisito está o no está en el alcance, y sin ese registro las marcas de alcance de D8 quedan sin origen.

**Forma.** Planilla de requerimientos RF-001 a RF-081, una marca por integrante. Votaron 8 de 9. **Regla de corte: 5 votos o más entra al alcance de la Etapa 1.** RF-082 a RF-094 se agregaron a la planilla después de la reunión con el cliente y **nunca se votaron**: entran por autoridad del cliente. RF-095 a RF-122 no existían cuando se votó.

**Lo que la votación confirmó.** El ciclo central obtuvo mayorías amplias sin excepción: contexto del alumno 8/8, catálogo 8/8, plantillas 8/8, registro de series 8/8, historial 8/8, indicadores de volumen y capacidad máxima 8/8, generación y su justificación 8/8, alternativas de sustitución 8/8. **La votación no cuestionó el producto: cuestionó su periferia.**

**Lo que la votación retiró**, y coincide en lo esencial con el orden de recorte que D12 ya tenía escrito: nutrición (2/8 y 1/8), comentarios (1/8), panel del gimnasio (2/8), parametrización de reglas (3/8), riesgo de abandono (1/8, 0/8, 0/8), presets (1/8).

**Los cuatro resultados que hubo que corregir, y por qué.** La regla de corte se aplicó, pero no de forma mecánica:

| Caso                                              | Votos | Qué se hizo y por qué                                                                                                                                                                                                                                    |
| ------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **RF-022** · copia independiente al asignar       | 0/8   | **Reincorporado.** La observación de la planilla lo agrupa con los presets; no lo es. Es el invariante de [PD-01 del modelo](#d4) y [DD-02](#d11): sin él, adaptar una rutina reescribe el historial de todos los alumnos que comparten plantilla |
| **RF-043** · cumplimiento de la prescripción      | 0/8   | **Reincorporado.** RN-79a lo usa para detectar `SOBREEXIGENCIA`; sin él el diagnóstico pierde dos de sus cinco situaciones. Y es lo único que distingue este producto de un registrador                                                                    |
| **RF-005 y RF-069** · autorización y aislamiento  | 2/8, 4/8 | **Reincorporados.** Son RA-01, RNF-14, RNF-20 y la mitigación de R-11. Sin ellos cualquiera lee los datos de salud de cualquiera                                                                                                                     |
| **RF-053** · interpretación de lenguaje natural   | 3/8   | **Conservado.** Está comprometido por escrito ante el Product Owner (`deliverable PO/alcance-ia-generativa.md` v2.1). Una votación interna no revoca un compromiso asumido. Ver I-10 en D12/§5                                                           |

**Las fusiones sugeridas por el equipo, resueltas.** Se aceptaron RF-032 ⊕ RF-033 → RF-027 (ampliada a RF-027, porque son tres transiciones del mismo autómata) y RF-004 → RF-065. **Se rechazó RF-054 ⊕ RF-055**, porque borra la frontera entre componente de decisión y componente narrativo y deja sin sujeto a RNF-24. **Se rechazó RF-005 dentro de la gestión de roles**, porque haría desaparecer la verificación por recurso.

La trazabilidad completa voto a voto está en el anexo del [baseline de alcance](#baseline).

#### 5. Cobertura inversa

Cada capacidad central de D1 y los requerimientos que la sostienen. Si alguna columna quedara vacía, el producto no cumpliría su propia definición.

| Capacidad                                                    | Requerimientos                                                 |
| ------------------------------------------------------------ | -------------------------------------------------------------- |
| C1 · Nadie queda sin plan                                    | RF-087, RF-025, RF-112, RF-111, RF-116                         |
| C2 · Ninguna prescripción contradice el estado de la persona | RF-086, RF-094, RF-009, RF-084, RF-085, RF-060, RF-114, RF-118 |
| C3 · La evolución se evalúa sola                             | RF-088, RF-040 a RF-046 ✎ *(v3.0: se retira RF-061)*           |
| C4 · El cambio lo decide el sistema, con fundamento          | RF-089, RF-090, RF-054, RF-059, RF-057, RF-072, RF-073         |
| C5 · El entrenador es la puerta                              | RF-110, RF-091, RF-036, RF-038, RF-109, RF-107                 |
| Sustrato de datos del que todo depende                       | RF-027 a RF-035, RF-031, RF-102, RF-103, RF-104                |
| Condición de existencia del gimnasio                         | RF-115, RF-116, RF-114, RF-118                                 |


---

<a id="parte-vi"></a>

## Parte VI — Arquitectura

<a id="arch-system"></a>

### Arquitectura general del sistema

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/system-overview.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-SYSTEM`

#### Topología

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

#### Propiedad de contratos

- Backend es dueño del OpenAPI público, del esquema transaccional, de las estructuras de integración y de las migraciones.
- Frontend genera tipos y cliente desde una versión explícita del OpenAPI del backend.
- IA es dueña del OpenAPI de su servicio de orquestación; backend genera o valida el cliente desde una versión explícita.
- El conector IA–LLM es privado del repositorio IA.
- Los jobs batch usan datasets versionados mediante vistas o snapshots descritos en [data-interface.md](#arch-data-interface).
- Un cambio incompatible conserva compatibilidad temporal y coordina PR relacionados.

#### Invariantes transversales

1. El historial ejecutado y las versiones congeladas nunca se reescriben.
2. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
3. PostgreSQL es la fuente de verdad transaccional; el LLM no accede a ella.
4. Toda salida inteligente registra versión, instante y contexto mínimo reproducible.
5. Backend mantiene autorización y validaciones de negocio; IA sólo persiste estados y resultados en estructuras designadas.
6. La indisponibilidad generativa no produce una rutina insegura ni degrada el resto del sistema: se deshabilita esa capacidad y permanecen las plantillas y operaciones manuales. ✎ **Deja de ser una degradación menor**: sin presets obligatorios, la generación es la única vía automática de prescripción, de modo que su caída impide dar plan a un alumno nuevo si el gimnasio no tiene plantillas cargadas. Ver [D11/DD-35](#d11) y D12/R-17.
7. Test y producción no comparten base ni credenciales, aunque inicialmente compartan API y configuración del modelo.

#### Detalle por componente

- [Frontend](#arch-frontend)
- [Backend](#arch-backend)
- [Servicio IA y analítica](#arch-analytics)
- [Interfaz de datos backend–IA](#arch-data-interface)
- [Integración generativa](#arch-generative-integration)


---

<a id="arch-frontend"></a>

### Arquitectura del frontend

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/frontend.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-FRONTEND`

#### Distribución

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

#### Contratos

- Backend es dueño de su OpenAPI y de toda estructura persistida.
- Frontend genera tipos y cliente desde una versión explícita de ese OpenAPI; no comparte código con backend.
- Frontend no consume el OpenAPI de IA ni conoce ngrok, el LLM o PostgreSQL.
- Los cambios incompatibles se coordinan mediante versionado y PR relacionados.

#### Responsabilidad

- Presentación, accesibilidad y estado de interacción.
- Estado remoto mediante TanStack Query.
- Polling de una generación asíncrona sólo contra backend, detenido en un estado terminal.
- Conservación local del identificador de una generación activa y del borrador de sesión cuando corresponda.
- Estados de carga, reintento e indisponibilidad. ✎ No se ofrece un preset como salida alternativa: RF-021 es alcance opcional. Ante indisponibilidad generativa el alumno ve el estado, no una acción que puede no existir.
- Validaciones de experiencia de usuario que la API vuelve a comprobar.

#### Invariantes

1. El frontend nunca accede directamente a PostgreSQL, Prisma, IA, ngrok ni proveedores externos.
2. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
3. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
4. La indisponibilidad de IA deshabilita la generación, no el resto del producto. ✎ Lo que permanece es la creación y asignación manual de plantillas por el entrenador (RF-019); los presets, sólo si se implementa RF-021 ([DD-35](#d11)).
5. Ninguna lógica de autorización o compatibilidad se confía sólo al cliente.


---

<a id="arch-backend"></a>

### Arquitectura del backend

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/backend.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-BACKEND`

#### Distribución

```text
React SPA -> Express + TypeScript -> Neon PostgreSQL
                 |
                 | HTTPS / OpenAPI IA
                 v
             ngrok -> API Python / Polo
```

El backend es un monolito modular desplegado en Vercel y dueño del OpenAPI público, las invariantes transaccionales, la autorización, Prisma y las migraciones.

#### Responsabilidad

Los módulos previstos son identidad, catálogo, rutinas, entrenamiento, métricas, seguimiento, administración e integración IA. Se crean al implementar historias verticales. Los routers sólo traducen HTTP; reglas y autorización viven en servicios o funciones de dominio y Prisma queda detrás de adaptadores de persistencia.

#### Fronteras

- OpenAPI del backend es la fuente de verdad para frontend.
- Prisma no se expone como contrato HTTP.
- PostgreSQL es la única fuente de verdad transaccional.
- Backend autoriza, minimiza el contexto y crea solicitudes idempotentes antes de invocar IA.
- El cliente del servicio IA se genera o valida desde el OpenAPI versionado por ese repositorio.
- El backend nunca espera al LLM: la API IA acepta con `202` y frontend consulta estado al backend.
- IA puede escribir sólo estados y resultados en estructuras de integración; backend es el único que crea entidades de dominio.
- Entrenamiento y scoring predictivo siguen fuera del camino de las peticiones.

#### Fallos y seguridad

- Cada intento generativo vence inicialmente a los 120 segundos y admite un único reintento.
- Una salida inválida nunca se presenta. Tras el segundo fallo la capacidad queda no disponible; no existe fallback determinístico de generación.
- El resto del sistema continúa y las plantillas privadas del entrenador y su creación manual permanecen disponibles (RF-019). ✎ El preset publicado (RF-021) pasa a alcance opcional y **no es la contingencia**: ver [D11/DD-35](#d11).
- Credenciales y conexiones test/producción son distintas; ninguna URL de base se recibe desde una petición.
- El Polo recibe sólo contexto necesario y un identificador técnico, nunca credenciales ni identificadores personales innecesarios.

#### Invariantes

1. Una plantilla se copia al solicitar una rutina; cambios posteriores no reescriben versiones existentes.
2. Al comenzar una sesión se congela lo prescripto junto a lo realmente ejecutado.
3. Historial e indicadores derivados no son fuentes de verdad editables.
4. El entrenador es la puerta de aprobación para poner una rutina en vigencia.
5. La autorización combina rol y propiedad o asignación del recurso.
6. Ningún resultado IA evita las validaciones de catálogo, compatibilidad, rangos y permisos.


---

<a id="arch-database"></a>

### Modelo relacional de PostgreSQL

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/database-relational-model.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-DATABASE`

**Estado:** propuesto para revisión · **Fecha:** 2026-09-01

#### Alcance y autoridad

Este documento traduce el [modelo de dominio](#d4) a una estructura relacional implementable en PostgreSQL 17. El dominio, las enumeraciones y los ciclos de vida continúan definidos exclusivamente por D2, D4, D5 y D6; aquí se definen tablas, claves, relaciones, restricciones e interfaces de acceso.

El backend es dueño de Prisma, del esquema y de todas las migraciones. El servicio IA sólo accede a las tablas del esquema `ai_integration` que se le concedan explícitamente.

#### Decisiones de modelado

- Usar `uuid` con `gen_random_uuid()` para claves primarias y `timestamptz` para instantes.
- Usar `date` para fechas del dominio y `numeric` para medidas, cargas y valores que no deben perder precisión.
- Usar nombres `snake_case`, claves foráneas explícitas y `created_at`/`updated_at` donde corresponda.
- Representar estados y enumeraciones cerradas mediante enums de Prisma/PostgreSQL; equipamiento, grupos musculares y articulaciones son tablas de referencia porque además tienen nombre, región y orden de presentación.
- Mantener las entidades transaccionales normalizadas. Reservar `jsonb` para snapshots técnicos de IA, explicaciones, métricas y auditoría, no para relaciones centrales.
- No borrar físicamente usuarios, ejercicios, plantillas, rutinas ni sesiones con historia. Se cambia su estado o se anonimizan los datos personales.
- Crear dos esquemas PostgreSQL en esta entrega:
  - `app`: fuente de verdad transaccional, accesible sólo por backend y migraciones;
  - `ai_integration`: cola durable y resultados técnicos, con permisos mínimos para backend e IA.
- No crear el esquema `analytics` en esta entrega. Si posteriormente se aprueba la etapa analítica, se incorporará mediante una migración específica junto con sus tablas y permisos.

##### Distribución física por esquema

- `app` contiene las 40 tablas transaccionales de las secciones 1 a 6 y `routine_candidate_generations`, que asocia un candidato del dominio con una solicitud técnica sin exponer el candidato al servicio IA: 41 tablas en total.
- `ai_integration` contiene únicamente `ai_generation_requests`, `ai_generation_attempts`, `ai_generation_results` y `ai_result_validations`.
- Backend y el rol de migraciones operan sobre ambos esquemas. El servicio IA recibe permisos mínimos sólo sobre las tablas necesarias de `ai_integration` y ningún permiso sobre `app`.

#### Vista general

```mermaid
erDiagram
    GYMS ||--o{ USERS : contains
    GYMS ||--o{ GYM_EQUIPMENT : declares
    USERS ||--o| STUDENT_PROFILES : may_have
    USERS ||--o| TRAINER_PROFILES : may_have
    STUDENT_PROFILES ||--o{ TRAINER_STUDENT_ASSIGNMENTS : receives
    TRAINER_PROFILES ||--o{ TRAINER_STUDENT_ASSIGNMENTS : supervises
    GYMS ||--o{ EXERCISES : owns
    GYMS ||--o{ ROUTINE_TEMPLATES : owns
    STUDENT_PROFILES ||--o{ ROUTINES : receives
    ROUTINES ||--o{ ROUTINE_VERSIONS : versions
    ROUTINE_VERSIONS ||--o{ TRAINING_SESSIONS : freezes
    STUDENT_PROFILES ||--o{ ROUTINE_CANDIDATES : requests
    ROUTINE_CANDIDATES ||--o{ ROUTINE_CANDIDATE_GENERATIONS : regenerates
    AI_GENERATION_REQUESTS ||--o{ ROUTINE_CANDIDATE_GENERATIONS : feeds
    AI_GENERATION_REQUESTS ||--o{ AI_GENERATION_ATTEMPTS : attempts
    AI_GENERATION_ATTEMPTS ||--o| AI_GENERATION_RESULTS : produces
    USERS ||--o{ NOTICES : receives
    USERS ||--o{ AUDIT_LOGS : acts
```

#### 1. Gimnasio, identidad y acceso

```mermaid
erDiagram
    GYMS {
        uuid id PK
        string name
        string timezone
        string affiliation_status
        boolean active
    }
    INVITATIONS {
        uuid id PK
        uuid gym_id FK
        uuid issued_by_user_id FK
        string email_normalized
        string status
        datetime expires_at
        uuid consumed_by_user_id FK
    }
    INVITATION_ROLES {
        uuid invitation_id PK,FK
        string role PK
    }
    USERS {
        uuid id PK
        uuid gym_id FK
        uuid invitation_id FK
        string email_normalized
        string display_name
        string password_hash
        string state
        datetime created_at
    }
    USER_ROLES {
        uuid user_id PK,FK
        string role PK
    }
    CONSENTS {
        uuid id PK
        uuid user_id FK
        string type
        boolean granted
        string accepted_text
        datetime recorded_at
    }
    AUTH_SESSIONS {
        uuid id PK
        uuid user_id FK
        string token_hash
        datetime last_activity_at
        datetime expires_at
        datetime revoked_at
    }
    PASSWORD_RESET_TOKENS {
        uuid id PK
        uuid user_id FK
        string token_hash
        datetime expires_at
        datetime used_at
    }

    GYMS ||--o{ INVITATIONS : issues_for
    USERS ||--o{ INVITATIONS : issues
    INVITATIONS ||--|{ INVITATION_ROLES : offers
    GYMS ||--|{ USERS : contains
    INVITATIONS o|--o| USERS : creates
    USERS ||--|{ USER_ROLES : has
    USERS ||--o{ CONSENTS : records
    USERS ||--o{ AUTH_SESSIONS : authenticates
    USERS ||--o{ PASSWORD_RESET_TOKENS : recovers
```

Restricciones principales:

- `users`: `UNIQUE (gym_id, email_normalized)`.
- `users.invitation_id`: único y anulable sólo para el primer administrador aprovisionado.
- `invitation_roles` y `user_roles`: clave primaria compuesta.
- Toda invitación vence a los 14 días y produce como máximo un usuario.
- Los tokens se guardan hasheados; nunca se almacena el valor utilizable.
- La aplicación impide eliminar el último rol de un usuario y el último administrador activo del gimnasio.

#### 2. Perfiles y relación entrenador–alumno

```mermaid
erDiagram
    USERS {
        uuid id PK
        uuid gym_id FK
    }
    STUDENT_PROFILES {
        uuid user_id PK,FK
        date birth_date
        string sex
        decimal height_cm
        string experience_level
        int available_days_per_week
        string membership_state
        string activity_level
    }
    TRAINER_PROFILES {
        uuid user_id PK,FK
        string specialty
        int experience_years
        string presentation
    }
    GOALS {
        uuid id PK
        uuid student_id FK
        string type
        date starts_on
        date ends_on
    }
    PHYSICAL_CONDITIONS {
        uuid id PK
        uuid student_id FK
        string body_zone_code
        string severity
        string description
        date starts_on
        date ends_on
    }
    FITNESS_CLEARANCES {
        uuid id PK
        uuid student_id FK
        uuid recorded_by_user_id FK
        date issued_on
        date expires_on
        string observation
    }
    BODY_MEASUREMENTS {
        uuid id PK
        uuid student_id FK
        string type
        decimal value
        date measured_on
    }
    TRAINER_STUDENT_ASSIGNMENTS {
        uuid id PK
        uuid student_id FK
        uuid trainer_id FK
        datetime starts_at
        datetime ends_at
        uuid started_by_user_id FK
        uuid ended_by_user_id FK
    }

    USERS ||--o| STUDENT_PROFILES : extends
    USERS ||--o| TRAINER_PROFILES : extends
    STUDENT_PROFILES ||--o{ GOALS : declares
    STUDENT_PROFILES ||--o{ PHYSICAL_CONDITIONS : reports
    STUDENT_PROFILES ||--o{ FITNESS_CLEARANCES : has
    USERS ||--o{ FITNESS_CLEARANCES : records
    STUDENT_PROFILES ||--o{ BODY_MEASUREMENTS : measures
    STUDENT_PROFILES ||--o{ TRAINER_STUDENT_ASSIGNMENTS : receives
    TRAINER_PROFILES ||--o{ TRAINER_STUDENT_ASSIGNMENTS : supervises
```

Restricciones principales:

- Índice único parcial en `goals (student_id) WHERE ends_on IS NULL`.
- Índice único parcial en `trainer_student_assignments (student_id) WHERE ends_at IS NULL`.
- `trainer_id <> student_id`.
- `body_measurements`: `UNIQUE (student_id, type, measured_on)`.
- Toda fecha de fin debe ser posterior a la de inicio.
- Los perfiles sólo existen si el usuario posee el rol correspondiente; esta invariante se valida transaccionalmente en backend.

#### 3. Inventario y catálogo de ejercicios

```mermaid
erDiagram
    GYMS {
        uuid id PK
    }
    EQUIPMENT {
        string code PK
        string name
        int display_order
    }
    GYM_EQUIPMENT {
        uuid gym_id PK,FK
        string equipment_code PK,FK
        boolean present
        uuid updated_by_user_id FK
        datetime updated_at
    }
    MUSCLE_GROUPS {
        string code PK
        string name
        string region
    }
    JOINTS {
        string code PK
        string name
        string region
    }
    EXERCISES {
        uuid id PK
        uuid gym_id FK
        uuid author_user_id FK
        string name
        string instructions
        string movement_pattern
        string difficulty_level
        boolean unilateral
        string visual_resource_url
        string origin
        string state
    }
    EXERCISE_EQUIPMENT {
        uuid exercise_id PK,FK
        string equipment_code PK,FK
    }
    EXERCISE_MUSCLES {
        uuid exercise_id PK,FK
        string muscle_code PK,FK
        string participation
    }
    EXERCISE_JOINTS {
        uuid exercise_id PK,FK
        string joint_code PK,FK
    }

    GYMS ||--o{ GYM_EQUIPMENT : inventories
    EQUIPMENT ||--o{ GYM_EQUIPMENT : appears_in
    GYMS o|--o{ EXERCISES : owns_custom
    EXERCISES ||--o{ EXERCISE_EQUIPMENT : requires
    EQUIPMENT ||--o{ EXERCISE_EQUIPMENT : required_by
    EXERCISES ||--o{ EXERCISE_MUSCLES : activates
    MUSCLE_GROUPS ||--o{ EXERCISE_MUSCLES : classifies
    EXERCISES ||--o{ EXERCISE_JOINTS : demands
    JOINTS ||--o{ EXERCISE_JOINTS : classifies
```

Restricciones principales:

- `exercises.gym_id IS NULL` sólo cuando `origin = 'CATALOGO_BASE'`; un ejercicio propio siempre informa gimnasio y autor.
- `UNIQUE (gym_id, lower(name))` para ejercicios propios; el catálogo base usa un índice equivalente con `gym_id IS NULL`.
- Índice único parcial en `exercise_muscles (exercise_id) WHERE participation = 'PRIMARIA'`.
- `PESO_CORPORAL` se carga como equipamiento de referencia y se considera siempre presente.
- Un ejercicio no se borra: pasa a `DESACTIVADO` y permanece referenciable por el historial.

#### 4. Plantillas, candidatos y rutinas

```mermaid
erDiagram
    ROUTINE_TEMPLATES {
        uuid id PK
        uuid gym_id FK
        uuid author_trainer_id FK
        string name
        string routine_type
        boolean active
    }
    TEMPLATE_DAYS {
        uuid id PK
        uuid template_id FK
        int position
        string name
    }
    TEMPLATE_EXERCISES {
        uuid id PK
        uuid template_day_id FK
        uuid exercise_id FK
        int position
        string note
    }
    TEMPLATE_SETS {
        uuid id PK
        uuid template_exercise_id FK
        int position
        int min_repetitions
        int max_repetitions
        decimal suggested_load
        int rest_seconds
        boolean warmup
    }
    ROUTINE_CANDIDATES {
        uuid id PK
        uuid student_id FK
        uuid requested_by_user_id FK
        string technical_status
        json current_structure
        int regeneration_count
        datetime last_activity_at
        datetime expires_at
        datetime confirmed_at
    }
    ROUTINES {
        uuid id PK
        uuid student_id FK
        uuid source_template_id FK
        uuid source_candidate_id FK
        string routine_type
        int target_weekly_frequency
        string state
        string origin
        uuid requested_by_user_id FK
        datetime requested_at
    }
    ROUTINE_REVIEWS {
        uuid id PK
        uuid routine_id FK
        uuid reviewed_version_id FK
        uuid reviewer_trainer_id FK
        string result
        string observation
        datetime reviewed_at
    }
    ROUTINE_VERSIONS {
        uuid id PK
        uuid routine_id FK
        int version_number
        boolean current
        uuid created_by_user_id FK
        uuid adaptation_proposal_id FK
        datetime created_at
    }
    ROUTINE_DAYS {
        uuid id PK
        uuid routine_version_id FK
        int position
        string name
        string dominant_pattern
    }
    ROUTINE_EXERCISES {
        uuid id PK
        uuid routine_day_id FK
        uuid exercise_id FK
        int position
        string note
        string compatibility_state
        string compatibility_reason
    }
    PRESCRIBED_SETS {
        uuid id PK
        uuid routine_exercise_id FK
        int position
        int min_repetitions
        int max_repetitions
        decimal suggested_load
        int rest_seconds
        boolean warmup
    }

    ROUTINE_TEMPLATES ||--|{ TEMPLATE_DAYS : contains
    TEMPLATE_DAYS ||--|{ TEMPLATE_EXERCISES : contains
    TEMPLATE_EXERCISES ||--|{ TEMPLATE_SETS : prescribes
    ROUTINE_CANDIDATES o|--o| ROUTINES : confirms_into
    ROUTINE_TEMPLATES o|--o{ ROUTINES : originates
    ROUTINES ||--o{ ROUTINE_REVIEWS : receives
    ROUTINES ||--|{ ROUTINE_VERSIONS : versions
    ROUTINE_VERSIONS ||--|{ ROUTINE_DAYS : contains
    ROUTINE_DAYS ||--|{ ROUTINE_EXERCISES : contains
    ROUTINE_EXERCISES ||--|{ PRESCRIBED_SETS : prescribes
    ROUTINE_VERSIONS ||--o{ ROUTINE_REVIEWS : reviewed_as
```

`routine_candidates` es almacenamiento técnico temporal, no una rutina ni un nuevo estado de `routines`. En la primera entrega sólo representa candidatos generados por IA: los presets son alcance opcional y no agregan tablas ni columnas hasta que se decida implementarlos. Conserva el snapshot ajustable para recuperar el flujo y reconstruir diferencias. Al confirmar, el backend crea en una transacción `routines`, `routine_versions`, días, ejercicios y series.

Un candidato usa los estados técnicos `ACTIVO`, `CONFIRMADO` y `ABANDONADO`. Mientras está activo expira después de 24 horas sin actividad; cada ajuste o regeneración actualiza `last_activity_at` y `expires_at`. Al confirmarlo se conservan identificador, solicitante, solicitudes y resultados generativos relacionados, cantidad de regeneraciones e instantes. La estructura final vive únicamente en las tablas relacionales de la rutina.

Restricciones principales:

- Orden único dentro de cada plantilla, día, versión y ejercicio.
- Una plantilla debe pertenecer al mismo gimnasio que su autor.
- `routine_candidates.regeneration_count BETWEEN 0 AND 3`.
- `routine_candidates.expires_at = last_activity_at + interval '24 hours'` mientras el candidato esté `ACTIVO`.
- Índices únicos parciales separados para una rutina `PROPUESTA` y una `VIGENTE` por alumno.
- `UNIQUE (routine_id, version_number)` e índice único parcial en `routine_versions (routine_id) WHERE current`.
- Una revisión favorable sólo puede crear o activar una versión si el revisor tiene una asignación vigente con el alumno.
- Toda rutina conserva copia profunda; modificar una plantilla nunca modifica una rutina existente.

#### 5. Sesiones y prescripción congelada

```mermaid
erDiagram
    ROUTINES {
        uuid id PK
    }
    ROUTINE_VERSIONS {
        uuid id PK
    }
    ROUTINE_DAYS {
        uuid id PK
    }
    TRAINING_SESSIONS {
        uuid id PK
        uuid student_id FK
        uuid routine_id FK
        uuid routine_version_id FK
        uuid routine_day_id FK
        string state
        datetime started_at
        datetime completed_at
        date occurred_on
        boolean deferred
        boolean simulated
        datetime unlocked_until
    }
    SESSION_SET_RECORDS {
        uuid id PK
        uuid session_id FK
        int position
        uuid prescribed_exercise_id FK
        uuid performed_exercise_id FK
        int prescribed_min_repetitions
        int prescribed_max_repetitions
        decimal prescribed_load
        boolean warmup
        decimal performed_load
        int performed_repetitions
        int perceived_effort
        boolean completed
        boolean additional
        string omission_reason
        boolean atypical_confirmed
    }
    SESSION_UNLOCKS {
        uuid id PK
        uuid session_id FK
        uuid trainer_id FK
        string reason
        datetime unlocked_at
        datetime expires_at
    }
    COMMENTS {
        uuid id PK
        uuid author_user_id FK
        uuid session_id FK
        uuid routine_id FK
        string text
        datetime created_at
    }

    ROUTINES ||--o{ TRAINING_SESSIONS : used_in
    ROUTINE_VERSIONS ||--o{ TRAINING_SESSIONS : freezes
    ROUTINE_DAYS ||--o{ TRAINING_SESSIONS : executes
    TRAINING_SESSIONS ||--|{ SESSION_SET_RECORDS : records
    TRAINING_SESSIONS ||--o| SESSION_UNLOCKS : may_unlock_once
    TRAINING_SESSIONS o|--o{ COMMENTS : receives
    ROUTINES o|--o{ COMMENTS : receives
```

Al iniciar una sesión se crean los `session_set_records` copiando la prescripción vigente. Los campos prescriptos y ejecutados permanecen juntos para que el historial no dependa de cambios posteriores.

Restricciones principales:

- Índice único parcial en `training_sessions (student_id) WHERE state = 'EN_CURSO'`.
- `UNIQUE (session_id, position)` en registros de serie.
- `UNIQUE (session_id)` en `session_unlocks`: una sesión sólo se desbloquea una vez.
- `perceived_effort BETWEEN 1 AND 10` cuando se informa.
- Un comentario referencia exactamente una sesión o una rutina mediante un `CHECK` exclusivo.
- La prescripción copiada en una sesión no se actualiza después de crearla.

#### 6. Avisos y auditoría transaccional

```mermaid
erDiagram
    USERS {
        uuid id PK
    }
    NOTICES {
        uuid id PK
        uuid recipient_user_id FK
        string type
        string reference_type
        uuid reference_id
        string text
        datetime created_at
        datetime read_at
        boolean expired
    }
    AUDIT_LOGS {
        uuid id PK
        uuid actor_user_id FK
        string operation
        string entity_type
        uuid entity_id
        json previous_value
        json new_value
        datetime created_at
    }

    USERS ||--o{ NOTICES : receives
    USERS ||--o{ AUDIT_LOGS : acts
```

Ambas tablas pertenecen a `app`: los avisos forman parte de la experiencia transaccional del usuario y la auditoría registra operaciones sensibles del backend. Ninguna es una salida analítica ni debe ser accesible por el servicio IA.

Restricciones principales:

- Los tipos de aviso usan la enumeración cerrada de D2.
- La no repetición, caducidad y reasignación de avisos siguen las reglas de RF-095 y D5.
- La auditoría cubre las operaciones sensibles enumeradas en RF-097.

#### 7. Interfaz durable Backend–IA

```mermaid
erDiagram
    ROUTINE_CANDIDATES {
        uuid id PK
    }
    ROUTINE_CANDIDATE_GENERATIONS {
        uuid candidate_id PK,FK
        uuid generation_request_id PK,FK
        int generation_number
    }
    AI_GENERATION_REQUESTS {
        uuid id PK
        string idempotency_key
        string state
        json minimized_context
        json preferences
        string context_hash
        datetime available_at
        string lease_owner
        datetime lease_until
        datetime created_at
        datetime finished_at
        datetime retention_until
    }
    AI_GENERATION_ATTEMPTS {
        uuid id PK
        uuid request_id FK
        int attempt_number
        string state
        datetime started_at
        datetime finished_at
        string error_code
        string model_version
        string configuration_version
        string contract_version
        string input_hash
    }
    AI_GENERATION_RESULTS {
        uuid id PK
        uuid attempt_id FK
        json structured_output
        string output_hash
        boolean structurally_valid
        datetime created_at
        datetime retention_until
    }
    AI_RESULT_VALIDATIONS {
        uuid id PK
        uuid result_id FK
        string validator_version
        boolean valid
        json violations
        datetime validated_at
    }

    ROUTINE_CANDIDATES ||--o{ ROUTINE_CANDIDATE_GENERATIONS : requests
    AI_GENERATION_REQUESTS ||--o| ROUTINE_CANDIDATE_GENERATIONS : belongs_to
    AI_GENERATION_REQUESTS ||--o{ AI_GENERATION_ATTEMPTS : retries
    AI_GENERATION_ATTEMPTS ||--o| AI_GENERATION_RESULTS : produces
    AI_GENERATION_RESULTS ||--o{ AI_RESULT_VALIDATIONS : checked_by_backend
```

`routine_candidate_generations` pertenece físicamente a `app`; las otras cuatro tablas del diagrama pertenecen a `ai_integration`. El backend administra la asociación y el servicio IA no recibe permisos para leer candidatos ni sus identificadores.

Estados técnicos aceptados:

- solicitud: `PENDIENTE`, `PROCESANDO`, `COMPLETADA`, `NO_DISPONIBLE`, `CANCELADA`;
- intento: `PENDIENTE`, `PROCESANDO`, `COMPLETADO`, `FALLIDO`, `AGOTADO_POR_TIEMPO`, `SALIDA_INVALIDA`.

Estos estados se incorporan a D6 antes de implementar la migración.

##### Contratos JSON versionados

Los campos `jsonb` no admiten estructuras libres. Sus contratos se publican en el OpenAPI del servicio IA y se validan con Pydantic en Python y Zod en backend.

- `minimized_context`: `schema_version`, objetivo, nivel de experiencia, frecuencia, condiciones físicas pertinentes sin texto identificatorio, equipamiento disponible y catálogo permitido. No contiene identificador de usuario, nombre, correo, teléfono, documento ni credenciales.
- `preferences`: `schema_version`, ejercicios excluidos, patrones preferidos y observaciones sanitizadas que aporten a la generación.
- `structured_output`: `schema_version`, tipo, frecuencia objetivo, días ordenados, ejercicios identificados por el catálogo, series, repeticiones, carga opcional, descanso, calentamiento y explicación.

Cada intento registra además `contract_version`, hashes de entrada y salida, versión del modelo y versión de configuración. Un cambio incompatible crea una versión nueva del contrato; nunca se interpreta silenciosamente un JSON viejo como si fuera nuevo.

Reglas de acceso:

- Backend crea solicitudes y candidatos, consulta estados, valida resultados y convierte un candidato confirmado en rutina.
- IA puede leer y reclamar solicitudes pendientes, actualizar su lease, insertar intentos y resultados y cerrar el estado técnico.
- IA no recibe permisos sobre `app.users`, perfiles, rutinas, sesiones ni aprobaciones.
- `minimized_context` no contiene nombre, correo, teléfono, documento, credenciales ni URLs de base.
- La elección Test/Producción ocurre por conexión y credencial del servicio, nunca por un campo enviado por el cliente.

Restricciones principales:

- `UNIQUE (idempotency_key)` por base de datos.
- `UNIQUE (request_id, attempt_number)` y `attempt_number BETWEEN 1 AND 2`.
- `UNIQUE (attempt_id)` en resultados.
- Reclamo mediante `SELECT ... FOR UPDATE SKIP LOCKED` y lease recuperable; un reinicio del worker no pierde el trabajo.
- Sólo un resultado validado favorablemente puede alimentar un candidato visible.
- Fallos, abandonos y respuestas inválidas se purgan a los 30 días; resultados aceptados conservan lo necesario para reproducibilidad y auditoría.

#### 8. Modelo futuro de adaptación y analítica — fuera de esta entrega

No se crearán tablas analíticas en esta entrega. El siguiente modelo queda únicamente como dirección futura y no forma parte de las primeras migraciones:

```mermaid
erDiagram
    STUDENT_PROFILES ||--o{ EVOLUTION_DIAGNOSTICS : receives
    EVOLUTION_DIAGNOSTICS ||--o{ EXERCISE_DIAGNOSTICS : details
    EVOLUTION_DIAGNOSTICS ||--o| ADAPTATION_PROPOSALS : may_generate
    ADAPTATION_PROPOSALS ||--|{ PROPOSED_ADJUSTMENTS : contains
    ADAPTATION_PROPOSALS o|--o| ROUTINE_VERSIONS : may_create
    STUDENT_PROFILES ||--o{ PERSONAL_RECORDS : achieves

    EVOLUTION_DIAGNOSTICS {
        uuid id PK
        uuid student_id FK
        uuid routine_version_id FK
        date period_start
        date period_end
        string global_situation
        decimal adherence
        string component_version
        datetime calculated_at
    }
    EXERCISE_DIAGNOSTICS {
        uuid id PK
        uuid diagnostic_id FK
        uuid exercise_id FK
        string situation
        json metrics
    }
    ADAPTATION_PROPOSALS {
        uuid id PK
        uuid diagnostic_id FK
        uuid student_id FK
        string state
        uuid resolved_by_trainer_id FK
        uuid resulting_version_id FK
        datetime created_at
        datetime resolved_at
    }
    PROPOSED_ADJUSTMENTS {
        uuid id PK
        uuid proposal_id FK
        uuid routine_exercise_id FK
        string type
        json previous_value
        json proposed_value
        string state
    }
    PERSONAL_RECORDS {
        uuid id PK
        uuid student_id FK
        uuid exercise_id FK
        uuid session_id FK
        string type
        decimal value
        date achieved_on
        boolean current
    }
    COMPONENT_EVALUATIONS {
        uuid id PK
        string component
        string version
        string dataset_version
        int sample_size
        json metrics
        json baseline_metrics
        datetime executed_at
    }
```

Las salidas analíticas son append-only: cada cálculo inserta un registro nuevo con versión e instante. El valor vigente es el más reciente; nunca se sobrescribe el pasado.

`risk_scores` no forma parte del modelo porque RF-061 a RF-063 están en estado WON'T. `profile_segments` tampoco se persiste: RF-064 define una descripción generativa efímera. Avisos y auditoría pertenecen al esquema transaccional `app` y están definidos en la sección 6.

#### 9. Orden de migraciones recomendado

1. Esquemas, extensiones necesarias, enums y tablas de referencia.
2. Gimnasio, invitaciones, usuarios, roles, sesiones de autenticación y consentimientos.
3. Perfiles, objetivos, condiciones, aptitudes, mediciones y asignaciones.
4. Inventario, ejercicios y clasificaciones.
5. Plantillas, candidatos, rutinas, versiones y revisiones.
6. Sesiones, registros congelados, comentarios y desbloqueos.
7. Avisos y auditoría transaccional en `app`.
8. Interfaz durable `ai_integration`, asociación de candidatos en `app` y permisos mínimos del rol IA.

Diagnósticos, propuestas, récords e indicadores analíticos quedan para una etapa posterior y no crean el esquema `analytics` en estas migraciones.

Cada paso se crea como una migración Prisma revisada y comprobada sobre PostgreSQL efímero antes de promoverse a Neon Test.

#### 10. Población inicial en Neon Test

El SQL Editor puede utilizarse para cargar datos de referencia y prueba después de que CI haya aplicado las migraciones. No debe utilizarse para crear manualmente tablas que Prisma desconozca.

Orden de carga:

1. `equipment`, `muscle_groups` y `joints`, usando literalmente las enumeraciones de D2.
2. Un gimnasio de prueba y su primer administrador mediante un procedimiento de aprovisionamiento transaccional.
3. Inventario del gimnasio.
4. Catálogo base de ejercicios y sus relaciones de equipamiento, músculos y articulaciones.
5. Usuarios ficticios, asignaciones y perfiles.
6. Plantillas privadas de entrenadores. No se cargan presets en esta entrega.

Todo script de carga debe ser idempotente (`INSERT ... ON CONFLICT ...`) y versionarse en backend. Neon Producción sólo recibe datos de referencia revisados; nunca se copian usuarios ni datos de Test.

#### 11. Decisiones cerradas para la primera entrega

1. Se crean únicamente los esquemas `app` y `ai_integration`; `analytics` queda fuera de esta entrega.
2. Solicitudes e intentos de IA usan los estados técnicos aceptados en la sección 7.
3. Un candidato activo vence después de 24 horas sin actividad y cada operación renueva el plazo.
4. Contexto, preferencias y salida usan contratos JSON versionados, sin datos identificatorios.
5. La autenticación usa sesiones propias; se conservan `auth_sessions` y `password_reset_tokens`.
6. No se crean tablas analíticas en esta entrega.
7. Los presets son opcionales: no se modelan ni migran salvo que el cronograma permita incorporarlos posteriormente.


---

<a id="arch-data-interface"></a>

### Interfaz de datos con el backend

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/data-interface.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-DATA-INTERFACE`

#### Principio

PostgreSQL contiene dos interfaces diferentes para IA: estructuras operativas de generación online y datasets versionados para analítica batch. Backend es dueño de ambas definiciones y de sus migraciones.

#### Generación online

- Backend crea la solicitud idempotente con contexto minimizado.
- El servicio IA reclama trabajos y escribe estados o resultados sólo en estructuras designadas.
- El resultado registra identificador, intento, modelo, configuración, contrato e instante.
- Backend valida y convierte una salida válida en candidato; IA no escribe rutinas ni aprobaciones.
- El rol IA recibe privilegios mínimos y separados para Neon Test y Neon Producción.
- La credencial autenticada ante IA selecciona internamente la conexión; el cliente nunca envía una URL de base.

Las solicitudes abandonadas, respuestas inválidas y fallos se eliminan a los 30 días. Los resultados aceptados conservan contexto mínimo y versiones según la política de auditoría.

#### Analítica batch

Cada job declara:

- nombre y versión del dataset de entrada;
- columnas, tipos, nulabilidad y unidades;
- instante de corte y zona horaria;
- claves de idempotencia;
- tabla o artefacto de salida;
- versión del componente y parámetros.

El motor batch sólo escribe salidas designadas y no actualiza sesiones, rutinas, usuarios ni otras fuentes transaccionales.

#### Desarrollo y pruebas

Backend e IA locales usan Neon Test con roles personales o de servicio restringidos. Nunca se copian datos personales reales al repositorio, fixtures o datasets de regresión. Las pruebas unitarias y de contrato usan datos sintéticos y PostgreSQL efímero en CI cuando necesitan modificar el esquema.

#### Cambios

Un cambio incompatible requiere:

1. nueva versión del contrato;
2. migración o vista preparada por backend;
3. compatibilidad temporal;
4. PR relacionados en backend e IA;
5. fixtures y tests de contrato actualizados;
6. despliegue por etapas antes de retirar la versión anterior.


---

<a id="arch-analytics"></a>

### Arquitectura del repositorio de IA

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/analytics-engine.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-ANALYTICS`

#### Dos límites ejecutables

`proyecto-gimnasio-ia` contiene componentes separados:

1. **Servicio generativo online:** API Python y worker asíncrono desplegados en el Polo.
2. **Analítica batch:** extracción, features, entrenamiento, evaluación y scoring predictivo futuros.

Compartir repositorio no permite que un componente use la frontera del otro ni que el trabajo batch entre en una petición.

#### Servicio generativo

```text
Express/Vercel -> ngrok -> API Python/Polo -> LLM/Polo
                              |
                              v
                         Neon PostgreSQL
```

- Expone HTTP versionado para backend; nunca para frontend.
- Acepta una solicitud idempotente con `202` y la delega a un worker durable.
- Orquesta el LLM mediante un conector privado y valida el esquema de su respuesta.
- Usa únicamente contexto minimizado y estructuras de integración autorizadas.
- Escribe estados y resultados técnicos; no crea, aprueba ni activa rutinas.
- Una única instancia atiende inicialmente test y producción con credenciales y conexiones aisladas.
- No existe modo fake ejecutable; los tests sí pueden usar dobles internos.

#### Analítica batch

- Lee vistas o snapshots versionados acordados con backend.
- Escribe resultados precalculados con versión, instante y explicación.
- No modifica fuentes transaccionales.
- Ejecuta extracción, validación, features point-in-time, entrenamiento, evaluación y persistencia idempotente.
- Si un modelo no supera un criterio simple, se conserva el criterio simple.

#### Operación en el Polo

API, worker, LLM y agente ngrok son procesos distintos. Deben arrancar con la máquina, reiniciarse ante fallos y exponer salud observable. Ngrok publica sólo la API Python mediante un dominio estable; el LLM queda local o privado.

#### Invariantes

- Ningún dato identificatorio innecesario llega al LLM.
- Ninguna salida se publica sin modelo, configuración, instante y contexto mínimo reproducible.
- El rol PostgreSQL de IA no accede a identidad ni modifica entidades de dominio.
- Ninguna feature batch usa información posterior al instante predicho.
- Falta de datos no equivale a cero.
- Los datos simulados se identifican y no se presentan como reales.


---

<a id="arch-generative-integration"></a>

### Integración de IA generativa, ambientes y pruebas

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/generative-ai-integration.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-GENERATIVE-AI`

**Estado:** aceptada · **Fecha:** 2026-08-29 · **Decisión:** [ADR 0009](#adr-0009)

#### Alcance y autoridad

La primera entrega generativa usa un único LLM para interpretar lenguaje natural, proponer el tipo y contenido de una rutina, explicar el criterio y ofrecer alternativas. La predicción de cargas y progreso futuro pertenece al pipeline analítico posterior.

> **Alcance de la Etapa 1** ([baseline](#baseline)). Se construyen `interpretarPedido` (RF-053, banda N2, conservado por compromiso ante el Product Owner pese a obtener 3 votos de 8), `generarRutina` (RF-054, RF-087), `explicarCriterios` (RF-055) y `sugerirAlternativas` (RF-059, que absorbe la exclusión dura de RF-060). Quedan diferidos `resumirProgreso` (RF-056) y, en banda N3, `describirPerfil` (RF-064).
>
> **Y una consecuencia que cambia el peso de este componente:** al diferirse los presets (RF-021) y no existir un generador determinístico, `generarRutina` **es la única vía automática de prescripción del sistema**. Su indisponibilidad no degrada una funcionalidad accesoria: deja al producto sin forma de dar un plan a un alumno nuevo, salvo que un entrenador arme una plantilla a mano. Ver [D11/DD-35](#d11) y D12/R-17.

El LLM siempre produce una salida candidata. El backend conserva autorización y reglas de negocio: minimiza el contexto, controla catálogo, compatibilidad, rangos y permisos, y convierte una salida válida en candidato. Un entrenador debe aprobar toda rutina antes de que llegue al alumno. El modelo no activa rutinas ni emite consejo médico.

#### Topología

```text
React/Vercel -> Express/Vercel -> ngrok -> API Python/Polo -> LLM/Polo
                       |                     |
                       +---- Neon -----------+
```

- Ngrok expone sólo la API Python; el LLM permanece local o privado en el Polo.
- La API Python acepta trabajos con `202`; un worker los procesa fuera de la petición.
- El servicio Python persiste estados y resultados en estructuras de integración. El LLM no conoce PostgreSQL.
- El frontend consulta estado exclusivamente al backend.
- Backend e IA se despliegan de manera independiente mediante contratos versionados.

#### Flujo de generación

1. El solicitante confirma parámetros estructurados.
2. Backend crea una solicitud idempotente con contexto anonimizado.
3. El servicio IA acepta la solicitud y el worker llama al LLM.
4. Cada intento tiene un límite configurable inicial de 120 segundos.
5. Una respuesta inválida o un fallo técnico admite un único reintento.
6. IA registra resultado, modelo, configuración, contrato e instante.
7. Backend valida la salida y, si es válida, presenta el candidato.
8. Al confirmarse, la rutina queda PROPUESTA y pasa al entrenador.

Tras el segundo fallo, la generación queda temporalmente no disponible. No hay generador determinístico alternativo ni adaptador `fake` ejecutable. El resto del sistema, las plantillas privadas y la creación manual por entrenadores permanecen operativos. Los presets sólo existirán si alcanza el tiempo para implementar RF-021.

#### Datos y aislamiento

El contexto enviado excluye datos identificatorios que no aportan a la rutina. El Polo recibe un identificador técnico, objetivo, nivel, frecuencia, condiciones pertinentes, equipamiento, catálogo permitido y preferencias. Ningún log guarda prompts completos, credenciales ni datos de salud.

El servicio IA sólo puede leer y escribir las estructuras de integración acordadas. No accede a tablas de identidad ni modifica rutinas, sesiones o aprobaciones. Backend es el único que transforma un resultado en entidad de dominio.

Una única API y configuración del modelo atienden inicialmente ambos ambientes. La credencial de consumo determina en el servidor si se usa Neon Test o Neon Producción. Las conexiones, roles y secretos son distintos y nunca se eligen mediante datos enviados por el cliente.

#### Trabajo local y ambientes

| Recurso | Local | Test (`test`) | Producción (`main`) |
| --- | --- | --- | --- |
| Frontend | Vite | Vercel Preview estable | Vercel Production |
| Backend | Express, conectado a Neon Test | Vercel + Neon Test | Vercel + Neon Producción |
| IA online | Python local opcional o servicio compartido del Polo | API y worker en el Polo | misma API/worker, credencial aislada |
| LLM | API del Polo cuando sea accesible | LLM del Polo | mismo LLM/configuración inicial |
| Analítica futura | jobs manuales sobre datos sintéticos/test | jobs batch | jobs batch |

El desarrollo ordinario no levanta PostgreSQL local: frontend y backend locales usan Neon Test. No se permiten resets, seeds destructivos ni migraciones automáticas sobre la base compartida. La creación segura de migraciones requiere resolver la estrategia declarada en [Base de datos de desarrollo](#ops-local-db).

Los tests unitarios y de contrato sustituyen el transporte HTTP o el conector LLM dentro del proceso de prueba; eso no constituye un modo fake de la aplicación. Las integraciones reales se ejecutan al promover a `test` y cuando cambia modelo, prompt o parámetros.

#### Promoción

```text
feature/* -> PR -> develop -> PR -> test -> PR -> main
```

- Todo PR ejecuta formato, tipos, unitarias y contratos, con aprobación de otra persona.
- `test` despliega Neon Test, Vercel y la versión test del servicio IA; allí se ejecutan integración, evaluación y E2E.
- `main` exige aprobación del dueño, checks verdes y smoke test posterior.
- Un cambio de modelo, prompt o parámetros necesita además una evaluación comparativa y validación de al menos un entrenador.
- Los cambios incompatibles backend–IA se despliegan por etapas y conservan compatibilidad temporal.

#### Estrategia de pruebas

| Nivel | Qué verifica | Cuándo |
| --- | --- | --- |
| Unidad | reglas, permisos, minimización, parser y máquina de estados | cada PR |
| Contrato | OpenAPI backend–IA, idempotencia y compatibilidad | cada PR |
| Persistencia | permisos del rol IA, reclamo durable y aislamiento de ambientes | cada PR/promoción |
| Integración | ngrok, timeout, reintento, caída del LLM y recuperación del worker | en `test` |
| Evaluación | catálogo, compatibilidad, rangos, números respaldados y lenguaje médico | cambios de IA |
| E2E | solicitud, polling, candidato, revisión, aprobación e indisponibilidad generativa | antes de `main` |

El dataset fijo cubre contexto incompleto, condiciones físicas, equipamiento ausente, prompt injection, respuestas mal formadas, timeout y caída del servicio. No se compara texto exacto: se verifican invariantes y una rúbrica humana. Las métricas incluyen latencia, reintentos, salida inválida, indisponibilidad, rechazo del entrenador y magnitud de edición.

#### Operación mínima

API Python, worker, LLM y agente ngrok deben arrancar con la máquina, reiniciarse ante fallos y exponer salud observable. El dominio ngrok debe ser estable. Si API, worker, túnel o LLM fallan, la generación se declara no disponible sin degradar el resto del sistema.


---

<a id="arch-generative"></a>

### IA generativa — LLM autohospedado

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/generative-ai.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-GENERATIVE-AI-SCOPE`

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto, pendiente de verificación de hardware    |
| **Depende de** | [D2](#d2), [D5](#d5), [D8](#d8), [D9](#d9), [D11/DD-14, DD-15, DD-31, DD-34](#d11), [system-overview.md](#arch-system) |

#### 1. Qué resuelve y qué no resuelve

La capa generativa cubre exclusivamente **componentes narrativos y de interpretación de lenguaje**, nunca prescripción (D11/DD-14):

| Requerimiento | Función | Tipo de componente |
| --- | --- | --- |
| RF-053 | Traducir una descripción en lenguaje natural a parámetros estructurados, presentados para confirmación antes de usarse | Interpretación |
| RF-054 | Construir la rutina a partir de esos parámetros y el contexto del alumno, sobre el catálogo prescribible del gimnasio | HYBRID: el LLM redacta la estructura candidata, pero **RN-39a, RN-44a-d y D5/§6 la validan de forma determinística antes de mostrarla** (RF-113) |
| RF-055 | Justificar en lenguaje natural los criterios aplicados a una rutina generada | Narrativo |
| RF-056 | Resumir la evolución de un alumno en un período, exclusivamente sobre indicadores ya calculados | Narrativo |
| RF-059 / RF-060 | Ordenar las alternativas de sustitución de un ejercicio (ejercicios parecidos) sobre el subconjunto del catálogo prescribible ya prefiltrado de forma determinista por patrón y compatibilidad | Selección sobre catálogo prefiltrado, con revalidación determinista posterior (RF-113) |
| RF-064 | Describir en lenguaje natural el perfil de comportamiento de un alumno a partir de sus indicadores ya calculados (frecuencia, volumen, intensidad relativos) y su objetivo — **efímero, no se persiste** | Narrativo sobre indicadores ya calculados |
| RF-075 / RF-108 | Redactar la pauta nutricional orientativa (energía y proteína por comida, sin nombrar alimentos) | Narrativo sobre valores ya calculados |

**Lo que el LLM nunca hace:** calcular compatibilidad, decidir qué ejercicios entran en una rutina más allá de proponer una estructura candidata sujeta a validación, incluir en una sustitución un ejercicio fuera del subconjunto prefiltrado que recibe como entrada, calcular indicadores, aprobar una rutina, ni emitir indicaciones médicas (RF-057). RN-44a-d, RN-39a, RN-79a y RN-89a son código determinista, no prompts. Ver [D11/DD-31 y DD-34](#d11).

#### 2. Dónde corre

El runtime de inferencia corre en un servidor administrado por el Polo Educativo de la Universidad, autohospedado, sin salir a un proveedor externo (ver [ADR-0004](#adr-0004)).

**Hardware disponible: `NO VERIFICADO`.** No hay documentación de CPU, GPU, VRAM, RAM ni almacenamiento del servidor institucional en ningún repositorio del proyecto. La arquitectura se diseña para no depender de un tamaño de modelo fijo, exactamente por esta razón: el modelo y su cuantización son **configuración** (variable de entorno leída por el runtime), no una decisión hardcodeada en el backend.

Dos perfiles de despliegue, a confirmar contra el hardware real antes de congelar el tamaño de modelo:

| Perfil | Hardware asumido | Modelo/cuantización | Riesgo |
| --- | --- | --- | --- |
| **A — con GPU** | GPU única, 8-16 GB VRAM `[S]` supuesto de trabajo | Qwen2.5-7B-Instruct o Qwen2.5-14B-Instruct, cuantización Q4_K_M/Q5_K_M (GGUF) o AWQ | Bajo: el presupuesto de 20 s de RNF-04 se cumple con margen |
| **B — solo CPU** | Sin GPU dedicada, RAM ≥ 16 GB `[S]` supuesto de trabajo | Qwen2.5-7B-Instruct, cuantización Q4_K_M | **Alto**: la latencia por token en CPU puede acercarse o superar el presupuesto de RNF-04 para rutinas largas, lo que empujaría el sistema a la vía determinística (RF-113) con más frecuencia de la prevista. Si se confirma este perfil, evaluar un modelo menor (Qwen2.5-3B) o degradar RF-053/RF-055 según el orden de recorte de [D12/§4, ítem 16](#d12) |

Selección de modelo y runtime justificada en [ai-model-selection.md](#arch-model-selection) y [ADR-0006](#adr-0006).

#### 3. Componentes y comunicación

Dos capas separadas, que no deben confundirse (ver §5 de la tarea de origen: modelo ≠ runtime):

```text
Backend (Express, monolito modular)
   |
   |  llamada de función in-process
   v
AI Gateway  ── módulo interno, puerto + adaptador ──
   |             (src/modules/ai-gateway en el backend)
   |  HTTP interno, red privada del servidor institucional
   v
LLM Server  ── runtime de inferencia (Ollama) sirviendo el modelo elegido ──
```

- **AI Gateway** vive **dentro del backend**, como un módulo más del monolito modular (no un servicio desplegado aparte). Expone un puerto (`GenerativeAiPort`) con un método por capacidad (`interpretarSolicitud`, `generarRutina`, `justificarRutina`, `resumirEvolucion`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil`) y una única implementación (`OllamaAdapter`) que habla el protocolo HTTP compatible con OpenAI que expone Ollama.
- **LLM Server** es el proceso de Ollama corriendo en el servidor del Polo, sirviendo el modelo configurado. No expone ningún endpoint de negocio: sólo inferencia de texto.
- El backend **nunca** ejecuta el motor Python de IA predictiva ni el runtime del LLM dentro del proceso de una petición HTTP entrante del frontend; sólo hace una llamada saliente al LLM Server y espera su respuesta dentro del presupuesto de RNF-04.

Por qué el Gateway es un puerto con adaptador reemplazable y no lógica dispersa por cada punto de llamada: ver [ADR-0005](#adr-0005). Su **ubicación de despliegue** quedó reemplazada por [ADR-0009](#adr-0009): el Gateway vive dentro del servicio Python del Polo, no dentro del monolito del backend.

#### 4. Flujo generativo (mapea FL-04)

```text
Alumno/Entrenador
   │  1. describe en lenguaje natural, o completa formulario
   ▼
Backend (router de rutinas)
   │  2. AI Gateway.interpretarSolicitud(texto)
   ▼
AI Gateway ──prompt versionado + schema──▶ LLM Server
   │  3. respuesta JSON candidata
   ▼
AI Gateway  4. valida contra JSON Schema; si falla, reintenta 1 vez (RF-113)
   │
   ▼
Backend  5. presenta parámetros para CONFIRMACIÓN del usuario (RF-053, paso 2 de FL-04)
   │
   ▼
Backend  6. AI Gateway.generarRutina(parámetros, contexto del alumno)
   │
   ▼
AI Gateway ──prompt + catálogo prescribible + contexto──▶ LLM Server
   │  7. estructura candidata de rutina (JSON)
   ▼
Backend  8. VALIDACIÓN DETERMINÍSTICA: RN-39a, RN-44a-d, D5/§6 (código, no LLM)
   │
   ├─ inválida → 1 reintento del paso 6 → si vuelve a fallar, vía determinística (RN-95b)
   │
   ▼
Backend  9. AI Gateway.justificarRutina(estructura validada) → texto (RF-055)
   │
   ▼
Frontend  10. candidato (RN-124): estructura + estado de compatibilidad + justificación
```

Cada llamada a `AI Gateway` se resuelve con timeout, y si el LLM Server no responde o el resultado no valida tras el reintento, el flujo continúa por la alternativa determinística (RF-058, RF-113, RN-99): entrada por formulario estructurado, justificación tabulada, generación por reglas simples. **Nunca se presenta un error al usuario por esta causa** (RNF-11).

#### 5. Contrato interno del AI Gateway

Cada método del puerto recibe y devuelve una estructura tipada; el backend nunca pasa texto libre del LLM directamente a una vista o a persistencia sin haber pasado por validación de schema.

##### 5.1 `interpretarSolicitud` (RF-053)

Entrada: texto libre del usuario, contexto mínimo (gimnasio, alumno).

Salida (JSON Schema, ejemplo):

```json
{
  "objetivo": "HIPERTROFIA",
  "frecuencia_semanal": 4,
  "restricciones": ["evitar sentadilla con barra"],
  "duracion_sesion_minutos": 60,
  "confianza": 0.86
}
```

`objetivo` restringido a la enumeración de [D2 §4.5](#d2); `frecuencia_semanal` restringido al rango de RN-38 (1-7). Un valor fuera de la enumeración es un fallo de validación, no un dato a persistir.

##### 5.2 `generarRutina` (RF-054)

Entrada: parámetros confirmados + contexto del alumno ([D2 §1.9](#d2): perfil, nivel, objetivo vigente, condiciones vigentes, aptitud, inventario del gimnasio, catálogo prescribible).

Salida: estructura completa de días → ejercicios → series prescriptas, usando exclusivamente identificadores del catálogo prescribible recibido como entrada (nunca nombres inventados). Se valida contra RN-39a y D5/§6 en código antes de mostrarse.

##### 5.3 `justificarRutina` / `resumirEvolucion` / `generarPautaNutricional` (RF-055, RF-056, RF-075/108)

Entrada: la estructura o los indicadores ya calculados (nunca datos crudos que el modelo deba resumir por su cuenta).

Salida:

```json
{
  "texto": "string",
  "valores_citados": [12.5, 4, "HIPERTROFIA"],
  "version_prompt": "generative/justificar-rutina@3",
  "version_modelo": "qwen2.5-7b-instruct-q4_k_m"
}
```

`valores_citados` es la lista de valores numéricos/categóricos que el texto menciona; el backend verifica que cada uno provenga literalmente de la entrada (RNF-24, RF-057) antes de mostrar el texto. Un valor no verificable descarta la respuesta y dispara el reintento/fallback.

##### 5.4 `sugerirAlternativas` (RF-059, RF-060)

Entrada: el ejercicio a sustituir, el contexto del alumno y **la lista de ejercicios candidatos ya prefiltrada de forma determinista** por el backend (mismo código de RN-44a-d y RN-45: mismo patrón de movimiento dominante, estado COMPATIBLE para ese alumno, equipamiento presente en el inventario). El LLM nunca recibe el catálogo completo ni ids fuera de esa lista.

Salida (JSON Schema): lista ordenada de hasta 5 ids, **todos pertenecientes a la lista de entrada**, con un motivo breve por ítem. El backend descarta cualquier id que no esté en la entrada y revalida el estado de compatibilidad de cada uno (RF-113) antes de mostrarlo. Si el LLM no responde o la salida no valida tras el reintento, se usa el orden determinista de RN-49a (coincidencia de participación muscular primaria y luego secundaria) sobre la misma lista prefiltrada.

La lista devuelta se persiste junto con `version_modelo` y `version_prompt` (RF-072); no se recalcula al reproducir un resultado pasado (ver §15 y el encuadre de RNF-27 en [DD-34](#d11)).

##### 5.5 `describirPerfil` (RF-064)

Entrada: los indicadores de comportamiento ya calculados del alumno (frecuencia, volumen e intensidad relativos) y su objetivo vigente.

Salida: una etiqueta corta y un texto legible ("alta frecuencia, bajo volumen", en vez de un identificador de clúster). Se aplican las mismas restricciones de `valores_citados` de §5.3: el texto no introduce ninguna cifra ausente de la entrada. **El resultado es efímero** — se genera al abrir la vista del entrenador o del administrador y no se persiste. No hay clustering ni un modelo poblacional detrás.

#### 6. Prompting

Separación estricta de secciones dentro de cada prompt, versionadas de forma independiente (`generative/<capacidad>@<versión>`):

1. **System prompt** — rol, restricciones permanentes ("nunca inventes valores numéricos ausentes de la entrada", "nunca emitas indicaciones médicas", "responde únicamente en el JSON Schema dado"). Fijo por capacidad, cambia poco.
2. **Schema de salida** — el JSON Schema exacto que se va a validar, incluido literalmente en el prompt para modelos sin API nativa de structured output, u ofrecido como `response_format`/`format` cuando el runtime lo soporta (Ollama lo soporta desde su API de generación estructurada).
3. **Contexto dinámico** — el contexto del alumno o los indicadores ya calculados, siempre como JSON serializado, nunca como prosa que el modelo deba reinterpretar.
4. **Instrucción de la tarea** — la petición concreta ("generá la justificación de esta rutina").
5. **Restricciones de negocio que NO van en el prompt**: la enumeración cerrada de equipamiento, patrones de movimiento y objetivos ([D2 §4](#d2)) se valida en código después de la respuesta, no se le pide "por favor" al modelo que la respete — el modelo puede proponer, el código dispone (RN-95b, RF-113).

Las plantillas de prompt viven versionadas en el repositorio del backend (no en el LLM Server), como archivos de texto bajo control de versión, con su propio changelog. Un cambio de prompt es un cambio de código: pasa por PR y por los casos de prueba de §10.

#### 7. Tool calling: herramientas invocables desde el LLM

RF-054 y RF-119 necesitan que, mientras arma el candidato de rutina (FL-04), el modelo pueda pedir alternativas de sustitución para un ejercicio puntual (RF-059, A4 de FL-04). Tras el replanteo de IA del 2026-08-28 ([DD-34](#d11)), ese orden **lo produce la propia capa generativa** (`sugerirAlternativas`, §5.4) sobre el subconjunto del catálogo ya prefiltrado de forma determinista — ya no hay un modelo clásico de ranking. Lo que **sí** se mantiene como herramienta determinista es la verificación de compatibilidad. Fundamento en [ADR-0008 (revisada)](#adr-0008).

**Herramientas expuestas por el AI Gateway al modelo:**

| Herramienta | Envuelve | Devuelve |
| --- | --- | --- |
| `verificarCompatibilidad(estructura_candidata, alumno_context)` | RN-44a-d (código determinista) | Estado de compatibilidad por ejercicio — el mismo cálculo que corre igual como validación posterior (§5, RF-113); exponerlo como herramienta le permite al modelo autocorregirse antes de terminar, no reemplaza la validación final |

El ordenamiento de alternativas de sustitución **no se expone como herramienta**: el modelo que ya está orquestando FL-04 recibe el subconjunto prefiltrado como parte del contexto y produce el orden inline, o el backend llama a `sugerirAlternativas` directamente (A4 de FL-04, FL-06). En ambos casos la salida sólo puede contener ids del subconjunto de entrada y se revalida por RN-44a-d antes de mostrarse (RF-113).

**Por qué el LLM ordena las alternativas pero no "razona sobre el catálogo entero".** El LLM recibe únicamente el subconjunto ya filtrado por patrón de movimiento, compatibilidad y equipamiento (mismo código que RN-44a-d y RN-45); no ve el catálogo completo ni puede inventar ids. La exclusión dura de lo contraindicado y la verificación final siguen siendo deterministas y son la barrera real (RF-113, RN-95b). Lo que se acepta a cambio: el orden de las alternativas ya no es exactamente reproducible entre corridas, sino "válido de forma repetida" — el mismo estándar de §10 para el resto de la capa generativa; la lista producida se persiste para RF-072 (ver el encuadre de RNF-27 en [DD-34](#d11)).

**Requisito sobre el modelo/runtime elegido**: esto es la razón por la que el soporte de tool calling en [ai-model-selection.md §1](#arch-model-selection) dejó de ser un "nice to have" y pasa a ser un requisito de peso — Qwen2.5 y Ollama lo soportan de forma madura, lo que valida la elección hecha en [ADR-0006](#adr-0006) también por este motivo, no sólo por licencia y calidad en español.

#### 8. RAG — no se usa (retrieval semántico), pero sí prefiltrado determinista

Ver justificación completa y el umbral de reapertura en [ADR-0007](#adr-0007). Resumen actualizado, con la parte de tamaño explícita:

- Las 12 enumeraciones cerradas de [D2 §4](#d2) entran completas en el prompt: son chicas y fijas, no necesitan recuperación.
- El **catálogo prescribible de un gimnasio no siempre es chico** (puede tener decenas a un par de cientos de ejercicios) y no se vuelca completo al prompt en cada llamada. El backend lo **prefiltra de forma determinista** — mismo código que ya exige RN-44a-d y RN-45 para la validación — por patrón de movimiento pedido, compatibilidad con el alumno y equipamiento del inventario, **antes** de construir el prompt. Sólo ese subconjunto ya válido entra al contexto, típicamente acotado a decenas de ejercicios por llamada, no al catálogo entero.
- Esto no es RAG semántico porque la necesidad no es de similitud aproximada: es un filtro **exacto** sobre atributos estructurados (RN-44a-d es una regla dura, no una preferencia difusa). Un vector store resolvería esto de forma aproximada, que es peor para una condición que tiene que ser exacta (RN-46: una incompatibilidad impide poner la rutina en vigencia).
- El resto del contexto del alumno (perfil, condiciones, indicadores) se arma con una consulta directa a PostgreSQL, acotada por alumno — no hay un corpus grande, no estructurado y cambiante (políticas, FAQ, documentación interna) que el LLM deba buscar semánticamente.

**Umbral de reapertura explícito**: si el catálogo prescribible filtrado de un gimnasio (ya acotado por patrón y compatibilidad, no el catálogo completo) empezara a superar un tamaño que ya no entra cómodo en el presupuesto de contexto del modelo elegido — algo que no se espera con equipamiento típico de gimnasio, dado el techo de 22 valores de equipamiento y 9 patrones de movimiento de [D2 §4](#d2) — ahí sí corresponde reabrir esta decisión y evaluar RAG semántico o paginación. No antes.

#### 9. Guardrails

| Riesgo | Mitigación |
| --- | --- |
| Alucinación de valores numéricos en texto narrativo | Verificación de `valores_citados` contra la entrada (RNF-24); descarte automático si no coincide |
| Alternativa de sustitución con un id inventado o fuera del subconjunto prefiltrado | El backend descarta todo id que no esté en la lista de entrada y revalida compatibilidad (RF-113); si no queda ninguno válido, se aplica el orden determinista de RN-49a |
| Salida fuera del schema | Validación de JSON Schema; 1 reintento; luego vía determinística (RF-113) |
| Indicación médica | Prohibición explícita en el system prompt + filtro de patrones (palabras clave clínicas) sobre la salida antes de mostrarla; RF-057 lo exige como requisito, no como buena práctica |
| Inyección de instrucciones en el texto libre del usuario ("ignorá las reglas anteriores y...") | El contexto dinámico y la instrucción de tarea van en secciones separadas y delimitadas del prompt; ninguna instrucción de negocio depende de que el modelo la respete — la validación determinística (RN-39a, RN-44a-d) es la barrera real, no el prompt |
| Uso indebido de datos del alumno | Ver §11 — el AI Gateway decide qué campos del contexto se serializan hacia el prompt; un campo nuevo en el modelo de datos no llega al LLM automáticamente |
| Mensaje comercial/narrativo incorrecto que llega al alumno | El sistema decide si el texto se envía: la salida del LLM es siempre una propuesta que pasa por la validación de §9 antes de presentarse; ninguna redacción se entrega directo desde el modelo |

#### 10. Evaluación de la IA generativa

Conjunto de casos de prueba representativo, fijo y versionado junto con los prompts (no exhaustivo, pero cubre los siete métodos del Gateway):

| Caso | Verifica |
| --- | --- |
| Interpretación con objetivo ambiguo ("quiero ponerme fuerte") | Mapea a un valor válido de la enumeración o pide aclaración, nunca inventa un valor fuera de ella |
| Interpretación con restricción de equipamiento mencionada en el texto | El equipamiento no se toma como parámetro (sale del inventario, RF-053) — el Gateway lo descarta si el modelo lo intenta incluir |
| Generación con inventario mínimo (sólo `PESO_CORPORAL`) | La estructura resultante no referencia equipamiento ausente; si no cubre los patrones mínimos, lo declara (E3 de FL-04) |
| Justificación sobre una rutina con un ajuste de `SUSTITUCION` | El texto no inventa una carga o repetición ausente del ajuste de entrada |
| Resumen de evolución con `DATOS_INSUFICIENTES` | El texto declara la insuficiencia, no la disimula con una afirmación genérica |
| Pauta nutricional sin datos suficientes | El Gateway no genera texto (RF-108) |
| Sugerencia de alternativas con un candidato contraindicado en la lista de entrada | La salida no lo incluye; ningún id fuera de la lista prefiltrada aparece en el resultado |
| Sugerencia de alternativas con el LLM no disponible | Se devuelve el orden determinista de RN-49a sobre la misma lista, sin error visible |
| Descripción de perfil con indicadores dados | El texto no introduce ninguna cifra ausente de la entrada; no se persiste |

Métricas sobre este conjunto y sobre una muestra ampliada (alineado con RNF-24/RNF-25):

- **Corrección factual**: tasa de `valores_citados` no verificables — objetivo 0% (RNF-24, sobre 50 textos por tipo).
- **Formato**: tasa de respuestas que no validan contra el JSON Schema en el primer intento.
- **Adherencia a instrucciones**: tasa de rutinas generadas que requieren el reintento de RF-113.
- **Latencia**: percentil 95 de cada método, contra el presupuesto de RNF-04 (20 s incluida validación).
- **Tasa de error/timeout**: proporción de llamadas que terminan en la vía determinística por indisponibilidad o timeout del LLM Server.
- **Consistencia**: misma entrada, incluida la temperatura configurada, produce estructuras dentro del mismo rango de validación en ejecuciones repetidas (no se exige determinismo exacto, se exige validez repetida).

No se usa únicamente evaluación subjetiva: las primeras cuatro métricas son automáticas y se ejecutan en CI sobre el conjunto de casos fijo antes de cambiar un prompt o un modelo.

#### 11. Privacidad y seguridad específicas del LLM

**Qué llega al prompt:** objetivo, nivel, condiciones físicas por zona/severidad (sin descripción libre — RN-10a ya excluye la descripción libre de todo cálculo, y por la misma razón no se serializa al prompt), inventario del gimnasio, catálogo prescribible, indicadores agregados ya calculados (volumen, adherencia, e1RM). Ningún dato de contacto, credencial ni identificador más allá del necesario para trazabilidad interna (id de contexto, no nombre ni correo).

**Qué nunca llega al prompt:** contraseñas, tokens de sesión, correo electrónico, teléfono, descripción libre de una condición física, historial de otro alumno, dato de un gimnasio distinto al del alumno en contexto.

**Qué se registra:** versión de prompt, versión de modelo, hash del contexto de entrada (no el contexto completo en texto plano en logs de aplicación de larga retención), latencia, resultado de validación. **Nunca** se registra el texto de una condición física ni el contenido completo del prompt en un log persistente de nivel INFO — esto es RNF-19 aplicado a la capa generativa, no una elección adicional. Un registro de auditoría completo (para depuración de una respuesta puntual) puede existir con retención corta y acceso restringido a quien opere el LLM Server, nunca en logs de acceso general.

**Ventaja de ser autohospedado**: ningún dato de alumnos (condición física, historial) sale de la infraestructura de la Universidad hacia un tercero. **Riesgo nuevo que introduce**: la Universidad pasa a ser responsable de operar, parchear y asegurar un servicio con datos potencialmente sensibles — sin esto, el riesgo estaba tercerizado a un proveedor con su propio cumplimiento; con esto, el equipo del proyecto y el Polo Educativo lo asumen directamente. Debe documentarse como parte del acuerdo operativo con la institución.

#### 12. Seguridad del servidor LLM

- El LLM Server **no se expone a Internet**. Sólo es alcanzable desde la red interna donde corre el backend (o mediante VPN/túnel si el backend no corre en la misma red del Polo). No hay razón declarada en este proyecto para exponerlo públicamente.
- Autenticación entre el AI Gateway y el LLM Server mediante un token compartido en variable de entorno (no en código), rotable sin redeploy del backend.
- TLS si el tráfico atraviesa un segmento de red no confiable; en red interna aislada, evaluado según lo que el Polo Educativo provea — `NO VERIFICADO`.
- Límite de recursos del proceso de inferencia (memoria, concurrencia máxima) configurado en el runtime, para que una petición no degrade el resto del servidor si es compartido con otros servicios del Polo.
- Rate limiting por usuario y por período en el backend, antes de llegar al Gateway (RNF-18) — protege al LLM Server de un solo usuario agotando la capacidad.
- Actualizaciones del runtime y del modelo son un cambio de versión documentado (§16), nunca un reemplazo silencioso.

#### 13. Fallback

> ⚠️ **v4.0 del alcance.** Donde este documento dice «presets publicados del gimnasio», léase **«plantillas del entrenador» (RF-019)**: RF-021 quedó diferido en la Etapa 1 y con él la publicación de presets. El objeto subyacente es el mismo —una plantilla de rutina—; lo que no existe es compartirla dentro del gimnasio. **El fallback deja de ser automático: requiere que exista al menos una plantilla cargada y que un entrenador la asigne.** Ver [DD-35](#d11), RN-95b y D12/R-17.

| Falla | Comportamiento |
| --- | --- |
| LLM no responde / timeout | Vía determinística: formulario estructurado en vez de NL, generación por reglas simples si corresponde, justificación tabulada (RF-058, A1 de FL-04) |
| LLM no responde al pedir alternativas de sustitución (FL-04/A4, FL-06) | Orden determinista de RN-49a sobre el subconjunto ya prefiltrado (coincidencia de participación muscular primaria y luego secundaria); el flujo de sustitución no se interrumpe (RN-99) |
| LLM no responde al pedir la descripción de perfil (RF-064) | La vista muestra los indicadores numéricos sin el texto descriptivo; nada más se degrada |
| Salida inválida (no pasa el JSON Schema o la validación de negocio) | 1 reintento; si vuelve a fallar, vía determinística (RF-113, E1 de FL-04). Nunca se presenta una propuesta inválida ni un error |
| GPU/recursos agotados en el LLM Server | El timeout de la llamada lo captura igual que una indisponibilidad; mismo camino que la fila anterior |
| Servicio completo fuera de línea | El resto del sistema sigue operando: registro de sesiones, revisión de rutinas, consulta de indicadores — nada de esto depende del LLM (RNF-11, RNF-12) |

#### 14. Observabilidad

Métricas por método del Gateway (`interpretarSolicitud`, `generarRutina`, `justificarRutina`, `resumirEvolucion`, `generarPautaNutricional`, `sugerirAlternativas`, `describirPerfil`):

- latencia (p50/p95/p99);
- tokens de entrada y salida;
- throughput (llamadas/minuto);
- tasa de error y de timeout;
- tasa de reintento (RF-113);
- tasa de fallback a vía determinística;
- versión de modelo y de prompt activas.

Nunca se registra información sensible del alumno en estas métricas (RNF-19) — son agregados numéricos y etiquetas de versión, no contenido.

#### 15. Versionado

- **Modelo**: identificador completo (`qwen2.5-7b-instruct-q4_k_m`) fijado en configuración del AI Gateway, no en el LLM Server únicamente — el backend registra qué versión produjo cada resultado (RF-072).
- **Prompt**: `generative/<capacidad>@<n>`, incrementado en cada cambio de contenido, con changelog en el propio archivo de plantilla.
- **Schema de salida**: versionado junto al prompt que lo referencia; un cambio de schema es incompatible por definición y requiere versión nueva de ambos.
- Cada resultado narrativo persistido conserva `version_modelo` y `version_prompt` (§5.3), cumpliendo RF-072 también para narrativos, aunque no sean "componentes de decisión" en el sentido de DD-14.
- La lista de alternativas de sustitución que se incorpora a un candidato de rutina se persiste con `version_modelo` y `version_prompt` (§5.4). Como el orden generativo no es exactamente reproducible, RF-072/RNF-27 se cumplen guardando la salida, no reejecutándola (ver [DD-34](#d11)). La descripción de perfil (§5.5) es efímera y no se persiste.

#### 16. Reemplazo del modelo en el futuro

Cambiar de Qwen a Llama, a otro modelo, o subir de tamaño no requiere tocar el backend fuera del AI Gateway:

1. El nuevo modelo se publica en el LLM Server (`ollama pull <modelo>`) y se valida con el conjunto de casos de §10.
2. Se compara contra el modelo vigente con las mismas métricas (RF-073 aplicado también acá: el modelo nuevo debe igualar o superar al vigente en el conjunto de prueba antes de promoverse).
3. Se cambia la variable de configuración del AI Gateway. El `GenerativeAiPort` no cambia; sólo cambia qué modelo atiende el `OllamaAdapter`.
4. Si el nuevo modelo requiere un runtime distinto (por ejemplo, vLLM por necesidad de concurrencia), se agrega un adaptador nuevo (`VllmAdapter`) que implementa el mismo puerto — el backend no distingue entre ellos.

#### 17. Costos y capacidad

Autohospedado no es costo cero:

- **Electricidad y amortización de hardware**: a cargo del Polo Educativo, fuera del presupuesto del proyecto — `NO VERIFICADO` si existe un límite o cuota asignada al equipo.
- **Administración**: alguien del equipo o del Polo debe mantener el runtime actualizado y monitorear el proceso — no está presupuestado en las 504 h de capacidad de construcción de [D12/§3](#d12); es trabajo adicional a declarar, no a absorber en silencio.
- **Estimación de carga** (de trabajo, no verificada contra uso real): generación de rutina es un evento poco frecuente por alumno (al incorporarse, al pedir una nueva, no en cada sesión). Con 5.000 alumnos (techo de RNF-36) y una tasa optimista de una generación por alumno por semana, son ~715 llamadas/día a `generarRutina`, muy por debajo del umbral de ~5 usuarios concurrentes donde Ollama empieza a degradarse (ver [ai-model-selection.md](#arch-model-selection)). El resumen narrado (RF-056) y la justificación (RF-055) tienen una frecuencia similar o menor. **Esta estimación es de diseño, no una medición — debe revisarse cuando haya uso real.**
- Con esta carga esperada, una sola GPU modesta (o incluso CPU con el riesgo de latencia ya señalado en §2) alcanza. No hay evidencia de que se necesite más de una instancia del LLM Server.


---

<a id="arch-model-selection"></a>

### Selección de modelo y runtime para la IA generativa

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/ai-model-selection.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-AI-MODEL-SELECTION`

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto, sujeto a revalidación cuando el hardware del servidor institucional esté verificado |
| **Depende de** | [generative-ai.md](#arch-generative), [ADR-0006](#adr-0006) |

Este documento separa dos decisiones distintas que suelen confundirse: **qué modelo** correr y **qué runtime** usar para servirlo. Cambiar una no obliga a cambiar la otra.

#### 1. Modelo

No se asumió de antemano que Llama o Qwen fueran la mejor opción. Se evaluaron cuatro familias con pesos abiertos, self-hostable, en el rango de tamaño realista para un servidor institucional de uso compartido (7B-14B parámetros, cuantizado).

| Familia | Licencia | Español / multilingüe | Tool calling / structured output | Ecosistema | Riesgo específico |
| --- | --- | --- | --- | --- | --- |
| **Qwen2.5 / Qwen3 (7B-14B)** | Apache 2.0 en los tamaños ≤32B, sin tope de uso | Mejor que Llama 3.1 en benchmarks multilingües/no-inglés a tamaño equivalente | Maduro, bien documentado | Amplio soporte GGUF/Ollama/vLLM | Ninguno relevante encontrado |
| **Llama 3.1 / 3.3 (8B)** | Licencia propia Meta: tope de 700M usuarios activos mensuales (no aplica a este proyecto), exige atribución "Built with Llama" | Soporta español, algo por detrás de Qwen en benchmarks no-inglés al mismo tamaño | Maduro | El más amplio de los cuatro: mayor cantidad de tutoriales, fine-tunes e integraciones | Licencia menos permisiva que Apache 2.0; restricciones de campo de uso a revisar si el proyecto cambia de naturaleza (académico → comercial) |
| **Gemma 2 / 3 (9B-12B)** | Licencia propia Google, sin tope de escala de usuarios | Buena calidad general | Buena | Eficiente en RAM, apta para hardware modesto | La licencia incorpora una **política de uso prohibido que restringe la generación de contenido en áreas médicas/de salud**, y Google se reserva el derecho de restringir remotamente un uso que la viole. Este proyecto redacta sobre condiciones físicas y pautas nutricionales — zona gris real, no descartable sin revisión legal |
| **Mistral 7B / Small** | Apache 2.0, sin restricciones | Aceptable, sin evidencia de liderazgo frente a Qwen en español | Soporte nativo de JSON mode y tool calling | Buen soporte en Ollama/vLLM | Ninguno relevante; queda como alternativa de respaldo |

**Fuentes consultadas** (documentación oficial y análisis de licencia, no rankings aislados): repositorios y model cards de Hugging Face para las licencias de Qwen2.5 por tamaño; análisis de la licencia de Gemma en TechCrunch y WCR.LEGAL sobre restricciones de uso; comparativas de rendimiento multilingüe y de soporte de runtime publicadas en 2025-2026 (ComputingForGeeks, benchmarks de tool calling en producción). Búsquedas realizadas en agosto de 2026; **revalidar antes de desplegar**, dado el ritmo de estas familias.

##### Decisión

**Qwen2.5-7B-Instruct** como modelo primario (o Qwen2.5-14B-Instruct si el hardware verificado lo permite con margen sobre RNF-04). Motivos, en orden de peso para este proyecto:

1. **Licencia**: Apache 2.0 sin tope de uso ni política de contenido restringido — es la única de las cuatro sin una zona de riesgo legal identificada para este dominio específico (salud/condición física).
2. **Español/multilingüe**: mejor evidencia relativa a tamaño equivalente que Llama 3.1, que es el candidato con el que más se lo compara por defecto.
3. **Structured output / tool calling**: maduro, necesario para RF-053/RF-054/RF-113 (validación de JSON Schema, reintento).
4. **Ecosistema de despliegue**: soporte GGUF amplio, compatible con Ollama de forma directa.

**Llama 3.1-8B-Instruct** queda documentado como alternativa de segunda preferencia: si la evaluación empírica sobre el conjunto de casos de [generative-ai.md §9](#arch-generative) muestra que Llama supera a Qwen en el dominio real del proyecto, o si el ecosistema de soporte comunitario resulta determinante para el equipo, se promueve sin cambiar nada fuera del AI Gateway (ver §15 de [generative-ai.md](#arch-generative)).

**Gemma queda deprioritizada**, no descartada de forma absoluta: si Qwen y Llama no cumplen calidad o rendimiento, Gemma es la siguiente opción a evaluar, pero requiere antes una revisión legal explícita de la política de uso prohibido contra el contenido real que este sistema genera (condiciones físicas, pauta nutricional).

**Mistral** queda como plan de respaldo con la misma licencia permisiva que Qwen, útil si Qwen no rinde bien en las pruebas iniciales.

#### 2. Runtime de inferencia

No confundir con el modelo: el runtime es el proceso que sirve el modelo, no el modelo en sí.

| Runtime | Operación | Uso de GPU | Batching/concurrencia | Structured output / tool calling | Observabilidad | Compatibilidad con hardware desconocido |
| --- | --- | --- | --- | --- | --- | --- |
| **Ollama** | Muy simple: un binario, un comando para cambiar de modelo (`ollama pull`) | Automática si hay GPU disponible, con fallback a CPU | Se degrada notablemente por encima de ~5 usuarios concurrentes según pruebas publicadas en 2025-2026 | API compatible con OpenAI, structured outputs y tool calling ya maduros, compatible de inmediato con clientes HTTP estándar | Básica (logs, métricas limitadas) | Alta: mismo binario corre en CPU o GPU sin cambiar la integración |
| **vLLM** | Requiere más configuración y tuning | Explícito, orientado a GPU | Excelente: PagedAttention sostiene alta concurrencia, ~6x el throughput de Ollama medido a 50 usuarios concurrentes en benchmarks publicados | Nativo y sólido | Mejor soporte de métricas de producción | Media: pensado para GPU dedicada, menos cómodo si el servidor termina siendo CPU-only |
| **llama.cpp** | Motor subyacente de Ollama; usarlo de forma directa agrega trabajo de integración sin ganancia si ya se usa Ollama | Sí, eficiente en CPU también | Limitada | Incompleto en la API directa (depende de la envoltura que se use) | Mínima sin envoltura adicional | Alta, pero redundante con Ollama para este proyecto |

##### Decisión

**Ollama** como runtime primario. Con la carga esperada de este proyecto (estimada en [generative-ai.md §16](#arch-generative): del orden de cientos de llamadas/día, muy por debajo del umbral de degradación observado en Ollama), la ventaja operativa —un equipo sin especialización en MLOps, sin GPU garantizada, necesitando cambiar de modelo sin fricción— pesa más que el throughput de producción de vLLM, que este proyecto no necesita todavía.

**vLLM queda documentado como ruta de escalamiento**, no como plan B inmediato: si el uso real supera el umbral de concurrencia donde Ollama se degrada (evidencia: a partir de ~5 usuarios simultáneos), se reemplaza el adaptador (`OllamaAdapter` → `VllmAdapter`) detrás del mismo puerto (`GenerativeAiPort`), sin cambios en el resto del backend.

**llama.cpp no se adopta como runtime directo**: ya es el motor detrás de Ollama para los formatos GGUF; adoptarlo por separado sólo agregaría una integración a mantener sin resolver nada que Ollama no resuelva ya para este proyecto.

#### 3. Resumen de la decisión

```text
Modelo:   Qwen2.5-7B-Instruct (GGUF, Q4_K_M/Q5_K_M según hardware verificado)
Runtime:  Ollama
Gateway:  puerto + adaptador dentro del servicio Python del Polo
          (patrón de ADR-0005; despliegue según ADR-0009)
```

Justificación completa y consecuencias en [ADR-0006](#adr-0006).


---

<a id="arch-predictive"></a>

### IA predictiva

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/architecture/predictive-ai.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ARCH-PREDICTIVE-AI`

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **Estado**     | Propuesto                                            |
| **Depende de** | [D5](#d5), [D8](#d8), [D9](#d9), [D11/DD-15, DD-31, DD-34](#d11), [analytics-engine.md](#arch-analytics), [generative-ai.md](#arch-generative) |

Este documento cubre los **objetivos, features, evaluación y ciclo de vida** de los componentes aprendidos. La mecánica del pipeline batch (extracción, validación, features point-in-time, entrenamiento, persistencia) ya está definida en [analytics-engine.md](#arch-analytics) y no se repite acá.

> ⏸ **Fuera de la Etapa 1.** RF-121 y RF-122 son los dos únicos componentes aprendidos que sobreviven a [DD-34](#d11), y ambos están marcados en D8 como **propuestas del equipo no validadas con el cliente**. El [baseline de alcance](#baseline) los difiere en consecuencia: no hay fundamento para consumir capacidad en ellos antes de confirmarlos. **En la Etapa 1 el proyecto entrega IA generativa, no predictiva**, y así conviene presentarlo. Este documento sigue siendo el diseño válido para cuando se confirmen.

#### 1. Qué es predictivo y qué no

Por [D11/DD-31](#d11), el diagnóstico (RN-79a), los ajustes (RN-89a), la compatibilidad (RN-44a-d) y la derivación del tipo de rutina (RN-39a) son **tablas deterministas**, no modelos aprendidos — están escritas, son auditables y no entran en este documento. Lo que sigue son **dos componentes** donde sí hay aprendizaje automático, ambos sobre series temporales, ninguno generativo, ninguno con respaldo directo del cliente (son propuestas de esta ronda de diseño — RF-121 y RF-122, ver el aviso en cada uno):

| Objetivo | Requerimiento | Tipo de tarea |
| --- | --- | --- |
| Sugerencia de carga de sesión `[propuesta 🆕, no validada con el cliente]` | RF-121 | Regresión sobre la tendencia reciente del alumno |
| Proyección de fuerza y mediciones corporales `[propuesta 🆕, no validada con el cliente]` | RF-122 | Proyección de serie temporal |

Ninguno de los dos usa un LLM para el cómputo: son problemas de serie temporal, no de lenguaje. Uno de ellos (RF-121) se **invoca** de forma síncrona desde el flujo de registro de sesión (FL-05), pero eso no cambia qué técnica lo resuelve.

**RF-121 y RF-122 no tienen pedido explícito del cliente detrás** (a diferencia del resto del corpus, evidenciado en RF-086 a RF-094 y decisiones del cliente — ver [D11/DD-01](#d11)). Surgieron de dos preguntas concretas planteadas durante el diseño de esta arquitectura: qué pasa entre sesión y sesión dentro del mismo ciclo de dos semanas (nada, hoy — hueco real entre RF-030 y RN-89a), y cómo dar una proyección de progreso sin inventar una cifra que el sistema no puede sostener. Quedan documentadas con prioridad SHOULD, marcadas `[S-11]` en [D12](#d12), y primeras en el orden de recorte — deben confirmarse con el cliente antes de construirse.

##### 1.1 Qué se movió fuera de este documento y por qué

Hasta el replanteo de IA del 2026-08-28 este documento describía cinco componentes aprendidos. Tres se reubicaron ([D11/DD-34](#d11)):

| Antes | Ahora |
| --- | --- |
| **Ranking de alternativas de sustitución (RF-059, RF-060)** — modelo clásico de similitud sobre atributos estructurados | Lo produce la **capa generativa** al pedírsele ejercicios parecidos, sobre el subconjunto del catálogo prescribible ya prefiltrado de forma determinista por patrón de movimiento y compatibilidad (RN-44a-d). Ver [generative-ai.md §7](#arch-generative). El orden alfabético por participación muscular de RN-49a queda como **fallback determinista** cuando el LLM no responde. |
| **Riesgo de abandono (RF-061 a RF-063)** — clasificación binaria / score de riesgo | **Descartado.** RF-061 a RF-063 pasan a WON'T por costo y esfuerzo relativos al valor esperado con los datos disponibles (S-03 `NO VERIFICADO`). No se degrada a una regla simple: se retira. El criterio de urgencia de la cartera (RF-107) deja de incluir el riesgo de abandono. Ver [D12/§4](#d12). |
| **Segmentación de perfiles (RF-064)** — clustering no supervisado sobre la base del gimnasio | La **descripción de perfil** la produce la capa generativa a partir de los indicadores ya calculados (frecuencia, volumen, intensidad relativos) y el objetivo del alumno, sin clustering. Es **efímera** — se genera al abrir la vista, no se persiste. Ver [generative-ai.md §1](#arch-generative). |

#### 2. Objetivo 1 — Sugerencia de carga de sesión (RF-121) `[propuesta, no validada con el cliente]`

| | |
| --- | --- |
| **Variable objetivo** | Carga y repeticiones sugeridas para la próxima serie de un ejercicio, dentro de la sesión de hoy |
| **Qué cubre hoy sin esto** | RF-030 precarga con el valor de la **última ejecución**, sin ajuste. RN-89a ajusta la prescripción cada dos semanas, a nivel de rutina, no de sesión. Entre ambos hay un hueco: de una sesión a la siguiente, dentro del mismo ciclo, nada sugiere progresión — el alumno decide solo si sube el peso (FL-05, paso 6) |
| **Features** | Tendencia de carga máxima estimada (e1RM) de las últimas sesiones en ese ejercicio, tendencia de esfuerzo percibido, cumplimiento de repeticiones reciente, si la última serie fue registrada como atípica (RN-55a) |
| **Datos históricos necesarios** | `RegistroSerie` del propio alumno en ese ejercicio — **no necesita datos de otros alumnos**: es un modelo por alumno-ejercicio, o una regla aplicada sobre la serie temporal individual. Esto lo hace viable incluso sin una base grande de usuarios (mitiga parcialmente S-03) |
| **Frecuencia de entrenamiento** | No aplica si se implementa como regla de progresión (p. ej. doble progresión: sube carga cuando se cumple el techo de repeticiones N sesiones seguidas); mensual si se implementa como modelo aprendido por segmento de alumnos |
| **Frecuencia de inferencia** | En el momento de precargar la serie (FL-05, paso 5), síncrono con la carga de la sesión — presupuesto de latencia acotado por RNF-06/RNF-07 (usabilidad de la pantalla de sesión), no por RNF-04 (que es del flujo generativo) |
| **Horizonte temporal** | Una sesión hacia adelante |
| **Criterio de referencia (baseline, RF-073)** | **RF-030 tal como existe hoy**: repetir el valor de la última ejecución. Es un baseline inusualmente fuerte y ya construido — cualquier sugerencia aprendida debe demostrar que mueve el cumplimiento o el esfuerzo percibido en una dirección mejor, no sólo que "parece razonable" |
| **Riesgo de leakage** | Bajo relativo al objetivo 2 (es intra-alumno, intra-ejercicio), pero la evaluación igual debe respetar el orden temporal: no usar sesiones futuras para sugerir una sesión pasada |
| **Piso de seguridad** | La sugerencia nunca reemplaza el mínimo de RF-030; si no hay tendencia suficiente (pocas sesiones registradas, datos contradictorios), se muestra exclusivamente el valor de RF-030. El alumno siempre confirma o corrige (FL-05, paso 6) — esto nunca se convierte en una prescripción automática |

#### 3. Objetivo 2 — Proyección de fuerza y mediciones corporales (RF-122) `[propuesta, no validada con el cliente]`

| | |
| --- | --- |
| **Variable objetivo** | Trayectoria proyectada de la carga máxima estimada por ejercicio y de las mediciones corporales (`MedicionCorporal`: peso, perímetros) si el alumno continúa con un patrón de entrenamiento similar al de las últimas semanas |
| **Por qué no es "predicción de músculo ganado"** | El sistema no mide composición corporal: la enumeración cerrada de [D2 §4.11](#d2) tiene 6 valores (peso y 4 perímetros), sin masa muscular ni porcentaje de grasa, y no hay instrumento (bioimpedancia, pliegues) que los capture. [D2 §2 — Términos prohibidos](#d2) ya excluye "calorías quemadas" y "puntaje de fitness" por no ser estimables con la información disponible; la misma razón aplica a una cifra de músculo ganado. Este objetivo proyecta **exactamente lo que el sistema ya deriva o registra** (e1RM, perímetros) y se presenta con esos nombres, nunca como composición corporal |
| **Features** | Serie temporal de carga máxima estimada por ejercicio; serie temporal de cada tipo de medición corporal registrada; adherencia del período (una proyección sobre una tendencia inestable es menos confiable y debe decirlo) |
| **Datos históricos necesarios** | `RegistroSerie` (para e1RM) y `MedicionCorporal` del propio alumno — igual que el objetivo 1, es por alumno, no depende de una base grande de usuarios |
| **Frecuencia de entrenamiento/inferencia** | A demanda, cuando el alumno consulta su panel de progreso (RNF-02) |
| **Horizonte temporal** | Semanas, a definir junto con el criterio de "patrón similar" — `NO VERIFICADO`, requiere acuerdo con el cliente sobre qué horizonte es útil sin volverse una promesa poco creíble |
| **Criterio de referencia (baseline)** | Extrapolación lineal simple de la tendencia reciente (regresión lineal sobre las últimas N semanas). Un modelo más complejo debe superar esto antes de promoverse (RF-073) |
| **Guardrail obligatorio** | Toda proyección se presenta con su incertidumbre (banda, no un único número) y con la declaración explícita de que es una proyección bajo continuidad de patrón, no una promesa de resultado — mismo principio que RF-012 y RF-108. Si el componente narrativo (capa generativa) redacta esta proyección en texto, se le aplica exactamente la misma verificación de valores citados que a RF-055/RF-056 (ver [generative-ai.md §9](#arch-generative)): el número proyectado tiene que provenir literalmente de este cálculo, nunca inventarse en la redacción |
| **Riesgo de leakage** | Igual que el objetivo 1: intra-alumno, pero respetar el orden temporal en la evaluación |

#### 4. Ciclo de vida (referencia)

El pipeline mecánico (extracción de snapshot, validación de esquema, features point-in-time, entrenamiento, evaluación contra el criterio de referencia, persistencia idempotente) está descrito en [analytics-engine.md §Pipeline](#arch-analytics). Lo que agrega este documento:

```text
Datos (PostgreSQL, snapshot versionado)
 ↓
Preparación + features point-in-time (motor Python)
 ↓
Training  ──sólo si hay volumen suficiente; si no, se usa el criterio de referencia──
 ↓
Evaluación contra criterio de referencia (RF-073, obligatoria, no opcional)
 ↓
¿Supera al criterio de referencia?
 ├─ No → se conserva el criterio de referencia, se documenta el resultado (E9)
 └─ Sí → Model registry mínimo: un identificador de versión + métricas, persistido junto al resultado (RF-072)
 ↓
Inferencia (batch/a demanda para el objetivo 2; síncrona por alumno-ejercicio para el objetivo 1)
 ↓
Monitoreo (§7)
 ↓
Reentrenamiento (mensual o a demanda)
```

**No se implementa un model registry ni feature store como los de un equipo de MLOps de producto**: dado el tamaño del proyecto (equipo universitario, capacidad de construcción de 504 h — [D12/§3](#d12)), el "registro" es la tabla `EvaluacionComponente` ya prevista en el [modelo de dominio](#d4) (componente, versión, dataset, tamaño de muestra, métricas obtenidas, métricas del criterio de referencia, fecha) más el archivo serializado del modelo versionado por nombre de archivo. Es proporcional al tamaño real del proyecto (no sobreingeniería, §29 de la tarea de origen).

**El objetivo 1 (§2, RF-121) no es batch.** Es una computación liviana por alumno-ejercicio (no poblacional), invocada de forma síncrona al precargar una serie (FL-05, paso 5). No entrena un modelo poblacional ni tiene ciclo de reentrenamiento mensual en el mismo sentido que el objetivo 2; su "entrenamiento" es, en el caso más simple, recalcular una tendencia sobre la serie temporal del propio alumno en el momento de la consulta. Se documenta la excepción para que no se le exija un pipeline batch que no necesita.

#### 5. Evaluación

| Objetivo | Métrica principal | Por qué |
| --- | --- | --- |
| Sugerencia de carga de sesión | Comparación contra RF-030: ¿la serie sugerida se completa con mejor cumplimiento o esfuerzo percibido más estable que repetir el último valor? | Mide si la sugerencia mejora sobre el baseline ya construido, no si "parece razonable" |
| Proyección de fuerza/mediciones | Error absoluto entre la proyección hecha en la semana N y el valor efectivamente observado en la semana N+k, contra el mismo error de la extrapolación lineal simple | Es forecasting: se evalúa contra lo que realmente pasó después, igual que cualquier proyección de serie temporal |

Sobre ambos: split train/validation/test respetando el orden temporal (nunca aleatorio — evitaría el leakage), y comparación obligatoria contra el criterio de referencia de cada objetivo (RF-073, RNF-26). Que el criterio simple gane es un resultado válido y debe informarse, no ocultarse — es la postura ya adoptada en D11/DD-31 y el propio D12/R-16.

**Detección de sobreajuste**: la métrica de validación y la de test deben mantenerse dentro de un margen declarado (a definir en la implementación); una brecha grande entre ambas invalida la promoción del modelo, con independencia de si superó al criterio de referencia en validación.

#### 6. Datos y calidad

- **Cantidad y representatividad**: dependen de S-03 (`NO VERIFICADO`). Si no hay historial real suficiente al momento de entrenar, se usa exclusivamente el criterio de referencia para cada objetivo y se declara explícitamente que el componente aprendido no está activo (RNF-12, DD-15: la ausencia del proceso no degrada el resto del sistema).
- **Datos simulados** (RF-071): identificados sin ambigüedad y excluidos de toda analítica presentada como real (DD-20, RNF-28). Un modelo entrenado sólo con datos simulados no debe presentarse como si generalizara a comportamiento real; se documenta esa limitación junto al resultado.
- **Datos faltantes**: ausencia de dato no equivale a cero (invariante ya declarada en [analytics-engine.md](#arch-analytics)) — un alumno sin esfuerzo percibido registrado no cuenta como esfuerzo percibido 0, cuenta como no evaluado en ese criterio (RN-81, precedente ya establecido).
- **Privacidad**: las features usadas son indicadores agregados y de comportamiento (adherencia, volumen, frecuencia, e1RM), no descripciones libres de condiciones físicas. El motor batch no debe recibir campos de texto libre con datos de salud como feature de un modelo — sólo los campos tipados que D4/D5 ya definen como calculables.

##### 6.1 Datasets externos evaluados para entrenar

Búsqueda de datasets públicos que pudieran acelerar el arranque de los objetivos 1 y 2, evitando el problema de partir de cero (S-03). Conclusión calibrada, sin sobrevender lo encontrado:

| Dataset | Contenido | Licencia | Utilidad real para este proyecto |
| --- | --- | --- | --- |
| [OpenPowerlifting](https://www.openpowerlifting.org/faq) | Resultados de competencias de powerlifting (sentadilla, banco, peso muerto) por atleta, a lo largo de años, a gran escala | Datos en dominio público (CC0) | Útil **sólo para el objetivo 2** (proyección de fuerza), y como validación de metodología, no como datos de entrenamiento directos: son atletas de competencia, no alumnos de gimnasio en general, y son intentos máximos en competencia, no series de entrenamiento |
| [free-exercise-db](https://github.com/yuhonas/free-exercise-db) | Catálogo de +800 ejercicios con clasificación muscular, equipamiento e instrucciones | Dominio público | No es un dataset de entrenamiento de modelos: es un candidato para la **carga inicial del catálogo** (RF-070, RF-099, S-09 en D12), un problema distinto y ya identificado en el corpus. Vale la pena evaluarlo para ese propósito, no para éste |
| Datasets de Kaggle de "gym workouts" (varios, ej. *Gym Members Exercise Dataset*, *721 Weight Training Workouts*) | Variado: algunos son resúmenes agregados por socio (no series temporales por sesión), otros son el registro de una sola persona durante varios años | Variable, revisar por dataset | El de una sola persona no generaliza a una población; los agregados no tienen el detalle serie-por-serie que exige `RegistroSerie`. Para los objetivos 1 y 2, al ser por alumno, el propio historial del alumno es lo que importa, no una base externa |

**Conclusión, sin dar vueltas:** no existe un dataset público que reemplace la necesidad de datos propios del sistema. Para los objetivos 1 y 2, al ser por alumno (no poblacionales), el propio historial del alumno alcanza sin necesidad de una base externa — son los objetivos menos expuestos al riesgo S-03, además de ser los menos evidenciados por el cliente (S-11). Mientras el historial real no exista, se usan datos simulados (RF-071) con la limitación siempre declarada (DD-20, RNF-28).

#### 7. Monitoreo posterior

- **Latencia**: para el objetivo 2 (batch/a demanda) se mide el tiempo del job completo, no de una predicción individual. Para el objetivo 1 (síncrono, dentro de FL-05) se mide como cualquier otra respuesta del backend, contra RNF-06/RNF-07.
- **Drift**: distribución de las features de entrada de una ejecución comparada contra la anterior; un cambio abrupto (p. ej. tras una migración de datos) debe alertar antes de publicar resultados nuevos.
- **Performance**: la métrica de §5 recalculada en cada reentrenamiento, conservada junto con la del criterio de referencia (RF-073), nunca sólo la del modelo aprendido.
- **Versión del modelo**: todo resultado persistido referencia la versión del componente que lo produjo (RF-072), ya modelado en `EvaluacionComponente`.


---

<a id="parte-vii"></a>

## Parte VII — Decisiones y ADR

<a id="d11"></a>

### D11 — Registro de decisiones de diseño

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/design-decisions.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D11`

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.2        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | Todos      |

**Cambios de la v1.0:** DD-13 (nutrición) queda resuelta · decisiones nuevas DD-26 a DD-32, que cierran los bloqueantes de la auditoría · 👁 marca las decisiones que las fuentes tomaron sin advertir que estaban decidiendo.

**Cambios de la v2.0:** DD-33, el candidato de rutina.

**Cambios de la v2.1:** DD-31 se ajusta al alcance generativo confirmado y a la ADR del servicio generativo: el LLM construye el candidato inicial; las tablas explícitas permanecen como validación y para el ciclo de adaptación.

**Cambios de la v2.2 ([baseline de alcance](#baseline)):** se escribe **DD-34**, el replanteo de IA del 2026-08-28 que ocho documentos del corpus ya citaban como fundamento y que **nunca había sido redactado** · se incorpora **DD-35**, el piso de disponibilidad de la prescripción tras retirarse los presets · **DD-33 queda derogada para la Etapa 1** y **DD-13 queda sin efecto** en ella; ambas conservan su texto íntegro por si el alcance se reabre.

**Alcance de estas decisiones.** Una decisión marcada «derogada para la Etapa 1» o «sin efecto» **no está anulada**: describe un diseño válido cuyo requisito de origen quedó fuera del alcance de esta etapa. Si el requisito vuelve, la decisión vuelve con él. Distinguirlo importa: borrarlas obligaría a rediscutirlas desde cero.

---

##### DD-01 · Jerarquía de las fuentes

**Contexto.** Tres cuerpos de material de distinta antigüedad y autoridad, sin fechas.
**Elegida.** Pedido del cliente (RF-082 a RF-094 y decisiones posteriores) > especificación funcional > análisis de scope inicial.
**Fundamento.** El análisis inicial es una opinión escrita antes de conocer el pedido del cliente. Conciliar produciría un documento sin criterio.
**Consecuencia asumida.** Varias recomendaciones bien argumentadas del análisis inicial quedan derogadas, en particular su tesis de que el ajuste de la rutina es trabajo manual del entrenador.

##### DD-02 · Copia al solicitar **más** versiones completas de la rutina

**Contexto.** Modificar una plantilla no debe alterar rutinas ya creadas (RF-022); aplicar una adaptación debe generar una versión nueva conservando las anteriores (RF-092).
**Opciones.** (a) Referencia a la plantilla. (b) Versionado con diferencias y propagación. (c) Copia sin versiones. (d) **Copia más versiones completas**.
**Elegida.** (d).
**Fundamento.** La objeción de coste al versionado apuntaba a las diferencias, la propagación y la resolución de conflictos. Una versión completa de una rutina es una copia profunda de una estructura pequeña: no hay diferencias que calcular ni conflictos que resolver, y RF-093 se responde comparando dos versiones.
**Consecuencia asumida.** Duplicación de datos, irrelevante a esta escala. Los cambios de plantilla no se propagan, que es el comportamiento deseado.

##### DD-03 · La sesión congela su propia prescripción 👁

**Elegida.** Al iniciarse, la sesión copia la prescripción del día en sus registros de serie (RF-028).
**Fundamento.** Vuelve cada sesión autocontenida e inmune a toda edición posterior, y produce el cumplimiento por serie sin trabajo adicional.
**Consecuencia asumida.** Duplicación de la prescripción por sesión.
**Nota.** La especificación heredada enuncia esto como requerimiento sin registrar que es la decisión de modelado más determinante del sistema. Sin ella, el versionado de DD-02 reescribiría el pasado.

##### DD-04 · Derivar los indicadores, persistir sólo eventos, salidas de componentes y marcas

**Elegida.** Derivar volumen, frecuencia, carga máxima estimada, adherencia y cumplimiento; persistir récords, diagnósticos, propuestas, estimaciones y el estado de compatibilidad de cada ejercicio de rutina.
**Fundamento.** Un indicador persistido queda inconsistente cuando cambia su definición. Un récord y una salida de componente son eventos fechados: recalcularlos pierde el instante y la versión.
**Excepción explícita.** El estado de compatibilidad es el único derivado que se persiste, porque la marca debe estar disponible al iniciar una sesión y en la vista de rutina sin recalcular el conjunto.

##### DD-05 · Catálogo base global, catálogo propio por gimnasio

**Contexto.** RF-013 exige un catálogo accesible a todos; RF-069 exige aislamiento por gimnasio; RF-017 permite a entrenadores crear ejercicios. Las tres cosas no pueden ser ciertas con un catálogo único.
**Elegida.** Base global no editable más catálogo propio por gimnasio.
**Fundamento.** Un catálogo global único filtra ejercicios de un gimnasio a otro; uno replicado multiplica la carga inicial y la curación, que es el trabajo caro y el que determina la calidad del volumen.
**Consecuencia asumida.** Un entrenador no puede promover su ejercicio al catálogo base.

##### DD-06 · La aptitud advierte, nunca bloquea

**Elegida.** Advertencia destacada al poner una rutina en vigencia y al iniciar una sesión; ninguna operación impedida `[F: cliente]`.
**Consecuencia asumida.** El sistema puede tener alumnos entrenando sin aptitud vigente. La responsabilidad queda en el gimnasio, y la advertencia queda registrada.

##### DD-07 · El estado de membresía es informativo

**Elegida.** Informativo `[F: cliente]`.
**Fundamento.** Una regla de bloqueo atraviesa todos los flujos de entrenamiento y multiplica los casos borde a cambio de valor nulo para el ciclo central.

##### DD-08 · Los roles son un conjunto 👁

**Fundamento.** Un entrenador también entrena. Modelarlo como valor único obliga a un rediseño en cuanto aparece el primer caso.
**Nota.** Es gratis ahora y caro después. Ver DD-28, que resuelve el caso concreto que esta decisión habilita.

##### DD-09 · Nada se borra

**Elegida.** Desactivación lógica universal; la única eliminación real es la anonimización en la baja de cuenta.
**Consecuencia asumida.** El catálogo y la base de usuarios acumulan registros inactivos.

##### DD-10 · La rutina es cíclica, no un calendario 👁

**Elegida.** El sistema propone el siguiente día del ciclo; el alumno elige.
**Fundamento.** Refleja cómo se entrena realmente y elimina un módulo entero de agenda, recordatorios y días perdidos. La adherencia se resuelve con la frecuencia semanal objetivo.
**Consecuencia asumida.** No hay recordatorios por día ni concepto de "día perdido".

##### DD-11 · Constantes documentadas en lugar de configuración

**Elegida.** Constantes fijadas en D5, cada una con su origen marcado; RF-047 desciende a COULD.
**Fundamento.** Ventanas configurables hacen que la adherencia de dos alumnos no sea comparable, y la comparación es lo que sostiene la cartera priorizada y la analítica del gimnasio.

##### DD-12 · Un solo entrenador vigente sobre una relación con historial

La estructura soporta el historial; RN-18 impone la unicidad. Sin el historial no se puede responder qué entrenador supervisó un período ni calcular la carga por entrenador. Coste marginal: nulo.

##### DD-13 · Alcance de la pauta nutricional — **RESUELTA**

**Contexto.** El cliente pidió generar dietas y descartó el seguimiento de comidas. La especificación heredada había excluido la generación de planes nutricionales por riesgo sanitario sin validador profesional.
**Opciones.**

|     | Forma                                                                                       | Riesgo                                                                                                            | Coste |
| --- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----- |
| (a) | Plan de comidas redactado libremente por un componente generativo                           | **Alto.** Sin base de alimentos no hay forma de verificar la salida; puede producir déficits o ignorar patologías | Bajo  |
| (b) | Plantillas de menú precargadas y revisadas por el equipo                                    | Bajo                                                                                                              | Medio |
| (c) | **Distribución orientativa de energía y macronutrientes por comida, sin nombrar alimentos** | Bajo                                                                                                              | Bajo  |

**Elegida.** (c). RF-075 y RF-108 quedan redactados en esos términos; RF-076 sigue fuera.
**Fundamento.** Cumple el pedido —el sistema produce una pauta alimentaria personalizada— sin afirmar nada que no pueda sostener y sin necesitar la base de alimentos que quedó fuera de alcance. (a) es la única opción que reintroduce el riesgo que la especificación había descartado, y también la única sin forma de evaluarse.
**Consecuencia asumida.** El alumno no recibe qué comer, sino cuánta energía y cuánta proteína distribuir. Si el cliente considera que eso no cumple su pedido, hay que volver sobre la decisión antes de construir, no después.
**Estado (v2.2).** **Sin efecto en la Etapa 1.** RF-012 obtuvo 2 votos de 8 y RF-074 obtuvo 1; con ellos fuera cae toda la cadena nutricional —RF-075 y RF-108 incluidos— y esta decisión queda sin sujeto. Coincide con el primer paso del orden de recorte de D12. El texto se conserva porque la pregunta que resuelve —qué significa «generar la dieta»— volverá si vuelve la nutrición.

##### DD-14 · Dos clases de componente inteligente

**Contexto.** El cliente definió la inteligencia como centro del producto; la redacción heredada de RF-057 prohibía que los componentes generativos produjeran valores o prescribieran cargas.
**Elegida.** Se distingue **componente de decisión** (produce valores y estructuras; validado y sujeto a revisión humana) de **componente narrativo** (sólo redacta sobre hechos calculados; no introduce ningún valor ausente de su entrada).
**Fundamento.** Prohibirle al sistema producir valores es incompatible con que decida. Mantener la prohibición sobre lo narrado conserva la única métrica de calidad barata, objetiva y contundente del proyecto: cero valores inventados en los textos.
**Consecuencia asumida.** El riesgo se traslada del texto a la prescripción, y se contiene con dos barreras: la validación automática de compatibilidad y de rangos, y la revisión del entrenador.

##### DD-15 · Las estimaciones se calculan de forma diferida

**Elegida.** Diferida y periódica, más a demanda del administrador.
**Fundamento.** Elimina la latencia en la petición del usuario, la dependencia de un segundo servicio en el camino crítico y el versionado en tiempo de ejecución. Y hace verdadera la regla de continuidad: si el proceso nunca corre, la columna dice "no disponible" y nada se rompe.
**Consecuencia asumida.** La estimación tiene la antigüedad de la última ejecución, que por eso se muestra siempre junto al valor.

##### DD-16 · Historial de objetivos y de condiciones con vigencia

**Fundamento.** Sin él no se puede determinar qué condiciones regían cuando se prescribió algo, y toda auditoría de una decisión pasada queda sin sustento.
**Consecuencia asumida.** Modelado temporal en dos entidades más, con su coste de consulta. Es el coste de poder explicar una decisión pasada.

##### DD-17 · El alumno no ve su estimación de riesgo

**Fundamento.** Presentarle una probabilidad de abandono es contraproducente y no admite justificación defendible. Sí ve sus indicadores objetivos de adherencia y cumplimiento, que son accionables.
**Consecuencia asumida.** Una vista distinta según el rol sobre el mismo alumno.
**Estado (v2.2).** **Sin efecto.** Al retirarse RF-061 a RF-063 en [DD-34](#dd-34--la-ia-predictiva-se-reduce-a-dos-componentes-por-alumno) no hay estimación de riesgo que mostrar ni que ocultar. El alumno sigue viendo sus indicadores objetivos de adherencia y cumplimiento.

##### DD-18 · Toda salida inteligente se registra con su versión y su contexto

**Fundamento.** Es lo que separa un componente evaluable de uno meramente demostrable, y lo que permite responder "¿por qué el sistema propuso esto?" seis semanas después.
**Consecuencia asumida.** Almacenamiento del contexto por cada resultado producido.

##### DD-19 · La sustitución cuenta como cumplimiento

**Elegida.** Cuenta como cumplida, marcada como sustituida; el volumen se imputa al ejercicio ejecutado.
**Fundamento.** Si sustituir castiga la métrica, el alumno deja de declararlo y el registro se degrada — y con él el contexto del que depende toda la inteligencia del sistema.

##### DD-20 · Los datos simulados se marcan y se excluyen de la analítica real

**Fundamento.** Un panel de retención que mezcla alumnos simulados con reales produce un número que no significa nada, y es indistinguible de uno correcto.

##### DD-21 · No hay acceso no autenticado

**Elegida.** Eliminado el catálogo público.
**Fundamento.** Agrega un cuarto ámbito de permisos y una superficie pública a cambio de valor nulo para el ciclo central. Refuerza además DD-29: el sistema no es abierto.

##### DD-22 · El administrador no accede al detalle individual sensible 👁

**Elegida.** Acceso de gestión y de agregación; sin sesiones, mediciones ni condiciones de un alumno concreto. Sí registra la aptitud, porque la constancia se presenta en el gimnasio y alguien tiene que cargarla, pero sólo su vigencia.
**Fundamento.** Minimización: su función no lo requiere.
**Consecuencia asumida.** Ante un problema con un alumno, el administrador depende del entrenador. Es correcto.

##### DD-23 · El fin de la asignación revoca también el acceso al histórico

**Fundamento.** El fundamento del acceso es la relación vigente, no el mérito histórico.
**Consecuencia asumida.** El indicador de carga por entrenador del panel del gimnasio se calcula sobre datos agregados y no requiere visibilidad individual del entrenador.

##### DD-24 · El correo es único por gimnasio, no globalmente

**Fundamento.** El sistema sirve a varios gimnasios y una persona puede ser alumna de dos.
**Consecuencia asumida.** La identificación en el ingreso debe resolver a qué gimnasio corresponde la cuenta. Es una consecuencia real y hay que diseñarla.

##### DD-25 · El entrenador es la única puerta

**Contexto.** El cliente indicó que el entrenador debe revisar toda rutina antes de que llegue al alumno. Esto contradice RF-025 (autoasignación) y la rama de RF-091 que facultaba al alumno a aprobar en ausencia de entrenador.
**Opciones.** (a) Eliminar la autoasignación. (b) **Conservarla como solicitud que no rige hasta ser revisada.** (c) Mantener la excepción para alumnos sin entrenador.
**Elegida.** (b), y se deroga la rama de RF-091.
**Fundamento.** (b) conserva la utilidad de que el alumno elija, elimina la excepción y deja una sola puerta. (c) reintroduce exactamente el caso que se quiso evitar.
**Consecuencia asumida, y es seria.** Todo alumno debe tener un entrenador vigente. Un alumno sin entrenador no puede recibir ninguna rutina nueva ni ninguna adaptación, y el sistema depende de que el entrenador revise a tiempo. Se mitiga con RF-112 y con el indicador E1b de D1, pero **el sistema queda expuesto a la congestión humana**. Riesgo registrado en D12/R-09.

##### DD-26 · El equipamiento es del gimnasio, no del alumno

**Contexto.** ¿Contra qué conjunto de equipamiento se valida una prescripción? `[F: cliente, 2026-08-18: "el foco está en el usuario, pero lo mantiene el gimnasio porque está asociado al mismo — depende de qué máquinas tiene el gimnasio"]`
**Opciones.** (a) Lo declara el alumno. (b) **Lo declara el gimnasio.** (c) Ambos, con intersección.
**Elegida.** (b). El inventario del gimnasio es la única fuente; el alumno no declara equipamiento.
**Fundamento.** Con (a), la falta de equipamiento sólo puede advertir —el alumno podría tener acceso circunstancial a algo que no declaró— y la validación se vuelve blanda: el generador puede proponer ejercicios imposibles. Con (b) la validación se vuelve dura: si la máquina no está en el gimnasio, el ejercicio no se puede hacer. (c) duplica el mantenimiento y reintroduce la ambigüedad de (a).
**Qué se gana.** El catálogo prescribible queda determinado por gimnasio; la incompatibilidad por equipamiento pasa de advertencia a impedimento (RN-47); la puesta en contexto del alumno pierde un paso; y el administrador adquiere una función con efecto real sobre la prescripción en lugar de un rol puramente administrativo.
**Qué se sacrifica.** Un alumno que además entrena en su casa no puede recibir una rutina que use su propio equipamiento.
**Consecuencia operativa que hay que asumir.** Si el administrador declara mal el inventario, todo el catálogo prescribible del gimnasio es incorrecto y ninguna rutina generada sirve. El inventario es un dato crítico, no una configuración cosmética. Riesgo en D12/R-15.

##### DD-27 · Objetivo y tipo de rutina comparten enumeración

**Contexto.** RF-083 exige verificar la correspondencia entre el tipo de la rutina y el objetivo del alumno, y las dos enumeraciones heredadas no coincidían.
**Elegida.** Una única enumeración de cuatro valores para ambos, con `ACONDICIONAMIENTO_GENERAL` compatible con cualquier objetivo.
**Fundamento.** Convierte la verificación de RF-083 en una comparación en lugar de un juicio, y la vuelve verificable sin ambigüedad.
**Consecuencia asumida.** `READAPTACION` queda fuera: no tiene objetivo de alumno equivalente y arrastra implicancias clínicas que el sistema declara fuera de alcance. Si el cliente lo requiere, hay que reabrir esta decisión y también el no-alcance de salud clínica de D1/§6.

##### DD-28 · Un entrenador que entrena necesita otro entrenador

**Contexto.** DD-08 admite que un usuario tenga los roles de alumno y entrenador. Pero RN-22 impide autoasignarse y DD-25 exige un entrenador vigente para que una rutina rija. Combinadas, dejaban al entrenador sin poder entrenar, mientras D3 afirmaba lo contrario.
**Opciones.** (a) Permitir que se apruebe a sí mismo. (b) Permitir que el administrador apruebe en ese caso. (c) **Exigir que otro entrenador lo tome como alumno.**
**Elegida.** (c).
**Fundamento.** (a) abre un agujero en la única regla que el cliente declaró indelegable. (b) convierte al administrador en aprobador de prescripciones, para lo cual no tiene ni competencia ni acceso a la información clínica (DD-22).
**Consecuencia asumida, y hay que decirla.** En un gimnasio con un solo entrenador, ese entrenador no puede tener rutina vigente. El sistema lo señala al administrador como situación a resolver incorporando otro entrenador. Es una limitación real, no un descuido.

##### DD-29 · El alta es por invitación

**Contexto.** `[F: cliente, 2026-08-18: "el sistema no es abierto para cualquier usuario; un gimnasio tiene que estar afiliado y avisarle al usuario para que se registre"]`
**Elegida.** La invitación nominal es la única vía de alta. La emite un administrador para cualquier rol, o un entrenador sólo con rol alumno, y determina el gimnasio y los roles del usuario resultante.
**Fundamento.** Resuelve de una sola vez cuatro problemas que estaban abiertos: cómo queda vinculado un usuario a un gimnasio, quién decide sus roles, cómo se impide el crecimiento espontáneo de usuarios, y quién responde por cada incorporación.
**Consecuencia asumida.** No hay adquisición espontánea de usuarios, que es exactamente lo que el modelo de negocio pide. Y el primer administrador de cada gimnasio no puede crearse por esta vía: ver DD-30.

##### DD-30 · El aprovisionamiento está fuera de la aplicación

**Contexto.** Si el alta es por invitación, nadie dentro de un gimnasio nuevo puede emitir la primera.
**Opciones.** (a) Un rol superadministrador multi-gimnasio dentro de la aplicación. (b) **Una operación de aprovisionamiento del proveedor, externa a la aplicación.** (c) Autorregistro del primer administrador.
**Elegida.** (b), atómica: o quedan creados el gimnasio y su primer administrador, o no queda nada.
**Fundamento.** (a) reintroduce el superadministrador multi-gimnasio, que está fuera de alcance y arrastra un cuarto ámbito de permisos. (c) contradice DD-29.
**Consecuencia asumida.** El sistema tiene una operación que no es accesible desde ninguna pantalla y que hay que ejecutar y documentar aparte. Es el precio de que el modelo de alta sea cerrado y coherente.

##### DD-31 · La generación y las reglas tienen autoridades distintas

**Contexto.** El alcance generativo v2.1 asigna al LLM la interpretación, el tipo y la construcción completa de la rutina. A la vez, compatibilidad, estructura y adaptación necesitan criterios verificables que impidan publicar una salida insegura o imposible.
**Elegida.** El LLM interpreta el pedido, selecciona el tipo y construye el candidato inicial. RN-39a y RN-44a a RN-44d no generan esa rutina: son barreras determinísticas y auditables que toda salida debe superar. El diagnóstico RN-79a y los ajustes RN-89a permanecen determinísticos. Los componentes aprendidos actúan en alternativas, riesgo y segmentación.
**Fundamento.** Esta división cumple el alcance sin transferir autoridad de seguridad al modelo. El candidato puede variar; catálogo, compatibilidad, rangos y puerta del entrenador no.
**Consecuencia asumida.** Una salida inválida se descarta y admite un reintento; después la generación queda no disponible. No existe construcción determinística alternativa. Las plantillas privadas y la creación manual por entrenadores siguen disponibles; **los presets son alcance opcional y no son la contingencia** ([DD-35](#dd-35--la-plantilla-del-entrenador-es-el-piso-de-disponibilidad-de-la-prescripción)). Ver ADR 0009, D12/R-08 y D13/N-15.

##### DD-32 · Existe una vía de corrección tardía, nominal y auditada

**Contexto.** El plazo de corrección de 48 h dejaba sin remedio un error detectado después, y un valor equivocado contamina de forma permanente la carga máxima estimada, el diagnóstico y toda la cadena de adaptación.
**Opciones.** (a) Ninguna corrección tardía. (b) **Desbloqueo por el entrenador, una sola vez por sesión, con motivo auditado.** (c) Corrección libre sin plazo.
**Elegida.** (b), complementada con el recálculo del récord sobre el histórico completo (RN-71) y con la confirmación de valores atípicos en el momento del registro (RN-55a).
**Fundamento.** (a) preserva la estabilidad de los indicadores a costa de conservar datos que se sabe que son falsos. (c) elimina la estabilidad de los indicadores. La excepción nominal y auditada conserva ambas cosas.
**Consecuencia asumida.** El plazo de 48 h deja de ser absoluto. El límite de un desbloqueo por sesión es lo que impide que la excepción se convierta en la norma.

##### DD-33 · El candidato se moldea; la propuesta, no

**Contexto.** El corpus dejaba que la rutina generada naciera PROPUESTA y le llegara al entrenador tal como salió del componente. El alumno que la había solicitado no tenía modo de intervenir sobre ella salvo pedir otra entera —consumiendo una rutina DESCARTADA y un aviso por RN-36a— o comentarla. Si el alumno no puede moldear lo que pidió, que la solicite él o que se la genere el sistema por su cuenta son la misma funcionalidad.
**Opciones.** (a) La rutina generada nace PROPUESTA, sin intervención del solicitante. (b) El alumno edita libremente su rutina propuesta. (c) **La generación produce un candidato ajustable, que sólo al confirmarse se convierte en rutina PROPUESTA.**
**Elegida.** (c), con las operaciones del alumno acotadas por D5/§5.2, revalidación en el acto (RN-126) y un tope de tres regeneraciones (RN-127).
**Fundamento.** (a) convierte la solicitud del alumno en un trámite y desaprovecha la ocasión más barata de acercar el plan a lo que la persona efectivamente va a hacer; además empuja toda inconformidad a la única salida disponible, que es pedir otra rutina entera. (b) contradice la matriz de D3 y, sobre todo, borra la frontera entre lo que el alumno elige y lo que el entrenador prescribe: series, repeticiones, descansos y cargas son prescripción. (c) conserva las dos cosas: el alumno decide **qué ejercicios** hace, el entrenador decide **cómo se hacen**, y la puerta de RN-35 sigue intacta porque nada rige sin revisión.
**Consecuencia asumida.** Aparece un objeto que no está en el ciclo de vida de D6 —el candidato— que no se persiste como rutina y muere si no se confirma; se declara explícitamente en D6/§1 para que nadie lo resuelva agregando un estado BORRADOR. Y el entrenador debe recibir en la revisión la diferencia entre lo que el componente produjo y lo que el alumno confirmó (RN-129, RF-120): sin eso revisaría como `GENERADA` una rutina que en realidad armó el alumno.
**Estado (v2.2).** **Derogada para la Etapa 1.** Al quedar fuera de alcance la solicitud de rutina por el alumno (RF-025, 3 votos de 8), desaparece el solicitante que esta decisión habilitaba a moldear el candidato. Su propio fundamento lo anticipa: si el alumno no puede moldear lo que pidió, que la solicite él o que se la genere el sistema son la misma funcionalidad — y en la Etapa 1 es lo segundo. RF-119, RF-120 y RN-124 a RN-129 quedan diferidos con ella. El texto se conserva íntegro: si el alcance se reabre, esta decisión vuelve tal como está.

##### DD-34 · La IA predictiva se reduce a dos componentes por alumno

**Contexto.** Replanteo de alcance de IA del 2026-08-28. `predictive-ai.md` describía cinco componentes aprendidos: alternativas de sustitución (RF-059, RF-060), riesgo de abandono (RF-061 a RF-063), segmentación de perfiles (RF-064), sugerencia de carga (RF-121) y proyección de trayectoria (RF-122). Construir y mantener cinco modelos clásicos —con sus features, entrenamiento, evaluación y despliegue batch— excede la capacidad del proyecto, y tres de ellos resuelven problemas que la capa generativa ya instalada cubre a costo marginal.

**Opciones.** (a) Conservar los cinco componentes aprendidos. (b) **Reducir a los dos que la capa generativa no puede cubrir, reubicar dos en ella y retirar uno del alcance.** (c) Retirar toda la IA predictiva y dejar sólo la generativa.

**Elegida.** (b), con este reparto:

| Componente                                   | Antes | Ahora                                                                                                                                                                                                                                    |
| -------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-059, RF-060 · alternativas de sustitución | ML    | **AI.** El orden lo produce la capa generativa sobre el subconjunto del catálogo ya prefiltrado de forma determinista por patrón, compatibilidad y equipamiento, con revalidación determinista posterior (RF-113). Siguen MUST            |
| RF-064 · segmentación de perfiles            | ML    | **AI.** Descripción del perfil de comportamiento redactada por la capa generativa a partir de los indicadores ya calculados, **sin clustering y sin persistirse**. Sigue SHOULD                                                           |
| RF-061 a RF-063 · riesgo de abandono         | ML    | **WON'T.** Se retiran del alcance por costo y esfuerzo frente al valor esperado con los datos disponibles (S-03). **No se degradan a una regla simple: se retiran**                                                                       |
| RF-121 · sugerencia de carga                 | ML    | Se conserva como componente aprendido. SHOULD                                                                                                                                                                                            |
| RF-122 · proyección de trayectoria           | ML    | Se conserva como componente aprendido. Sube de COULD a SHOULD                                                                                                                                                                             |

**Fundamento.** (a) mantiene cinco líneas de aprendizaje automático en un proyecto cuya capacidad ya está por debajo del alcance, y dos de ellas producen salidas que un modelo de lenguaje ya instalado genera con calidad suficiente sobre entradas que el sistema calcula de todos modos. (c) elimina la única dimensión de aprendizaje automático genuino y deja sin sujeto a RF-073 y RNF-26. (b) conserva esa dimensión donde tiene sustento —dos componentes por alumno, sobre series temporales que el sistema efectivamente captura— y libera la capacidad que consumían los otros tres.

El riesgo de abandono se retira **y no se sustituye por una regla**, porque una regla simple sobre inasistencia no es una estimación de riesgo: es un umbral de inasistencia, y presentarlo como lo primero sería peor que no tenerlo.

**Consecuencias asumidas.**

- **Se pierde la reproducibilidad exacta del orden de alternativas.** RF-059 pasa al estándar de «validez repetida» del resto de la capa generativa. RF-072 y RNF-27 se cumplen **persistiendo la lista producida**, no reejecutándola.
- **Se amplía la superficie de dependencia del servidor de modelos.** FL-06 —sustitución durante una sesión en curso, sin lenguaje natural de por medio— pasa a invocar el modelo, con el orden determinista de RN-49a como alternativa cuando no responde (RN-99). Es una dependencia que antes no existía y hay que medirla.
- **Se derogan `ScoreRiesgo` y `SegmentoPerfil`** en D4. `EvaluacionComponente` se conserva para RF-121 y RF-122.
- **FL-16 queda derogado** y RF-107 pierde «riesgo de abandono alto» de su orden de urgencia.
- **DD-17 queda sin efecto**: no hay estimación de riesgo que ocultarle al alumno.
- **La parte de [ADR-0008](#adr-0008) referida al ranking de RF-059 queda reemplazada**; el resto de esa ADR sigue vigente.
- **Degradar RF-061 a RF-063 desde MUST exige acuerdo explícito del cliente** (D12/§4). Esta decisión lo propone; no lo sustituye. La votación posterior lo respalda: obtuvieron 1, 0 y 0 votos de 8.

##### DD-35 · La plantilla del entrenador es el piso de disponibilidad de la prescripción

**Contexto.** El equipo resolvió no construir presets —«No usaremos preset, todo será generado desde cero con una batería de prompts», respuesta a D4 del Acta de Redefinición— y la votación lo confirma: RF-021 obtuvo 1 voto de 8. Pero RF-058, RN-95b y la ADR del servicio generativo apoyaban **toda** la continuidad ante indisponibilidad en «conservar la solicitud de presets publicados del gimnasio como vía disponible». Retirado el preset, esa garantía quedó sin referente y la creación de rutinas pasó a depender por completo de un servicio que corre en infraestructura de terceros.

**Opciones.** (a) Dejarlo como está y aceptar que sin servicio generativo no hay ninguna vía de prescripción. (b) **Designar la plantilla del entrenador (RF-019) como vía manual y piso de disponibilidad.** (c) Reintroducir los presets contra la decisión del equipo y la votación. (d) Construir un generador determinístico de rutinas como alternativa.

**Elegida.** (b). En este corpus un preset **era** una plantilla publicada: RF-021 agregaba la publicación y la reutilización entre entrenadores, no la capacidad de construir la rutina. Esa capacidad vive en RF-019, que obtuvo 8 votos de 8. Lo que se pierde al retirar RF-021 es compartirlas; lo que se conserva es poder crearlas y asignarlas.

**Fundamento.** (a) deja al producto sin ninguna forma de cumplir su propia capacidad C1 cuando falla un servicio externo. (c) contradice una decisión explícita del equipo y una votación inequívoca. (d) es exactamente el fallback determinístico que [ADR 0009](#adr-0009) descartó de forma deliberada, y reconstruirlo duplicaría la lógica de prescripción en dos implementaciones que divergirían.

**Consecuencia asumida, y hay que decirla con todas las letras.** RF-019 deja de ser una comodidad del entrenador y pasa a ser un requisito de disponibilidad: **si un gimnasio no tiene ninguna plantilla cargada y el servicio generativo no responde, un alumno nuevo no obtiene ninguna rutina.** No hay mitigación técnica para ese caso dentro del alcance recortado; la mitigación es operativa —cargar plantillas de arranque al aprovisionar el gimnasio— y hay que ejecutarla, no suponerla. Ver [D12/R-17](#d12) y la decisión PD-03 del [baseline de alcance](#baseline).


---

<a id="adr-0001"></a>

### ADR 0001 — Monorepo y motor analítico batch

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0001-monorepo-and-batch-engine.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0001`

- Estado: reemplazada por ADR 0002
- Fecha: 2026-08-18

#### Contexto

Nueve integrantes trabajarán durante aproximadamente catorce semanas. El producto combina una SPA, una API transaccional y análisis/ML, pero el presupuesto no justifica microservicios ni múltiples despliegues backend.

#### Decisión

Mantener frontend, backend, contratos y motor Python en un único repositorio. Desplegar el backend como monolito modular. Ejecutar el motor como proceso programado o manual que escribe resultados en PostgreSQL, fuera del camino de las peticiones.

#### Consecuencias

- La IA puede inspeccionar contratos y consumidores juntos.
- Los cambios transversales se revisan en un solo PR.
- El motor puede usar el ecosistema Python sin imponerlo al backend.
- No hay inferencia online ni segundo servicio obligatorio.
- CI debe validar TypeScript y Python y se deben respetar límites explícitos entre carpetas.


---

<a id="adr-0002"></a>

### ADR 0002 — Separación en tres repositorios

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0002-three-repositories.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0002`

- Estado: aceptada, parcialmente reemplazada por ADR 0003 y ADR 0009
- Fecha: 2026-08-24

#### Contexto

El equipo decidió asignar frontend, backend y análisis/IA a repositorios independientes. La frontera de despliegue y la responsabilidad de cada grupo pesan más que la navegación conjunta del monorepo.

#### Decisión

Mantener tres repositorios:

- `proyecto-gimnasio`: SPA React;
- `proyecto-gimnasio-back`: API Express, Prisma y PostgreSQL;
- `proyecto-gimnasio-ia`: servicio generativo online y procesos batch Python.

El backend publica OpenAPI para frontend. IA publica OpenAPI para su servicio de orquestación; backend genera o valida su cliente desde una versión explícita. La analítica batch se integra por estructuras persistidas o snapshots acordados. Nunca hay imports entre repositorios.

El corpus funcional y técnico vive exclusivamente en `proyecto-gimnasio-documentacion` según ADR 0003. Los repositorios de código conservan sólo README y AGENTS locales y enlazan la fuente canónica.

#### Consecuencias

- Cada repositorio instala, prueba, versiona y despliega de manera autónoma.
- Se eliminan workspaces y dependencias por ruta local.
- Los cambios transversales requieren coordinación y PR relacionados.
- La documentación compartida no se copia; cada cambio indica los repositorios afectados.
- [ADR 0009](#adr-0009) agrega un servicio generativo online al repositorio IA sin alterar la frontera de los jobs batch.


---

<a id="adr-0003"></a>

### ADR 0003 — Repositorio documental central

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0003-central-documentation-repository.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0003`

- Estado: aceptada
- Fecha: 2026-08-25
- Reemplaza la distribución documental definida implícitamente por ADR 0002.

#### Contexto

El corpus funcional y las guías de entrega estaban copiados en frontend, backend e IA. Aunque las copias nacieron idénticas, cada cambio exigía tres PR y podía producir versiones incompatibles para personas y agentes.

#### Decisión

Mantener toda documentación compartida y específica del sistema en `proyecto-gimnasio-documentacion`, sin duplicados entre repositorios. Cada repositorio de código conserva solamente:

- `README.md`, como entrada operativa y enlace a la fuente canónica;
- `AGENTS.md`, con instrucciones locales y la ruta de lectura del corpus central.

El repositorio documental publica `manifest.json` como mapa determinista para agentes. Toda pieza canónica tiene un identificador, una ruta única, un alcance y condiciones explícitas de carga.

#### Consecuencias

- Un cambio documental se revisa y versiona una sola vez.
- Los cambios de código y documentación que dependan entre sí usan PR relacionados.
- Trabajar sin acceso al repositorio documental no autoriza a reconstruir reglas por memoria ni a copiar documentos al repositorio de código.
- La validación automática rechaza enlaces rotos, documentos no registrados y contenido Markdown duplicado.


---

<a id="adr-0004"></a>

### ADR 0004 — LLM autohospedado sobre infraestructura del Polo

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0004-self-hosted-llm-server.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0004-SELF-HOSTED-LLM`

- Estado: aceptada
- Fecha: 2026-08-25

#### Contexto

RF-053 a RF-058, RF-075 y RF-108 requieren un servicio de generación de lenguaje. [D12/S-05](#d12) asume "un servicio de generación gratuito o de coste muy bajo con calidad suficiente" sin especificar si es un proveedor externo (API de terceros) o un modelo propio. La Universidad ofrece un servidor administrado por el Polo Educativo para este propósito.

#### Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | API de un proveedor externo (OpenAI, Anthropic, etc.) | Datos de condiciones físicas y hábitos de entrenamiento de los alumnos salen de la infraestructura de la Universidad hacia un tercero. Coste variable por token, dependiente de un servicio fuera de control del proyecto. Cumple S-05 ("servicio gratuito o de bajo coste") sólo si el proveedor ofrece nivel gratuito suficiente |
| (b) | **LLM autohospedado en el servidor del Polo Educativo** | Ningún dato de alumnos sale de la infraestructura de la Universidad. Coste de operación (no de API) asumido por la institución. Requiere que alguien administre el runtime |
| (c) | Sin componente generativo, todo por formulario estructurado | Cumple RF-058 como comportamiento normal en vez de como fallback, pero renuncia a RF-053 y RF-055 tal como están redactados, y a la propuesta de valor declarada en [D1 §3.0](#d1) sobre la interpretación de lenguaje natural |

#### Decisión

(b). El LLM corre autohospedado en el servidor del Polo Educativo.

#### Fundamento

RNF-21 ya exige que los datos de condiciones físicas, aptitud y mediciones sólo se traten con consentimiento explícito registrado; enviarlos a un proveedor externo de generación agrega una parte procesadora adicional que complica ese consentimiento y la trazabilidad de RNF-19. El self-hosting resuelve esto de raíz: el dato no sale del perímetro de la institución. Además, (a) hace que la disponibilidad y el coste del componente generativo dependan de un tercero fuera del control del proyecto, mientras que RF-058 ya asume que ese servicio puede no estar disponible — tener el servidor bajo administración propia (institucional) da más control sobre esa disponibilidad que un proveedor externo.

#### Consecuencias

- El equipo (o el Polo Educativo) debe operar, actualizar y monitorear un proceso de inferencia — trabajo no incluido en las 504 h de capacidad de construcción de [D12/§3](#d12); debe declararse como carga adicional real, coordinada con la institución.
- El hardware disponible es `NO VERIFICADO` al momento de esta decisión — ver [generative-ai.md §2](#arch-generative). El tamaño de modelo elegido debe ser configuración, no una decisión fija, hasta que se confirme.
- Se mantiene RF-058 como comportamiento de excepción (indisponibilidad puntual), no como comportamiento normal — a diferencia de la opción (c).
- Ver [ADR-0006](#adr-0006) para qué modelo y runtime corren sobre esta infraestructura.


---

<a id="adr-0005"></a>

### ADR 0005 — AI Gateway como módulo interno del backend

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0005-ai-gateway-in-process-module.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0005-AI-GATEWAY`

- Estado: **parcialmente reemplazada** por [ADR 0009](#adr-0009) el 2026-09-01
- Fecha: 2026-08-25

> **Qué queda reemplazado y qué no.** La **ubicación de despliegue** decidida aquí —opción (b), módulo dentro del monolito del backend— queda reemplazada: la ADR 0009 despliega el servicio generativo como un proceso Python propio con worker durable en el Polo, es decir la opción (c) que esta ADR descarta. El motivo es una restricción física que esta ADR no consideró: un intento de generación puede durar hasta 120 segundos y Vercel no sostiene una petición de esa duración.
>
> **El patrón sigue vigente:** puerto estable más adaptador reemplazable, con timeout, reintento, límite por usuario, validación de esquema, redacción de registros y versionado de prompt concentrados en un único punto. Lo que cambia es dónde vive ese punto, no que exista.
>
> **La advertencia de coste operativo sigue vigente y sin resolver:** operar un proceso adicional es trabajo que la capacidad de construcción del proyecto no contabiliza. Ver ADR 0009, «Puntos operativos pendientes».

#### Contexto

`Backend/AGENTS.md` ya instruye "encapsular LLM y recomendadores detrás de puertos/adaptadores", pero no especifica si ese puerto vive dentro del backend o como un servicio propio desplegado entre el backend y el LLM Server. Hace falta decidirlo antes de implementar RF-053 a RF-058.

#### Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | El backend llama al LLM Server directamente, sin capa intermedia | Timeout, reintento, límite, redacción de logs y validación de schema se dispersan en cada punto de llamada del backend, contradiciendo la instrucción ya vigente en `AGENTS.md` de encapsular esto |
| (b) | **AI Gateway como módulo interno del backend** (puerto + adaptador, dentro del mismo monolito modular) | Un único punto donde viven timeout, reintento, límite, validación de schema, redacción de logs y versionado de prompt. No agrega un servicio para desplegar ni operar |
| (c) | AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server | Mismas ventajas de encapsulamiento que (b), más la posibilidad de que otros consumidores (además del backend) lo usen — pero agrega un tercer proceso a desplegar, versionar y operar |

#### Decisión

(b). El AI Gateway es un módulo interno del backend (puerto `GenerativeAiPort` + adaptador `OllamaAdapter`), no un servicio desplegado por separado.

#### Fundamento

[D12/§3](#d12) ya muestra una capacidad de construcción de ~504 h contra un trabajo estimado de ~900 h — no hay margen para operar un tercer servicio (build, deploy, monitoreo, actualizaciones) sin sustento real de necesidad. ADR-0001 y ADR-0002 ya fijan la convención de monolito modular con un solo despliegue de backend, evitando microservicios que el presupuesto no justifica; agregar un Gateway desplegado aparte repite ese error que el propio proyecto ya evitó una vez para el backend en general. (a) se descarta porque ya existe la instrucción explícita de encapsular, y no seguirla dispersaría lógica transversal (timeout, rate limit, redacción, versión de prompt) en cada punto de llamada, dificultando tanto el cambio de modelo como la auditoría de RNF-19.

Ningún consumidor además del propio backend necesita al AI Gateway hoy: no hay integración con Telegram, WhatsApp ni ningún otro canal en el alcance de este proyecto (verificado contra D1-D13, sin resultados). Si eso cambiara, sería el disparador real para reconsiderar (c).

#### Consecuencias

- El AI Gateway comparte el ciclo de despliegue del backend: una actualización del Gateway es una actualización del backend, con el mismo `npm run check` y el mismo pipeline de PR.
- El puerto (`GenerativeAiPort`) es la interfaz estable; el adaptador (`OllamaAdapter`) es lo único que cambia si cambia el runtime o el modelo (ver [ADR-0006](#adr-0006)).
- **Camino de evolución declarado, no implementado ahora**: si en el futuro aparece un segundo consumidor del LLM (por ejemplo, una herramienta interna del Polo Educativo, o un canal de mensajería), o si la concurrencia real supera lo que el backend puede sostener llamando directo al LLM Server, se promueve el módulo a servicio desplegado sin cambiar el contrato del puerto — sólo su ubicación de despliegue.


---

<a id="adr-0006"></a>

### ADR 0006 — Modelo Qwen2.5-7B-Instruct sobre runtime Ollama

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0006-llm-model-and-runtime-selection.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0006-LLM-RUNTIME`

- Estado: aceptada, sujeta a revalidación cuando el hardware del servidor institucional esté verificado
- Fecha: 2026-08-25

#### Contexto

RF-053 a RF-058 necesitan un modelo de lenguaje self-hostable y un runtime que lo sirva. No se debía asumir de antemano que Llama o Qwen fueran la mejor opción; había que reunir evidencia sobre licencia, calidad en español, soporte de salida estructurada/tool calling y ecosistema de despliegue antes de elegir. La comparación completa está en [ai-model-selection.md](#arch-model-selection); este ADR registra la decisión y su fundamento.

#### Opciones de modelo

Qwen2.5/3 (7B-14B), Llama 3.1/3.3 (8B), Gemma 2/3 (9B-12B), Mistral 7B/Small. Comparadas en licencia, calidad en español/multilingüe, soporte de structured output/tool calling y ecosistema — ver tabla completa en [ai-model-selection.md §1](#arch-model-selection).

#### Opciones de runtime

Ollama, vLLM, llama.cpp. Comparadas en operación, uso de GPU, concurrencia y madurez de structured output/tool calling — ver tabla completa en [ai-model-selection.md §2](#arch-model-selection).

#### Decisión

**Modelo: Qwen2.5-7B-Instruct** (o 14B si el hardware verificado lo permite dentro del presupuesto de RNF-04), cuantizado GGUF.
**Runtime: Ollama.**

#### Fundamento

**Modelo.** Qwen2.5 en los tamaños ≤32B tiene licencia Apache 2.0 sin tope de uso ni política de contenido restringido; es la única de las cuatro familias evaluadas sin una zona de riesgo legal identificada para el contenido real que este sistema genera (condiciones físicas, pauta nutricional orientativa). Gemma, en cambio, incorpora una política de uso prohibido que restringe explícitamente la generación de contenido médico/de salud, con derecho de Google a restringir remotamente un uso que la viole — un riesgo real y no descartable sin revisión legal para este dominio, dado RF-057 y RF-075/RF-108. Llama 3.1 tiene una licencia utilizable para este proyecto (el tope de 700M MAU no aplica) pero es menos permisiva que Apache 2.0 y, según la evidencia relevada, rinde algo por detrás de Qwen en tareas no inglesas al mismo tamaño — un factor decisivo dado que este es un producto en español. Mistral queda como alternativa de respaldo con la misma licencia permisiva, sin evidencia de ventaja sobre Qwen en español.

**Runtime.** La carga esperada (estimada en [generative-ai.md §16](#arch-generative): del orden de cientos de llamadas por día) está muy por debajo del umbral donde, según la evidencia relevada, Ollama empieza a degradarse frente a vLLM (~5 usuarios concurrentes). Ollama resuelve mejor la restricción real de este proyecto: un equipo sin especialización en operación de modelos, sobre un hardware `NO VERIFICADO` que puede terminar siendo sólo CPU — Ollama corre en ambos casos con la misma integración, mientras que vLLM está pensado para GPU dedicada y agrega complejidad de configuración que no se traduce en beneficio a esta escala.

#### Consecuencias

- El modelo y su cuantización quedan fijados en configuración del AI Gateway ([ADR-0005](#adr-0005), desplegado según [ADR-0009](#adr-0009)), no hardcodeados, porque el hardware real del servidor institucional todavía no está verificado.
- Llama 3.1-8B queda documentado como segunda preferencia si la evaluación empírica sobre el conjunto de casos de [generative-ai.md §9](#arch-generative) lo justifica.
- Gemma no se adopta sin que antes exista una revisión legal explícita de su política de uso frente al contenido real generado por este sistema.
- Si la concurrencia real supera lo que Ollama sostiene bien, se reemplaza `OllamaAdapter` por `VllmAdapter` detrás del mismo puerto, sin tocar el resto del backend (ver [generative-ai.md §15](#arch-generative)).
- Esta decisión debe revisarse cuando el hardware del servidor del Polo Educativo se confirme, y periódicamente, dado el ritmo de publicación de estas familias de modelos.


---

<a id="adr-0007"></a>

### ADR 0007 — Sin RAG semántico, con prefiltrado determinista

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0007-no-rag.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0007-NO-RAG`

- Estado: aceptada, revisada
- Fecha: 2026-08-25 (revisión: mismo día, tras objeción sobre el tamaño del catálogo)

#### Contexto

RAG (indexar un corpus, recuperarlo por similitud semántica y dárselo al LLM como contexto) es una técnica habitual cuando un componente generativo necesita consultar conocimiento dinámico que no cabe ni conviene fijar en el prompt. Antes de descartarla o adoptarla había que determinar si alguno de los componentes generativos de este proyecto (RF-053 a RF-058, RF-075, RF-108, RF-119) tiene esa necesidad.

**Revisión de esta ADR**: la primera versión concluyó "no RAG" apoyándose sólo en que las enumeraciones cerradas de [D2 §4](#d2) son chicas, sin analizar el tamaño del catálogo de ejercicios — el otro conocimiento que el LLM necesita para RF-054/RF-119. Un catálogo prescribible de gimnasio (base + propio, filtrado por equipamiento) puede tener perfectamente decenas a un par de cientos de ejercicios, no es automáticamente "chico". Esta versión corrige ese análisis incompleto.

#### Análisis

Qué conocimiento necesita cada componente generativo, y de qué tamaño es:

| Componente | Conocimiento que necesita | Tamaño | ¿Es candidato a RAG semántico? |
| --- | --- | --- | --- |
| RF-053 · interpretación de NL | Las 12 enumeraciones cerradas de [D2 §4](#d2) | Fijo y pequeño (cientos de tokens) | No: entra completo en el prompt |
| RF-054/RF-119 · generación de rutina y candidato | El catálogo prescribible del gimnasio, y dentro de él las alternativas de un patrón de movimiento puntual | Variable, potencialmente no chico (decenas a cientos de ejercicios por gimnasio) | **No, pero por una razón distinta a "es chico"**: ver más abajo |
| RF-055, RF-056, RF-075/RF-108 · narrativos | Estructuras y valores ya calculados por el backend o el motor batch | Acotado por alumno | No: la entrada es exactamente el dato que hay que redactar, no algo que buscar |

**Por qué el catálogo tampoco necesita RAG semántico, a pesar de no ser trivialmente chico.** El problema de "qué ejercicios son válidos para esta rutina/este ejercicio a sustituir" no es un problema de búsqueda por similitud difusa — es un filtro **exacto** sobre atributos estructurados que el sistema ya calcula en código: patrón de movimiento pedido, compatibilidad con las condiciones del alumno (RN-44a-d), equipamiento presente en el inventario (RN-45). RN-46 exige que una incompatibilidad **impida** poner la rutina en vigencia — es una regla dura, no una preferencia. Un vector store resuelve por similitud aproximada, que es la herramienta equivocada para una condición que tiene que ser exacta y auditable.

La solución correcta no es "no hace falta ningún tipo de recuperación": es que el **backend prefiltra el catálogo de forma determinista antes de construir el prompt**, con el mismo código que ya exige RN-44a-d/RN-45 para la validación posterior. El LLM nunca ve el catálogo completo; ve el subconjunto ya compatible y ya acotado por patrón, que en la práctica queda en el orden de decenas de ejercicios por llamada — dentro del presupuesto de contexto de cualquiera de los modelos evaluados en [ai-model-selection.md](#arch-model-selection) sin dificultad.

#### Decisión

No se implementa RAG semántico (embeddings + vector store). El conocimiento que cada componente generativo necesita se entrega como contexto estructurado directo (JSON armado por el backend), y en el caso del catálogo, **prefiltrado de forma determinista** por el mismo código que ya hace cumplir RN-44a-d/RN-45, antes de construir el prompt — no el catálogo completo, no una búsqueda por similitud.

#### Fundamento

Adoptar RAG semántico sin necesidad real agrega un almacén vectorial, un pipeline de ingesta/chunking/embeddings y una etapa de recuperación (con su propio re-ranking, actualización y trazabilidad) a un proyecto con capacidad de construcción ya ajustada ([D12/§3](#d12)), para resolver un problema que un filtro SQL con `WHERE` ya resuelve de forma exacta, auditable y más barata de mantener — y que además hay que ejecutar de todas formas como validación determinista (RF-113), así que no ejecutarlo también como filtro previo sería trabajo duplicado, no ahorro. El prefiltrado determinista no es una alternativa más liviana a RAG: es la herramienta correcta para un problema de filtro exacto, mientras que RAG semántico está pensado para un problema de similitud aproximada que este proyecto no tiene.

#### Consecuencias

- El contexto de cada llamada generativa se arma en el backend con acceso directo a los datos transaccionales, no en una capa de recuperación separada.
- El catálogo que llega al prompt de `generarRutina`/`sugerirAlternativas` (ver [generative-ai.md §7](#arch-generative)) es siempre el subconjunto ya filtrado por patrón + compatibilidad + inventario, nunca el catálogo completo del gimnasio.
- **Umbral explícito de reapertura**: si el catálogo prescribible filtrado de un gimnasio (ya acotado, no el catálogo entero) creciera lo suficiente como para no entrar cómodo en el presupuesto de contexto del modelo elegido, corresponde reabrir esta decisión y evaluar recuperación semántica o paginación — no se espera que esto ocurra con equipamiento típico de gimnasio (22 valores de equipamiento, 9 patrones de movimiento — [D2 §4](#d2)), pero queda como condición de disparo explícita en vez de un "algún día" vago.
- Si en el futuro el sistema incorpora una base de conocimiento grande y no estructurada (por ejemplo, una biblioteca de metodología de entrenamiento en texto libre que el LLM deba consultar), esta decisión debe reabrirse explícitamente con su propio ADR — no debe agregarse RAG por extensión silenciosa de este diseño.


---

<a id="adr-0008"></a>

### ADR 0008 — Componentes clásicos como herramientas del LLM

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0008-tool-calling-for-ml-components.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0008-ML-TOOLS`

- Estado: **revisada** (2026-08-28) — ver la nota de revisión al final
- Fecha: 2026-08-25

#### Contexto

RF-059 (ranking de alternativas de sustitución) se invoca desde dentro del flujo de creación de rutina asistido por el LLM (FL-04/A4). Esto planteó una pregunta real: si ya se está usando un LLM para interpretar, generar y justificar la rutina, ¿no debería el mismo LLM también ordenar las alternativas de sustitución, en vez de mantener un componente clásico aparte? La misma pregunta aplica, con menos fuerza, a la segmentación de perfiles (RF-064).

#### Opciones

| | Opción | Consecuencia |
| --- | --- | --- |
| (a) | El LLM razona en lenguaje natural sobre el catálogo y produce el orden de alternativas él mismo | Un único componente para todo el flujo, pero pierde reproducibilidad exacta (RF-072/RNF-27), necesita de todas formas una re-validación determinista posterior (RF-060/RN-44a-d) porque no se puede confiar en que el LLM excluya correctamente lo contraindicado, y ata FL-06 (sustitución durante una sesión, sin lenguaje natural de por medio) a la disponibilidad del LLM Server sin necesidad |
| (b) | **El ranking se sigue calculando con el modelo/regla clásica ya descrita en `predictive-ai.md`, expuesto al LLM como una herramienta invocable (tool calling) durante FL-04, y llamado directamente por el backend en FL-06** | Un cálculo, dos formas de invocarlo. El LLM decide cuándo pedir alternativas; el modelo clásico calcula cuáles, de forma reproducible y ya validada |
| (c) | Dos implementaciones separadas y no relacionadas: una para el flujo generativo, otra para FL-06 | Duplica el mantenimiento de la misma lógica de negocio (RN-49a) en dos lugares, con riesgo real de que diverjan |

#### Decisión (original — parcialmente reemplazada, ver nota de revisión)

(b). El ranking de RF-059 (y, del mismo modo, la verificación de compatibilidad de RN-44a-d cuando se usa dentro del flujo generativo) se mantiene como cómputo clásico, expuesto al AI Gateway como una función que el LLM puede invocar mientras arma el candidato de rutina.

#### Fundamento

RF-060 exige excluir de forma dura los ejercicios contraindicados o de nivel superior — una condición que ya corre en código (RN-44a-d) y que, por RF-113, se re-valida sobre cualquier salida antes de mostrarla al usuario. Si el LLM también calculara el ranking, esa validación determinista tendría que ejecutarse de todas formas como red de seguridad — es decir, el costo del cómputo clásico ya está pagado sí o sí, y dejar que el LLM lo intente además no ahorra nada, sólo agrega una fuente más de variabilidad y una llamada más al modelo. RF-072/RNF-27 exigen reproducibilidad exacta a partir de versión y contexto guardado: un ranking por similitud sobre atributos estructurados (patrón de movimiento, participación muscular) es exactamente reproducible; un ranking producido por generación de lenguaje no lo es entre corridas ni entre versiones de modelo. Y RF-059 se usa también en FL-06 (sustitución durante una sesión en curso, sin lenguaje natural, con necesidad de responder rápido) — atarlo a la disponibilidad del LLM Server introduciría una dependencia que hoy no existe, contra RNF-11.

La pregunta que motivó esta ADR tiene una respuesta general, no sólo para RF-059: **la ubicación en el flujo (dónde se invoca) no determina la técnica que resuelve el problema (cómo se calcula)**. Un LLM con tool calling maduro (ya elegido en [ADR-0006](#adr-0006) también por esta razón) permite que ambas cosas convivan: el modelo de lenguaje orquesta la conversación y decide cuándo necesita un dato o un cálculo; los componentes especializados —deterministas o de ML clásico— siguen siendo la fuente de ese dato o cálculo.

#### Consecuencias

- El AI Gateway expone `verificarCompatibilidad` como herramienta invocable además de los métodos de generación/interpretación/redacción ya descritos en `generative-ai.md §5`. Ver `generative-ai.md §7` para el contrato completo.
- Ningún componente de compatibilidad se reimplementa dentro de un prompt.

---

#### Nota de revisión (2026-08-28) — replanteo de IA

Tras el replanteo de alcance de IA ([D11/DD-34](#d11)), **la parte de esta ADR referida al ranking de RF-059 se reemplaza por la opción (a)**: el orden de las alternativas de sustitución lo produce ahora la capa generativa (`sugerirAlternativas`, `generative-ai.md §5.4`), no un modelo clásico. Motivos del cambio de contexto:

- Ya no existe un modelo/regla clásica de ranking en `predictive-ai.md` que exponer — construirlo y mantenerlo era costo que el proyecto decidió no asumir (S-03, capacidad de 504 h).
- Se acepta la pérdida de reproducibilidad **exacta**: RF-059 pasa al estándar de "validez repetida" del resto de la capa generativa (`generative-ai.md §10`), y RF-072/RNF-27 se cumplen **persistiendo la lista producida**, no reejecutándola.
- FL-06 (sustitución en sesión) pasa a invocar el LLM, con el orden determinista de RN-49a como fallback cuando el LLM no responde (RN-99). Esto amplía la superficie de dependencia del LLM Server — declarado como consecuencia asumida en DD-34 y D12/§4.

**Lo que de esta ADR sigue vigente sin cambios:** `verificarCompatibilidad` como herramienta determinista invocable, la exclusión dura de RN-44a-d en código, y el principio de que "dónde se invoca ≠ cómo se calcula" para los componentes que sí son deterministas (compatibilidad, diagnóstico, ajustes, estructura).


---

<a id="adr-0009"></a>

### ADR 0009 — Servicio generativo online en el Polo

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/decisions/adr/0009-servicio-generativo-online-en-el-polo.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `ADR-0009`

- Estado: aceptada
- Fecha: 2026-08-29 (renumerada el 2026-09-01)

#### Nota de renumeración

Esta ADR se emitió con el número 0004, ya ocupado por [ADR 0004: LLM autohospedado sobre infraestructura del Polo Educativo](#adr-0004). Eran dos decisiones distintas con el mismo identificador. Se renumera a **0009** conservando su fecha y su contenido. Relación con las otras dos ADR del mismo dominio:

- **ADR 0004 (LLM autohospedado)** sigue vigente y es complementaria: decide *dónde corre el modelo* —infraestructura del Polo, no un proveedor externo—. Esta ADR decide *qué proceso lo orquesta y dónde vive ese proceso*.
- **[ADR 0005 (AI Gateway como módulo interno del backend)](#adr-0005) queda reemplazada en su parte de ubicación de despliegue.** Aquella descartó explícitamente la opción «(c) AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server», que es exactamente lo que esta ADR decide. La contradicción existió con ambas en estado «aceptada» desde el 2026-08-29; se resuelve a favor de esta.

##### Por qué prevalece esta ADR sobre la 0005

El fundamento de la ADR 0005 es un presupuesto de esfuerzo: no hay capacidad para operar un tercer servicio. El de esta ADR es una restricción física: un intento de generación puede durar hasta 120 segundos y Vercel no sostiene una petición de esa duración, de modo que hace falta un proceso durable fuera de la función serverless. Un presupuesto se renegocia; la restricción no.

**Lo que de la ADR 0005 sigue vigente y se adopta aquí:** el patrón puerto y adaptador. Timeout, reintento, límite por usuario, validación de esquema, redacción de registros y versionado de prompt viven en un único punto —ahora dentro del servicio Python, no del backend— y el conector hacia el modelo es un adaptador reemplazable sin tocar el resto.

**Lo que la ADR 0005 advertía y sigue siendo cierto:** operar API, worker, modelo y agente ngrok en el Polo es trabajo de operación que la capacidad de construcción del proyecto no contabiliza. Ver los puntos operativos pendientes al final de este documento.

#### Contexto

El alcance generativo v2.1 asigna a un LLM la interpretación de pedidos, la selección del tipo de rutina, la construcción de una rutina completa, la explicación y la oferta de alternativas. El LLM ya se ejecuta en infraestructura del Polo. Por políticas de red, el código Python también puede desplegarse allí, pero su API debe exponerse mediante ngrok.

La arquitectura anterior describía `proyecto-gimnasio-ia` únicamente como motor batch, sin HTTP, y exigía una construcción determinística cuando el proveedor generativo fallaba. Esas dos restricciones son incompatibles con el alcance confirmado.

#### Decisión

`proyecto-gimnasio-ia` tendrá dos límites ejecutables independientes:

1. un **servicio generativo online** Python, con API HTTP versionada y worker asíncrono, desplegado en el Polo;
2. trabajos analíticos y predictivos batch, fuera del camino de las peticiones.

El servicio Python orquesta el LLM del Polo; el LLM no es el servicio de orquestación ni accede a PostgreSQL. Ngrok publica únicamente la API Python mediante un dominio HTTPS estable.

```text
React -> Express/Vercel -> ngrok -> API Python/Polo -> LLM/Polo
              |                       |
              +------ Neon <----------+
```

##### Flujo asíncrono

1. El frontend solicita la generación al backend.
2. El backend autoriza, minimiza el contexto y persiste una solicitud con identificador idempotente.
3. El backend llama al servicio Python, que acepta con `202` sin esperar al LLM.
4. Un worker reclama la solicitud persistida, llama al LLM y escribe el resultado en estructuras de integración designadas.
5. El frontend consulta el estado exclusivamente al backend.
6. El backend valida esquema, catálogo, compatibilidad y rangos; sólo entonces crea un candidato.
7. Ninguna rutina entra en vigencia sin revisión favorable de un entrenador.

Cada intento puede durar como máximo 120 segundos. Una salida inválida o un fallo técnico admite un único reintento. Tras el segundo fallo la generación queda `NO_DISPONIBLE`; no se construye una rutina determinística. El resto del sistema y la creación manual por entrenadores continúan. Los presets quedan como alcance opcional y no son una dependencia de esta contingencia.

##### Contratos y autoridad

- IA es dueña del OpenAPI del servicio de orquestación y del conector privado hacia el LLM.
- Backend genera o valida su cliente desde una versión explícita de ese OpenAPI.
- Backend es dueño de Prisma, las migraciones, las estructuras de integración y todas las reglas de negocio.
- El servicio IA sólo accede a estructuras de integración expresamente autorizadas; no crea, aprueba, asigna ni activa rutinas.
- Backend e IA se despliegan independientemente. Los cambios incompatibles usan una versión nueva y compatibilidad temporal.

##### Datos y credenciales

El Polo recibe únicamente el contexto necesario: identificador técnico, objetivo, nivel, frecuencia, condiciones físicas pertinentes, equipamiento, catálogo permitido y preferencias confirmadas. No recibe nombre, correo, teléfono, documento ni credenciales, y los logs no guardan prompts completos ni datos de salud.

Una única API y configuración del modelo atienden inicialmente test y producción. Credenciales de consumo diferentes seleccionan conexiones PostgreSQL diferentes, configuradas en el servidor; ninguna petición suministra una URL de base. El authtoken de ngrok, las credenciales backend–IA y las credenciales IA–LLM son secretos distintos.

Los resultados aceptados conservan contexto mínimo y versiones para auditoría. Solicitudes abandonadas, respuestas inválidas y fallos se eliminan a los 30 días. Los casos de regresión se anonimizan antes de conservarse.

##### Ambientes

- Frontend y backend locales usan Neon Test y la credencial test del servicio IA.
- No se implementa un adaptador `fake` ejecutable. Los tests pueden reemplazar el transporte HTTP o el conector LLM con dobles de prueba.
- `test` despliega el ambiente estable de prueba; `main`, producción.
- Neon Test y Neon Producción no comparten base ni credenciales.

#### Consecuencias

- Se reemplazan las restricciones batch-only de ADR 0002 para el repositorio IA; el pipeline analítico batch permanece vigente.
- DD-31 deja de asignar la construcción inicial de rutinas a una tabla determinística: RN-39a y la compatibilidad pasan a ser barreras de validación, no el generador principal.
- RF-058, RF-113, RNF-04, RNF-11 y RNF-18 dejan de exigir fallback determinístico para generación.
- Ngrok y la disponibilidad de la máquina del Polo pasan a ser dependencias operativas. Un dominio estable, reinicio automático y monitoreo son requisitos de producción.
- El servicio online exige un proceso API y un worker durable; no se ejecuta el LLM dentro de una petición de Vercel ni como tarea de fondo no durable.
- Un cambio de modelo, prompt o parámetros requiere evaluación de regresión y validación de al menos un entrenador antes de producción.

#### Puntos operativos pendientes

Antes del primer despliegue real deben confirmarse el contrato y autenticación del LLM, la capacidad de ejecutar servicios permanentes en el Polo, el plan de ngrok con dominio estable y el mecanismo de instalación y rollback del código Python. Estos puntos no cambian la frontera decidida.


---

<a id="parte-viii"></a>

## Parte VIII — Planificación

<a id="d12"></a>

### D12 — Riesgos y supuestos

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/planning/risks-and-assumptions.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `D12`

|                |                 |
| -------------- | --------------- |
| **Versión**    | 3.0             |
| **Fecha**      | 2026-09-01      |
| **Estado**     | Normativo       |
| **Depende de** | D1, D5, D8, D11 |

**Cambios de la v1.0:** §1.1 registra **todas** las constantes numéricas del sistema con su origen, que en la v1.0 aparecían en D5 como si fueran datos del dominio · riesgos nuevos R-15 y R-16 · §5 actualizada: de las seis inconsistencias abiertas quedan dos, y ninguna es bloqueante.

**Cambios de la v2.0:** §1.1 registra la constante del tope de regeneraciones del candidato de rutina (RN-127).

**Cambios de la v3.0 ([baseline de alcance](#baseline)):** cuatro riesgos nuevos derivados del recorte de alcance · R-03 cerrado · §3 recalculada sobre el alcance de la Etapa 1 · §4 reemplazada por el orden de retirada por bandas · **I-09**, una inconsistencia sobre la propia capacidad que conviene resolver antes de usar §3 para negociar alcance.

---

#### 1. Supuestos

| ID       | Supuesto                                                                                                                                                                                     | Origen                                                                                            | Impacto si es falso                                                                                                                                                                                                                                                  |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **S-01** | El equipo es de 9 personas y dispone de aproximadamente 14 semanas                                                                                                                           | El cliente escribió "somos 3 personas" y a continuación listó 9 nombres con rol; se tomó la lista | **Crítico.** Con 3 personas ningún conjunto MUST de este corpus es alcanzable y hay que rehacer el alcance desde D1                                                                                                                                                  |
| **S-02** | La dedicación efectiva ronda las 10 h semanales por persona                                                                                                                                  | Análisis inicial                                                                                  | **Muy alto.** Ver §3                                                                                                                                                                                                                                                 |
| **S-03** | Existe una fuente de datos externa con historial de entrenamiento por usuario y por serie a lo largo del tiempo                                                                              | Sin verificar                                                                                     | **Alto.** Los conjuntos públicos de gimnasio suelen ser de afluencia o catálogos de ejercicios, no historiales longitudinales por persona. Si no existe, la generación simulada (RF-071) es la única vía y la estimación de riesgo queda con la limitación declarada |
| **S-04** | La caracterización del problema de D1/§1 y §2 corresponde a la realidad de un gimnasio                                                                                                       | Análisis interno, sin contraste                                                                   | **Alto y barato de verificar.** Una conversación con un entrenador en ejercicio confirma o refuta la premisa de todo el producto                                                                                                                                     |
| **S-05** | El Polo permite operar el LLM, la API Python, el worker y un túnel ngrok estable con disponibilidad suficiente para test y producción                                                        | Decisión del cliente; verificación operativa pendiente                                             | **Alto.** Si falla API, worker, túnel o máquina, la generación se deshabilita y permanecen las plantillas privadas y la creación manual por entrenadores                                                                                                            |
| **S-06** | Es aplicable la legislación argentina de protección de datos personales, que trata la información de salud como dato sensible                                                                | Decisión del cliente                                                                              | **Bajo en diseño, alto en presentación.** El corpus ya incorpora consentimiento, minimización y anonimización                                                                                                                                                        |
| **S-07** | Un gimnasio tiene una única zona horaria y no opera en varias sedes                                                                                                                          | Inferido de la exclusión de sucursales                                                            | **Bajo.** Si es falso, cambia la definición de día y de semana                                                                                                                                                                                                       |
| **S-08** | La cátedra no exige nutrición, metodología ni entregables concretos                                                                                                                          | Confirmado sólo respecto de tecnologías                                                           | **Medio.** Puede invalidar el alcance de DD-13 y la forma de los entregables                                                                                                                                                                                         |
| **S-09** | El catálogo externo permite su uso y redistribución en las condiciones del proyecto, y contiene o permite derivar el equipamiento requerido y las articulaciones exigidas por cada ejercicio | Las fuentes citan licencias sin verificación                                                      | **Alto.** Si la fuente no trae equipamiento ni articulaciones, hay que curarlas a mano y RF-099 crece de forma sustancial. Verificar **antes** de la carga inicial                                                                                                   |
| **S-10** | La taxonomía muscular de 17 grupos y la de 8 articulaciones son suficientes para expresar las contraindicaciones que un alumno declara en la práctica                                        | Convención de este proyecto                                                                       | **Medio-alto.** Si un alumno necesita declarar algo que no entra en las 25 zonas corporales, la contraindicación no se calcula y la compatibilidad falla en silencio. Verificar con un entrenador real                                                               |

##### 1.1 Constantes del sistema y su origen

Registro completo de las constantes que D5 fija. `[F]` proviene de una fuente · `[S]` es una convención de este proyecto, **sin fuente externa y discutible con el cliente**. Las marcadas `[S]` son las que hay que poner sobre la mesa en la primera conversación con un entrenador en ejercicio.

| Constante                                           | Valor                                             | Regla         | Origen                                                                      |
| --------------------------------------------------- | ------------------------------------------------- | ------------- | --------------------------------------------------------------------------- |
| Vencimiento de la invitación                        | 14 días                                           | RN-02b        | `[S]`                                                                       |
| Caducidad del enlace de recuperación                | 2 horas                                           | RN-06         | `[S]`                                                                       |
| Expiración de sesión de usuario                     | 30 días                                           | RN-07         | `[S]`                                                                       |
| Aviso previo de vencimiento de aptitud              | 30 días                                           | RN-13b        | `[S]`                                                                       |
| Rango de peso corporal                              | 20,0 – 400,0 kg                                   | RN-17         | `[S]`                                                                       |
| Rango de altura                                     | 100 – 250 cm                                      | RN-17         | `[S]`                                                                       |
| Rango de perímetros                                 | 10,0 – 250,0 cm                                   | RN-17         | `[S]`                                                                       |
| Días de rutina                                      | 1 – 7                                             | RN-41         | `[S]`                                                                       |
| Repeticiones prescriptas                            | 1 – 100                                           | RN-43         | `[S]`                                                                       |
| Descanso                                            | 0 – 600 s                                         | RN-43         | `[S]`                                                                       |
| **Tabla completa de derivación del tipo de rutina** | Ver RN-39a                                        | RN-39a        | `[S]` — **la de mayor impacto de toda la lista**                            |
| Correspondencia severidad → impide/advierte         | MODERADA y SEVERA impiden                         | RN-44b        | `[S]`                                                                       |
| Criterio de nivel                                   | El ejercicio no puede superar el nivel del alumno | RN-44c        | `[S]`                                                                       |
| Cierre de sesión por inactividad                    | 8 horas                                           | RN-53         | `[F]` análisis inicial                                                      |
| Rango de carga registrada                           | 0,00 – 1.000,00 kg                                | RN-55         | `[S]`                                                                       |
| Umbral de registro atípico                          | 150% del mejor histórico                          | RN-55a        | `[S]`                                                                       |
| Plazo de corrección de sesión                       | 48 horas                                          | RN-58         | `[F]` análisis inicial                                                      |
| Plazo de desbloqueo excepcional                     | 24 horas, una vez                                 | RN-58a        | `[S]`                                                                       |
| Antigüedad máxima de sesión diferida                | 90 días                                           | RN-59         | `[S]`                                                                       |
| Ponderación primaria / secundaria                   | 1,0 / 0,5                                         | RN-62         | `[F]` análisis inicial                                                      |
| Tope de repeticiones para estimar carga máxima      | 12                                                | RN-65         | `[S]`                                                                       |
| Mínimo para calcular adherencia                     | 2 semanas                                         | RN-68         | `[S]`                                                                       |
| Umbral de estancamiento                             | variación < +2,5% en 6 semanas, ≥ 4 sesiones      | RN-74, RN-74a | `[S]`                                                                       |
| Umbral de caída de adherencia                       | 25 puntos porcentuales                            | RN-75         | `[S]`                                                                       |
| Rango de referencia de volumen                      | 6 – 22 series efectivas semanales                 | RN-76         | `[F]` análisis inicial                                                      |
| Periodicidad del diagnóstico                        | 2 semanas                                         | RN-78         | `[S]`                                                                       |
| **Tabla completa de criterios de diagnóstico**      | Ver RN-79a                                        | RN-79a        | `[S]`                                                                       |
| **Tabla completa de reglas de ajuste**              | Ver RN-89a                                        | RN-89a        | `[S]` — **junto con RN-39a, lo que más conviene validar con un entrenador** |
| Incremento de carga                                 | +2,5%, mínimo 2,50 kg                             | RN-89a        | `[S]`                                                                       |
| Reducción de carga                                  | −10%                                              | RN-89a        | `[S]`                                                                       |
| Umbral de adherencia para reducir frecuencia        | 60% en 4 semanas                                  | RN-89a        | `[S]`                                                                       |
| Caducidad de propuesta                              | 30 días                                           | RN-87         | `[S]`                                                                       |
| ~~Periodicidad de la estimación de riesgo~~ ⏸        | semanal                                           | RN-100        | `[S]`                                                                       |
| Caducidad de avisos                                 | 90 días                                           | RN-113        | `[S]`                                                                       |
| Plazo de anonimización                              | 7 días                                            | RN-106        | `[S]`                                                                       |
| Rango de ingesta proteica                           | 1,6 – 2,2 g/kg                                    | RN-120        | `[S]`                                                                       |
| Tope de regeneraciones de un candidato de rutina    | 3                                                 | RN-127        | `[S]`                                                                       |

**Lectura de esta tabla.** De 37 constantes, 4 provienen del análisis inicial y **33 son convenciones adoptadas por este proyecto**. Ninguna es un dato del dominio verificado. Las tres tablas —derivación del tipo, criterios de diagnóstico y reglas de ajuste— concentran el riesgo: si están mal, el sistema funciona y prescribe mal, que es peor que fallar.

#### 2. Riesgos

| ID       | Riesgo                                                                                 | Prob.        | Impacto      | Mitigación concreta                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------- | -------------------------------------------------------------------------------------- | ------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R-01** | El conjunto MUST no entra en el plazo                                                  | **Muy alta** | **Muy alto** | **Sigue en Muy alta después del recorte.** El alcance bajó de 97 a 80 requisitos (–18 %), pero lo que se retiró es barato y lo que se confirmó es el ciclo central. La banda N1 sola está entre 0,9 × y 1,4 × la capacidad (§3). Conversación de alcance con el cliente **antes de escribir código**, con §4 sobre la mesa. Punto de control formal al cierre del Sprint 3 |
| **R-02** | El ciclo de adaptación resulta más costoso de lo previsto                              | Media ⬇      | Muy alto     | Las tablas RN-79a y RN-89a lo vuelven un motor de reglas construible y testeable de forma aislada. El riesgo bajó de alta a media al escribirlas                                                                                                                                                                                                                                                                                                            |
| ~~R-03~~ | ~~La estimación de riesgo se queda sin datos reales~~                                  | —            | —            | **Cerrado.** RF-061 a RF-063 se retiraron del alcance en [DD-34](#d11) y la votación lo confirmó: 1, 0 y 0 votos de 8. Sin componente no hay riesgo                                                                                                                                                             |
| **R-04** | Un error en las decisiones de modelado de D4 se descubre tarde                         | Media        | **Muy alto** | Congelar D4 y D5 antes de la primera línea de código. Las decisiones críticas son DD-02, DD-03, DD-04 y DD-26                                                                                                                                                                                                                                                                                                                                               |
| **R-05** | La pantalla de registro de sesión resulta más difícil de lo previsto                   | Alta         | Alto         | Es el flujo de mayor frecuencia y el que produce el contexto del que depende toda la inteligencia. Prototiparla temprano y probarla en un teléfono real                                                                                                                                                                                                                                                                                                     |
| **R-06** | El recurso gráfico de la representación muscular no llega a tiempo                     | Media        | Medio        | Encargarlo temprano sobre los 17 grupos de D2/§4.2. Alternativa definida: barras por grupo muscular                                                                                                                                                                                                                                                                                                                                                         |
| **R-07** | La clasificación muscular importada es pobre y distorsiona el volumen                  | Media        | **Alto**     | RF-099: curación manual de los ejercicios más frecuentes. Un volumen mal calculado corrompe el diagnóstico y con él todas las propuestas                                                                                                                                                                                                                                                                                                                    |
| **R-08** | Los componentes generativos producen salidas inválidas de forma recurrente             | Media        | Alto         | RF-113 y RN-95b: ninguna salida inválida llega al usuario; un reintento y luego indisponibilidad. Medir rechazo, edición, invalidez y cuántas veces hay que recurrir a una plantilla manual; validar cada cambio con dataset fijo y un entrenador                                                                                                                                     |
| **R-09** | Congestión de la puerta: el entrenador no revisa a tiempo                              | Media        | **Alto**     | Consecuencia directa de DD-25. RF-112, priorización de lo pendiente en la cartera (RF-107) e indicador E1b. Si el tiempo de revisión crece, hay que informarlo, no absorberlo                                                                                                                                                                                                                                                                               |
| **R-10** | Participación desigual entre nueve personas                                            | Alta         | Alto         | Demostración interna semanal de software funcionando; cada persona dueña de al menos una funcionalidad de complejidad real                                                                                                                                                                                                                                                                                                                                  |
| **R-11** | Integración tardía entre las partes                                                    | Media        | Alto         | Un recorrido completo desplegado en las primeras semanas; contrato entre capas acordado y congelado temprano                                                                                                                                                                                                                                                                                                                                                |
| **R-12** | Fallo el día de la demostración                                                        | Baja         | Muy alto     | Congelamiento con antelación; entorno alternativo probado; grabación de respaldo. **El aprovisionamiento (RF-115) tiene que estar probado**: sin él no hay gimnasio y no hay demostración                                                                                                                                                                                                                                                                   |
| **R-13** | Exámenes de otras materias consumen dos semanas                                        | **Muy alta** | Medio        | Ya descontado en §3. Debe estar descontado también en el plan                                                                                                                                                                                                                                                                                                                                                                                               |
| **R-14** | El coste o la capacidad del servicio de generación resulta insuficiente                 | Media        | Medio        | Límite por usuario, idempotencia, métricas de latencia y concurrencia, un reintento máximo. ✎ **Ya no hay presets de contingencia obligatorios** (RF-021 pasó a alcance opcional): la contingencia es una plantilla del entrenador, que alguien tiene que haber cargado antes — ver R-17                                                                                             |
| **R-15** | **El inventario del gimnasio se declara mal o queda desactualizado**                   | **Alta**     | **Alto**     | Consecuencia directa de DD-26: el inventario determina el catálogo prescribible de todo el gimnasio. Un inventario incorrecto no produce un error visible, produce rutinas silenciosamente inservibles. Mitigación: RN-118 advierte al administrador cuando el inventario no cubre los patrones mínimos, y RN-117 reevalúa las rutinas ante cada cambio. **No hay mitigación técnica para un inventario que declara equipamiento que el gimnasio no tiene** |
| **R-16** | **La expectativa sobre el LLM excede su autoridad real**                               | Media        | Alto         | Se agrava con el recorte: al diferirse los presets, el modelo pasa a ser la única vía automática de creación. DD-31 y ADR 0009: el LLM construye el candidato, pero no evita catálogo, compatibilidad, rangos ni aprobación. Demostrar esa frontera y medir cuánto corrige o rechaza el entrenador                                                                                                                                                                                                           |
| **R-17** 🆕 | **La prescripción depende por completo del servicio generativo**                       | **Alta**     | **Muy alto** | Consecuencia directa de diferir RF-021 sin construir un generador determinístico. Sin servicio y sin plantillas cargadas, **un alumno nuevo no obtiene ninguna rutina** y la capacidad C1 deja de cumplirse (RNF-42). Mitigación: cargar plantillas de arranque por gimnasio en el aprovisionamiento y medir la disponibilidad real del Polo desde el Sprint 1. **No hay mitigación técnica dentro del alcance recortado.** Ver [DD-35](#d11) |
| **R-18** 🆕 | **Contradicción arquitectónica descubierta al integrar**                              | Media ⬇      | **Alto**     | Las ADR 0005 y 0009 estuvieron ambas «aceptadas» decidiendo lo contrario sobre dónde vive el servicio de IA. **Resuelto el 2026-09-01**: prevalece la 0009 y la 0005 queda parcialmente reemplazada. Queda el riesgo residual de que alguien implemente contra la versión vieja del corpus |
| **R-19** 🆕 | **La adherencia se mide sesgada y nadie lo declara**                                  | Media        | Medio        | Sin registro diferido (RF-034, 2 votos de 8), una sesión no cargada el mismo día se pierde para siempre. La adherencia —insumo de RN-89a global y del criterio de urgencia— queda sesgada a la baja. **Mitigación: declararlo en la presentación del indicador y en la defensa.** No corregirlo en silencio |
| **R-20** 🆕 | **Un ejercicio propio mal cargado no se puede retirar**                               | Media        | Bajo         | Sin RF-018 (0 votos) no hay desactivación. Acotado al ámbito de un gimnasio y corregible por su autor. Deuda aceptada |

#### 3. Aritmética del esfuerzo

```
9 personas × 10 h/semana × 14 semanas                  = 1.260 h nominales
− curva de aprendizaje y puesta en marcha      (≈10%)  =  −126 h
− coordinación, reuniones e integración        (≈15%)  =  −189 h
− exámenes, feriados e imprevistos             (≈15%)  =  −189 h
──────────────────────────────────────────────────────────────────
Presupuesto efectivo de trabajo                        ≈  756 h
```

De las 9 personas, **3 no construyen funcionalidades** según esta versión del cálculo: dirección de proyecto (Lorenzatti) y calidad (Grasso, Vignolo). Su trabajo es real y necesario, pero no produce requerimientos.

```
Capacidad de construcción ≈ 6/9 × 756                  ≈  504 h
Composición: 1 líder técnico + 2 desarrolladores senior + 3 junior
```

> ⚠️ **Este descuento está en disputa. Ver I-09 en §5.** El Documento de Planificación e Inicio §1.3 afirma lo contrario con todas las letras —«los roles de gestión no son de dedicación exclusiva: **todos los integrantes participan en la construcción del software**»— y asigna a las tres personas a equipos verticales con alcance funcional. Entre 504 h y 756 h hay un 50 % de diferencia. **Es el denominador de toda esta sección y de la conversación de alcance de R-01.**

##### Contraste con el alcance de la Etapa 1

Sobre el alcance del [baseline](#baseline): 80 requisitos, de los cuales 57 son banda N1.

| Conjunto     | Requisitos | Optimista (8 h) | Realista (10–12 h) | Frente a ~504 h | Frente a ~756 h |
| ------------ | ---------- | --------------- | ------------------ | --------------- | --------------- |
| N1           | 57         | ~456 h          | 570 – 684 h        | 0,9 × a 1,4 ×   | 0,6 × a 0,9 ×   |
| N1 + N2      | 76         | ~608 h          | 760 – 912 h        | 1,2 × a 1,8 ×   | 0,8 × a 1,2 ×   |
| N1 + N2 + N3 | 80         | ~640 h          | 800 – 960 h        | 1,3 × a 1,9 ×   | 0,8 × a 1,3 ×   |

**Conclusión.** Con 504 h, ni siquiera el núcleo entra con holgura y el alcance completo está entre 1,3 y 1,9 veces por encima. Con 756 h, el núcleo entra y el alcance completo queda al límite. **La diferencia entre «hay que recortar el núcleo» y «hay que trabajar ordenado» depende de un dato que ningún documento midió** — y que el equipo tiene.

El promedio de 8 a 12 h por requisito además subestima tres subsistemas: el Módulo 15 (adaptación), la ejecución de sesiones y la representación de indicadores. No son requisitos: son pantallas y motores completos.

#### 4. Orden de retirada

Escrito de antemano para que la decisión ya esté tomada cuando llegue el momento. **Sustituye al orden de corte de la v2.1**, que se escribió antes de que existiera la clasificación por bandas.

**Nunca se recorta la banda N1.** Son los 57 requisitos sin los cuales el producto no cumple lo que el cliente declaró condición de aprobación: alta e invitación · inventario y catálogo prescribible · contexto del alumno con sus condiciones · plantillas, copia al asignar y versionado · compatibilidad y rutina inicial · registro de sesiones y series · indicadores de base · el ciclo de diagnóstico y adaptación completo · la puerta del entrenador · generación y su comportamiento ante fallo.

**Orden de retirada, de primero a último:**

**Antes de esta lista.** RF-021 (presets) ya es `COULD` y está fuera del alcance comprometido: si el cronograma no permite implementarlo, no se retira nada — simplemente no se construye, sin degradar ningún requisito `MUST`. Lo mismo vale para todo lo marcado ⏸ DIFERIDO en D8: **ya está fuera de la cuenta de §3.**

| #  | Se retira                                    | Queda en su lugar                                   | Banda |
| -- | -------------------------------------------- | ----------------------------------------------------- | ----- |
| 1  | RF-067 · estado de membresía                 | Nada. Es informativo y no condiciona nada            | N3    |
| 2  | RF-064 · descripción del perfil              | Nada                                                 | N3    |
| 3  | RF-052 · indicadores agregados de la cartera | La cartera priorizada de RF-036                      | N3    |
| 4  | RF-017 y RF-100 · catálogo propio            | Sólo el catálogo base                                | N3/N2 |
| 5  | RF-093 · historial de adaptaciones           | Las versiones de rutina siguen consultables          | N2    |
| 6  | RF-044 · récords personales                  | La evolución por ejercicio de RF-050                 | N2    |
| 7  | RF-045 · media móvil de mediciones           | La serie sin suavizado                               | N2    |
| 8  | RF-072 y RF-073 · trazabilidad y evaluación  | La justificación de RF-090. **Se pierde el criterio de éxito E9** | N2 |
| 9  | RF-031 · ajustes durante la sesión           | Registro secuencial de lo prescripto                 | N2    |
| 10 | RF-014 · búsqueda y filtrado                 | Listado completo del catálogo                        | N2    |
| 11 | RF-053 · interpretación de lenguaje natural  | Formulario de parámetros estructurados. **Requiere liberar el compromiso ante el Product Owner** (I-10) | N2 |

**A partir de acá se degrada la banda N1, y cada paso exige acuerdo explícito del cliente:**

| #  | Se degrada                                | A qué                                                                                          |
| -- | ----------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 12 | RF-055 · explicación en lenguaje natural  | Presentación tabulada del criterio y los datos. Conserva la condición C5 del acta, pierde la capa narrativa |
| 13 | RF-054 y RF-087 · generación              | Creación manual por entrenadores desde sus plantillas; **no se conserva una generación automática equivalente**. Es renunciar a la IA como núcleo, que el cliente declaró centro del producto |
| 14 | RF-049 · representación muscular          | Barras por grupo muscular                                                                       |
| 15 | RF-050 · evolución por ejercicio          | Sólo carga máxima estimada                                                                      |
| 16 | RF-088 a RF-094 · ciclo de adaptación     | Nada. **Es entregar un producto que no es el que el cliente pidió, y hay que decirlo con esas palabras** |

Del paso 12 en adelante, lo que se entrega deja de responder a la condición de aprobación declarada por el cliente. No es un recorte de alcance: es un cambio de producto.

#### 5. Inconsistencias no resueltas

| #        | Inconsistencia                                                                  | Estado                                                                            |
| -------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **I-09** 🆕 | **La capacidad de construcción está calculada sobre un supuesto que otra fuente contradice.** §3 descuenta a tres personas y llega a ~504 h; el Documento de Planificación e Inicio §1.3 dice que las nueve construyen y les asigna alcance funcional en equipos verticales | **Abierta y de alto impacto.** Es el denominador de R-01 y de PD-01. Ninguna de las dos fuentes es evidentemente correcta: hay que **medir la disponibilidad real que declara cada integrante**, no elegir el documento que convenga. Resolver antes de la conversación de alcance |
| I-01     | El cliente escribió "somos 3 personas" y listó 9                                | **Abierta.** Se tomó la lista. Confirmación pendiente (S-01)                      |
| I-06     | `READAPTACION` quedó fuera de los tipos de rutina por sus implicancias clínicas | **Abierta, de bajo riesgo.** Decidido en DD-27; requiere confirmación del cliente |
| I-07     | Creación segura de migraciones sin modificar Neon Test compartida               | **Abierta.** Elegir PostgreSQL efímero local o una base shadow separada antes de la primera migración |
| I-08     | Operación productiva del servicio IA en el Polo mediante ngrok                  | **Abierta.** Confirmar dominio estable, servicios permanentes, contrato LLM y mecanismo de instalación/rollback. **Quién opera esos cuatro procesos es trabajo no contabilizado en §3** |
| **I-10** 🆕 | **RF-053 obtuvo 3 votos de 8 pero está comprometido por escrito ante el Product Owner** (`deliverable PO/alcance-ia-generativa.md` v2.1) | **Abierta.** Una votación interna no revoca un compromiso asumido. O el Product Owner lo libera, o se construye pese al voto. Se conserva en alcance mientras tanto |
| ~~I-11~~ | ~~Dos ADR con el número 0004, decidiendo cosas incompatibles~~                  | **Cerrada el 2026-09-01.** La del servicio del Polo se renumera a ADR 0009 y la ADR 0005 queda parcialmente reemplazada en su parte de ubicación de despliegue |
| ~~I-12~~ | ~~DD-34 citada por ocho documentos y nunca redactada~~                          | **Cerrada el 2026-09-01.** Escrita en D11 v2.2 |
| ~~I-02~~ | Forma de la generación nutricional                                              | **Cerrada** en DD-13: pauta orientativa sin nombrar alimentos                     |
| ~~I-03~~ | Alerta ante valores atípicos                                                    | **Cerrada** en RN-55a                                                             |
| ~~I-04~~ | Situación de estímulo insuficiente                                              | **Cerrada**: incorporada como quinta situación (RN-79a) con su regla de ajuste    |
| ~~I-05~~ | Taxonomía muscular canónica                                                     | **Cerrada** en D2/§4.2 y §4.3. Queda el supuesto S-10 sobre su suficiencia        |


---

<a id="baseline"></a>

### Baseline de alcance — Vivaz Adaptive · Etapa 1

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/planning/baseline-alcance-2026-09.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `PLAN-BASELINE`

|                          |                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Versión**              | 4.0                                                                                                                                  |
| **Fecha**                | 2026-09-01                                                                                                                           |
| **Estado**               | Propuesta de baseline. Requiere validación del equipo y conversación de alcance con el cliente (§P/PD-01)                            |
| **Reemplaza**            | La clasificación de alcance de [D8](#d8) v3.3 y el plan de sprints del Acta de Redefinición §5 |
| **Autoritativo para**    | Alcance de la etapa, trazabilidad de la votación, orden de construcción y deuda documental                                            |
| **No autoritativo para** | El enunciado de los requisitos (sigue siendo D8), las reglas (D5), el modelo (D4) ni los estados (D6)                                 |

**Fuentes.** `Documento_Planificacion_Inicio_Proyecto.docx` (baseline documental, 81 RF) · `Acta Redefinicion.docx` (redefinición del núcleo por el cliente, con las cuatro respuestas del equipo ya registradas) · `Lista de Requisitos.xlsx` (votación de 8 de 9 integrantes sobre RF-001..RF-081, más RF-082..RF-094 agregados sin votar) · el corpus documental completo · los tres repositorios de código.

---

#### A. Resumen ejecutivo

**Vivaz Adaptive es un sistema que mantiene la prescripción de entrenamiento de cada alumno adecuada a su estado, y que somete cada cambio a la aprobación de un entrenador.** No es un registrador de entrenamientos con analítica encima: el registro, los indicadores y los tableros existen porque sin ellos no hay diagnóstico, y sin diagnóstico no hay adaptación fundamentada.

Tres hechos gobiernan esta versión del baseline:

1. **El cliente declaró la adaptación como condición de aprobación.** «Si no está, el proyecto no se aprueba». Todo lo demás es negociable; esto no.
2. **La votación del equipo redujo el alcance, pero menos de lo que parece.** De 97 requisitos en alcance en D8 v3.3 se pasa a **80 en la Etapa 1**: 19 diferidos, 6 absorbidos por fusión y 4 degradados a regla. La votación no contradijo el núcleo — recortó la periferia (nutrición, comentarios, paneles agregados, riesgo de abandono, parametrización) y confirmó por unanimidad práctica el ciclo central. Lo que recortó cuesta poco; lo que confirmó cuesta casi todo.
3. **Nada del dominio está implementado.** Los tres repositorios contienen andamiaje: Express con `/health` y `/ready`, un `schema.prisma` sin modelos, una SPA con una pantalla de bienvenida y un paquete Python vacío. Toda la funcionalidad de este documento es diseño, no software.

**El alcance sigue por encima de la capacidad.** 80 requisitos, de los cuales 57 son núcleo, contra ~504 h de capacidad de construcción. La banda N1 sola consume entre el 90 % y el 140 % del presupuesto; el conjunto completo, entre el 130 % y el 190 % (§D.4). La aritmética de [D12/§3](#d12) no cierra ni siquiera con este recorte. Este documento entrega la decisión ya preparada: tres bandas de alcance y un orden de retirada escrito de antemano, para que el recorte sea una decisión y no un accidente de la semana 12.

**Y el denominador de esa cuenta está en duda.** Las ~504 h suponen que tres de las nueve personas no construyen software; el Documento de Planificación afirma lo contrario con todas las letras. Resolver esa contradicción cambia la conversación de alcance antes de tenerla (§M/I-09).

---

#### B. Nuevo alcance funcional, en prosa

Un gimnasio se afilia mediante una operación externa a la aplicación que crea el gimnasio y su primer administrador. Ese administrador declara **qué equipamiento tiene el gimnasio** —dato crítico, no cosmético: determina qué puede prescribirse a todo el mundo— e invita nominalmente a entrenadores y alumnos. Nadie se registra por su cuenta.

Un alumno que acepta su invitación declara su perfil, su objetivo y sus condiciones físicas mediante un formulario tabulado de categorías cerradas, cada una con zona corporal y severidad. Puede cargar su aptitud deportiva; el sistema advierte si falta o venció, pero no bloquea. Registra mediciones corporales fechadas.

Con ese contexto —y sin ningún historial— **el sistema genera su rutina completa**: elige el tipo de rutina compatible con su objetivo, la construye sobre el catálogo prescribible de su gimnasio (los ejercicios cuyo equipamiento está efectivamente en el inventario), y verifica que ningún ejercicio esté contraindicado por una condición vigente. La rutina nace **propuesta**, no vigente. Un entrenador con asignación vigente la revisa y la aprueba. Sin esa aprobación no rige. Sin excepciones, cualquiera sea el origen de la rutina.

El alumno entrena. Al iniciar una sesión, el sistema **congela la prescripción del día dentro de la propia sesión**: lo que se indicó y lo que se hizo conviven en la misma fila, y la sesión de hoy no cambia porque la rutina cambie mañana. Registra carga, repeticiones y, si quiere, esfuerzo percibido. Puede sustituir un ejercicio, agregar u omitir series. Reanuda una sesión interrumpida; si no vuelve, se cierra sola.

De ese registro el sistema deriva volumen y frecuencia por grupo muscular, capacidad máxima estimada por ejercicio, adherencia sobre ventana móvil, cumplimiento de series y de repeticiones, y récords personales. Con eso detecta estancamiento, caída de adherencia y desbalance.

**Cada dos semanas el sistema evalúa la rutina vigente** y asigna a cada ejercicio y al conjunto una de cinco situaciones. Si corresponde, elabora una **propuesta de adaptación**: ajuste de carga, de volumen, de esquema, sustitución de un ejercicio o cambio de estructura. Cada ajuste lleva el criterio que lo motiva y el dato que lo sustenta. La propuesta se verifica contra las condiciones del alumno y los rangos de su tipo de rutina antes de presentarse, y **el entrenador la acepta entera, la acepta en parte o la rechaza**. Aceptarla genera una versión nueva de la rutina; las anteriores se conservan y las sesiones ya ejecutadas no se tocan.

Un cambio de objetivo, la aparición o el cierre de una condición física, el vencimiento de la aptitud o **un cambio del inventario del gimnasio** disparan la reevaluación inmediata: el sistema marca los ejercicios que dejaron de ser compatibles sin retirarlos, avisa, y elabora la propuesta correspondiente.

El entrenador ve su cartera ordenada por urgencia —primero lo que espera su revisión, después incompatibilidades, estancamiento y caída de adherencia— y la ficha consolidada de cada alumno. El alumno ve su panel de progreso, su evolución por ejercicio y sus mediciones, y toda vista **declara qué información le falta en lugar de mostrar un cero**.

##### Lo que este alcance deliberadamente ya no incluye

Ninguna forma de nutrición. Ningún comentario ni mensajería. Ningún panel analítico del gimnasio. Ninguna estimación de riesgo de abandono. Ningún preset publicado ni catálogo de preajustes. Ninguna solicitud de rutina iniciada por el alumno. Ninguna representación muscular sobre esquema corporal —el mismo dato se presenta como barras por grupo muscular—. Ningún registro diferido de sesiones pasadas. Ninguna parametrización de reglas de cálculo. Ninguna baja de cuenta con portabilidad y anonimización (§P/PD-02).

---

#### C. Capacidades del producto

Ocho áreas de capacidad estructuran el sistema. La columna «D1» las mapea contra las capacidades centrales ya declaradas en [D1/§3](#d1), que no cambian.

| #     | Área de capacidad            | Qué garantiza                                                                                                                                                          | D1     |
| ----- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| CAP-1 | **Ámbito y acceso**          | Un gimnasio existe, sus usuarios entran sólo por invitación, y cada operación se autoriza por rol *y* por relación con el recurso concreto                              | —      |
| CAP-2 | **Contexto del alumno**      | El sistema sabe quién es la persona, qué se propone y qué no puede hacer — la entrada de todo componente de decisión                                                    | C2     |
| CAP-3 | **Catálogo prescribible**    | El conjunto de ejercicios efectivamente ejecutables en *este* gimnasio, clasificados de forma que la compatibilidad sea calculable                                      | C2     |
| CAP-4 | **Prescripción**             | Una rutina existe, tiene tipo, es coherente con el objetivo, es compatible con la persona, y evoluciona por versiones sin destruir el pasado                            | C1, C2 |
| CAP-5 | **Ejecución registrada**     | Lo prescripto y lo ejecutado conviven en la misma sesión, y la sesión es inmune a los cambios posteriores de la rutina                                                  | —      |
| CAP-6 | **Evidencia**                | El registro plano se convierte en indicadores y señales verificables, y toda vista declara lo que le falta                                                              | C3     |
| CAP-7 | **Adaptación fundamentada**  | La evolución se diagnostica sola y produce una propuesta acotada, justificada y compatible                                                                              | C3, C4 |
| CAP-8 | **La puerta del entrenador** | Ninguna rutina rige ni cambia sin aprobación humana, y el entrenador sabe a quién atender primero                                                                       | C5     |

**Cómo se relacionan.** CAP-1 habilita todo. CAP-2 y CAP-3 son las dos entradas de CAP-4: sin contexto no hay a quién prescribir, sin catálogo prescribible no hay con qué. CAP-5 produce el sustrato de CAP-6, y CAP-6 el de CAP-7. CAP-8 es la salida obligatoria de CAP-4 y de CAP-7 — es el único punto por el que un cambio llega al alumno.

**Dependencia crítica no obvia.** CAP-4 depende de la disponibilidad del servicio generativo con una fuerza que el corpus actual no declara. Ver §F.4 y §G/DEP-04.

---

#### D. Regla de corte aplicada y alcance resultante

##### D.1 La regla y sus tres excepciones

La regla base es: **≥ 5 votos = candidato al alcance de la Etapa 1**. Votaron 8 de 9 integrantes (Vioti no registró votos), de modo que 5 es mayoría estricta de quienes votaron y 8 es unanimidad.

Tres conjuntos entran sin votación, y hay que decir por qué:

- **RF-082 a RF-094** se agregaron a la planilla *después* de la reunión con el cliente y nunca se votaron. Entran por **autoridad del cliente**, no por voto: son la funcionalidad que el cliente declaró condición de aprobación. Someterlos a votación habría sido un error de proceso.
- **RF-095 a RF-122** no existían cuando se votó: los produjo el análisis posterior del corpus. Entran únicamente si son **dependencia técnica necesaria** de algo aprobado, y cada uno se justifica individualmente en §G. Los que no lo son, salen.
- **Requisitos con menos de 5 votos que son dependencia necesaria** de uno aprobado. No se reincorporan como funcionalidad independiente: se absorben, se subordinan o se declaran dependencia.

##### D.2 Resultado

| Categoría                                                          | Cantidad |
| ------------------------------------------------------------------ | -------- |
| Aprobados por votación (≥ 5), sobrevivientes tras las fusiones      | 40       |
| Incorporados por autoridad del cliente (RF-082..094)               | 13       |
| Dependencias necesarias reincorporadas o derivadas                 | 26       |
| Conservados por compromiso ante el Product Owner (RF-053)          | 1        |
| **En alcance — Etapa 1**                                           | **80**   |
| Absorbidos por fusión (RF-004, RF-023, RF-032, RF-033, RF-060, RF-107) | 6    |
| Fuera de esta etapa (diferidos)                                    | 19       |
| Fuera de alcance (firme)                                           | 14       |
| Degradados a regla, criterio o restricción                         | 4        |

> **Corrección de la primera emisión.** La versión inicial de este documento declaró 68 requisitos en alcance. Era un error de recuento: se contaron las 18 entradas `DEP-xx` de §G como si fueran 18 identificadores, cuando seis de ellas agrupan dos o tres (`DEP-04` = RF-058 + RF-113, `DEP-06` = RF-005 + RF-069, `DEP-09` = RF-071 + RF-106, `DEP-11` = RF-114 + RF-118, `DEP-12` = RF-115 + RF-116 + RF-100, `DEP-15` = RF-112 + RF-109). Las tablas de §D.3 siempre enumeraron el conjunto correcto. **El recorte real es 97 → 80, no 97 → 68**, y el contraste con la capacidad es peor de lo que se declaró. Ver §D.4.

##### D.3 Alcance de la Etapa 1, por área de capacidad

Los identificadores son los de [D8](#d8) y **no se renumeran**: 122 identificadores están referenciados de forma cruzada en veinte documentos del corpus y en los `AGENTS.md` de los tres repositorios de código. Renumerarlos destruiría trazabilidad existente a cambio de nada. La normalización se hace por **absorción declarada** (§E) y por reorganización en capacidades, no por renumeración.

Banda: **N1** núcleo, no se recorta · **N2** comprometido · **N3** condicionado al hito del Sprint 3.

###### CAP-1 · Ámbito y acceso

| RF     | Requisito                                              | Votos | Origen        | Banda |
| ------ | ------------------------------------------------------ | ----- | ------------- | ----- |
| RF-115 | Aprovisionamiento del gimnasio, externo a la aplicación | —     | Dependencia   | N1    |
| RF-116 | Alta exclusivamente por invitación                     | —     | Cliente N-26  | N1    |
| RF-001 | Completar la cuenta desde una invitación               | 8     | Votación      | N1    |
| RF-002 | Autenticación y gestión de sesión                      | 8     | Votación      | N1    |
| RF-003 | Recuperación y cambio de credenciales                  | 8     | Votación      | N2    |
| RF-005 | Autorización por rol **y** por relación con el recurso | 2     | Dependencia   | N1    |
| RF-069 | Ámbito de la información por gimnasio                  | 4     | Dependencia   | N1    |
| RF-065 | Gestión de cuentas, roles e invitaciones               | 8 ⊕ 6 | Votación (F5) | N1    |
| RF-066 | Asignación entrenador–alumno con historial             | 2     | Dependencia   | N1    |
| RF-112 | Señalar alumnos sin entrenador y bloquear lo pendiente | —     | Dependencia   | N2    |
| RF-109 | Transferir lo pendiente al entrenador entrante         | —     | Dependencia   | N2    |
| RF-067 | Estado de membresía, informativo                       | 8     | Votación      | N3    |

###### CAP-2 · Contexto del alumno

| RF     | Requisito                                         | Votos | Origen      | Banda |
| ------ | ------------------------------------------------- | ----- | ----------- | ----- |
| RF-007 | Perfil del alumno                                 | 8     | Votación    | N1    |
| RF-008 | Objetivo vigente con historial de vigencia        | 8     | Votación    | N1    |
| RF-009 | Condiciones físicas con zona corporal y severidad | 8     | Votación    | N1    |
| RF-085 | Historial de vigencia de las condiciones          | —     | Cliente     | N1    |
| RF-084 | Aptitud con vencimiento; advierte, no bloquea     | —     | Cliente     | N2    |
| RF-010 | Mediciones corporales fechadas                    | 8     | Votación    | N1    |
| RF-111 | Determinar y exponer si hay contexto suficiente   | —     | Dependencia | N2    |
| RF-096 | Consentimiento explícito para datos de salud      | —     | Dependencia | N2    |

###### CAP-3 · Catálogo prescribible

| RF     | Requisito                                                       | Votos | Origen       | Banda |
| ------ | --------------------------------------------------------------- | ----- | ------------ | ----- |
| RF-013 | Catálogo de ejercicios consultable                              | 8     | Votación     | N1    |
| RF-014 | Búsqueda y filtrado                                             | 8     | Votación     | N2    |
| RF-015 | Información descriptiva y recurso visual                        | 8     | Votación     | N2    |
| RF-016 | Clasificación muscular primaria/secundaria y articulaciones     | 8     | Votación     | N1    |
| RF-099 | Taxonomía canónica cerrada y curación manual de los frecuentes  | —     | Dependencia  | N1    |
| RF-070 | Carga inicial repetible desde fuente externa                    | 8     | Votación     | N1    |
| RF-114 | Inventario de equipamiento del gimnasio                         | —     | Cliente N-27 | N1    |
| RF-118 | Catálogo prescribible = catálogo ∩ inventario                   | —     | Dependencia  | N1    |
| RF-100 | Catálogo base global frente al catálogo propio del gimnasio     | —     | Dependencia  | N2    |
| RF-017 | Incorporación de ejercicios por entrenadores                    | 5     | Votación     | N3    |

###### CAP-4 · Prescripción

| RF     | Requisito                                                              | Votos | Origen       | Banda |
| ------ | ---------------------------------------------------------------------- | ----- | ------------ | ----- |
| RF-019 | Plantillas estructuradas en días y ejercicios                          | 8     | Votación     | N1    |
| RF-020 | Prescripción de series, rangos, carga sugerida y descanso              | 6     | Votación     | N1    |
| RF-022 | Copia profunda e independiente al asignar                              | 0     | Dependencia  | N1    |
| RF-024 | Frecuencia semanal objetivo dentro del rango del tipo                  | 2     | Dependencia  | N1    |
| RF-026 | Una vigente y una propuesta como máximo; archivado consultable         | 6     | Votación     | N1    |
| RF-082 | Tipo de rutina y derivación de estructura, esquemas y rangos           | —     | Cliente N1   | N1    |
| RF-083 | Correspondencia entre tipo de rutina y objetivo                        | —     | Cliente      | N1    |
| RF-086 | Verificación de compatibilidad, con regla explícita de correspondencia | —     | Cliente N4   | N1    |
| RF-087 | Generación de la rutina inicial sin historial previo                   | —     | Cliente N6   | N1    |
| RF-092 | Versionado de la rutina adaptada                                       | —     | Cliente      | N1    |
| RF-110 | Revisión y aprobación explícita antes de toda vigencia                 | —     | Cliente N-14 | N1    |

###### CAP-5 · Ejecución registrada

| RF     | Requisito                                                          | Votos     | Origen        | Banda |
| ------ | ------------------------------------------------------------------ | --------- | ------------- | ----- |
| RF-027 | **Ciclo de vida de la sesión**: inicio, curso, reanudación y cierre | 8 ⊕ 3 ⊕ 7 | Votación (F1) | N1    |
| RF-028 | Congelamiento de la prescripción dentro de la sesión               | 5         | Votación      | N1    |
| RF-029 | Registro por serie de lo prescripto y lo ejecutado                 | 8         | Votación      | N1    |
| RF-030 | Precarga con la última ejecución del alumno                        | 1         | Dependencia   | N1    |
| RF-031 | Agregar, omitir y sustituir durante la sesión                      | 6         | Votación      | N2    |
| RF-035 | Historial de sesiones con comparación prescripto/ejecutado         | 8         | Votación      | N1    |

###### CAP-6 · Evidencia

| RF     | Requisito                                               | Votos | Origen      | Banda |
| ------ | ------------------------------------------------------- | ----- | ----------- | ----- |
| RF-040 | Volumen y frecuencia por grupo muscular                 | 8     | Votación    | N1    |
| RF-041 | Capacidad máxima estimada por ejercicio                 | 8     | Votación    | N1    |
| RF-042 | Adherencia sobre ventana móvil de cuatro semanas        | 5     | Votación    | N1    |
| RF-043 | Cumplimiento de series y de repeticiones                | 0     | Dependencia | N1    |
| RF-046 | Señales: estancamiento, caída de adherencia, desbalance | 7     | Votación    | N1    |
| RF-044 | Récords personales                                      | 6     | Votación    | N2    |
| RF-045 | Evolución de mediciones con media móvil                 | 8     | Votación    | N2    |
| RF-048 | Panel de progreso del alumno                            | 8     | Votación    | N2    |
| RF-050 | Evolución por ejercicio                                 | 8     | Votación    | N2    |
| RF-051 | Comportamiento explícito ante información insuficiente  | 7     | Votación    | N1    |
| RF-052 | Indicadores agregados de la cartera                     | 8     | Votación    | N3    |
| RF-064 | Descripción del perfil de comportamiento, efímera       | 6     | Votación    | N3    |

###### CAP-7 · Adaptación fundamentada

| RF     | Requisito                                                            | Votos | Origen        | Banda |
| ------ | -------------------------------------------------------------------- | ----- | ------------- | ----- |
| RF-088 | Diagnóstico periódico con cinco situaciones y precedencia definida    | —     | Cliente N7    | N1    |
| RF-089 | Propuesta de adaptación por tabla explícita situación → ajuste        | —     | Cliente N8    | N1    |
| RF-090 | Criterio y datos que sustentan cada ajuste                           | —     | Cliente N8    | N1    |
| RF-091 | Aprobación total, parcial o rechazo por el entrenador                | —     | Cliente N9    | N1    |
| RF-094 | Reevaluación por cambio de objetivo, condición, aptitud o inventario | —     | Cliente N13   | N1    |
| RF-059 | Alternativas admisibles de sustitución, con exclusión dura           | 8 ⊕ 2 | Votación (F3) | N1    |
| RF-093 | Historial de adaptaciones aplicadas                                  | —     | Cliente N10   | N2    |

###### CAP-8 · La puerta del entrenador y la generación

| RF     | Requisito                                                        | Votos | Origen        | Banda |
| ------ | ---------------------------------------------------------------- | ----- | ------------- | ----- |
| RF-036 | Cartera priorizada, con criterio de urgencia único y ordenado    | 5 ⊕ — | Votación (F4) | N1    |
| RF-037 | Ficha consolidada del alumno                                     | 8     | Votación      | N1    |
| RF-038 | Intervención del entrenador sobre la rutina, con autoría y aviso | 7 ⊕ 1 | Votación (F2) | N1    |
| RF-054 | Generación asíncrona del candidato de rutina                     | 8     | Votación      | N1    |
| RF-055 | Explicación en lenguaje natural de los criterios aplicados       | 8     | Votación      | N1    |
| RF-057 | Restricciones sobre el contenido generado                        | 0     | Dependencia   | N1    |
| RF-058 | Continuidad ante indisponibilidad de la generación               | 1     | Dependencia   | N1    |
| RF-113 | Descarte de salida inválida, un reintento, luego no disponible   | —     | Dependencia   | N1    |
| RF-053 | Interpretación de lenguaje natural a parámetros estructurados    | 3     | **Compromiso PO** | N2 |
| RF-095 | Avisos dentro de la aplicación, con enumeración cerrada          | —     | Dependencia   | N2    |

###### Transversales de datos

| RF     | Requisito                                                    | Votos | Origen                     | Banda |
| ------ | ------------------------------------------------------------ | ----- | -------------------------- | ----- |
| RF-071 | Generación e identificación de datos simulados               | 3     | Dependencia                | N1    |
| RF-106 | Excluir los simulados de toda analítica presentada como real | —     | Dependencia                | N1    |
| RF-072 | Versión, contexto e instante de toda salida inteligente      | 0     | Dependencia                | N2    |
| RF-073 | Evaluación reproducible de los componentes generativos       | 0     | Dependencia (transformado) | N2    |

**Reparto por banda:** N1 = 57 · N2 = 19 · N3 = 4. **Total en alcance: 80.**

##### D.4 El contraste con la capacidad, recalculado

La banda N1 sola tiene 57 requisitos. Con el promedio optimista de 8 h por requisito que usa [D12/§3](#d12) son ~456 h; con el realista de 10 a 12 h, entre 570 y 684 h. **La capacidad de construcción declarada es ~504 h.**

| Conjunto        | Requisitos | Optimista (8 h) | Realista (10–12 h) | Frente a ~504 h |
| --------------- | ---------- | --------------- | ------------------ | --------------- |
| N1              | 57         | ~456 h          | 570 – 684 h        | 0,9 × a 1,4 ×   |
| N1 + N2         | 76         | ~608 h          | 760 – 912 h        | 1,2 × a 1,8 ×   |
| N1 + N2 + N3    | 80         | ~640 h          | 800 – 960 h        | 1,3 × a 1,9 ×   |

**Lectura honesta:** el núcleo solo cabe si todo sale bien y nada más se construye. El alcance completo no cabe. Es la misma conclusión de D12, con la mejora de que ahora el corte ya está trazado por banda y no hay que improvisarlo.

**Y hay una incertidumbre sobre el denominador que conviene resolver antes de discutir el numerador** — ver §M/I-09: el propio cálculo de las ~504 h se apoya en un supuesto que el Documento de Planificación contradice.

---

#### E. Fusiones y normalización semántica

##### E.1 Fusiones aceptadas

| #  | Fusión                    | Resultado | Qué se conserva                                                                                                                                                                                                                                                                                                    | Origen                                               |
| -- | ------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| F1 | RF-027 ⊕ RF-032 ⊕ RF-033  | RF-027    | Las tres transiciones del mismo autómata (D6/§4): iniciar con un día del ciclo e impedir dos en curso; conservar estado y reanudar; cerrar por inactividad; finalizar con duración e incorporar al historial. Se conservan como criterios de aceptación separados                                                   | Sugerida por el equipo (RF-32/33), ampliada a RF-027 |
| F2 | RF-023 ⊕ RF-038           | RF-038    | Modificar ejercicios, series, repeticiones, cargas y descansos de un alumno concreto sin afectar la plantilla ni a otros alumnos, **más** autoría, instante y aviso. Resuelve además la brecha de votos (1 frente a 7) sobre la misma operación                                                                     | Análisis                                             |
| F3 | RF-059 ⊕ RF-060           | RF-059    | El orden de alternativas **y** la exclusión dura de lo contraindicado o de nivel superior. RF-060 no era un requisito: era la restricción de seguridad sobre la salida de RF-059                                                                                                                                    | Análisis                                             |
| F4 | RF-036 ⊕ RF-107           | RF-036    | La cartera ordenada **y** la definición del orden de urgencia. RF-107 se creó porque RF-036 no era verificable sin él; separados producían una dependencia circular ya señalada en D8                                                                                                                               | Análisis                                             |
| F5 | RF-004 (planilla) → RF-065 | RF-065   | «Gestión de roles» (8 votos en la planilla) y «Gestión de usuarios y roles» (6 votos) son el mismo requisito. Los 8 votos se imputan a RF-065. La observación del equipo sobre **dos interfaces distintas por rol, con un conmutador**, se conserva como criterio de aceptación de la experiencia por rol            | Sugerida por el equipo                               |

##### E.2 Fusiones rechazadas, con fundamento

| Fusión sugerida         | Decisión        | Fundamento                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RF-054 ⊕ RF-055         | **Rechazada**   | Son las dos clases de componente inteligente que [D11/DD-14](#d11) separa deliberadamente. RF-054 **decide** (produce estructura y valores, se valida contra compatibilidad y rangos, pasa por el entrenador). RF-055 **narra** (no puede introducir ningún número ausente de su entrada, RN-94, exigible al 100 % y verificable de forma automática). Fusionarlos borra la frontera donde vive la garantía de que el texto no miente, y deja sin sujeto a RNF-24 |
| RF-005 → RF-004/RF-065  | **Rechazada**   | RF-065 responde «qué rol tiene esta persona»; RF-005 responde «¿este recurso concreto le pertenece o le está asignado?». Es el doble filtro RA-01, la mitigación de R-11 y el sujeto de RNF-14, que exige una prueba por cada operación con identificador de alumno. Absorberlo en la gestión de roles haría desaparecer la verificación por recurso, que es exactamente el defecto de seguridad más frecuente en sistemas de este tipo |
| RF-088 ⊕ RF-089         | **Rechazada**   | Un diagnóstico sin propuesta es un resultado válido y frecuente (RN-89a/restricción 4, FL-09/A1), no un fallo. Son dos salidas persistidas con fechas, versiones y modos de fallo distintos. Fusionarlas obligaría a inventar una «propuesta vacía»                                                                                                                                                                             |
| RF-021 → RF-020         | **Sin efecto**  | RF-021 sale del alcance (§F). La observación del equipo queda resuelta por vía de exclusión, no de fusión                                                                                                                                                                                                                                                                                                                       |

##### E.3 Degradaciones: de requisito a regla, criterio o restricción

Cuatro elementos del corpus estaban escritos como requisitos funcionales sin serlo. Se conservan íntegros como normas verificables; dejan de contarse como alcance funcional.

| RF     | Pasa a ser                                           | Dónde vive                                                     |
| ------ | ---------------------------------------------------- | -------------------------------------------------------------- |
| RF-098 | Restricción de integridad — ya existe como **RI-01** | [D4/§4](#d4)                             |
| RF-102 | Convención transversal de unidades y precisión       | [D2/§3](#d2) más validación de servidor     |
| RF-103 | Convención transversal de tiempo (UTC, semana única) | [D2/§3](#d2)                                |
| RF-104 | Criterio de aceptación de RF-029; ya es **RNF-13**   | [D9/§3](#d9)        |

---

#### F. Requerimientos excluidos y diferidos

##### F.1 Salen por votación

| RF     | Requisito                              | Votos | Consecuencia y compensación                                                                                                                                                                                             |
| ------ | -------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-011 | Perfil del entrenador                  | 4     | El alumno ve el nombre de su entrenador, no su presentación profesional. Sin efecto sobre el ciclo                                                                                                                       |
| RF-012 | Estimación energética orientativa      | 2     | Con RF-074, RF-075 y RF-108 fuera, **la nutrición desaparece por completo de esta etapa**. Coincide con el orden de recorte de D12/§4                                                                                    |
| RF-074 | Indicador nutricional diario           | 1     | —                                                                                                                                                                                                                        |
| RF-018 | Curación y desactivación de ejercicios | 0     | Un ejercicio propio mal cargado no se puede retirar. Mitigación: RF-017 es de ámbito de gimnasio y su autor puede corregirlo. **Deuda aceptada**, registrada en §M/R-20                                                  |
| RF-101 | Ejercicio desactivado en rutina vigente | —    | Cae con RF-018: sin desactivación no hay caso                                                                                                                                                                            |
| RF-021 | Publicación y reutilización de presets | 1     | Ver §F.4 — es la exclusión de mayor impacto arquitectónico                                                                                                                                                               |
| RF-025 | Solicitud de rutina por el alumno      | 3     | La rutina la origina el entrenador o la generación inicial automática (RF-087). C1 se sigue cumpliendo. Arrastra a RF-119 y RF-120                                                                                       |
| RF-119 | Candidato de rutina ajustable          | —     | **Deroga [DD-33](#d11) para esta etapa.** Sin solicitud del alumno no hay solicitante que ajuste. Retira RN-124 a RN-129 y el flujo FL-03                                                    |
| RF-120 | Diferencia visible para el revisor     | —     | Cae con RF-119: el entrenador revisa la salida del componente sin capa intermedia                                                                                                                                       |
| RF-034 | Registro y corrección diferidos        | 2     | Una sesión no registrada el mismo día se pierde. **Sesga la adherencia a la baja** — hay que declararlo al presentar el indicador. Arrastra a RF-117                                                                     |
| RF-117 | Desbloqueo de sesión                   | —     | Cae con RF-034. El plazo de corrección vuelve a ser absoluto, con el costo de CB-70                                                                                                                                     |
| RF-039 | Comentarios asincrónicos               | 1     | No hay canal entrenador↔alumno salvo los avisos de RF-095                                                                                                                                                                |
| RF-047 | Parametrización de reglas de cálculo   | 3     | Las constantes quedan documentadas en D12/§1.1 y fijadas en código                                                                                                                                                      |
| RF-049 | Representación muscular sobre esquema  | 4     | **Degradado, no eliminado:** el mismo dato (RF-040) se presenta como barras por grupo muscular dentro de RF-048. Elimina el riesgo R-06 y la dependencia del recurso vectorial. Requiere confirmación del cliente (§P/PD-08) |
| RF-056 | Resumen narrado del progreso           | 4     | Ya lo había sustituido la justificación de la propuesta (RF-090), más específica y verificable                                                                                                                          |
| RF-068 | Panel analítico del gimnasio           | 2     | El administrador conserva gestión, no analítica                                                                                                                                                                          |
| RF-006 | Baja de cuenta y portabilidad          | 0     | **Diferido con riesgo legal declarado** — ver §P/PD-02. Arrastra a RF-105                                                                                                                                               |
| RF-097 | Auditoría general                      | —     | **Reducida**, no eliminada: se conserva la trazabilidad puntual de RF-038, RF-066, RF-091 y RF-114                                                                                                                       |

##### F.2 Ya estaban fuera y se confirman

RF-061, RF-062 y RF-063 (riesgo de abandono, WON'T desde v3.3; 1, 0 y 0 votos — la votación confirma la decisión) · RF-076 base de alimentos · RF-077 mensajería · RF-078 pagos · RF-079 video propio · RF-080 representación tridimensional · RF-081 dispositivos de monitorización · RF-075 y RF-108 pauta nutricional, que caen con RF-012.

##### F.2b RF-053 se conserva pese a no alcanzar el corte, y por qué

La interpretación de lenguaje natural obtuvo **3 de 8 votos**. Bajo la regla base debería salir, y la primera emisión de este documento la sacó. Esa decisión no se sostiene.

`deliverable PO/alcance-ia-generativa.md` v2.1, del 2026-08-28, dice literalmente qué se entrega al Product Owner: «**Entiende un pedido en lenguaje natural.** El entrenador o el alumno describen lo que necesitan con sus palabras y el sistema lo traduce a parámetros concretos, que se muestran para confirmar antes de usarlos», y encabeza esa lista con «qué nos comprometemos a entregar. **El alcance comprometido es un piso**». Es un compromiso escrito ante el Product Owner, no una aspiración interna.

**Una votación interna de 3 de 8 no revoca un compromiso ya asumido con el cliente.** RF-053 se conserva en alcance, en banda N2, con el conflicto declarado. Retirarlo es una conversación con el Product Owner, no una consecuencia mecánica del corte — es la decisión PD-07, reformulada en consecuencia.

Esto obliga además a una corrección técnica: la mitigación de inyección de prompt no puede apoyarse en «no entra texto libre al sistema», porque sí entra. Se apoya en dónde queda confinado — ver RNF-41 en §L.

##### F.3 Salen por no haber sido validados con el cliente

RF-121 (sugerencia de carga de la próxima serie) y RF-122 (proyección de trayectoria). D8 v3.2 ya los declara como **propuestas del equipo, no pedidos del cliente**, pendientes de confirmación. No hay fundamento para consumir capacidad en ellos en esta etapa. RF-030 sigue siendo el piso garantizado de precarga.

##### F.4 La exclusión de los presets, y por qué es la más importante

La planilla y el acta coinciden: RF-021 obtuvo 1 voto, RF-022 obtuvo 0, y el equipo respondió a la decisión D4 del acta con **«No usaremos preset, todo será generado desde cero con una batería de prompts»**. La exclusión está sobradamente respaldada.

Tiene dos consecuencias que el corpus actual no absorbe:

1. **RF-022 no es una funcionalidad de presets.** La observación de la planilla —«Del 021 al 025 incluidos, todos pertenecen a los presets, si se hace uno se tienen que hacer todos»— agrupa mal a RF-022. La copia profunda e independiente al asignar es el invariante que impide que modificar una plantilla reescriba el pasado de doce alumnos ([D4/PD-01](#d4), DD-02). Sin él, el versionado de RF-092 no tiene sobre qué operar y la adaptación destruye historial. **RF-022 se reincorpora como dependencia necesaria de máxima prioridad**, y se deja constancia de que su voto nulo proviene de una lectura equivocada del enunciado, no de una decisión de alcance.

2. **Se queda sin fallback la continuidad ante indisponibilidad generativa.** RF-058, RN-95b y la ADR 0004 apoyan toda la continuidad en «conservar la solicitud de presets publicados del gimnasio como vía disponible». Sin presets, esa frase queda vacía. **Resolución adoptada:** la vía manual es la **plantilla del entrenador (RF-019, 8 votos)**, que en este corpus es el mismo objeto que un preset sin publicar. RF-019 deja de ser una comodidad y pasa a ser el piso de disponibilidad de CAP-4. Hay que reescribir RF-058, RN-95b y las consecuencias de la ADR 0004 en esos términos (§O). Queda un hueco real que debe confirmarse: **un alumno nuevo, en un gimnasio sin plantillas cargadas y con el servicio generativo caído, no obtiene ninguna rutina** (§P/PD-03).

---

#### G. Dependencias necesarias

Elementos que no son funcionalidad de negocio independiente pero sin los cuales el alcance aprobado no funciona. Se declaran como dependencia, no como requisito nuevo.

| ID     | Dependencia                                            | Votos | De qué es dependencia                            | Qué pasa si no está                                                                                                                                                                                          |
| ------ | ------------------------------------------------------ | ----- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DEP-01 | **RF-022** copia al asignar                            | 0     | RF-019, RF-038, RF-092, todo CAP-7               | La adaptación reescribe el pasado de todos los alumnos que comparten plantilla. Corrupción de datos, no inconveniencia                                                                                       |
| DEP-02 | **RF-043** cumplimiento                                | 0     | RF-088 (`SOBREEXIGENCIA`), RF-046                | El diagnóstico pierde dos de sus cinco situaciones. Y es lo único que distingue este producto de un registrador                                                                                              |
| DEP-03 | **RF-024** frecuencia objetivo                         | 2     | RF-042 (adherencia), RN-89a global               | La adherencia no tiene denominador                                                                                                                                                                           |
| DEP-04 | **RF-058 + RF-113** continuidad e invalidez            | 1, —  | RF-054, RF-087, todo CAP-4                       | Una salida inválida llega al entrenador como si fuera una propuesta. Marcados **MUST\*** por el propio equipo en la planilla                                                                                 |
| DEP-05 | **RF-057** restricciones del contenido                 | 0     | RF-055, RF-090                                   | Un texto generado puede inventar números o emitir indicaciones médicas. Marcado **MUST\*** en la planilla                                                                                                    |
| DEP-06 | **RF-005 + RF-069** autorización y ámbito              | 2, 4  | Toda operación con identificador ajeno           | Cualquiera lee los datos de salud de cualquiera. R-11, RNF-14, RNF-20                                                                                                                                        |
| DEP-07 | **RF-066** asignación entrenador–alumno                | 2     | RF-005, RF-036, RF-038, RF-091, RF-110           | No existe sujeto que pueda autorizar la puerta. La capacidad C5 no es implementable                                                                                                                          |
| DEP-08 | **RF-030** precarga                                    | 1     | RNF-07 (dos interacciones por serie), RF-029     | Registrar una serie deja de caber en el uso real: de pie, entre series, con una mano                                                                                                                         |
| DEP-09 | **RF-071 + RF-106** datos simulados                    | 3, —  | RF-088, RF-046, toda demostración                | En catorce semanas no se acumula historial suficiente para que el diagnóstico produzca nada. El cliente autorizó explícitamente arrancar con datos cargados a mano                                           |
| DEP-10 | **RF-099** taxonomía y curación                        | —     | RF-016, RF-040, RF-086                           | El volumen se calcula mal y **corrompe el diagnóstico y con él todas las propuestas** (R-07)                                                                                                                 |
| DEP-11 | **RF-114 + RF-118** inventario y catálogo prescribible | —     | RF-086, RF-054, RF-087, RF-059                   | Se prescriben ejercicios imposibles de ejecutar en ese gimnasio. Decisión del cliente (N-27), no del equipo                                                                                                  |
| DEP-12 | **RF-115 + RF-116 + RF-100** alta y ámbito             | —     | Todo                                             | No hay gimnasio, no hay usuarios, no hay demostración (R-12)                                                                                                                                                 |
| DEP-13 | **RF-096** consentimiento                              | —     | RF-009, RF-010, RF-084                           | Se tratan datos de salud sin base. RNF-21                                                                                                                                                                    |
| DEP-14 | **RF-111** contexto suficiente                         | —     | RF-054, RF-087, RF-088                           | La inteligencia decide con huecos y nadie se entera                                                                                                                                                          |
| DEP-15 | **RF-112 + RF-109** continuidad de la puerta           | —     | RF-110, RF-066                                   | Un alumno sin entrenador queda en un limbo silencioso y sus propuestas se pierden al reasignarlo                                                                                                             |
| DEP-16 | **RF-072** trazabilidad de salidas                     | 0     | RF-090, criterio de éxito E9                     | No se puede auditar por qué el sistema propuso lo que propuso. **Alcance reducido**: versión, instante y contexto de entrada de las salidas que producen una propuesta; no un registro general               |
| DEP-17 | **RF-073** evaluación de componentes                   | 0     | RNF-24, RNF-25, criterio E9                      | **Transformado**: con RF-061 a RF-063 fuera y RF-059 en la capa generativa, ya no hay modelo clásico que evaluar. Pasa a ser el **conjunto de regresión generativa** que se corre antes de cambiar prompt, modelo o parámetros |
| DEP-18 | **RF-095** avisos                                      | —     | RF-038, RF-044, RF-046, RF-091                   | Cuatro requisitos prometen notificar y no hay canal. **Alcance reducido** a los tipos que el ciclo necesita                                                                                                  |

---

#### H. Impacto arquitectónico

##### H.1 Punto de partida real

Verificado sobre los tres repositorios el 2026-09-01:

| Repositorio              | Qué hay                                                                                                       | Qué **no** hay                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `proyecto-gimnasio`      | Vite + React + TS, ESLint/Prettier, Vitest, CI, Dockerfile, `App.tsx` con una pantalla de bienvenida           | Router, estado remoto, cliente de API, vistas                                      |
| `proyecto-gimnasio-back` | Express + TS, CORS por lista blanca, `/health` y `/ready`, cliente Prisma, pipeline de migraciones, Vercel, CI | **Ningún modelo en `schema.prisma`**, ninguna ruta de dominio, ninguna autorización |
| `proyecto-gimnasio-ia`   | Paquete Python con pandas, scikit-learn y sqlalchemy declarados; ruff, mypy strict, pytest, CI                 | **Paquete vacío** — ni API HTTP, ni worker, ni conector LLM                         |

**Conclusión:** no hay funcionalidad implementada ni parcialmente implementada; no hay funcionalidad implementada y no documentada; no hay deuda técnica de producto. Toda la deuda es documental (§O). El punto de partida es limpio, lo que permite tomar las decisiones de §H.2 sin costo de migración — pero **sólo hasta la primera migración de Prisma**.

##### H.2 Base de datos

El recorte no altera el núcleo del modelo, pero retira entidades completas.

| Cambio                                                                                                                          | Motivo                                                              |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Se retira** `Comentario`                                                                                                      | RF-039 fuera                                                        |
| **Se retira** el atributo `nivel de actividad` de `PerfilAlumno`                                                                | RF-012 fuera                                                        |
| **Se retira** `PlantillaRutina.publicada`                                                                                       | RF-021 fuera; una plantilla ya no se publica                        |
| **Se reduce** `RutinaAsignada.origen` a `PLANTILLA_ENTRENADOR` y `GENERADA`                                                      | RF-021 y RF-025 fuera                                               |
| **Se retiran** de `SesionEntrenamiento` los atributos `es diferida` y `desbloqueada hasta`                                       | RF-034 y RF-117 fuera                                               |
| **Se retiran** `ScoreRiesgo` y `SegmentoPerfil`                                                                                 | Ya derogadas en D4 v2.1                                             |
| **Se reduce** `RegistroAuditoria` a las operaciones de RF-038, RF-066, RF-091 y RF-114                                           | RF-097 reducido                                                     |
| **Se conserva íntegro** el eje `RutinaAsignada → VersionRutina → DiaRutina → EjercicioRutina → SeriePrescripta`                  | Es el núcleo. DEP-01                                                |
| **Se conservan íntegras** `EjercicioMusculo` y `EjercicioArticulacion`                                                           | Sin ellas la compatibilidad no es calculable (DEP-10)               |
| **Se conservan** las 23 restricciones de integridad RI-01 a RI-23                                                               | Ninguna depende de algo excluido                                    |

**Índices que hay que definir desde la primera migración**, porque son los que sostienen RNF-01 y RNF-36: `RegistroSerie(sesion, orden)` único · `RegistroSerie(ejercicio_ejecutado, sesion)` para volumen y capacidad máxima · `SesionEntrenamiento(alumno, fecha_de_ocurrencia)` para adherencia e historial · `RutinaAsignada(alumno, estado)` parcial sobre VIGENTE y PROPUESTA · `AsignacionEntrenador(alumno)` parcial sobre `hasta IS NULL` · `CondicionFisica(perfil)` parcial sobre `hasta IS NULL` · `Ejercicio(gimnasio)` admitiendo `NULL` para el catálogo base.

**Aislamiento multi-gimnasio.** Se resuelve en el modelo (`gimnasio` en toda entidad raíz, RI-01, RA-02), no en el motor. No se adopta *row-level security* de PostgreSQL: agrega una segunda fuente de autorización que hay que mantener sincronizada con la de la aplicación, y el proyecto no tiene capacidad para operar dos. Se compensa con RNF-14: una prueba automatizada por cada operación con identificador de alumno.

##### H.3 Backend

- **Monolito modular en Express y TypeScript sobre Vercel.** No cambia. Los módulos que el recorte deja en pie: identidad, contexto, catálogo, prescripción, entrenamiento, indicadores, adaptación e integración IA. Desaparecen los de nutrición y analítica del gimnasio.
- **La autorización es una capa única, no un `if` por ruta.** RA-01 es un doble filtro y RNF-14 exige una prueba por operación. Si se dispersa, R-11 se materializa. Debe existir antes de la segunda ruta de dominio, no después de la vigésima.
- **Transaccionalidad.** Cuatro operaciones son atómicas o no son: el aprovisionamiento (RNF-38), la puesta en vigencia de una rutina (crear versión, archivar la anterior, registrar la revisión), la resolución de una propuesta (crear versión, resolver ajustes, emitir aviso) y la copia profunda al asignar. Ninguna admite estado intermedio observable.
- **Concurrencia.** Tres puntos reales, ya catalogados: CB-14 (versión nueva con sesión en curso — la sesión conserva su prescripción congelada, PD-02 del modelo, sin bloqueo), CB-30 (misma propuesta resuelta dos veces — control de versión optimista sobre el estado de la propuesta), CB-66 (el inventario cambia mientras se aprueba una rutina — revalidar en el instante de la puesta en vigencia, no en el de apertura del formulario).
- **Idempotencia.** RF-104/RNF-13 sobre el registro de series, y clave idempotente sobre la solicitud de generación. Son los dos únicos puntos donde el reintento del cliente es cotidiano.
- **El backend nunca espera al LLM.** La solicitud se acepta y el frontend consulta estado contra el backend. No es una optimización: Vercel no sostiene una petición de 120 segundos.

##### H.4 Servicio de IA — la decisión que está bloqueada

**El corpus contiene dos decisiones arquitectónicas incompatibles, ambas en estado «aceptada»:**

|                                  | ADR 0005 (2026-08-25)                                                                                                                                 | ADR 0004 «servicio generativo online en el Polo» (2026-08-29)                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Qué decide                       | El AI Gateway es un **módulo interno del backend** (`GenerativeAiPort` más `OllamaAdapter`). El backend llama al LLM Server directamente               | `proyecto-gimnasio-ia` expone una **API HTTP Python con worker asíncrono** desplegada en el Polo y publicada por ngrok. El backend la llama a ella |
| Opción explícitamente descartada | «(c) AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server»                                                        | —                                                                                                                                 |
| Fundamento                       | No hay capacidad para operar un tercer servicio                                                                                                       | Vercel no puede sostener el LLM dentro de una petición; hace falta un worker durable                                              |

La ADR 0004 decide exactamente la opción (c) que la ADR 0005 descarta, y **no la declara reemplazada**. La arquitectura vigente (`system-overview.md`, `backend.md`, `analytics-engine.md`) sigue a la ADR 0004. **Esto debe resolverse antes de la primera línea de código de integración** (§P/PD-04).

Recomendación técnica, para que la decisión llegue preparada: **prevalece la ADR 0004**, porque su fundamento es una restricción física (Vercel no sostiene 120 segundos de inferencia; hace falta un proceso durable) y el de la ADR 0005 es un presupuesto de esfuerzo. Pero el fundamento de la ADR 0005 sigue siendo real: operar API, worker, LLM y agente ngrok en el Polo es trabajo no contabilizado en las 504 h. Lo que corresponde es **marcar la ADR 0005 como reemplazada por la ADR 0004 en su parte de ubicación de despliegue**, conservar de ella el puerto y el adaptador como patrón interno del servicio Python, y declarar la operación del Polo como carga adicional explícita.

**Lo que el recorte cambia en la capa de IA:**

| Antes (D8 v3.3)                                       | Ahora                                                                                                                                        |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `interpretarPedido` (RF-053) — lenguaje natural libre | **Se conserva** (§F.2b). Su salida es un conjunto de parámetros de enumeraciones cerradas, validado y confirmado por el usuario antes de usarse. Es la única entrada de texto libre del sistema y no alcanza a `generarRutina` |
| `generarRutina` (RF-054, RF-087)                      | Sin cambios. **Pasa a ser la única vía de creación automática**, sin preset del que partir                                                    |
| `explicarCriterios` (RF-055)                          | Sin cambios                                                                                                                                  |
| `sugerirAlternativas` (RF-059)                        | Sin cambios, con RF-060 absorbido como exclusión dura previa y posterior                                                                      |
| `resumirProgreso` (RF-056)                            | **Retirado**                                                                                                                                  |
| `describirPerfil` (RF-064)                            | Se conserva (6 votos), efímero, banda N3                                                                                                      |
| Fallback igual a presets publicados                   | **Fallback igual a plantillas del entrenador (RF-019)**                                                                                       |

**Responsabilidades que no son del LLM, y hay que poder demostrarlo en la defensa:** el catálogo prescribible (filtro exacto en SQL, ADR 0007), la compatibilidad (RN-44a a RN-44d, exclusión dura en código), los rangos del tipo de rutina (RN-39a), el diagnóstico (RN-79a) y las reglas de ajuste (RN-89a). El LLM construye el candidato y redacta; no calcula compatibilidad, no aprueba, no persiste y no emite indicaciones médicas.

##### H.5 Frontend

Vistas que el recorte deja en pie, por rol:

- **Alumno (7):** completar cuenta desde invitación · contexto (perfil, objetivo, condiciones, aptitud, mediciones) · rutina vigente · **sesión activa** · historial · panel de progreso · avisos.
- **Entrenador (6):** cartera priorizada · ficha del alumno · revisión de rutina propuesta · resolución de propuesta de adaptación · edición de rutina y plantillas · generación de rutina desde formulario.
- **Administrador (3):** invitaciones y roles · asignaciones · inventario.

**Desaparecen:** comentarios, panel del gimnasio, pauta nutricional, mapa muscular sobre esquema corporal, ajuste del candidato de rutina y registro diferido.

**La sesión activa es la pantalla de mayor riesgo del proyecto** (R-05) y la que produce el sustrato del que depende toda la inteligencia. Restricciones no negociables: usable a 360 px sin desplazamiento horizontal (RNF-06), dos interacciones por serie con los valores precargados (RNF-07, y por eso DEP-08), borrador local con reintento ante pérdida de conexión (RNF-10) y envío idempotente (RNF-13).

**La observación del equipo sobre alumno y entrenador con dos interfaces y un conmutador** (planilla, RF-004) se conserva como criterio de aceptación de RF-065, y encaja con DD-08 (los roles son un conjunto) y DD-28 (un entrenador que entrena necesita otro entrenador).

##### H.6 Contratos entre repositorios

Sin cambios de propiedad: el backend es dueño del OpenAPI público, del esquema y de las migraciones; el frontend genera su cliente desde una versión explícita; el servicio IA es dueño del OpenAPI de orquestación. Lo que el recorte simplifica es la superficie: desaparecen los endpoints de comentarios, analítica del gimnasio, nutrición, candidato ajustable y registro diferido.

**Los tres contratos hay que congelarlos temprano** (R-11): el OpenAPI del backend en la semana 3, el OpenAPI del servicio IA junto con la primera generación, y el esquema de la base antes de la primera migración a `test`.

---

#### I. Modelo funcional y de dominio

El modelo de [D4](#d4) se conserva salvo las retiradas de §H.2. Los cuatro puntos que gobiernan su corrección:

1. **Copia más versiones completas** (PD-01 del modelo). La rutina se copia al asignarse y cada adaptación produce una versión completa nueva. No hay diferencias que calcular ni conflictos que resolver, y el historial de adaptaciones se responde comparando dos versiones.
2. **La sesión es autocontenida** (PD-02 del modelo). Copia su prescripción al iniciarse. El pasado es inmune al versionado sin lógica adicional, y el cumplimiento sale gratis por serie.
3. **Derivado o persistido** (PD-03 del modelo). Se derivan volumen, capacidad máxima estimada, adherencia y cumplimiento; se persisten sólo los eventos con fecha (récord), las salidas fechadas de un componente (diagnóstico, propuesta) y la única marca derivada que debe sobrevivir a la consulta (`estado de compatibilidad` de `EjercicioRutina`).
4. **El equipamiento es del gimnasio** (PD-07 del modelo). Por eso la incompatibilidad por equipamiento **impide** en lugar de advertir, y por eso el inventario es un dato crítico.

**Consistencia temporal — el eje que no puede romperse.** Cinco entidades tienen vigencia: objetivo, condición física, aptitud, asignación entrenador–alumno y versión de rutina. La regla que las une: **toda pregunta sobre el pasado se responde con el estado vigente en esa fecha, no con el estado actual.** Una sesión referencia la versión bajo la que se ejecutó (RI-16); el diagnóstico referencia la versión evaluada; una condición cerrada no borra la propuesta que motivó, la invalida. Un diseño que reemplace la vigencia por un campo mutable hace irrespondible la pregunta que el cliente pidió responder: *por qué cambió esta rutina*.

---

#### J. Flujos críticos

Cinco flujos concentran el valor. Los tres marcados ⭐ son la demostración del producto.

##### J.1 ⭐ FL-A · Incorporación con rutina inmediata (CAP-1 → CAP-2 → CAP-4 → CAP-8)

El administrador o el entrenador emite una invitación nominal → la persona crea su cuenta y queda vinculada al gimnasio → declara perfil, objetivo y condiciones → el sistema verifica que el contexto es suficiente (RF-111) → genera una rutina completa sobre el catálogo prescribible, filtrada por compatibilidad (RF-087, RF-086) → la rutina nace **PROPUESTA** → el entrenador asignado la revisa y la aprueba → entra en **VIGENCIA** y el alumno recibe el aviso.

**Estado final esperado:** ningún alumno incorporado termina el día sin una rutina propuesta (criterio E1).
**Excepciones:** contexto insuficiente → se declara qué falta y no se genera · generación no disponible → el entrenador asigna una plantilla propia (RF-019) · sin entrenador vigente → la rutina queda propuesta y el administrador es señalado (RF-112).

##### J.2 ⭐ FL-B · Sesión de entrenamiento (CAP-5)

Selecciona un día del ciclo → el sistema **congela la prescripción dentro de la sesión** → registra serie a serie con los valores de la última ejecución precargados → puede agregar, omitir o sustituir → finaliza, o se cierra sola por inactividad.

**Estado final esperado:** la sesión conserva de forma conjunta lo prescripto y lo ejecutado, y no cambia nunca más.
**Excepciones:** pérdida de conexión → borrador local y reintento · reanudación → misma sesión, mismo congelamiento · valor atípico → confirmación explícita · envío repetido → un solo registro.

##### J.3 ⭐ FL-C · Diagnóstico y adaptación (CAP-6 → CAP-7 → CAP-8)

Cada dos semanas, fuera del camino de la petición: el sistema evalúa cada ejercicio de la rutina vigente y le asigna una de cinco situaciones por orden de precedencia → determina la situación global → aplica la tabla situación → ajuste → **verifica la propuesta completa contra compatibilidad y rangos antes de presentarla** → avisa al entrenador → el entrenador acepta entera, acepta en parte o rechaza → si acepta, se genera una versión nueva y se avisa al alumno.

**Estado final esperado:** toda adaptación aplicada conserva el criterio que la motivó y el dato que la sustenta (criterio E7); ninguna sesión ejecutada cambia (criterio E6).
**Excepciones:** datos insuficientes → diagnóstico registrado sin propuesta, declarando qué faltó · ningún ajuste aplicable → diagnóstico sin propuesta, que **es un resultado, no un fallo** · esfuerzo percibido nunca registrado → se diagnostica sin ese criterio y se declara · la propuesta deja de ser compatible antes de resolverse → INVALIDADA y se genera otra · treinta días sin resolver → CADUCADA · la asignación termina durante la revisión → la operación no se completa.

##### J.4 FL-D · Reevaluación por cambio de contexto (CAP-2/CAP-3 → CAP-7)

Cambia el objetivo, aparece o se cierra una condición, vence la aptitud **o cambia el inventario del gimnasio** → se recalcula el catálogo prescribible si corresponde → se reevalúa la rutina vigente → los ejercicios afectados se **marcan sin retirarse** → se avisa al entrenador y al alumno → se elabora la propuesta de sustitución.

**Por qué se marca y no se retira:** retirar un ejercicio de una rutina vigente es una decisión de prescripción, y la prescripción es del entrenador. Mientras haya una marca, el alumno recibe la advertencia al iniciar cada sesión que lo incluya.
**Excepción crítica:** no existe alternativa admisible en el catálogo prescribible → el ajuste no se propone, y el hecho se declara explícitamente en la propuesta en lugar de silenciarse.

##### J.5 FL-E · Revisión priorizada (CAP-8)

El entrenador ve su cartera ordenada por urgencia: pendientes de revisión → incompatibilidad sobrevenida → estancamiento → caída de adherencia → sin señal. Entra a la ficha consolidada, resuelve lo pendiente o interviene directamente sobre la rutina.

**Riesgo asociado:** si el tiempo de revisión crece, el sistema deja de servir por congestión humana, no por defecto técnico (criterio E1b, riesgo R-09). Hay que medirlo, no absorberlo.

---

#### K. Casos borde y errores

El corpus ya tiene 73 casos borde catalogados en [D10](#d10). Lo que aporta este baseline es **dónde se resuelve cada clase**, y qué cambia con el recorte.

| Clase                                   | Dónde se resuelve                        | Ejemplos                                                                                                                                                                                          |
| --------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vacíos y arranque**                   | Presentación más RF-051                  | Alumno sin sesiones, representación sin datos, cartera vacía, gimnasio recién aprovisionado, inventario vacío                                                                                      |
| **Datos ausentes o degradados**         | Regla de negocio                         | Ejercicio sin clasificación muscular (no aporta volumen, distinto de aportar cero) · esfuerzo percibido nunca registrado (se diagnostica sin ese criterio y se declara) · condición sin zona corporal |
| **Cambios en el tiempo**                | Vigencia más versionado                  | Condición nueva que invalida una propuesta pendiente · aptitud que vence en pleno período · retiro de equipamiento usado por muchas rutinas                                                        |
| **Interrupción**                        | Máquina de estados (RF-027)              | Cierre de la aplicación a mitad de sesión · vuelta pasadas ocho horas · invitación a medio usar                                                                                                     |
| **Concurrencia**                        | Transacción más control optimista        | Versión nueva con sesión en curso · misma propuesta resuelta dos veces · inventario que cambia durante una aprobación                                                                              |
| **Permisos en los bordes**              | Autorización centralizada (RA-01..RA-10) | Asignación que termina durante la revisión · actor con doble rol consultando a un alumno no asignado · acceso por enlace directo a un recurso ajeno                                                |
| **Fallos de dependencias**              | Arquitectura más RF-058 y RF-113         | Servicio IA, ngrok o LLM caídos o lentos · fuente externa del catálogo cambiada · proceso diferido nunca ejecutado                                                                                 |
| **Límites y valores extremos**          | Validación de servidor (RF-102)          | Carga cero o negativa · más de cien repeticiones · fecha futura o anterior a noventa días · sesión que cruza medianoche · alumno en otra zona horaria                                              |
| **Comportamiento absurdo pero posible** | Regla de negocio                         | Ocho sesiones en un día · carga muy superior al histórico → confirmación explícita · entrenador que rechaza sistemáticamente todo → información sobre la calidad del diagnóstico, no un error      |

##### K.1 Casos que el recorte elimina

CB-11 (estimación de riesgo nunca calculada), CB-70 (error de carga detectado un mes después — desaparece con RF-034 y RF-117), CB-72 y CB-73 (tope de regeneraciones y candidato abandonado — desaparecen con RF-119).

##### K.2 Casos que el recorte agrava, y que hay que tratar explícitamente

| Caso                                                                           | Por qué se agrava                                                   | Dónde se resuelve                                                                                                                                                                     |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CB-20 / CB-36 · el servicio generativo no responde o no produce salida válida** | Con presets fuera, era el único fallback declarado                  | RF-058 reescrito: la vía manual es la plantilla del entrenador. **Y hay que declarar el hueco**: gimnasio sin plantillas más servicio caído igual a alumno nuevo sin rutina (§P/PD-03) |
| **CB-21 · no existe alternativa admisible para un ejercicio incompatible**     | Sin RF-101 no hay tratamiento paralelo para el ejercicio desactivado | El ajuste no se propone y el hecho se declara en la propuesta. El ejercicio queda marcado INCOMPATIBLE en la rutina vigente                                                            |
| **Sesión no registrada el mismo día**                                          | Sin RF-034 el dato se pierde definitivamente                        | **La adherencia queda sesgada a la baja y hay que declararlo en la presentación del indicador**, no corregirlo en silencio                                                             |
| **CB-13 · ejercicio propio mal cargado**                                       | Sin RF-018 no hay desactivación                                     | Corrección por el autor. Deuda aceptada, §M/R-20                                                                                                                                      |

---

#### L. Requisitos no funcionales

Se conserva [D9](#d9) v2.0 con estos ajustes. La regla se mantiene: **un requisito no funcional sin forma de comprobarlo es una aspiración**, y no se inventan cifras.

| RNF           | Cambio                                                                                                                                                                                                                                                                                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RNF-05        | ✎ Retirar «y estimación de riesgo». Queda: el diagnóstico se ejecuta fuera del camino de la petición                                                                                                                                                                                                                                                              |
| RNF-11        | ✎ «los presets del gimnasio siguen solicitables» → «las plantillas del entrenador siguen asignables»                                                                                                                                                                                                                                                              |
| RNF-18        | ✎ Igual sustitución en el criterio de verificación                                                                                                                                                                                                                                                                                                                |
| RNF-26        | ✎ Reencuadrar: ya no hay modelo clásico contra el que comparar. Pasa a ser la comparación de la rutina generada contra la construida a mano por un entrenador sobre el mismo caso                                                                                                                                                                                  |
| RNF-28        | ✎ Retirar «vistas de riesgo». Queda la analítica sobre datos simulados                                                                                                                                                                                                                                                                                            |
| RNF-35        | **Retirado.** Cae con RF-049. La accesibilidad del dato queda cubierta por RNF-34 sobre la presentación en barras                                                                                                                                                                                                                                                  |
| RNF-39        | Se conserva. El cambio de inventario es la operación masiva de mayor riesgo de rendimiento                                                                                                                                                                                                                                                                         |
| **RNF-41** 🆕 | El texto libre del usuario queda confinado a la interpretación de RF-053, y no alcanza a ningún otro componente generativo: `generarRutina`, `sugerirAlternativas` y los narrativos reciben exclusivamente parámetros de enumeraciones cerradas y estructuras ya validadas por el servidor. *Verificación:* inspección del contrato del servicio IA — el único campo de texto libre del usuario es la entrada de `interpretarPedido`, y su salida se valida contra las enumeraciones de D2/§4 y se confirma con el usuario antes de propagarse |
| **RNF-42** 🆕 | Todo alumno con contexto suficiente tiene una rutina propuesta dentro de las 24 h de completar su incorporación. *Verificación:* consulta sobre la base — cero alumnos con contexto suficiente y sin rutina. Es el criterio E1 hecho comprobable, y el que la exclusión de presets pone en riesgo                                                                    |

**Cifras que siguen sin fundamento externo y hay que declarar como convención del proyecto, no como restricción:** los umbrales de RN-79a (4 sesiones, 70 %, ±2,5 %, esfuerzo ≥ 9 o ≤ 5), las magnitudes de RN-89a (+2,5 %, −10 %, ±1 serie, 2,50 kg), la periodicidad de dos semanas, la caducidad de treinta días y la ventana de adherencia de cuatro semanas. Están registradas como `[S]` en D12/§1.1 y son discutibles con el cliente (§P/PD-09).

---

#### M. Riesgos

Se conserva la matriz de [D12/§2](#d12) con estos cambios.

| ID          | Riesgo                                                                        | Prob.    | Impacto  | Cambio y tratamiento                                                                                                                                                                                                                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R-01        | El conjunto MUST no entra en el plazo                                         | **Muy alta** | Muy alto | **Se mantiene en Muy alta.** El recorte pasa de 79 MUST a 57 requisitos de banda N1 — una reducción del 28 %, no la que hacía falta. N1 sola está entre 0,9 × y 1,4 × la capacidad (§D.4). Bandas y §N.3 como decisión preparada, pero la decisión sigue siendo del cliente                                                              |
| R-03        | La estimación de riesgo se queda sin datos reales                             | —        | —        | **Cerrado.** RF-061 a RF-063 fuera, confirmado por la votación                                                                                                                                                                                                                                                                             |
| **R-17** 🆕 | **La disponibilidad de CAP-4 depende por completo del servicio generativo**   | **Alta** | **Muy alto** | Consecuencia directa de excluir los presets. Sin generación y sin plantillas cargadas, un alumno nuevo no obtiene rutina. Mitigación: cargar plantillas de arranque por gimnasio en el aprovisionamiento, y medir la disponibilidad real del Polo desde el Sprint 1. **No hay mitigación técnica dentro del alcance recortado** |
| **R-18** 🆕 | **La contradicción ADR 0004 / ADR 0005 se descubre al integrar**              | **Alta** | **Alto** | Dos decisiones «aceptadas» e incompatibles sobre dónde vive el servicio de IA. Resolverlo antes de la primera línea de integración (§P/PD-04)                                                                                                                                                                                               |
| **R-19** 🆕 | **La adherencia se mide sesgada y nadie lo declara**                          | Media    | Medio    | Sin registro diferido (RF-034), una sesión no cargada el mismo día se pierde. La adherencia —insumo de RN-89a global— queda sesgada a la baja. Mitigación: declararlo en la presentación del indicador y en la defensa                                                                                                                       |
| **R-20** 🆕 | **Un ejercicio propio mal cargado no se puede retirar**                       | Media    | Bajo     | Sin RF-018. Acotado al ámbito del gimnasio. Deuda aceptada                                                                                                                                                                                                                                                                                 |
| R-07        | La clasificación muscular importada es pobre                                  | Media    | **Alto** | **Sube de prioridad.** Es la única entrada de RF-040, y un volumen mal calculado corrompe el diagnóstico y todas las propuestas. La curación manual (RF-099) deja de ser opcional                                                                                                                                                            |
| R-09        | Congestión de la puerta del entrenador                                        | Media    | Alto     | Se agrava: sin comentarios (RF-039) el entrenador no tiene canal ligero para responder sin abrir la ficha                                                                                                                                                                                                                                   |
| R-15        | El inventario del gimnasio se declara mal o queda desactualizado              | Alta     | Alto     | Sin cambios. Sigue sin haber mitigación técnica para un inventario que declara equipamiento inexistente                                                                                                                                                                                                                                     |
| R-16        | La expectativa sobre el LLM excede su autoridad real                          | Media    | Alto     | Se agrava con la exclusión de presets: el LLM pasa a ser la única vía automática de creación                                                                                                                                                                                                                                                |

##### M.1 Inconsistencia que precede a la conversación de alcance

| #     | Inconsistencia                                                                                                                                                                                                                                                                                                                     | Estado                                                                                                    |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **I-09** 🆕 | **La capacidad de construcción está calculada sobre un supuesto que otra fuente contradice.** [D12/§3](#d12) descuenta a tres personas —dirección de proyecto y las dos de calidad— y llega a «≈ 6/9 × 756 ≈ 504 h». El Documento de Planificación e Inicio §1.3 dice lo contrario de forma explícita: «Los roles de gestión **no son de dedicación exclusiva: todos los integrantes participan en la construcción del software**», y de hecho asigna a las tres personas a equipos verticales con alcance funcional | **Abierta y de alto impacto.** Entre 504 h y 756 h hay un 50 % de diferencia. Es el denominador de PD-01: conviene resolverlo *antes* de discutir qué se recorta, no después |

Ninguna de las dos fuentes es evidentemente correcta. D12 es más reciente y su descuento es prudente; el Documento de Planificación es la fuente de la asignación de roles y describe una organización en equipos verticales donde las tres personas tienen alcance funcional asignado. **No hay que elegir la que convenga: hay que preguntarle al equipo cuántas horas de construcción aporta realmente cada persona**, que es un dato que el equipo tiene y ninguno de los dos documentos midió.

---

#### N. Orden de construcción recomendado

##### N.1 Qué se conserva y qué se corrige del plan del acta

**Se conserva** la instrucción del cliente: primero el motor de adaptación sobre datos cargados a mano, después la gestión de entidades, y dentro de ella alta, baja y edición en ese orden. El fundamento técnico es sólido: construir el motor primero obliga a resolver el modelo de dominio en la primera semana, que es justamente la mitigación de R-04.

**Se corrigen dos defectos del plan del acta:**

1. **El Sprint 2 construye «preajustes»**, que ya no existen. Ese trabajo desaparece.
2. **El Sprint 5 construye la generación asistida**, pero al excluirse los presets **la generación pasó a ser la única vía automática de creación de rutinas**. Dejarla para el quinto sprint significa que durante cuatro sprints no existe ninguna forma de que aparezca una rutina salvo cargarla a mano. Hay que adelantarla.

##### N.2 Plan propuesto

| Sprint | Fechas        | Objetivo                                                                                                                                                                            | Entregable demostrable                                                                                                                       |
| ------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | 01/09 – 14/09 | Modelo de dominio congelado · esqueleto desplegado de punta a punta · siembra de datos (RF-071) · diagnóstico y reglas de ajuste (RF-088, RF-089, RF-090)                            | Dado un alumno y una rutina sembrados, el sistema produce una propuesta de adaptación coherente y justificada                                 |
| **2**  | 15/09 – 28/09 | Contexto del alumno · catálogo, taxonomía e inventario · catálogo prescribible · **compatibilidad (RF-086)** · altas                                                                | Una rutina se bloquea porque un ejercicio está contraindicado, y el sistema ofrece alternativas admisibles                                    |
| **3**  | 29/09 – 12/10 | **Generación de la rutina inicial (RF-087, RF-054, RF-055, RF-113)** · autorización completa · revisión y puesta en vigencia (RF-110, RF-091)                                        | Un alumno nuevo se incorpora, recibe una rutina generada y compatible, y su entrenador la aprueba. **Circuito de prescripción cerrado**       |
| **4**  | 13/10 – 26/10 | Ejecución y registro de sesiones (RF-027 a RF-035) · indicadores reales (RF-040 a RF-046) · bajas                                                                                    | El alumno entrena, y el diagnóstico del Sprint 1 corre sobre actividad real en lugar de sembrada                                              |
| **5**  | 27/10 – 09/11 | Cartera y ficha (RF-036, RF-037) · paneles (RF-048, RF-050, RF-051) · alternativas de sustitución (RF-059) · reevaluación por cambio de contexto (RF-094) · ediciones                | **Ciclo completo cerrado sobre datos reales.** Banda N2 completa                                                                              |
| **6**  | 10/11 – 23/11 | Estabilización · regresión generativa (RF-073) · banda N3 si el hito del Sprint 3 se cumplió · documentación y defensa                                                               | Sistema desplegado, medido y demostrable                                                                                                     |

**Diferencia clave con el plan del acta:** el circuito de prescripción cierra en el Sprint 3 en lugar del Sprint 5. A partir de ahí cada sprint agrega evidencia sobre un circuito que ya funciona, en vez de construir piezas que todavía no se pueden conectar.

**Punto de control formal al cierre del Sprint 3:** si el circuito de prescripción no cerró, se activa el orden de retirada de §N.3 antes del Sprint 4, no en la semana 12.

##### N.3 Orden de retirada

Escrito de antemano para que la decisión ya esté tomada cuando llegue el momento. Nunca se recorta la banda N1.

| #  | Se retira                                    | Queda en su lugar                            |
| -- | -------------------------------------------- | -------------------------------------------- |
| 1  | RF-067 estado de membresía                   | Nada                                         |
| 2  | RF-064 descripción del perfil                | Nada                                         |
| 3  | RF-052 indicadores agregados de la cartera   | La cartera de RF-036                         |
| 4  | RF-017 y RF-100 catálogo propio del gimnasio | Sólo el catálogo base                        |
| 5  | RF-093 historial de adaptaciones             | Las versiones de rutina siguen consultables  |
| 6  | RF-044 récords personales                    | La evolución de RF-050                       |
| 7  | RF-045 media móvil de mediciones             | La serie sin suavizado                       |
| 8  | RF-031 ajustes durante la sesión             | Registro secuencial de lo prescripto         |
| 9  | RF-014 búsqueda y filtrado                   | Listado completo del catálogo                |
| 10 | RF-072 trazabilidad de salidas               | La justificación de RF-090                   |

**A partir de acá se degradan requisitos de la banda N1, y cada paso exige acuerdo explícito del cliente.** El primero sería RF-055 (explicación en lenguaje natural), sustituida por la presentación tabulada del criterio y los datos — lo que conserva la condición C5 del acta pero pierde la capa narrativa. Retirar cualquier cosa de CAP-7 significa entregar un sistema que no es el que el cliente pidió, y hay que decirlo con esas palabras.

---

#### O. Deuda documental: qué hay que actualizar

##### O.1 Defectos del corpus, independientes del alcance

Detectados ejecutando la propia herramienta de validación del repositorio y rastreando referencias cruzadas.

| #    | Defecto                                                                                                                                                                                                                                                                                         | Gravedad       | Corrección                                                                                       |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- | ------------------------------------------------------------------------------------------------ |
| DC-1 | **`DD-34` no existe.** Ocho documentos lo citan como fundamento del replanteo de IA (D8, D4, D3, D6, D7, `generative-ai.md`, `predictive-ai.md`, ADR 0008). `design-decisions.md` está en v2.1 y termina en DD-33                                                                                 | **Bloqueante** | Escribir DD-34 en D11 con el contenido que las ocho referencias le atribuyen, y subir D11 a v2.2 |
| DC-2 | **Dos ADR numeradas 0004** con decisiones distintas: `0004-self-hosted-llm-server.md` (25/08) y `0004-servicio-generativo-online-en-el-polo.md` (29/08)                                                                                                                                          | **Bloqueante** | Renumerar la segunda como ADR 0009 y declarar explícitamente su relación con la 0004 y la 0005  |
| DC-3 | **La ADR 0005 contradice a la ADR 0004 (Polo)** y sigue en estado «aceptada» sin declararse reemplazada                                                                                                                                                                                          | **Bloqueante** | §P/PD-04 · marcar la 0005 como parcialmente reemplazada                                          |
| DC-4 | **Nueve documentos no registrados en `manifest.json`** → `python tools/check_docs.py` falla, y con él el workflow `quality.yml` sobre `main`: `ai-model-selection.md`, `generative-ai.md`, `predictive-ai.md`, las ADR 0004 (self-hosted), 0005, 0006, 0007 y 0008, y `deliverable PO/alcance-ia-generativa.md` | **Alta**       | Registrarlos en el manifiesto con alcance, autoridad y `load_when`                                |
| DC-5 | **D13 está en v2.0 y contradice a D8 v3.3**: N-17 declara RF-061 a RF-063 «en MUST» y la capacidad C3 los incluye. Están en WON'T                                                                                                                                                                | Alta           | Subir D13 a v3.0                                                                                 |
| DC-6 | **RNF-05 y RNF-28 siguen nombrando la estimación de riesgo**; `CB-11` describe un caso de una funcionalidad retirada                                                                                                                                                                             | Media          | §L y D10                                                                                         |
| DC-7 | **El entregable al Product Owner salta de la sección 1 a la 3** — falta la sección 2                                                                                                                                                                                                             | Media          | Completar o renumerar                                                                            |
| DC-8 | **`architecture/generative-ai-integration.md` y `architecture/generative-ai.md`** coexisten sin que el manifiesto distinga sus autoridades; sólo el primero está registrado                                                                                                                       | Media          | Declarar la frontera entre ambos o fusionarlos                                                   |

##### O.2 Cambios derivados del nuevo alcance

| Documento                                                        | Cambio                                                                                                                                                                                                                                              | Prioridad |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| [D8](#d8)                 | → v4.0. Reorganizar por capacidades · marcar los veinte diferidos · registrar las cinco fusiones y las cuatro degradaciones · reescribir RF-058 (plantillas, no presets) · retirar RF-119, RF-120, RF-121 y RF-122                                    | **Alta**  |
| [D1](#d1)                        | §3.2 «los presets del gimnasio permanecen» → plantillas del entrenador · §6 incorporar las exclusiones nuevas · criterios de éxito: retirar los que dependen de lo excluido                                                                          | **Alta**  |
| [D5](#d5)                                | Retirar §5.2 y RN-124 a RN-129 (candidato) · reescribir RN-95b · retirar las reglas de nutrición · conservar íntegras RN-39a, RN-44a a RN-44d, RN-79a y RN-89a                                                                                       | **Alta**  |
| [D4](#d4)                                  | → v2.2. Retiradas de §H.2 · `origen` de `RutinaAsignada` con dos valores · declarar los índices                                                                                                                                                      | **Alta**  |
| [D11](#d11)                          | Escribir **DD-34** (DC-1) · marcar **DD-33 derogada para esta etapa** (cae con RF-119) · **DD-13 sin efecto** (nutrición fuera) · nueva **DD-35: la plantilla del entrenador es el piso de disponibilidad de la prescripción**                        | **Alta**  |
| [D12](#d12)                                  | R-17 a R-20 · R-03 cerrado · §4 sustituida por §N.3 · nueva aritmética                                                                                                                                                                              | **Alta**  |
| [D13](#d13)                           | → v3.0. Incorporar la votación como fuente · corregir DC-5 · **agregar N-28: video demostrativo por ejercicio, hoy sin cobertura** (§P/PD-10)                                                                                                        | **Alta**  |
| `architecture/*`                                                 | Retirar la interpretación de lenguaje natural del contrato generativo · sustituir el fallback de presets · alinear con la resolución de PD-04                                                                                                        | **Alta**  |
| `manifest.json`                                                  | DC-4 · registrar este documento                                                                                                                                                                                                                     | **Alta**  |
| [D6](#d6)                         | Retirar el candidato de §1 · sesión sin `desbloqueada hasta` ni `es diferida`                                                                                                                                                                        | Media     |
| [D7](#d7)                               | Derogar FL-03 y FL-08 · reescribir FL-04 sin interpretación de lenguaje natural · retirar FL-21                                                                                                                                                      | Media     |
| [D10](#d10)                                   | Retirar CB-11, CB-70, CB-72 y CB-73 · agregar los casos agravados de §K.2                                                                                                                                                                           | Media     |
| [D9](#d9)             | Los cambios de §L, incluidos RNF-41 y RNF-42                                                                                                                                                                                                        | Media     |
| [D3](#d3)                      | Retirar de la matriz las filas de comentarios, nutrición y panel del gimnasio                                                                                                                                                                       | Media     |
| [D2](#d2)                                     | Retirar «preset» como término con entidad propia · reducir §4.12 a los tipos de aviso que sobreviven                                                                                                                                                | Media     |
| Diagramas                                                        | Casos de uso (desaparecen «Autoasignarse una rutina», «Publicar preset» y «Comentar»; el proceso programado pierde la estimación de riesgo) · modelo de datos · secuencia de generación                                                              | Media     |

---

#### P. Decisiones pendientes

Sólo las que requieren decisión humana. No hay respuesta técnica que las cierre.

| #     | Decisión                                                                                                                                                                                                                                                                                       | Quién                | Cuándo                                          |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------- |
| PD-00 | **¿Cuánta capacidad de construcción hay realmente?** D12 dice ~504 h descontando a tres personas; el Documento de Planificación dice que las nueve construyen (I-09). Entre una lectura y otra hay un 50 %. **Es el denominador de PD-01 y hay que resolverlo primero**, midiendo la disponibilidad real declarada por cada integrante, no eligiendo el documento que convenga | Project Manager      | **Antes de PD-01**                              |
| PD-01 | **El alcance sigue por encima de la capacidad.** 57 requisitos de banda N1 contra ~504 h — entre 0,9 × y 1,4 × sólo el núcleo (§D.4). Hay que decidir con el cliente qué se entrega, con §N.3 sobre la mesa. Es la misma conversación que D12/R-01 pide desde hace dos semanas                  | Cliente              | Antes del Sprint 2                              |
| PD-02 | **Baja de cuenta, portabilidad y anonimización (RF-006, RF-105) quedan fuera con 0 votos.** El sistema almacena condiciones físicas, aptitud y mediciones: datos sensibles. Diferirlo es una decisión de exposición, no de alcance funcional, y hay que tomarla explícitamente                  | Cliente y equipo     | Antes del Sprint 2                              |
| PD-03 | **Sin presets, la creación de rutinas depende por completo del servicio generativo.** Confirmar que la plantilla del entrenador es el fallback aceptado, y aceptar que un alumno nuevo, en un gimnasio sin plantillas y con el servicio caído, no obtiene rutina                                | Cliente              | Antes del Sprint 3                              |
| PD-04 | **ADR 0004 (Polo) frente a ADR 0005.** ¿El servicio de IA es un módulo interno del backend o un servicio Python desplegado en el Polo? Recomendación en §H.4                                                                                                                                    | Líder técnico        | **Antes de la primera línea de integración**    |
| PD-05 | **¿Quién opera el Polo?** API, worker, LLM y agente ngrok son cuatro procesos que deben arrancar con la máquina, reiniciarse y exponer salud. Es trabajo no contabilizado en las 504 h                                                                                                          | Equipo e institución | Sprint 1                                        |
| PD-06 | **Escribir DD-34** (DC-1). Ocho documentos apoyan su replanteo de IA en una decisión que no existe                                                                                                                                                                                              | Equipo               | Sprint 1                                        |
| PD-07 | **RF-053 obtuvo 3 de 8 votos pero está comprometido por escrito ante el Product Owner** (`alcance-ia-generativa.md` v2.1). El equipo no lo quiere; el compromiso existe. O el Product Owner libera el compromiso, o RF-053 se construye pese al voto. **No se puede dejar sin resolver: es la única entrada de texto libre del sistema y condiciona RNF-41** | Product Owner        | Antes del Sprint 3                              |
| PD-08 | **RF-049 degradado a barras por grupo muscular.** El documento de planificación lo describe como «diferencial visual y conceptual del producto». La votación le dio 4 de 8                                                                                                                      | Cliente              | Antes del Sprint 5                              |
| PD-09 | **Umbrales y magnitudes de RN-79a y RN-89a.** Son convenciones del equipo sin fundamento externo, y determinan literalmente qué le va a proponer el sistema a una persona. Merecen validación con alguien del oficio                                                                            | Cliente o entrenador | Sprint 2                                        |
| PD-10 | **El video demostrativo por ejercicio (N11 del acta) nunca entró al corpus.** RF-015 pide «al menos un recurso visual»; el cliente mencionó video. Confirmar si el enlace embebido es exigible                                                                                                  | Cliente              | Sprint 2                                        |
| PD-11 | Abiertas de D12 que siguen sin resolver: **I-06** (`READAPTACION` fuera de los tipos de rutina) · **I-07** (base shadow para migraciones sin tocar Neon Test) · **I-08** (operación productiva por ngrok)                                                                                        | Equipo               | I-07 antes de la primera migración              |
| PD-12 | **La votación registra 8 de 9 integrantes.** Quien no votó es la persona que tiene asignado el módulo de IA generativa completo. Conviene confirmar que el recorte de CAP-8 tiene su acuerdo                                                                                                    | Project Manager      | Inmediato                                       |

---

#### Anexo · Trazabilidad de la votación

`≥5` aprobado por votación · `DEP` dependencia necesaria · `CLI` autoridad del cliente · `F` absorbido por fusión · `—` fuera de esta etapa

| Planilla    | Requisito (planilla)                    | Votos | Decisión | Resultado en el baseline                                        |
| ----------- | --------------------------------------- | ----- | -------- | --------------------------------------------------------------- |
| RF-001      | Registro de usuarios                    | 8     | ≥5       | RF-001 · alta desde invitación · CAP-1 · N1                     |
| RF-002      | Autenticación y gestión de sesión       | 8     | ≥5       | RF-002 · CAP-1 · N1                                             |
| RF-003      | Recuperación y cambio de credenciales   | 8     | ≥5       | RF-003 · CAP-1 · N2                                             |
| RF-004      | Gestión de roles                        | 8     | F5       | → RF-065                                                        |
| RF-005      | Control de acceso a la información      | 2     | DEP-06   | RF-005 · **fusión con RF-004 rechazada**                        |
| RF-006      | Baja de cuenta y portabilidad           | 0     | —        | Diferido · PD-02 · arrastra RF-105                              |
| RF-007      | Perfil del alumno                       | 8     | ≥5       | RF-007 · CAP-2 · N1                                             |
| RF-008      | Objetivo de entrenamiento               | 8     | ≥5       | RF-008 · CAP-2 · N1                                             |
| RF-009      | Condiciones y restricciones             | 8     | ≥5       | RF-009 más RF-085 · CAP-2 · N1                                  |
| RF-010      | Mediciones corporales                   | 8     | ≥5       | RF-010 · CAP-2 · N1                                             |
| RF-011      | Perfil del entrenador                   | 4     | —        | Fuera                                                           |
| RF-012      | Estimación energética                   | 2     | —        | Fuera · cae toda la nutrición                                   |
| RF-013      | Catálogo de ejercicios                  | 8     | ≥5       | RF-013 · CAP-3 · N1                                             |
| RF-014      | Búsqueda y filtrado                     | 8     | ≥5       | RF-014 · CAP-3 · N2                                             |
| RF-015      | Información descriptiva                 | 8     | ≥5       | RF-015 · CAP-3 · N2 · ver PD-10                                 |
| RF-016      | Clasificación muscular                  | 8     | ≥5       | RF-016 más RF-099 · CAP-3 · N1                                  |
| RF-017      | Ejercicios propios del entrenador       | 5     | ≥5       | RF-017 más RF-100 · CAP-3 · N3                                  |
| RF-018      | Curación y desactivación                | 0     | —        | Fuera · arrastra RF-101 · R-20                                  |
| RF-019      | Plantillas de rutina                    | 8     | ≥5       | RF-019 · **piso de disponibilidad de CAP-4** · N1               |
| RF-020      | Prescripción de series                  | 6     | ≥5       | RF-020 · CAP-4 · N1                                             |
| RF-021      | Publicación de presets                  | 1     | —        | Fuera · confirma la respuesta D4 del acta                       |
| RF-022      | Asignación por copia independiente      | 0     | DEP-01   | **Reincorporado.** Voto nulo por lectura equivocada             |
| RF-023      | Personalización de la rutina asignada   | 1     | F2       | → RF-038                                                        |
| RF-024      | Objetivo de frecuencia semanal          | 2     | DEP-03   | RF-024 · CAP-4 · N1                                             |
| RF-025      | Autoasignación por el alumno            | 3     | —        | Fuera · arrastra RF-119 y RF-120                                |
| RF-026      | Vigencia y archivado                    | 6     | ≥5       | RF-026 · CAP-4 · N1                                             |
| RF-027      | Inicio de sesión de entrenamiento       | 8     | F1       | RF-027 · ciclo de vida completo · N1                            |
| RF-028      | Congelamiento de la prescripción        | 5     | ≥5       | RF-028 · CAP-5 · N1                                             |
| RF-029      | Registro de series ejecutadas           | 8     | ≥5       | RF-029 · CAP-5 · N1                                             |
| RF-030      | Precarga de valores de referencia       | 1     | DEP-08   | RF-030 · sostiene RNF-07                                        |
| RF-031      | Ajustes durante la sesión               | 6     | ≥5       | RF-031 · CAP-5 · N2                                             |
| RF-032      | Reanudación de sesiones                 | 3     | F1       | → RF-027                                                        |
| RF-033      | Finalización de sesión                  | 7     | F1       | → RF-027                                                        |
| RF-034      | Registro y corrección diferidos         | 2     | —        | Fuera · arrastra RF-117 · R-19                                  |
| RF-035      | Historial de entrenamientos             | 8     | ≥5       | RF-035 · CAP-5 · N1                                             |
| RF-036      | Cartera priorizada                      | 5     | F4       | RF-036 · absorbe RF-107 · N1                                    |
| RF-037      | Ficha integral del alumno               | 8     | ≥5       | RF-037 · CAP-8 · N1                                             |
| RF-038      | Intervención sobre la rutina            | 7     | F2       | RF-038 · absorbe RF-023 · N1                                    |
| RF-039      | Comentarios de seguimiento              | 1     | —        | Fuera · agrava R-09                                             |
| RF-040      | Volumen y frecuencia por grupo muscular | 8     | ≥5       | RF-040 · CAP-6 · N1                                             |
| RF-041      | Capacidad máxima estimada               | 8     | ≥5       | RF-041 · CAP-6 · N1                                             |
| RF-042      | Adherencia al plan                      | 5     | ≥5       | RF-042 · CAP-6 · N1                                             |
| RF-043      | Cumplimiento de la prescripción         | 0     | DEP-02   | **Reincorporado.** Sin él el diagnóstico pierde dos situaciones |
| RF-044      | Récords personales                      | 6     | ≥5       | RF-044 · CAP-6 · N2                                             |
| RF-045      | Evolución de mediciones                 | 8     | ≥5       | RF-045 · CAP-6 · N2                                             |
| RF-046      | Señales de seguimiento                  | 7     | ≥5       | RF-046 · CAP-6 · N1                                             |
| RF-047      | Parametrización de reglas               | 3     | —        | Fuera · constantes documentadas                                 |
| RF-048      | Panel de progreso del alumno            | 8     | ≥5       | RF-048 · absorbe la presentación de RF-040 en barras · N2       |
| RF-049      | Representación muscular                 | 4     | —        | **Degradado** a barras dentro de RF-048 · PD-08                 |
| RF-050      | Evolución por ejercicio                 | 8     | ≥5       | RF-050 · CAP-6 · N2                                             |
| RF-051      | Ante información insuficiente           | 7     | ≥5       | RF-051 · CAP-6 · N1                                             |
| RF-052      | Panel agregado del entrenador           | 8     | ≥5       | RF-052 · CAP-6 · N3                                             |
| RF-053      | Interpretación de lenguaje natural      | 3     | Compromiso PO | **Conservado pese a no alcanzar el corte** · §F.2b · PD-07 |
| RF-054      | Generación asistida de rutinas          | 8     | ≥5       | RF-054 · **fusión con RF-055 rechazada**                        |
| RF-055      | Justificación de la propuesta generada  | 8     | ≥5       | RF-055 · componente narrativo separado                          |
| RF-056      | Resumen periódico del progreso          | 4     | —        | Fuera · ya sustituido por RF-090                                |
| RF-057      | Restricciones del contenido generado    | 0     | DEP-05   | **Reincorporado.** MUST* en la propia planilla                  |
| RF-058      | Continuidad ante indisponibilidad       | 1     | DEP-04   | **Reincorporado y reescrito** · §F.4                            |
| RF-059      | Recomendación de sustitutos             | 8     | F3       | RF-059 · absorbe RF-060 · N1                                    |
| RF-060      | Condicionamiento de recomendaciones     | 2     | F3       | → RF-059 · exclusión dura                                       |
| RF-061      | Riesgo de abandono                      | 1     | —        | Fuera · la votación confirma el WON'T de v3.3                   |
| RF-062      | Explicabilidad de la estimación         | 0     | —        | Fuera                                                           |
| RF-063      | Actualización de estimaciones           | 0     | —        | Fuera                                                           |
| RF-064      | Segmentación de perfiles                | 6     | ≥5       | RF-064 · efímero, generativo · N3                               |
| RF-065      | Gestión de usuarios y roles             | 6     | F5       | RF-065 · absorbe RF-004 (8 votos) · N1                          |
| RF-066      | Asignaciones entrenador–alumno          | 2     | DEP-07   | **Reincorporado.** Sujeto de la puerta                          |
| RF-067      | Estado de membresía                     | 8     | ≥5       | RF-067 · informativo · N3                                       |
| RF-068      | Panel analítico del gimnasio            | 2     | —        | Fuera                                                           |
| RF-069      | Ámbito por gimnasio                     | 4     | DEP-06   | **Reincorporado.** Aislamiento                                  |
| RF-070      | Carga inicial del catálogo              | 8     | ≥5       | RF-070 · CAP-3 · N1                                             |
| RF-071      | Datos de demostración                   | 3     | DEP-09   | **Reincorporado.** Autorizado por el cliente                    |
| RF-072      | Trazabilidad de resultados inteligentes | 0     | DEP-16   | Reincorporado con alcance reducido                              |
| RF-073      | Evaluación de componentes inteligentes  | 0     | DEP-17   | **Transformado** en regresión generativa                        |
| RF-074      | Indicador nutricional diario            | 1     | —        | Fuera                                                           |
| RF-075..081 | Exclusiones ya evaluadas                | 0     | —        | Se confirman                                                    |
| RF-082..094 | Requisitos nuevos del cliente           | —     | CLI      | Todos en alcance · CAP-4 y CAP-7 · §D.3                         |
| RF-095..118 | Derivados del análisis del corpus       | —     | DEP o —  | Individualmente justificados en §G                              |
| RF-119..122 | Candidato ajustable e IA predictiva     | —     | —        | Fuera · §F.1 y §F.3                                             |

---

**Este documento no es normativo hasta que el equipo lo vote y el cliente resuelva PD-01.** Hasta entonces, la referencia de alcance sigue siendo D8 v3.3.


---

<a id="parte-ix"></a>

## Parte IX — Operación

<a id="ops-local-db"></a>

### Base de datos compartida de desarrollo

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/operations/local-database.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `OPS-LOCAL-DB`

#### Estrategia

El trabajo local ordinario usa **Neon Test**, compartida por el equipo. Producción usa otro proyecto o base, otras conexiones y otros roles. Ningún desarrollador recibe credenciales productivas.

Frontend no accede a PostgreSQL. Backend local usa un rol personal o de aplicación test; el servicio IA usa un rol restringido a estructuras de integración.

#### Primera configuración

```bash
npm ci
cp .env.example .env
npm run db:generate
npm run db:status
npm run dev
```

En PowerShell, usar `Copy-Item .env.example .env`. La persona responsable entrega la conexión Neon Test por un canal seguro; nunca se copia una credencial real en `.env.example`, GitHub, issues o documentación.

#### Reglas sobre la base compartida

- No ejecutar `prisma migrate reset`, `prisma db push` ni seeds destructivos.
- No ejecutar migraciones automáticamente al iniciar la aplicación.
- Cada prueba o desarrollador identifica sus datos y elimina sólo lo que creó.
- Las pruebas destructivas o de integración compartida se serializan.
- Los tests unitarios no dependen de Neon.
- CI aplica migraciones una sola vez por ambiente mediante `prisma migrate deploy` y un rol `migrator` separado.

#### Crear migraciones · decisión I-07 resuelta

`prisma migrate dev` no se ejecuta contra Neon Test compartida. El autor de una migración usa exclusivamente PostgreSQL 17 efímero mediante `compose.migrations.yaml` del backend. El contenedor usa `tmpfs`, no conserva datos y no levanta la aplicación.

Flujo del autor:

1. Partir de `develop` actualizado y levantar el contenedor con `docker compose -f compose.migrations.yaml up -d --wait`.
2. Definir temporalmente `DATABASE_URL=postgresql://gym_migrator@localhost:55432/gym_migrations?schema=public` en esa terminal. El contenedor acepta conexiones sin contraseña únicamente porque es efímero y publica el puerto sólo sobre `127.0.0.1`.
3. Modificar `schema.prisma` y ejecutar `npm run db:migrate -- --name <nombre_descriptivo>`.
4. Revisar el SQL generado, ejecutar `npm run db:status` y `npm run check`.
5. Destruir y recrear el contenedor, y ejecutar `npm run db:deploy` para verificar todo el historial desde una base vacía.
6. Detener el contenedor y restaurar la variable de entorno anterior.

El PR incluye `schema.prisma`, el directorio nuevo de `prisma/migrations`, pruebas y una explicación de compatibilidad. Nunca se edita una migración ya integrada. La aplicación local continúa usando Neon Test con el rol runtime y no usa Docker salvo al crear migraciones.

CI también aplica el historial completo sobre PostgreSQL 17 limpio dentro del check `quality`. No usa secretos ni Neon para esta validación.

#### Promoción

- Merge a `test`: CI ejecuta `npm run db:deploy` contra Neon Test antes del despliegue compatible.
- Merge a `main`: CI ejecuta el mismo comando contra Neon Producción con aprobación del dueño.
- Los cambios incompatibles usan expansión, migración de consumidores y contracción posterior para permitir rollback.

Los environments de GitHub `test` y `Production` contienen un secret homónimo `MIGRATION_DATABASE_URL`, con URL directa y rol migrador propio de cada ambiente. Estas credenciales no se guardan en Vercel ni se entregan a desarrolladores. El workflow las expone a Prisma como `DATABASE_URL` sólo durante el job.


---

<a id="parte-x"></a>

## Parte X — Entrega y gobierno del trabajo

<a id="delivery-github"></a>

### Flujo de trabajo en GitHub

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/delivery/github-workflow.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `DELIVERY-GITHUB`

#### Ramas

Estas reglas aplican a frontend, backend e IA:

- `main`: producción, estable y etiquetada.
- `test`: ambiente estable de integración y aceptación.
- `develop`: integración del próximo incremento.
- `feature/<issue>-<descripcion>`: trabajo funcional desde `develop`.
- `fix/<issue>-<descripcion>`: corrección desde `develop`.
- `hotfix/<issue>-<descripcion>`: corrección urgente desde `main`.

No se usan ramas `release/*`. El mismo commit promovido de `develop` a `test` y luego a `main` mantiene trazabilidad entre ambientes. Un hotfix vuelve después a `develop` y `test` para evitar divergencia.

##### Repositorio documental

`proyecto-gimnasio-documentacion` mantiene únicamente `main`. Puede aceptar push directo por su protección reducida, aunque los cambios normativos o coordinados con código deberían usar una rama corta y PR para dejar visible la discusión. Siempre se ejecuta `quality`.

#### Flujo normal

```text
feature/* -> PR -> develop -> PR -> test -> PR -> main
                                  |             |
                                test        producción
```

1. Crear o asignar un issue con criterios de aceptación.
2. Crear la rama desde `develop`.
3. Abrir PR y mantenerlo acotado.
4. Exigir CI verde y aprobación de una persona distinta de quien hizo el último push.
5. Hacer squash merge a `develop`.
6. Abrir PR de promoción `develop -> test`; desplegar y ejecutar integración, evaluación y E2E.
7. Corregir fallos mediante ramas desde `develop` y volver a promover, sin commits exclusivos en `test`.
8. Abrir PR `test -> main`; exigir aprobación del dueño, checks y smoke test posterior.

Backend e IA se despliegan independientemente. Cuando cambia un contrato incompatible, primero se agrega una versión compatible, después se promueven consumidores y finalmente se retira la anterior.

Un cambio de modelo, prompt o parámetros requiere dataset de regresión verde y validación de al menos un entrenador antes de `main`.

#### Protección recomendada

Para `develop` y `test`:

- prohibir push directo, force-push y eliminación;
- exigir PR y una aprobación de otra persona;
- invalidar aprobaciones ante nuevos commits;
- exigir conversaciones resueltas y check `quality`;
- permitir squash merge.

Para `main`:

- aplicar las reglas anteriores;
- exigir aprobación del Code Owner propietario;
- impedir bypass de las reglas;
- deshabilitar auto-merge;
- exigir el environment `production` con aprobación manual del dueño.

Los despliegues de `test` usan el environment `test`. La aprobación habilita el merge, pero no lo ejecuta automáticamente.

#### Commits y versiones

Usar Conventional Commits en inglés:

```text
feat(training): persist completed sets
fix(auth): enforce student ownership
docs(ai): define online generation boundary
```

Las releases usan SemVer y tags `vX.Y.Z`; mientras el producto no sea estable, `v0.x.y`.


---

<a id="delivery-permissions"></a>

### Permisos y protección del repositorio

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/delivery/repository-permissions.md` · **Repositorio:** Documentación · **ID en el manifiesto:** `DELIVERY-PERMISSIONS`

#### Repositorios personales

Los cuatro repositorios pertenecen inicialmente a `Maico-Zurbriggen`. En repositorios personales los colaboradores tienen lectura y escritura, mientras las reglas de ramas restringen cómo integran cambios. `.github/CODEOWNERS` identifica a `@Maico-Zurbriggen` como dueño requerido para `main`.

Si se necesitan roles granulares, los repositorios deben transferirse a una organización.

#### Ruleset de `main`

- requerir pull request;
- requerir una aprobación del Code Owner propietario;
- descartar aprobaciones al agregar commits;
- requerir aprobación del último push por otra persona;
- exigir conversaciones resueltas y check `quality` actualizado;
- bloquear force-push, eliminación y bypass;
- permitir sólo squash merge;
- deshabilitar auto-merge.

#### Rulesets de `develop` y `test`

- requerir PR y una aprobación;
- exigir una persona distinta de quien realizó el último push;
- descartar aprobaciones obsoletas;
- exigir conversaciones resueltas y check `quality`;
- bloquear force-push y eliminación;
- impedir commits exclusivos en `test`: las correcciones nacen desde `develop` y se promueven.

#### Repositorio documental

`proyecto-gimnasio-documentacion` usa sólo `main` y protección reducida:

- historial lineal;
- force-push y eliminación bloqueados;
- sin aprobación, Code Owner ni check previo obligatorios;
- push directo permitido;
- CI `quality` posterior al push.

Los cambios normativos o coordinados con código deberían usar PR aunque GitHub no lo imponga.

#### Environments

- `test`: despliegues desde la rama `test`, con secretos de Neon Test y credenciales test de IA.
- `production`: despliegues sólo desde `main`, con aprobación manual del propietario.

Los secretos de producción no están disponibles en PRs, `develop`, `test` ni computadoras locales.

#### Verificación

1. Push directo a ramas protegidas: rechazado.
2. PR sin aprobación: no fusionable.
3. Nuevo commit: aprobación descartada.
4. `test` sólo recibe promociones desde `develop`.
5. `main` sólo habilita merge con aprobación del dueño y CI verde.
6. Auto-merge no aparece disponible.


---

<a id="parte-xi"></a>

## Parte XI — Repositorios de código

<a id="repo-frontend-readme"></a>

### Frontend — README

> **Origen:** `Frontend/proyecto-gimnasio/README.md` · **Repositorio:** Frontend · **ID en el manifiesto:** `—`

SPA React de la plataforma de entrenamiento asistido.

#### Responsabilidad

- presentar flujos de alumno, entrenador y administrador;
- mantener la sesión activa usable desde 360 px;
- consumir exclusivamente la API REST del backend;
- gestionar estado remoto con TanStack Query;
- seguir generaciones asíncronas mediante polling al backend;
- mostrar presets del gimnasio cuando generación no esté disponible.

Frontend no accede a PostgreSQL, Prisma, servicio IA, ngrok ni LLM. El OpenAPI del backend es la fuente de verdad para tipos y cliente HTTP.

#### Requisitos

- Node.js 24 o superior;
- npm 11.6 o superior.

#### Inicio local

```bash
npm ci
cp .env.example .env
npm run dev
```

En PowerShell, usar `Copy-Item .env.example .env`. La aplicación queda en `http://localhost:5173` y espera el backend configurado por `VITE_API_URL`.

#### Verificación

```bash
npm run check
```

#### Repositorios relacionados

- Backend: `proyecto-gimnasio-back`.
- Servicio IA y analítica: `proyecto-gimnasio-ia`.
- Documentación canónica: [proyecto-gimnasio-documentacion](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-documentacion).

Para trabajo asistido por IA, comenzar por `AGENTS.md` y el `manifest.json` del repositorio documental.


---

<a id="repo-frontend-agents"></a>

### Frontend — AGENTS (instrucciones del repositorio)

> **Origen:** `Frontend/proyecto-gimnasio/AGENTS.md` · **Repositorio:** Frontend · **ID en el manifiesto:** `—`

#### Contexto

Este repositorio contiene la SPA React de la plataforma. Backend Express y el servicio Python de IA son repositorios independientes. El servicio IA orquesta de forma asíncrona el LLM alojado en el Polo y también contendrá jobs analíticos batch; frontend no conoce ninguno de esos límites.

La documentación canónica vive en `Maico-Zurbriggen/proyecto-gimnasio-documentacion`. Con repositorios hermanos, leer primero `../proyecto-gimnasio-documentacion/AGENTS.md` y usar `manifest.json`. Si no está disponible localmente, consultar GitHub; no reconstruir reglas por memoria ni copiar documentación aquí.

#### Responsabilidad

- Construir una SPA React móvil primero, plenamente usable a 360 px.
- Consumir exclusivamente el OpenAPI público del backend mediante cliente generado.
- No acceder a PostgreSQL, Prisma, IA, ngrok, LLM ni proveedores externos.
- Mantener reglas de negocio y autorización en backend.
- Usar TanStack Query para estado remoto; reservar estado global para necesidades demostradas.
- Conservar localmente el identificador de una generación activa para recuperarla tras recargar.

#### Generación asíncrona

- Crear la solicitud en backend y consultar su estado mediante polling; nunca mantener una petición abierta esperando al LLM.
- Detener polling en estados terminales y diseñar carga, reintento, error e indisponibilidad.
- Si generación no está disponible, deshabilitar esa sección y mantener visibles los presets publicados del gimnasio.
- Toda salida es candidato; no presentarla como rutina vigente antes de la aprobación del entrenador.
- No implementar lógica de compatibilidad o permisos sólo en cliente.

#### Convenciones

- Organizar por feature cuando aparezcan funcionalidades.
- Diseñar carga, vacío, error y reintento junto con el camino feliz.
- Cumplir accesibilidad por teclado, etiquetas y contraste; no comunicar sólo por color.
- Conservar localmente el borrador de sesión activa con estrategia de sincronización explícita.
- Mantener el SVG muscular inline y controlado por props; no agregar canvas, WebGL ni 3D.
- Nombrar dominio con `product/glossary.md` del repositorio documental.

#### Forma de trabajo

- Crear ramas desde `develop`; todo cambio entra por PR.
- Promover `develop → test → main`; no crear commits exclusivos en `test`.
- Usar Conventional Commits en inglés.
- No agregar dependencias de producción sin justificar su necesidad.
- Actualizar el cliente generado en el mismo PR que adopte un contrato backend nuevo.
- Relacionar PR de código y documental cuando cambie contrato, regla o flujo.

#### Verificación

- Ejecutar `npm run check` antes de cerrar una tarea.
- Agregar pruebas de interacción para flujos y Playwright sólo para recorridos E2E críticos.

#### Code Review Rules

- Señalar permisos confiados sólo al cliente.
- Señalar interfaces de sesión que pierdan datos ante una interrupción.
- Señalar DTO manuales que deberían provenir de OpenAPI.
- Señalar estado remoto copiado innecesariamente a stores globales.
- Señalar llamadas directas a IA, ngrok o LLM.


---

<a id="repo-backend-readme"></a>

### Backend — README

> **Origen:** `Backend/proyecto-gimnasio-back/README.md` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

API REST Express + TypeScript, Prisma y PostgreSQL. Se despliega en Vercel, persiste en Neon y orquesta solicitudes hacia el servicio Python del Polo mediante su API expuesta por ngrok.

#### Requisitos

- Node.js 24 o superior;
- npm 11.6 o superior;
- acceso autorizado a Neon Test;
- credencial test del servicio IA cuando se prueba integración real;
- Docker Desktop, únicamente para quienes creen migraciones.

#### Inicio local

```bash
npm ci
cp .env.example .env
npm run db:generate
npm run dev
```

En PowerShell, usar `Copy-Item .env.example .env`. La API queda en `http://localhost:3000`.

- `GET /health` verifica que el proceso HTTP esté disponible.
- `GET /ready` ejecuta una consulta mínima contra PostgreSQL y devuelve `503` si Neon no está disponible.

`DATABASE_URL` debe ser la conexión pooled de `backend_test`; el hostname de Neon contiene `-pooler`. `CORS_ORIGINS` acepta orígenes separados por comas y debe incluir `http://localhost:5173` para desarrollo local.

Hasta que exista la primera migración, `npm run db:status` informa correctamente que la base todavía no está administrada por Prisma Migrate. Para verificar la conexión inicial usar `GET /ready`.

#### Despliegue en Vercel

Vercel detecta `src/app.ts` como la entrada Express. `src/main.ts` se usa solamente para levantar el servidor local. Las Functions se ejecutan en São Paulo (`gru1`) para mantenerlas cerca de Neon `sa-east-1`.

- Preview asociado a `test`: `DATABASE_URL` de `backend_test` y URL del frontend Test en `CORS_ORIGINS`.
- Production asociado a `main`: `DATABASE_URL` de `backend_production` y URL del frontend productivo en `CORS_ORIGINS`.
- No configurar roles `migrator` ni credenciales administrativas en Vercel.

Tras cambiar una variable de entorno, volver a desplegar para aplicarla.

#### Base de datos

El backend local usa Neon Test compartida. No ejecutar `prisma migrate reset`, `prisma db push`, seeds destructivos ni `migrate dev` sobre esa base. Las migraciones se aplican desde CI mediante `npm run db:deploy`.

##### Crear una migración

Sólo el autor de una migración levanta PostgreSQL efímero:

```powershell
docker compose -f compose.migrations.yaml up -d --wait
$previousDatabaseUrl = $env:DATABASE_URL
$env:DATABASE_URL = "postgresql://gym_migrator@localhost:55432/gym_migrations?schema=public"
npm run db:migrate -- --name nombre_descriptivo
npm run db:status
npm run check
```

Revisar el SQL generado y comprobar que todo el historial se aplica sobre una base vacía:

```powershell
docker compose -f compose.migrations.yaml down
docker compose -f compose.migrations.yaml up -d --wait
npm run db:deploy
npm run db:status
docker compose -f compose.migrations.yaml down
```

Restaurar la conexión que tenía la terminal:

```powershell
if ($null -eq $previousDatabaseUrl) {
  Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
} else {
  $env:DATABASE_URL = $previousDatabaseUrl
}
```

El PR incluye `schema.prisma`, la migración generada y sus pruebas. Nunca se modifica una migración ya integrada. Los datos del contenedor no persisten después de detenerlo.

Antes de cambiar el esquema, consultar [operations/local-database.md](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-documentacion/blob/main/operations/local-database.md).

##### Promoción

- `test`: GitHub Actions aplica las migraciones en Neon Test con el secret de su environment.
- `main`: GitHub Actions espera la aprobación del environment `Production` y luego aplica las migraciones en Neon Producción.
- Vercel conserva únicamente la credencial runtime con pooler; nunca recibe el rol migrador.

#### Verificación

```bash
npm run check
```

El backend publica OpenAPI como contrato para el frontend. El corpus funcional, la arquitectura y las reglas de dominio se mantienen exclusivamente en [proyecto-gimnasio-documentacion](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-documentacion). Para trabajo asistido por IA, comenzar por su `AGENTS.md` y `manifest.json`.


---

<a id="repo-backend-agents"></a>

### Backend — AGENTS (instrucciones del repositorio)

> **Origen:** `Backend/proyecto-gimnasio-back/AGENTS.md` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

#### Contexto

Este repositorio contiene la API Express + TypeScript, Prisma y las migraciones PostgreSQL. El frontend React y el motor batch Python viven en repositorios independientes. Antes de implementar una historia, consultar el documento funcional correspondiente en `docs/`.
Este repositorio contiene la API Express + TypeScript, Prisma y las migraciones PostgreSQL. El frontend React y el motor batch Python viven en repositorios independientes.

La documentación canónica vive en `Maico-Zurbriggen/proyecto-gimnasio-documentacion`. Cuando los repositorios están clonados como carpetas hermanas, leer primero `../proyecto-gimnasio-documentacion/AGENTS.md` y usar su `manifest.json` para seleccionar el contexto de la tarea. Si

#### Responsabilidad

- Mantener un monolito modular desplegable en Vercel.
- Hacer cumplir invariantes, autorización, transacciones y contratos HTTP.
- Separar módulos por dominio al implementar historias verticales.
- Mantener `app.ts` libre del arranque para probar con Supertest.
- Usar routers y middleware explícitos; no crear un framework interno.
- Mantener Prisma como infraestructura; no exponer modelos ORM.
- Publicar OpenAPI como fuente de verdad del frontend.

#### Dominio y seguridad

- Autorizar en dos pasos: rol y propiedad/asignación del recurso. Probar ambos.
- Usar cookies `httpOnly` para sesión; nunca guardar tokens en `localStorage`.
- Congelar la prescripción al iniciar una sesión y conservarla junto a los valores reales.
- Aplicar baja lógica cuando el historial dependa de una entidad.
- No modificar migraciones ya aplicadas. Crear una nueva y documentar cambios incompatibles.
- Actualizar OpenAPI en el mismo PR que cambie un contrato.
- Nombrar conceptos con los términos literales de `docs/D2-glosario.md`.
- Nombrar conceptos con los términos literales de `product/glossary.md` del repositorio documental.

#### Integración IA

- Encapsular el servicio IA detrás de un cliente generado o validado desde su OpenAPI.
- Frontend nunca conoce la URL de IA; backend es el único consumidor.
- Crear una solicitud idempotente, minimizar el contexto y aceptar el flujo asíncrono con `202`.
- Leer estados y resultados de estructuras de integración; validar catálogo, compatibilidad, rangos y permisos antes de crear un candidato.
- Cada intento vence inicialmente a los 120 segundos y admite un único reintento.
- Tras el segundo fallo declarar generación no disponible; no implementar fallback determinístico.
- Mantener disponibles los presets publicados del gimnasio, siempre sujetos a aprobación del entrenador.
- Usar credenciales distintas para test y producción. No enviar URLs de base, datos identificatorios innecesarios ni secretos al Polo.
- Los tests pueden simular transporte HTTP; no agregar un modo fake ejecutable.

#### Forma de trabajo

- Crear ramas desde `develop`; todo cambio entra por pull request.
- Usar Conventional Commits en inglés: `type(scope): summary`.
- No agregar dependencias de producción sin justificar su necesidad en el PR.
- Relacionar el PR de código con el PR documental cuando cambie un contrato, una regla, una migración conceptual o un flujo.

#### Verificación

- Ejecutar `npm run check`.
- Priorizar unitarias para reglas, API tests para permisos y persistencia para integración.
- Probar idempotencia, timeout, reintento, rol IA restringido y aislamiento test/producción.

#### Code Review Rules

- Señalar routers con lógica de dominio o Prisma directo.
- Señalar identificadores de alumno sin prueba 403 de acceso ajeno.
- Señalar migraciones destructivas sobre la base compartida.
- Señalar llamadas al LLM desde backend o trabajos Python dentro de una petición.
- Exigir test para regla, permiso y corrección de bug.


---

<a id="repo-ia-readme"></a>

### Servicio de IA y analítica — README

> **Origen:** `IA/proyecto-gimnasio-ia/README.md` · **Repositorio:** IA · **ID en el manifiesto:** `—`

Servicio Python de generación online y procesos batch de análisis y machine learning.

#### Responsabilidad

##### Generación online

- exponer un OpenAPI versionado para backend;
- aceptar solicitudes asíncronas e idempotentes;
- orquestar el LLM alojado en el Polo;
- persistir estados y resultados en estructuras autorizadas de Neon;
- registrar modelo, configuración, contrato e instante;
- no crear ni aprobar rutinas.

##### Analítica batch

- construir features point-in-time;
- entrenar y evaluar contra criterios simples;
- calcular resultados reproducibles;
- escribir salidas precalculadas para backend.

#### Despliegue objetivo

API y worker se ejecutan en el Polo. Ngrok expone únicamente la API Python mediante un dominio estable. El LLM permanece local o privado y no accede a PostgreSQL.

#### Requisitos actuales

- Python 3.13;
- acceso autorizado a Neon Test;
- acceso a la API del LLM del Polo para integración real.

#### Inicio local

```bash
python -m venv .venv
# Activar el entorno virtual
python -m pip install -e ".[dev]"
cp .env.example .env
```

Las dependencias HTTP y los comandos de API/worker se incorporarán con el esqueleto de integración. Backend es dueño de las migraciones; este repositorio no ejecuta cambios de esquema.

#### Verificación

```bash
python -m ruff check .
python -m mypy src
python -m pytest
```

La interfaz de datos con el backend está descrita en `docs/data-interface.md`. El corpus funcional compartido está indexado en `docs/README.md`.
La interfaz con el backend está descrita en `architecture/data-interface.md` del [repositorio documental](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-documentacion). Allí también viven el corpus funcional, la arquitectura y las reglas de dominio. Para trabajo asistido por IA, comenzar por su `AGENTS.md` y `manifest.json`.


---

<a id="repo-ia-agents"></a>

### Servicio de IA y analítica — AGENTS (instrucciones del repositorio)

> **Origen:** `IA/proyecto-gimnasio-ia/AGENTS.md` · **Repositorio:** IA · **ID en el manifiesto:** `—`

#### Contexto

Este repositorio contiene los procesos batch Python de análisis y machine learning. La API Express y el frontend React viven en repositorios independientes. Antes de implementar una tarea, consultar el documento funcional correspondiente en `docs/`.

La documentación canónica vive en `Maico-Zurbriggen/proyecto-gimnasio-documentacion`. Con repositorios hermanos, leer primero `../proyecto-gimnasio-documentacion/AGENTS.md` y usar `manifest.json`. Si no está local, consultar GitHub; no copiar documentación aquí.

#### Servicio generativo

- Mantener separados API, autenticación, contratos, orquestación, conector LLM, persistencia y worker.
- Publicar OpenAPI versionado como fuente de verdad para backend.
- Aceptar solicitudes idempotentes con `202`; nunca esperar al LLM dentro de la petición.
- Procesar mediante worker durable capaz de recuperar trabajos tras un reinicio.
- Llamar al LLM sólo mediante un conector privado y validar su salida estructural.
- Escribir únicamente estados y resultados en estructuras de integración acordadas.
- No crear, aprobar, asignar ni activar rutinas; backend conserva reglas y autoridad.
- Cada intento vence inicialmente a los 120 segundos y admite un único reintento.
- Tras el segundo fallo registrar indisponibilidad; no generar fallback determinístico.

#### Datos y seguridad

- Construir features point-in-time: ninguna fila puede usar información posterior al instante predicho.
- Separar train, validation y test por tiempo o usuario; documentar la elección.
- Comparar todo modelo contra un criterio de referencia simple.
- Preferir una regla cuando el modelo no aporte una mejora medible.
- Fijar seeds, versiones, parámetros y artefactos necesarios para reproducir resultados.
- No usar datos personales reales ni subir datasets sensibles, modelos grandes o notebooks con salidas privadas.
- Los notebooks son exploratorios; la lógica aceptada debe migrar a módulos y tests.
- Nombrar conceptos con los términos literales de `product/glossary.md` del repositorio documental.

#### Forma de trabajo

- Crear ramas desde `develop`; todo cambio entra por pull request.
- Usar Conventional Commits en inglés: `type(scope): summary`.
- Coordinar mediante PR relacionados cualquier cambio en la interfaz de datos con el backend.
- Relacionar el PR de código con el PR documental cuando cambie un dataset, una regla, una métrica o un flujo.

#### Verificación

- Ejecutar `python -m ruff check .`.
- Ejecutar `python -m mypy src`.
- Ejecutar `python -m pytest`.
- Probar idempotencia, reinicio del worker, timeout, reintento, permisos PostgreSQL y aislamiento de ambientes.

#### Code Review Rules

- Bloquear espera del LLM dentro de la petición HTTP.
- Bloquear acceso a tablas de dominio o datos identificatorios innecesarios.
- Bloquear resultados sin modelo, configuración, instante y contexto reproducible.
- Bloquear cambios de IA sin evaluación y revisión humana requerida.
- Bloquear fuga temporal o splits no reproducibles en jobs batch.


---

<a id="anexos"></a>

## Anexos

<a id="anexo-manifest"></a>

### Anexo A — manifest.json: mapa de enrutamiento del corpus

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/manifest.json` · **Repositorio:** Documentación · **ID en el manifiesto:** `—`

```json
{
  "schema_version": 1,
  "corpus_version": "3.0",
  "updated_at": "2026-09-01",
  "purpose": "Deterministic routing map for humans and AI agents. Paths are canonical and unique.",
  "repositories": {
    "frontend": "https://github.com/Maico-Zurbriggen/proyecto-gimnasio",
    "backend": "https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back",
    "analytics": "https://github.com/Maico-Zurbriggen/proyecto-gimnasio-ia",
    "documentation": "https://github.com/Maico-Zurbriggen/proyecto-gimnasio-documentacion"
  },
  "documents": [
    {"id":"INDEX-CORPUS","path":"corpus-guide.md","scope":"system","authoritative_for":["reading order","corpus status"],"load_when":["starting project work","planning documentation changes"]},
    {"id":"D1","path":"product/vision-and-objectives.md","scope":"product","authoritative_for":["vision","scope","success criteria"],"load_when":["starting any feature","prioritizing scope"]},
    {"id":"D2","path":"product/glossary.md","scope":"system","authoritative_for":["terminology","closed enumerations"],"load_when":["writing code","writing documentation","designing contracts"]},
    {"id":"D3","path":"domain/actors-roles-permissions.md","scope":"domain","authoritative_for":["actors","roles","access rules"],"load_when":["authentication","authorization","user flows"]},
    {"id":"D4","path":"domain/domain-model.md","scope":"domain","authoritative_for":["entities","relationships","integrity constraints"],"load_when":["database changes","API design","analytics schema"]},
    {"id":"D5","path":"domain/business-rules.md","scope":"domain","authoritative_for":["business rules","constants","calculations"],"load_when":["implementing validation","implementing calculations","changing behavior"]},
    {"id":"D6","path":"domain/lifecycles-and-states.md","scope":"domain","authoritative_for":["states","transitions","forbidden transitions"],"load_when":["implementing stateful entities","designing workflows"]},
    {"id":"D10","path":"domain/edge-cases.md","scope":"domain","authoritative_for":["edge cases","failure behavior"],"load_when":["implementing a feature","writing tests","reviewing completion"]},
    {"id":"D7","path":"flows/functional-flows.md","scope":"product","authoritative_for":["end-to-end functional flows"],"load_when":["implementing a user journey","designing UI","designing API"]},
    {"id":"D8","path":"requirements/functional-requirements.md","scope":"product","authoritative_for":["functional requirements","priority","dependencies"],"load_when":["planning","estimating","acceptance review"]},
    {"id":"D9","path":"requirements/non-functional-requirements.md","scope":"system","authoritative_for":["quality attributes","verification criteria"],"load_when":["test strategy","security","performance","reliability"]},
    {"id":"D13","path":"requirements/traceability.md","scope":"system","authoritative_for":["requirement traceability","coverage gaps"],"load_when":["changing scope","auditing coverage","preparing a release"]},
    {"id":"ARCH-SYSTEM","path":"architecture/system-overview.md","scope":"system","authoritative_for":["repository topology","system boundaries","integration ownership"],"load_when":["starting technical work","changing an integration"]},
    {"id":"ARCH-FRONTEND","path":"architecture/frontend.md","scope":"frontend","authoritative_for":["frontend boundary","frontend responsibilities"],"load_when":["frontend architecture","frontend integration"]},
    {"id":"ARCH-BACKEND","path":"architecture/backend.md","scope":"backend","authoritative_for":["backend boundary","backend responsibilities"],"load_when":["backend architecture","API design","persistence"]},
    {"id":"ARCH-DATABASE","path":"architecture/database-relational-model.md","scope":"backend,analytics","authoritative_for":["PostgreSQL tables","database relations","database constraints","AI integration storage"],"load_when":["database changes","writing migrations","seeding data","implementing persistence"]},
    {"id":"ARCH-ANALYTICS","path":"architecture/analytics-engine.md","scope":"analytics","authoritative_for":["online AI service boundary","batch pipeline","analytics boundary"],"load_when":["analytics work","generative AI service work","model lifecycle"]},
    {"id":"ARCH-DATA-INTERFACE","path":"architecture/data-interface.md","scope":"backend,analytics","authoritative_for":["backend-AI persistence contract","backend-analytics data contract"],"load_when":["changing AI persistence","changing datasets","changing snapshots","persisting scores"]},
    {"id":"ARCH-GENERATIVE-AI","path":"architecture/generative-ai-integration.md","scope":"system","authoritative_for":["generative AI deployment topology","AI environments","AI test strategy"],"load_when":["deploying the AI service","configuring AI environments","testing AI integration"]},
    {"id":"ARCH-AI-MODEL-SELECTION","path":"architecture/ai-model-selection.md","scope":"analytics","authoritative_for":["generative model comparison","LLM runtime comparison"],"load_when":["selecting an LLM","selecting an LLM runtime","verifying Polo hardware"]},
    {"id":"ARCH-GENERATIVE-AI-SCOPE","path":"architecture/generative-ai.md","scope":"analytics","authoritative_for":["generative AI functional scope","AI Gateway contract","prompting","guardrails","deterministic safeguards around LLM output"],"load_when":["implementing generative behavior","changing a prompt or model","reviewing LLM responsibilities"]},
    {"id":"ARCH-PREDICTIVE-AI","path":"architecture/predictive-ai.md","scope":"analytics","authoritative_for":["predictive component proposals","predictive model lifecycle"],"load_when":["evaluating predictive features","implementing predictive models"]},
    {"id":"D11","path":"decisions/design-decisions.md","scope":"system","authoritative_for":["product design decisions"],"load_when":["questioning existing behavior","proposing a design change"]},
    {"id":"ADR-0001","path":"decisions/adr/0001-monorepo-and-batch-engine.md","scope":"historical","authoritative_for":["superseded monorepo decision"],"load_when":["reviewing repository history"]},
    {"id":"ADR-0002","path":"decisions/adr/0002-three-repositories.md","scope":"system","authoritative_for":["three-code-repository decision"],"load_when":["changing repository boundaries"]},
    {"id":"ADR-0003","path":"decisions/adr/0003-central-documentation-repository.md","scope":"system","authoritative_for":["documentation ownership","documentation topology"],"load_when":["adding documentation","moving documentation"]},
    {"id":"ADR-0009","path":"decisions/adr/0009-servicio-generativo-online-en-el-polo.md","scope":"system","authoritative_for":["online generative service decision","Polo and ngrok deployment boundary","generation failure policy"],"load_when":["implementing generative AI","deploying AI service","changing AI availability behavior"]},
    {"id":"ADR-0004-SELF-HOSTED-LLM","path":"decisions/adr/0004-self-hosted-llm-server.md","scope":"analytics","authoritative_for":["self-hosted LLM decision"],"load_when":["deploying the LLM","evaluating external LLM providers"]},
    {"id":"ADR-0005-AI-GATEWAY","path":"decisions/adr/0005-ai-gateway-in-process-module.md","scope":"backend,analytics","authoritative_for":["AI gateway port-and-adapter pattern"],"load_when":["implementing the AI gateway","changing backend-AI boundaries"]},
    {"id":"ADR-0006-LLM-RUNTIME","path":"decisions/adr/0006-llm-model-and-runtime-selection.md","scope":"analytics","authoritative_for":["LLM model decision","LLM runtime decision"],"load_when":["deploying the LLM","changing model or runtime"]},
    {"id":"ADR-0007-NO-RAG","path":"decisions/adr/0007-no-rag.md","scope":"analytics","authoritative_for":["RAG exclusion decision","deterministic exercise prefiltering"],"load_when":["designing LLM context","evaluating retrieval"]},
    {"id":"ADR-0008-ML-TOOLS","path":"decisions/adr/0008-tool-calling-for-ml-components.md","scope":"analytics","authoritative_for":["ML component tool-calling decision"],"load_when":["integrating classic ML with the LLM","designing AI tools"]},
    {"id":"D12","path":"planning/risks-and-assumptions.md","scope":"project","authoritative_for":["assumptions","risks","capacity","scope cuts"],"load_when":["planning","committing dates","recording an unresolved point"]},
    {"id":"PLAN-BASELINE","path":"planning/baseline-alcance-2026-09.md","scope":"project","authoritative_for":["stage scope","requirement vote traceability","build order","documentation debt"],"load_when":["planning a sprint","questioning whether something is in scope","estimating","auditing documentation debt"]},
    {"id":"OPS-LOCAL-DB","path":"operations/local-database.md","scope":"backend","authoritative_for":["shared Neon Test workflow","Prisma migration workflow"],"load_when":["setting up backend locally","changing database schema"]},
    {"id":"DELIVERY-GITHUB","path":"delivery/github-workflow.md","scope":"delivery","authoritative_for":["branches","pull requests","releases"],"load_when":["creating a branch","opening a pull request","preparing a release"]},
    {"id":"DELIVERY-PERMISSIONS","path":"delivery/repository-permissions.md","scope":"delivery","authoritative_for":["repository permissions","branch protection"],"load_when":["administering repositories","reviewing access"]},
    {"id":"DELIVERABLE-PO-GENERATIVE-AI","path":"deliverable PO/alcance-ia-generativa.md","scope":"product","authoritative_for":["Product Owner generative AI deliverable","generative AI scope committed to the Product Owner"],"load_when":["reviewing committed generative AI scope","changing generative scope","presenting generative AI scope to the Product Owner"]},
    {"id":"MASTER-COMPILATION","path":"Documentacion_Maestra.md","scope":"system","authoritative_for":[],"load_when":["reading the whole corpus in a single file","onboarding a person to the entire project"],"note":"Non-normative compilation of every documented file, generated mechanically. Never edit it directly and never cite it as a source: each section states its canonical origin file, and that file always wins."}
  ]
}
```


---

<a id="anexo-check-docs"></a>

### Anexo B — tools/check_docs.py: validador del corpus

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/tools/check_docs.py` · **Repositorio:** Documentación · **ID en el manifiesto:** `—`

```python
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = {"README.md", "AGENTS.md"}
LINK = re.compile(r"!?\[[^]]*]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    documents = manifest.get("documents", [])
    ids = [document["id"] for document in documents]
    paths = [document["path"] for document in documents]

    if len(ids) != len(set(ids)):
        fail(errors, "manifest.json contains duplicate document ids")
    if len(paths) != len(set(paths)):
        fail(errors, "manifest.json contains duplicate document paths")

    markdown_paths = {
        path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.md")
    }
    registered = set(paths)
    unregistered = markdown_paths - registered - ENTRYPOINTS
    missing = registered - markdown_paths
    for path in sorted(unregistered):
        fail(errors, f"unregistered Markdown document: {path}")
    for path in sorted(missing):
        fail(errors, f"manifest path does not exist: {path}")

    hashes: dict[str, str] = {}
    for relative in sorted(markdown_paths):
        path = ROOT / relative
        content = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
        if digest in hashes:
            fail(errors, f"duplicate Markdown content: {relative} and {hashes[digest]}")
        hashes[digest] = relative

        for raw_target in LINK.findall(content):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target_path).resolve()
            if not resolved.is_relative_to(ROOT):
                fail(errors, f"link escapes repository: {relative} -> {target}")
            elif not resolved.exists():
                fail(errors, f"broken relative link: {relative} -> {target}")

    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(markdown_paths)} Markdown files and {len(documents)} manifest entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```


---

<a id="anexo-pr-template"></a>

### Anexo C — Plantilla de pull request (idéntica en los tres repositorios de código)

> **Origen:** `Backend/proyecto-gimnasio-back/.github/pull_request_template.md` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```markdown
## Qué cambia

<!-- Resumen breve y enlace al issue. -->

Closes #

## Cómo se validó

- [ ] Lint
- [ ] Typecheck
- [ ] Tests
- [ ] Build
- [ ] Prueba manual en 360 px si cambia una interfaz

## Impacto

- [ ] Cambia el contrato OpenAPI
- [ ] Incluye una migración nueva
- [ ] Cambia permisos o acceso a datos
- [ ] Cambia métricas, features o modelos
- [ ] Incluye fallback para una dependencia externa

## Evidencia

<!-- Capturas, salida relevante o explicación de por qué no aplica. -->
```


---

<a id="anexo-issue-bug"></a>

### Anexo D.1 — Plantilla de issue: reporte de error

> **Origen:** `Backend/proyecto-gimnasio-back/.github/ISSUE_TEMPLATE/bug.yml` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```yaml
name: Bug
description: Reportar un comportamiento incorrecto y reproducible.
title: '[Bug]: '
labels: [bug]
body:
  - type: textarea
    id: current
    attributes:
      label: Comportamiento actual
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Comportamiento esperado
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Pasos para reproducir
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Evidencia y entorno
      description: Capturas, logs sanitizados, navegador, commit o ambiente.
```


---

<a id="anexo-issue-feature"></a>

### Anexo D.2 — Plantilla de issue: funcionalidad

> **Origen:** `Backend/proyecto-gimnasio-back/.github/ISSUE_TEMPLATE/feature.yml` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```yaml
name: Historia o feature
description: Proponer una unidad vertical de valor.
title: '[Feature]: '
labels: [feature]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problema
      description: Qué necesita el actor y por qué.
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Criterios de aceptación
      description: Condiciones observables y verificables.
      placeholder: |
        - [ ] Dado ..., cuando ..., entonces ...
    validations:
      required: true
  - type: dropdown
    id: area
    attributes:
      label: Área principal
      options:
        - Frontend
        - Backend
        - Motor analítico
        - Transversal
    validations:
      required: true
  - type: textarea
    id: out-of-scope
    attributes:
      label: Fuera de alcance
      description: Qué no se resolverá en esta historia.
```


---

<a id="anexo-codeowners"></a>

### Anexo E — CODEOWNERS (idéntico en los tres repositorios de código)

> **Origen:** `Backend/proyecto-gimnasio-back/.github/CODEOWNERS` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```text
# Mientras el repositorio pertenezca a una cuenta personal, el propietario
# revisa cualquier cambio destinado a main.
* @Maico-Zurbriggen
```


---

<a id="anexo-ci-docs"></a>

### Anexo F.1 — CI del repositorio documental

> **Origen:** `Documentación/proyecto-gimnasio-documentacion/.github/workflows/quality.yml` · **Repositorio:** Documentación · **ID en el manifiesto:** `—`

```yaml
name: Documentation quality

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Validate corpus
        run: python tools/check_docs.py
```


---

<a id="anexo-ci-frontend"></a>

### Anexo F.2 — CI del frontend

> **Origen:** `Frontend/proyecto-gimnasio/.github/workflows/ci.yml` · **Repositorio:** Frontend · **ID en el manifiesto:** `—`

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main, develop]

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      - name: Install JavaScript dependencies
        run: npm ci

      - name: Check repository
        run: npm run check
```


---

<a id="anexo-ci-backend"></a>

### Anexo F.3 — CI del backend

> **Origen:** `Backend/proyecto-gimnasio-back/.github/workflows/ci.yml` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main, test, develop]

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    services:
      postgres:
        image: postgres:17-alpine
        env:
          POSTGRES_DB: gym_ci
          POSTGRES_USER: gym_ci
          POSTGRES_HOST_AUTH_METHOD: trust
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U gym_ci -d gym_ci"
          --health-interval 2s
          --health-timeout 5s
          --health-retries 15

    env:
      DATABASE_URL: postgresql://gym_ci@localhost:5432/gym_ci?schema=public

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Apply migrations to a clean database
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:deploy

      - name: Verify migration status
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:status

      - name: Check repository
        run: npm run check
```


---

<a id="anexo-ci-migrations"></a>

### Anexo F.4 — Workflow de migraciones del backend

> **Origen:** `Backend/proyecto-gimnasio-back/.github/workflows/migrations.yml` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```yaml
name: Database migrations

on:
  push:
    branches: [test, main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: database-migrations-${{ github.ref_name }}
  cancel-in-progress: false

jobs:
  migrate-test:
    name: migrate-test
    if: github.ref == 'refs/heads/test'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: test
    env:
      DATABASE_URL: ${{ secrets.MIGRATION_DATABASE_URL }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Apply pending migrations
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:deploy

      - name: Verify migration status
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:status

  migrate-production:
    name: migrate-production
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: Production
    env:
      DATABASE_URL: ${{ secrets.MIGRATION_DATABASE_URL }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Apply pending migrations
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:deploy

      - name: Verify migration status
        if: ${{ hashFiles('prisma/migrations/**/migration.sql') != '' }}
        run: npm run db:status
```


---

<a id="anexo-ci-ia"></a>

### Anexo F.5 — CI del servicio de IA

> **Origen:** `IA/proyecto-gimnasio-ia/.github/workflows/ci.yml` · **Repositorio:** IA · **ID en el manifiesto:** `—`

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main, develop]

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
          cache: pip

      - name: Install dependencies
        run: python -m pip install -e ".[dev]"

      - name: Lint
        run: python -m ruff check .

      - name: Typecheck
        run: python -m mypy src

      - name: Test
        run: python -m pytest
```


---

<a id="anexo-env-frontend"></a>

### Anexo G.1 — Variables de entorno del frontend

> **Origen:** `Frontend/proyecto-gimnasio/.env.example` · **Repositorio:** Frontend · **ID en el manifiesto:** `—`

```dotenv
VITE_API_URL=http://localhost:3000
```


---

<a id="anexo-env-backend"></a>

### Anexo G.2 — Variables de entorno del backend

> **Origen:** `Backend/proyecto-gimnasio-back/.env.example` · **Repositorio:** Backend · **ID en el manifiesto:** `—`

```dotenv
NODE_ENV=development
API_PORT=3000
# Lista separada por comas, sin barras finales.
CORS_ORIGINS=http://localhost:5173

# Neon Test. Reemplazar localmente con una credencial autorizada; nunca versionarla.
DATABASE_URL=postgresql://USER:PASSWORD@HOST-POOLER/DATABASE?sslmode=require&channel_binding=require&connect_timeout=30

# Servicio Python expuesto mediante el dominio estable de ngrok.
AI_SERVICE_URL=https://gimnasio-ia.ngrok.app
AI_SERVICE_AUTH_MODE=api_key
AI_SERVICE_API_KEY=
AI_GENERATION_TIMEOUT_SECONDS=120
AI_GENERATION_MAX_RETRIES=1
AI_RESULT_RETENTION_DAYS=30
```


---

<a id="anexo-env-ia"></a>

### Anexo G.3 — Variables de entorno del servicio de IA

> **Origen:** `IA/proyecto-gimnasio-ia/.env.example` · **Repositorio:** IA · **ID en el manifiesto:** `—`

```dotenv
APP_ENV=test
API_HOST=127.0.0.1
API_PORT=8000

# Neon Test con el rol restringido del servicio IA.
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require

# Backend -> servicio IA. Test y producción usan secretos distintos en el Polo.
AI_SERVICE_API_KEY_TEST=
AI_SERVICE_API_KEY_PRODUCTION=

# Servicio IA -> LLM del Polo. El mecanismo definitivo sigue pendiente.
LLM_API_URL=http://127.0.0.1:9000
LLM_AUTH_MODE=api_key
LLM_API_KEY=

GENERATION_TIMEOUT_SECONDS=120
GENERATION_MAX_RETRIES=1
FAILED_RESULT_RETENTION_DAYS=30

# NGROK_AUTHTOKEN pertenece a la configuración del agente ngrok, no a la aplicación.
```
