# Preparación repetible de la demostración de adaptación

Ventana operativa incorporada el 15 de noviembre de 2026 para la exposición de Vivaz Adaptive. Usa alumnos y ejercicios existentes de la misma base del despliegue. La autorización del solicitante incluye preparar sus historiales y restaurarlos; no requiere una base de demostración separada. Los datos de entrenamiento preparados se identifican como simulados según [RN-107](../domain/business-rules.md#12-datos-privacidad-y-trazabilidad).

Material de apoyo para la exposición: [guía de estudio de 2:30](guia-estudio-diagnostico-propuesta-2m30.md) y [lista breve de preparación y repetición](preparacion-demo-diagnostico-y-propuestas.md).

## Habilitar en el despliegue

1. Promover los cambios de backend y frontend mediante el [flujo habitual](../delivery/github-workflow.md).
2. Aplicar las migraciones nuevas del backend con el rol migrador: `20261115120000_adaptation_demo_runs` y `20261115121000_demo_routine_origin`. Son aditivas; preservan las prescripciones y los entrenamientos previos. La segunda extiende la procedencia de rutina y su restricción de integridad.
3. Configurar `ADAPTATION_DEMO_ENABLED=true` en el backend y desplegarlo. La omisión o `false` deshabilita las tres operaciones HTTP. La autorización sigue exigiendo sesión, rol ENTRENADOR y asignación vigente en el mismo gimnasio; no existe una clave administrativa en el navegador.
4. Desplegar el frontend compatible. Entrar como entrenador y abrir **Rutinas → Preparar demo**, o `/entrenador/demostracion/adaptacion`. El enlace abre una ventana separada con la misma sesión.

Para volver a deshabilitar el panel, restaurar primero todas las preparaciones activas y luego cambiar la variable a `false`. El despliegue y las migraciones sobre la base compartida no forman parte de la verificación local del cambio.

## Preparar la presentación de 2:30

1. Elegir un alumno existente, activo y asignado al entrenador. Debe tener una rutina vigente completa, con ejercicios compatibles, aprobados y habilitados en el gimnasio. No debe haber una sesión en curso.
2. Pulsar **Preparar estímulo insuficiente** y esperar el resultado. La ventana conserva el estado aunque se recargue. No hace falta invocar un cron ni cargar sesiones una por una.
3. Abrir **Bandeja** o **Ver propuesta**. Verificar un ajuste de carga **60 → 62,5 kg**, el criterio y las métricas. Las advertencias de mediciones originales siguen siendo aplicables: el panel no modifica peso, altura, objetivo, condiciones ni consentimiento.
4. Durante la exposición, mostrar la propuesta pendiente, el sustento y la aprobación o rechazo. Marcar los ajustes a aceptar y pulsar **Aprobar seleccionados (cantidad)**; para aceptar todo, **Seleccionar todos → Aprobar todos (cantidad)**. Sin selección no se puede aprobar. Aprobar crea una versión nueva sólo con los ajustes seleccionados; los restantes quedan rechazados. Los umbrales siguen siendo convenciones del proyecto sin validación profesional; no presentar estos registros como entrenamiento real.
5. Al terminar, pulsar **Restaurar datos originales** para cada alumno utilizado.

## Casos disponibles y repetición

Los botones preparan estímulo insuficiente, sobreexigencia, primer estancamiento, segundo estancamiento, progresión adecuada y datos insuficientes. Se mantienen el tipo de rutina y sus ejercicios existentes. La prescripción temporal respeta los límites del tipo y el motor aplica las [reglas de ajuste](../domain/business-rules.md#92-reglas-de-ajuste--rn-89a). Progresión adecuada y datos insuficientes no generan propuestas.

Cada día de la rutina recibe sesiones históricas con fechas relativas al día del cálculo, cubriendo las dos mitades del período de seis semanas. El caso de datos insuficientes prepara sólo tres sesiones del primer día, para que un ejercicio repetido en varios días tampoco alcance cuatro sesiones. El segundo estancamiento agrega un diagnóstico anterior real sobre el historial preparado; requiere al menos una alternativa aprobada, habilitada, de igual patrón y elegible para el alumno, que no esté ya en la rutina. No se crean ejercicios alternativos ficticios.

Las cargas, repeticiones, descansos y esfuerzos preparados varían entre ejercicios, series y sesiones. Los días de rutina se distribuyen en fechas distintas. La variación es determinística para que repetir el mismo caso conserve la evidencia; los resultados siempre se calculan con RN-79a, sin escribir métricas ni situaciones a mano. Estímulo insuficiente conserva el tope de repeticiones y esfuerzo bajo en las dos últimas sesiones; sobreexigencia mantiene tres sesiones consecutivas de bajo cumplimiento. En estancamiento, pequeñas variaciones de carga y repeticiones producen cambios de capacidad estimada por debajo del umbral de progresión.

La propuesta presenta un resumen de métricas con unidades y coma decimal, y una tabla cronológica de cumplimiento y esfuerzo por sesión. Los datos faltantes se identifican como sin registrar y los criterios no evaluados se declaran. El detalle se puede desplegar cuando hay más de seis sesiones.

Repetir el mismo caso pendiente el mismo día reutiliza su preparación. Tras aprobar o rechazar, pulsar nuevamente el caso crea una preparación nueva y conserva el original como punto de retorno. Cambiar de caso restaura el anterior y prepara el siguiente en una sola transacción. Si el siguiente falla, permanece intacta la preparación anterior. Se admite una preparación activa por alumno, por lo que pueden prepararse varios alumnos para tener varias propuestas simultáneas.

La preparación guarda una versión interna del generador. Al pulsar el caso sobre una preparación anterior a esta revisión, se restaura y se vuelve a preparar una sola vez; los clics posteriores reutilizan la versión actual. La actualización conserva la evidencia anterior y no necesita migraciones adicionales.

## Restauración y trazabilidad

El punto de retorno guarda la rutina y versión originales. Preparar archiva temporalmente esa rutina y activa una de origen `DEMOSTRACION`, enlazada al punto de retorno. Restaurar archiva la rutina preparada, incluidas las versiones creadas al aprobar; reactiva la original, invalida propuestas todavía pendientes y vence sus avisos. No elimina diagnósticos ni auditorías, porque son evidencia inmutable. Las preparaciones restauradas quedan fuera de los listados de uso habitual.

Las sesiones y diagnósticos preparados llevan procedencia simulada. Los indicadores reales y los jobs periódicos de diagnóstico, propuestas, renovación y controles de mediciones no incorporan esta preparación. El inicio de entrenamiento real queda bloqueado hasta restaurar. Preparar, aprobar y restaurar se coordinan con los bloqueos de alumno y catálogo; una rutina distinta puesta en vigencia o una regeneración pendiente impiden una restauración que pudiera pisar cambios ajenos.

Cerrar la ventana no restaura automáticamente: la preparación es durable y puede recuperarse. Cada repetición después de resolver conserva evidencia y puede aumentar el almacenamiento; esta herramienta es para la demostración acotada, no para poblar masivamente el sistema.

## Verificación y contrato

El backend publica `openapi/adaptation-demo.openapi.json`, generado desde los schemas HTTP. El frontend genera su contrato con `npm run demo:contract`. Operaciones: `GET /demo/adaptations`, `POST /demo/adaptations/{studentId}` y `POST /demo/adaptations/{studentId}/restore`.

Pruebas de dominio: seis escenarios en los cuatro tipos de rutina. Pruebas API: sesión, rol, asignación, flag, validación y conflictos. Integración PostgreSQL: escenarios, aprobación, rechazo, repetición concurrente, reversión de fallos, preservación del original y bloqueo de entrenamiento. Las pruebas de integración requieren `ADAPTATION_DEMO_TEST_DATABASE_URL` con una base efímera local llamada `gym_demo_test`; nunca usan `DATABASE_URL` como alternativa. La interfaz tiene pruebas de interacción y revisión en navegador a 360 px y en escritorio.
