# Integración de IA generativa, ambientes y pruebas

**Estado:** propuesta de integración · **Fecha:** 2026-08-28 · **Fuente de alcance:** “Alcance de la IA — capa generativa”, v2.1

Este documento resume cómo integrar la capa generativa, cómo trabajar localmente y cómo promover cambios. No reemplaza las reglas de negocio de [D5](../domain/business-rules.md), los requisitos de [D8](../requirements/functional-requirements.md) ni las decisiones de [D11](../decisions/design-decisions.md).

## 1. Alcance y límite de autoridad

La primera entrega usa un único LLM para interpretar pedidos en lenguaje natural, proponer el tipo y contenido de una rutina, explicar el criterio y ofrecer alternativas. La predicción de cargas y progreso futuro queda fuera de esta entrega.

El modelo produce siempre un **candidato**, nunca una orden ejecutable. El backend Express conserva la autoridad: aporta sólo ejercicios válidos y el contexto mínimo, valida esquema, catálogo, compatibilidad, rangos y permisos, permite confirmar parámetros y persiste trazabilidad. Un entrenador debe aprobar la propuesta antes de que llegue al alumno. El modelo no activa rutinas, no prescribe ante lesiones ni emite consejo médico.

### Integración recomendada

```text
React (Vercel) -> API Express (Vercel) -> PostgreSQL (Neon)
                         |
                         v
              Servicio generativo Python
              (Cloud Run Service o Polo)

Trabajos predictivos futuros -> Cloud Run Jobs -> snapshots/resultados versionados
```

- El backend implementa un puerto `RoutineGenerator`; los adaptadores `fake`, `remote` y, si se necesita, otro proveedor mantienen reemplazable al modelo.
- El servicio Python expone una API privada y versionada. Recibe contexto minimizado y devuelve JSON estructurado; no accede a PostgreSQL ni decide autorización.
- El backend valida la respuesta. Si es inválida, realiza un solo reintento y después activa el camino de contingencia.
- Cada resultado registra modelo/configuración, versión del contrato, contexto de entrada o su referencia, fecha, validaciones, reintentos y decisión del entrenador. Los logs no guardan datos de salud ni prompts sensibles.
- La capa generativa online y los trabajos predictivos batch son despliegues distintos, aunque puedan compartir repositorio y librerías Python.

Antes de implementar se deben cerrar mediante ADR tres diferencias con el corpus actual:

1. D11/DD-31 asigna tipo de rutina y adaptación a tablas deterministas; el nuevo alcance los asigna al LLM. Se recomienda que el LLM genere el candidato y que las tablas continúen como restricciones auditables y fallback, no como autoridad eliminable.
2. RF-058, RF-113 y RNF-04/11/18 exigen continuidad determinista; el alcance recibido permite que crear o adaptar quede temporalmente indisponible y sólo conserva el formulario. Se recomienda mantener el formulario y un generador determinista mínimo; si se descarta, deben modificarse esos requisitos de forma explícita.
3. La arquitectura vigente describe Python sólo como motor batch. El servicio generativo online requiere un nuevo límite desplegable y actualizar `architecture/analytics-engine.md`, los `AGENTS.md` afectados y el contrato backend–IA.

## 2. Ambientes y trabajo local

| Recurso | Local | Test (`test`) | Producción (`main`) |
| --- | --- | --- | --- |
| Frontend | Vite, `localhost` | Vercel | Vercel |
| Backend | Express, `localhost` | Vercel | Vercel |
| PostgreSQL | Docker Compose | Proyecto/branch Neon aislado | Proyecto Neon aislado |
| IA generativa | `AI_MODE=fake` por defecto; Python local opcional | Cloud Run Service o Polo | Cloud Run Service o Polo |
| Predictivo futuro | job Python manual | Cloud Run Jobs | Cloud Run Jobs |

Cada repositorio publica un `.env.example`; los `.env` reales y credenciales nunca se versionan. El desarrollador levanta PostgreSQL con Compose, aplica migraciones desde backend, inicia backend y frontend con npm y usa el adaptador `fake` para trabajar sin GPU, costo ni red. Quien modifica la integración de IA levanta además el servicio Python o apunta al ambiente compartido de test con credenciales personales y límites de uso.

