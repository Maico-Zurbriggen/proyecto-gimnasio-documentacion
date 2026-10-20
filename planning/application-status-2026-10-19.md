# Estado de la aplicación al 19 de octubre de 2026

Documento descriptivo de auditoría de implementación. No sustituye requisitos, reglas ni decisiones. Se acompaña del [manual de uso](../operations/user-manual.md).

## 1. Resultado y alcance de la revisión

La aplicación tiene implementado un circuito sustancial de incorporación y prescripción: gimnasios, invitaciones, autenticación, contexto del alumno, condiciones físicas, catálogo, plantillas, rutinas manuales, generación con IA, aprobación por entrenador y regularización de mediciones. También hay renovación automática y revisión de propuestas de adaptación.

**Todavía no constituye una plataforma completa de seguimiento del entrenamiento.** Sesión, Progreso e Historial del alumno son placeholders. No hay recorrido implementado para registrar sesiones y series reales ni un motor completo de indicadores y diagnóstico por ejecución. La analítica administrativa presenta números fijos.

La revisión combina rutas y formularios del frontend, clientes HTTP, routers, casos de uso y persistencia del backend, contratos, procesamiento y pruebas del servicio IA. La presencia de tablas, tipos o una pantalla visual no se contabiliza como funcionalidad terminada. No se calcula un porcentaje de avance: contar archivos o endpoints no mide aceptación funcional.

### Versiones examinadas

| Repositorio | Rama local | Commit |
| --- | --- | --- |
| Frontend | `develop` | `9930455ef4b170f7425b567c95c1aa06c8532cf4` |
| Backend | `develop` | `1ea631a1adf88514c5da2bd186c3c495706db738` |
| IA | `develop` | `28d061cd046f033b0de6b95ac720d8c1fca701ca` |

Los tres árboles de código estaban limpios al comenzar. Se inspeccionó documentación local en `main`. No se consultaron ramas remotas ni despliegues: estas conclusiones corresponden a estos commits, no certifican el estado de producción.

## 2. Matriz de cobertura funcional

**Integrado en código:** hay pantalla, consumo del backend y persistencia prevista en el adaptador real. Esta categoría no significa prueba E2E ejecutada con PostgreSQL y servicios desplegados. **Condicionado:** requiere jobs, servicios o datos externos. **Parcial/API:** hay piezas funcionales, pero falta recorrido de usuario. **Presentación:** maqueta o placeholder.

