# Manual de uso de la aplicación

Fecha de revisión: **19 de octubre de 2026**. Versión inicial basada en las ramas locales `develop` de frontend, backend e IA. Documento descriptivo, no normativo.

Este manual explica las funciones que tienen pantalla y soporte en el código revisado. Su disponibilidad en un ambiente concreto depende de la versión desplegada, los datos y los servicios configurados. No se realizó una prueba con usuarios reales en producción. El [informe de estado](../planning/application-status-2026-10-19.md) identifica los commits, las verificaciones y las limitaciones.

Las reglas oficiales siguen en [roles y permisos](../domain/actors-roles-permissions.md), [flujos funcionales](../flows/functional-flows.md) y [estados](../domain/lifecycles-and-states.md). Aquí se describe cómo operar la implementación observada; no se amplía el alcance del producto.

## 1. Qué se puede hacer hoy

La aplicación permite incorporar gimnasios y personas por invitación, completar el contexto del alumno, declarar condiciones físicas, consultar ejercicios, solicitar rutinas con IA, crear rutinas manuales o desde plantillas y someterlas a revisión del entrenador. También permite controlar la actualización de mediciones y revisar propuestas de renovación o adaptación existentes.

**Todavía no permite registrar entrenamientos desde la pantalla Sesión ni consultar un progreso o historial real en las pantallas que llevan esos nombres.** La analítica administrativa contiene cifras ilustrativas. No usar esas pantallas como evidencia de actividad o resultados de alumnos.

| Usuario | Área de entrada | Funciones disponibles |
| --- | --- | --- |
| Alumno | Resumen | Contexto, condiciones físicas, medidas solicitadas, catálogo, generación, consulta de rutina y pedido de cambios sobre una propuesta |
| Entrenador | Cartera | Alumnos asignados, invitaciones a alumnos, plantillas, rutinas manuales, generación, revisión de rutinas, resolución de adaptaciones y desbloqueo por mediciones |
| Administrador | Analítica | Invitaciones, asignaciones, inventario, habilitación y revisión de ejercicios, parámetros de generación; el panel de indicadores es ilustrativo |
| SuperAdmin | Gimnasios | Alta, edición, suspensión y reactivación de gimnasios e invitación del primer administrador |

## 2. Acceso y cuenta: todos los usuarios

### 2.1 Crear la cuenta desde una invitación

1. Abrir el enlace recibido por correo. La aplicación no ofrece registro libre.
2. Verificar el gimnasio y el correo que presenta la invitación.
3. Completar el nombre y elegir una contraseña; repetirla en el campo de confirmación.
4. Cumplir los requisitos que aparecen en pantalla: al menos ocho caracteres, una mayúscula, una minúscula y un número. El máximo admitido es de 64 caracteres.
5. Leer el consentimiento para datos de salud cuando se presente. La cuenta puede crearse sin otorgarlo, pero será necesario para guardar datos de salud.
6. Confirmar el alta. Se inicia la sesión; las cuentas con rol Alumno pasan a la puesta en contexto.

Si la invitación venció, fue revocada o ya se usó, solicitar ayuda a quien la emitió. Si se reenvió, abrir el correo más reciente: el enlace anterior deja de servir.

### 2.2 Iniciar sesión y navegar

1. Abrir `/ingresar` en la dirección del ambiente que indique el gimnasio.
2. Ingresar correo y contraseña.
3. Usar el menú de la propia área. En móvil se abre con el control de navegación.
4. Si la cuenta tiene varios roles, usar los accesos de cambio de área. Sólo aparecen los roles que realmente tiene la cuenta.

Una cuenta sin roles asignados verá una pantalla de falta de acceso. Una suspensión de cuenta o de gimnasio puede impedir ingresar. Pedir al responsable que revise el estado; cambiar de pantalla no otorga permisos.

### 2.3 Recuperar o cambiar contraseña

**Sin sesión:** entrar en recuperación desde el acceso, indicar el correo y enviar la solicitud. La respuesta es la misma exista o no una cuenta. Si corresponde, se recibe un enlace de un solo uso, con duración de dos horas. La pantalla informa un máximo de dos pedidos diarios. Abrir el último enlace, ingresar y confirmar la nueva contraseña, y volver a iniciar sesión. El restablecimiento cierra las sesiones anteriores.

**Con sesión:** abrir **Cambiar contraseña** en el menú de cuenta, ingresar la contraseña nueva, repetirla y guardar. La sesión actual continúa y las demás se cierran.