El fake debe implementar el mismo contrato y ofrecer fixtures de éxito, incompatibilidad, timeout, JSON inválido y servicio caído. Frontend consume únicamente OpenAPI del backend; backend e IA comparten un JSON Schema versionado o generan tipos desde una única definición. Los cambios incompatibles usan una nueva versión y permiten una transición coordinada.

Cada desarrollador usa su propia base local. Test y producción no comparten base, credenciales, almacenamiento ni servicio de IA. Las migraciones se generan y prueban localmente, pero CI las aplica una sola vez por ambiente; la aplicación no las ejecuta al arrancar.

## 3. Camino de un cambio a producción

```text
feature/* -> pull request a develop -> develop
develop -> pull request de promoción a test -> test estable
test -> pull request de release a main -> producción
```

Las ramas de feature nacen desde `develop`. Todo PR ejecuta formato, tipos, pruebas unitarias y de contrato; requiere la revisión de otra persona. Al promover a `test`, se despliegan frontend, backend, IA y migraciones en recursos de test, se ejecutan integración, evaluación del modelo y E2E. La promoción de `test` a `main` requiere aprobación del dueño del repositorio, checks verdes y smoke test posterior. Debe poder revertirse la aplicación y conservarse compatibilidad de base de datos durante el rollback.

Este flujo reemplazaría el staging mediante `release/*` documentado actualmente en [GitHub workflow](../delivery/github-workflow.md); debe aprobarse y actualizarse allí antes de configurar las reglas de ramas.

## 4. Estrategia de pruebas recomendada

No conviene comparar el texto exacto del LLM. Se versiona un conjunto fijo de casos y se verifican invariantes objetivas más una rúbrica humana.

| Nivel | Qué prueba | Cuándo |
| --- | --- | --- |
| Unidad | reglas, permisos, validadores, composición de contexto y parser | cada PR |
| Contrato | esquema backend–IA, compatibilidad entre versiones y fixtures del fake | cada PR |
| Integración | timeout, reintento único, fallback, persistencia y aislamiento de datos | cada PR/promoción |
| Evaluación del modelo | catálogo, compatibilidad, rangos, cobertura, números respaldados, lenguaje médico y latencia | cambios de modelo, prompt o parámetros; antes de `test` |
| E2E | pedido, confirmación, candidato, regeneración, envío al entrenador, aprobación y contingencia | en `test` antes de `main` |
| Humana | claridad, utilidad, motivo de rechazo y magnitud de edición | muestra de releases y monitoreo |

El conjunto de regresión debe cubrir perfiles incompletos o contradictorios, condiciones físicas, equipamiento ausente, distintos niveles, prompt injection, rutinas extensas, respuesta mal formada y caída del proveedor. Como puertas iniciales: 100 % de respuestas con esquema válido después del reintento, 0 ejercicios fuera del catálogo o incompatibles después de validar, 0 números no respaldados en explicaciones, y cumplimiento del límite de latencia de RNF-04. La calidad se sigue además con tasa de rechazo del entrenador, regeneraciones, porcentaje editado, fallos de validación, fallback, latencia y costo por candidato.

Los casos aprobados por entrenadores pasan al dataset de regresión sin datos personales. Un cambio de modelo, prompt, cuantización o parámetros se trata como cambio de código: versión nueva, evaluación comparativa contra la versión activa, despliegue en test y promoción explícita. Nunca se prueba en producción con usuarios como sustituto de la evaluación previa.

## 5. Orden de implementación

1. Resolver las tres decisiones abiertas y registrar el ADR.
2. Congelar el esquema backend–IA y construir el adaptador `fake`.
3. Implementar validación, auditoría, reintento y contingencia en backend.
4. Implementar el servicio Python y conectarlo sólo en test.
5. Construir el dataset de regresión con revisión de un entrenador.
6. Habilitar producción después de superar contrato, evaluación, E2E y aprobación humana.
