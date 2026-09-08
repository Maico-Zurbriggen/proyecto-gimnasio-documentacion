# Contexto del alumno — registro, actualización y uso en IA

|                |                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Versión**    | 1.3                                                                                                              |
| **Fecha**      | 2026-09-08                                                                                                       |
| **Estado**     | Propuesto                                                                                                        |
| **Depende de** | [D2](../product/glossary.md), [D4](domain-model.md), [D5](business-rules.md), [D8](../requirements/functional-requirements.md), [ia-etapa1](../architecture/ia-etapa1.md) |

Define qué datos componen el contexto del alumno, cómo se captan (cerrado + abierto), cómo se mantienen vigentes y cómo viajan a la IA. No redefine entidades ni reglas: el modelo vive en [D4](domain-model.md) y las reglas en [D5](business-rules.md); aquí el ciclo de vida del dato.

**Cambios de la v1.1:** se detallan campos cerrados con sus opciones (con puntero canónico a D2), dueño de cada dato, el flujo de registro en tres pasos a nivel UX, la matriz de actualización por ritmo, las preferencias opcionales por generación y el contrato del Context Builder con el prompt.

**Cambios de la v1.2:** se agregan las **observaciones generales** del alumno (al registrarse, §2.7) y las **observaciones del pedido** (al generar, §6): texto libre que el modelo sí ingiere, pero **sólo por la puerta de `interpretarPedido`** (RNF-41) — se traducen a parámetros estructurados, se confirman con el usuario y recién entonces alimentan `generarRutina`. El texto crudo nunca viaja directo a generación.

**Cambios de la v1.3:** las preferencias estables (§2.6) se dividen en tres campos: **ejercicios a evitar** (exclusión dura, ya existía), **ejercicios favoritos** (preferencia blanda, nuevo) y **grupos musculares a priorizar** (énfasis, nuevo). Los dos nuevos son multiselect cerrados —no texto libre— porque nombran elementos que el sistema ya enumera (catálogo, D2/§4.2): viajan tipados directo a `generarRutina` sin interpretación. Las observaciones generales quedan como residual abierto.

> Convención: los valores de cada enumeración se listan aquí como lectura rápida. Ante cualquier discrepancia, el canónico es [D2](../product/glossary.md) §4.

## 1. Principios

1. **Cerrado calcula, abierto se interpreta y confirma.** Todo lo que una regla consume (compatibilidad, rangos, adherencia) es enumeración o número. El texto libre del alumno llega al modelo **sólo por `interpretarPedido`** (RNF-41): se traduce a parámetros de enumeraciones cerradas, se confirman con el usuario y recién entonces alimentan la generación. El texto crudo nunca entra a un cálculo, a `generarRutina` ni a logs persistentes (RNF-19).
2. **Tres pasos, uno obligatorio** (RNF-08): cuenta y mínimo decidible el día uno; el resto progresivo.
3. **Nada que no alimente el ciclo.** Si un campo no lo consume una regla (D5), el generador (FL-04) o un indicador, no existe.
4. **Vigencia, no mutación.** Objetivo, condiciones, asignación y versiones ya tienen historial; peso y mediciones son series fechadas. El pasado se reinterpreta, no se reescribe (baseline §I).
5. **Tipado o no viaja.** Un campo nuevo en el modelo no llega al LLM hasta que el Context Builder lo incluya explícitamente (§7).

## 2. Estructura cerrada (calcula)

Cada fila indica quién la declara y en qué paso del registro se pide (§4). Rangos en [D5](business-rules.md) RN-17, RN-38, RN-43, RN-55.

### 2.1 Cuenta e identidad (fijos, paso 1)

| Campo | Tipo / opciones | Dueño y edición |
| ----- | --------------- | --------------- |
| Nombre para mostrar | texto libre corto (identificatorio, no clínico) | Alumno al registrarse; corrección por administrador |
| Contraseña | credencial (hasheada, nunca al contexto IA) | Alumno |
| Consentimiento de datos de salud | checkbox separado, con texto aceptado conservado (RN-104, RF-096) | Alumno; sin él no hay condiciones ni mediciones (FL-19/A2) |

### 2.2 Mínimo decidible (paso 1, obligatorio)

