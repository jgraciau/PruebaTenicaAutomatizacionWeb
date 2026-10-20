# Informe de deuda técnica — Automatizacion Web Bon-Bonite

Los candidatos requieren validación en el código fuente.

## Hallazgos

### Candidatos a deuda por falta de vínculos

Los componentes sin relaciones registradas requieren validación; el mapa no prueba que estén sin uso.

- **Evidencia:** tasks: 3, targets: 17, models: 2
- **Severidad:** MEDIUM

### Se repiten secuencias completas de pasos

Los escenarios con secuencia idéntica pueden requerir cambios coordinados.

- **Evidencia:** La secuencia más repetida aparece 5 veces.
- **Severidad:** LOW
## Recomendaciones

### Clasificar los componentes sin vínculos

Confirmar referencias reales y distinguir código obsoleto de relaciones no detectadas antes de modificarlo.

- **Evidencia:** tasks: 3, targets: 17, models: 2
- **Severidad:** MEDIUM

### Evaluar parametrización de escenarios repetidos

Comparar intención y datos de las secuencias repetidas antes de considerar Scenario Outline.

- **Evidencia:** Máximo de repeticiones exactas: 5.
- **Severidad:** LOW
