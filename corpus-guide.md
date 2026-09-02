# Corpus documental — Plataforma de entrenamiento asistido

**Versión del corpus** 3.0 · **Fecha** 2026-09-01 · **Estado** alineado con el [baseline de alcance de la Etapa 1](planning/baseline-alcance-2026-09.md), el [modelo relacional](architecture/database-relational-model.md) y ADR 0009. Puntos abiertos en D12/§5, entre ellos **I-09**, que afecta al cálculo de capacidad

La v2.0 incorpora las 42 correcciones de la auditoría y las dos definiciones del cliente que las hicieron posibles: **el sistema no es abierto** (el gimnasio afilia e invita) y **el equipamiento es del gimnasio** (la prescripción depende de qué máquinas tiene).

La v2.1 incorpora el **candidato de rutina**: el solicitante moldea la rutina generada antes de enviarla a revisión, sin tocar la prescripción y sin mover la puerta del entrenador. Toca D3, D5, D6, D7, D8, D10, D11 y D12. Ver D11/DD-33.

La v2.2 centraliza el corpus en un repositorio documental único, organiza las rutas por responsabilidad y agrega `manifest.json` como mapa determinista para agentes. No modifica reglas funcionales.

La v2.3 incorpora una [propuesta de integración generativa](architecture/generative-ai-integration.md) con ambientes, trabajo local, promoción y pruebas. Declara tres diferencias que requieren ADR antes de cambiar la arquitectura o los requisitos vigentes.

La v2.4 aceptó [ADR 0009](decisions/adr/0009-servicio-generativo-online-en-el-polo.md): servicio Python y worker en el Polo, ingreso por ngrok, LLM separado, generación asíncrona y Neon Test compartida. También adoptó la promoción `develop → test → main`.

**La v3.0 incorpora el [baseline de alcance de la Etapa 1](planning/baseline-alcance-2026-09.md)**, que cruza la votación del equipo con el Acta de Redefinición y con el estado real de los tres repositorios de código. Tres cosas que conviene saber antes de leer el resto del corpus:

1. **Existe una dimensión de alcance separada de la prioridad.** Un requisito puede ser MUST y estar diferido: la prioridad dice cuánto importa al producto, el alcance dice si se construye ahora. D8 v4.0 marca las dos.
2. **Nada del dominio está implementado.** Los tres repositorios contienen andamiaje. Todo el corpus es diseño, no descripción de software existente.
3. **Se cerraron tres defectos estructurales del propio corpus:** DD-34 estaba citada por ocho documentos y nunca redactada · dos ADR compartían el número 0004 decidiendo cosas incompatibles · nueve documentos no estaban registrados en el manifiesto, con lo que la validación automática fallaba. Los tres están corregidos.

**Y quedan dos preguntas abiertas que condicionan la planificación**, no la documentación: cuánta capacidad de construcción hay realmente (I-09 en D12/§5) y si el Product Owner libera el compromiso sobre la interpretación de lenguaje natural (I-10).

La v2.7 incorpora el [modelo relacional PostgreSQL](architecture/database-relational-model.md), contratos JSON versionados sin datos identificatorios, candidatos con vencimiento por inactividad y estados técnicos de generación. Los presets dejan de ser contingencia obligatoria y pasan a alcance `COULD`; la primera entrega conserva plantillas privadas y creación manual por entrenadores.

---

## Cómo leerlo

