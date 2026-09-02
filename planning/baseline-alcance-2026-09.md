# Baseline de alcance — Vivaz Adaptive · Etapa 1

|                          |                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Versión**              | 4.0                                                                                                                                  |
| **Fecha**                | 2026-09-01                                                                                                                           |
| **Estado**               | Propuesta de baseline. Requiere validación del equipo y conversación de alcance con el cliente (§P/PD-01)                            |
| **Reemplaza**            | La clasificación de alcance de [D8](../requirements/functional-requirements.md) v3.3 y el plan de sprints del Acta de Redefinición §5 |
| **Autoritativo para**    | Alcance de la etapa, trazabilidad de la votación, orden de construcción y deuda documental                                            |
| **No autoritativo para** | El enunciado de los requisitos (sigue siendo D8), las reglas (D5), el modelo (D4) ni los estados (D6)                                 |

**Fuentes.** `Documento_Planificacion_Inicio_Proyecto.docx` (baseline documental, 81 RF) · `Acta Redefinicion.docx` (redefinición del núcleo por el cliente, con las cuatro respuestas del equipo ya registradas) · `Lista de Requisitos.xlsx` (votación de 8 de 9 integrantes sobre RF-001..RF-081, más RF-082..RF-094 agregados sin votar) · el corpus documental completo · los tres repositorios de código.

---

## A. Resumen ejecutivo

**Vivaz Adaptive es un sistema que mantiene la prescripción de entrenamiento de cada alumno adecuada a su estado, y que somete cada cambio a la aprobación de un entrenador.** No es un registrador de entrenamientos con analítica encima: el registro, los indicadores y los tableros existen porque sin ellos no hay diagnóstico, y sin diagnóstico no hay adaptación fundamentada.

Tres hechos gobiernan esta versión del baseline:

1. **El cliente declaró la adaptación como condición de aprobación.** «Si no está, el proyecto no se aprueba». Todo lo demás es negociable; esto no.
2. **La votación del equipo redujo el alcance, pero menos de lo que parece.** De 97 requisitos en alcance en D8 v3.3 se pasa a **80 en la Etapa 1**: 19 diferidos, 6 absorbidos por fusión y 4 degradados a regla. La votación no contradijo el núcleo — recortó la periferia (nutrición, comentarios, paneles agregados, riesgo de abandono, parametrización) y confirmó por unanimidad práctica el ciclo central. Lo que recortó cuesta poco; lo que confirmó cuesta casi todo.
3. **Nada del dominio está implementado.** Los tres repositorios contienen andamiaje: Express con `/health` y `/ready`, un `schema.prisma` sin modelos, una SPA con una pantalla de bienvenida y un paquete Python vacío. Toda la funcionalidad de este documento es diseño, no software.

**El alcance sigue por encima de la capacidad.** 80 requisitos, de los cuales 57 son núcleo, contra ~504 h de capacidad de construcción. La banda N1 sola consume entre el 90 % y el 140 % del presupuesto; el conjunto completo, entre el 130 % y el 190 % (§D.4). La aritmética de [D12/§3](risks-and-assumptions.md) no cierra ni siquiera con este recorte. Este documento entrega la decisión ya preparada: tres bandas de alcance y un orden de retirada escrito de antemano, para que el recorte sea una decisión y no un accidente de la semana 12.

**Y el denominador de esa cuenta está en duda.** Las ~504 h suponen que tres de las nueve personas no construyen software; el Documento de Planificación afirma lo contrario con todas las letras. Resolver esa contradicción cambia la conversación de alcance antes de tenerla (§M/I-09).

---

## B. Nuevo alcance funcional, en prosa

Un gimnasio se afilia mediante una operación externa a la aplicación que crea el gimnasio y su primer administrador. Ese administrador declara **qué equipamiento tiene el gimnasio** —dato crítico, no cosmético: determina qué puede prescribirse a todo el mundo— e invita nominalmente a entrenadores y alumnos. Nadie se registra por su cuenta.

Un alumno que acepta su invitación declara su perfil, su objetivo y sus condiciones físicas mediante un formulario tabulado de categorías cerradas, cada una con zona corporal y severidad. Puede cargar su aptitud deportiva; el sistema advierte si falta o venció, pero no bloquea. Registra mediciones corporales fechadas.

Con ese contexto —y sin ningún historial— **el sistema genera su rutina completa**: elige el tipo de rutina compatible con su objetivo, la construye sobre el catálogo prescribible de su gimnasio (los ejercicios cuyo equipamiento está efectivamente en el inventario), y verifica que ningún ejercicio esté contraindicado por una condición vigente. La rutina nace **propuesta**, no vigente. Un entrenador con asignación vigente la revisa y la aprueba. Sin esa aprobación no rige. Sin excepciones, cualquiera sea el origen de la rutina.

El alumno entrena. Al iniciar una sesión, el sistema **congela la prescripción del día dentro de la propia sesión**: lo que se indicó y lo que se hizo conviven en la misma fila, y la sesión de hoy no cambia porque la rutina cambie mañana. Registra carga, repeticiones y, si quiere, esfuerzo percibido. Puede sustituir un ejercicio, agregar u omitir series. Reanuda una sesión interrumpida; si no vuelve, se cierra sola.

De ese registro el sistema deriva volumen y frecuencia por grupo muscular, capacidad máxima estimada por ejercicio, adherencia sobre ventana móvil, cumplimiento de series y de repeticiones, y récords personales. Con eso detecta estancamiento, caída de adherencia y desbalance.

**Cada dos semanas el sistema evalúa la rutina vigente** y asigna a cada ejercicio y al conjunto una de cinco situaciones. Si corresponde, elabora una **propuesta de adaptación**: ajuste de carga, de volumen, de esquema, sustitución de un ejercicio o cambio de estructura. Cada ajuste lleva el criterio que lo motiva y el dato que lo sustenta. La propuesta se verifica contra las condiciones del alumno y los rangos de su tipo de rutina antes de presentarse, y **el entrenador la acepta entera, la acepta en parte o la rechaza**. Aceptarla genera una versión nueva de la rutina; las anteriores se conservan y las sesiones ya ejecutadas no se tocan.

Un cambio de objetivo, la aparición o el cierre de una condición física, el vencimiento de la aptitud o **un cambio del inventario del gimnasio** disparan la reevaluación inmediata: el sistema marca los ejercicios que dejaron de ser compatibles sin retirarlos, avisa, y elabora la propuesta correspondiente.

El entrenador ve su cartera ordenada por urgencia —primero lo que espera su revisión, después incompatibilidades, estancamiento y caída de adherencia— y la ficha consolidada de cada alumno. El alumno ve su panel de progreso, su evolución por ejercicio y sus mediciones, y toda vista **declara qué información le falta en lugar de mostrar un cero**.

### Lo que este alcance deliberadamente ya no incluye

Ninguna forma de nutrición. Ningún comentario ni mensajería. Ningún panel analítico del gimnasio. Ninguna estimación de riesgo de abandono. Ningún preset publicado ni catálogo de preajustes. Ninguna solicitud de rutina iniciada por el alumno. Ninguna representación muscular sobre esquema corporal —el mismo dato se presenta como barras por grupo muscular—. Ningún registro diferido de sesiones pasadas. Ninguna parametrización de reglas de cálculo. Ninguna baja de cuenta con portabilidad y anonimización (§P/PD-02).

---

## C. Capacidades del producto

Ocho áreas de capacidad estructuran el sistema. La columna «D1» las mapea contra las capacidades centrales ya declaradas en [D1/§3](../product/vision-and-objectives.md), que no cambian.

| #     | Área de capacidad            | Qué garantiza                                                                                                                                                          | D1     |
| ----- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| CAP-1 | **Ámbito y acceso**          | Un gimnasio existe, sus usuarios entran sólo por invitación, y cada operación se autoriza por rol *y* por relación con el recurso concreto                              | —      |
| CAP-2 | **Contexto del alumno**      | El sistema sabe quién es la persona, qué se propone y qué no puede hacer — la entrada de todo componente de decisión                                                    | C2     |
| CAP-3 | **Catálogo prescribible**    | El conjunto de ejercicios efectivamente ejecutables en *este* gimnasio, clasificados de forma que la compatibilidad sea calculable                                      | C2     |
| CAP-4 | **Prescripción**             | Una rutina existe, tiene tipo, es coherente con el objetivo, es compatible con la persona, y evoluciona por versiones sin destruir el pasado                            | C1, C2 |
| CAP-5 | **Ejecución registrada**     | Lo prescripto y lo ejecutado conviven en la misma sesión, y la sesión es inmune a los cambios posteriores de la rutina                                                  | —      |
| CAP-6 | **Evidencia**                | El registro plano se convierte en indicadores y señales verificables, y toda vista declara lo que le falta                                                              | C3     |
| CAP-7 | **Adaptación fundamentada**  | La evolución se diagnostica sola y produce una propuesta acotada, justificada y compatible                                                                              | C3, C4 |
| CAP-8 | **La puerta del entrenador** | Ninguna rutina rige ni cambia sin aprobación humana, y el entrenador sabe a quién atender primero                                                                       | C5     |

**Cómo se relacionan.** CAP-1 habilita todo. CAP-2 y CAP-3 son las dos entradas de CAP-4: sin contexto no hay a quién prescribir, sin catálogo prescribible no hay con qué. CAP-5 produce el sustrato de CAP-6, y CAP-6 el de CAP-7. CAP-8 es la salida obligatoria de CAP-4 y de CAP-7 — es el único punto por el que un cambio llega al alumno.

**Dependencia crítica no obvia.** CAP-4 depende de la disponibilidad del servicio generativo con una fuerza que el corpus actual no declara. Ver §F.4 y §G/DEP-04.

---

## D. Regla de corte aplicada y alcance resultante

### D.1 La regla y sus tres excepciones

La regla base es: **≥ 5 votos = candidato al alcance de la Etapa 1**. Votaron 8 de 9 integrantes (Vioti no registró votos), de modo que 5 es mayoría estricta de quienes votaron y 8 es unanimidad.

Tres conjuntos entran sin votación, y hay que decir por qué:

- **RF-082 a RF-094** se agregaron a la planilla *después* de la reunión con el cliente y nunca se votaron. Entran por **autoridad del cliente**, no por voto: son la funcionalidad que el cliente declaró condición de aprobación. Someterlos a votación habría sido un error de proceso.
- **RF-095 a RF-122** no existían cuando se votó: los produjo el análisis posterior del corpus. Entran únicamente si son **dependencia técnica necesaria** de algo aprobado, y cada uno se justifica individualmente en §G. Los que no lo son, salen.
- **Requisitos con menos de 5 votos que son dependencia necesaria** de uno aprobado. No se reincorporan como funcionalidad independiente: se absorben, se subordinan o se declaran dependencia.

### D.2 Resultado

| Categoría                                                          | Cantidad |
| ------------------------------------------------------------------ | -------- |
| Aprobados por votación (≥ 5), sobrevivientes tras las fusiones      | 40       |
| Incorporados por autoridad del cliente (RF-082..094)               | 13       |
| Dependencias necesarias reincorporadas o derivadas                 | 26       |
| Conservados por compromiso ante el Product Owner (RF-053)          | 1        |
| **En alcance — Etapa 1**                                           | **80**   |
| Absorbidos por fusión (RF-004, RF-023, RF-032, RF-033, RF-060, RF-107) | 6    |
| Fuera de esta etapa (diferidos)                                    | 19       |
| Fuera de alcance (firme)                                           | 14       |
| Degradados a regla, criterio o restricción                         | 4        |

> **Corrección de la primera emisión.** La versión inicial de este documento declaró 68 requisitos en alcance. Era un error de recuento: se contaron las 18 entradas `DEP-xx` de §G como si fueran 18 identificadores, cuando seis de ellas agrupan dos o tres (`DEP-04` = RF-058 + RF-113, `DEP-06` = RF-005 + RF-069, `DEP-09` = RF-071 + RF-106, `DEP-11` = RF-114 + RF-118, `DEP-12` = RF-115 + RF-116 + RF-100, `DEP-15` = RF-112 + RF-109). Las tablas de §D.3 siempre enumeraron el conjunto correcto. **El recorte real es 97 → 80, no 97 → 68**, y el contraste con la capacidad es peor de lo que se declaró. Ver §D.4.