| Capacidad | Estado observado | Alcance y límite |
| --- | --- | --- |
| Login, logout y sesión | Integrado en código | Cookie httpOnly, resolución de roles y guardas; backend comprueba permisos |
| Recuperación y cambio de contraseña | Integrado en código; correo condicionado | Token de recuperación, límites, invalidación de sesiones y formularios |
| Alta por invitación | Integrado en código; correo condicionado | Validación, consumo, consentimiento opcional al alta y sesión inicial |
| Invitar, listar, reenviar y revocar | Integrado en código | Entrenador invita alumnos; administrador elige roles; backend limita gestión |
| Gestión de gimnasios | Integrado en código | SuperAdmin crea, edita, suspende, reactiva y reemite invitación inicial |
| Contexto del alumno | Integrado en código | Objetivo, nivel, disponibilidad, nacimiento, sexo, altura, peso y consentimiento |
| Condiciones físicas | Integrado en código | Declaración expresa, alta, cierre e historial; lectura del entrenador asignado |
| Asignación entrenador–alumno | Integrado en código | Alta/cambio de asignación por administrador; evita autoasignación |
| Catálogo de ejercicios | Integrado en código | Búsqueda, filtros, paginación, detalle, imágenes y mapa muscular |
| Catálogo propio y curación | Integrado en código | Entrenador propone y edita fichas propias permitidas; administrador revisa y habilita |
| Habilitación de ejercicios | Integrado en código | Explícita y por gimnasio; aprobación de ficha y habilitación son distintas |
| Inventario | Integrado con divergencia | Coexisten `/admin/inventory` y `/catalog/inventory`; no tienen los mismos efectos |
| Plantillas | Integrado con límite de interfaz | Crear, editar y desactivar; reactivación en backend sin recorrido visible |
| Rutina desde plantilla | Integrado en código | Copia independiente como propuesta; aprobación separada |
| Rutina manual | Integrado en código | Editor de días, ejercicios habilitados y series; aprobación separada |
| Generación inicial con IA | Integrado; condicionado | Alumno propio y entrenador asignado; procesamiento externo, polling y finalización |
| Cambios en lenguaje natural a propuesta | Integrado con límite de recuperación | Alumno y entrenador; reemplazo validado; tracking del panel sólo en memoria |
| Consulta de rutina del alumno | Integrado en código | Vigente y pendiente, detalle y prompt; falta historial navegable de rechazadas/archivadas |
| Revisión de rutina propuesta | Integrado en código | Aprobar o rechazar con motivo; archiva anterior; controla disponibilidad y cambios de contexto |
| Cartera y ficha de alumno | Integrado en código | Recuentos reales, priorización, condiciones, estado y prescripción |
| Carga de medidas por renovación | Integrado en código | Altura y peso; no equivale a un módulo de evolución de mediciones |
| Controles de medición y bloqueo | Integrado; condicionado | Evaluación por job, tres ciclos omitidos, carga pendiente y aprobación del entrenador |
| Renovación automática | Implementada; condicionada | Job horario, controles, solicitudes IA, finalización y propuestas de estructura |
| Revisar adaptaciones | Integrado en código | Total/parcial/rechazo, evidencia, versiones y regeneración según propuesta |
| Diagnóstico completo por sesiones ejecutadas | Pendiente | Las vistas de revisión existentes no completan por sí mismas este circuito |
| Sesión, Progreso e Historial del alumno | Presentación | Rutas resueltas con `PlaceholderPage` |
| Perfil profesional del entrenador | Presentación | `PlaceholderPage` |
| Analítica administrativa | Presentación, salvo checklist | `182`, `74%` y `13` son constantes; checklist sí consulta preparación real |
| Edición de reglas de cálculo | Presentación | `/admin/reglas` usa `PlaceholderPage` |
| Gestión integral de cuentas existentes | Parcial/API | Invitaciones no equivalen a editar roles, membresía, aptitud o suspensión de usuarios |
| Avisos y auditoría | Parcial | Backend persiste efectos, pero no hay bandeja de avisos ni visor de auditoría en frontend |
| Analítica batch y modelos predictivos en IA | Pendiente | Dependencias opcionales y previsiones arquitectónicas no constituyen jobs implementados |
| Presets, nutrición y comentarios | Sin recorrido disponible | No documentados como operaciones utilizables en el manual |

## 3. Qué aporta cada repositorio

### Frontend

React, TanStack Query y rutas protegidas por sesión y rol. El router y la navegación distinguen cuatro áreas. Resumen y Mi rutina consumen rutinas reales; la cartera consume alumnos asignados. Las pantallas implementadas incluyen estados de carga, error y vacío con distintos grados de reintento.

El tracking de generación inicial conserva identificador y clave de idempotencia en localStorage. La propuesta generada se finaliza a través del backend y se presenta pendiente de revisión. El frontend no llama directamente al servicio Python ni a Ollama.

El cumplimiento de cliente generado es parcial: catálogo usa `openapi-fetch` y tipos generados; gestión de generación también tiene contrato generado. Persisten schemas y DTO manuales en archivos como `src/api/inventory.ts`, `auth.ts` y `prescriptions.ts`. Esto requiere seguimiento frente a la instrucción de consumir contratos generados.

### Backend

API Express modular con Prisma, autorización, casos de uso y persistencia PostgreSQL. Los módulos reales abarcan autenticación, invitaciones, gimnasios, asignaciones, inventario, catálogo, contexto, objetivos, condiciones físicas, mediciones, alumnos, prescripciones, rutinas, generación y evolución.

