import html
from typing import Any


def _bar_chart(metrics: dict[str, int]) -> str:
    labels = {
        "features": "Características",
        "step_definitions": "Definiciones de pasos",
        "tasks": "Tasks",
        "questions": "Questions",
        "interactions": "Interactions",
        "user_interfaces": "Interfaces de usuario",
        "models": "Modelos",
    }
    entries = [
        (labels.get(key, key.replace("_", " ").title()), int(value))
        for key, value in metrics.items()
        if key not in {"gherkin_steps", "scenarios"}
    ]
    max_value = max((value for _, value in entries), default=1) or 1
    chart_width = 760
    label_width = 180
    value_width = 50
    bar_width = chart_width - label_width - value_width
    row_height = 34
    height = max(96, len(entries) * row_height + 20)
    rows: list[str] = []
    for index, (label, value) in enumerate(entries):
        y = 16 + index * row_height
        width = round((value / max_value) * bar_width) if value else 0
        rows.append(
            f'<text x="0" y="{y + 17}" class="chart-label">{html.escape(label)}</text>'
            f'<rect x="{label_width}" y="{y}" width="{bar_width}" height="22" rx="6" class="bar-bg"/>'
            f'<rect x="{label_width}" y="{y}" width="{width}" height="22" rx="6" class="bar"/>'
            f'<text x="{label_width + bar_width + 12}" y="{y + 17}" class="chart-value">{value}</text>'
        )
    return (
        f'<svg class="bar-chart" viewBox="0 0 {chart_width} {height}" role="img" '
        'aria-label="Gráfica de barras del inventario de componentes">' + "".join(rows) + "</svg>"
    )


def _donut_chart(metrics: dict[str, int]) -> str:
    keys = (
        "feature_to_step_definition",
        "step_definition_to_task",
        "step_definition_to_model",
        "task_to_interaction",
        "task_to_question",
    )
    labels = (
        "Característica → paso",
        "Paso → Task",
        "Paso → Modelo",
        "Task → Interaction",
        "Task → Question",
    )
    values = [int(metrics.get(key, 0)) for key in keys]
    colors = ("#2563eb", "#7c3aed", "#0891b2", "#ea580c")
    total = sum(values)
    radius = 62
    circumference = 2 * 3.141592653589793 * radius
    offset = 0.0
    segments: list[str] = []
    if total:
        for value, color in zip(values, colors):
            length = circumference * value / total
            segments.append(
                f'<circle cx="90" cy="90" r="{radius}" fill="none" stroke="{color}" '
                f'stroke-width="24" stroke-dasharray="{length:.2f} {circumference - length:.2f}" '
                f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 90 90)"/>'
            )
            offset += length
        center = f'<text x="90" y="86" text-anchor="middle" class="donut-total">{total}</text><text x="90" y="106" text-anchor="middle" class="donut-caption">vínculos</text>'
    else:
        segments.append(f'<circle cx="90" cy="90" r="{radius}" fill="none" stroke="#e2e8f0" stroke-width="24"/>')
        center = '<text x="90" y="96" text-anchor="middle" class="donut-caption">Sin vínculos</text>'
    legend = []
    for index, (label, value, color) in enumerate(zip(labels, values, colors)):
        y = 32 + index * 30
        legend.append(
            f'<circle cx="196" cy="{y - 5}" r="5" fill="{color}"/>'
            f'<text x="210" y="{y}" class="legend-label">{html.escape(label)}</text>'
            f'<text x="425" y="{y}" text-anchor="end" class="legend-value">{value}</text>'
        )
    return (
        '<svg class="donut-chart" viewBox="0 0 450 180" role="img" '
        'aria-label="Gráfica de distribución de relaciones">'
        + "".join(segments) + center + "".join(legend) + "</svg>"
    )