**Para salir:** usar **Cerrar sesión**. Cerrar la pestaña por sí solo no equivale a cerrar sesión.

## 3. Manual del alumno

### 3.1 Completar o actualizar el contexto

Abrir `/alumno/puesta-en-contexto`. Al completar una cuenta de alumno se llega a esta pantalla automáticamente.

1. Elegir objetivo: fuerza, hipertrofia, resistencia muscular o acondicionamiento general.
2. Elegir nivel de experiencia: principiante, intermedio o avanzado.
3. Informar los días disponibles por semana, fecha de nacimiento, sexo, altura en centímetros y peso en kilogramos.
4. Otorgar el consentimiento para tratar datos de salud si todavía falta.
5. Pulsar **Guardar y continuar**.

La pantalla muestra el entrenador asignado o avisa que todavía falta uno. **Completar más tarde** permite salir, pero la generación puede permanecer impedida por contexto incompleto. La página puede volver a abrirse mediante su dirección para actualizar estos datos; **Mi perfil** actualmente se concentra en condiciones físicas y no contiene el formulario completo de contexto.

### 3.2 Declarar condiciones físicas

Entrar en **Mi perfil** (`/alumno/perfil`).

1. Si falta consentimiento, leerlo y otorgarlo desde la pantalla.
2. Declarar expresamente que no hay condiciones, o completar una condición.
3. Para una condición, elegir zona corporal y severidad; agregar fecha de inicio y descripción cuando corresponda.
4. Revisar y confirmar la declaración. Atender las confirmaciones adicionales que aparezcan.
5. Consultar las condiciones vigentes y el historial mostrado en la misma sección.
6. Cuando una condición deje de estar vigente, usar la acción de cierre y confirmarla.

El entrenador asignado puede consultar estas declaraciones. El alumno no modifica las condiciones de otras personas. Declarar que no hay condiciones es distinto de dejar la sección sin completar.

### 3.3 Solicitar una rutina con IA

Entrar en **Resumen** (`/alumno`) o **Mi rutina** (`/alumno/rutina`).

1. Completar el contexto y la declaración de condiciones físicas.
2. En **Generar rutina**, escribir las indicaciones solicitadas. Ejemplo: «Quiero priorizar fuerza y organizar mis días disponibles con sesiones de hasta 60 minutos».
3. Enviar una vez y esperar el estado del proceso. La respuesta no es inmediata.
4. Cuando finalice y se valide, abrir **Ver rutina**.
5. Revisar la propuesta y esperar la decisión del entrenador.

La solicitud inicial conserva su seguimiento en este navegador para recuperarse tras recargar o pasar entre Resumen y Mi rutina. Si la pantalla indica una salida terminada que todavía no pudo convertirse en rutina, usar el reintento de finalización que ofrezca. **Que la IA haya terminado no significa que la rutina esté aprobada.**

Si ya hay una propuesta pendiente, abrirla con **Ver rutina pendiente de revisión**. No crear una segunda solicitud inicial para resolver la misma propuesta.

El catálogo debe tener ejercicios aprobados y habilitados por el administrador. Si no hay suficientes datos, la IA explica que no puede cumplir el pedido, o el servicio está indisponible, corregir lo indicado y reintentar cuando corresponda. El entrenador puede continuar con plantillas o creación manual.

### 3.4 Consultar la rutina

En **Mi rutina** se presentan por separado la rutina vigente y la pendiente, cuando existan.

Revisar tipo, frecuencia semanal, versión, origen, días, ejercicios y series. El detalle presenta repeticiones, descanso y carga sugerida cuando está informada, además de notas o advertencias disponibles. Una carga sin informar no debe interpretarse como cero. Las rutinas generadas pueden mostrar el **Prompt solicitado**.

La pendiente puede indicar:

| Texto o estado | Qué hacer |
| --- | --- |
| Pendiente de revisión / `PROPUESTA` | Esperar al entrenador; se puede pedir un cambio sobre la propuesta |
| Esperando asignación de entrenador / `BLOQUEADA` | Pedir al gimnasio que complete la asignación |
| Rutina vigente / `VIGENTE` | Consultar la prescripción aprobada |

El resumen ofrece una vista previa; usar **Ver rutina completa** para abrir el detalle. Las rutinas rechazadas o archivadas no tienen un recorrido completo de consulta en el Historial actual.

### 3.5 Pedir cambios antes de la aprobación