El flujo generativo crea y conserva solicitudes idempotentes, arma contexto, despacha al servicio IA y valida la finalización. La aprobación del entrenador sigue siendo una operación distinta. Las solicitudes nuevas usan contrato `2.0`; se conserva tratamiento para solicitudes anteriores `1.0`.

`vercel.json` declara controles de mediciones diarios y renovación de rutinas cada hora. El código de esos jobs existe y exige autenticación interna. No se verificó su habilitación, ejecución efectiva ni resultados en el despliegue.

### IA

FastAPI acepta despacho autenticado con UUID y devuelve `202`; Vercel Queues entrega el trabajo al consumidor. El servicio usa persistencia de integración para claim/lease, intentos, estados y resultados; llama a Ollama mediante su conector. En desarrollo hay un worker local que recupera pendientes desde persistencia.

Hay contratos, prompts, validación estructurada, cálculo de capacidad de contexto, compatibilidad de versiones, timeout y reintento. La configuración por defecto admite dos intentos de 120 segundos; esto no es una garantía de duración total, porque pueden intervenir cola, despacho y finalización. La falta de capacidad no se resuelve truncando catálogo ni fabricando una rutina de contingencia.

IA no aprueba ni pone rutinas en vigencia. No se encontraron procesos analíticos batch funcionales ni un motor predictivo operativo. Sus dependencias opcionales no justifican presentarlos como implementados.

## 4. Hallazgos que afectan el uso y la evaluación

### H1. El entrenamiento todavía no se registra

El router monta placeholders en Sesión, Progreso e Historial y no hay un módulo backend de ejecución de sesiones registrado en `src/app.ts`. El esquema de datos puede anticipar esas entidades, pero no hay un recorrido para generar actividad real desde la aplicación. El producto puede demostrar prescripción y revisión; no puede demostrar todavía el ciclo completo de entrenamiento y análisis.

### H2. La analítica muestra cifras de ejemplo

`AdminAnalyticsPage.tsx` declara que es una vista de referencia y contiene números fijos. Se debe evitar presentar esas cifras como socios, actividad o seguimiento reales. La checklist de preparación embebida sí está conectada al backend.

### H3. Dos recorridos de inventario producen efectos distintos

`InventoryPage.tsx` consume `/admin/inventory`: calcula catálogo prescribible por equipamiento y su repositorio marca/restaura compatibilidades. `CatalogPage.tsx` consume `/catalog/inventory`: utiliza revisión del inventario, devuelve ejercicios habilitados relacionados y delega la revisión explícita, sin habilitar automáticamente.

Ambos guardan equipamiento, pero el recorrido anterior conserva reglas y métricas distintas del modelo de habilitación explícita. El checklist anterior tampoco comprueba que haya ejercicios habilitados o IA accesible. Hace falta unificar el comportamiento y definir cuál será la entrada de operación; esta auditoría sólo lo registra.

### H4. Recuperación desigual de generaciones

La generación inicial persiste tracking en `generationTracking.ts`. `RoutineChangeRequestPanel.tsx` usa `requestId` e idempotencia en estado del componente. Recargar o desmontar ese panel pierde su seguimiento local aunque el trabajo del servidor continúe. No prometer la misma recuperación en ambos recorridos.

### H5. Motivo de rechazo persistido sin bandeja visible

Backend guarda revisión, aviso y auditoría; la pantalla del entrenador anuncia que el alumno recibe el motivo. Sin embargo, Mi rutina selecciona sólo `VIGENTE`, `PROPUESTA` o `BLOQUEADA`, e Historial es placeholder. No hay una bandeja de avisos implementada. Persistir el aviso no garantiza que el alumno pueda leerlo desde la interfaz.

### H6. Las pestañas de la ficha no son módulos separados

Las rutas de Resumen, Rutina y Mediciones del alumno del entrenador montan el mismo `StudentDetailPage`. El usuario puede operar la ficha, pero no dispone por eso de una serie histórica de mediciones ni de un detalle de progreso adicional.

