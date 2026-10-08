# Corpus documental — Plataforma de entrenamiento asistido

**Versión del corpus** 4.0 · **Fecha** 2026-10-07 · **Estado** implementación local de catálogo y generación actualizada por [ADR 0013](decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md), pendiente de curación del dataset real, promoción y evaluación profesional. Los demás alcances conservan su baseline y decisiones posteriores.

La v4.0 implementa localmente [RepDB y habilitaciones por gimnasio](architecture/exercise-catalog.md), contexto completo del alumno y selección/prescripción con IA. Retira el prefiltrado, top 32 y validación determinista de entrenamiento; conserva controles técnicos y revisión humana. Los snapshots físicos y diagramas implementados distinguen lo existente de lo diseñado. `Documentacion_Maestra.md` es una compilación histórica y no incluye esta actualización; consultar los archivos canónicos.

La v2.0 incorpora las 42 correcciones de la auditoría y las dos definiciones del cliente que las hicieron posibles: **el sistema no es abierto** (el gimnasio afilia e invita) y **el equipamiento es del gimnasio** (la prescripción depende de qué máquinas tiene).

La v2.1 incorpora el **candidato de rutina**: el solicitante moldea la rutina generada antes de enviarla a revisión, sin tocar la prescripción y sin mover la puerta del entrenador. Toca D3, D5, D6, D7, D8, D10, D11 y D12. Ver D11/DD-33.

La v2.2 centraliza el corpus en un repositorio documental único, organiza las rutas por responsabilidad y agrega `manifest.json` como mapa determinista para agentes. No modifica reglas funcionales.

La v2.3 incorpora una [propuesta de integración generativa](architecture/generative-ai-integration.md) con ambientes, trabajo local, promoción y pruebas. Declara tres diferencias que requieren ADR antes de cambiar la arquitectura o los requisitos vigentes.

La v2.4 aceptó [ADR 0009](decisions/adr/0009-servicio-generativo-online-en-el-polo.md): servicio Python y worker en el Polo, ingreso por ngrok, LLM separado, generación asíncrona y Neon Test compartida. También adoptó la promoción `develop → test → main`.

**La v3.0 incorpora el [baseline de alcance de la Etapa 1](planning/baseline-alcance-2026-09.md)**, que cruza la votación del equipo con el Acta de Redefinición y con el estado real de los tres repositorios de código. Tres cosas que conviene saber antes de leer el resto del corpus:

1. **Existe una dimensión de alcance separada de la prioridad.** Un requisito puede ser MUST y estar diferido: la prioridad dice cuánto importa al producto, el alcance dice si se construye ahora. D8 v4.0 marca las dos.
2. **Estado histórico de la v3.0.** La implementación posterior tiene [referencia física](architecture/database-schema-reference.md) y [secuencias](architecture/implemented-sequence-diagrams.md); el catálogo de ADR 0013 está implementado localmente; su publicación real y despliegue siguen pendientes.
3. **Se cerraron tres defectos estructurales del propio corpus:** DD-34 estaba citada por ocho documentos y nunca redactada · dos ADR compartían el número 0004 decidiendo cosas incompatibles · nueve documentos no estaban registrados en el manifiesto, con lo que la validación automática fallaba. Los tres están corregidos.

**La v3.1 confirma la baseline v4.0 y congela la frontera de persistencia de la Etapa 1.** No se crean candidato ajustable, comentarios, sesiones diferidas, desbloqueos, baja anonimizada ni tablas predictivas. Diagnósticos, propuestas, ajustes y récords se incorporan a `app`; generación conserva sólo sus solicitudes, intentos, resultados y validaciones en `ai_integration`. Lo diferido se agregará, si vuelve al alcance, mediante migraciones futuras.

**La v3.2 traslada la API y el worker Python a Vercel sin mover el LLM del Polo.** ADR 0010 reemplaza la ubicación decidida por ADR 0009: FastAPI acepta con `202`, Vercel Queues entrega el UUID de forma durable y un consumidor Python llama a Ollama mediante ngrok autenticado. Preview de `test` y Production de `main` conservan bases, URLs y secretos aislados.

**La v3.3 reemplaza ngrok por Cloudflare Tunnel para acceder al único LLM del Polo.** ADR 0011 define `LLM_API_URL` y un `LLM_API_TOKEN` Bearer compartidos inicialmente por test y producción; `AI_SERVICE_API_KEY` continúa separado por ambiente para autenticar backend hacia IA.

**La v3.6 reincorpora RF-025 por decisión del Product Owner.** Sólo el alumno autenticado solicita para sí una generación; backend finaliza técnicamente una salida válida como rutina `PROPUESTA` y el entrenador asignado conserva la aprobación exclusiva. El candidato editable de RF-119 y la comparación de RF-120 continúan diferidos.

**Y quedan dos preguntas abiertas que condicionan la planificación**, no la documentación: cuánta capacidad de construcción hay realmente (I-09 en D12/§5) y si el Product Owner libera el compromiso sobre la interpretación de lenguaje natural (I-10).

