# Reporte de arquitectura: PruebaTenicaAutomatizacionWeb

- **Raíz analizada:** `.`
- **Archivos fuente analizados:** 48
- **Frameworks detectados:** Serenity BDD, Cucumber, Gradle, Screenplay

## Inventario de componentes

| Componente | Cantidad |
| --- | ---: |
| Características | 4 |
| Definiciones de pasos | 4 |
| Tasks | 13 |
| Questions | 4 |
| Interactions | 3 |
| Interfaces de usuario | 6 |
| Modelos | 4 |
| Escenarios | 8 |
| Pasos de Gherkin | 51 |

## Patrones detectados

- **Cucumber Gherkin:** 4 (Archivos Feature y escenarios analizados).
- **Definiciones de pasos Cucumber:** 4 (Clases Java con anotaciones Cucumber o ubicadas en stepDefinitions).
- **Tasks de Screenplay:** 13 (Clases Java del paquete tasks que implementan Task).
- **Questions de Screenplay:** 4 (Clases Java del paquete questions que usan Question<T>).
- **Interactions de Screenplay:** 3 (Clases Java del paquete interactions).
- **Interfaces de usuario Screenplay:** 6 (Clases Java del paquete userInterfaces con Target).

## Relaciones

- **Característica → definición de paso:** 51 vínculos
- **Definición de paso → Task:** 12 vínculos
- **Task → Interaction:** 7 vínculos
- **Task → Question:** 0 vínculos

Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre clases Java son observadas.

## Alcance y limitaciones

Este reporte se basa únicamente en la inspección estática del código fuente. No ejecuta la aplicación Java ni sus pruebas. Las relaciones pueden estar incompletas cuando el código usa llamadas indirectas, inyección de dependencias o expresiones Cucumber que no se pueden inferir con seguridad.
