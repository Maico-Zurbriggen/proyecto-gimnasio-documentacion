# D6 — Ciclos de vida y estados

|                |            |
| -------------- | ---------- |
| **Versión**    | 2.4        |
| **Fecha**      | 2026-09-02 |
| **Estado**     | Normativo  |
| **Depende de** | D2, D4, D5 |

**Cambios de la v2.2:** §10 — la estimación de riesgo y la segmentación se retiran del alcance ([D11/DD-34](../decisions/design-decisions.md)); la descripción de perfil (RF-064) es efímera y no genera registros.

**Cambios de la v2.3 ([baseline de alcance](../planning/baseline-alcance-2026-09.md)).** Ningún autómata cambia. Lo que cambia es qué transiciones existen en la Etapa 1:

- **El candidato de rutina no existe en esta etapa.** Se declaraba en §1 como objeto explícitamente fuera del ciclo de vida, para que nadie lo resolviera agregando un estado `BORRADOR`. Al diferirse RF-119 y RF-025, **la advertencia sigue valiendo con más fuerza**: la salida de una generación se convierte directamente en rutina `PROPUESTA`, y sigue sin haber un estado intermedio.
- **La sesión conserva sus cuatro transiciones** —iniciar, reanudar, cerrar por inactividad, finalizar—, ahora reunidas bajo un único requisito (RF-027 absorbe RF-032 y RF-033). El autómata de §4 es la especificación de ese requisito y no se toca.
- **La sesión pierde el desbloqueo por el entrenador** (RF-117, diferido con RF-034): el plazo de corrección vuelve a ser absoluto, con el coste que CB-70 describía.
- **`RutinaAsignada.origen` pierde `PRESET_ELEGIDO_POR_ALUMNO`**: quedan `PLANTILLA_ENTRENADOR` y `GENERADA`.

**Cambios de la v2.4 (baseline v4.0 confirmada).** Se retiran del detalle el candidato técnico, el desbloqueo de sesiones y la baja de usuario. Las solicitudes e intentos generativos conservan sus estados técnicos; una salida validada origina directamente una rutina `PROPUESTA`.

**Cambios de la v1.0:** ciclo de la invitación · estado `DESCARTADA` de rutina, que faltaba y dejaba indefinido un caso frecuente · desbloqueo excepcional de sesión · aclaración de que una versión nueva no transiciona la rutina · corrección del diagrama de rutina, cuya flecha de rechazo apuntaba al estado equivocado.

**Cambios de la v2.0:** se declara que el **candidato de rutina** (D5/RN-124) no es un estado de este ciclo, y por qué no se agrega uno.

**Cambios de la v2.1:** se incorporan los estados técnicos de solicitudes, intentos y candidatos generativos, separados del ciclo de vida de la rutina.

Las transiciones prohibidas importan tanto como las permitidas: cada una evita un defecto que de otro modo aparece en producción.

---

## 1. Invitación

```
   emitida ──▶ VIGENTE ──┬──▶ USADA      (terminal, produce un usuario)
                         ├──▶ REVOCADA   (terminal, decisión del emisor)
                         └──▶ CADUCADA   (terminal, 14 días)
```

| Estado   | Significado                                                | Quién provoca la entrada                   |
| -------- | ---------------------------------------------------------- | ------------------------------------------ |
| VIGENTE  | Habilita a crear una cuenta en ese gimnasio con esos roles | Administrador, o entrenador con rol ALUMNO |
| USADA    | Ya produjo un usuario                                      | La persona invitada                        |
| REVOCADA | Anulada antes de usarse                                    | Administrador o el emisor                  |
| CADUCADA | Venció sin usarse                                          | Sistema, a los 14 días (RN-02b)            |

**Transiciones imposibles:** usar dos veces la misma invitación (RI-19) · revocar o caducar una invitación ya usada, porque el usuario ya existe y su alta no se deshace: para retirarlo se suspende o se da de baja la cuenta · modificar los roles de una invitación ya usada, porque cambiarían los permisos de un usuario existente sin auditarlo como cambio de rol.

## 2. Rutina

```
   solicitud (entrenador, alumno o generación)
                  │
                  ▼
            ┌───────────┐  revisión desfavorable   ┌────────────┐
            │ PROPUESTA │ ────────────────────────▶│ RECHAZADA  │ (terminal)
            └─────┬─────┘                          └────────────┘
   revisión       │  │
   favorable      │  └── otra solicitud ──▶ ┌────────────┐
                  │                          │ DESCARTADA │ (terminal)
                  ▼                          └────────────┘
            ┌───────────┐
            │  VIGENTE  │◀── (una versión nueva NO transiciona la rutina)
            └─────┬─────┘
   otra rutina    │
   entra en       ▼
   vigencia  ┌────────────┐
             │ ARCHIVADA  │ (terminal)
             └────────────┘

            ┌────────────┐   el alumno queda sin entrenador vigente
            │ BLOQUEADA  │◀──────────── desde PROPUESTA
            └─────┬──────┘
                  └──▶ vuelve a PROPUESTA al reasignarse un entrenador
```

