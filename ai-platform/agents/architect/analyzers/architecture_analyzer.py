from typing import Any

from agents.architect.analyzers._utils import (
    finding,
    cycle_affected_count,
    dependency_metrics,
    isolated_components,
    components,
    graph_edges,
    recommendation,
)


class ArchitectureAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        metrics = dependency_metrics(maps)
        edges = graph_edges(maps)
        cycle_count = cycle_affected_count(maps)
        disconnected = isolated_components(maps)
        disconnected_count = sum(len(items) for items in disconnected.values())
        component_categories = (
            "features",
            "scenarios",
            "step_definitions",
            "actors",
            "tasks",
            "questions",
            "interactions",
            "targets",
            "models",
        )
        component_count = sum(
            len(components(architecture, category))
            for category in component_categories
        )

        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, str]] = []
        findings.append(
            finding(
                "architecture.inventory",
                "Resumen de estructura y dependencias",
                "Inventario estático de componentes, relaciones y señales de acoplamiento.",
                (
                    f"{component_count} componentes; {metrics['node_count']} nodos; "
                    f"{metrics['edge_count']} relaciones; "
                    f"acoplamiento medio {metrics['average_degree']:.2f}; "
                    f"máximo {metrics['max_degree']}."
                ),
                "low",
            )
        )
        if cycle_count:
            findings.append(
                finding(
                    "architecture.cycles",
                    "Se detectaron ciclos en el grafo",
                    "Los ciclos pueden dificultar la comprensión de dependencias.",
                    f"{cycle_count} nodo(s) afectados por ciclos en el grafo.",
                    "high",
                )
            )
        else:
            findings.append(
                finding(
                    "architecture.no-cycles",
                    "No se registran ciclos de dependencias",
                    "El grafo disponible no contiene ciclos declarados.",
                    f"{len(edges)} relaciones examinadas.",
                    "low",
                )
            )

        scan_errors = architecture.get("scan_errors", [])
        project = architecture.get("project", {})
        if not scan_errors and isinstance(project, dict):
            scan_errors = project.get("scan_errors", [])
        if scan_errors:
            error_count = len(scan_errors) if isinstance(scan_errors, list) else 1
            findings.append(
                finding(
                    "architecture.scan-errors",
                    "El inventario reporta errores de análisis",
                    "Los errores de lectura pueden dejar incompleta la vista arquitectónica.",
                    f"{error_count} error(es) reportado(s) en architecture-map.json.",
                    "high",
                )
            )
        if disconnected_count:
            summary = ", ".join(
                f"{name}: {len(items)}"
                for name, items in disconnected.items()
                if items
            )
            findings.append(
                finding(
                    "architecture.disconnected-components",
                    "Hay componentes sin relaciones registradas",
                    "Un componente aislado puede ser obsoleto o reflejar una limitación de extracción; no prueba código muerto.",
                    summary,
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "architecture",
                    "Validar los componentes sin relaciones",
                    "Contrastar los componentes aislados con referencias del código y corregir el mapa o retirar solo los elementos confirmados como obsoletos.",
                    summary,
                    "medium",
                )
            )

        return {
            "findings": findings,
            "risks": [],
            "recommendations": recommendations,
        }