La v2.7 incorpora el [modelo relacional PostgreSQL](architecture/database-relational-model.md), contratos JSON versionados sin datos identificatorios, candidatos con vencimiento por inactividad y estados técnicos de generación. Los presets dejan de ser contingencia obligatoria y pasan a alcance `COULD`; la primera entrega conserva plantillas privadas y creación manual por entrenadores.

---

## Cómo leerlo

| Doc                                       | Contenido                                                                                             | Léelo si                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [D1](product/vision-and-objectives.md)                 | Visión, capacidad central, alcance y 13 criterios de éxito                                            | Es el criterio que juzga todo lo demás. **Empezá acá**                         |
| [D2](product/glossary.md)                              | Glosario normativo + **12 enumeraciones cerradas**                                                    | Vas a escribir cualquier cosa. Un término o un valor que no esté acá no se usa |
| [D3](domain/actors-roles-permissions.md) | Actores, roles y reglas de acceso, incluida habilitación por gimnasio | Trabajás en autorización |
| [D4](domain/domain-model.md) | Entidades, decisiones de modelado y restricciones de integridad | Vas a tocar la estructura de datos |
| [D5](domain/business-rules.md) | Reglas de negocio, constantes y límites de autoridad de IA | Implementás cualquier cálculo o validación |
| [D6](domain/lifecycles-and-states.md)                   | 10 ciclos de vida, con las transiciones **imposibles** y su motivo                                    | Implementás una entidad con estado                                             |
| [D7](flows/functional-flows.md) | Flujos, incluida habilitación de ejercicios (FL-23) | Implementás una funcionalidad completa |
| [D8](requirements/functional-requirements.md) | Requisitos con tipo, prioridad, alcance y dependencias | Planificás o estimás |
| [D9](requirements/non-functional-requirements.md)       | 40 requerimientos, todos con criterio de verificación                                                 | Definís la estrategia de pruebas                                               |
| [D10](domain/edge-cases.md) | Casos borde, incluida disponibilidad y contexto de IA (CB-83 a CB-88) | Antes de dar por terminada una funcionalidad |
| [D11](decisions/design-decisions.md) | Decisiones y reemplazos, incluido DD-36/ADR 0013 | Querés saber por qué algo es así |
| [D12](planning/risks-and-assumptions.md)                | 10 supuestos, **37 constantes con su origen**, 16 riesgos, aritmética del esfuerzo y orden de recorte | Sos responsable del plan. **Leelo antes de comprometer fechas**                |
| [D13](requirements/traceability.md)                     | Qué requerimiento responde a qué necesidad, y qué quedó sin cubrir                                    | Preparás la defensa o discutís alcance con el cliente                          |

## Las cuatro tablas que sostienen la prescripción

RN-39a es referencia para IA y entrenador; RN-44a a RN-44d describen su evaluación de adecuación. No validan la generación en código. RN-79a y RN-89a mantienen su alcance de diagnóstico/adaptación batch.

| Tabla                         | Dónde              | Qué determina                                                                                  |
| ----------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| Restricciones del tipo de rutina | D5/RN-39a | Referencias de entrenamiento para IA y revisión del entrenador |
| Compatibilidad | D5/RN-44a a RN-44d | Adecuación evaluada por IA y entrenador, sin exclusión en código |
| Criterios de diagnóstico      | D5/RN-79a          | Cuál de las cinco situaciones tiene cada ejercicio y el conjunto                               |
| Reglas de ajuste              | D5/RN-89a          | Qué ajuste, de qué tipo y de qué magnitud, corresponde a cada situación                        |

## Convención de marcado

`[F]` lo afirma una fuente · `[I]` inferencia · `[S]` convención de este proyecto, sin fuente externa · 👁 decisión que las fuentes tomaron sin advertirlo · 🆕 nuevo · ⬆⬇ cambio de prioridad · ✎ enunciado modificado · ⛔ derogado

## Lo que hay que resolver antes de escribir código

1. **Confirmar el tamaño del equipo** (D12/S-01). El cliente escribió "somos 3 personas" y listó 9. Se tomó la lista.
2. **Mantener la baseline aprobada.** Toda ampliación se trata como cambio de alcance y, si requiere persistencia, como una migración futura; no se reservan tablas o columnas ahora.
3. **Validar las cuatro tablas con un entrenador en ejercicio.** 33 de las 37 constantes del sistema son convenciones de este proyecto, no datos del dominio (D12/§1.1). Si están mal, el sistema funciona y prescribe mal, que es peor que fallar.
4. **Congelar D4 y D5.** Un error en DD-02, DD-03, DD-04 o DD-26 se paga con un rediseño imposible a mitad del plazo.
5. **Completar mapeos y revisar imágenes de RepDB** antes de publicar fichas; respetar licencia y atribución, y medir la capacidad del LLM con el catálogo completo.
6. **Verificar la carga de datos simulados y su marcado inequívoco** para demostrar diagnóstico y adaptación sin confundirlos con actividad real.
7. **Cerrar los puntos de producto abiertos** de D12/§5.
8. **Resolver la creación de migraciones** sin ejecutar `migrate dev` sobre Neon Test compartida (D12/I-07).
9. **Confirmar la operación en el Polo**: contrato LLM, dominio Cloudflare Tunnel estable, procesos permanentes y rollback (D12/I-08).