| Estado     | Significado                                                                           | Quién provoca la entrada                                                                                   |
| ---------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| PROPUESTA  | Rutina completa asociada al alumno, sin efecto. Visible para el alumno, no ejecutable | Entrenador, alumno al **confirmar** una rutina generada —o un preset opcional—, sistema (RF-087)            |
| BLOQUEADA  | Propuesta sin aprobador porque el alumno no tiene entrenador vigente                  | Sistema, al finalizar la asignación (RN-23)                                                                |
| VIGENTE    | Rutina bajo la cual el alumno puede iniciar sesiones                                  | Entrenador, mediante revisión favorable                                                                    |
| RECHAZADA  | Revisión desfavorable, con motivo. El alumno puede solicitar otra                     | Entrenador                                                                                                 |
| DESCARTADA | Fue sustituida por otra solicitud antes de ser revisada                               | Quien solicitó la nueva (RN-36a)                                                                           |
| ARCHIVADA  | Fue vigente y otra la sustituyó. Consultable, no ejecutable                           | Sistema                                                                                                    |

**El candidato de rutina no es un estado.** Lo que el solicitante ajusta antes de enviar a revisión (RN-124, D5/§5.2) no es una `RutinaAsignada`: no se persiste como rutina, no transiciona y desaparece si no se confirma. La rutina nace directamente en PROPUESTA, al confirmarse el candidato. **No se agrega un estado BORRADOR**: sería un estado sin efecto, sin aprobador y sin historial que preservar, y obligaría a decidir qué hacer con los borradores que nadie confirma. Ver D11/DD-33.

**Transiciones imposibles**

| Transición                                                                         | Por qué                                                                                                                             |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| PROPUESTA → VIGENTE sin revisión favorable de un entrenador con asignación vigente | RN-35. Es la regla que el cliente definió como indelegable                                                                          |
| RECHAZADA o DESCARTADA → cualquier estado                                          | Terminales. Para volver a intentarlo se solicita una rutina nueva, y así el historial muestra cada intento por separado             |
| ARCHIVADA → VIGENTE                                                                | Reactivarla reabriría el cálculo de adherencia de un período cerrado. Se solicita una nueva a partir de la misma plantilla          |
| VIGENTE → RECHAZADA o → PROPUESTA                                                  | Lo que ya rige no se rechaza ni vuelve a estar pendiente: se sustituye poniendo otra en vigencia, o se ajusta generando una versión |
| Dos rutinas VIGENTE, o dos PROPUESTA, del mismo alumno                             | RI-06                                                                                                                               |
| BLOQUEADA → VIGENTE                                                                | Requiere pasar por PROPUESTA, es decir, requiere entrenador                                                                         |

**Una adaptación aceptada no transiciona la rutina.** Genera una versión nueva (§3) y la rutina sigue VIGENTE. La resolución de la propuesta por el entrenador **es** la revisión exigida por RN-35, y no se pide una segunda (RN-35a).

## 3. Versión de rutina

```
   puesta en vigencia ──▶ VERSIÓN 1 (vigente)
                                │
        propuesta aceptada, o   │
        intervención directa    ▼
                          VERSIÓN 2 (vigente) · VERSIÓN 1 → SUPERSEDIDA
```

| Estado      | Significado                                                 |
| ----------- | ----------------------------------------------------------- |
| VIGENTE     | Estructura que rige hoy. Exactamente una por rutina (RI-07) |
| SUPERSEDIDA | Estructura que rigió en un período. Inmutable y consultable |

**Transiciones imposibles:** modificar una versión SUPERSEDIDA, que reescribiría el pasado bajo el cual se ejecutaron sesiones · volver a marcar vigente una versión anterior, en su lugar se genera una versión nueva con el contenido anterior para que el historial sea lineal y fechado · crear una versión sin propuesta resuelta ni intervención registrada de un entrenador, porque toda versión tiene autor y motivo.

## 4. Sesión de entrenamiento

```
   inicio                 finalización              48 h
 ──────────▶ EN_CURSO ──────────────▶ COMPLETADA ────────▶ BLOQUEADA
                 │
                 │ 8 h sin actividad
                 ▼
            ABANDONADA (terminal)
```

