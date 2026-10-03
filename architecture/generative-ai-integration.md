# Integración de IA generativa, ambientes y pruebas

**Estado:** aceptada · **Actualizada:** 2026-09-29 · **Decisiones:** [ADR 0010](../decisions/adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) y [ADR 0012](../decisions/adr/0012-api-polo-ngrok.md)

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
2. Backend verifica identidad, minimiza el contexto y prefiltra el catálogo compatible.
3. Backend persiste idempotentemente la solicitud con contexto minimizado y catálogo prefiltrado, y registra el ownership solicitud–alumno–solicitante.
4. Backend envía sólo el UUID técnico a la API IA. La API comprueba que la solicitud exista y siga procesable, publica ese UUID en Vercel Queues y responde `202`.
5. Frontend consulta el estado exclusivamente a backend.
6. Cada intento tiene un límite configurable inicial de 120 segundos; una salida inválida o fallo técnico admite un único reintento.
7. IA registra resultado, modelo, configuración, contrato e instante.
8. Al quedar `COMPLETADA`, frontend solicita la finalización técnica; backend revalida y crea idempotentemente una rutina `PROPUESTA`.
9. El entrenador asignado revisa esa propuesta y es el único que puede aprobarla para ponerla en vigencia.

Tras el segundo fallo, la generación queda temporalmente no disponible. No hay generador determinístico alternativo ni adaptador `fake` ejecutable. El resto del sistema, las plantillas privadas y la creación manual por entrenadores permanecen operativos. Los presets sólo existirán si alcanza el tiempo para implementar RF-021.

## Datos y aislamiento

El contexto enviado excluye datos identificatorios que no aportan a la rutina. El Polo recibe un identificador técnico, objetivo, nivel, frecuencia, condiciones pertinentes, equipamiento, catálogo permitido y preferencias. Ningún log guarda prompts completos, credenciales ni datos de salud.

La llamada a `/api/chat` usa el formato JSON nativo y desactiva la salida de razonamiento del modelo (`think: false`). La configuración `generative/generar-rutina@4` recibe streaming JSONL, exige el fragmento final `done: true` y aplica un límite total de 120 segundos por intento. Pide un plan privado compacto: el modelo elige grupos de series con cantidad, repeticiones, descanso y calentamiento. Pydantic valida el plan; IA comprueba las restricciones entregadas por backend y el adaptador expande esas cantidades al contrato público de rutina existente, con carga sin especificar. Una salida inválida usa el único reintento. El prompt incluye los rangos y la cobertura calculados por backend desde sus reglas de validación. El Polo rechazó el JSON Schema estricto en `format` al no poder compilar su gramática.

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

El ambiente local independiente conserva la inferencia real por la API autenticada del Polo. PostgreSQL y el procesamiento de solicitudes corren localmente, sin Neon. El conector limita el contexto a 8192 tokens y la disponibilidad verifica que el modelo configurado figure entre los instalados. Las conexiones a PostgreSQL vencen a los cinco segundos y el worker retoma su consulta periódica tras un fallo temporal.

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
| Evaluación | catálogo, compatibilidad, rangos, números respaldados y lenguaje médico | cambios de IA |
| E2E | solicitud, polling, candidato, revisión, aprobación e indisponibilidad generativa | antes de `main` |

El dataset fijo cubre contexto incompleto, condiciones físicas, equipamiento ausente, prompt injection, respuestas mal formadas, timeout y caída del servicio. No se compara texto exacto: se verifican invariantes y una rúbrica humana. Las métricas incluyen latencia, reintentos, salida inválida, indisponibilidad, rechazo del entrenador y magnitud de edición.

## Operación mínima

Vercel opera API Python, cola y consumidor. Ollama, el router y el agente ngrok deben arrancar con la m?quina del Polo y reiniciarse ante fallos. El servicio IA usa el prefijo `/polo` y el token propio del proxy. Si API, cola, consumidor, router o LLM fallan, la generaci?n se declara no disponible sin degradar el resto del sistema.
