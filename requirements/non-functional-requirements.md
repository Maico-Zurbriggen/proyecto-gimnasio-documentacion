# D9 — Requerimientos no funcionales

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.1        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | D1, D5, D8 |

Sólo se incluyen requerimientos con criterio de verificación concreto. Un requerimiento no funcional sin forma de comprobarlo es una aspiración.

**Cambios de la v1.0:** RNF-24 y RNF-25 llevan tamaño de muestra declarado, sin el cual no eran verificables · RNF-15 fija un criterio comprobable en lugar de un adjetivo · RNF-37 a RNF-40 cubren invitación, inventario, reevaluación masiva y desbloqueo.

**Cambios de la v2.1 ([baseline de alcance](../planning/baseline-alcance-2026-09.md)):** se corrigen cuatro requisitos que seguían nombrando la estimación de riesgo, retirada del alcance en el replanteo de IA · RNF-11 y RNF-18 dejan de apoyarse en los presets, diferidos con RF-021 · **RNF-35 queda diferido** con RF-049 · se incorporan **RNF-41** (dónde queda confinado el texto libre del usuario) y **RNF-42** (nadie se queda sin plan), este último porque el criterio de éxito E1 dejó de estar garantizado al retirarse los presets.

---

## 1. Rendimiento

| ID     | Requerimiento                      | Criterio de verificación                                                                                              |
| ------ | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| RNF-01 | Lectura de las vistas principales  | Percentil 95 por debajo de 500 ms con 300 alumnos y 150.000 registros de serie cargados                               |
| RNF-02 | Panel de progreso del alumno       | Carga completa en menos de 1,5 s con seis meses de historial                                                          |
| RNF-03 | Cartera del entrenador             | Se ordena y presenta en menos de 1,5 s con 50 alumnos                                                                 |
| RNF-04 | Generación de una rutina           | La solicitud se acepta sin esperar al LLM; cada intento alcanza un estado terminal en un máximo inicial configurable de 120 s, con un solo reintento antes de declarar indisponibilidad |
| RNF-05 | Diagnóstico y procesos diferidos ✎ | Se ejecutan fuera del camino de la petición del usuario. Ninguna vista queda a la espera de su cálculo. *(v2.1: se retira «estimación de riesgo», sin sujeto desde [D11/DD-34](../decisions/design-decisions.md))* |

## 2. Usabilidad

| ID     | Requerimiento                                                                                               | Criterio de verificación                                                                                                            |
| ------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| RNF-06 | La sesión de entrenamiento es plenamente usable en pantalla de 360 px de ancho                              | Recorrido completo de registro de una sesión de 5 ejercicios ejecutado en un dispositivo de ese ancho sin desplazamiento horizontal |
| RNF-07 | Registrar una serie con los valores precargados correctos requiere como máximo dos interacciones            | Medido sobre el recorrido de RNF-06                                                                                                 |
| RNF-08 | El alumno completa su incorporación en tres pasos como máximo, de los cuales sólo el primero es obligatorio | Verificado sobre FL-01                                                                                                              |
| RNF-09 | Ninguna vista presenta cero, vacío ni un valor por defecto cuando la causa es falta de datos                | Revisión sistemática de todas las vistas con un alumno sin historial. Ver D10/§A                                                    |

## 3. Robustez y continuidad

| ID     | Requerimiento                                                                             | Criterio de verificación                                                                                                     |
| ------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| RNF-10 | La sesión en curso conserva un estado local y reintenta el envío ante pérdida de conexión | Prueba con red interrumpida durante el registro: ningún dato ingresado se pierde                                             |
| RNF-11 | Ningún fallo generativo degrada el resto del sistema ni expone un error técnico ✎          | Prueba con API IA, Cloudflare Tunnel o LLM inaccesible: la generación se declara no disponible y **las plantillas y operaciones manuales siguen funcionando** (RF-019). *(v2.1: los presets dejan de ser la contingencia — RF-021, alcance opcional.* **Esta prueba ya no demuestra que un alumno nuevo obtenga rutina**: eso es RNF-42*)* |
| RNF-12 | La no ejecución de los procesos diferidos no degrada ninguna otra funcionalidad           | Prueba con la base sin diagnósticos ni estimaciones: todas las vistas funcionan y declaran la información como no disponible |
| RNF-13 | El envío repetido de una misma operación de registro no produce duplicados                | Envío del mismo registro de serie tres veces: un único registro resultante                                                   |

