# D11 — Registro de decisiones

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.2        |
| **Fecha**      | 2026-09-01 |
| **Estado**     | Normativo  |
| **Depende de** | Todos      |

**Cambios de la v1.0:** DD-13 (nutrición) queda resuelta · decisiones nuevas DD-26 a DD-32, que cierran los bloqueantes de la auditoría · 👁 marca las decisiones que las fuentes tomaron sin advertir que estaban decidiendo.

**Cambios de la v2.0:** DD-33, el candidato de rutina.

**Cambios de la v2.1:** DD-31 se ajusta al alcance generativo confirmado y a la ADR del servicio generativo: el LLM construye el candidato inicial; las tablas explícitas permanecen como validación y para el ciclo de adaptación.

**Cambios de la v2.2 ([baseline de alcance](../planning/baseline-alcance-2026-09.md)):** se escribe **DD-34**, el replanteo de IA del 2026-08-28 que ocho documentos del corpus ya citaban como fundamento y que **nunca había sido redactado** · se incorpora **DD-35**, el piso de disponibilidad de la prescripción tras retirarse los presets · **DD-33 queda derogada para la Etapa 1** y **DD-13 queda sin efecto** en ella; ambas conservan su texto íntegro por si el alcance se reabre.

**Alcance de estas decisiones.** Una decisión marcada «derogada para la Etapa 1» o «sin efecto» **no está anulada**: describe un diseño válido cuyo requisito de origen quedó fuera del alcance de esta etapa. Si el requisito vuelve, la decisión vuelve con él. Distinguirlo importa: borrarlas obligaría a rediscutirlas desde cero.

---

### DD-01 · Jerarquía de las fuentes

**Contexto.** Tres cuerpos de material de distinta antigüedad y autoridad, sin fechas.
**Elegida.** Pedido del cliente (RF-082 a RF-094 y decisiones posteriores) > especificación funcional > análisis de scope inicial.
**Fundamento.** El análisis inicial es una opinión escrita antes de conocer el pedido del cliente. Conciliar produciría un documento sin criterio.
**Consecuencia asumida.** Varias recomendaciones bien argumentadas del análisis inicial quedan derogadas, en particular su tesis de que el ajuste de la rutina es trabajo manual del entrenador.

### DD-02 · Copia al solicitar **más** versiones completas de la rutina

**Contexto.** Modificar una plantilla no debe alterar rutinas ya creadas (RF-022); aplicar una adaptación debe generar una versión nueva conservando las anteriores (RF-092).
**Opciones.** (a) Referencia a la plantilla. (b) Versionado con diferencias y propagación. (c) Copia sin versiones. (d) **Copia más versiones completas**.
**Elegida.** (d).
**Fundamento.** La objeción de coste al versionado apuntaba a las diferencias, la propagación y la resolución de conflictos. Una versión completa de una rutina es una copia profunda de una estructura pequeña: no hay diferencias que calcular ni conflictos que resolver, y RF-093 se responde comparando dos versiones.
**Consecuencia asumida.** Duplicación de datos, irrelevante a esta escala. Los cambios de plantilla no se propagan, que es el comportamiento deseado.

### DD-03 · La sesión congela su propia prescripción 👁

**Elegida.** Al iniciarse, la sesión copia la prescripción del día en sus registros de serie (RF-028).
**Fundamento.** Vuelve cada sesión autocontenida e inmune a toda edición posterior, y produce el cumplimiento por serie sin trabajo adicional.
**Consecuencia asumida.** Duplicación de la prescripción por sesión.
**Nota.** La especificación heredada enuncia esto como requerimiento sin registrar que es la decisión de modelado más determinante del sistema. Sin ella, el versionado de DD-02 reescribiría el pasado.

### DD-04 · Derivar los indicadores, persistir sólo eventos, salidas de componentes y marcas