Sin estos tres más la declaración de condiciones (§2.3) no hay contexto suficiente (RF-111, RN-97b) y no se genera rutina.

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Objetivo vigente | D2/§4.5, 4 valores: `FUERZA` · `HIPERTROFIA` · `RESISTENCIA_MUSCULAR` · `ACONDICIONAMIENTO_GENERAL` | Uno vigente como máximo; declarar uno nuevo cierra el anterior (RN-09). `ACONDICIONAMIENTO_GENERAL` es compatible con cualquier tipo de rutina (RN-40) |
| Nivel de experiencia | D2/§4.4, ordenado: `PRINCIPIANTE` < `INTERMEDIO` < `AVANZADO` | Limita ejercicios prescribibles por dificultad (RN-44c). Vale también para el nivel de dificultad del ejercicio |
| Días disponibles/semana | entero 1–7 | Referencia de frecuencia; la rutina declara su propia frecuencia objetivo 1–7 (RN-38) |

### 2.3 Condiciones físicas (paso 1, declarar incluso "ninguna")

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Zona corporal | D2 zona = §4.2 ∪ §4.3, 25 valores: 17 grupos (`PECTORAL`, `DELTOIDES_ANTERIOR`, `DELTOIDES_LATERAL`, `BICEPS`, `ANTEBRAZO`, `ABDOMINALES`, `OBLICUOS`, `CUADRICEPS`, `ADUCTORES`, `DORSAL`, `TRAPECIO`, `DELTOIDES_POSTERIOR`, `TRICEPS`, `ERECTORES_LUMBARES`, `GLUTEO`, `ISQUIOTIBIALES`, `GEMELOS`) + 8 articulaciones (`HOMBRO`, `CODO`, `MUNECA`, `COLUMNA_CERVICAL`, `COLUMNA_LUMBAR`, `CADERA`, `RODILLA`, `TOBILLO`) | Es lo que hace calculable la contraindicación (RN-44a) |
| Severidad | D2/§4.6: `LEVE` (advierte) · `MODERADA` (impide) · `SEVERA` (impide) | Efecto en RN-44b |
| Vigencia | `desde` (fecha, obligatoria) / `hasta` (fecha, vacía = vigente) | Varias vigentes a la vez (RN-10); el cierre no reabre el pasado (RN-11) |
| Descripción libre | texto corto complementario | **No participa de ningún cálculo** (RN-10a); el matiz narrativo vive en §3 |

Declarar "no tengo ninguna" es una declaración positiva y cuenta para el contexto suficiente (FL-01/A1). No es lo mismo que no haber contestado.

### 2.4 Perfil corporal y de entrenamiento (paso 2)

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Fecha de nacimiento | fecha pasada | Base de edad para Mifflin-St Jeor si vuelve nutrición (§13 diferido); corrección por admin |
| Sexo | enum cerrado del sistema | Idem anterior |
| Altura | 100–250 cm (RN-17) | Corrección por admin |
| Peso actual | 20,0–400,0 kg, 1 decimal (RN-17); es la **primera medición** de la serie `PESO_CORPORAL` | Luego vive como serie fechada (§5) |
| Años entrenando | número ≥ 0 | Calibra la primera carga sugerida y la lectura del entrenador; no entra a reglas |
| Actividad anterior | texto corto (p. ej. "fútbol 2 años", "nada") | Idem; orienta, no calcula |
| Duración por sesión | minutos, entero | Acota la cantidad de ejercicios por día que el generador puede proponer |

### 2.5 Evidencia y aptitud (paso 3)

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Mediciones por tipo y fecha | D2/§4.11, 6 tipos: `PESO_CORPORAL` · `PERIMETRO_CINTURA` · `PERIMETRO_CADERA` · `PERIMETRO_BRAZO` · `PERIMETRO_MUSLO` · `PERIMETRO_PECHO`; única por (tipo, fecha) (RN-15); sin fecha futura (RN-16); perímetros 10,0–250,0 cm | Serie fechada; alimenta e1RM, volumen relativo y proyección. Evolución con media móvil 7 días (RF-045) |
| Aptitud (apto físico) | fecha de emisión + fecha de vencimiento + observación; la carga el alumno o un administrador (RN-13a) | Ausencia/vencimiento **advierte, nunca impide** (RN-13); avisos `APTITUD_POR_VENCER` 30 días antes y el día del vencimiento (RN-13b) |

### 2.6 Preferencias estables (paso 3)