1. Abrir la rutina en estado `PROPUESTA` en **Mi rutina**.
2. Buscar **Pedir cambios** y describir lo que debería ser diferente. Ejemplo: «Sacá el press militar y redistribuí los ejercicios de hombro».
3. Enviar y esperar la generación de reemplazo.
4. Revisar la nueva propuesta. Sigue requiriendo aprobación del entrenador.

La propuesta anterior se reemplaza cuando la nueva termina y supera la validación. Si falla, el pedido no pone una rutina en vigencia. Este panel de cambios no conserva localmente el identificador como sí lo hace la solicitud inicial: conviene permanecer en la pantalla hasta que concluya; si se interrumpe, volver a consultar las rutinas antes de repetir el pedido.

### 3.6 Actualizar mediciones y regularizar un bloqueo

En **Resumen**, cuando aparezca el aviso de renovación, pulsar **Cargar medidas**, completar altura y peso actualizados y guardar. Revisar la confirmación antes de salir.

El código usa ciclos de 60 días y avisa desde siete días antes. El aviso de ciclo vencido no equivale por sí solo a que una propuesta nueva esté vigente; la revisión del entrenador sigue siendo necesaria. Estos plazos describen el código observado y están señalados como diferencia documental en el informe.

Tras tres ciclos consecutivos sin confirmar las medidas, el área de alumno puede quedar restringida:

1. Completar peso y altura en **Regularización de mediciones**.
2. Enviar y verificar el estado pendiente de aprobación.
3. Esperar que el entrenador asignado apruebe la regularización.
4. Volver a acceder al área del alumno.

Guardar las medidas no desbloquea automáticamente. Si todavía no hay entrenador, solicitar al gimnasio la asignación. La evaluación automática de ciclos requiere que se ejecuten los jobs del backend.

### 3.7 Consultar ejercicios

Entrar en **Ejercicios** (`/alumno/catalogo`), buscar por nombre y combinar los filtros disponibles de músculo, equipamiento, patrón, dificultad, origen o disponibilidad. Abrir una ficha para ver instrucciones, consejos, músculos, articulaciones, equipamiento e imágenes disponibles. Usar la paginación para recorrer resultados.

El mapa muscular de la ficha describe el ejercicio; no es un cálculo del progreso personal. El alumno consulta el catálogo y no crea ni habilita ejercicios.

### 3.8 Secciones todavía pendientes

**Sesión**, **Progreso** e **Historial** son pantallas de presentación. No hay un flujo operativo para cargar series ejecutadas, guardar un entrenamiento, consultar récords o ver evolución personal desde esas opciones.

## 4. Manual del entrenador

### 4.1 Consultar la cartera y abrir un alumno

Entrar en **Cartera** (`/entrenador`) o **Alumnos** (`/entrenador/alumnos`). La cartera consulta alumnos reales asignados, prioriza atención y muestra recuentos de bloqueos y revisiones pendientes.

Abrir un alumno para consultar el estado, faltas consecutivas de mediciones, última medición, altura, resumen de rutina, condiciones físicas declaradas y propuestas pendientes. Las pestañas **Resumen**, **Rutina** y **Mediciones** actualmente llevan a la misma ficha; no representan tres módulos independientes ni una serie histórica completa de mediciones.

Sólo puede trabajar con alumnos con asignación vigente. Si un alumno no aparece, pedir al administrador que revise la asignación. Un entrenador con rol Alumno necesita otro entrenador para la revisión de su propia rutina.

### 4.2 Invitar alumnos

1. Abrir **Invitar alumnos** (`/entrenador/invitaciones`).
2. Ingresar el correo y pulsar **Enviar invitación**. El rol se fija en Alumno.
3. Consultar estado y vencimiento en el listado.
4. Si corresponde y tiene permiso, usar **Reenviar** o **Revocar** en una invitación vigente.

Cuando el alumno completa una invitación emitida por el entrenador, queda asignado a él. Reenviar invalida el enlace previo; revocar requiere confirmación. La pantalla distingue fallos de entrega del correo: verificar el resultado antes de considerar que la persona recibió la invitación.

### 4.3 Crear y mantener plantillas

Entrar en **Plantillas** (`/entrenador/plantillas`).

1. Completar nombre y tipo de la plantilla; la cantidad de días se define en su estructura.
2. Agregar días y nombrarlos.
3. Buscar y agregar ejercicios habilitados.
4. Configurar series: mínimo y máximo de repeticiones, descanso y calentamiento cuando corresponda; completar los demás campos que ofrezca el editor.
5. Crear la plantilla y verificar la confirmación.
6. Para modificar una existente, abrir **Editar** y **Guardar cambios**.
7. Para retirarla de la selección habitual, usar **Desactivar**.

