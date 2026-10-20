# Cumplimiento Screenplay — Automatizacion Web Bon-Bonite

La presencia de categorías y relaciones no certifica responsabilidades internas ni comportamiento en ejecución.

## Hallazgos

### El principio SRP no se puede certificar con los mapas

Los knowledge maps no incluyen responsabilidades internas suficientes para demostrar que cada clase tiene un único motivo de cambio.

- **Evidencia:** Se requiere inspección de código fuente para validar SRP.
- **Severidad:** LOW

### El mapa no valida responsabilidades internas

La presencia de componentes y relaciones no demuestra que la implementación respete las responsabilidades Screenplay.

- **Evidencia:** Los knowledge maps representan estructura estática, no cuerpos de métodos ni resultados de ejecución.
- **Severidad:** LOW
## Recomendaciones

### Validar responsabilidades en el código

Revisar responsabilidades internas de Tasks, Questions e Interactions y las definiciones de pasos; los mapas por sí solos no certifican cumplimiento.

- **Evidencia:** La evidencia disponible es estática.
- **Severidad:** LOW