### D.3 Alcance de la Etapa 1, por área de capacidad

Los identificadores son los de [D8](../requirements/functional-requirements.md) y **no se renumeran**: 122 identificadores están referenciados de forma cruzada en veinte documentos del corpus y en los `AGENTS.md` de los tres repositorios de código. Renumerarlos destruiría trazabilidad existente a cambio de nada. La normalización se hace por **absorción declarada** (§E) y por reorganización en capacidades, no por renumeración.

Banda: **N1** núcleo, no se recorta · **N2** comprometido · **N3** condicionado al hito del Sprint 3.

#### CAP-1 · Ámbito y acceso

| RF     | Requisito                                              | Votos | Origen        | Banda |
| ------ | ------------------------------------------------------ | ----- | ------------- | ----- |
| RF-115 | Aprovisionamiento del gimnasio, externo a la aplicación | —     | Dependencia   | N1    |
| RF-116 | Alta exclusivamente por invitación                     | —     | Cliente N-26  | N1    |
| RF-001 | Completar la cuenta desde una invitación               | 8     | Votación      | N1    |
| RF-002 | Autenticación y gestión de sesión                      | 8     | Votación      | N1    |
| RF-003 | Recuperación y cambio de credenciales                  | 8     | Votación      | N2    |
| RF-005 | Autorización por rol **y** por relación con el recurso | 2     | Dependencia   | N1    |
| RF-069 | Ámbito de la información por gimnasio                  | 4     | Dependencia   | N1    |
| RF-065 | Gestión de cuentas, roles e invitaciones               | 8 ⊕ 6 | Votación (F5) | N1    |
| RF-066 | Asignación entrenador–alumno con historial             | 2     | Dependencia   | N1    |
| RF-112 | Señalar alumnos sin entrenador y bloquear lo pendiente | —     | Dependencia   | N2    |
| RF-109 | Transferir lo pendiente al entrenador entrante         | —     | Dependencia   | N2    |
| RF-067 | Estado de membresía, informativo                       | 8     | Votación      | N3    |

#### CAP-2 · Contexto del alumno

| RF     | Requisito                                         | Votos | Origen      | Banda |
| ------ | ------------------------------------------------- | ----- | ----------- | ----- |
| RF-007 | Perfil del alumno                                 | 8     | Votación    | N1    |
| RF-008 | Objetivo vigente con historial de vigencia        | 8     | Votación    | N1    |
| RF-009 | Condiciones físicas con zona corporal y severidad | 8     | Votación    | N1    |
| RF-085 | Historial de vigencia de las condiciones          | —     | Cliente     | N1    |
| RF-084 | Aptitud con vencimiento; advierte, no bloquea     | —     | Cliente     | N2    |
| RF-010 | Mediciones corporales fechadas                    | 8     | Votación    | N1    |
| RF-111 | Determinar y exponer si hay contexto suficiente   | —     | Dependencia | N2    |
| RF-096 | Consentimiento explícito para datos de salud      | —     | Dependencia | N2    |

#### CAP-3 · Catálogo prescribible

| RF     | Requisito                                                       | Votos | Origen       | Banda |
| ------ | --------------------------------------------------------------- | ----- | ------------ | ----- |
| RF-013 | Catálogo de ejercicios consultable                              | 8     | Votación     | N1    |
| RF-014 | Búsqueda y filtrado                                             | 8     | Votación     | N2    |
| RF-015 | Información descriptiva y recurso visual                        | 8     | Votación     | N2    |
| RF-016 | Clasificación muscular primaria/secundaria y articulaciones     | 8     | Votación     | N1    |
| RF-099 | Taxonomía canónica cerrada y curación manual de los frecuentes  | —     | Dependencia  | N1    |
| RF-070 | Carga inicial repetible desde fuente externa                    | 8     | Votación     | N1    |
| RF-114 | Inventario de equipamiento del gimnasio                         | —     | Cliente N-27 | N1    |
| RF-118 | Catálogo prescribible = catálogo ∩ inventario                   | —     | Dependencia  | N1    |
| RF-100 | Catálogo base global frente al catálogo propio del gimnasio     | —     | Dependencia  | N2    |
| RF-017 | Incorporación de ejercicios por entrenadores                    | 5     | Votación     | N3    |

#### CAP-4 · Prescripción

| RF     | Requisito                                                              | Votos | Origen       | Banda |
| ------ | ---------------------------------------------------------------------- | ----- | ------------ | ----- |
| RF-019 | Plantillas estructuradas en días y ejercicios                          | 8     | Votación     | N1    |
| RF-020 | Prescripción de series, rangos, carga sugerida y descanso              | 6     | Votación     | N1    |
| RF-022 | Copia profunda e independiente al asignar                              | 0     | Dependencia  | N1    |
| RF-024 | Frecuencia semanal objetivo dentro del rango del tipo                  | 2     | Dependencia  | N1    |
| RF-026 | Una vigente y una propuesta como máximo; archivado consultable         | 6     | Votación     | N1    |
| RF-082 | Tipo de rutina y derivación de estructura, esquemas y rangos           | —     | Cliente N1   | N1    |
| RF-083 | Correspondencia entre tipo de rutina y objetivo                        | —     | Cliente      | N1    |
| RF-086 | Verificación de compatibilidad, con regla explícita de correspondencia | —     | Cliente N4   | N1    |
| RF-087 | Generación de la rutina inicial sin historial previo                   | —     | Cliente N6   | N1    |
| RF-092 | Versionado de la rutina adaptada                                       | —     | Cliente      | N1    |
| RF-110 | Revisión y aprobación explícita antes de toda vigencia                 | —     | Cliente N-14 | N1    |

#### CAP-5 · Ejecución registrada

| RF     | Requisito                                                          | Votos     | Origen        | Banda |
| ------ | ------------------------------------------------------------------ | --------- | ------------- | ----- |
| RF-027 | **Ciclo de vida de la sesión**: inicio, curso, reanudación y cierre | 8 ⊕ 3 ⊕ 7 | Votación (F1) | N1    |
| RF-028 | Congelamiento de la prescripción dentro de la sesión               | 5         | Votación      | N1    |
| RF-029 | Registro por serie de lo prescripto y lo ejecutado                 | 8         | Votación      | N1    |
| RF-030 | Precarga con la última ejecución del alumno                        | 1         | Dependencia   | N1    |
| RF-031 | Agregar, omitir y sustituir durante la sesión                      | 6         | Votación      | N2    |
| RF-035 | Historial de sesiones con comparación prescripto/ejecutado         | 8         | Votación      | N1    |

#### CAP-6 · Evidencia

| RF     | Requisito                                               | Votos | Origen      | Banda |
| ------ | ------------------------------------------------------- | ----- | ----------- | ----- |
| RF-040 | Volumen y frecuencia por grupo muscular                 | 8     | Votación    | N1    |
| RF-041 | Capacidad máxima estimada por ejercicio                 | 8     | Votación    | N1    |
| RF-042 | Adherencia sobre ventana móvil de cuatro semanas        | 5     | Votación    | N1    |
| RF-043 | Cumplimiento de series y de repeticiones                | 0     | Dependencia | N1    |
| RF-046 | Señales: estancamiento, caída de adherencia, desbalance | 7     | Votación    | N1    |
| RF-044 | Récords personales                                      | 6     | Votación    | N2    |
| RF-045 | Evolución de mediciones con media móvil                 | 8     | Votación    | N2    |
| RF-048 | Panel de progreso del alumno                            | 8     | Votación    | N2    |
| RF-050 | Evolución por ejercicio                                 | 8     | Votación    | N2    |
| RF-051 | Comportamiento explícito ante información insuficiente  | 7     | Votación    | N1    |
| RF-052 | Indicadores agregados de la cartera                     | 8     | Votación    | N3    |
| RF-064 | Descripción del perfil de comportamiento, efímera       | 6     | Votación    | N3    |

#### CAP-7 · Adaptación fundamentada

| RF     | Requisito                                                            | Votos | Origen        | Banda |
| ------ | -------------------------------------------------------------------- | ----- | ------------- | ----- |
| RF-088 | Diagnóstico periódico con cinco situaciones y precedencia definida    | —     | Cliente N7    | N1    |
| RF-089 | Propuesta de adaptación por tabla explícita situación → ajuste        | —     | Cliente N8    | N1    |
| RF-090 | Criterio y datos que sustentan cada ajuste                           | —     | Cliente N8    | N1    |
| RF-091 | Aprobación total, parcial o rechazo por el entrenador                | —     | Cliente N9    | N1    |
| RF-094 | Reevaluación por cambio de objetivo, condición, aptitud o inventario | —     | Cliente N13   | N1    |
| RF-059 | Alternativas admisibles de sustitución, con exclusión dura           | 8 ⊕ 2 | Votación (F3) | N1    |
| RF-093 | Historial de adaptaciones aplicadas                                  | —     | Cliente N10   | N2    |

#### CAP-8 · La puerta del entrenador y la generación

| RF     | Requisito                                                        | Votos | Origen        | Banda |
| ------ | ---------------------------------------------------------------- | ----- | ------------- | ----- |
| RF-036 | Cartera priorizada, con criterio de urgencia único y ordenado    | 5 ⊕ — | Votación (F4) | N1    |
| RF-037 | Ficha consolidada del alumno                                     | 8     | Votación      | N1    |
| RF-038 | Intervención del entrenador sobre la rutina, con autoría y aviso | 7 ⊕ 1 | Votación (F2) | N1    |
| RF-054 | Generación asíncrona del candidato de rutina                     | 8     | Votación      | N1    |
| RF-055 | Explicación en lenguaje natural de los criterios aplicados       | 8     | Votación      | N1    |
| RF-057 | Restricciones sobre el contenido generado                        | 0     | Dependencia   | N1    |
| RF-058 | Continuidad ante indisponibilidad de la generación               | 1     | Dependencia   | N1    |
| RF-113 | Descarte de salida inválida, un reintento, luego no disponible   | —     | Dependencia   | N1    |
| RF-053 | Interpretación de lenguaje natural a parámetros estructurados    | 3     | **Compromiso PO** | N2 |
| RF-095 | Avisos dentro de la aplicación, con enumeración cerrada          | —     | Dependencia   | N2    |

#### Transversales de datos

| RF     | Requisito                                                    | Votos | Origen                     | Banda |
| ------ | ------------------------------------------------------------ | ----- | -------------------------- | ----- |
| RF-071 | Generación e identificación de datos simulados               | 3     | Dependencia                | N1    |
| RF-106 | Excluir los simulados de toda analítica presentada como real | —     | Dependencia                | N1    |
| RF-072 | Versión, contexto e instante de toda salida inteligente      | 0     | Dependencia                | N2    |
| RF-073 | Evaluación reproducible de los componentes generativos       | 0     | Dependencia (transformado) | N2    |

**Reparto por banda:** N1 = 57 · N2 = 19 · N3 = 4. **Total en alcance: 80.**

### D.4 El contraste con la capacidad, recalculado

La banda N1 sola tiene 57 requisitos. Con el promedio optimista de 8 h por requisito que usa [D12/§3](risks-and-assumptions.md) son ~456 h; con el realista de 10 a 12 h, entre 570 y 684 h. **La capacidad de construcción declarada es ~504 h.**

| Conjunto        | Requisitos | Optimista (8 h) | Realista (10–12 h) | Frente a ~504 h |
| --------------- | ---------- | --------------- | ------------------ | --------------- |
| N1              | 57         | ~456 h          | 570 – 684 h        | 0,9 × a 1,4 ×   |
| N1 + N2         | 76         | ~608 h          | 760 – 912 h        | 1,2 × a 1,8 ×   |
| N1 + N2 + N3    | 80         | ~640 h          | 800 – 960 h        | 1,3 × a 1,9 ×   |