Tres campos que expresan gusto y prioridad duraderos. Se editan en cualquier momento y rigen para la próxima generación. Precedencia fija: **compatibilidad (RN-44a–d) > ejercicios a evitar > favoritos y prioridades**, que son blandas: si no se pueden satisfacer, se declara y se genera igual, nunca se viola un rango ni una incompatibilidad para cumplir un gusto.

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Ejercicios a evitar | multiselect sobre el catálogo prescribible del gimnasio | **Exclusión dura y duradera** (disgusto, incomodidad histórica). Entra a cada generación como exclusión; equivale al "no me gustan" estable |
| Ejercicios favoritos | multiselect sobre el catálogo prescribible, hasta 10 `[S]` | **Preferencia blanda**: el generador prefiere incluirlos dentro del conjunto compatible. Si un favorito es incompatible (nivel, condición, inventario), se excluye y se declara — el gusto nunca vence a RN-44a–d |
| Grupos musculares a priorizar | multiselect sobre D2/§4.2 (17 valores), hasta 5 `[S]` | **Énfasis de volumen** ("quiero hacer crecer piernas"): sesga la construcción hacia esos grupos **dentro** de los máximos por tipo (RN-39a) y los rangos de desbalance (RN-76). No crea volumen sobre el máximo ni corrige un desbalance por exceso ajeno |

Si el inventario del gimnasio cambia y un ejercicio favorito o evitado deja de ser prescribible, se conserva marcado pero sin efecto hasta que vuelva al catálogo; no se borra solo.

### 2.7 Observaciones generales (abierto que sí alimenta al modelo)

| Campo | Tipo / opciones | Notas |
| ----- | --------------- | ----- |
| Observaciones generales | texto libre, opcional, hasta 1000 caracteres `[S]`, editable siempre (paso 3 y luego desde el perfil) | Residual abierto: lo que el alumno quiera que el modelo tenga en cuenta y **no tiene campo propio** — horarios reales, miedos, motivaciones ("quiero llegar bien al verano"), contexto de vida, lesiones viejas narradas. Los gustos por ejercicios y los músculos a desarrollar tienen sus campos en §2.6 y no se repiten acá. **Ingesta (§7.4):** entra a `interpretarPedido` junto al pedido, que extrae parámetros estructurados (foco, exclusiones, patrón, duración, frecuencia); el alumno los confirma y sólo lo confirmado llega a `generarRutina`. El texto crudo no se persiste en logs (RNF-19); el snapshot conserva los parámetros confirmados y el hash del texto origen (RN-98) |

Límite de longitud y truncado visible: si supera los 1000 caracteres se rechaza con el límite en el mensaje, no se corta en silencio.

### 2.8 Lo que no existe (y por qué)

Equipamiento del alumno (D4/PD-07: prescribe el inventario del gimnasio) · DNI, domicilio (RN-105) · nutrición, sueño/estrés (sin consumidor en el ciclo Etapa 1) · nivel de actividad (diferido con RF-012).

## 3. Estructura abierta (dos destinos)

El texto libre tiene dos destinos con reglas distintas. Las **observaciones generales** (§2.7) y las **del pedido** (§6) las ingiere el modelo por `interpretarPedido`. Los dos textos de abajo son sólo para el entrenador y **jamás se serializan a ningún prompt** (privacidad + RN-94):

1. **Comentario para tu entrenador** (paso 3, opcional, editable): contexto humano — miedos, gustos, lesiones viejas narradas, horarios reales, qué le motiva.
2. **Nota por condición** (opcional, junto a cada condición): matiz que la terna zona/severidad/desde no captura ("me duele al bajar, no al subir").

El entrenador los lee en la ficha consolidada (RF-037) y puede traducirlos a datos cerrados (p. ej. agregar una condición o un ejercicio a evitar). El sistema nunca los interpreta solo. Una molestia contada en sesión tampoco se registra como condición por cuenta propia: se sugiere declararla (FL-06/E2, CB-23).

## 4. Flujo de registro (FL-01)

Tres pasos progresivos, un solo obligatorio (RNF-08):

1. **Paso 1 — obligatorio: cuenta + mínimo decidible.** Nombre, contraseña, consentimiento de salud; objetivo, nivel, días; condiciones o "ninguna". Al completarlo, el sistema evalúa contexto suficiente (RF-111): si falta algo lo declara y no genera (RN-97b, CB-10). Si hay entrenador asignado (invitado por él), la rutina generada queda PROPUESTA; si no, se genera igual y queda BLOQUEADA señalizada al administrador (RN-21, FL-01/A2).
2. **Paso 2 — perfil corporal y de entrenamiento** (§2.4). Avisos de completitud, nunca bloqueo.
3. **Paso 3 — evidencia, aptitud y preferencias** (§2.5–§2.7 + comentario abierto §3). Avisos de completitud, nunca bloqueo. Aquí se piden por primera vez favoritos, grupos a priorizar y observaciones generales, con ejemplos visibles ("¿qué ejercicios disfrutás?", "¿qué músculo querés desarrollar?", "contanos horarios, miedos, motivaciones...") para que el alumno entienda que el modelo los va a tener en cuenta.