### H7. La revisión de adaptación supera la generación de evidencia disponible

Existen consulta, resolución parcial o total, rechazo y regeneración de propuestas. La renovación automática tiene un productor concreto. No se encontró un circuito completo de diagnóstico y adaptación por sesiones ejecutadas. Evitar equiparar la capacidad de resolver propuestas con analítica de entrenamiento terminada.

### H8. Documentación histórica desactualizada

`corpus-guide.md` conserva la frase histórica «Nada del dominio está implementado». La referencia de secuencias lleva fecha de snapshot de septiembre y no cubre todos los recorridos actuales. El código permite generación al entrenador asignado, aunque documentos anteriores la restringen al alumno. También conserva ambos transportes en menciones de infraestructura.

El backend define ciclo de 60 días y antelación de siete; el comentario del código declara pendiente su incorporación al corpus. Estos datos se describen en el manual como comportamiento observado, sin convertirlos por esta auditoría en nuevas reglas normativas. Se registra el punto en [riesgos y supuestos](risks-and-assumptions.md).

### H9. Contratos y regeneración de clientes requieren seguimiento

Hay DTO/schemas HTTP escritos a mano en frontend. Además, `catalog:generate` apunta a `../Backend/openapi/catalog.openapi.json`, mientras que el repositorio hermano disponible se llama `proyecto-gimnasio-back`. No impide usar el archivo ya generado, pero el comando no corresponde al layout revisado y dificulta reproducir su actualización.

### H10. Hallazgo de dependencias del backend

`npm audit --json`, ejecutado durante esta revisión, reportó tres entradas de severidad alta en la cadena `prisma → @prisma/config → deepmerge-ts`, asociadas al aviso `GHSA-ggr8-5vv4-36mx`. Son tres entradas derivadas de una misma cadena, no tres incidentes independientes comprobados. Prisma figura como dependencia de desarrollo en el manifiesto del backend. Se requiere evaluar exposición y actualización compatible; no se aplicó `npm audit fix` ni se modificó el lockfile como parte de la auditoría.

## 5. Verificación ejecutada

Se ejecutaron los checks locales sin migrar ni sembrar bases, sin llamar al LLM real y sin enviar correos. Los resultados finales se detallan debajo. El paso inicial detectó dependencias locales incompletas: faltaba `openapi-fetch` en frontend, el cliente Prisma estaba desactualizado y faltaba `tokenizers` en la venv de IA. Se intentó preparar las dependencias declaradas para separar entorno de código.

| Componente | Verificación | Resultado |
| --- | --- | --- |
| Frontend | `npm run check` con `VITE_API_URL=http://localhost:3000` | Correcto: formato, lint, tipos, 219 pruebas en 48 archivos y build; advertencia de bundle mayor a 500 kB |
| Backend | `npm run check` | Correcto: formato, lint, tipos, 633 pruebas aprobadas y build; 65 pruebas omitidas en cuatro suites que requieren PostgreSQL aislado |
| IA | `python -m ruff check .` | Correcto |
| IA | `python -m mypy src` | Correcto: 14 archivos; fue necesario descartar la caché con `--no-incremental` tras instalar `tokenizers`, y luego pasó el comando habitual |
| IA | `python -m pytest -p no:cacheprovider` | 88 aprobadas, 2 omitidas por necesitar `AI_TEST_DATABASE_URL` aislada |
| Documentación | `python tools/check_docs.py` | Correcto: 49 documentos Markdown y 47 entradas de manifiesto |

Frontend tuvo además una ejecución con 218 pruebas aprobadas y una fallida: `ExerciseImage.test.tsx` espera URL local fija mientras la configuración existente apunta a un backend de test. Se repitió con `VITE_API_URL=http://localhost:3000` en el proceso, sin modificar `.env`. El primer intento de tests dentro del sandbox también encontró `spawn EPERM` al iniciar esbuild; se usó ejecución autorizada fuera de esa restricción.

