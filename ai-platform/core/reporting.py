from collections import defaultdict
from html import escape
from typing import Any


_COMPONENT_LABELS = {
    "features": "Flujos de negocio",
    "scenarios": "Escenarios",
    "steps": "Pasos definidos",
    "step_definitions": "Implementaciones de pasos",
    "tasks": "Tareas reutilizables",
    "questions": "Validaciones",
    "interactions": "Interacciones técnicas",
    "targets": "Elementos de interfaz",
    "models": "Modelos de datos",
    "actors": "Actores",
}
_RELATION_LABELS = {
    "contains": "incluye escenario",
    "step_definition": "paso relacionado con código",
    "invokes_task": "paso ejecuta tarea",
    "uses_actor": "paso usa actor",
    "asks_question": "paso consulta validación",
    "uses_interaction": "tarea usa interacción",
    "uses_model": "tarea usa modelo de datos",
    "queries_target": "validación consulta elemento",
    "uses_target": "interacción usa elemento",
}
_STYLES = """
:root{color-scheme:light;--ink:#172b4d;--muted:#52647a;--line:#dce4ec;
--paper:#fff;--canvas:#f3f6fa;--blue:#175cd3;--blue-soft:#eaf2ff;
--green:#087443;--green-soft:#e6f6ee;--amber:#8a4b08;--amber-soft:#fff4df}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink);
font:15px/1.55 "Segoe UI",Arial,sans-serif}main{max-width:1120px;margin:auto;padding:32px 22px 56px}
.hero{padding:32px;border-radius:20px;background:linear-gradient(120deg,#102c56,#175cd3);
color:white;box-shadow:0 12px 30px #172b4d20}.eyebrow{text-transform:uppercase;
letter-spacing:.12em;font-size:.76rem;font-weight:700;opacity:.8}.hero h1{font-size:clamp(2rem,5vw,3rem);
line-height:1.1;margin:.55rem 0}.hero p{max-width:760px;color:#e3edff;margin:.6rem 0 0}
.meta{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}.pill{display:inline-flex;
align-items:center;border-radius:999px;padding:5px 11px;background:#ffffff20;font-size:.85rem}
.section{margin-top:30px}.section h2{font-size:1.35rem;margin:0 0 5px}.intro{color:var(--muted);margin:0 0 15px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:13px}
.card,.panel{background:var(--paper);border:1px solid var(--line);border-radius:14px;
padding:18px;box-shadow:0 4px 14px #172b4d08}.card .number{display:block;font-size:2rem;
font-weight:750;line-height:1.2;color:var(--blue)}.card .label{display:block;margin-top:6px;
color:var(--muted);font-size:.91rem}.card .hint{display:block;margin-top:8px;color:#66778b;font-size:.78rem}
.callout{border-left:4px solid var(--blue);background:var(--blue-soft);padding:14px 17px;
border-radius:0 10px 10px 0;color:var(--ink)}.callout.warning{border-color:#d98910;background:var(--amber-soft)}
.callout.success{border-color:#0b8a50;background:var(--green-soft)}
.table-wrap{overflow-x:auto;background:var(--paper);border:1px solid var(--line);border-radius:13px}
table{width:100%;border-collapse:collapse;min-width:650px}th,td{text-align:left;padding:12px 14px;
border-bottom:1px solid var(--line);vertical-align:top}th{background:#f8fafc;color:#43566d;
font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}tr:last-child td{border-bottom:0}
.status{font-size:.8rem;font-weight:700;border-radius:999px;padding:4px 9px;white-space:nowrap}
.status.good{background:var(--green-soft);color:var(--green)}.status.review{background:var(--amber-soft);color:var(--amber)}
.feature{margin:14px 0;border:1px solid var(--line);border-radius:13px;background:var(--paper);overflow:hidden}
.feature summary{padding:15px 18px;cursor:pointer;font-weight:700}.feature summary span{float:right;
font-weight:500;color:var(--muted)}.feature-body{padding:0 18px 14px}.scenario{padding:12px 0;
border-top:1px solid var(--line)}.scenario h3{font-size:1rem;margin:0 0 7px}.step-list{margin:0;padding-left:22px}
.step-list li{margin:5px 0}.muted{color:var(--muted)}.small{font-size:.84rem}
.next-steps{display:grid;gap:10px;counter-reset:actions}.next-step{counter-increment:actions;
background:var(--paper);border:1px solid var(--line);border-radius:11px;padding:13px 15px}
.next-step:before{content:counter(actions);display:inline-grid;place-items:center;width:25px;height:25px;
margin-right:9px;border-radius:50%;background:var(--blue-soft);color:var(--blue);font-weight:700}
footer{margin-top:32px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.83rem}
code{font-size:.82em;overflow-wrap:anywhere}a{color:var(--blue)}
@media(max-width:600px){main{padding:16px 12px 36px}.hero{padding:23px}.feature summary span{float:none;display:block}}
"""


