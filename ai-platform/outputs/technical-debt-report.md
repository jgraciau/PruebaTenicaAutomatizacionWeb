# Informe de deuda técnica — Automatizacion Web Bon-Bonite

Los candidatos requieren validación en el código fuente.

## Hallazgos

### Candidatos a deuda por falta de vínculos

Los componentes sin relaciones registradas requieren validación; el mapa no prueba que estén sin uso.

- **Evidencia:** tasks: 3, targets: 17, models: 2
- **Severidad:** MEDIUM

### Hay componentes con nombres duplicados

Los nombres repetidos pueden representar lógica duplicada o clases distintas con nombres ambiguos; validar sus responsabilidades antes de consolidar.

- **Evidencia:** targets:contenidodelacuenta: 2; targets:enlacedecierredesesión: 2; targets:ingresoaliniciarsesion: 2
- **Severidad:** MEDIUM

### Hay componentes candidatos a no utilizados

La ausencia de referencias en los mapas no prueba que un elemento esté muerto; la extracción puede omitir usos indirectos o reflexivos.

- **Evidencia:** models: model:src/main/java/models/LoginCredentials.java, models: model:src/main/java/models/Orden.java
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

### Revisar componentes con nombres duplicados

Comparar implementación, consumidores y propósito de los componentes señalados; extraer o renombrar solo cuando la duplicación sea confirmada.

- **Evidencia:** 3 posible(s) duplicado(s) adicional(es).
- **Severidad:** MEDIUM

### Verificar componentes candidatos a no utilizados

Buscar referencias en el código fuente y revisar configuración, reflexión y puntos de entrada antes de eliminar cualquier componente.

- **Evidencia:** 2 componente(s) no tienen referencias registradas.
- **Severidad:** MEDIUM

### Evaluar parametrización de escenarios repetidos

Comparar intención y datos de las secuencias repetidas antes de considerar Scenario Outline.

- **Evidencia:** Máximo de repeticiones exactas: 5.
- **Severidad:** LOW