Editar una plantilla no cambia las rutinas ya creadas a partir de ella. La pantalla actual lista plantillas activas y ofrece desactivarlas; no presenta un recorrido de reactivación, aunque backend contempla esa operación.

### 4.4 Crear una rutina para un alumno

Abrir la ficha del alumno y la sección de prescripción. Si está bloqueado por mediciones, resolver primero su regularización.

| Alternativa | Pasos | Resultado |
| --- | --- | --- |
| Desde plantilla | Elegir una plantilla activa y pulsar **Asignar como propuesta**, nombre actual del botón | Copia independiente pendiente de revisión |
| Manual | Completar tipo y frecuencia, agregar días, ejercicios habilitados y series; enviar el formulario | Rutina `PROPUESTA` |
| IA | Escribir indicaciones en el panel de generación de la ficha y enviar | Rutina pendiente después del procesamiento y validación |

Si ya hay una propuesta sin resolver, revisarla antes de crear otra. Crear o copiar una rutina no la pone en vigencia. Las alternativas manual y por plantilla siguen disponibles cuando falla la generación.

### 4.5 Revisar una rutina inicial o de reemplazo

1. Entrar en **Rutinas → Por revisar** (`/entrenador/rutinas/revisar`).
2. Abrir una rutina por aprobar. También puede revisarse desde la ficha del alumno.
3. Examinar días, ejercicios, series y advertencias. En la pantalla dedicada puede pedir cambios con IA antes de decidir.
4. Completar una observación si corresponde.
5. Elegir **Aprobar y poner en vigencia** o **Rechazar**.
6. Para rechazar, indicar obligatoriamente el motivo. Si hay diferencia con el objetivo del alumno, revisar y confirmar expresamente cuando se solicite.
7. Verificar la decisión registrada.

La aprobación archiva la rutina vigente anterior, si existía. El rechazo conserva la vigente anterior. Una propuesta con ejercicios que dejaron de estar habilitados puede impedir la aprobación: recargar, revisar y solicitar otra cuando corresponda. Si cambió el contexto o alguien resolvió la propuesta desde otra sesión, actualizar antes de volver a decidir.

La pantalla dice que el alumno recibe el motivo del rechazo, pero el recorrido de consulta de rutinas rechazadas no está expuesto en su interfaz actual. No asumir que existe una bandeja de avisos o que el alumno podrá leerlo allí.

### 4.6 Resolver una propuesta de adaptación o renovación

En **Rutinas → Por revisar** también aparecen propuestas de ajustes sobre rutinas existentes. Son diferentes de las rutinas iniciales pendientes.

1. Abrir la propuesta.
2. Consultar período, diagnóstico y evidencia disponibles; atender la advertencia de datos desactualizados.
3. Comparar valores anteriores y propuestos. Los cambios de estructura muestran el detalle de la planilla.
4. Para aceptar todo, usar **Aprobar**.
5. Para aceptar parte, marcar los ajustes elegidos y usar **Aprobar parcialmente**, si está habilitado para esa propuesta.
6. Para rechazar, escribir motivo y pulsar **Rechazar**.
7. Verificar la resolución. La aprobación genera una nueva versión y conserva la anterior.

Cuando aparezca **Regenerar con IA**, describir qué debe mejorar la planilla y usar **Regenerar planilla con IA**. Esperar el estado final y revisar el resultado antes de aprobar. Si falla, la planilla anterior sigue disponible. El reemplazo usa los ejercicios habilitados y parámetros actuales del gimnasio.

Este flujo puede operar sobre propuestas existentes y las producidas por la renovación implementada. No significa que ya exista un diagnóstico automático completo basado en sesiones reales: el registro de sesiones y ese ciclo analítico siguen pendientes.

### 4.7 Aprobar una regularización de mediciones

1. Abrir al alumno bloqueado desde la cartera.
2. Comprobar que cargó peso y altura y que la regularización espera aprobación.
3. Usar la acción del panel de desbloqueo.
4. Verificar **Alumno desbloqueado**. La racha de faltas vuelve a cero y recupera el acceso.

Si faltan las medidas, pedir al alumno que las complete. Sólo el entrenador asignado puede aprobar esta regularización.

### 4.8 Proponer ejercicios propios

En **Ejercicios** (`/entrenador/catalogo`), usar la acción de proponer una ficha propia. Completar nombre, descripción, instrucciones, consejos, patrón, dificultad, equipamiento, músculos y articulaciones; agregar la información de imágenes admitida por el formulario. Enviar a revisión.