**Lectura honesta:** el núcleo solo cabe si todo sale bien y nada más se construye. El alcance completo no cabe. Es la misma conclusión de D12, con la mejora de que ahora el corte ya está trazado por banda y no hay que improvisarlo.

**Y hay una incertidumbre sobre el denominador que conviene resolver antes de discutir el numerador** — ver §M/I-09: el propio cálculo de las ~504 h se apoya en un supuesto que el Documento de Planificación contradice.

---

## E. Fusiones y normalización semántica

### E.1 Fusiones aceptadas

| #  | Fusión                    | Resultado | Qué se conserva                                                                                                                                                                                                                                                                                                    | Origen                                               |
| -- | ------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| F1 | RF-027 ⊕ RF-032 ⊕ RF-033  | RF-027    | Las tres transiciones del mismo autómata (D6/§4): iniciar con un día del ciclo e impedir dos en curso; conservar estado y reanudar; cerrar por inactividad; finalizar con duración e incorporar al historial. Se conservan como criterios de aceptación separados                                                   | Sugerida por el equipo (RF-32/33), ampliada a RF-027 |
| F2 | RF-023 ⊕ RF-038           | RF-038    | Modificar ejercicios, series, repeticiones, cargas y descansos de un alumno concreto sin afectar la plantilla ni a otros alumnos, **más** autoría, instante y aviso. Resuelve además la brecha de votos (1 frente a 7) sobre la misma operación                                                                     | Análisis                                             |
| F3 | RF-059 ⊕ RF-060           | RF-059    | El orden de alternativas **y** la exclusión dura de lo contraindicado o de nivel superior. RF-060 no era un requisito: era la restricción de seguridad sobre la salida de RF-059                                                                                                                                    | Análisis                                             |
| F4 | RF-036 ⊕ RF-107           | RF-036    | La cartera ordenada **y** la definición del orden de urgencia. RF-107 se creó porque RF-036 no era verificable sin él; separados producían una dependencia circular ya señalada en D8                                                                                                                               | Análisis                                             |
| F5 | RF-004 (planilla) → RF-065 | RF-065   | «Gestión de roles» (8 votos en la planilla) y «Gestión de usuarios y roles» (6 votos) son el mismo requisito. Los 8 votos se imputan a RF-065. La observación del equipo sobre **dos interfaces distintas por rol, con un conmutador**, se conserva como criterio de aceptación de la experiencia por rol            | Sugerida por el equipo                               |

### E.2 Fusiones rechazadas, con fundamento

| Fusión sugerida         | Decisión        | Fundamento                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RF-054 ⊕ RF-055         | **Rechazada**   | Son las dos clases de componente inteligente que [D11/DD-14](../decisions/design-decisions.md) separa deliberadamente. RF-054 **decide** (produce estructura y valores, se valida contra compatibilidad y rangos, pasa por el entrenador). RF-055 **narra** (no puede introducir ningún número ausente de su entrada, RN-94, exigible al 100 % y verificable de forma automática). Fusionarlos borra la frontera donde vive la garantía de que el texto no miente, y deja sin sujeto a RNF-24 |
| RF-005 → RF-004/RF-065  | **Rechazada**   | RF-065 responde «qué rol tiene esta persona»; RF-005 responde «¿este recurso concreto le pertenece o le está asignado?». Es el doble filtro RA-01, la mitigación de R-11 y el sujeto de RNF-14, que exige una prueba por cada operación con identificador de alumno. Absorberlo en la gestión de roles haría desaparecer la verificación por recurso, que es exactamente el defecto de seguridad más frecuente en sistemas de este tipo |
| RF-088 ⊕ RF-089         | **Rechazada**   | Un diagnóstico sin propuesta es un resultado válido y frecuente (RN-89a/restricción 4, FL-09/A1), no un fallo. Son dos salidas persistidas con fechas, versiones y modos de fallo distintos. Fusionarlas obligaría a inventar una «propuesta vacía»                                                                                                                                                                             |
| RF-021 → RF-020         | **Sin efecto**  | RF-021 sale del alcance (§F). La observación del equipo queda resuelta por vía de exclusión, no de fusión                                                                                                                                                                                                                                                                                                                       |

### E.3 Degradaciones: de requisito a regla, criterio o restricción

Cuatro elementos del corpus estaban escritos como requisitos funcionales sin serlo. Se conservan íntegros como normas verificables; dejan de contarse como alcance funcional.

| RF     | Pasa a ser                                           | Dónde vive                                                     |
| ------ | ---------------------------------------------------- | -------------------------------------------------------------- |
| RF-098 | Restricción de integridad — ya existe como **RI-01** | [D4/§4](../domain/domain-model.md)                             |
| RF-102 | Convención transversal de unidades y precisión       | [D2/§3](../product/glossary.md) más validación de servidor     |
| RF-103 | Convención transversal de tiempo (UTC, semana única) | [D2/§3](../product/glossary.md)                                |
| RF-104 | Criterio de aceptación de RF-029; ya es **RNF-13**   | [D9/§3](../requirements/non-functional-requirements.md)        |

---

## F. Requerimientos excluidos y diferidos

### F.1 Salen por votación

| RF     | Requisito                              | Votos | Consecuencia y compensación                                                                                                                                                                                             |
| ------ | -------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-011 | Perfil del entrenador                  | 4     | El alumno ve el nombre de su entrenador, no su presentación profesional. Sin efecto sobre el ciclo                                                                                                                       |
| RF-012 | Estimación energética orientativa      | 2     | Con RF-074, RF-075 y RF-108 fuera, **la nutrición desaparece por completo de esta etapa**. Coincide con el orden de recorte de D12/§4                                                                                    |
| RF-074 | Indicador nutricional diario           | 1     | —                                                                                                                                                                                                                        |
| RF-018 | Curación y desactivación de ejercicios | 0     | Un ejercicio propio mal cargado no se puede retirar. Mitigación: RF-017 es de ámbito de gimnasio y su autor puede corregirlo. **Deuda aceptada**, registrada en §M/R-20                                                  |
| RF-101 | Ejercicio desactivado en rutina vigente | —    | Cae con RF-018: sin desactivación no hay caso                                                                                                                                                                            |
| RF-021 | Publicación y reutilización de presets | 1     | Ver §F.4 — es la exclusión de mayor impacto arquitectónico                                                                                                                                                               |
| RF-025 | Solicitud de rutina por el alumno      | 3     | La rutina la origina el entrenador o la generación inicial automática (RF-087). C1 se sigue cumpliendo. Arrastra a RF-119 y RF-120                                                                                       |
| RF-119 | Candidato de rutina ajustable          | —     | **Deroga [DD-33](../decisions/design-decisions.md) para esta etapa.** Sin solicitud del alumno no hay solicitante que ajuste. Retira RN-124 a RN-129 y el flujo FL-03                                                    |
| RF-120 | Diferencia visible para el revisor     | —     | Cae con RF-119: el entrenador revisa la salida del componente sin capa intermedia                                                                                                                                       |
| RF-034 | Registro y corrección diferidos        | 2     | Una sesión no registrada el mismo día se pierde. **Sesga la adherencia a la baja** — hay que declararlo al presentar el indicador. Arrastra a RF-117                                                                     |
| RF-117 | Desbloqueo de sesión                   | —     | Cae con RF-034. El plazo de corrección vuelve a ser absoluto, con el costo de CB-70                                                                                                                                     |
| RF-039 | Comentarios asincrónicos               | 1     | No hay canal entrenador↔alumno salvo los avisos de RF-095                                                                                                                                                                |
| RF-047 | Parametrización de reglas de cálculo   | 3     | Las constantes quedan documentadas en D12/§1.1 y fijadas en código                                                                                                                                                      |
| RF-049 | Representación muscular sobre esquema  | 4     | **Degradado, no eliminado:** el mismo dato (RF-040) se presenta como barras por grupo muscular dentro de RF-048. Elimina el riesgo R-06 y la dependencia del recurso vectorial. Requiere confirmación del cliente (§P/PD-08) |
| RF-056 | Resumen narrado del progreso           | 4     | Ya lo había sustituido la justificación de la propuesta (RF-090), más específica y verificable                                                                                                                          |
| RF-068 | Panel analítico del gimnasio           | 2     | El administrador conserva gestión, no analítica                                                                                                                                                                          |
| RF-006 | Baja de cuenta y portabilidad          | 0     | **Diferido con riesgo legal declarado** — ver §P/PD-02. Arrastra a RF-105                                                                                                                                               |
| RF-097 | Auditoría general                      | —     | **Reducida**, no eliminada: se conserva la trazabilidad puntual de RF-038, RF-066, RF-091 y RF-114                                                                                                                       |

### F.2 Ya estaban fuera y se confirman

