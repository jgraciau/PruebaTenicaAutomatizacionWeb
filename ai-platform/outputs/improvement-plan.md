# Plan de mejora — Automatizacion Web Bon-Bonite

Recomendaciones priorizadas mediante severidad estática; confirmar evidencia antes de aplicar cambios.

## P1

### Reducir dependencias directas concentradas

Revisar los nodos con mayor abanico y separar responsabilidades solo cuando el análisis del código confirme límites cohesivos.

- **Categoría:** risk
- **Evidencia:** 2 nodo(s) tienen 8 o más dependencias directas.

### Revisar componentes de alto acoplamiento

Examinar las relaciones entrantes y salientes de los componentes señalados y aplicar inversión de dependencias o límites de módulo cuando corresponda.

- **Categoría:** risk
- **Evidencia:** 3 nodo(s) tienen 10 o más relaciones.

## P2

### Validar los componentes sin relaciones

Contrastar los componentes aislados con referencias del código y corregir el mapa o retirar solo los elementos confirmados como obsoletos.

- **Categoría:** architecture
- **Evidencia:** tasks: 3, targets: 17, models: 2

### Clasificar los componentes sin vínculos

Confirmar referencias reales y distinguir código obsoleto de relaciones no detectadas antes de modificarlo.

- **Categoría:** debt
- **Evidencia:** tasks: 3, targets: 17, models: 2

### Revisar componentes con nombres duplicados

Comparar implementación, consumidores y propósito de los componentes señalados; extraer o renombrar solo cuando la duplicación sea confirmada.

- **Categoría:** debt
- **Evidencia:** 3 posible(s) duplicado(s) adicional(es).

### Verificar componentes candidatos a no utilizados

Buscar referencias en el código fuente y revisar configuración, reflexión y puntos de entrada antes de eliminar cualquier componente.

- **Categoría:** debt
- **Evidencia:** 2 componente(s) no tienen referencias registradas.

### Validar focos de complejidad estructural

Medir complejidad en el código fuente de los nodos señalados; reducir el abanico de dependencias únicamente cuando corresponda a responsabilidades mezcladas.

- **Categoría:** risk
- **Evidencia:** El mapa no informa complejidad ciclomática; máximo de dependencias salientes: 32.

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
- **Evidencia:** 14 componente(s) compartidos (4 Tasks/Questions/Interactions reutilizables); 1 grupo(s) de escenarios con pasos idénticos.

### Validar responsabilidades en el código

Revisar responsabilidades internas de Tasks, Questions e Interactions y las definiciones de pasos; los mapas por sí solos no certifican cumplimiento.

- **Categoría:** screenplay
- **Evidencia:** La evidencia disponible es estática.
