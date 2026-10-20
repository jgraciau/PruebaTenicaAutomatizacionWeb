# Revisión de arquitectura — Automatizacion Web Bon-Bonite

Valoración heurística derivada de knowledge maps; los componentes sin relaciones no se consideran automáticamente código muerto.

## Puntuaciones (0-100)

- **architecture:** 100/100 (LOW) — Basado en 107 nodos, 111 relaciones, 0 ciclos y 0 errores de análisis.
- **maintainability:** 91/100 (LOW) — Penaliza 22 componentes sin relación entre 89 componentes Screenplay inventariados.
- **reusability:** 75/100 (MEDIUM) — Señal heurística basada en relaciones (111) y recomendaciones de componentes compartidos.
- **screenplay_compliance:** 100/100 (LOW) — 7/7 categorías presentes; 6/6 tipos de relación registrados.
- **overall_quality:** 92/100 (LOW) — Media aritmética de arquitectura, mantenibilidad, reutilización y estructura Screenplay.
## Hallazgos

### No se registran ciclos de dependencias

El grafo disponible no contiene ciclos declarados.

- **Evidencia:** 111 relaciones examinadas.
- **Severidad:** LOW

### Hay componentes sin relaciones registradas

Un componente aislado puede ser obsoleto o reflejar una limitación de extracción; no prueba código muerto.

- **Evidencia:** tasks: 3, targets: 17, models: 2
- **Severidad:** MEDIUM