RF-061, RF-062 y RF-063 (riesgo de abandono, WON'T desde v3.3; 1, 0 y 0 votos — la votación confirma la decisión) · RF-076 base de alimentos · RF-077 mensajería · RF-078 pagos · RF-079 video propio · RF-080 representación tridimensional · RF-081 dispositivos de monitorización · RF-075 y RF-108 pauta nutricional, que caen con RF-012.

### F.2b RF-053 se conserva pese a no alcanzar el corte, y por qué

La interpretación de lenguaje natural obtuvo **3 de 8 votos**. Bajo la regla base debería salir, y la primera emisión de este documento la sacó. Esa decisión no se sostiene.

`deliverable PO/alcance-ia-generativa.md` v2.1, del 2026-08-28, dice literalmente qué se entrega al Product Owner: «**Entiende un pedido en lenguaje natural.** El entrenador o el alumno describen lo que necesitan con sus palabras y el sistema lo traduce a parámetros concretos, que se muestran para confirmar antes de usarlos», y encabeza esa lista con «qué nos comprometemos a entregar. **El alcance comprometido es un piso**». Es un compromiso escrito ante el Product Owner, no una aspiración interna.

**Una votación interna de 3 de 8 no revoca un compromiso ya asumido con el cliente.** RF-053 se conserva en alcance, en banda N2, con el conflicto declarado. Retirarlo es una conversación con el Product Owner, no una consecuencia mecánica del corte — es la decisión PD-07, reformulada en consecuencia.

Esto obliga además a una corrección técnica: la mitigación de inyección de prompt no puede apoyarse en «no entra texto libre al sistema», porque sí entra. Se apoya en dónde queda confinado — ver RNF-41 en §L.

### F.3 Salen por no haber sido validados con el cliente

RF-121 (sugerencia de carga de la próxima serie) y RF-122 (proyección de trayectoria). D8 v3.2 ya los declara como **propuestas del equipo, no pedidos del cliente**, pendientes de confirmación. No hay fundamento para consumir capacidad en ellos en esta etapa. RF-030 sigue siendo el piso garantizado de precarga.

### F.4 La exclusión de los presets, y por qué es la más importante

La planilla y el acta coinciden: RF-021 obtuvo 1 voto, RF-022 obtuvo 0, y el equipo respondió a la decisión D4 del acta con **«No usaremos preset, todo será generado desde cero con una batería de prompts»**. La exclusión está sobradamente respaldada.

Tiene dos consecuencias que el corpus actual no absorbe:

1. **RF-022 no es una funcionalidad de presets.** La observación de la planilla —«Del 021 al 025 incluidos, todos pertenecen a los presets, si se hace uno se tienen que hacer todos»— agrupa mal a RF-022. La copia profunda e independiente al asignar es el invariante que impide que modificar una plantilla reescriba el pasado de doce alumnos ([D4/PD-01](../domain/domain-model.md), DD-02). Sin él, el versionado de RF-092 no tiene sobre qué operar y la adaptación destruye historial. **RF-022 se reincorpora como dependencia necesaria de máxima prioridad**, y se deja constancia de que su voto nulo proviene de una lectura equivocada del enunciado, no de una decisión de alcance.

2. **Se queda sin fallback la continuidad ante indisponibilidad generativa.** RF-058, RN-95b y la ADR 0004 apoyan toda la continuidad en «conservar la solicitud de presets publicados del gimnasio como vía disponible». Sin presets, esa frase queda vacía. **Resolución adoptada:** la vía manual es la **plantilla del entrenador (RF-019, 8 votos)**, que en este corpus es el mismo objeto que un preset sin publicar. RF-019 deja de ser una comodidad y pasa a ser el piso de disponibilidad de CAP-4. Hay que reescribir RF-058, RN-95b y las consecuencias de la ADR 0004 en esos términos (§O). Queda un hueco real que debe confirmarse: **un alumno nuevo, en un gimnasio sin plantillas cargadas y con el servicio generativo caído, no obtiene ninguna rutina** (§P/PD-03).

---

## G. Dependencias necesarias

Elementos que no son funcionalidad de negocio independiente pero sin los cuales el alcance aprobado no funciona. Se declaran como dependencia, no como requisito nuevo.

| ID     | Dependencia                                            | Votos | De qué es dependencia                            | Qué pasa si no está                                                                                                                                                                                          |
| ------ | ------------------------------------------------------ | ----- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DEP-01 | **RF-022** copia al asignar                            | 0     | RF-019, RF-038, RF-092, todo CAP-7               | La adaptación reescribe el pasado de todos los alumnos que comparten plantilla. Corrupción de datos, no inconveniencia                                                                                       |
| DEP-02 | **RF-043** cumplimiento                                | 0     | RF-088 (`SOBREEXIGENCIA`), RF-046                | El diagnóstico pierde dos de sus cinco situaciones. Y es lo único que distingue este producto de un registrador                                                                                              |
| DEP-03 | **RF-024** frecuencia objetivo                         | 2     | RF-042 (adherencia), RN-89a global               | La adherencia no tiene denominador                                                                                                                                                                           |
| DEP-04 | **RF-058 + RF-113** continuidad e invalidez            | 1, —  | RF-054, RF-087, todo CAP-4                       | Una salida inválida llega al entrenador como si fuera una propuesta. Marcados **MUST\*** por el propio equipo en la planilla                                                                                 |
| DEP-05 | **RF-057** restricciones del contenido                 | 0     | RF-055, RF-090                                   | Un texto generado puede inventar números o emitir indicaciones médicas. Marcado **MUST\*** en la planilla                                                                                                    |
| DEP-06 | **RF-005 + RF-069** autorización y ámbito              | 2, 4  | Toda operación con identificador ajeno           | Cualquiera lee los datos de salud de cualquiera. R-11, RNF-14, RNF-20                                                                                                                                        |
| DEP-07 | **RF-066** asignación entrenador–alumno                | 2     | RF-005, RF-036, RF-038, RF-091, RF-110           | No existe sujeto que pueda autorizar la puerta. La capacidad C5 no es implementable                                                                                                                          |
| DEP-08 | **RF-030** precarga                                    | 1     | RNF-07 (dos interacciones por serie), RF-029     | Registrar una serie deja de caber en el uso real: de pie, entre series, con una mano                                                                                                                         |
| DEP-09 | **RF-071 + RF-106** datos simulados                    | 3, —  | RF-088, RF-046, toda demostración                | En catorce semanas no se acumula historial suficiente para que el diagnóstico produzca nada. El cliente autorizó explícitamente arrancar con datos cargados a mano                                           |
| DEP-10 | **RF-099** taxonomía y curación                        | —     | RF-016, RF-040, RF-086                           | El volumen se calcula mal y **corrompe el diagnóstico y con él todas las propuestas** (R-07)                                                                                                                 |
| DEP-11 | **RF-114 + RF-118** inventario y catálogo prescribible | —     | RF-086, RF-054, RF-087, RF-059                   | Se prescriben ejercicios imposibles de ejecutar en ese gimnasio. Decisión del cliente (N-27), no del equipo                                                                                                  |
| DEP-12 | **RF-115 + RF-116 + RF-100** alta y ámbito             | —     | Todo                                             | No hay gimnasio, no hay usuarios, no hay demostración (R-12)                                                                                                                                                 |
| DEP-13 | **RF-096** consentimiento                              | —     | RF-009, RF-010, RF-084                           | Se tratan datos de salud sin base. RNF-21                                                                                                                                                                    |
| DEP-14 | **RF-111** contexto suficiente                         | —     | RF-054, RF-087, RF-088                           | La inteligencia decide con huecos y nadie se entera                                                                                                                                                          |
| DEP-15 | **RF-112 + RF-109** continuidad de la puerta           | —     | RF-110, RF-066                                   | Un alumno sin entrenador queda en un limbo silencioso y sus propuestas se pierden al reasignarlo                                                                                                             |
| DEP-16 | **RF-072** trazabilidad de salidas                     | 0     | RF-090, criterio de éxito E9                     | No se puede auditar por qué el sistema propuso lo que propuso. **Alcance reducido**: versión, instante y contexto de entrada de las salidas que producen una propuesta; no un registro general               |
| DEP-17 | **RF-073** evaluación de componentes                   | 0     | RNF-24, RNF-25, criterio E9                      | **Transformado**: con RF-061 a RF-063 fuera y RF-059 en la capa generativa, ya no hay modelo clásico que evaluar. Pasa a ser el **conjunto de regresión generativa** que se corre antes de cambiar prompt, modelo o parámetros |
| DEP-18 | **RF-095** avisos                                      | —     | RF-038, RF-044, RF-046, RF-091                   | Cuatro requisitos prometen notificar y no hay canal. **Alcance reducido** a los tipos que el ciclo necesita                                                                                                  |

---

## H. Impacto arquitectónico

### H.1 Punto de partida real

Verificado sobre los tres repositorios el 2026-09-01:

| Repositorio              | Qué hay                                                                                                       | Qué **no** hay                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `proyecto-gimnasio`      | Vite + React + TS, ESLint/Prettier, Vitest, CI, Dockerfile, `App.tsx` con una pantalla de bienvenida           | Router, estado remoto, cliente de API, vistas                                      |
| `proyecto-gimnasio-back` | Express + TS, CORS por lista blanca, `/health` y `/ready`, cliente Prisma, pipeline de migraciones, Vercel, CI | **Ningún modelo en `schema.prisma`**, ninguna ruta de dominio, ninguna autorización |
| `proyecto-gimnasio-ia`   | Paquete Python con pandas, scikit-learn y sqlalchemy declarados; ruff, mypy strict, pytest, CI                 | **Paquete vacío** — ni API HTTP, ni worker, ni conector LLM                         |

**Conclusión:** no hay funcionalidad implementada ni parcialmente implementada; no hay funcionalidad implementada y no documentada; no hay deuda técnica de producto. Toda la deuda es documental (§O). El punto de partida es limpio, lo que permite tomar las decisiones de §H.2 sin costo de migración — pero **sólo hasta la primera migración de Prisma**.

### H.2 Base de datos

El recorte no altera el núcleo del modelo, pero retira entidades completas.

| Cambio                                                                                                                          | Motivo                                                              |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Se retira** `Comentario`                                                                                                      | RF-039 fuera                                                        |
| **Se retira** el atributo `nivel de actividad` de `PerfilAlumno`                                                                | RF-012 fuera                                                        |
| **Se retira** `PlantillaRutina.publicada`                                                                                       | RF-021 fuera; una plantilla ya no se publica                        |
| **Se reduce** `RutinaAsignada.origen` a `PLANTILLA_ENTRENADOR` y `GENERADA`                                                      | RF-021 y RF-025 fuera                                               |
| **Se retiran** de `SesionEntrenamiento` los atributos `es diferida` y `desbloqueada hasta`                                       | RF-034 y RF-117 fuera                                               |
| **Se retiran** `ScoreRiesgo` y `SegmentoPerfil`                                                                                 | Ya derogadas en D4 v2.1                                             |
| **Se reduce** `RegistroAuditoria` a las operaciones de RF-038, RF-066, RF-091 y RF-114                                           | RF-097 reducido                                                     |
| **Se conserva íntegro** el eje `RutinaAsignada → VersionRutina → DiaRutina → EjercicioRutina → SeriePrescripta`                  | Es el núcleo. DEP-01                                                |
| **Se conservan íntegras** `EjercicioMusculo` y `EjercicioArticulacion`                                                           | Sin ellas la compatibilidad no es calculable (DEP-10)               |
| **Se conservan** las 23 restricciones de integridad RI-01 a RI-23                                                               | Ninguna depende de algo excluido                                    |

**Índices que hay que definir desde la primera migración**, porque son los que sostienen RNF-01 y RNF-36: `RegistroSerie(sesion, orden)` único · `RegistroSerie(ejercicio_ejecutado, sesion)` para volumen y capacidad máxima · `SesionEntrenamiento(alumno, fecha_de_ocurrencia)` para adherencia e historial · `RutinaAsignada(alumno, estado)` parcial sobre VIGENTE y PROPUESTA · `AsignacionEntrenador(alumno)` parcial sobre `hasta IS NULL` · `CondicionFisica(perfil)` parcial sobre `hasta IS NULL` · `Ejercicio(gimnasio)` admitiendo `NULL` para el catálogo base.

**Aislamiento multi-gimnasio.** Se resuelve en el modelo (`gimnasio` en toda entidad raíz, RI-01, RA-02), no en el motor. No se adopta *row-level security* de PostgreSQL: agrega una segunda fuente de autorización que hay que mantener sincronizada con la de la aplicación, y el proyecto no tiene capacidad para operar dos. Se compensa con RNF-14: una prueba automatizada por cada operación con identificador de alumno.

### H.3 Backend

- **Monolito modular en Express y TypeScript sobre Vercel.** No cambia. Los módulos que el recorte deja en pie: identidad, contexto, catálogo, prescripción, entrenamiento, indicadores, adaptación e integración IA. Desaparecen los de nutrición y analítica del gimnasio.
- **La autorización es una capa única, no un `if` por ruta.** RA-01 es un doble filtro y RNF-14 exige una prueba por operación. Si se dispersa, R-11 se materializa. Debe existir antes de la segunda ruta de dominio, no después de la vigésima.
- **Transaccionalidad.** Cuatro operaciones son atómicas o no son: el aprovisionamiento (RNF-38), la puesta en vigencia de una rutina (crear versión, archivar la anterior, registrar la revisión), la resolución de una propuesta (crear versión, resolver ajustes, emitir aviso) y la copia profunda al asignar. Ninguna admite estado intermedio observable.
- **Concurrencia.** Tres puntos reales, ya catalogados: CB-14 (versión nueva con sesión en curso — la sesión conserva su prescripción congelada, PD-02 del modelo, sin bloqueo), CB-30 (misma propuesta resuelta dos veces — control de versión optimista sobre el estado de la propuesta), CB-66 (el inventario cambia mientras se aprueba una rutina — revalidar en el instante de la puesta en vigencia, no en el de apertura del formulario).
- **Idempotencia.** RF-104/RNF-13 sobre el registro de series, y clave idempotente sobre la solicitud de generación. Son los dos únicos puntos donde el reintento del cliente es cotidiano.
- **El backend nunca espera al LLM.** La solicitud se acepta y el frontend consulta estado contra el backend. No es una optimización: Vercel no sostiene una petición de 120 segundos.

### H.4 Servicio de IA — la decisión que está bloqueada

**El corpus contiene dos decisiones arquitectónicas incompatibles, ambas en estado «aceptada»:**

|                                  | ADR 0005 (2026-08-25)                                                                                                                                 | ADR 0004 «servicio generativo online en el Polo» (2026-08-29)                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Qué decide                       | El AI Gateway es un **módulo interno del backend** (`GenerativeAiPort` más `OllamaAdapter`). El backend llama al LLM Server directamente               | `proyecto-gimnasio-ia` expone una **API HTTP Python con worker asíncrono** desplegada en el Polo y publicada por ngrok. El backend la llama a ella |
| Opción explícitamente descartada | «(c) AI Gateway como microservicio propio, desplegado aparte, entre el backend y el LLM Server»                                                        | —                                                                                                                                 |
| Fundamento                       | No hay capacidad para operar un tercer servicio                                                                                                       | Vercel no puede sostener el LLM dentro de una petición; hace falta un worker durable                                              |

La ADR 0004 decide exactamente la opción (c) que la ADR 0005 descarta, y **no la declara reemplazada**. La arquitectura vigente (`system-overview.md`, `backend.md`, `analytics-engine.md`) sigue a la ADR 0004. **Esto debe resolverse antes de la primera línea de código de integración** (§P/PD-04).

Recomendación técnica, para que la decisión llegue preparada: **prevalece la ADR 0004**, porque su fundamento es una restricción física (Vercel no sostiene 120 segundos de inferencia; hace falta un proceso durable) y el de la ADR 0005 es un presupuesto de esfuerzo. Pero el fundamento de la ADR 0005 sigue siendo real: operar API, worker, LLM y agente ngrok en el Polo es trabajo no contabilizado en las 504 h. Lo que corresponde es **marcar la ADR 0005 como reemplazada por la ADR 0004 en su parte de ubicación de despliegue**, conservar de ella el puerto y el adaptador como patrón interno del servicio Python, y declarar la operación del Polo como carga adicional explícita.

**Lo que el recorte cambia en la capa de IA:**

| Antes (D8 v3.3)                                       | Ahora                                                                                                                                        |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `interpretarPedido` (RF-053) — lenguaje natural libre | **Se conserva** (§F.2b). Su salida es un conjunto de parámetros de enumeraciones cerradas, validado y confirmado por el usuario antes de usarse. Es la única entrada de texto libre del sistema y no alcanza a `generarRutina` |
| `generarRutina` (RF-054, RF-087)                      | Sin cambios. **Pasa a ser la única vía de creación automática**, sin preset del que partir                                                    |
| `explicarCriterios` (RF-055)                          | Sin cambios                                                                                                                                  |
| `sugerirAlternativas` (RF-059)                        | Sin cambios, con RF-060 absorbido como exclusión dura previa y posterior                                                                      |
| `resumirProgreso` (RF-056)                            | **Retirado**                                                                                                                                  |
| `describirPerfil` (RF-064)                            | Se conserva (6 votos), efímero, banda N3                                                                                                      |
| Fallback igual a presets publicados                   | **Fallback igual a plantillas del entrenador (RF-019)**                                                                                       |

**Responsabilidades que no son del LLM, y hay que poder demostrarlo en la defensa:** el catálogo prescribible (filtro exacto en SQL, ADR 0007), la compatibilidad (RN-44a a RN-44d, exclusión dura en código), los rangos del tipo de rutina (RN-39a), el diagnóstico (RN-79a) y las reglas de ajuste (RN-89a). El LLM construye el candidato y redacta; no calcula compatibilidad, no aprueba, no persiste y no emite indicaciones médicas.

### H.5 Frontend

Vistas que el recorte deja en pie, por rol:

- **Alumno (7):** completar cuenta desde invitación · contexto (perfil, objetivo, condiciones, aptitud, mediciones) · rutina vigente · **sesión activa** · historial · panel de progreso · avisos.
- **Entrenador (6):** cartera priorizada · ficha del alumno · revisión de rutina propuesta · resolución de propuesta de adaptación · edición de rutina y plantillas · generación de rutina desde formulario.
- **Administrador (3):** invitaciones y roles · asignaciones · inventario.

**Desaparecen:** comentarios, panel del gimnasio, pauta nutricional, mapa muscular sobre esquema corporal, ajuste del candidato de rutina y registro diferido.

**La sesión activa es la pantalla de mayor riesgo del proyecto** (R-05) y la que produce el sustrato del que depende toda la inteligencia. Restricciones no negociables: usable a 360 px sin desplazamiento horizontal (RNF-06), dos interacciones por serie con los valores precargados (RNF-07, y por eso DEP-08), borrador local con reintento ante pérdida de conexión (RNF-10) y envío idempotente (RNF-13).

**La observación del equipo sobre alumno y entrenador con dos interfaces y un conmutador** (planilla, RF-004) se conserva como criterio de aceptación de RF-065, y encaja con DD-08 (los roles son un conjunto) y DD-28 (un entrenador que entrena necesita otro entrenador).

### H.6 Contratos entre repositorios

Sin cambios de propiedad: el backend es dueño del OpenAPI público, del esquema y de las migraciones; el frontend genera su cliente desde una versión explícita; el servicio IA es dueño del OpenAPI de orquestación. Lo que el recorte simplifica es la superficie: desaparecen los endpoints de comentarios, analítica del gimnasio, nutrición, candidato ajustable y registro diferido.

**Los tres contratos hay que congelarlos temprano** (R-11): el OpenAPI del backend en la semana 3, el OpenAPI del servicio IA junto con la primera generación, y el esquema de la base antes de la primera migración a `test`.

---

## I. Modelo funcional y de dominio

El modelo de [D4](../domain/domain-model.md) se conserva salvo las retiradas de §H.2. Los cuatro puntos que gobiernan su corrección:

1. **Copia más versiones completas** (PD-01 del modelo). La rutina se copia al asignarse y cada adaptación produce una versión completa nueva. No hay diferencias que calcular ni conflictos que resolver, y el historial de adaptaciones se responde comparando dos versiones.
2. **La sesión es autocontenida** (PD-02 del modelo). Copia su prescripción al iniciarse. El pasado es inmune al versionado sin lógica adicional, y el cumplimiento sale gratis por serie.
3. **Derivado o persistido** (PD-03 del modelo). Se derivan volumen, capacidad máxima estimada, adherencia y cumplimiento; se persisten sólo los eventos con fecha (récord), las salidas fechadas de un componente (diagnóstico, propuesta) y la única marca derivada que debe sobrevivir a la consulta (`estado de compatibilidad` de `EjercicioRutina`).
4. **El equipamiento es del gimnasio** (PD-07 del modelo). Por eso la incompatibilidad por equipamiento **impide** en lugar de advertir, y por eso el inventario es un dato crítico.

**Consistencia temporal — el eje que no puede romperse.** Cinco entidades tienen vigencia: objetivo, condición física, aptitud, asignación entrenador–alumno y versión de rutina. La regla que las une: **toda pregunta sobre el pasado se responde con el estado vigente en esa fecha, no con el estado actual.** Una sesión referencia la versión bajo la que se ejecutó (RI-16); el diagnóstico referencia la versión evaluada; una condición cerrada no borra la propuesta que motivó, la invalida. Un diseño que reemplace la vigencia por un campo mutable hace irrespondible la pregunta que el cliente pidió responder: *por qué cambió esta rutina*.

---

## J. Flujos críticos

Cinco flujos concentran el valor. Los tres marcados ⭐ son la demostración del producto.

### J.1 ⭐ FL-A · Incorporación con rutina inmediata (CAP-1 → CAP-2 → CAP-4 → CAP-8)

El administrador o el entrenador emite una invitación nominal → la persona crea su cuenta y queda vinculada al gimnasio → declara perfil, objetivo y condiciones → el sistema verifica que el contexto es suficiente (RF-111) → genera una rutina completa sobre el catálogo prescribible, filtrada por compatibilidad (RF-087, RF-086) → la rutina nace **PROPUESTA** → el entrenador asignado la revisa y la aprueba → entra en **VIGENCIA** y el alumno recibe el aviso.

**Estado final esperado:** ningún alumno incorporado termina el día sin una rutina propuesta (criterio E1).
**Excepciones:** contexto insuficiente → se declara qué falta y no se genera · generación no disponible → el entrenador asigna una plantilla propia (RF-019) · sin entrenador vigente → la rutina queda propuesta y el administrador es señalado (RF-112).

### J.2 ⭐ FL-B · Sesión de entrenamiento (CAP-5)

Selecciona un día del ciclo → el sistema **congela la prescripción dentro de la sesión** → registra serie a serie con los valores de la última ejecución precargados → puede agregar, omitir o sustituir → finaliza, o se cierra sola por inactividad.

**Estado final esperado:** la sesión conserva de forma conjunta lo prescripto y lo ejecutado, y no cambia nunca más.
**Excepciones:** pérdida de conexión → borrador local y reintento · reanudación → misma sesión, mismo congelamiento · valor atípico → confirmación explícita · envío repetido → un solo registro.

### J.3 ⭐ FL-C · Diagnóstico y adaptación (CAP-6 → CAP-7 → CAP-8)

Cada dos semanas, fuera del camino de la petición: el sistema evalúa cada ejercicio de la rutina vigente y le asigna una de cinco situaciones por orden de precedencia → determina la situación global → aplica la tabla situación → ajuste → **verifica la propuesta completa contra compatibilidad y rangos antes de presentarla** → avisa al entrenador → el entrenador acepta entera, acepta en parte o rechaza → si acepta, se genera una versión nueva y se avisa al alumno.

**Estado final esperado:** toda adaptación aplicada conserva el criterio que la motivó y el dato que la sustenta (criterio E7); ninguna sesión ejecutada cambia (criterio E6).
**Excepciones:** datos insuficientes → diagnóstico registrado sin propuesta, declarando qué faltó · ningún ajuste aplicable → diagnóstico sin propuesta, que **es un resultado, no un fallo** · esfuerzo percibido nunca registrado → se diagnostica sin ese criterio y se declara · la propuesta deja de ser compatible antes de resolverse → INVALIDADA y se genera otra · treinta días sin resolver → CADUCADA · la asignación termina durante la revisión → la operación no se completa.

### J.4 FL-D · Reevaluación por cambio de contexto (CAP-2/CAP-3 → CAP-7)

Cambia el objetivo, aparece o se cierra una condición, vence la aptitud **o cambia el inventario del gimnasio** → se recalcula el catálogo prescribible si corresponde → se reevalúa la rutina vigente → los ejercicios afectados se **marcan sin retirarse** → se avisa al entrenador y al alumno → se elabora la propuesta de sustitución.

**Por qué se marca y no se retira:** retirar un ejercicio de una rutina vigente es una decisión de prescripción, y la prescripción es del entrenador. Mientras haya una marca, el alumno recibe la advertencia al iniciar cada sesión que lo incluya.
**Excepción crítica:** no existe alternativa admisible en el catálogo prescribible → el ajuste no se propone, y el hecho se declara explícitamente en la propuesta en lugar de silenciarse.

### J.5 FL-E · Revisión priorizada (CAP-8)

El entrenador ve su cartera ordenada por urgencia: pendientes de revisión → incompatibilidad sobrevenida → estancamiento → caída de adherencia → sin señal. Entra a la ficha consolidada, resuelve lo pendiente o interviene directamente sobre la rutina.

**Riesgo asociado:** si el tiempo de revisión crece, el sistema deja de servir por congestión humana, no por defecto técnico (criterio E1b, riesgo R-09). Hay que medirlo, no absorberlo.

---

## K. Casos borde y errores

El corpus ya tiene 73 casos borde catalogados en [D10](../domain/edge-cases.md). Lo que aporta este baseline es **dónde se resuelve cada clase**, y qué cambia con el recorte.

| Clase                                   | Dónde se resuelve                        | Ejemplos                                                                                                                                                                                          |
| --------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vacíos y arranque**                   | Presentación más RF-051                  | Alumno sin sesiones, representación sin datos, cartera vacía, gimnasio recién aprovisionado, inventario vacío                                                                                      |
| **Datos ausentes o degradados**         | Regla de negocio                         | Ejercicio sin clasificación muscular (no aporta volumen, distinto de aportar cero) · esfuerzo percibido nunca registrado (se diagnostica sin ese criterio y se declara) · condición sin zona corporal |
| **Cambios en el tiempo**                | Vigencia más versionado                  | Condición nueva que invalida una propuesta pendiente · aptitud que vence en pleno período · retiro de equipamiento usado por muchas rutinas                                                        |
| **Interrupción**                        | Máquina de estados (RF-027)              | Cierre de la aplicación a mitad de sesión · vuelta pasadas ocho horas · invitación a medio usar                                                                                                     |
| **Concurrencia**                        | Transacción más control optimista        | Versión nueva con sesión en curso · misma propuesta resuelta dos veces · inventario que cambia durante una aprobación                                                                              |
| **Permisos en los bordes**              | Autorización centralizada (RA-01..RA-10) | Asignación que termina durante la revisión · actor con doble rol consultando a un alumno no asignado · acceso por enlace directo a un recurso ajeno                                                |
| **Fallos de dependencias**              | Arquitectura más RF-058 y RF-113         | Servicio IA, ngrok o LLM caídos o lentos · fuente externa del catálogo cambiada · proceso diferido nunca ejecutado                                                                                 |
| **Límites y valores extremos**          | Validación de servidor (RF-102)          | Carga cero o negativa · más de cien repeticiones · fecha futura o anterior a noventa días · sesión que cruza medianoche · alumno en otra zona horaria                                              |
| **Comportamiento absurdo pero posible** | Regla de negocio                         | Ocho sesiones en un día · carga muy superior al histórico → confirmación explícita · entrenador que rechaza sistemáticamente todo → información sobre la calidad del diagnóstico, no un error      |

### K.1 Casos que el recorte elimina

CB-11 (estimación de riesgo nunca calculada), CB-70 (error de carga detectado un mes después — desaparece con RF-034 y RF-117), CB-72 y CB-73 (tope de regeneraciones y candidato abandonado — desaparecen con RF-119).

### K.2 Casos que el recorte agrava, y que hay que tratar explícitamente

| Caso                                                                           | Por qué se agrava                                                   | Dónde se resuelve                                                                                                                                                                     |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CB-20 / CB-36 · el servicio generativo no responde o no produce salida válida** | Con presets fuera, era el único fallback declarado                  | RF-058 reescrito: la vía manual es la plantilla del entrenador. **Y hay que declarar el hueco**: gimnasio sin plantillas más servicio caído igual a alumno nuevo sin rutina (§P/PD-03) |
| **CB-21 · no existe alternativa admisible para un ejercicio incompatible**     | Sin RF-101 no hay tratamiento paralelo para el ejercicio desactivado | El ajuste no se propone y el hecho se declara en la propuesta. El ejercicio queda marcado INCOMPATIBLE en la rutina vigente                                                            |
| **Sesión no registrada el mismo día**                                          | Sin RF-034 el dato se pierde definitivamente                        | **La adherencia queda sesgada a la baja y hay que declararlo en la presentación del indicador**, no corregirlo en silencio                                                             |
| **CB-13 · ejercicio propio mal cargado**                                       | Sin RF-018 no hay desactivación                                     | Corrección por el autor. Deuda aceptada, §M/R-20                                                                                                                                      |

---

## L. Requisitos no funcionales

Se conserva [D9](../requirements/non-functional-requirements.md) v2.0 con estos ajustes. La regla se mantiene: **un requisito no funcional sin forma de comprobarlo es una aspiración**, y no se inventan cifras.

| RNF           | Cambio                                                                                                                                                                                                                                                                                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RNF-05        | ✎ Retirar «y estimación de riesgo». Queda: el diagnóstico se ejecuta fuera del camino de la petición                                                                                                                                                                                                                                                              |
| RNF-11        | ✎ «los presets del gimnasio siguen solicitables» → «las plantillas del entrenador siguen asignables»                                                                                                                                                                                                                                                              |
| RNF-18        | ✎ Igual sustitución en el criterio de verificación                                                                                                                                                                                                                                                                                                                |
| RNF-26        | ✎ Reencuadrar: ya no hay modelo clásico contra el que comparar. Pasa a ser la comparación de la rutina generada contra la construida a mano por un entrenador sobre el mismo caso                                                                                                                                                                                  |
| RNF-28        | ✎ Retirar «vistas de riesgo». Queda la analítica sobre datos simulados                                                                                                                                                                                                                                                                                            |
| RNF-35        | **Retirado.** Cae con RF-049. La accesibilidad del dato queda cubierta por RNF-34 sobre la presentación en barras                                                                                                                                                                                                                                                  |
| RNF-39        | Se conserva. El cambio de inventario es la operación masiva de mayor riesgo de rendimiento                                                                                                                                                                                                                                                                         |
| **RNF-41** 🆕 | El texto libre del usuario queda confinado a la interpretación de RF-053, y no alcanza a ningún otro componente generativo: `generarRutina`, `sugerirAlternativas` y los narrativos reciben exclusivamente parámetros de enumeraciones cerradas y estructuras ya validadas por el servidor. *Verificación:* inspección del contrato del servicio IA — el único campo de texto libre del usuario es la entrada de `interpretarPedido`, y su salida se valida contra las enumeraciones de D2/§4 y se confirma con el usuario antes de propagarse |
| **RNF-42** 🆕 | Todo alumno con contexto suficiente tiene una rutina propuesta dentro de las 24 h de completar su incorporación. *Verificación:* consulta sobre la base — cero alumnos con contexto suficiente y sin rutina. Es el criterio E1 hecho comprobable, y el que la exclusión de presets pone en riesgo                                                                    |

**Cifras que siguen sin fundamento externo y hay que declarar como convención del proyecto, no como restricción:** los umbrales de RN-79a (4 sesiones, 70 %, ±2,5 %, esfuerzo ≥ 9 o ≤ 5), las magnitudes de RN-89a (+2,5 %, −10 %, ±1 serie, 2,50 kg), la periodicidad de dos semanas, la caducidad de treinta días y la ventana de adherencia de cuatro semanas. Están registradas como `[S]` en D12/§1.1 y son discutibles con el cliente (§P/PD-09).

---

## M. Riesgos

Se conserva la matriz de [D12/§2](risks-and-assumptions.md) con estos cambios.

| ID          | Riesgo                                                                        | Prob.    | Impacto  | Cambio y tratamiento                                                                                                                                                                                                                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R-01        | El conjunto MUST no entra en el plazo                                         | **Muy alta** | Muy alto | **Se mantiene en Muy alta.** El recorte pasa de 79 MUST a 57 requisitos de banda N1 — una reducción del 28 %, no la que hacía falta. N1 sola está entre 0,9 × y 1,4 × la capacidad (§D.4). Bandas y §N.3 como decisión preparada, pero la decisión sigue siendo del cliente                                                              |
| R-03        | La estimación de riesgo se queda sin datos reales                             | —        | —        | **Cerrado.** RF-061 a RF-063 fuera, confirmado por la votación                                                                                                                                                                                                                                                                             |
| **R-17** 🆕 | **La disponibilidad de CAP-4 depende por completo del servicio generativo**   | **Alta** | **Muy alto** | Consecuencia directa de excluir los presets. Sin generación y sin plantillas cargadas, un alumno nuevo no obtiene rutina. Mitigación: cargar plantillas de arranque por gimnasio en el aprovisionamiento, y medir la disponibilidad real del Polo desde el Sprint 1. **No hay mitigación técnica dentro del alcance recortado** |
| **R-18** 🆕 | **La contradicción ADR 0004 / ADR 0005 se descubre al integrar**              | **Alta** | **Alto** | Dos decisiones «aceptadas» e incompatibles sobre dónde vive el servicio de IA. Resolverlo antes de la primera línea de integración (§P/PD-04)                                                                                                                                                                                               |
| **R-19** 🆕 | **La adherencia se mide sesgada y nadie lo declara**                          | Media    | Medio    | Sin registro diferido (RF-034), una sesión no cargada el mismo día se pierde. La adherencia —insumo de RN-89a global— queda sesgada a la baja. Mitigación: declararlo en la presentación del indicador y en la defensa                                                                                                                       |
| **R-20** 🆕 | **Un ejercicio propio mal cargado no se puede retirar**                       | Media    | Bajo     | Sin RF-018. Acotado al ámbito del gimnasio. Deuda aceptada                                                                                                                                                                                                                                                                                 |
| R-07        | La clasificación muscular importada es pobre                                  | Media    | **Alto** | **Sube de prioridad.** Es la única entrada de RF-040, y un volumen mal calculado corrompe el diagnóstico y todas las propuestas. La curación manual (RF-099) deja de ser opcional                                                                                                                                                            |
| R-09        | Congestión de la puerta del entrenador                                        | Media    | Alto     | Se agrava: sin comentarios (RF-039) el entrenador no tiene canal ligero para responder sin abrir la ficha                                                                                                                                                                                                                                   |
| R-15        | El inventario del gimnasio se declara mal o queda desactualizado              | Alta     | Alto     | Sin cambios. Sigue sin haber mitigación técnica para un inventario que declara equipamiento inexistente                                                                                                                                                                                                                                     |
| R-16        | La expectativa sobre el LLM excede su autoridad real                          | Media    | Alto     | Se agrava con la exclusión de presets: el LLM pasa a ser la única vía automática de creación                                                                                                                                                                                                                                                |

### M.1 Inconsistencia que precede a la conversación de alcance

| #     | Inconsistencia                                                                                                                                                                                                                                                                                                                     | Estado                                                                                                    |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **I-09** 🆕 | **La capacidad de construcción está calculada sobre un supuesto que otra fuente contradice.** [D12/§3](risks-and-assumptions.md) descuenta a tres personas —dirección de proyecto y las dos de calidad— y llega a «≈ 6/9 × 756 ≈ 504 h». El Documento de Planificación e Inicio §1.3 dice lo contrario de forma explícita: «Los roles de gestión **no son de dedicación exclusiva: todos los integrantes participan en la construcción del software**», y de hecho asigna a las tres personas a equipos verticales con alcance funcional | **Abierta y de alto impacto.** Entre 504 h y 756 h hay un 50 % de diferencia. Es el denominador de PD-01: conviene resolverlo *antes* de discutir qué se recorta, no después |

Ninguna de las dos fuentes es evidentemente correcta. D12 es más reciente y su descuento es prudente; el Documento de Planificación es la fuente de la asignación de roles y describe una organización en equipos verticales donde las tres personas tienen alcance funcional asignado. **No hay que elegir la que convenga: hay que preguntarle al equipo cuántas horas de construcción aporta realmente cada persona**, que es un dato que el equipo tiene y ninguno de los dos documentos midió.

---

## N. Orden de construcción recomendado

### N.1 Qué se conserva y qué se corrige del plan del acta

**Se conserva** la instrucción del cliente: primero el motor de adaptación sobre datos cargados a mano, después la gestión de entidades, y dentro de ella alta, baja y edición en ese orden. El fundamento técnico es sólido: construir el motor primero obliga a resolver el modelo de dominio en la primera semana, que es justamente la mitigación de R-04.

**Se corrigen dos defectos del plan del acta:**

1. **El Sprint 2 construye «preajustes»**, que ya no existen. Ese trabajo desaparece.
2. **El Sprint 5 construye la generación asistida**, pero al excluirse los presets **la generación pasó a ser la única vía automática de creación de rutinas**. Dejarla para el quinto sprint significa que durante cuatro sprints no existe ninguna forma de que aparezca una rutina salvo cargarla a mano. Hay que adelantarla.

### N.2 Plan propuesto

| Sprint | Fechas        | Objetivo                                                                                                                                                                            | Entregable demostrable                                                                                                                       |
| ------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | 01/09 – 14/09 | Modelo de dominio congelado · esqueleto desplegado de punta a punta · siembra de datos (RF-071) · diagnóstico y reglas de ajuste (RF-088, RF-089, RF-090)                            | Dado un alumno y una rutina sembrados, el sistema produce una propuesta de adaptación coherente y justificada                                 |
| **2**  | 15/09 – 28/09 | Contexto del alumno · catálogo, taxonomía e inventario · catálogo prescribible · **compatibilidad (RF-086)** · altas                                                                | Una rutina se bloquea porque un ejercicio está contraindicado, y el sistema ofrece alternativas admisibles                                    |
| **3**  | 29/09 – 12/10 | **Generación de la rutina inicial (RF-087, RF-054, RF-055, RF-113)** · autorización completa · revisión y puesta en vigencia (RF-110, RF-091)                                        | Un alumno nuevo se incorpora, recibe una rutina generada y compatible, y su entrenador la aprueba. **Circuito de prescripción cerrado**       |
| **4**  | 13/10 – 26/10 | Ejecución y registro de sesiones (RF-027 a RF-035) · indicadores reales (RF-040 a RF-046) · bajas                                                                                    | El alumno entrena, y el diagnóstico del Sprint 1 corre sobre actividad real en lugar de sembrada                                              |
| **5**  | 27/10 – 09/11 | Cartera y ficha (RF-036, RF-037) · paneles (RF-048, RF-050, RF-051) · alternativas de sustitución (RF-059) · reevaluación por cambio de contexto (RF-094) · ediciones                | **Ciclo completo cerrado sobre datos reales.** Banda N2 completa                                                                              |
| **6**  | 10/11 – 23/11 | Estabilización · regresión generativa (RF-073) · banda N3 si el hito del Sprint 3 se cumplió · documentación y defensa                                                               | Sistema desplegado, medido y demostrable                                                                                                     |

**Diferencia clave con el plan del acta:** el circuito de prescripción cierra en el Sprint 3 en lugar del Sprint 5. A partir de ahí cada sprint agrega evidencia sobre un circuito que ya funciona, en vez de construir piezas que todavía no se pueden conectar.

**Punto de control formal al cierre del Sprint 3:** si el circuito de prescripción no cerró, se activa el orden de retirada de §N.3 antes del Sprint 4, no en la semana 12.

### N.3 Orden de retirada

Escrito de antemano para que la decisión ya esté tomada cuando llegue el momento. Nunca se recorta la banda N1.

| #  | Se retira                                    | Queda en su lugar                            |
| -- | -------------------------------------------- | -------------------------------------------- |
| 1  | RF-067 estado de membresía                   | Nada                                         |
| 2  | RF-064 descripción del perfil                | Nada                                         |
| 3  | RF-052 indicadores agregados de la cartera   | La cartera de RF-036                         |
| 4  | RF-017 y RF-100 catálogo propio del gimnasio | Sólo el catálogo base                        |
| 5  | RF-093 historial de adaptaciones             | Las versiones de rutina siguen consultables  |
| 6  | RF-044 récords personales                    | La evolución de RF-050                       |
| 7  | RF-045 media móvil de mediciones             | La serie sin suavizado                       |
| 8  | RF-031 ajustes durante la sesión             | Registro secuencial de lo prescripto         |
| 9  | RF-014 búsqueda y filtrado                   | Listado completo del catálogo                |
| 10 | RF-072 trazabilidad de salidas               | La justificación de RF-090                   |

**A partir de acá se degradan requisitos de la banda N1, y cada paso exige acuerdo explícito del cliente.** El primero sería RF-055 (explicación en lenguaje natural), sustituida por la presentación tabulada del criterio y los datos — lo que conserva la condición C5 del acta pero pierde la capa narrativa. Retirar cualquier cosa de CAP-7 significa entregar un sistema que no es el que el cliente pidió, y hay que decirlo con esas palabras.

---

## O. Deuda documental: qué hay que actualizar

### O.1 Defectos del corpus, independientes del alcance

Detectados ejecutando la propia herramienta de validación del repositorio y rastreando referencias cruzadas.

| #    | Defecto                                                                                                                                                                                                                                                                                         | Gravedad       | Corrección                                                                                       |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- | ------------------------------------------------------------------------------------------------ |
| DC-1 | **`DD-34` no existe.** Ocho documentos lo citan como fundamento del replanteo de IA (D8, D4, D3, D6, D7, `generative-ai.md`, `predictive-ai.md`, ADR 0008). `design-decisions.md` está en v2.1 y termina en DD-33                                                                                 | **Bloqueante** | Escribir DD-34 en D11 con el contenido que las ocho referencias le atribuyen, y subir D11 a v2.2 |
| DC-2 | **Dos ADR numeradas 0004** con decisiones distintas: `0004-self-hosted-llm-server.md` (25/08) y `0004-servicio-generativo-online-en-el-polo.md` (29/08)                                                                                                                                          | **Bloqueante** | Renumerar la segunda como ADR 0009 y declarar explícitamente su relación con la 0004 y la 0005  |
| DC-3 | **La ADR 0005 contradice a la ADR 0004 (Polo)** y sigue en estado «aceptada» sin declararse reemplazada                                                                                                                                                                                          | **Bloqueante** | §P/PD-04 · marcar la 0005 como parcialmente reemplazada                                          |
| DC-4 | **Nueve documentos no registrados en `manifest.json`** → `python tools/check_docs.py` falla, y con él el workflow `quality.yml` sobre `main`: `ai-model-selection.md`, `generative-ai.md`, `predictive-ai.md`, las ADR 0004 (self-hosted), 0005, 0006, 0007 y 0008, y `deliverable PO/alcance-ia-generativa.md` | **Alta**       | Registrarlos en el manifiesto con alcance, autoridad y `load_when`                                |
| DC-5 | **D13 está en v2.0 y contradice a D8 v3.3**: N-17 declara RF-061 a RF-063 «en MUST» y la capacidad C3 los incluye. Están en WON'T                                                                                                                                                                | Alta           | Subir D13 a v3.0                                                                                 |
| DC-6 | **RNF-05 y RNF-28 siguen nombrando la estimación de riesgo**; `CB-11` describe un caso de una funcionalidad retirada                                                                                                                                                                             | Media          | §L y D10                                                                                         |
| DC-7 | **El entregable al Product Owner salta de la sección 1 a la 3** — falta la sección 2                                                                                                                                                                                                             | Media          | Completar o renumerar                                                                            |
| DC-8 | **`architecture/generative-ai-integration.md` y `architecture/generative-ai.md`** coexisten sin que el manifiesto distinga sus autoridades; sólo el primero está registrado                                                                                                                       | Media          | Declarar la frontera entre ambos o fusionarlos                                                   |

### O.2 Cambios derivados del nuevo alcance

| Documento                                                        | Cambio                                                                                                                                                                                                                                              | Prioridad |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| [D8](../requirements/functional-requirements.md)                 | → v4.0. Reorganizar por capacidades · marcar los veinte diferidos · registrar las cinco fusiones y las cuatro degradaciones · reescribir RF-058 (plantillas, no presets) · retirar RF-119, RF-120, RF-121 y RF-122                                    | **Alta**  |
| [D1](../product/vision-and-objectives.md)                        | §3.2 «los presets del gimnasio permanecen» → plantillas del entrenador · §6 incorporar las exclusiones nuevas · criterios de éxito: retirar los que dependen de lo excluido                                                                          | **Alta**  |
| [D5](../domain/business-rules.md)                                | Retirar §5.2 y RN-124 a RN-129 (candidato) · reescribir RN-95b · retirar las reglas de nutrición · conservar íntegras RN-39a, RN-44a a RN-44d, RN-79a y RN-89a                                                                                       | **Alta**  |
| [D4](../domain/domain-model.md)                                  | → v2.2. Retiradas de §H.2 · `origen` de `RutinaAsignada` con dos valores · declarar los índices                                                                                                                                                      | **Alta**  |
| [D11](../decisions/design-decisions.md)                          | Escribir **DD-34** (DC-1) · marcar **DD-33 derogada para esta etapa** (cae con RF-119) · **DD-13 sin efecto** (nutrición fuera) · nueva **DD-35: la plantilla del entrenador es el piso de disponibilidad de la prescripción**                        | **Alta**  |
| [D12](risks-and-assumptions.md)                                  | R-17 a R-20 · R-03 cerrado · §4 sustituida por §N.3 · nueva aritmética                                                                                                                                                                              | **Alta**  |
| [D13](../requirements/traceability.md)                           | → v3.0. Incorporar la votación como fuente · corregir DC-5 · **agregar N-28: video demostrativo por ejercicio, hoy sin cobertura** (§P/PD-10)                                                                                                        | **Alta**  |
| `architecture/*`                                                 | Retirar la interpretación de lenguaje natural del contrato generativo · sustituir el fallback de presets · alinear con la resolución de PD-04                                                                                                        | **Alta**  |
| `manifest.json`                                                  | DC-4 · registrar este documento                                                                                                                                                                                                                     | **Alta**  |
| [D6](../domain/lifecycles-and-states.md)                         | Retirar el candidato de §1 · sesión sin `desbloqueada hasta` ni `es diferida`                                                                                                                                                                        | Media     |
| [D7](../flows/functional-flows.md)                               | Derogar FL-03 y FL-08 · reescribir FL-04 sin interpretación de lenguaje natural · retirar FL-21                                                                                                                                                      | Media     |
| [D10](../domain/edge-cases.md)                                   | Retirar CB-11, CB-70, CB-72 y CB-73 · agregar los casos agravados de §K.2                                                                                                                                                                           | Media     |
| [D9](../requirements/non-functional-requirements.md)             | Los cambios de §L, incluidos RNF-41 y RNF-42                                                                                                                                                                                                        | Media     |
| [D3](../domain/actors-roles-permissions.md)                      | Retirar de la matriz las filas de comentarios, nutrición y panel del gimnasio                                                                                                                                                                       | Media     |
| [D2](../product/glossary.md)                                     | Retirar «preset» como término con entidad propia · reducir §4.12 a los tipos de aviso que sobreviven                                                                                                                                                | Media     |
| Diagramas                                                        | Casos de uso (desaparecen «Autoasignarse una rutina», «Publicar preset» y «Comentar»; el proceso programado pierde la estimación de riesgo) · modelo de datos · secuencia de generación                                                              | Media     |

---

## P. Decisiones pendientes

Sólo las que requieren decisión humana. No hay respuesta técnica que las cierre.

| #     | Decisión                                                                                                                                                                                                                                                                                       | Quién                | Cuándo                                          |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------- |
| PD-00 | **¿Cuánta capacidad de construcción hay realmente?** D12 dice ~504 h descontando a tres personas; el Documento de Planificación dice que las nueve construyen (I-09). Entre una lectura y otra hay un 50 %. **Es el denominador de PD-01 y hay que resolverlo primero**, midiendo la disponibilidad real declarada por cada integrante, no eligiendo el documento que convenga | Project Manager      | **Antes de PD-01**                              |
| PD-01 | **El alcance sigue por encima de la capacidad.** 57 requisitos de banda N1 contra ~504 h — entre 0,9 × y 1,4 × sólo el núcleo (§D.4). Hay que decidir con el cliente qué se entrega, con §N.3 sobre la mesa. Es la misma conversación que D12/R-01 pide desde hace dos semanas                  | Cliente              | Antes del Sprint 2                              |
| PD-02 | **Baja de cuenta, portabilidad y anonimización (RF-006, RF-105) quedan fuera con 0 votos.** El sistema almacena condiciones físicas, aptitud y mediciones: datos sensibles. Diferirlo es una decisión de exposición, no de alcance funcional, y hay que tomarla explícitamente                  | Cliente y equipo     | Antes del Sprint 2                              |
| PD-03 | **Sin presets, la creación de rutinas depende por completo del servicio generativo.** Confirmar que la plantilla del entrenador es el fallback aceptado, y aceptar que un alumno nuevo, en un gimnasio sin plantillas y con el servicio caído, no obtiene rutina                                | Cliente              | Antes del Sprint 3                              |
| PD-04 | **ADR 0004 (Polo) frente a ADR 0005.** ¿El servicio de IA es un módulo interno del backend o un servicio Python desplegado en el Polo? Recomendación en §H.4                                                                                                                                    | Líder técnico        | **Antes de la primera línea de integración**    |
| PD-05 | **¿Quién opera el Polo?** API, worker, LLM y agente ngrok son cuatro procesos que deben arrancar con la máquina, reiniciarse y exponer salud. Es trabajo no contabilizado en las 504 h                                                                                                          | Equipo e institución | Sprint 1                                        |
| PD-06 | **Escribir DD-34** (DC-1). Ocho documentos apoyan su replanteo de IA en una decisión que no existe                                                                                                                                                                                              | Equipo               | Sprint 1                                        |
| PD-07 | **RF-053 obtuvo 3 de 8 votos pero está comprometido por escrito ante el Product Owner** (`alcance-ia-generativa.md` v2.1). El equipo no lo quiere; el compromiso existe. O el Product Owner libera el compromiso, o RF-053 se construye pese al voto. **No se puede dejar sin resolver: es la única entrada de texto libre del sistema y condiciona RNF-41** | Product Owner        | Antes del Sprint 3                              |
| PD-08 | **RF-049 degradado a barras por grupo muscular.** El documento de planificación lo describe como «diferencial visual y conceptual del producto». La votación le dio 4 de 8                                                                                                                      | Cliente              | Antes del Sprint 5                              |
| PD-09 | **Umbrales y magnitudes de RN-79a y RN-89a.** Son convenciones del equipo sin fundamento externo, y determinan literalmente qué le va a proponer el sistema a una persona. Merecen validación con alguien del oficio                                                                            | Cliente o entrenador | Sprint 2                                        |
| PD-10 | **El video demostrativo por ejercicio (N11 del acta) nunca entró al corpus.** RF-015 pide «al menos un recurso visual»; el cliente mencionó video. Confirmar si el enlace embebido es exigible                                                                                                  | Cliente              | Sprint 2                                        |
| PD-11 | Abiertas de D12 que siguen sin resolver: **I-06** (`READAPTACION` fuera de los tipos de rutina) · **I-07** (base shadow para migraciones sin tocar Neon Test) · **I-08** (operación productiva por ngrok)                                                                                        | Equipo               | I-07 antes de la primera migración              |
| PD-12 | **La votación registra 8 de 9 integrantes.** Quien no votó es la persona que tiene asignado el módulo de IA generativa completo. Conviene confirmar que el recorte de CAP-8 tiene su acuerdo                                                                                                    | Project Manager      | Inmediato                                       |

---

## Anexo · Trazabilidad de la votación

`≥5` aprobado por votación · `DEP` dependencia necesaria · `CLI` autoridad del cliente · `F` absorbido por fusión · `—` fuera de esta etapa

| Planilla    | Requisito (planilla)                    | Votos | Decisión | Resultado en el baseline                                        |
| ----------- | --------------------------------------- | ----- | -------- | --------------------------------------------------------------- |
| RF-001      | Registro de usuarios                    | 8     | ≥5       | RF-001 · alta desde invitación · CAP-1 · N1                     |
| RF-002      | Autenticación y gestión de sesión       | 8     | ≥5       | RF-002 · CAP-1 · N1                                             |
| RF-003      | Recuperación y cambio de credenciales   | 8     | ≥5       | RF-003 · CAP-1 · N2                                             |
| RF-004      | Gestión de roles                        | 8     | F5       | → RF-065                                                        |
| RF-005      | Control de acceso a la información      | 2     | DEP-06   | RF-005 · **fusión con RF-004 rechazada**                        |
| RF-006      | Baja de cuenta y portabilidad           | 0     | —        | Diferido · PD-02 · arrastra RF-105                              |
| RF-007      | Perfil del alumno                       | 8     | ≥5       | RF-007 · CAP-2 · N1                                             |
| RF-008      | Objetivo de entrenamiento               | 8     | ≥5       | RF-008 · CAP-2 · N1                                             |
| RF-009      | Condiciones y restricciones             | 8     | ≥5       | RF-009 más RF-085 · CAP-2 · N1                                  |
| RF-010      | Mediciones corporales                   | 8     | ≥5       | RF-010 · CAP-2 · N1                                             |
| RF-011      | Perfil del entrenador                   | 4     | —        | Fuera                                                           |
| RF-012      | Estimación energética                   | 2     | —        | Fuera · cae toda la nutrición                                   |
| RF-013      | Catálogo de ejercicios                  | 8     | ≥5       | RF-013 · CAP-3 · N1                                             |
| RF-014      | Búsqueda y filtrado                     | 8     | ≥5       | RF-014 · CAP-3 · N2                                             |
| RF-015      | Información descriptiva                 | 8     | ≥5       | RF-015 · CAP-3 · N2 · ver PD-10                                 |
| RF-016      | Clasificación muscular                  | 8     | ≥5       | RF-016 más RF-099 · CAP-3 · N1                                  |
| RF-017      | Ejercicios propios del entrenador       | 5     | ≥5       | RF-017 más RF-100 · CAP-3 · N3                                  |
| RF-018      | Curación y desactivación                | 0     | —        | Fuera · arrastra RF-101 · R-20                                  |
| RF-019      | Plantillas de rutina                    | 8     | ≥5       | RF-019 · **piso de disponibilidad de CAP-4** · N1               |
| RF-020      | Prescripción de series                  | 6     | ≥5       | RF-020 · CAP-4 · N1                                             |
| RF-021      | Publicación de presets                  | 1     | —        | Fuera · confirma la respuesta D4 del acta                       |
| RF-022      | Asignación por copia independiente      | 0     | DEP-01   | **Reincorporado.** Voto nulo por lectura equivocada             |
| RF-023      | Personalización de la rutina asignada   | 1     | F2       | → RF-038                                                        |
| RF-024      | Objetivo de frecuencia semanal          | 2     | DEP-03   | RF-024 · CAP-4 · N1                                             |
| RF-025      | Autoasignación por el alumno            | 3     | —        | Fuera · arrastra RF-119 y RF-120                                |
| RF-026      | Vigencia y archivado                    | 6     | ≥5       | RF-026 · CAP-4 · N1                                             |
| RF-027      | Inicio de sesión de entrenamiento       | 8     | F1       | RF-027 · ciclo de vida completo · N1                            |
| RF-028      | Congelamiento de la prescripción        | 5     | ≥5       | RF-028 · CAP-5 · N1                                             |
| RF-029      | Registro de series ejecutadas           | 8     | ≥5       | RF-029 · CAP-5 · N1                                             |
| RF-030      | Precarga de valores de referencia       | 1     | DEP-08   | RF-030 · sostiene RNF-07                                        |
| RF-031      | Ajustes durante la sesión               | 6     | ≥5       | RF-031 · CAP-5 · N2                                             |
| RF-032      | Reanudación de sesiones                 | 3     | F1       | → RF-027                                                        |
| RF-033      | Finalización de sesión                  | 7     | F1       | → RF-027                                                        |
| RF-034      | Registro y corrección diferidos         | 2     | —        | Fuera · arrastra RF-117 · R-19                                  |
| RF-035      | Historial de entrenamientos             | 8     | ≥5       | RF-035 · CAP-5 · N1                                             |
| RF-036      | Cartera priorizada                      | 5     | F4       | RF-036 · absorbe RF-107 · N1                                    |
| RF-037      | Ficha integral del alumno               | 8     | ≥5       | RF-037 · CAP-8 · N1                                             |
| RF-038      | Intervención sobre la rutina            | 7     | F2       | RF-038 · absorbe RF-023 · N1                                    |
| RF-039      | Comentarios de seguimiento              | 1     | —        | Fuera · agrava R-09                                             |
| RF-040      | Volumen y frecuencia por grupo muscular | 8     | ≥5       | RF-040 · CAP-6 · N1                                             |
| RF-041      | Capacidad máxima estimada               | 8     | ≥5       | RF-041 · CAP-6 · N1                                             |
| RF-042      | Adherencia al plan                      | 5     | ≥5       | RF-042 · CAP-6 · N1                                             |
| RF-043      | Cumplimiento de la prescripción         | 0     | DEP-02   | **Reincorporado.** Sin él el diagnóstico pierde dos situaciones |
| RF-044      | Récords personales                      | 6     | ≥5       | RF-044 · CAP-6 · N2                                             |
| RF-045      | Evolución de mediciones                 | 8     | ≥5       | RF-045 · CAP-6 · N2                                             |
| RF-046      | Señales de seguimiento                  | 7     | ≥5       | RF-046 · CAP-6 · N1                                             |
| RF-047      | Parametrización de reglas               | 3     | —        | Fuera · constantes documentadas                                 |
| RF-048      | Panel de progreso del alumno            | 8     | ≥5       | RF-048 · absorbe la presentación de RF-040 en barras · N2       |
| RF-049      | Representación muscular                 | 4     | —        | **Degradado** a barras dentro de RF-048 · PD-08                 |
| RF-050      | Evolución por ejercicio                 | 8     | ≥5       | RF-050 · CAP-6 · N2                                             |
| RF-051      | Ante información insuficiente           | 7     | ≥5       | RF-051 · CAP-6 · N1                                             |
| RF-052      | Panel agregado del entrenador           | 8     | ≥5       | RF-052 · CAP-6 · N3                                             |
| RF-053      | Interpretación de lenguaje natural      | 3     | Compromiso PO | **Conservado pese a no alcanzar el corte** · §F.2b · PD-07 |
| RF-054      | Generación asistida de rutinas          | 8     | ≥5       | RF-054 · **fusión con RF-055 rechazada**                        |
| RF-055      | Justificación de la propuesta generada  | 8     | ≥5       | RF-055 · componente narrativo separado                          |
| RF-056      | Resumen periódico del progreso          | 4     | —        | Fuera · ya sustituido por RF-090                                |
| RF-057      | Restricciones del contenido generado    | 0     | DEP-05   | **Reincorporado.** MUST* en la propia planilla                  |
| RF-058      | Continuidad ante indisponibilidad       | 1     | DEP-04   | **Reincorporado y reescrito** · §F.4                            |
| RF-059      | Recomendación de sustitutos             | 8     | F3       | RF-059 · absorbe RF-060 · N1                                    |
| RF-060      | Condicionamiento de recomendaciones     | 2     | F3       | → RF-059 · exclusión dura                                       |
| RF-061      | Riesgo de abandono                      | 1     | —        | Fuera · la votación confirma el WON'T de v3.3                   |
| RF-062      | Explicabilidad de la estimación         | 0     | —        | Fuera                                                           |
| RF-063      | Actualización de estimaciones           | 0     | —        | Fuera                                                           |
| RF-064      | Segmentación de perfiles                | 6     | ≥5       | RF-064 · efímero, generativo · N3                               |
| RF-065      | Gestión de usuarios y roles             | 6     | F5       | RF-065 · absorbe RF-004 (8 votos) · N1                          |
| RF-066      | Asignaciones entrenador–alumno          | 2     | DEP-07   | **Reincorporado.** Sujeto de la puerta                          |
| RF-067      | Estado de membresía                     | 8     | ≥5       | RF-067 · informativo · N3                                       |
| RF-068      | Panel analítico del gimnasio            | 2     | —        | Fuera                                                           |
| RF-069      | Ámbito por gimnasio                     | 4     | DEP-06   | **Reincorporado.** Aislamiento                                  |
| RF-070      | Carga inicial del catálogo              | 8     | ≥5       | RF-070 · CAP-3 · N1                                             |
| RF-071      | Datos de demostración                   | 3     | DEP-09   | **Reincorporado.** Autorizado por el cliente                    |
| RF-072      | Trazabilidad de resultados inteligentes | 0     | DEP-16   | Reincorporado con alcance reducido                              |
| RF-073      | Evaluación de componentes inteligentes  | 0     | DEP-17   | **Transformado** en regresión generativa                        |
| RF-074      | Indicador nutricional diario            | 1     | —        | Fuera                                                           |
| RF-075..081 | Exclusiones ya evaluadas                | 0     | —        | Se confirman                                                    |
| RF-082..094 | Requisitos nuevos del cliente           | —     | CLI      | Todos en alcance · CAP-4 y CAP-7 · §D.3                         |
| RF-095..118 | Derivados del análisis del corpus       | —     | DEP o —  | Individualmente justificados en §G                              |
| RF-119..122 | Candidato ajustable e IA predictiva     | —     | —        | Fuera · §F.1 y §F.3                                             |

---

**Este documento no es normativo hasta que el equipo lo vote y el cliente resuelva PD-01.** Hasta entonces, la referencia de alcance sigue siendo D8 v3.3.