| Doc                                       | Contenido                                                                                             | Léelo si                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [D1](product/vision-and-objectives.md)                 | Visión, capacidad central, alcance y 13 criterios de éxito                                            | Es el criterio que juzga todo lo demás. **Empezá acá**                         |
| [D2](product/glossary.md)                              | Glosario normativo + **12 enumeraciones cerradas**                                                    | Vas a escribir cualquier cosa. Un término o un valor que no esté acá no se usa |
| [D3](domain/actors-roles-permissions.md)                | Actores, matriz de permisos, 10 reglas de acceso                                                      | Trabajás en autorización                                                       |
| [D4](domain/domain-model.md)                            | Entidades, 8 puntos difíciles con alternativas y sacrificios, 23 restricciones                        | Vas a tocar la estructura de datos. **Congelar antes de escribir código**      |
| [D5](domain/business-rules.md)                          | 152 reglas verificables, **cada constante con su origen marcado**                                     | Implementás cualquier cálculo o validación                                     |
| [D6](domain/lifecycles-and-states.md)                   | 10 ciclos de vida, con las transiciones **imposibles** y su motivo                                    | Implementás una entidad con estado                                             |
| [D7](flows/functional-flows.md)                         | 21 flujos con cursos normales, alternativos y de excepción                                            | Implementás una funcionalidad completa                                         |
| [D8](requirements/functional-requirements.md)           | RF-001 a RF-120 con tipo, prioridad y dependencias                                                    | Planificás o estimás                                                           |
| [D9](requirements/non-functional-requirements.md)       | 40 requerimientos, todos con criterio de verificación                                                 | Definís la estrategia de pruebas                                               |
| [D10](domain/edge-cases.md)                             | 73 casos borde en 10 categorías                                                                       | Antes de dar por terminada cualquier funcionalidad                             |
| [D11](decisions/design-decisions.md)                    | 33 decisiones con opciones, fundamento y consecuencias                                                | Querés saber por qué algo es así, o pensás cambiarlo                           |
| [D12](planning/risks-and-assumptions.md)                | 10 supuestos, **37 constantes con su origen**, 16 riesgos, aritmética del esfuerzo y orden de recorte | Sos responsable del plan. **Leelo antes de comprometer fechas**                |
| [D13](requirements/traceability.md)                     | Qué requerimiento responde a qué necesidad, y qué quedó sin cubrir                                    | Preparás la defensa o discutís alcance con el cliente                          |

## Las cuatro tablas que sostienen la prescripción

Son determinísticas, auditables y discutibles con un entrenador real. En generación inicial validan la salida del LLM; en diagnóstico y adaptación determinan el comportamiento:

| Tabla                         | Dónde              | Qué determina                                                                                  |
| ----------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| Restricciones del tipo de rutina | D5/RN-39a       | Valida frecuencia, días, series, repeticiones, descansos y cobertura mínima del tipo propuesto |
| Compatibilidad                | D5/RN-44a a RN-44d | Cuándo un ejercicio está contraindicado, excede el nivel o falta el equipamiento               |
| Criterios de diagnóstico      | D5/RN-79a          | Cuál de las cinco situaciones tiene cada ejercicio y el conjunto                               |
| Reglas de ajuste              | D5/RN-89a          | Qué ajuste, de qué tipo y de qué magnitud, corresponde a cada situación                        |

## Convención de marcado

`[F]` lo afirma una fuente · `[I]` inferencia · `[S]` convención de este proyecto, sin fuente externa · 👁 decisión que las fuentes tomaron sin advertirlo · 🆕 nuevo · ⬆⬇ cambio de prioridad · ✎ enunciado modificado · ⛔ derogado

## Lo que hay que resolver antes de escribir código

1. **Confirmar el tamaño del equipo** (D12/S-01). El cliente escribió "somos 3 personas" y listó 9. Se tomó la lista.
2. **Conversación de alcance.** 82 requerimientos MUST contra ~504 h de capacidad de construcción (D12/§3) — entre 1,3 y 1,8 veces lo que entra. El orden de recorte está en D12/§4.
3. **Validar las cuatro tablas con un entrenador en ejercicio.** 33 de las 37 constantes del sistema son convenciones de este proyecto, no datos del dominio (D12/§1.1). Si están mal, el sistema funciona y prescribe mal, que es peor que fallar.
4. **Congelar D4 y D5.** Un error en DD-02, DD-03, DD-04 o DD-26 se paga con un rediseño imposible a mitad del plazo.
5. **Verificar la fuente del catálogo** (D12/S-09): tiene que traer, o permitir derivar, el equipamiento requerido y las articulaciones exigidas por cada ejercicio. Sin eso, la compatibilidad se cura a mano.
6. **Verificar que existe una fuente de datos con historial por usuario y por serie** (D12/S-03). De eso depende que el aprendizaje automático predictivo, que es núcleo, tenga sustento.
7. **Cerrar los puntos de producto abiertos** de D12/§5.
8. **Resolver la creación de migraciones** sin ejecutar `migrate dev` sobre Neon Test compartida (D12/I-07).
9. **Confirmar la operación en el Polo**: contrato LLM, dominio ngrok estable, procesos permanentes y rollback (D12/I-08).