def _report_data(maps: dict[str, dict[str, Any]]) -> dict[str, Any]:
    architecture = maps["architecture-map"]
    metrics = maps["screenplay-map"]["metrics"]
    relationships = maps["relationship-map"]["relationships"]
    project = architecture["project"]
    definitions_by_id = {
        item["id"]: item for item in architecture.get("step_definitions", [])
    }
    task_by_id = {item["id"]: item for item in architecture.get("tasks", [])}
    relations_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in relationships:
        relations_by_source[edge["source_id"]].append(edge)

    feature_summaries: list[dict[str, Any]] = []
    unmatched_steps: list[dict[str, str]] = []
    matched_step_total = 0
    for feature in architecture.get("features", []):
        scenarios: list[dict[str, Any]] = []
        feature_step_count = 0
        feature_matched_count = 0
        for scenario in feature.get("scenarios", []):
            scenario_edges = [
                edge
                for edge in relations_by_source.get(scenario["id"], [])
                if edge["relation"] == "step_definition"
            ]
            matched_steps = {
                step
                for edge in scenario_edges
                for step in edge["evidence"].removeprefix("Heuristic match for: ").split("; ")
            }
            matched_steps.intersection_update(scenario.get("steps", []))
            scenario_steps = scenario.get("steps", [])
            missing = [step for step in scenario_steps if step not in matched_steps]
            feature_step_count += len(scenario_steps)
            feature_matched_count += len(matched_steps)
            matched_step_total += len(matched_steps)
            for step in missing:
                unmatched_steps.append(
                    {
                        "feature": feature["name"],
                        "scenario": scenario["name"],
                        "step": step,
                    }
                )
            linked_definitions = [
                definitions_by_id[edge["target_id"]]
                for edge in scenario_edges
                if edge["target_id"] in definitions_by_id
            ]
            task_ids = {
                edge["target_id"]
                for definition in linked_definitions
                for edge in relations_by_source.get(definition["id"], [])
                if edge["relation"] == "invokes_task"
            }
            question_ids = {
                edge["target_id"]
                for definition in linked_definitions
                for edge in relations_by_source.get(definition["id"], [])
                if edge["relation"] == "asks_question"
            }
            scenarios.append(
                {
                    "name": scenario["name"],
                    "steps": scenario_steps,
                    "matched_steps": matched_steps,
                    "missing_steps": missing,
                    "definition_names": sorted(
                        {definition["name"] for definition in linked_definitions}
                    ),
                    "task_names": sorted(
                        {
                            task_by_id[task_id]["name"]
                            for task_id in task_ids
                            if task_id in task_by_id
                        }
                    ),
                    "validation_count": len(question_ids),
                }
            )
        feature_summaries.append(
            {
                "name": feature["name"],
                "scenario_count": len(scenarios),
                "step_count": feature_step_count,
                "matched_step_count": feature_matched_count,
                "scenarios": scenarios,
            }
        )

    step_count = int(metrics.get("steps", 0))
    traceability = round(matched_step_total / step_count * 100) if step_count else 0
    relation_counts: dict[str, int] = defaultdict(int)
    for edge in relationships:
        relation_counts[edge["relation"]] += 1
    return {
        "project": project,
        "metrics": metrics,
        "features": feature_summaries,
        "unmatched_steps": unmatched_steps,
        "matched_step_count": matched_step_total,
        "traceability": traceability,
        "relationships": relationships,
        "relation_counts": relation_counts,
    }