## 4. Seguridad

| ID     | Requerimiento                                                                                                                                                                                                  | Criterio de verificación                                                                                                                                  |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-14 | Toda operación sobre un recurso de un alumno concreto rechaza a un actor no autorizado                                                                                                                         | Una prueba automatizada por cada operación con identificador de alumno, que verifica el rechazo con un actor autenticado pero sin relación con el recurso |
| RNF-15 | Las contraseñas se almacenan mediante una función de derivación de clave con sal única por usuario y coste configurable, calibrada para que una verificación tarde al menos 200 ms en el entorno de producción | Medición del tiempo de verificación e inspección del almacenamiento: ninguna contraseña recuperable, ninguna sal compartida                               |
| RNF-16 | Las credenciales de sesión no son accesibles desde el código de la página                                                                                                                                      | Inspección                                                                                                                                                |
| RNF-17 | Los intentos de autenticación están limitados por origen y por período                                                                                                                                         | Prueba: el sexto intento en un minuto desde un mismo origen es rechazado                                                                                  |
| RNF-18 | Las invocaciones a servicios externos de generación están limitadas por usuario y por período                                                                                                                  | Prueba: superado el límite, no se envía otra invocación, se informa indisponibilidad temporal y permanece disponible la creación manual de plantillas por el entrenador ✎ |
| RNF-19 | Ningún registro de diagnóstico contiene credenciales, contraseñas ni datos de salud                                                                                                                            | Inspección de los registros producidos durante el recorrido completo                                                                                      |
| RNF-20 | El acceso del entrenador cesa en el instante en que finaliza la asignación                                                                                                                                     | Prueba: operación iniciada antes y confirmada después del fin de la asignación, rechazada                                                                 |

## 5. Privacidad

| ID     | Requerimiento                                                                                                 | Criterio de verificación                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| RNF-21 | Los datos de condiciones físicas, aptitud y mediciones sólo se tratan con consentimiento explícito registrado | Prueba: sin consentimiento registrado, las operaciones correspondientes son rechazadas                                           |
| RNF-22 | La baja de cuenta produce anonimización efectiva en 7 días o menos                                            | Prueba: tras el proceso, ningún dato identificatorio del usuario es recuperable, y sus sesiones siguen contando en los agregados |
| RNF-23 | El sistema no solicita ni almacena documento de identidad ni domicilio                                        | Inspección del modelo de datos                                                                                                   |

## 6. Calidad de los componentes inteligentes

| ID     | Requerimiento                                                                                         | Criterio de verificación                                                                                                                                                                                                                                                                                                                                              |
| ------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-24 | Ningún texto generado contiene un valor numérico ausente de sus datos de entrada                      | Verificación automática sobre **50 textos generados** de cada tipo narrativo: tasa de valores no presentes igual a cero                                                                                                                                                                                                                                               |
| RNF-25 | Toda rutina generada es válida por construcción                                                       | Sobre **200 rutinas generadas** cubriendo los cuatro tipos y al menos tres inventarios distintos: 100% con ejercicios existentes en el catálogo prescribible, 100% sin ejercicios incompatibles, 100% dentro de los rangos de la tabla de derivación del tipo, 100% con la cobertura mínima de patrones o con la declaración explícita de qué patrón no pudo cubrirse |
| RNF-26 | La rutina generada se evalúa contra un criterio de referencia explícito ✎ | Tras [DD-34](../decisions/design-decisions.md) no queda un modelo clásico contra el que comparar en la Etapa 1. El criterio de referencia pasa a ser **la rutina que un entrenador construye a mano sobre el mismo caso**, sobre un conjunto fijo de casos. Que la construida a mano resulte mejor es un resultado admisible y debe informarse |
| RNF-27 | Toda salida de un componente inteligente es reproducible a partir de lo registrado                    | Dado un resultado almacenado, su versión de componente y su contexto de entrada permiten reejecutar y obtener el mismo resultado                                                                                                                                                                                                                                      |
| RNF-28 | Todo resultado producido sobre datos simulados está identificado como tal en toda presentación ✎ | Inspección de las vistas de indicadores, diagnóstico y propuestas de adaptación. *(v2.1: se retira «vistas de riesgo», sin sujeto desde DD-34)* |

