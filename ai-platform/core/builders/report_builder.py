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
    for key in ("feature_to_step_definition", "step_definition_to_task", "task_to_interaction", "task_to_question"):
        lines.append(f"- **{_RELATION_LABELS[key]}:** {len(dependencies[key])} vínculos")
    lines.extend(["", "Las relaciones entre características y definiciones de pasos son heurísticas; las referencias directas entre clases Java son observadas.", ""])
    if project["scan_errors"]:
        lines.extend(["## Advertencias del análisis", ""])
        lines.extend(f"- {error}" for error in project["scan_errors"])
        lines.append("")
    lines.extend(["## Alcance y limitaciones", "", "Este reporte se basa únicamente en la inspección estática del código fuente. No ejecuta la aplicación Java ni sus pruebas. Las relaciones pueden estar incompletas cuando el código usa llamadas indirectas, inyección de dependencias o expresiones Cucumber que no se pueden inferir con seguridad.", ""])
    return "\n".join(lines)
