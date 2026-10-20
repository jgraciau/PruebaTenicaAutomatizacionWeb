# Framework Knowledge Agent (FKA) — Sprint 1

Analizador estático de repositorios Java / Serenity BDD / Cucumber / Gradle / Screenplay. No ejecuta código ni pruebas Java y no depende de IA generativa.

## Requisitos e instalación

Python 3.10 o superior. El runtime usa solo la biblioteca estándar; pytest se requiere para las pruebas.

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

`main.py` está dentro de `PruebaTenicaAutomatizacionWeb\ai-platform`. Puedes ejecutarlo desde esa carpeta:

```powershell
Set-Location "C:\ruta\al\repositorio\PruebaTenicaAutomatizacionWeb\ai-platform"
python main.py
```

O desde la carpeta padre del repositorio, especificando la ruta al script:

```powershell
python .\PruebaTenicaAutomatizacionWeb\ai-platform\main.py `
  --root ".\PruebaTenicaAutomatizacionWeb" `
  --output ".\PruebaTenicaAutomatizacionWeb\ai-platform"
```

Para analizar otro proyecto, cambia `--root` por la ruta real de su carpeta. `--output` indica dónde escribir los artefactos; también puedes usar una ruta absoluta:

```powershell
python .\PruebaTenicaAutomatizacionWeb\ai-platform\main.py `
  --root "C:\ruta\real\al\proyecto-java" `
  --output "C:\ruta\real\para\los\artefactos"
```

Antes del análisis completo, FKA inspecciona la estructura y señales Java/Gherkin para inferir los paquetes y componentes Screenplay existentes. La ejecución completa escribe ese diagnóstico en `outputs/project-profile.json` y utiliza el inventario detectado para analizar también paquetes no convencionales como `actions`, `answers`, `flow` o `pages`. El perfil solo adapta reglas de análisis en memoria; no modifica archivos del proyecto. Para validar otro repositorio antes de generar mapas, añade `--preflight-only`:

```powershell
python .\PruebaTenicaAutomatizacionWeb\ai-platform\main.py `
  --root "C:\ruta\real\al\proyecto-java" `
  --output "C:\ruta\real\para\los\artefactos" `
  --preflight-only
```

Sustituye esas rutas de ejemplo por directorios existentes en tu equipo; `C:\ruta\...` es un marcador y no una ruta ejecutable. El preflight reporta readiness `ready`, `partial` o `unsupported`, convenciones detectadas, conteos y advertencias. `partial` indica que faltan señales Screenplay esperadas; `unsupported` indica que no se encontraron fuentes Java/Gherkin para analizar. La detección automática depende de evidencia estática (anotaciones, tipos implementados, `Target` y estructura); convenciones propietarias que no expongan esas señales requerirán ampliar el perfil.

Generated files:

- `outputs/project-profile.json` — diagnóstico previo y convenciones detectadas.
- `knowledge/architecture-map.json`
- `knowledge/screenplay-map.json`
- `knowledge/dependency-map.json`
- `outputs/architecture-report.md`
- `outputs/architecture-report.html` — dashboard visual offline con gráficas SVG integradas, regenerado en cada ejecución.

Las rutas de los mapas son relativas a `--root`, usan separadores `/` y los artefactos se escriben en UTF-8 con orden estable de claves. Se excluyen `.git`, `.gradle`, carpetas del IDE, `build`, `target`, `venv`, `node_modules` y otros directorios generados. Los archivos ilegibles o que no estén en UTF-8 se omiten; las advertencias se registran en `project.scan_errors`. Las raíces inexistentes se manejan sin interrumpir el proceso; la CLI devuelve un código distinto de cero si no pudo analizar archivos.

Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre tipos Java se marcan como observadas. Se analizan anotaciones y expresiones comunes de Cucumber en Java. El panel HTML incluye gráficas del inventario de componentes y distribución de relaciones, métricas, patrones detectados y advertencias. Las gráficas SVG y los estilos están integrados: no requieren acceso a la red ni paquetes de visualización. Abre `outputs/architecture-report.html` en un navegador moderno después de ejecutar el escáner. Tanto el reporte HTML como el Markdown se regeneran automáticamente en cada ejecución de `python main.py` y se presentan en español.

Los pasos de `Background` se incluyen en el inventario y se relacionan con sus definiciones de pasos. El mapa de dependencias distingue asociaciones heurísticas Feature → Step Definition de referencias Java observadas; cuando un Task usa varias Interactions se conserva cada vínculo. Los Models detectados en directorios de pruebas con sufijo `Test`/`Tests` no se cuentan como modelos de producción.

## Validación

```powershell
python -m pytest -q
```