No se ejecutaron pruebas de integración contra PostgreSQL, pruebas de entrega real de cola, envío real de correos, generación con Ollama ni evaluación de calidad por entrenador. Tampoco se validaron accesibilidad y diseño a 360 px en navegador. Esos límites impiden declarar el sistema listo para producción sólo por esta revisión.

## 6. Próximos cierres recomendados

1. Completar registro de sesión y series, su recuperación ante interrupciones y su API.
2. Conectar progreso, historial e indicadores a actividad real; reemplazar o retirar cifras ilustrativas.
3. Unificar inventario, habilitación explícita, revisiones y checklist de preparación.
4. Persistir recuperación del pedido de cambios y exponer al alumno los motivos de rechazo y avisos.
5. Completar generación de diagnóstico por sesiones y su integración con la revisión de propuestas.
6. Cerrar contratos generados y actualizar referencias documentales mediante cambios coordinados.
7. Ejecutar aceptación en un ambiente aislado: alta → contexto → propuesta → revisión → vigencia, renovación, bloqueo y recuperación; comprobar además aislamiento entre gimnasios y asignaciones.

Esta lista propone prioridades a partir de la cobertura observada; no altera la prioridad normativa de los requisitos.

## 7. Evidencia de implementación

Enlaces permanentes a los commits examinados; permiten volver a comprobar el informe aunque cambie `develop`.

| Evidencia | Fuentes |
| --- | --- |
| Rutas, roles y placeholders | [Router frontend](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/app/router/AppRouter.tsx), [navegación](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/app/layout/nav.ts) |
| Analítica ilustrativa | [Panel administrativo](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/administration/pages/AdminAnalyticsPage.tsx) |
| Rutinas y cambios | [Mi rutina](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/prescriptions/pages/StudentRoutinePage.tsx), [pedido de cambios](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/routine-generations/components/RoutineChangeRequestPanel.tsx), [tracking inicial](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/routine-generations/lib/generationTracking.ts) |
| Prescripción y aprobación | [Panel de prescripción](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/prescriptions/components/RoutinePrescriptionPanel.tsx), [persistencia de revisión](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/modules/prescriptions/infrastructure/persistence/prisma-prescriptions.repository.ts) |
| Ficha y regularización | [Ficha del alumno](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/students/pages/StudentDetailPage.tsx), [control de acceso por mediciones](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/students/components/MeasurementBlockGate.tsx) |
| Inventario y catálogo | [Cliente de inventario anterior](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/api/inventory.ts), [catálogo actual](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/exercise-catalog/CatalogPage.tsx), [persistencia de catálogo](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/modules/exercise-catalog/infrastructure/persistence/prisma-catalog.repository.ts) |
| Composición de backend | [App y routers registrados](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/app.ts), [permisos de generación](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/modules/routine-generations/infrastructure/http/routine-generations.routes.ts) |
| Renovación y adaptaciones | [Renovación de ciclos](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/modules/evolution/application/use-cases/renew-routine-cycles.use-case.ts), [cron](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/vercel.json), [revisión y regeneración](https://github.com/Maico-Zurbriggen/proyecto-gimnasio/blob/9930455ef4b170f7425b567c95c1aa06c8532cf4/src/features/adaptation-proposals/pages/ProposalReviewPage.tsx) |
| Plazos implementados | [Ciclo y aviso](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-back/blob/1ea631a1adf88514c5da2bd186c3c495706db738/src/modules/routines/domain/services/routine-renewal.ts) |
| Servicio IA | [API y cola](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-ia/blob/28d061cd046f033b0de6b95ac720d8c1fca701ca/src/gym_engine/api/app.py), [orquestación](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-ia/blob/28d061cd046f033b0de6b95ac720d8c1fca701ca/src/gym_engine/service.py), [conector v2](https://github.com/Maico-Zurbriggen/proyecto-gimnasio-ia/blob/28d061cd046f033b0de6b95ac720d8c1fca701ca/src/gym_engine/llm_v2.py) |
