# Interfaz de datos con el backend

## Principio

PostgreSQL contiene dos interfaces diferentes para IA: estructuras operativas de generación online y datasets versionados para analítica batch. Backend es dueño de ambas definiciones y de sus migraciones.

## Generación online

- Backend crea la solicitud idempotente con contexto minimizado.
- El servicio IA reclama trabajos y escribe estados o resultados sólo en estructuras designadas.
- El resultado registra identificador, intento, modelo, configuración, contrato e instante.
- Backend valida y convierte una salida válida directamente en rutina `PROPUESTA`; IA no escribe rutinas ni aprobaciones.
- El rol IA recibe privilegios mínimos y separados para Neon Test y Neon Producción.
- La credencial autenticada ante IA selecciona internamente la conexión; el cliente nunca envía una URL de base.

Las solicitudes abandonadas, respuestas inválidas y fallos se eliminan a los 30 días. Los resultados aceptados conservan contexto mínimo y versiones según la política de auditoría.

## Analítica batch

Cada job declara:

- nombre y versión del dataset de entrada;
- columnas, tipos, nulabilidad y unidades;
- instante de corte y zona horaria;
- claves de idempotencia;
- tabla o artefacto de salida;
- versión del componente y parámetros.

El motor batch sólo escribe salidas designadas y no actualiza sesiones, rutinas, usuarios ni otras fuentes transaccionales.

## Desarrollo y pruebas

Backend e IA locales usan Neon Test con roles personales o de servicio restringidos. Nunca se copian datos personales reales al repositorio, fixtures o datasets de regresión. Las pruebas unitarias y de contrato usan datos sintéticos y PostgreSQL efímero en CI cuando necesitan modificar el esquema.

## Cambios

Un cambio incompatible requiere:

1. nueva versión del contrato;
2. migración o vista preparada por backend;
3. compatibilidad temporal;
4. PR relacionados en backend e IA;
5. fixtures y tests de contrato actualizados;
6. despliegue por etapas antes de retirar la versión anterior.
