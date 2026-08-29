# Flujo de trabajo en GitHub

## Ramas

Estas reglas aplican a frontend, backend e IA:

- `main`: producción, estable y etiquetada.
- `test`: ambiente estable de integración y aceptación.
- `develop`: integración del próximo incremento.
- `feature/<issue>-<descripcion>`: trabajo funcional desde `develop`.
- `fix/<issue>-<descripcion>`: corrección desde `develop`.
- `hotfix/<issue>-<descripcion>`: corrección urgente desde `main`.

No se usan ramas `release/*`. El mismo commit promovido de `develop` a `test` y luego a `main` mantiene trazabilidad entre ambientes. Un hotfix vuelve después a `develop` y `test` para evitar divergencia.

### Repositorio documental

`proyecto-gimnasio-documentacion` mantiene únicamente `main`. Puede aceptar push directo por su protección reducida, aunque los cambios normativos o coordinados con código deberían usar una rama corta y PR para dejar visible la discusión. Siempre se ejecuta `quality`.

## Flujo normal

```text
feature/* -> PR -> develop -> PR -> test -> PR -> main
                                  |             |
                                test        producción
```

1. Crear o asignar un issue con criterios de aceptación.
2. Crear la rama desde `develop`.
3. Abrir PR y mantenerlo acotado.
4. Exigir CI verde y aprobación de una persona distinta de quien hizo el último push.
5. Hacer squash merge a `develop`.
6. Abrir PR de promoción `develop -> test`; desplegar y ejecutar integración, evaluación y E2E.
7. Corregir fallos mediante ramas desde `develop` y volver a promover, sin commits exclusivos en `test`.
8. Abrir PR `test -> main`; exigir aprobación del dueño, checks y smoke test posterior.

Backend e IA se despliegan independientemente. Cuando cambia un contrato incompatible, primero se agrega una versión compatible, después se promueven consumidores y finalmente se retira la anterior.

Un cambio de modelo, prompt o parámetros requiere dataset de regresión verde y validación de al menos un entrenador antes de `main`.

## Protección recomendada

Para `develop` y `test`:

- prohibir push directo, force-push y eliminación;
- exigir PR y una aprobación de otra persona;
- invalidar aprobaciones ante nuevos commits;
- exigir conversaciones resueltas y check `quality`;
- permitir squash merge.

Para `main`:

- aplicar las reglas anteriores;
- exigir aprobación del Code Owner propietario;
- impedir bypass de las reglas;
- deshabilitar auto-merge;
- exigir el environment `production` con aprobación manual del dueño.

Los despliegues de `test` usan el environment `test`. La aprobación habilita el merge, pero no lo ejecuta automáticamente.

## Commits y versiones

Usar Conventional Commits en inglés:

```text
feat(training): persist completed sets
fix(auth): enforce student ownership
docs(ai): define online generation boundary
```

Las releases usan SemVer y tags `vX.Y.Z`; mientras el producto no sea estable, `v0.x.y`.