| Estado     | Significado                                                     | Cuenta para indicadores              |
| ---------- | --------------------------------------------------------------- | ------------------------------------ |
| EN_CURSO   | Iniciada, con prescripción congelada, admite registro de series | No                                   |
| COMPLETADA | Finalizada por el alumno. Corregible durante 48 h (RN-58)       | Sí                                   |
| ABANDONADA | Cerrada por inactividad. Conserva lo registrado                 | No, salvo como señal de interrupción |
| BLOQUEADA  | Completada y fuera del plazo de corrección                      | Sí                                   |

**Transiciones imposibles**

| Transición                                                          | Por qué                                                                                                        |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| ABANDONADA → EN_CURSO                                               | Es un estado terminal; la Etapa 1 no admite registrar sesiones diferidas                                      |
| COMPLETADA → EN_CURSO                                               | El estado en curso implica una prescripción abierta; corregir no es reabrir                                    |
| BLOQUEADA → COMPLETADA                                              | RF-117 está diferido; el plazo de corrección de 48 horas es absoluto                                           |
| Dos sesiones EN_CURSO del mismo alumno                              | RN-50                                                                                                          |
| Iniciar una sesión en tiempo real sobre una rutina no VIGENTE       | RN-51                                                                                                          |
| Modificar la prescripción congelada, en cualquier estado            | RN-61                                                                                                          |

**Sobre ABANDONADA.** Sus series registradas se conservan y son visibles en el historial, marcadas como tales. Descartarlas perdería evidencia de interrupción, que es una señal de comportamiento relevante para el diagnóstico.

## 5. Propuesta de adaptación

```
   diagnóstico ──▶ PENDIENTE ──┬──▶ ACEPTADA_TOTAL      ─▶ genera versión
                       │        ├──▶ ACEPTADA_PARCIAL    ─▶ genera versión
                       │        ├──▶ RECHAZADA           ─▶ no genera versión
                       │        └──▶ INVALIDADA          ─▶ el contexto cambió
                       │
                       ├── 30 días sin resolver ──▶ CADUCADA
                       └── alumno sin entrenador ──▶ BLOQUEADA ──▶ vuelve a PENDIENTE
```

| Estado                            | Significado                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| PENDIENTE                         | Esperando la revisión del entrenador                                                                                   |
| BLOQUEADA                         | Sin aprobador por falta de asignación vigente                                                                          |
| ACEPTADA_TOTAL / ACEPTADA_PARCIAL | Resuelta favorablemente. Generó una versión nueva                                                                      |
| RECHAZADA                         | Resuelta desfavorablemente, con motivo registrado                                                                      |
| INVALIDADA                        | El contexto del alumno cambió y la propuesta dejó de ser compatible antes de resolverse. Se genera una propuesta nueva |
| CADUCADA                          | Venció sin resolución. El hecho se registra                                                                            |

**Transiciones imposibles:** aplicarse sin resolución favorable (RN-86, el principio central del producto) · resolverla el propio alumno (RA-07) · reabrir una propuesta resuelta, caducada o invalidada, porque el historial de adaptaciones sería ininterpretable si las propuestas mutaran · generar dos versiones a partir de una misma propuesta.

## 6. Ejercicio del catálogo

```
  carga inicial ─────────────────────────▶ APROBADO ⇄ DESACTIVADO
  creación por entrenador ──▶ PROPUESTO ───┤
                                           └──▶ RECHAZADO (terminal)
```

| Estado      | Visible en búsquedas           | Prescribible                                                       |
| ----------- | ------------------------------ | ------------------------------------------------------------------ |
| PROPUESTO   | Sólo para su autor             | No                                                                 |
| APROBADO    | Sí                             | Sí, si su equipamiento está en el inventario del gimnasio (RN-116) |
| RECHAZADO   | Sólo para su autor, con motivo | No                                                                 |
| DESACTIVADO | No                             | No, pero permanece en rutinas y sesiones existentes (RN-29)        |

**Transiciones imposibles:** borrado físico en cualquier estado (RN-27) · modificación de un ejercicio del catálogo base por cualquier usuario (RN-24) · desactivación que altere registros históricos que lo referencian.

## 7. Estado de compatibilidad de un ejercicio dentro de una rutina

No es un ciclo de vida sino una **clasificación recalculada** en cada verificación (RN-45), persistida para que la marca esté disponible sin recalcular.

