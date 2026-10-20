from typing import Any

from agents.architect.analyzers._utils import (
    cycle_affected_count,
    finding,
    recommendation,
    relationships,
)


class RiskAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        graph = maps.get("dependency-graph", {})
        edges = graph.get("edges", [])
        if not isinstance(edges, list) or not edges:
            edges = relationships(maps)
        risks: list[dict[str, str]] = []
        recommendations: list[dict[str, str]] = []

        if architecture.get("scan_errors"):
            risks.append(
                finding(
                    "risk.incomplete-scan",
                    "Cobertura del inventario potencialmente incompleta",
                    "Los errores de análisis pueden ocultar componentes o relaciones.",
                    f"Errores registrados: {architecture['scan_errors']}",
                    "high",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Resolver errores del análisis estático",
                    "Revisar los errores de lectura antes de basar decisiones de arquitectura en el inventario.",
                    "architecture-map.json contiene errores de análisis.",
                    "high",
                )
            )

        heuristic_edges = [
            edge
            for edge in relationships(maps)
            if "heuristic" in str(edge.get("evidence", "")).lower()
        ]
        if heuristic_edges:
            risks.append(
                finding(
                    "risk.heuristic-traceability",
                    "La trazabilidad incluye asociaciones heurísticas",
                    "Las asociaciones inferidas pueden vincular escenarios con definiciones de pasos de forma imprecisa.",
                    f"{len(heuristic_edges)} relación(es) contienen evidencia heurística.",
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Verificar la trazabilidad heurística",
                    "Validar los vínculos inferidos contra una fuente determinista o pruebas y conservar su carácter estimado hasta entonces.",
                    f"{len(heuristic_edges)} relación(es) heurísticas.",
                    "medium",
                )
            )

        cycle_count = cycle_affected_count(maps)
        if cycle_count:
            risks.append(
                finding(
                    "risk.dependency-cycles",
                    "Los ciclos pueden propagar cambios",
                    "Las dependencias cíclicas complican cambios aislados y análisis de impacto.",
                    f"{cycle_count} nodo(s) afectados por ciclos.",
                    "high",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Analizar y romper ciclos de dependencias",
                    "Revisar las dependencias cíclicas y separar responsabilidades donde el código confirme acoplamiento.",
                    f"{cycle_count} nodo(s) afectados por ciclos.",
                    "high",
                )
            )

        return {
            "findings": [],
            "risks": risks,
            "recommendations": recommendations,
        }