def _recommendations(data: dict[str, Any]) -> list[str]:
    recommendations: list[str] = []
    missing = len(data["unmatched_steps"])
    if missing:
        recommendations.append(
            f"Revisar los {missing} pasos sin una definición de código identificada; "
            "el detalle aparece por escenario en este informe."
        )
    else:
        recommendations.append(
            "Los pasos de los escenarios tienen una definición asociada por análisis "
            "estático; confirmar la correspondencia durante una ejecución de pruebas."
        )
    if not data["metrics"].get("questions", 0):
        recommendations.append(
            "No se detectaron Questions/validaciones; confirmar que los escenarios "
            "verifican resultados de negocio y no solo acciones."
        )
    if data["project"].get("scan_errors"):
        recommendations.append(
            f"Resolver {len(data['project']['scan_errors'])} errores de lectura o "
            "configuración antes de usar el inventario como referencia completa."
        )
    recommendations.append(
        "Ejecutar la suite de automatización para conocer resultados, fallos y "
        "estabilidad; este análisis no ejecuta pruebas ni valida la aplicación."
    )
    return recommendations


def _business_summary(data: dict[str, Any]) -> str:
    metrics = data["metrics"]
    if not metrics.get("scenarios"):
        return (
            "No se identificaron escenarios para resumir. Comprueba las rutas y "
            "el formato de las especificaciones configurados."
        )
    feature_count = len(data["features"])
    scenario_count = metrics.get("scenarios", 0)
    return (
        f"Se identificaron {scenario_count} escenarios distribuidos en "
        f"{feature_count} flujos de negocio. El código contiene "
        f"{metrics.get('tasks', 0)} tareas reutilizables y "
        f"{metrics.get('questions', 0)} validaciones detectadas. "
        f"{data['matched_step_count']} de {metrics.get('steps', 0)} pasos tienen "
        "una definición de código asociada por análisis estático."
    )


def render_markdown_report(maps: dict[str, dict[str, Any]]) -> str:
    data = _report_data(maps)
    project = data["project"]
    metrics = data["metrics"]
    feature_rows = "\n".join(
        f"| {feature['name']} | {feature['scenario_count']} | "
        f"{feature['matched_step_count']} / {feature['step_count']} |"
        for feature in data["features"]
    ) or "| No se detectaron flujos | 0 | 0 / 0 |"
    component_rows = "\n".join(
        f"| {_COMPONENT_LABELS.get(name, name.replace('_', ' ').title())} | {count} |"
        for name, count in metrics.items()
        if name in _COMPONENT_LABELS
    )
    scenario_sections: list[str] = []
    for feature in data["features"]:
        scenario_lines = []
        for scenario in feature["scenarios"]:
            scenario_lines.append(
                f"### {scenario['name']}\n\n"
                f"Pasos identificados en código: {len(scenario['matched_steps'])} "
                f"de {len(scenario['steps'])}.\n\n"
                + "\n".join(
                    f"- {'✓' if step in scenario['matched_steps'] else '○'} {step}"
                    for step in scenario["steps"]
                )
                + (
                    "\n\nAcciones identificadas: "
                    + ", ".join(scenario["task_names"])
                    if scenario["task_names"]
                    else ""
                )
            )
        scenario_sections.append(
            f"## {feature['name']}\n\n" + "\n\n".join(scenario_lines)
        )
    recommendations = "\n".join(
        f"{index}. {recommendation}"
        for index, recommendation in enumerate(_recommendations(data), start=1)
    )
    errors = "\n".join(
        f"- {error}" for error in project.get("scan_errors", [])
    ) or "- No se registraron errores de lectura."
    return (
        f"# Reporte de arquitectura | {project['name']}\n\n"
        f"**{project['framework']} · {project['language']} · Screenplay**\n\n"
        f"> {_business_summary(data)}\n\n"
        "## Resumen para producto\n\n"
        f"- **Escenarios:** {metrics.get('scenarios', 0)} en "
        f"{metrics.get('features', 0)} flujos.\n"
        f"- **Trazabilidad estimada:** {data['matched_step_count']} de "
        f"{metrics.get('steps', 0)} ({data['traceability']}%, estimación estática).\n"
        f"- **Acciones reutilizables:** {metrics.get('tasks', 0)} Tasks y "
        f"{metrics.get('interactions', 0)} Interactions.\n"
        f"- **Validaciones detectadas:** {metrics.get('questions', 0)} Questions.\n\n"
        "## Cobertura del inventario\n\n"
        "| Flujo de negocio | Escenarios | Pasos con definición / total |\n"
        "|---|---:|---:|\n"
        f"{feature_rows}\n\n"
        "## Inventario de componentes\n\n"
        "| Qué representa | Elementos detectados |\n|---|---:|\n"
        f"{component_rows}\n\n"
        "## Escenarios y pasos\n\n"
        + ("\n\n".join(scenario_sections) or "No hay escenarios disponibles.")
        + "\n\n## Próximas acciones recomendadas\n\n"
        f"{recommendations}\n\n"
        "## Alcance y calidad del análisis\n\n"
        "Este reporte describe lo encontrado en el código y las especificaciones; "
        "no ejecuta pruebas, no confirma que la aplicación funcione y no equivale "
        "a cobertura de pruebas aprobadas. La relación entre un paso escrito y "
        "su definición de código es una estimación heurística.\n\n"
        f"Errores de lectura: {len(project.get('scan_errors', []))}.\n\n"
        f"{errors}\n"
    )


