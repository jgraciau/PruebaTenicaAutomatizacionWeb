# Framework Knowledge Agent (FKA) — Sprint 1

Analizador estático de repositorios Java / Serenity BDD / Cucumber / Gradle / Screenplay. No ejecuta código ni pruebas Java y no depende de IA generativa.

## Requisitos e instalación

Python 3.10 o superior. El runtime usa solo la biblioteca estándar; pytest se requiere para las pruebas.

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

Desde este directorio, el comando predeterminado analiza el repositorio padre y escribe aquí los artefactos:

```powershell
python main.py
```

Usa `--root` para seleccionar el repositorio fuente y `--output` para seleccionar el directorio de artefactos:

```powershell
python main.py --root "C:/path/to/java-project" --output "C:/path/to/artifacts"
```

Generated files:

- `knowledge/architecture-map.json`
- `knowledge/screenplay-map.json`
- `knowledge/dependency-map.json`
- `outputs/architecture-report.md`
- `outputs/architecture-report.html` — dashboard visual offline con gráficas SVG integradas, regenerado en cada ejecución.

Las rutas de los mapas son relativas a `--root`, usan separadores `/` y los artefactos se escriben en UTF-8 con orden estable de claves. Se excluyen `.git`, `.gradle`, carpetas del IDE, `build`, `target`, `venv`, `node_modules` y otros directorios generados. Los archivos ilegibles o que no estén en UTF-8 se omiten; las advertencias se registran en `project.scan_errors`. Las raíces inexistentes se manejan sin interrumpir el proceso; la CLI devuelve un código distinto de cero si no pudo analizar archivos.

Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre tipos Java se marcan como observadas. Se analizan anotaciones y expresiones comunes de Cucumber en Java. El panel HTML incluye gráficas del inventario de componentes y distribución de relaciones, métricas, patrones detectados y advertencias. Las gráficas SVG y los estilos están integrados: no requieren acceso a la red ni paquetes de visualización. Abre `outputs/architecture-report.html` en un navegador moderno después de ejecutar el escáner. Tanto el reporte HTML como el Markdown se regeneran automáticamente en cada ejecución de `python main.py` y se presentan en español.

## Validación

```powershell
python -m pytest -q
```
