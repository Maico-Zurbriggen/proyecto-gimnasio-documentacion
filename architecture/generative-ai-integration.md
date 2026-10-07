# Integración de IA generativa, ambientes y pruebas

**Actualización 2026-10-07:** contrato `2.0` implementado localmente de [ADR 0013](../decisions/adr/0013-catalogo-repdb-y-seleccion-ia.md) pendiente de promoción y evaluación profesional. Transporte, cola y ambientes se conservan; cambia catálogo y autoridad de selección/prescripción.

**Estado:** aceptada · **Actualizada:** 2026-09-29 · **Decisiones:** [ADR 0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) y [ADR 0012](../decisions/adr/0012-api-polo-ngrok.md)

## Alcance y autoridad

La primera entrega generativa usa un único LLM para interpretar lenguaje natural, proponer el tipo y contenido de una rutina, explicar el criterio y ofrecer alternativas. La predicción de cargas y progreso futuro pertenece al pipeline analítico posterior.

> **Alcance de la Etapa 1** ([baseline](../planning/baseline-alcance-2026-09.md)). Se construyen `interpretarPedido` (RF-053, banda N2, conservado por compromiso ante el Product Owner pese a obtener 3 votos de 8), `generarRutina` (RF-054, RF-087), `explicarCriterios` (RF-055) y `sugerirAlternativas` (RF-059, que absorbe la evaluación de adecuación de RF-060). Quedan diferidos `resumirProgreso` (RF-056) y, en banda N3, `describirPerfil` (RF-064).
>
> **Y una consecuencia que cambia el peso de este componente:** al diferirse los presets (RF-021) y no existir un generador determinístico, `generarRutina` **es la única vía automática de prescripción del sistema**. Su indisponibilidad no degrada una funcionalidad accesoria: deja al producto sin forma de dar un plan a un alumno nuevo, salvo que un entrenador arme una plantilla a mano. Ver [D11/DD-35](../decisions/design-decisions.md) y D12/R-17.

El LLM selecciona, evalúa y prescribe con todo el catálogo habilitado. Backend conserva autorización, minimización, estructura, referencias y disponibilidad, y crea una PROPUESTA. El entrenador evalúa su adecuación y aprueba; el modelo no activa rutinas ni escribe entidades de dominio.

## Topología

```text
React/Vercel -> Express/Vercel -> FastAPI/Vercel -> Vercel Queues
                       |              |                 |
                       +----------- Neon <---- worker --+
                                                        |
                                                        v
                                  ngrok -> Polo API -> Ollama
```

- Backend nunca llama al túnel; llama al deployment Vercel de IA de su ambiente.
- La API Python acepta trabajos con `202`; Vercel Queues invoca un consumidor privado fuera de la petición.
- La API autenticada del Polo expone Ollama por el prefijo `/polo`. IA envía `POLO_API_TOKEN` como Bearer y `ngrok-skip-browser-warning: 1` para evitar la pantalla intermedia de ngrok.
- El servicio Python persiste estados y resultados en estructuras de integración. El LLM no conoce PostgreSQL.
- El frontend consulta estado exclusivamente al backend.
- Backend e IA se despliegan de manera independiente mediante contratos versionados.

## Flujo de generación

1. El alumno autenticado solicita para sí una rutina y confirma texto libre o parámetros estructurados.
2. Backend verifica identidad y toma todo el catálogo aprobado y habilitado del gimnasio, sin filtros de entrenamiento.
3. Backend persiste idempotentemente contexto mínimo, catálogo completo y versiones, y registra el ownership solicitud–alumno–solicitante.
4. Backend envía sólo el UUID técnico a la API IA. La API comprueba que la solicitud exista y siga procesable, publica ese UUID en Vercel Queues y responde `202`.
5. Frontend consulta el estado exclusivamente a backend.
6. Cada intento tiene un límite configurable inicial de 120 segundos; una salida inválida o fallo técnico admite un único reintento.
7. IA registra resultado, modelo, configuración, contrato e instante.
8. Al quedar `COMPLETADA`, backend finaliza idempotentemente si formato, referencias, disponibilidad y contexto siguen válidos; crea PROPUESTA. Un contexto cambiado exige una solicitud nueva.
9. El entrenador asignado revisa esa propuesta y es el único que puede aprobarla para ponerla en vigencia.