**Elegida.** Derivar volumen, frecuencia, carga máxima estimada, adherencia y cumplimiento; persistir récords, diagnósticos, propuestas, estimaciones y el estado de compatibilidad de cada ejercicio de rutina.
**Fundamento.** Un indicador persistido queda inconsistente cuando cambia su definición. Un récord y una salida de componente son eventos fechados: recalcularlos pierde el instante y la versión.
**Excepción explícita.** El estado de compatibilidad es el único derivado que se persiste, porque la marca debe estar disponible al iniciar una sesión y en la vista de rutina sin recalcular el conjunto.

### DD-05 · Catálogo base global, catálogo propio por gimnasio

**Contexto.** RF-013 exige un catálogo accesible a todos; RF-069 exige aislamiento por gimnasio; RF-017 permite a entrenadores crear ejercicios. Las tres cosas no pueden ser ciertas con un catálogo único.
**Elegida.** Base global no editable más catálogo propio por gimnasio.
**Fundamento.** Un catálogo global único filtra ejercicios de un gimnasio a otro; uno replicado multiplica la carga inicial y la curación, que es el trabajo caro y el que determina la calidad del volumen.
**Consecuencia asumida.** Un entrenador no puede promover su ejercicio al catálogo base.

### DD-06 · La aptitud advierte, nunca bloquea

**Elegida.** Advertencia destacada al poner una rutina en vigencia y al iniciar una sesión; ninguna operación impedida `[F: cliente]`.
**Consecuencia asumida.** El sistema puede tener alumnos entrenando sin aptitud vigente. La responsabilidad queda en el gimnasio, y la advertencia queda registrada.

### DD-07 · El estado de membresía es informativo

**Elegida.** Informativo `[F: cliente]`.
**Fundamento.** Una regla de bloqueo atraviesa todos los flujos de entrenamiento y multiplica los casos borde a cambio de valor nulo para el ciclo central.

### DD-08 · Los roles son un conjunto 👁

**Fundamento.** Un entrenador también entrena. Modelarlo como valor único obliga a un rediseño en cuanto aparece el primer caso.
**Nota.** Es gratis ahora y caro después. Ver DD-28, que resuelve el caso concreto que esta decisión habilita.

### DD-09 · Nada se borra

**Elegida.** Desactivación lógica universal; la única eliminación real es la anonimización en la baja de cuenta.
**Consecuencia asumida.** El catálogo y la base de usuarios acumulan registros inactivos.

### DD-10 · La rutina es cíclica, no un calendario 👁

**Elegida.** El sistema propone el siguiente día del ciclo; el alumno elige.
**Fundamento.** Refleja cómo se entrena realmente y elimina un módulo entero de agenda, recordatorios y días perdidos. La adherencia se resuelve con la frecuencia semanal objetivo.
**Consecuencia asumida.** No hay recordatorios por día ni concepto de "día perdido".

### DD-11 · Constantes documentadas en lugar de configuración

**Elegida.** Constantes fijadas en D5, cada una con su origen marcado; RF-047 desciende a COULD.
**Fundamento.** Ventanas configurables hacen que la adherencia de dos alumnos no sea comparable, y la comparación es lo que sostiene la cartera priorizada y la analítica del gimnasio.

### DD-12 · Un solo entrenador vigente sobre una relación con historial

La estructura soporta el historial; RN-18 impone la unicidad. Sin el historial no se puede responder qué entrenador supervisó un período ni calcular la carga por entrenador. Coste marginal: nulo.

### DD-13 · Alcance de la pauta nutricional — **RESUELTA**

**Contexto.** El cliente pidió generar dietas y descartó el seguimiento de comidas. La especificación heredada había excluido la generación de planes nutricionales por riesgo sanitario sin validador profesional.
**Opciones.**

|     | Forma                                                                                       | Riesgo                                                                                                            | Coste |
| --- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----- |
| (a) | Plan de comidas redactado libremente por un componente generativo                           | **Alto.** Sin base de alimentos no hay forma de verificar la salida; puede producir déficits o ignorar patologías | Bajo  |
| (b) | Plantillas de menú precargadas y revisadas por el equipo                                    | Bajo                                                                                                              | Medio |
| (c) | **Distribución orientativa de energía y macronutrientes por comida, sin nombrar alimentos** | Bajo                                                                                                              | Bajo  |

