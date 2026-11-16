# Preparar y repetir la demo de diagnóstico y propuestas

El panel usa **los alumnos y los ejercicios existentes de la muestra desplegada**. Prepara un historial identificado como simulado y calcula el diagnóstico y la propuesta con el motor real. Conserva la rutina y el entrenamiento originales para restaurarlos.

## Dejarlo habilitado una sola vez

- Integrar y desplegar los cambios del backend y frontend.
- Aplicar las dos migraciones nuevas de demostración mediante el proceso del proyecto.
- Configurar `ADAPTATION_DEMO_ENABLED=true` en el backend.
- Entrar con una cuenta de entrenador que tenga alumnos activos asignados.

El procedimiento técnico está en [la guía operativa](adaptation-demo.md). La implementación se verificó localmente; esta tarea no aplicó migraciones ni modificó datos en la base compartida.

## Preparación antes de los 2:30

1. Ir a **Rutinas → Preparar demo**: abre una ventana aparte.
2. Elegir un alumno con una rutina vigente y ejercicios habilitados. Finalizar cualquier sesión que esté en curso.
3. Pulsar **Preparar estímulo insuficiente** y esperar el resultado.
4. Abrir **Ver propuesta** o **Abrir bandeja**. Comprobar el cambio **60 → 62,5 kg**, el criterio y sus datos.
5. Dejar esa propuesta pendiente en la pantalla que vas a mostrar.

Durante la exposición seguí la [guía de estudio de 2:30](guia-estudio-diagnostico-propuesta-2m30.md). La preparación de datos se hace antes de empezar a contar el tiempo.

Para aprobar sólo algunos ajustes, marcarlos y pulsar **Aprobar seleccionados (cantidad)**. Para aprobar todo, usar **Seleccionar todos → Aprobar todos (cantidad)**. Sin selección no se puede aprobar; los ajustes sin marcar quedan rechazados al resolver la propuesta.

## Botones de respaldo

| Caso | Resultado que permite mostrar |
| --- | --- |
| Estímulo insuficiente | Aumentar carga: 60 → 62,5 kg. |
| Sobreexigencia | Reducir carga y quitar una serie, dentro de los límites. |
| Primer estancamiento | Cambiar esquema y volumen. |
| Segundo estancamiento | Sustituir por una alternativa existente y habilitada del mismo patrón. |
| Progresión adecuada | Evolución favorable; no se genera propuesta. |
| Datos insuficientes | Falta evidencia; no se genera propuesta. |

Para varias propuestas simultáneas, prepará distintos alumnos. Sobre un mismo alumno se mantiene un caso activo. El segundo estancamiento necesita una alternativa apta que no esté ya en su rutina; si falta, el panel informa el problema y conserva la preparación anterior.

## Repetir y terminar

- **Mismo caso pendiente, mismo día:** se reutiliza; no se duplican registros.
- **Después de aprobar o rechazar:** pulsar otra vez el caso crea una propuesta nueva.
- **Cambiar de caso:** restaura el anterior y prepara el siguiente automáticamente.
- **Al terminar:** pulsar **Restaurar datos originales** en cada alumno preparado. También funciona después de aprobar.
- **Si cerraste la ventana:** abrirla de nuevo; la preparación queda guardada.

Restaurar vuelve a la rutina original, archiva la preparada y retira sus propuestas pendientes de la bandeja. Los diagnósticos y la auditoría quedan conservados e identificados. Mientras haya una preparación activa, se impide iniciar entrenamiento real. Los datos preparados quedan fuera de los indicadores reales.

**Recordatorio para la defensa:** estos umbrales son convenciones del proyecto, todavía no validadas con un entrenador.
