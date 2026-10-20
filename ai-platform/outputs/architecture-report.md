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
| Modelos | 3 |
| Escenarios | 8 |
| Pasos de Gherkin | 51 |

## Patrones detectados

- **Cucumber Gherkin:** 4 (Feature files and parsed scenarios).
- **Definiciones de pasos Cucumber:** 4 (Java classes with Cucumber annotations or stepDefinitions path).
- **Tasks de Screenplay:** 13 (Java classes in task package implementing Task).
- **Questions de Screenplay:** 4 (Java classes in questions package using Question<T>).
- **Interactions de Screenplay:** 3 (Java classes in interactions package).
- **Interfaces de usuario Screenplay:** 6 (Java classes in userInterfaces package with Target).

## Relaciones

- **Característica → definición de paso:** 51 vínculos
- **Definición de paso → Task:** 12 vínculos
- **Definición de paso → Modelo:** 1 vínculos
- **Task → Interaction:** 7 vínculos
- **Task → Question:** 0 vínculos

Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre clases Java son observadas.

## Hallazgos de calidad

- **Riesgos detectados:** 1
- **Componentes huérfanos:** 3
- **Grupos de componentes duplicados:** 0

### Riesgos

- **Medium — ORPHAN_COMPONENTS:** Se detectaron 3 componentes sin relaciones conocidas.

### Componentes sin relaciones conocidas

- `src/main/java/models/LoginCredentials.java` (model: LoginCredentials)
- `src/main/java/models/Orden.java` (model: Orden)
- `src/main/java/userInterfaces/ResgisterPage.java` (user_interface: ResgisterPage)

## Alcance y limitaciones

Este reporte se basa únicamente en la inspección estática del código fuente. No ejecuta la aplicación Java ni sus pruebas. Las relaciones pueden estar incompletas cuando el código usa llamadas indirectas, inyección de dependencias o expresiones Cucumber que no se pueden inferir con seguridad.
