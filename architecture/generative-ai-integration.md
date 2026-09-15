# Integración de IA generativa, ambientes y pruebas

**Estado:** aceptada · **Actualizada:** 2026-09-15 · **Decisión:** [ADR 0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md)

## Alcance y autoridad

La primera entrega generativa usa un único LLM para interpretar lenguaje natural, proponer el tipo y contenido de una rutina, explicar el criterio y ofrecer alternativas. La predicción de cargas y progreso futuro pertenece al pipeline analítico posterior.

> **Alcance de la Etapa 1** ([baseline](../planning/baseline-alcance-2026-09.md)). Se construyen `interpretarPedido` (RF-053, banda N2, conservado por compromiso ante el Product Owner pese a obtener 3 votos de 8), `generarRutina` (RF-054, RF-087), `explicarCriterios` (RF-055) y `sugerirAlternativas` (RF-059, que absorbe la exclusión dura de RF-060). Quedan diferidos `resumirProgreso` (RF-056) y, en banda N3, `describirPerfil` (RF-064).
>
> **Y una consecuencia que cambia el peso de este componente:** al diferirse los presets (RF-021) y no existir un generador determinístico, `generarRutina` **es la única vía automática de prescripción del sistema**. Su indisponibilidad no degrada una funcionalidad accesoria: deja al producto sin forma de dar un plan a un alumno nuevo, salvo que un entrenador arme una plantilla a mano. Ver [D11/DD-35](../decisions/design-decisions.md) y D12/R-17.

El LLM produce una salida estructurada que nunca es vigente por sí misma. El backend conserva autorización y reglas de negocio: minimiza el contexto, controla catálogo, compatibilidad, rangos y permisos, y convierte una salida válida directamente en rutina `PROPUESTA`. Un entrenador debe aprobarla antes de que llegue al alumno. El modelo no activa rutinas ni emite consejo médico.

## Topología

```text
React/Vercel -> Express/Vercel -> FastAPI/Vercel -> Vercel Queues
                       |              |                 |
                       +----------- Neon <---- worker --+
                                                        |
                                                        v
                                              ngrok -> Ollama/Polo
```

- Backend nunca llama a ngrok; llama al deployment Vercel de IA de su ambiente.
- La API Python acepta trabajos con `202`; Vercel Queues invoca un consumidor privado fuera de la petición.
- Ngrok expone sólo la inferencia necesaria del LLM y exige autenticación de servicio.
- El servicio Python persiste estados y resultados en estructuras de integración. El LLM no conoce PostgreSQL.
- El frontend consulta estado exclusivamente al backend.
- Backend e IA se despliegan de manera independiente mediante contratos versionados.

## Flujo de generación

1. El solicitante confirma parámetros estructurados.
2. Backend crea una solicitud idempotente con contexto anonimizado y envía sólo su UUID a IA.
3. El servicio IA valida el UUID, lo encola y responde `202`; el consumidor llama al LLM.
4. Cada intento tiene un límite configurable inicial de 120 segundos.
5. Una respuesta inválida o un fallo técnico admite un único reintento.
6. IA registra resultado, modelo, configuración, contrato e instante.
7. Backend valida la salida y, si es válida, presenta el candidato.
8. Al confirmarse, la rutina queda PROPUESTA y pasa al entrenador.

Tras el segundo fallo, la generación queda temporalmente no disponible. No hay generador determinístico alternativo ni adaptador `fake` ejecutable. El resto del sistema, las plantillas privadas y la creación manual por entrenadores permanecen operativos. Los presets sólo existirán si alcanza el tiempo para implementar RF-021.

## Datos y aislamiento

El contexto enviado excluye datos identificatorios que no aportan a la rutina. El Polo recibe un identificador técnico, objetivo, nivel, frecuencia, condiciones pertinentes, equipamiento, catálogo permitido y preferencias. Ningún log guarda prompts completos, credenciales ni datos de salud.

El servicio IA sólo puede leer y escribir las estructuras de integración acordadas. No accede a tablas de identidad ni modifica rutinas, sesiones o aprobaciones. Backend es el único que transforma un resultado en entidad de dominio.

Un único proyecto Vercel genera dos deployments estables. Preview de `test` usa Neon Test y Production de `main` usa Neon Producción. Sus URLs, conexiones, roles y secretos son distintos y nunca se eligen mediante datos enviados por el cliente.

## Trabajo local y ambientes

| Recurso | Local | Test (`test`) | Producción (`main`) |
| --- | --- | --- | --- |
| Frontend | Vite | Vercel Preview estable | Vercel Production |
| Backend | Express, conectado a Neon Test | Vercel + Neon Test | Vercel + Neon Producción |
| IA online | FastAPI local con Test; cola real mediante Vercel CLI | Vercel Preview + Queues + Neon Test | Vercel Production + Queues + Neon Producción |
| LLM | API del Polo cuando sea accesible | LLM del Polo | mismo LLM/configuración inicial |
| Analítica futura | jobs manuales sobre datos sintéticos/test | jobs batch | jobs batch |

El desarrollo ordinario no levanta PostgreSQL local: frontend y backend locales usan Neon Test. No se permiten resets, seeds destructivos ni migraciones automáticas sobre la base compartida. La creación segura de migraciones requiere resolver la estrategia declarada en [Base de datos de desarrollo](../operations/local-database.md).

Los tests unitarios y de contrato sustituyen el transporte HTTP o el conector LLM dentro del proceso de prueba; eso no constituye un modo fake de la aplicación. Las integraciones reales se ejecutan al promover a `test` y cuando cambia modelo, prompt o parámetros.

## Promoción

```text
feature/* -> PR -> develop -> PR -> test -> PR -> main
```

- Todo PR ejecuta formato, tipos, unitarias y contratos, con aprobación de otra persona.
- `test` despliega Preview de frontend, backend e IA contra Neon Test; allí se ejecutan integración, evaluación y E2E.
- `main` exige aprobación del dueño, checks verdes y smoke test posterior.
- Un cambio de modelo, prompt o parámetros necesita además una evaluación comparativa y validación de al menos un entrenador.
- Los cambios incompatibles backend–IA se despliegan por etapas y conservan compatibilidad temporal.

## Estrategia de pruebas

| Nivel | Qué verifica | Cuándo |
| --- | --- | --- |
| Unidad | reglas, permisos, minimización, parser y máquina de estados | cada PR |
| Contrato | OpenAPI backend–IA, idempotencia y compatibilidad | cada PR |
| Persistencia | permisos del rol IA, reclamo durable y aislamiento de ambientes | cada PR/promoción |
| Integración | Vercel Queues, ngrok, timeout, reintento, redelivery y caída del LLM | en `test` |
| Evaluación | catálogo, compatibilidad, rangos, números respaldados y lenguaje médico | cambios de IA |
| E2E | solicitud, polling, candidato, revisión, aprobación e indisponibilidad generativa | antes de `main` |

El dataset fijo cubre contexto incompleto, condiciones físicas, equipamiento ausente, prompt injection, respuestas mal formadas, timeout y caída del servicio. No se compara texto exacto: se verifican invariantes y una rúbrica humana. Las métricas incluyen latencia, reintentos, salida inválida, indisponibilidad, rechazo del entrenador y magnitud de edición.

## Operación mínima

Vercel opera API Python, cola y consumidor. Ollama y el agente ngrok deben arrancar con la máquina del Polo y reiniciarse ante fallos. El dominio ngrok debe ser estable y autenticado. Si API, cola, consumidor, túnel o LLM fallan, la generación se declara no disponible sin degradar el resto del sistema.