## 7. Mantenibilidad y entrega

| ID     | Requerimiento                                                                                                              | Criterio de verificación                            |
| ------ | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| RNF-29 | La lógica de cálculo de indicadores y la de construcción y validación de rutinas están cubiertas por pruebas automatizadas | Cobertura igual o superior al 70% en esos módulos   |
| RNF-30 | Toda incorporación de cambios exige la ejecución exitosa de la verificación automatizada                                   | Configuración del repositorio                       |
| RNF-31 | Un integrante que clona el repositorio tiene el sistema en ejecución local en menos de 10 minutos                          | Prueba con un integrante que no lo haya hecho antes |
| RNF-32 | Los cambios de estructura de datos están versionados desde el inicio                                                       | Inspección del repositorio                          |

## 8. Compatibilidad y accesibilidad

| ID     | Requerimiento                                                                                                          | Criterio de verificación                                                 |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| RNF-33 | Funciona en las dos últimas versiones de los navegadores mayoritarios, de escritorio y móviles                         | Recorrido de FL-05 y FL-02 en cada uno                                   |
| RNF-34 | Contraste de texto conforme al nivel AA, navegación completa por teclado y etiquetas en todos los campos de formulario | Auditoría automatizada más recorrido manual por teclado de FL-02 y FL-05 |
| RNF-35 | ⏸ **DIFERIDO** con RF-049. La presentación en barras por grupo muscular queda cubierta por RNF-34                     | —                                                                        |

## 9. Escalabilidad

| ID     | Requerimiento                                                                                                                                              | Criterio de verificación                                                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| RNF-36 | El diseño soporta 5.000 alumnos sin rediseño estructural                                                                                                   | Prueba de carga con ese volumen sembrado, cumpliendo RNF-01             |
| RNF-39 | Un cambio del inventario del gimnasio reevalúa todas las rutinas vigentes afectadas en menos de 60 s con 500 alumnos, sin bloquear ninguna sesión en curso | Prueba: retirar un equipamiento usado por el 30% de las rutinas y medir |

## 10. Alta y arranque

| ID     | Requerimiento                                                                                                           | Criterio de verificación                                                                                               |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| RNF-41 🆕 | El texto libre del usuario queda confinado a la interpretación de RF-053 y no alcanza a ningún otro componente generativo | Inspección del contrato del servicio IA: el único campo de texto libre del usuario es la entrada de `interpretarPedido`; su salida se valida contra las enumeraciones cerradas de D2/§4 y se confirma con el usuario antes de propagarse. `generarRutina`, `sugerirAlternativas` y los narrativos reciben sólo parámetros tipados y estructuras ya validadas |
| RNF-42 🆕 | Todo alumno con contexto suficiente tiene una rutina propuesta dentro de las 24 h de completar su incorporación         | Consulta sobre la base: cero alumnos con contexto suficiente y sin rutina propuesta ni vigente. Es el criterio de éxito E1 hecho comprobable, y **el que la indisponibilidad generativa pone en riesgo** — ver RNF-11 y D12/R-17 |
| RNF-37 | Ninguna cuenta puede crearse sin una invitación vigente                                                                 | Prueba: todo intento de alta sin invitación, con invitación caducada, revocada o ya usada, es rechazado                |
| RNF-38 | El aprovisionamiento de un gimnasio es atómico: o quedan creados el gimnasio y su primer administrador, o no queda nada | Prueba con fallo inducido a mitad del proceso: ningún gimnasio sin administrador en la base                            |
| RNF-40 | El desbloqueo de una sesión es irrepetible y siempre auditado                                                           | Prueba: el segundo desbloqueo de la misma sesión es rechazado, y el primero deja registro con actor, motivo e instante |

---

## No incluidos deliberadamente

Se nombran para dejar constancia de que fueron considerados y descartados por alcance, lo que vale más que implementarlos a medias:

acuerdo de nivel de servicio de disponibilidad · internacionalización · funcionamiento sin conexión completo · escalado horizontal · alta disponibilidad · doble factor de autenticación · cifrado a nivel de campo · auditoría de seguridad externa · gestión centralizada de secretos.
