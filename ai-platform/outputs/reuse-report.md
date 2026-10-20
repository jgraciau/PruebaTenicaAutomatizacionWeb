# Informe de reutilización — Automatizacion Web Bon-Bonite

Las relaciones compartidas son señales estáticas y no evidencian reutilización entre proyectos.

## Hallazgos

### Se observan componentes compartidos

Las relaciones estáticas sugieren consumidores múltiples; no demuestran reutilización entre proyectos.

- **Evidencia:** 14 componente(s) tienen más de una relación registrada.
- **Severidad:** LOW

### Oportunidades de reutilización de tasks

Se consideran reutilizables los componentes con más de un consumidor distinto registrado; comprobar contratos y semántica antes de extraer abstracciones.

- **Evidencia:** task:src/main/java/tasks/browser/OpenBrowser.java (2 consumidores); task:src/main/java/tasks/LoginBonBonite.java (2 consumidores)
- **Severidad:** LOW

### Oportunidades de reutilización de questions

Se consideran reutilizables los componentes con más de un consumidor distinto registrado; comprobar contratos y semántica antes de extraer abstracciones.

- **Evidencia:** No hay consumidores múltiples registrados.
- **Severidad:** LOW

### Oportunidades de reutilización de interactions

Se consideran reutilizables los componentes con más de un consumidor distinto registrado; comprobar contratos y semántica antes de extraer abstracciones.

- **Evidencia:** interaction:src/main/java/interactions/ClickJs.java (4 consumidores); interaction:src/main/java/interactions/ScrollToCenter.java (2 consumidores)
- **Severidad:** LOW
## Recomendaciones

### Conservar y validar oportunidades de reutilización

Revisar los componentes y flujos compartidos antes de extraer abstracciones; parametrizar escenarios solo si su semántica coincide.

- **Evidencia:** 14 componente(s) compartidos (4 Tasks/Questions/Interactions reutilizables); 1 grupo(s) de escenarios con pasos idénticos.
- **Severidad:** LOW
