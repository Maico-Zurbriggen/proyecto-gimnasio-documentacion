# Integración de IA generativa, ambientes y pruebas

**Estado:** aceptada · **Fecha:** 2026-08-29 · **Decisión:** [ADR 0009](../decisions/adr/0009-servicio-generativo-online-en-el-polo.md)

## Alcance y autoridad

La primera entrega generativa usa un único LLM para interpretar lenguaje natural, proponer el tipo y contenido de una rutina, explicar el criterio y ofrecer alternativas. La predicción de cargas y progreso futuro pertenece al pipeline analítico posterior.

> **Alcance de la Etapa 1** ([baseline](../planning/baseline-alcance-2026-09.md)). Se construyen `interpretarPedido` (RF-053, banda N2, conservado por compromiso ante el Product Owner pese a obtener 3 votos de 8), `generarRutina` (RF-054, RF-087), `explicarCriterios` (RF-055) y `sugerirAlternativas` (RF-059, que absorbe la exclusión dura de RF-060). Quedan diferidos `resumirProgreso` (RF-056) y, en banda N3, `describirPerfil` (RF-064).
>
> **Y una consecuencia que cambia el peso de este componente:** al diferirse los presets (RF-021) y no existir un generador determinístico, `generarRutina` **es la única vía automática de prescripción del sistema**. Su indisponibilidad no degrada una funcionalidad accesoria: deja al producto sin forma de dar un plan a un alumno nuevo, salvo que un entrenador arme una plantilla a mano. Ver [D11/DD-35](../decisions/design-decisions.md) y D12/R-17.

El LLM siempre produce una salida candidata. El backend conserva autorización y reglas de negocio: minimiza el contexto, controla catálogo, compatibilidad, rangos y permisos, y convierte una salida válida en candidato. Un entrenador debe aprobar toda rutina antes de que llegue al alumno. El modelo no activa rutinas ni emite consejo médico.

## Topología

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

## Flujo de generación

1. El solicitante confirma parámetros estructurados.
2. Backend crea una solicitud idempotente con contexto anonimizado.
3. El servicio IA acepta la solicitud y el worker llama al LLM.
4. Cada intento tiene un límite configurable inicial de 120 segundos.
5. Una respuesta inválida o un fallo técnico admite un único reintento.
6. IA registra resultado, modelo, configuración, contrato e instante.
7. Backend valida la salida y, si es válida, presenta el candidato.
8. Al confirmarse, la rutina queda PROPUESTA y pasa al entrenador.

Tras el segundo fallo, la generación queda temporalmente no disponible. No hay generador determinístico alternativo ni adaptador `fake` ejecutable. El resto del sistema, las plantillas privadas y la creación manual por entrenadores permanecen operativos. Los presets sólo existirán si alcanza el tiempo para implementar RF-021.

## Datos y aislamiento

El contexto enviado excluye datos identificatorios que no aportan a la rutina. El Polo recibe un identificador técnico, objetivo, nivel, frecuencia, condiciones pertinentes, equipamiento, catálogo permitido y preferencias. Ningún log guarda prompts completos, credenciales ni datos de salud.

El servicio IA sólo puede leer y escribir las estructuras de integración acordadas. No accede a tablas de identidad ni modifica rutinas, sesiones o aprobaciones. Backend es el único que transforma un resultado en entidad de dominio.

Una única API y configuración del modelo atienden inicialmente ambos ambientes. La credencial de consumo determina en el servidor si se usa Neon Test o Neon Producción. Las conexiones, roles y secretos son distintos y nunca se eligen mediante datos enviados por el cliente.

## Trabajo local y ambientes

| Recurso | Local | Test (`test`) | Producción (`main`) |
| --- | --- | --- | --- |
| Frontend | Vite | Vercel Preview estable | Vercel Production |
| Backend | Express, conectado a Neon Test | Vercel + Neon Test | Vercel + Neon Producción |
| IA online | Python local opcional o servicio compartido del Polo | API y worker en el Polo | misma API/worker, credencial aislada |
| LLM | API del Polo cuando sea accesible | LLM del Polo | mismo LLM/configuración inicial |
| Analítica futura | jobs manuales sobre datos sintéticos/test | jobs batch | jobs batch |

El desarrollo ordinario no levanta PostgreSQL local: frontend y backend locales usan Neon Test. No se permiten resets, seeds destructivos ni migraciones automáticas sobre la base compartida. La creación segura de migraciones requiere resolver la estrategia declarada en [Base de datos de desarrollo](../operations/local-database.md).

Los tests unitarios y de contrato sustituyen el transporte HTTP o el conector LLM dentro del proceso de prueba; eso no constituye un modo fake de la aplicación. Las integraciones reales se ejecutan al promover a `test` y cuando cambia modelo, prompt o parámetros.

## Promoción

```text
feature/* -> PR -> develop -> PR -> test -> PR -> main
```

- Todo PR ejecuta formato, tipos, unitarias y contratos, con aprobación de otra persona.
- `test` despliega Neon Test, Vercel y la versión test del servicio IA; allí se ejecutan integración, evaluación y E2E.
- `main` exige aprobación del dueño, checks verdes y smoke test posterior.
- Un cambio de modelo, prompt o parámetros necesita además una evaluación comparativa y validación de al menos un entrenador.
- Los cambios incompatibles backend–IA se despliegan por etapas y conservan compatibilidad temporal.

## Estrategia de pruebas

| Nivel | Qué verifica | Cuándo |
| --- | --- | --- |
| Unidad | reglas, permisos, minimización, parser y máquina de estados | cada PR |
| Contrato | OpenAPI backend–IA, idempotencia y compatibilidad | cada PR |
| Persistencia | permisos del rol IA, reclamo durable y aislamiento de ambientes | cada PR/promoción |
| Integración | ngrok, timeout, reintento, caída del LLM y recuperación del worker | en `test` |
| Evaluación | catálogo, compatibilidad, rangos, números respaldados y lenguaje médico | cambios de IA |
| E2E | solicitud, polling, candidato, revisión, aprobación e indisponibilidad generativa | antes de `main` |

El dataset fijo cubre contexto incompleto, condiciones físicas, equipamiento ausente, prompt injection, respuestas mal formadas, timeout y caída del servicio. No se compara texto exacto: se verifican invariantes y una rúbrica humana. Las métricas incluyen latencia, reintentos, salida inválida, indisponibilidad, rechazo del entrenador y magnitud de edición.

## Operación mínima

API Python, worker, LLM y agente ngrok deben arrancar con la máquina, reiniciarse ante fallos y exponer salud observable. El dominio ngrok debe ser estable. Si API, worker, túnel o LLM fallan, la generación se declara no disponible sin degradar el resto del sistema.
