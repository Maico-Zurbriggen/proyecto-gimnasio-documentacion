# Permisos y protección del repositorio

## Repositorios personales

Los cuatro repositorios pertenecen inicialmente a `Maico-Zurbriggen`. En repositorios personales los colaboradores tienen lectura y escritura, mientras las reglas de ramas restringen cómo integran cambios. `.github/CODEOWNERS` identifica a `@Maico-Zurbriggen` como dueño requerido para `main`.

Si se necesitan roles granulares, los repositorios deben transferirse a una organización.

## Ruleset de `main`

- requerir pull request;
- requerir una aprobación del Code Owner propietario;
- descartar aprobaciones al agregar commits;
- requerir aprobación del último push por otra persona;
- exigir conversaciones resueltas y check `quality` actualizado;
- bloquear force-push, eliminación y bypass;
- permitir sólo squash merge;
- deshabilitar auto-merge.

## Rulesets de `develop` y `test`

- requerir PR y una aprobación;
- exigir una persona distinta de quien realizó el último push;
- descartar aprobaciones obsoletas;
- exigir conversaciones resueltas y check `quality`;
- bloquear force-push y eliminación;
- impedir commits exclusivos en `test`: las correcciones nacen desde `develop` y se promueven.

## Repositorio documental

`proyecto-gimnasio-documentacion` usa sólo `main` y protección reducida:

- historial lineal;
- force-push y eliminación bloqueados;
- sin aprobación, Code Owner ni check previo obligatorios;
- push directo permitido;
- CI `quality` posterior al push.

Los cambios normativos o coordinados con código deberían usar PR aunque GitHub no lo imponga.

## Environments

- `test`: despliegues desde la rama `test`, con secretos de Neon Test y credenciales test de IA.
- `production`: despliegues sólo desde `main`, con aprobación manual del propietario.

Los secretos de producción no están disponibles en PRs, `develop`, `test` ni computadoras locales.

## Verificación

1. Push directo a ramas protegidas: rechazado.
2. PR sin aprobación: no fusionable.
3. Nuevo commit: aprobación descartada.
4. `test` sólo recibe promociones desde `develop`.
5. `main` sólo habilita merge con aprobación del dueño y CI verde.
6. Auto-merge no aparece disponible.
