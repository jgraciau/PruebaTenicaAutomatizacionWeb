from typing import Any

from agents.architect.analyzers._utils import (
    finding,
    cycle_affected_count,
    isolated_components,
    relationships,
    recommendation,
)


class ArchitectureAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        graph = maps.get("dependency-graph", {})
        edges = graph.get("edges", [])
        if not isinstance(edges, list) or not edges:
            edges = relationships(maps)
        cycle_count = cycle_affected_count(maps)
        disconnected = isolated_components(maps)
        disconnected_count = sum(len(items) for items in disconnected.values())

        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, str]] = []
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