**Elegida.** (c). RF-075 y RF-108 quedan redactados en esos términos; RF-076 sigue fuera.
**Fundamento.** Cumple el pedido —el sistema produce una pauta alimentaria personalizada— sin afirmar nada que no pueda sostener y sin necesitar la base de alimentos que quedó fuera de alcance. (a) es la única opción que reintroduce el riesgo que la especificación había descartado, y también la única sin forma de evaluarse.
**Consecuencia asumida.** El alumno no recibe qué comer, sino cuánta energía y cuánta proteína distribuir. Si el cliente considera que eso no cumple su pedido, hay que volver sobre la decisión antes de construir, no después.
**Estado (v2.2).** **Sin efecto en la Etapa 1.** RF-012 obtuvo 2 votos de 8 y RF-074 obtuvo 1; con ellos fuera cae toda la cadena nutricional —RF-075 y RF-108 incluidos— y esta decisión queda sin sujeto. Coincide con el primer paso del orden de recorte de D12. El texto se conserva porque la pregunta que resuelve —qué significa «generar la dieta»— volverá si vuelve la nutrición.

### DD-14 · Dos clases de componente inteligente

**Contexto.** El cliente definió la inteligencia como centro del producto; la redacción heredada de RF-057 prohibía que los componentes generativos produjeran valores o prescribieran cargas.
**Elegida.** Se distingue **componente de decisión** (produce valores y estructuras; validado y sujeto a revisión humana) de **componente narrativo** (sólo redacta sobre hechos calculados; no introduce ningún valor ausente de su entrada).
**Fundamento.** Prohibirle al sistema producir valores es incompatible con que decida. Mantener la prohibición sobre lo narrado conserva la única métrica de calidad barata, objetiva y contundente del proyecto: cero valores inventados en los textos.
**Consecuencia asumida.** El riesgo se traslada del texto a la prescripción, y se contiene con dos barreras: la validación automática de compatibilidad y de rangos, y la revisión del entrenador.

### DD-15 · Las estimaciones se calculan de forma diferida

**Elegida.** Diferida y periódica, más a demanda del administrador.
**Fundamento.** Elimina la latencia en la petición del usuario, la dependencia de un segundo servicio en el camino crítico y el versionado en tiempo de ejecución. Y hace verdadera la regla de continuidad: si el proceso nunca corre, la columna dice "no disponible" y nada se rompe.
**Consecuencia asumida.** La estimación tiene la antigüedad de la última ejecución, que por eso se muestra siempre junto al valor.

### DD-16 · Historial de objetivos y de condiciones con vigencia

**Fundamento.** Sin él no se puede determinar qué condiciones regían cuando se prescribió algo, y toda auditoría de una decisión pasada queda sin sustento.
**Consecuencia asumida.** Modelado temporal en dos entidades más, con su coste de consulta. Es el coste de poder explicar una decisión pasada.

### DD-17 · El alumno no ve su estimación de riesgo

