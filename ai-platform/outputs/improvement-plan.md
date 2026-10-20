# Plan de mejora — Automatizacion Web Bon-Bonite

Recomendaciones priorizadas mediante severidad estática; confirmar evidencia antes de aplicar cambios.

## P2

### Validar los componentes sin relaciones

Contrastar los componentes aislados con referencias del código y corregir el mapa o retirar solo los elementos confirmados como obsoletos.

- **Categoría:** architecture
- **Evidencia:** tasks: 3, targets: 17, models: 2

### Clasificar los componentes sin vínculos

Confirmar referencias reales y distinguir código obsoleto de relaciones no detectadas antes de modificarlo.

- **Categoría:** debt
- **Evidencia:** tasks: 3, targets: 17, models: 2

### Verificar la trazabilidad heurística

Validar los vínculos inferidos contra una fuente determinista o pruebas y conservar su carácter estimado hasta entonces.

- **Categoría:** risk
- **Evidencia:** 16 relación(es) heurísticas.

## P3

### Evaluar parametrización de escenarios repetidos

Comparar intención y datos de las secuencias repetidas antes de considerar Scenario Outline.

- **Categoría:** debt
- **Evidencia:** Máximo de repeticiones exactas: 5.

### Conservar y validar oportunidades de reutilización

Revisar los componentes y flujos compartidos antes de extraer abstracciones; parametrizar escenarios solo si su semántica coincide.

- **Categoría:** reuse
- **Evidencia:** 14 componente(s) compartidos; 1 grupo(s) de escenarios con pasos idénticos.

### Validar responsabilidades en el código

Revisar responsabilidades internas de Tasks, Questions e Interactions y las definiciones de pasos; los mapas por sí solos no certifican cumplimiento.

- **Categoría:** screenplay
- **Evidencia:** La evidencia disponible es estática.