| Valor                 | Se asigna cuando                                                                                                          | Efecto                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| COMPATIBLE            | Ninguna regla de D5/§6 lo objeta                                                                                          | Ninguno                                                          |
| ADVERTIDO             | Contraindicado por una condición de severidad `LEVE`                                                                      | Se señala; no impide                                             |
| INCOMPATIBLE          | Contraindicado con severidad `MODERADA` o `SEVERA`, o nivel superior al del alumno, o equipamiento ausente del inventario | Impide poner la rutina en vigencia; genera ajuste de sustitución |
| EJERCICIO_DESACTIVADO | El ejercicio fue desactivado del catálogo                                                                                 | Se señala; puede ejecutarse; genera ajuste de sustitución        |

**Nunca se retira un ejercicio automáticamente por cambiar su estado de compatibilidad.** Retirarlo es decisión del entrenador (RN-92).

## 8. Asignación entrenador–alumno

| Estado     | Significado                                                  |
| ---------- | ------------------------------------------------------------ |
| VIGENTE    | `hasta` sin informar. Habilita todo el acceso del entrenador |
| FINALIZADA | `hasta` informado. Terminal e inmutable                      |

**Transiciones imposibles:** reactivar una asignación finalizada, en su lugar se crea una nueva para que el historial refleje la discontinuidad · dos asignaciones vigentes del mismo alumno (RN-18) · una asignación de un entrenador consigo mismo (RN-22).

## 9. Usuario

```
   ACTIVO ⇄ SUSPENDIDO
```

| Estado     | Puede autenticarse | Sus datos                                                             |
| ---------- | ------------------ | --------------------------------------------------------------------- |
| ACTIVO     | Sí                 | Íntegros                                                              |
| SUSPENDIDO | No                 | Íntegros. Las asignaciones no se alteran: la suspensión es reversible |

**Transiciones imposibles:** suspender destruyendo asignaciones · suspender al último administrador activo del gimnasio (RN-03a, RI-23). La baja y anonimización de cuenta están diferidas con RF-006 y RF-105; sus estados se agregarán si vuelven al alcance.

## 10. Entidades sin ciclo de vida

**Aptitud.** Su condición es derivada de la fecha: vigente si su vencimiento no fue superado, vencida en caso contrario, ausente si no hay ninguna registrada. Se modela como derivada y no como estado persistido porque un estado persistido exigiría un proceso que lo actualice, y quedaría desactualizado exactamente el día que importa. **Los tres casos se distinguen siempre** y nunca se colapsan en "no tiene aptitud": ausente y vencida requieren acciones distintas.

**Diagnóstico y salidas fechadas de un componente.** Cada cálculo produce un registro nuevo, fechado y con la versión del componente. No se actualizan ni se borran. El vigente es el de fecha más reciente. **Si nunca se ejecutó ningún cálculo**, la información se presenta como no disponible y ninguna funcionalidad se degrada (RNF-12). Ése es el caso normal el primer día del sistema, no una anomalía. *(La estimación de riesgo de abandono y la segmentación se retiraron del alcance — D11/DD-34; la descripción de perfil, RF-064, es efímera y no genera registros.)*

**Récord personal.** Tiene un indicador de vigencia, no estados: un récord deja de ser vigente cuando otro lo supera, o cuando el recálculo de RN-71 lo desplaza. Los superados se conservan para poder dibujar la progresión.

## 11. Solicitud e intento generativos

### Solicitud generativa

```text
PENDIENTE → PROCESANDO ─┬→ COMPLETADA
     ▲                  ├→ NO_DISPONIBLE
     └─ lease vencido ──┘

PENDIENTE o PROCESANDO → CANCELADA
```

| Estado         | Significado |
| -------------- | ----------- |
| PENDIENTE      | Disponible para que un worker la reclame |
| PROCESANDO     | Reclamada mediante un lease temporal |
| COMPLETADA     | Tiene un resultado estructural que backend puede validar |
| NO_DISPONIBLE  | Agotó dos intentos sin resultado válido |
| CANCELADA      | El solicitante abandonó antes de obtener un resultado utilizable |

Un lease vencido devuelve la solicitud a `PENDIENTE` sin perder el intento registrado. `COMPLETADA`, `NO_DISPONIBLE` y `CANCELADA` son terminales.

### Intento generativo

```text
PENDIENTE → PROCESANDO ─┬→ COMPLETADO
                        ├→ FALLIDO
                        ├→ AGOTADO_POR_TIEMPO
                        └→ SALIDA_INVALIDA
```

Cada solicitud admite como máximo dos intentos. Los cuatro estados de salida son terminales para el intento; tras el primer fallo la solicitud vuelve a `PENDIENTE`, y tras el segundo pasa a `NO_DISPONIBLE`. Una salida completada que supera la validación del backend origina directamente una rutina `PROPUESTA`; no existe un candidato persistido intermedio.