**Fundamento.** Presentarle una probabilidad de abandono es contraproducente y no admite justificación defendible. Sí ve sus indicadores objetivos de adherencia y cumplimiento, que son accionables.
**Consecuencia asumida.** Una vista distinta según el rol sobre el mismo alumno.
**Estado (v2.2).** **Sin efecto.** Al retirarse RF-061 a RF-063 en [DD-34](#dd-34--la-ia-predictiva-se-reduce-a-dos-componentes-por-alumno) no hay estimación de riesgo que mostrar ni que ocultar. El alumno sigue viendo sus indicadores objetivos de adherencia y cumplimiento.

### DD-18 · Toda salida inteligente se registra con su versión y su contexto

**Fundamento.** Es lo que separa un componente evaluable de uno meramente demostrable, y lo que permite responder "¿por qué el sistema propuso esto?" seis semanas después.
**Consecuencia asumida.** Almacenamiento del contexto por cada resultado producido.

### DD-19 · La sustitución cuenta como cumplimiento

**Elegida.** Cuenta como cumplida, marcada como sustituida; el volumen se imputa al ejercicio ejecutado.
**Fundamento.** Si sustituir castiga la métrica, el alumno deja de declararlo y el registro se degrada — y con él el contexto del que depende toda la inteligencia del sistema.

### DD-20 · Los datos simulados se marcan y se excluyen de la analítica real

**Fundamento.** Un panel de retención que mezcla alumnos simulados con reales produce un número que no significa nada, y es indistinguible de uno correcto.

### DD-21 · No hay acceso no autenticado

**Elegida.** Eliminado el catálogo público.
**Fundamento.** Agrega un cuarto ámbito de permisos y una superficie pública a cambio de valor nulo para el ciclo central. Refuerza además DD-29: el sistema no es abierto.

### DD-22 · El administrador no accede al detalle individual sensible 👁

**Elegida.** Acceso de gestión y de agregación; sin sesiones, mediciones ni condiciones de un alumno concreto. Sí registra la aptitud, porque la constancia se presenta en el gimnasio y alguien tiene que cargarla, pero sólo su vigencia.
**Fundamento.** Minimización: su función no lo requiere.
**Consecuencia asumida.** Ante un problema con un alumno, el administrador depende del entrenador. Es correcto.

### DD-23 · El fin de la asignación revoca también el acceso al histórico

**Fundamento.** El fundamento del acceso es la relación vigente, no el mérito histórico.
**Consecuencia asumida.** El indicador de carga por entrenador del panel del gimnasio se calcula sobre datos agregados y no requiere visibilidad individual del entrenador.

### DD-24 · El correo es único por gimnasio, no globalmente

**Fundamento.** El sistema sirve a varios gimnasios y una persona puede ser alumna de dos.
**Consecuencia asumida.** La identificación en el ingreso debe resolver a qué gimnasio corresponde la cuenta. Es una consecuencia real y hay que diseñarla.

### DD-25 · El entrenador es la única puerta

**Contexto.** El cliente indicó que el entrenador debe revisar toda rutina antes de que llegue al alumno. Esto contradice RF-025 (autoasignación) y la rama de RF-091 que facultaba al alumno a aprobar en ausencia de entrenador.
**Opciones.** (a) Eliminar la autoasignación. (b) **Conservarla como solicitud que no rige hasta ser revisada.** (c) Mantener la excepción para alumnos sin entrenador.
**Elegida.** (b), y se deroga la rama de RF-091.
**Fundamento.** (b) conserva la utilidad de que el alumno elija, elimina la excepción y deja una sola puerta. (c) reintroduce exactamente el caso que se quiso evitar.
**Consecuencia asumida, y es seria.** Todo alumno debe tener un entrenador vigente. Un alumno sin entrenador no puede recibir ninguna rutina nueva ni ninguna adaptación, y el sistema depende de que el entrenador revise a tiempo. Se mitiga con RF-112 y con el indicador E1b de D1, pero **el sistema queda expuesto a la congestión humana**. Riesgo registrado en D12/R-09.

### DD-26 · El equipamiento es del gimnasio, no del alumno

**Contexto.** ¿Contra qué conjunto de equipamiento se valida una prescripción? `[F: cliente, 2026-08-18: "el foco está en el usuario, pero lo mantiene el gimnasio porque está asociado al mismo — depende de qué máquinas tiene el gimnasio"]`
**Opciones.** (a) Lo declara el alumno. (b) **Lo declara el gimnasio.** (c) Ambos, con intersección.
**Elegida.** (b). El inventario del gimnasio es la única fuente; el alumno no declara equipamiento.
**Fundamento.** Con (a), la falta de equipamiento sólo puede advertir —el alumno podría tener acceso circunstancial a algo que no declaró— y la validación se vuelve blanda: el generador puede proponer ejercicios imposibles. Con (b) la validación se vuelve dura: si la máquina no está en el gimnasio, el ejercicio no se puede hacer. (c) duplica el mantenimiento y reintroduce la ambigüedad de (a).
**Qué se gana.** El catálogo prescribible queda determinado por gimnasio; la incompatibilidad por equipamiento pasa de advertencia a impedimento (RN-47); la puesta en contexto del alumno pierde un paso; y el administrador adquiere una función con efecto real sobre la prescripción en lugar de un rol puramente administrativo.
**Qué se sacrifica.** Un alumno que además entrena en su casa no puede recibir una rutina que use su propio equipamiento.
**Consecuencia operativa que hay que asumir.** Si el administrador declara mal el inventario, todo el catálogo prescribible del gimnasio es incorrecto y ninguna rutina generada sirve. El inventario es un dato crítico, no una configuración cosmética. Riesgo en D12/R-15.

### DD-27 · Objetivo y tipo de rutina comparten enumeración

**Contexto.** RF-083 exige verificar la correspondencia entre el tipo de la rutina y el objetivo del alumno, y las dos enumeraciones heredadas no coincidían.
**Elegida.** Una única enumeración de cuatro valores para ambos, con `ACONDICIONAMIENTO_GENERAL` compatible con cualquier objetivo.
**Fundamento.** Convierte la verificación de RF-083 en una comparación en lugar de un juicio, y la vuelve verificable sin ambigüedad.
**Consecuencia asumida.** `READAPTACION` queda fuera: no tiene objetivo de alumno equivalente y arrastra implicancias clínicas que el sistema declara fuera de alcance. Si el cliente lo requiere, hay que reabrir esta decisión y también el no-alcance de salud clínica de D1/§6.

### DD-28 · Un entrenador que entrena necesita otro entrenador

**Contexto.** DD-08 admite que un usuario tenga los roles de alumno y entrenador. Pero RN-22 impide autoasignarse y DD-25 exige un entrenador vigente para que una rutina rija. Combinadas, dejaban al entrenador sin poder entrenar, mientras D3 afirmaba lo contrario.
**Opciones.** (a) Permitir que se apruebe a sí mismo. (b) Permitir que el administrador apruebe en ese caso. (c) **Exigir que otro entrenador lo tome como alumno.**
**Elegida.** (c).
**Fundamento.** (a) abre un agujero en la única regla que el cliente declaró indelegable. (b) convierte al administrador en aprobador de prescripciones, para lo cual no tiene ni competencia ni acceso a la información clínica (DD-22).
**Consecuencia asumida, y hay que decirla.** En un gimnasio con un solo entrenador, ese entrenador no puede tener rutina vigente. El sistema lo señala al administrador como situación a resolver incorporando otro entrenador. Es una limitación real, no un descuido.

### DD-29 · El alta es por invitación

**Contexto.** `[F: cliente, 2026-08-18: "el sistema no es abierto para cualquier usuario; un gimnasio tiene que estar afiliado y avisarle al usuario para que se registre"]`
**Elegida.** La invitación nominal es la única vía de alta. La emite un administrador para cualquier rol, o un entrenador sólo con rol alumno, y determina el gimnasio y los roles del usuario resultante.
**Fundamento.** Resuelve de una sola vez cuatro problemas que estaban abiertos: cómo queda vinculado un usuario a un gimnasio, quién decide sus roles, cómo se impide el crecimiento espontáneo de usuarios, y quién responde por cada incorporación.
**Consecuencia asumida.** No hay adquisición espontánea de usuarios, que es exactamente lo que el modelo de negocio pide. Y el primer administrador de cada gimnasio no puede crearse por esta vía: ver DD-30.

### DD-30 · El aprovisionamiento está fuera de la aplicación

**Contexto.** Si el alta es por invitación, nadie dentro de un gimnasio nuevo puede emitir la primera.
**Opciones.** (a) Un rol superadministrador multi-gimnasio dentro de la aplicación. (b) **Una operación de aprovisionamiento del proveedor, externa a la aplicación.** (c) Autorregistro del primer administrador.
**Elegida.** (b), atómica: o quedan creados el gimnasio y su primer administrador, o no queda nada.
**Fundamento.** (a) reintroduce el superadministrador multi-gimnasio, que está fuera de alcance y arrastra un cuarto ámbito de permisos. (c) contradice DD-29.
**Consecuencia asumida.** El sistema tiene una operación que no es accesible desde ninguna pantalla y que hay que ejecutar y documentar aparte. Es el precio de que el modelo de alta sea cerrado y coherente.

### DD-31 · La generación y las reglas tienen autoridades distintas

**Contexto.** El alcance generativo v2.1 asigna al LLM la interpretación, el tipo y la construcción completa de la rutina. A la vez, compatibilidad, estructura y adaptación necesitan criterios verificables que impidan publicar una salida insegura o imposible.
**Elegida.** El LLM interpreta el pedido, selecciona el tipo y construye el candidato inicial. RN-39a y RN-44a a RN-44d no generan esa rutina: son barreras determinísticas y auditables que toda salida debe superar. El diagnóstico RN-79a y los ajustes RN-89a permanecen determinísticos. Los componentes aprendidos actúan en alternativas, riesgo y segmentación.
**Fundamento.** Esta división cumple el alcance sin transferir autoridad de seguridad al modelo. El candidato puede variar; catálogo, compatibilidad, rangos y puerta del entrenador no.
**Consecuencia asumida.** Una salida inválida se descarta y admite un reintento; después la generación queda no disponible. No existe construcción determinística alternativa. Las plantillas privadas y la creación manual por entrenadores siguen disponibles; **los presets son alcance opcional y no son la contingencia** ([DD-35](#dd-35--la-plantilla-del-entrenador-es-el-piso-de-disponibilidad-de-la-prescripción)). Ver ADR 0010, D12/R-08 y D13/N-15.

### DD-32 · Existe una vía de corrección tardía, nominal y auditada

**Contexto.** El plazo de corrección de 48 h dejaba sin remedio un error detectado después, y un valor equivocado contamina de forma permanente la carga máxima estimada, el diagnóstico y toda la cadena de adaptación.
**Opciones.** (a) Ninguna corrección tardía. (b) **Desbloqueo por el entrenador, una sola vez por sesión, con motivo auditado.** (c) Corrección libre sin plazo.
**Elegida.** (b), complementada con el recálculo del récord sobre el histórico completo (RN-71) y con la confirmación de valores atípicos en el momento del registro (RN-55a).
**Fundamento.** (a) preserva la estabilidad de los indicadores a costa de conservar datos que se sabe que son falsos. (c) elimina la estabilidad de los indicadores. La excepción nominal y auditada conserva ambas cosas.
**Consecuencia asumida.** El plazo de 48 h deja de ser absoluto. El límite de un desbloqueo por sesión es lo que impide que la excepción se convierta en la norma.

### DD-33 · El candidato se moldea; la propuesta, no

**Contexto.** El corpus dejaba que la rutina generada naciera PROPUESTA y le llegara al entrenador tal como salió del componente. El alumno que la había solicitado no tenía modo de intervenir sobre ella salvo pedir otra entera —consumiendo una rutina DESCARTADA y un aviso por RN-36a— o comentarla. Si el alumno no puede moldear lo que pidió, que la solicite él o que se la genere el sistema por su cuenta son la misma funcionalidad.
**Opciones.** (a) La rutina generada nace PROPUESTA, sin intervención del solicitante. (b) El alumno edita libremente su rutina propuesta. (c) **La generación produce un candidato ajustable, que sólo al confirmarse se convierte en rutina PROPUESTA.**
**Elegida.** (c), con las operaciones del alumno acotadas por D5/§5.2, revalidación en el acto (RN-126) y un tope de tres regeneraciones (RN-127).
**Fundamento.** (a) convierte la solicitud del alumno en un trámite y desaprovecha la ocasión más barata de acercar el plan a lo que la persona efectivamente va a hacer; además empuja toda inconformidad a la única salida disponible, que es pedir otra rutina entera. (b) contradice la matriz de D3 y, sobre todo, borra la frontera entre lo que el alumno elige y lo que el entrenador prescribe: series, repeticiones, descansos y cargas son prescripción. (c) conserva las dos cosas: el alumno decide **qué ejercicios** hace, el entrenador decide **cómo se hacen**, y la puerta de RN-35 sigue intacta porque nada rige sin revisión.
**Consecuencia asumida.** Aparece un objeto que no está en el ciclo de vida de D6 —el candidato— que no se persiste como rutina y muere si no se confirma; se declara explícitamente en D6/§1 para que nadie lo resuelva agregando un estado BORRADOR. Y el entrenador debe recibir en la revisión la diferencia entre lo que el componente produjo y lo que el alumno confirmó (RN-129, RF-120): sin eso revisaría como `GENERADA` una rutina que en realidad armó el alumno.
**Estado (v2.2).** **Derogada para la Etapa 1.** Al quedar fuera de alcance la solicitud de rutina por el alumno (RF-025, 3 votos de 8), desaparece el solicitante que esta decisión habilitaba a moldear el candidato. Su propio fundamento lo anticipa: si el alumno no puede moldear lo que pidió, que la solicite él o que se la genere el sistema son la misma funcionalidad — y en la Etapa 1 es lo segundo. RF-119, RF-120 y RN-124 a RN-129 quedan diferidos con ella. El texto se conserva íntegro: si el alcance se reabre, esta decisión vuelve tal como está.
**Estado (v3.6).** RF-025 se reincorpora por decisión posterior del Product Owner, pero DD-33 no se reactiva: el alumno solicita para sí y no moldea un candidato. Una salida válida se materializa directamente como rutina `PROPUESTA` y el entrenador asignado conserva la aprobación obligatoria. RF-119, RF-120 y RN-124 a RN-129 siguen diferidos.

### DD-34 · La IA predictiva se reduce a dos componentes por alumno

**Contexto.** Replanteo de alcance de IA del 2026-08-28. `predictive-ai.md` describía cinco componentes aprendidos: alternativas de sustitución (RF-059, RF-060), riesgo de abandono (RF-061 a RF-063), segmentación de perfiles (RF-064), sugerencia de carga (RF-121) y proyección de trayectoria (RF-122). Construir y mantener cinco modelos clásicos —con sus features, entrenamiento, evaluación y despliegue batch— excede la capacidad del proyecto, y tres de ellos resuelven problemas que la capa generativa ya instalada cubre a costo marginal.

**Opciones.** (a) Conservar los cinco componentes aprendidos. (b) **Reducir a los dos que la capa generativa no puede cubrir, reubicar dos en ella y retirar uno del alcance.** (c) Retirar toda la IA predictiva y dejar sólo la generativa.

**Elegida.** (b), con este reparto:

| Componente                                   | Antes | Ahora                                                                                                                                                                                                                                    |
| -------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-059, RF-060 · alternativas de sustitución | ML    | **AI.** El orden lo produce la capa generativa sobre el subconjunto del catálogo ya prefiltrado de forma determinista por patrón, compatibilidad y equipamiento, con revalidación determinista posterior (RF-113). Siguen MUST            |
| RF-064 · segmentación de perfiles            | ML    | **AI.** Descripción del perfil de comportamiento redactada por la capa generativa a partir de los indicadores ya calculados, **sin clustering y sin persistirse**. Sigue SHOULD                                                           |
| RF-061 a RF-063 · riesgo de abandono         | ML    | **WON'T.** Se retiran del alcance por costo y esfuerzo frente al valor esperado con los datos disponibles (S-03). **No se degradan a una regla simple: se retiran**                                                                       |
| RF-121 · sugerencia de carga                 | ML    | Se conserva como componente aprendido. SHOULD                                                                                                                                                                                            |
| RF-122 · proyección de trayectoria           | ML    | Se conserva como componente aprendido. Sube de COULD a SHOULD                                                                                                                                                                             |

**Fundamento.** (a) mantiene cinco líneas de aprendizaje automático en un proyecto cuya capacidad ya está por debajo del alcance, y dos de ellas producen salidas que un modelo de lenguaje ya instalado genera con calidad suficiente sobre entradas que el sistema calcula de todos modos. (c) elimina la única dimensión de aprendizaje automático genuino y deja sin sujeto a RF-073 y RNF-26. (b) conserva esa dimensión donde tiene sustento —dos componentes por alumno, sobre series temporales que el sistema efectivamente captura— y libera la capacidad que consumían los otros tres.

El riesgo de abandono se retira **y no se sustituye por una regla**, porque una regla simple sobre inasistencia no es una estimación de riesgo: es un umbral de inasistencia, y presentarlo como lo primero sería peor que no tenerlo.

**Consecuencias asumidas.**

- **Se pierde la reproducibilidad exacta del orden de alternativas.** RF-059 pasa al estándar de «validez repetida» del resto de la capa generativa. RF-072 y RNF-27 se cumplen **persistiendo la lista producida**, no reejecutándola.
- **Se amplía la superficie de dependencia del servidor de modelos.** FL-06 —sustitución durante una sesión en curso, sin lenguaje natural de por medio— pasa a invocar el modelo, con el orden determinista de RN-49a como alternativa cuando no responde (RN-99). Es una dependencia que antes no existía y hay que medirla.
- **Se derogan `ScoreRiesgo` y `SegmentoPerfil`** en D4. `EvaluacionComponente` se conserva para RF-121 y RF-122.
- **FL-16 queda derogado** y RF-107 pierde «riesgo de abandono alto» de su orden de urgencia.
- **DD-17 queda sin efecto**: no hay estimación de riesgo que ocultarle al alumno.
- **La parte de [ADR-0008](adr/0008-tool-calling-for-ml-components.md) referida al ranking de RF-059 queda reemplazada**; el resto de esa ADR sigue vigente.
- **Degradar RF-061 a RF-063 desde MUST exige acuerdo explícito del cliente** (D12/§4). Esta decisión lo propone; no lo sustituye. La votación posterior lo respalda: obtuvieron 1, 0 y 0 votos de 8.

### DD-35 · La plantilla del entrenador es el piso de disponibilidad de la prescripción

**Contexto.** El equipo resolvió no construir presets —«No usaremos preset, todo será generado desde cero con una batería de prompts», respuesta a D4 del Acta de Redefinición— y la votación lo confirma: RF-021 obtuvo 1 voto de 8. Pero RF-058, RN-95b y la ADR del servicio generativo apoyaban **toda** la continuidad ante indisponibilidad en «conservar la solicitud de presets publicados del gimnasio como vía disponible». Retirado el preset, esa garantía quedó sin referente y la creación de rutinas pasó a depender por completo de un servicio que corre en infraestructura de terceros.

**Opciones.** (a) Dejarlo como está y aceptar que sin servicio generativo no hay ninguna vía de prescripción. (b) **Designar la plantilla del entrenador (RF-019) como vía manual y piso de disponibilidad.** (c) Reintroducir los presets contra la decisión del equipo y la votación. (d) Construir un generador determinístico de rutinas como alternativa.

**Elegida.** (b). En este corpus un preset **era** una plantilla publicada: RF-021 agregaba la publicación y la reutilización entre entrenadores, no la capacidad de construir la rutina. Esa capacidad vive en RF-019, que obtuvo 8 votos de 8. Lo que se pierde al retirar RF-021 es compartirlas; lo que se conserva es poder crearlas y asignarlas.

**Fundamento.** (a) deja al producto sin ninguna forma de cumplir su propia capacidad C1 cuando falla un servicio externo. (c) contradice una decisión explícita del equipo y una votación inequívoca. (d) es exactamente el fallback determinístico que [ADR 0010](adr/0010-servicio-ia-en-vercel-y-llm-en-el-polo.md) descarta de forma deliberada, y reconstruirlo duplicaría la lógica de prescripción en dos implementaciones que divergirían.

**Consecuencia asumida, y hay que decirla con todas las letras.** RF-019 deja de ser una comodidad del entrenador y pasa a ser un requisito de disponibilidad: **si un gimnasio no tiene ninguna plantilla cargada y el servicio generativo no responde, un alumno nuevo no obtiene ninguna rutina.** No hay mitigación técnica para ese caso dentro del alcance recortado; la mitigación es operativa —cargar plantillas de arranque al aprovisionar el gimnasio— y hay que ejecutarla, no suponerla. Ver [D12/R-17](../planning/risks-and-assumptions.md) y la decisión PD-03 del [baseline de alcance](../planning/baseline-alcance-2026-09.md).