def render_html_report(
    architecture: dict[str, Any],
    screenplay: dict[str, Any],
    dependencies: dict[str, Any],
) -> str:
    project = architecture["project"]
    metrics = screenplay["metrics"]
    relation_labels = {
        "feature_to_step_definition": "Característica → definición de paso",
        "step_definition_to_task": "Definición de paso → Task",
        "step_definition_to_model": "Definición de paso → Modelo",
        "task_to_interaction": "Task → Interaction",
        "task_to_question": "Task → Question",
    }
    relation_metrics = {
        key: len(dependencies.get(key, []))
        for key in (
            "feature_to_step_definition",
            "step_definition_to_task",
            "step_definition_to_model",
            "task_to_interaction",
            "task_to_question",
        )
    }
    metric_labels = {
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
    inventory = "".join(
        f'<tr><th scope="row">{html.escape(metric_labels.get(key, key.replace("_", " ").title()))}</th><td>{int(value)}</td></tr>'
        for key, value in metrics.items()
    )
    pattern_labels = {
        "Cucumber Gherkin": "Cucumber Gherkin",
        "Cucumber Step Definitions": "Definiciones de pasos Cucumber",
        "Screenplay Tasks": "Tasks de Screenplay",
        "Screenplay Questions": "Questions de Screenplay",
        "Screenplay Interactions": "Interactions de Screenplay",
        "Screenplay User Interfaces": "Interfaces de usuario Screenplay",
    }
    evidence_labels = {
        "Feature files and parsed scenarios": "Archivos Feature y escenarios analizados",
        "Java classes with Cucumber annotations or stepDefinitions path": "Clases Java con anotaciones Cucumber o ubicadas en stepDefinitions",
        "Java classes in task package implementing Task": "Clases Java del paquete tasks que implementan Task",
        "Java classes in questions package using Question<T>": "Clases Java del paquete questions que usan Question<T>",
        "Java classes in interactions package": "Clases Java del paquete interactions",
        "Java classes in userInterfaces package with Target": "Clases Java del paquete userInterfaces con Target",
    }
    pattern_cards: list[str] = []
    for item in screenplay["patterns_detected"]:
        pattern_name = str(item["pattern"])
        evidence = str(item["evidence"])
        localized_name = pattern_labels.get(pattern_name, pattern_name)
        localized_evidence = str(item.get("evidence_es", evidence_labels.get(evidence, evidence)))
        pattern_cards.append(
            f'<article class="pattern"><div><h3>{html.escape(localized_name)}</h3>'
            f'<p>{html.escape(localized_evidence)}</p></div>'
            f'<span class="pattern-count">{int(item["count"])}</span></article>'
        )
    patterns = "".join(pattern_cards)
    relationship_rows = "".join(
        f'<tr><th scope="row">{html.escape(relation_labels[key])}</th>'
        f'<td>{count}</td><td><span class="badge">{"Heurística" if key == "feature_to_step_definition" else "Observada"}</span></td></tr>'
        for key, count in relation_metrics.items()
    )
    warnings = "".join(f"<li>{html.escape(str(error))}</li>" for error in project["scan_errors"])
    warning_section = (
        f'<section class="card warning"><h2>Advertencias del análisis</h2><ul>{warnings}</ul></section>'
        if warnings
        else '<section class="card success"><h2>Estado del análisis</h2><p>No se encontraron errores de lectura o exploración.</p></section>'
    )
    quality = architecture.get("quality", {})
    risks = quality.get("risks", [])
    risk_items = "".join(
        f'<li><strong>{html.escape(str(risk["severity"]).title())} — '
        f'{html.escape(str(risk["code"]))}:</strong> '
        f'{html.escape(str(risk["description"]))}</li>'
        for risk in risks
    ) or "<li>No se detectaron riesgos estáticos.</li>"
    orphan_items = "".join(
        f'<li><code>{html.escape(str(item["path"]))}</code> '
        f'({html.escape(str(item["component_type"]))}: '
        f'{html.escape(str(item["name"]))})</li>'
        for item in quality.get("orphaned_components", [])
    ) or "<li>No se detectaron componentes huérfanos.</li>"
    duplicate_items = "".join(
        f'<li><strong>{html.escape(str(item["component_type"]))} — '
        f'{html.escape(str(item["name"]))}:</strong> '
        f'{", ".join(f"<code>{html.escape(str(path))}</code>" for path in item["paths"])}</li>'
        for item in quality.get("duplicate_components", [])
    ) or "<li>No se detectaron componentes duplicados por nombre dentro de su categoría.</li>"
    quality_section = (
        '<section class="grid">'
        f'<article class="card"><h2>Riesgos detectados ({len(risks)})</h2><ul class="quality-list">{risk_items}</ul></article>'
        f'<article class="card"><h2>Componentes huérfanos ({len(quality.get("orphaned_components", []))})</h2><ul class="quality-list">{orphan_items}</ul></article>'
        f'<article class="card"><h2>Componentes duplicados ({len(quality.get("duplicate_components", []))})</h2><ul class="quality-list">{duplicate_items}</ul></article>'
        '</section>'
    )
    generated_items = [
        ("Archivos fuente", project["source_files_scanned"]),
        ("Características", metrics.get("features", 0)),
        ("Escenarios", metrics.get("scenarios", 0)),
        ("Pasos de Gherkin", metrics.get("gherkin_steps", 0)),
        ("Componentes Screenplay", sum(metrics.get(key, 0) for key in ("tasks", "questions", "interactions", "user_interfaces"))),
    ]
    summary_cards = "".join(
        f'<article class="summary-card"><span>{html.escape(label)}</span><strong>{int(value)}</strong></article>'
        for label, value in generated_items
    )
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>Reporte de arquitectura FKA — {html.escape(str(project["name"]))}</title>
  <style>
    :root {{ color-scheme: light; --ink:#142033; --muted:#617087; --line:#e5eaf1; --bg:#f4f7fb; --card:#fff; --accent:#2563eb; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.55 "Segoe UI",Arial,sans-serif; }}
    main {{ max-width:1180px; margin:0 auto; padding:36px 24px 60px; }}
    .hero {{ padding:30px 34px; color:#fff; border-radius:20px; background:linear-gradient(120deg,#142b55,#2563eb 72%,#0891b2); box-shadow:0 12px 35px #16396b24; }}
    .eyebrow {{ text-transform:uppercase; letter-spacing:.14em; font-size:12px; opacity:.8; }}
    h1 {{ margin:8px 0; font-size:clamp(27px,4vw,40px); line-height:1.15; }}
    .hero p {{ margin:5px 0 0; opacity:.86; }}
    .summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:14px; margin:20px 0; }}
    .summary-card,.card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; box-shadow:0 4px 14px #182c4810; }}
    .summary-card {{ padding:17px 20px; }} .summary-card span {{ display:block; color:var(--muted); font-size:13px; }} .summary-card strong {{ display:block; margin-top:3px; font-size:30px; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; margin:18px 0; }}
    .card {{ padding:22px; min-width:0; }} h2 {{ margin:0 0 14px; font-size:20px; }} h3 {{ margin:0; font-size:15px; }}
    .chart-wrap {{ width:100%; overflow-x:auto; }} .bar-chart {{ min-width:540px; width:100%; height:auto; }} .donut-chart {{ min-width:420px; width:100%; max-width:560px; height:auto; }}
    .chart-label,.legend-label {{ fill:#35445a; font:13px "Segoe UI",Arial,sans-serif; }} .chart-value,.legend-value {{ fill:#142033; font:bold 13px "Segoe UI",Arial,sans-serif; }}
    .bar-bg {{ fill:#edf2f8; }} .bar {{ fill:#3b82f6; }} .donut-total {{ fill:#142033; font:bold 22px "Segoe UI",Arial,sans-serif; }} .donut-caption {{ fill:#718096; font:12px "Segoe UI",Arial,sans-serif; }}
    table {{ width:100%; border-collapse:collapse; }} th,td {{ text-align:left; border-bottom:1px solid var(--line); padding:10px 8px; }} td {{ text-align:right; font-variant-numeric:tabular-nums; }} thead th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.05em; }}
    .pattern {{ display:flex; justify-content:space-between; align-items:center; gap:16px; padding:13px 0; border-bottom:1px solid var(--line); }} .pattern:last-child {{ border:0; }} .pattern p {{ margin:3px 0 0; color:var(--muted); font-size:13px; }} .pattern-count {{ min-width:42px; padding:5px 10px; border-radius:10px; background:#eff6ff; color:#1d4ed8; font-weight:700; text-align:center; }}
    .badge {{ display:inline-block; padding:3px 9px; border-radius:999px; background:#eef2ff; color:#4338ca; font-size:12px; }}
    .meta {{ color:var(--muted); }} .warning {{ border-left:4px solid #f59e0b; }} .success {{ border-left:4px solid #10b981; }} .success p {{ margin:0; color:#166534; }} .warning ul {{ margin-bottom:0; }}
    .scope {{ color:var(--muted); }} footer {{ margin-top:22px; color:var(--muted); font-size:13px; }}
    @media(max-width:760px) {{ main {{ padding:18px 13px 36px; }} .hero {{ padding:23px; }} .grid {{ grid-template-columns:1fr; }} .card {{ padding:18px; }} }}
    @media print {{ body {{ background:#fff; }} main {{ max-width:none; padding:0; }} .hero {{ box-shadow:none; print-color-adjust:exact; }} .card,.summary-card {{ box-shadow:none; break-inside:avoid; }} }}
  </style>
</head>
<body>
<main>
  <header class="hero">
    <div class="eyebrow">Framework Knowledge Agent · Análisis estático</div>
    <h1>Reporte de arquitectura</h1>
    <p>{html.escape(str(project["name"]))}</p>
  </header>
  <section class="summary" aria-label="Resumen del proyecto">{summary_cards}</section>
  <section class="grid">
    <article class="card"><h2>Inventario de componentes</h2><div class="chart-wrap">{_bar_chart(metrics)}</div></article>
    <article class="card"><h2>Distribución de relaciones</h2><div class="chart-wrap">{_donut_chart(relation_metrics)}</div></article>
  </section>
  <section class="grid">
    <article class="card"><h2>Detalle del inventario</h2><table><thead><tr><th>Componente</th><th>Cantidad</th></tr></thead><tbody>{inventory}</tbody></table></article>
    <article class="card"><h2>Patrones detectados</h2>{patterns}</article>
  </section>
  <section class="card"><h2>Relaciones</h2><table><thead><tr><th>Relación</th><th>Vínculos</th><th>Clasificación</th></tr></thead><tbody>{relationship_rows}</tbody></table>
    <p class="meta">Raíz analizada: <code>{html.escape(str(project["root"]))}</code> · Frameworks detectados: {html.escape(", ".join(map(str, project["frameworks"])))}</p>
  </section>
  {warning_section}
  {quality_section}
  <section class="card scope" style="margin-top:18px"><h2>Alcance y limitaciones</h2><p>Este reporte inspecciona únicamente los archivos fuente. No ejecuta código Java ni pruebas. Las relaciones entre características y definiciones de pasos son heurísticas; las referencias de tipos Java son observadas. Las llamadas indirectas, la inyección de dependencias y las expresiones Cucumber no compatibles pueden limitar la detección de relaciones.</p></section>
  <footer>Generado por FKA · Las gráficas SVG están integradas; este reporte funciona sin conexión y se actualiza en cada ejecución.</footer>
</main>
</body>
</html>
'''