Puede editar sus propias fichas mientras no estén aprobadas. Para corregir una aprobada, el administrador debe retirarla antes. La aprobación y la habilitación para el gimnasio las realiza el administrador. **Mi perfil** del entrenador sigue siendo una pantalla de presentación.

## 5. Manual del administrador

### 5.1 Preparar el gimnasio

La entrada **Analítica** muestra una lista de preparación conectada al backend junto con indicadores de muestra. Para dejar disponible el circuito de rutinas:

1. Invitar al menos un entrenador y esperar que complete su cuenta.
2. Registrar el equipamiento.
3. Revisar el catálogo y habilitar explícitamente ejercicios aprobados.
4. Invitar alumnos y asignarles entrenador.
5. Configurar opcionalmente los parámetros de generación.

La lista de preparación sólo comprueba entrenadores e inventario. Que figure completa no certifica catálogo habilitado, conectividad con IA ni un recorrido completo operativo.

### 5.2 Invitar personas

Abrir **Invitaciones** (`/admin/usuarios`). Ingresar correo, elegir uno o varios roles del gimnasio —Alumno, Entrenador, Administrador— y enviar. Consultar las invitaciones, sus roles, emisor, emisión, vencimiento y estado. Reenviar o revocar cuando la acción esté disponible y el backend autorice.

Esta pantalla administra invitaciones. No contiene una gestión completa de cuentas existentes para cambiar roles, aptitud, membresía, suspender usuarios o consultar auditoría. El rol SuperAdmin no se concede por este formulario.

### 5.3 Asignar o cambiar entrenador

1. Abrir **Asignaciones** (`/admin/asignaciones`).
2. Localizar al alumno; los que no tienen entrenador aparecen primero.
3. Elegir un entrenador del gimnasio.
4. Pulsar **Asignar** o **Cambiar**.
5. Revisar la confirmación.

Si no hay entrenadores disponibles, invitar uno. La pantalla evita la autoasignación. Las rutinas pendientes bloqueadas por falta de entrenador pueden pasar a su bandeja cuando se completa la asignación.

### 5.4 Registrar inventario y habilitar ejercicios

La aplicación tiene dos entradas de inventario, con comportamientos distintos en esta versión:

| Entrada | Uso observado |
| --- | --- |
| **Inventario** (`/admin/inventario`) | Seleccionar equipamiento y guardar; presenta cobertura calculada y marca incompatibilidades de rutinas según el recorrido anterior |
| **Catálogo** (`/admin/ejercicios`), panel de inventario | Guardar equipamiento con control de revisión; devuelve ejercicios habilitados relacionados para revisarlos manualmente |

Para preparar el catálogo actual, usar el panel de **Catálogo**, guardar el equipamiento y revisar los ejercicios relacionados. **El inventario no habilita automáticamente ejercicios.** Cambiar máquinas y habilitar ejercicios son operaciones distintas. La divergencia entre las dos entradas está registrada en el informe técnico; no asumir que producen idénticos efectos sobre rutinas anteriores.

En el catálogo:

1. Buscar y filtrar ejercicios.
2. Marcar o desmarcar su disponibilidad para el gimnasio.
3. Guardar el lote de cambios con el botón que muestra la pantalla.
4. Verificar el mensaje de confirmación. Se admiten hasta 200 cambios pendientes por lote.

Sólo pueden habilitarse fichas aprobadas. El peso corporal se considera siempre disponible como equipamiento. Antes de salir, guardar: las selecciones pendientes todavía no son cambios confirmados.

### 5.5 Revisar fichas propias del gimnasio

1. Filtrar por origen del gimnasio y estado de ficha.
2. Abrir el detalle y revisar técnica, clasificación e imágenes.
3. Para aprobar, pulsar **Aprobar ficha**. Si también debe quedar disponible, seleccionar **Habilitar en el gimnasio al aprobar**.
4. Para rechazar, escribir el motivo y pulsar **Rechazar**.
5. Para retirar una ficha aprobada, indicar motivo y usar **Retirar ficha**.

Aprobar sin marcar la habilitación no la incorpora a las nuevas prescripciones. Retirar conserva el historial y deshabilita la ficha. El administrador revisa las fichas; el formulario de propuesta y edición pertenece al entrenador autor.

### 5.6 Configurar la generación

Abrir **Configuración** (`/admin/configuracion`).

