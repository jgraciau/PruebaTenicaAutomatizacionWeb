# Informe de riesgos — Automatizacion Web Bon-Bonite

Riesgos estáticos, no resultados de ejecución.

## Riesgos

### Hay nodos con muchas dependencias directas

Un abanico elevado de dependencias puede aumentar el impacto de cambios y el esfuerzo de pruebas.

- **Evidencia:** interaction:src/main/java/interactions/ClickJs.java (32 dependencias), question:src/main/java/questions/ObtenerResumenOrden.java (8 dependencias)
- **Severidad:** HIGH

### Hay componentes con alto acoplamiento estructural

Un número elevado de relaciones entrantes y salientes aumenta el costo de cambios y el riesgo de efectos colaterales.

- **Evidencia:** interaction:src/main/java/interactions/ClickJs.java (36 relaciones), step_definition:src/test/java/stepDefinitions/RegisterUserDefinitions.java (13 relaciones), step_definition:src/test/java/stepDefinitions/ProductManagementDefinitions.java (11 relaciones)
- **Severidad:** HIGH

### Hay posibles focos de complejidad estructural

No se dispone de complejidad ciclomática; el número de dependencias salientes se usa solo como proxy de concentración estructural.

- **Evidencia:** Máximo de dependencias salientes: 32.
- **Severidad:** MEDIUM

### La trazabilidad incluye asociaciones heurísticas

Las asociaciones inferidas pueden vincular escenarios con definiciones de pasos de forma imprecisa.

- **Evidencia:** 16 relación(es) contienen evidencia heurística.
- **Severidad:** MEDIUM