def render_html_report(maps: dict[str, dict[str, Any]]) -> str:
    data = _report_data(maps)
    project = data["project"]
    metrics = data["metrics"]
    missing_count = len(data["unmatched_steps"])
    cards = [
        (
            metrics.get("scenarios", 0),
            "Escenarios",
            f"en {metrics.get('features', 0)} flujos de negocio",
        ),
        (
            f"{data['traceability']}%",
            "Pasos con código asociado",
            f"{data['matched_step_count']} de {metrics.get('steps', 0)} · estimación",
        ),
        (
            metrics.get("tasks", 0),
            "Acciones reutilizables",
            "Tasks identificadas",
        ),
        (
            metrics.get("questions", 0),
            "Validaciones",
            "Questions identificadas",
        ),
        (
            metrics.get("targets", 0),
            "Elementos de interfaz",
            "selectores identificados",
        ),
    ]
    card_html = "".join(
        "<article class=\"card\">"
        f"<span class=\"number\">{escape(str(value))}</span>"
        f"<span class=\"label\">{escape(label)}</span>"
        f"<span class=\"hint\">{escape(hint)}</span></article>"
        for value, label, hint in cards
    )
    feature_rows = "".join(
        "<tr>"
        f"<td><strong>{escape(feature['name'])}</strong></td>"
        f"<td>{feature['scenario_count']}</td>"
        f"<td>{feature['step_count']}</td>"
        f"<td>{feature['matched_step_count']} / {feature['step_count']}</td>"
        "</tr>"
        for feature in data["features"]
    ) or '<tr><td colspan="4">No se detectaron flujos de negocio.</td></tr>'
    feature_details: list[str] = []
    for feature in data["features"]:
        scenario_details: list[str] = []
        for scenario in feature["scenarios"]:
            step_items = "".join(
                "<li>"
                f"<span class=\"status {'good' if step in scenario['matched_steps'] else 'review'}\">"
                f"{'Relacionado' if step in scenario['matched_steps'] else 'Revisar'}</span> "
                f"{escape(step)}</li>"
                for step in scenario["steps"]
            ) or '<li class="muted">No se detectaron pasos.</li>'
            code_details = []
            if scenario["definition_names"]:
                code_details.append(
                    "Definiciones: "
                    + ", ".join(escape(name) for name in scenario["definition_names"])
                )
            if scenario["task_names"]:
                code_details.append(
                    "Acciones: "
                    + ", ".join(escape(name) for name in scenario["task_names"])
                )
            if scenario["validation_count"]:
                code_details.append(
                    f"{scenario['validation_count']} validaciones relacionadas"
                )
            scenario_details.append(
                "<div class=\"scenario\">"
                f"<h3>{escape(scenario['name'])}</h3>"
                f"<ul class=\"step-list\">{step_items}</ul>"
                + (
                    '<p class="muted small">'
                    + " · ".join(code_details)
                    + "</p>"
                    if code_details
                    else ""
                )
                + "</div>"
            )
        feature_details.append(
            '<details class="feature"><summary>'
            f"{escape(feature['name'])}<span>{feature['scenario_count']} escenarios · "
            f"{feature['matched_step_count']}/{feature['step_count']} pasos relacionados"
            "</span></summary><div class=\"feature-body\">"
            + "".join(scenario_details)
            + "</div></details>"
        )
    recommendations = "".join(
        f'<div class="next-step">{escape(item)}</div>'
        for item in _recommendations(data)
    )
    status_class = "warning" if missing_count or project.get("scan_errors") else "success"
    status_message = (
        f"Hay {missing_count} pasos para revisar."
        if missing_count
        else "No se detectaron pasos sin relación estática."
    )
    errors = project.get("scan_errors", [])
    error_html = (
        "<ul>"
        + "".join(f"<li>{escape(error)}</li>" for error in errors)
        + "</ul>"
        if errors
        else "No se registraron errores de lectura."
    )
    return (
        "<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>Reporte para producto | {escape(project['name'])}</title>"
        f"<style>{_STYLES}</style></head><body><main>"
        '<header class="hero"><div class="eyebrow">Screenplay Knowledge Platform · '
        "Reporte para producto</div>"
        f"<h1>{escape(project['name'])}</h1>"
        f"<p>{escape(_business_summary(data))}</p>"
        '<div class="meta">'
        f'<span class="pill">{escape(project["framework"])}</span>'
        f'<span class="pill">{escape(project["language"])}</span>'
        '<span class="pill">Screenplay</span>'
        "</div></header>"
        '<section class="section"><h2>Resumen ejecutivo</h2>'
        '<p class="intro">Qué está descrito y cómo se conecta con la automatización.</p>'
        f'<div class="cards">{card_html}</div></section>'
        '<section class="section"><h2>Estado de trazabilidad</h2>'
        '<p class="intro">Indica si los pasos de los escenarios se pudieron relacionar '
        "estáticamente con código; no indica si las pruebas pasan.</p>"
        f'<div class="callout {status_class}">{escape(status_message)} '
        f'Trazabilidad estimada: <strong>{data["traceability"]}%</strong> '
        f'({data["matched_step_count"]} de {metrics.get("steps", 0)} pasos).</div></section>'
        '<section class="section"><h2>Cobertura por flujo de negocio</h2>'
        '<p class="intro">Resumen de escenarios escritos y pasos con una posible '
        'definición en el código.</p><div class="table-wrap"><table><thead><tr>'
        "<th>Flujo</th><th>Escenarios</th><th>Pasos escritos</th>"
        "<th>Pasos relacionados</th></tr></thead>"
        f"<tbody>{feature_rows}</tbody></table></div></section>"
        '<section class="section"><h2>Detalle por escenario</h2>'
        '<p class="intro">Expande un flujo para revisar sus pasos y las acciones '
        "detectadas.</p>"
        + (
            "".join(feature_details)
            or '<div class="panel">No se identificaron escenarios.</div>'
        )
        + "</section>"
        '<section class="section"><h2>Próximas acciones</h2>'
        '<p class="intro">Siguientes comprobaciones sugeridas para el equipo.</p>'
        f'<div class="next-steps">{recommendations}</div></section>'
        '<section class="section"><h2>Alcance del análisis</h2>'
        '<div class="callout warning">Análisis estático del repositorio. No ejecuta '
        "pruebas, no confirma comportamiento de la aplicación y no equivale a "
        "cobertura aprobada. Las asociaciones paso-código son heurísticas.</div>"
        f'<p class="muted small">Archivos leídos: {metrics.get("source_files_scanned", project.get("source_files_scanned", 0))} · '
        f'Errores de lectura: {len(errors)}.</p>'
        f'<div class="panel small">{error_html}</div></section>'
        "<footer>Reporte generado a partir de las especificaciones y el código "
        "configurados en SKP. Úsalo como apoyo para conversar sobre alcance, "
        "mantenimiento y próximos pasos; no como evidencia de ejecución exitosa."
        "</footer></main></body></html>"
    )