La generación del alta no produce candidato ajustable: va directo a PROPUESTA ([FL-01](../flows/functional-flows.md)). Sin consentimiento de salud no hay condiciones ni mediciones y por tanto no hay contexto suficiente (FL-19/A2).

## 5. Actualización: qué cambia, cuándo y qué dispara

Todo cambio de contexto re-snapshotea la entrada versionada (RN-98): cada diagnóstico y propuesta referencia el contexto con el que se calculó, no el actual.

| Ritmo | Dato | Quién / cadencia | Efecto |
| ----- | ---- | ---------------- | ------ |
| Fijo | Nombre, nacimiento, sexo | Nunca (corrección por admin) | Ninguno |
| Por evento | Objetivo nuevo (cierra el anterior, RN-09) | El alumno lo cambia | Reevaluación + propuesta de cambio de tipo (RN-91, RN-89a) |
| Por evento | Alta/cierre de condición (RN-10, RN-11) | El alumno la declara/cierra | Reevaluación inmediata, marca sin retirar (RN-92, [FL-12](../flows/functional-flows.md)) |
| Por evento | Días, duración, nivel, evitar / favoritos / grupos a priorizar | Cada nueva generación o edición libre | Entran a la próxima generación; si hay rutina vigente incompatible, reevaluación (RN-45). Favoritos y prioridades no disparan reevaluación por sí solos: sólo pesan al construir |
| Periódico sugerido | Peso y mediciones | Prompt mensual en el panel ("¿actualizás tu peso?"); aptitud con avisos RN-13b | Alimentan e1RM, volumen relativo y proyección; la serie conserva cada punto fechado, la carga nueva no reescribe la anterior (RN-15) |
| Periódico sugerido | Comentario abierto y notas | Edición libre del alumno | Solo ficha del entrenador; ningún efecto automático |
| Por evento | Observaciones generales (§2.7) | El alumno las edita cuando quiere | Se reinterpretan en la próxima generación vía `interpretarPedido`; no tocan la rutina vigente ni disparan reevaluación por sí solas |
| Derivado | e1RM, adherencia, señales, récords | Cada sesión / cada 2 semanas (RN-78) | Diagnóstico RN-79a; nunca se editan a mano |

**UX de actualización:** el panel recuerda, no obliga. Dato fijo: sin recordatorio. Dato por evento: edición directa + confirmación del efecto ("cambiar tu objetivo va a proponer una rutina nueva"). Dato periódico: tarjeta mensual descartable para peso/mediciones; si el alumno la ignora, los indicadores lo declaran como falta de datos (RN-73), no como cero.

## 6. Preferencias por generación (opcionales, solo esa vez)

Al pedir o regenerar una rutina ([FL-04](../flows/functional-flows.md), pasos 1–2), además del objetivo general vigente, el solicitante puede declarar para **esa** generación:

- **Qué le gustaría trabajar** (foco libre u opcional por grupo/patrón, p. ej. "más pierna esta vez", "énfasis en espalda"): es la pregunta opcional del pedido; si no dice nada, se usa el objetivo y el equilibrio por defecto.
- **Observaciones del pedido** (texto libre, opcional, hasta 500 caracteres `[S]`): lo puntual de esta vez ("esta semana tengo poco tiempo", "me duele el hombro desde ayer" — esto último además sugiere declarar condición, FL-06/E2). Se suma a las observaciones generales §2.7 como entrada de `interpretarPedido`.
- Ejercicios a excluir esta vez (además de los estables de §2.6).
- Patrón preferido, duración y frecuencia distintas de las habituales.

Reglas: todo lo libre (foco, observaciones) entra por **`interpretarPedido`**, que lo traduce a parámetros estructurados; se confirman antes de usarse (RN-128, RF-053/paso 2) y sólo lo confirmado llega a `generarRutina` (RNF-41). Si la interpretación es incorrecta, el solicitante la corrige en ese paso — por eso existe. Lo declarado **no altera el perfil** (el foco de hoy no cambia el objetivo vigente ni las observaciones generales); no consume el tope de RN-127 salvo regeneración completa. Si no declara nada, se usan los valores del perfil más las observaciones generales vigentes. Los favoritos y grupos a priorizar estables (§2.6) se aplican por defecto; el foco del pedido los matiza sólo esa vez — si los contradice, vale el foco y se declara. En Etapa 1 no hay candidato ajustable: la salida válida va directo a PROPUESTA.