Tras el segundo fallo, la generación queda temporalmente no disponible. No hay generador determinístico alternativo ni adaptador `fake` ejecutable. El resto del sistema, las plantillas privadas y la creación manual por entrenadores permanecen operativos. Los presets sólo existirán si alcanza el tiempo para implementar RF-021.

## Datos y aislamiento

El contexto enviado excluye datos identificatorios que no aportan a la rutina. El Polo recibe un identificador técnico, objetivo, nivel, frecuencia, condiciones pertinentes, equipamiento, catálogo permitido y preferencias. Ningún log guarda prompts completos, credenciales ni datos de salud.

La inferencia conserva streaming JSON y final explícito. El contrato nuevo retira rangos y cobertura calculados por backend; los alias y grupos de series sólo compactan y expanden la decisión del modelo. La implementación de prompts previa no acredita esta migración: debe versionarse y evaluarse con backend e IA (data-interface.md).

El servicio IA sólo puede leer y escribir las estructuras de integración acordadas. No accede a tablas de identidad ni modifica rutinas, sesiones o aprobaciones. Backend es el único que transforma un resultado en entidad de dominio.

Un único proyecto Vercel genera dos deployments estables. Preview de `test` usa Neon Test y Production de `main` usa Neon Producción. Sus URLs de servicio IA, conexiones, roles y claves backend–IA son distintos y nunca se eligen mediante datos enviados por el cliente. Ambos deployments comparten inicialmente `LLM_API_URL` y `LLM_API_TOKEN` porque consumen el mismo LLM del Polo.

## Trabajo local y ambientes

| Recurso | Local | Test (`test`) | Producción (`main`) |
| --- | --- | --- | --- |
| Frontend | Vite | Vercel Preview estable | Vercel Production |
| Backend | Express + PostgreSQL local | Vercel + Neon Test | Vercel + Neon Producción |
| IA online | FastAPI + worker local + rol PostgreSQL restringido | Vercel Preview + Queues + Neon Test | Vercel Production + Queues + Neon Producción |
| LLM | API autenticada del Polo | LLM del Polo | mismo LLM/configuración inicial |
| Analítica futura | jobs manuales sobre datos sintéticos/test | jobs batch | jobs batch |

El desarrollo independiente levanta PostgreSQL local persistente. IA consulta solicitudes pendientes y leases vencidos periódicamente y conserva la concurrencia uno y el máximo de dos intentos. No se permiten resets, seeds destructivos ni migraciones automáticas sobre la base compartida. La configuración y creación segura de migraciones se describen en [Base de datos de desarrollo](../operations/local-database.md).

Los tests unitarios y de contrato sustituyen el transporte HTTP o el conector LLM dentro del proceso de prueba; eso no constituye un modo fake de la aplicación. Las integraciones reales se ejecutan al promover a `test` y cuando cambia modelo, prompt o parámetros.

El ambiente local conserva inferencia real por la API del Polo, PostgreSQL y worker locales. El límite actual de 8192 tokens requiere revisión para el catálogo habilitado completo; no autoriza truncarlo. Conexiones PostgreSQL vencen a los cinco segundos y el worker retoma tras fallos temporales.

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
| Integración | Vercel Queues, API Polo/ngrok, token, timeout, reintento, redelivery y caída del LLM | en `test` |
| Evaluación | Calidad de prescripción revisada por entrenador; schema, referencias, contexto completo, concurrencia y capacidad por checks técnicos | cambios de IA |
| E2E | habilitación, solicitud, polling, propuesta, revisión, aprobación e indisponibilidad | antes de `main` |

El dataset fijo cubre contexto incompleto, condiciones físicas, equipamiento ausente, prompt injection, respuestas mal formadas, timeout y caída del servicio. No se compara texto exacto: se verifican invariantes y una rúbrica humana. Las métricas incluyen latencia, reintentos, salida inválida, indisponibilidad, rechazo del entrenador y magnitud de edición.

## Operación mínima

Vercel opera API Python, cola y consumidor. Ollama, el router y el agente ngrok deben arrancar con la máquina del Polo y reiniciarse ante fallos. El servicio IA usa el prefijo `/polo` y el token propio del proxy. Si API, cola, consumidor, router o LLM fallan, la generación se declara no disponible sin degradar el resto del sistema.