1. Elegir si se usarán parámetros definidos por el gimnasio.
2. Configurar mínimos y máximos de ejercicios por día, series de trabajo, repeticiones y descanso; indicar cantidad de series de calentamiento.
3. Guardar y verificar la confirmación.
4. Si otro administrador cambió los valores, **Recargar parámetros** antes de guardar otra vez.

Sin parámetros guardados, la IA decide la prescripción según el contexto. Los parámetros se aplican a nuevas generaciones, renovaciones y regeneraciones. Una propuesta existente conserva su configuración; hay que regenerarla para usar los valores nuevos.

### 5.7 Límites de esta área

Los valores **182**, **74 %** y **13** del panel Analítica son ilustrativos, no indicadores reales del gimnasio. **Reglas** es una pantalla de presentación y no permite editar cálculos. El administrador no cuenta en esta interfaz con acceso al detalle de salud o sesiones de alumnos.

## 6. Manual del SuperAdmin

### 6.1 Dar de alta un gimnasio

1. Abrir **Alta de gimnasio** (`/superadmin/gimnasios/nuevo`).
2. Completar nombre, zona horaria y correo del primer administrador.
3. Confirmar la creación y verificar el destinatario informado.
4. Pedir al administrador que complete su cuenta con el enlace del correo.
5. Consultar en **Gimnasios** el estado de esa invitación.

El gimnasio queda creado con su invitación de arranque. El SuperAdmin no registra las medidas de alumnos ni revisa sus rutinas.

### 6.2 Mantener los gimnasios

En **Gimnasios** (`/superadmin`):

| Acción | Pasos y resultado |
| --- | --- |
| Editar | Cambiar nombre o zona horaria y guardar; si hay sesiones registradas, puede requerirse confirmar el impacto del cambio horario |
| Suspender | Pulsar **Suspender**, leer el mensaje y confirmar; los usuarios del gimnasio no pueden ingresar mientras siga suspendido |
| Reactivar | Pulsar **Reactivar** y confirmar para permitir nuevamente el acceso |
| Reenviar invitación inicial | Usar la acción mientras el primer administrador no haya completado la cuenta; verificar el correo destinatario |

La suspensión no borra los datos. El listado informa estados pendiente, vencida, revocada o usada de la invitación inicial cuando existe. Una invitación usada no se reenvía para volver a crear al administrador.

## 7. Problemas habituales

| Situación | Cómo continuar |
| --- | --- |
| No llega una invitación o recuperación | Revisar spam y el correo informado; comprobar el resultado de envío y usar el enlace más reciente |
| No puedo generar | Completar contexto, consentimiento y declaración de condiciones; pedir al administrador que revise ejercicios aprobados y habilitados |
| La IA no puede cumplir las indicaciones | Leer la explicación y reformular; el entrenador puede crear una propuesta manual o usar una plantilla |
| La IA está indisponible | Reintentar cuando se habilite; las demás funciones y alternativas manuales continúan |
| Ya existe una propuesta | Abrirla y pedir cambios o solicitar su resolución; no enviar otra solicitud inicial |
| La propuesta cambió en otra sesión | Recargar y volver a revisar antes de aprobar |
| Un ejercicio dejó de estar disponible | Revisar con el administrador y el entrenador; puede ser necesario rechazar o regenerar la propuesta |
| No aparece un alumno en la cartera | Revisar la asignación con el administrador |
| Cargué medidas y sigo restringido | Esperar la aprobación del entrenador; guardar medidas no equivale a desbloquear |
| No puedo ingresar después de una suspensión | Pedir al responsable que revise el estado de la cuenta o del gimnasio |
| Sesión, Progreso o Historial no registran nada | Son pantallas pendientes en esta versión |

## 8. Recorrido sugerido para una demostración

1. SuperAdmin crea el gimnasio; el primer administrador acepta la invitación.
2. Administrador invita a un entrenador, registra inventario y habilita ejercicios.
3. Entrenador acepta la cuenta e invita a un alumno.
4. Alumno acepta, completa contexto, consentimiento y condiciones físicas.
5. Alumno solicita una rutina con IA; si el servicio no está operativo, el entrenador crea una manual o desde plantilla.
6. Alumno consulta la propuesta y, opcionalmente, pide cambios.
7. Entrenador revisa y pone en vigencia.
8. Alumno abre Mi rutina y verifica el estado y la prescripción.

Este recorrido demuestra el circuito de prescripción disponible. La ejecución de entrenamientos, las métricas de progreso y el historial de sesiones requieren implementación adicional.
