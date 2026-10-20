from typing import Any


_METRIC_LABELS = {
    "features": "Características",
    "scenarios": "Escenarios",
    "gherkin_steps": "Pasos de Gherkin",
    "step_definitions": "Definiciones de pasos",
    "tasks": "Tasks",
    "questions": "Questions",
    "interactions": "Interactions",
    "user_interfaces": "Interfaces de usuario",
    "models": "Modelos",
}

_PATTERN_LABELS = {
    "Cucumber Gherkin": "Cucumber Gherkin",
    "Cucumber Step Definitions": "Definiciones de pasos Cucumber",
    "Screenplay Tasks": "Tasks de Screenplay",
    "Screenplay Questions": "Questions de Screenplay",
    "Screenplay Interactions": "Interactions de Screenplay",
    "Screenplay User Interfaces": "Interfaces de usuario Screenplay",
}

_RELATION_LABELS = {
    "feature_to_step_definition": "Característica → definición de paso",
    "step_definition_to_task": "Definición de paso → Task",
    "step_definition_to_model": "Definición de paso → Modelo",
    "task_to_interaction": "Task → Interaction",
    "task_to_question": "Task → Question",
}


def render_report(architecture: dict[str, Any], screenplay: dict[str, Any], dependencies: dict[str, Any]) -> str:
    project = architecture["project"]
    lines = [
        f"# Reporte de arquitectura: {project['name']}",
        "",
        f"- **Raíz analizada:** `{project['root']}`",
        f"- **Archivos fuente analizados:** {project['source_files_scanned']}",
        f"- **Frameworks detectados:** {', '.join(project['frameworks'])}",
        "",
        "## Inventario de componentes",
        "",
        "| Componente | Cantidad |",
        "| --- | ---: |",
    ]
    for key, count in screenplay["metrics"].items():
        lines.append(f"| {_METRIC_LABELS.get(key, key.replace('_', ' ').title())} | {count} |")
    lines.extend(["", "## Patrones detectados", ""])
    for pattern in screenplay["patterns_detected"]:
        label = _PATTERN_LABELS.get(pattern["pattern"], pattern["pattern"])
        evidence = pattern.get("evidence_es", pattern["evidence"])
        lines.append(f"- **{label}:** {pattern['count']} ({evidence}).")
    lines.extend(["", "## Relaciones", ""])
    for key in (
        "feature_to_step_definition",
        "step_definition_to_task",
        "step_definition_to_model",
        "task_to_interaction",
        "task_to_question",
    ):
        lines.append(
            f"- **{_RELATION_LABELS[key]}:** {len(dependencies.get(key, []))} vínculos"
        )
    lines.extend(["", "Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre clases Java son observadas.", ""])
    quality = architecture.get("quality", {})
    lines.extend(["## Hallazgos de calidad", ""])
    lines.append(f"- **Riesgos detectados:** {len(quality.get('risks', []))}")
    lines.append(f"- **Componentes huérfanos:** {len(quality.get('orphaned_components', []))}")
    lines.append(f"- **Grupos de componentes duplicados:** {len(quality.get('duplicate_components', []))}")
    if quality.get("risks"):
        lines.extend(["", "### Riesgos", ""])
        lines.extend(f"- **{risk['severity'].title()} — {risk['code']}:** {risk['description']}" for risk in quality["risks"])
    if quality.get("orphaned_components"):
        lines.extend(["", "### Componentes sin relaciones conocidas", ""])
        lines.extend(f"- `{item['path']}` ({item['component_type']}: {item['name']})" for item in quality["orphaned_components"])
    if quality.get("duplicate_components"):
        lines.extend(["", "### Nombres duplicados dentro de una categoría", ""])
        lines.extend(f"- **{item['component_type']} — {item['name']}:** {', '.join(f'`{path}`' for path in item['paths'])}" for item in quality["duplicate_components"])
    lines.append("")
    if project["scan_errors"]:
        lines.extend(["## Advertencias del análisis", ""])
        lines.extend(f"- {error}" for error in project["scan_errors"])
        lines.append("")
    lines.extend(["## Alcance y limitaciones", "", "Este reporte se basa únicamente en la inspección estática del código fuente. No ejecuta la aplicación Java ni sus pruebas. Las relaciones pueden estar incompletas cuando el código usa llamadas indirectas, inyección de dependencias o expresiones Cucumber que no se pueden inferir con seguridad.", ""])
    return "\n".join(lines)