## 7. Arquitectura del contexto

```text
Perfil + series + vigencia ──▶ Context Builder (backend, determinista)
   │  snapshot versionado + hash (RN-98) ──▶ prompts (allowlist §7.1)
   │  textos sólo-entrenador (§3) ──▶ ficha del entrenador (nunca a ningún prompt)
   │  observaciones generales (§2.7) + del pedido (§6)
   │        ──▶ interpretarPedido ──▶ parámetros confirmados ──▶ generarRutina
   ▼
Diagnóstico / Propuesta referencian snapshot, no estado actual
```

### 7.1 Allowlist de los prompts (lo único que viaja al LLM)

**A `interpretarPedido`** (único que recibe texto libre, RNF-41): observaciones generales §2.7 + observaciones del pedido §6 + foco declarado, con contexto mínimo (gimnasio, alumno). Su salida se valida contra las enumeraciones cerradas de D2/§4 y se confirma con el usuario antes de propagarse.

**A `generarRutina` y demás componentes** (sólo tipado, nunca texto crudo): objetivo vigente, nivel, días, condiciones como pares (zona, severidad) **sin descripción libre**, parámetros confirmados derivados de las observaciones, preferencias estables tipadas (exclusiones, favoritos, grupos a priorizar — §2.6), aptitud como estado (vigente/vencida/ausente, sin documentos), inventario del gimnasio, catálogo prescribible, rutina vigente (estructura), indicadores agregados del período y esfuerzo percibido medio. Nunca: credenciales, correo, texto libre (§3 y crudos de §2.7/§6), datos de otro alumno u otro gimnasio. Sin prompts completos ni salud en logs persistentes (RNF-19). Ver [ia-etapa1](../architecture/ia-etapa1.md) §3.

### 7.2 Context Builder (backend, único armador)

Función determinista del backend: reúne perfil + series + vigencia a la fecha de la operación, valida contexto suficiente (RF-111) y emite un snapshot `{version, contexto, hash}` que se conserva junto a cada resultado (RN-98, RF-072). El servicio IA sólo lee la cola de integración y nunca toca las tablas de dominio ([generative-ai-integration](../architecture/generative-ai-integration.md)).

### 7.3 Qué ve cada consumidor

| Consumidor | Recibe |
| ---------- | ------ |
| Intérprete (`interpretarPedido`) | Observaciones generales §2.7 + del pedido §6 + contexto mínimo; devuelve parámetros tipados a confirmar |
| Generador (`generarRutina`) | Snapshot cerrado + prescribible + preferencias estables §2.6 + parámetros confirmados del pedido (§6) |
| Entrenador (ficha RF-037) | Todo lo anterior en claro + textos §3 y observaciones §2.7 + historial y snapshots |
| Alumno (su panel) | Sus datos + qué falta para contexto suficiente + recordatorios §5 |
| Diagnóstico / propuesta | Snapshot referenciado, reproducible |

### 7.4 Por qué el texto crudo no va directo a generación

Pasar las observaciones crudas a `generarRutina` rompería tres garantías normativas: RNF-41 (el texto libre queda confinado a `interpretarPedido`), la barrera anti-inyección (una observación podría traer "ignorá las reglas..." — la defensa real es que ninguna regla depende del prompt, [generative-ai](../architecture/generative-ai.md) §9) y RN-94/RN-96 (un narrativo no introduce valores; ningún componente emite consejo médico). El camino interpretación → confirmación → parámetros tipados conserva la intención del alumno —el modelo sí tiene en cuenta lo que escribió— sin darle al texto poder sobre la prescripción: RN-39a y §6 siguen validando toda salida y el entrenador sigue autorizando (RN-35).

## 8. Trazabilidad

RF-007, RF-008, RF-009, RF-010, RF-084, RF-085, RF-037, RF-045, RF-053, RF-054, RF-096, RF-111 · RN-09 a RN-17, RN-44a–44d, RN-91, RN-92, RN-94, RN-96, RN-97b, RN-98, RN-104, RN-105, RN-128 · RNF-08, RNF-19, RNF-24, RNF-41 · FL-01, FL-04, FL-06/E2, FL-12 · CB-10, CB-21, CB-22, CB-23.
