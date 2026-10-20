from typing import Any

from agents.architect.analyzers._utils import (
    cycle_affected_count,
    dependency_metrics,
    finding,
    recommendation,
    relationships,
)


class RiskAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        metrics = dependency_metrics(maps)
        risks: list[dict[str, str]] = []
        recommendations: list[dict[str, str]] = []

        project = architecture.get("project", {})
        scan_errors = architecture.get("scan_errors", [])
        if not scan_errors and isinstance(project, dict):
            scan_errors = project.get("scan_errors", [])
        if scan_errors:
            risks.append(
                finding(
                    "risk.incomplete-scan",
                    "Cobertura del inventario potencialmente incompleta",
                    "Los errores de análisis pueden ocultar componentes o relaciones.",
                    f"Errores registrados: {scan_errors}",
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

        fan_out = metrics["fan_out"]
        high_dependency_nodes = {
            node_id: count for node_id, count in fan_out.items() if count >= 8
        }
        if high_dependency_nodes:
            evidence = ", ".join(
                f"{node_id} ({count} dependencias)"
                for node_id, count in sorted(
                    high_dependency_nodes.items(),
                    key=lambda item: (-item[1], item[0]),
                )[:10]
            )
            risks.append(
                finding(
                    "risk.high-dependency",
                    "Hay nodos con muchas dependencias directas",
                    "Un abanico elevado de dependencias puede aumentar el impacto de cambios y el esfuerzo de pruebas.",
                    evidence,
                    "high",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Reducir dependencias directas concentradas",
                    "Revisar los nodos con mayor abanico y separar responsabilidades solo cuando el análisis del código confirme límites cohesivos.",
                    f"{len(high_dependency_nodes)} nodo(s) tienen 8 o más dependencias directas.",
                    "high",
                )
            )

        high_coupling_nodes = {
            node_id: degree
            for node_id, degree in metrics["degree"].items()
            if degree >= 10
        }
        if high_coupling_nodes:
            risks.append(
                finding(
                    "risk.high-coupling",
                    "Hay componentes con alto acoplamiento estructural",
                    "Un número elevado de relaciones entrantes y salientes aumenta el costo de cambios y el riesgo de efectos colaterales.",
                    ", ".join(
                        f"{node_id} ({degree} relaciones)"
                        for node_id, degree in sorted(
                            high_coupling_nodes.items(),
                            key=lambda item: (-item[1], item[0]),
                        )[:10]
                    ),
                    "high",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Revisar componentes de alto acoplamiento",
                    "Examinar las relaciones entrantes y salientes de los componentes señalados y aplicar inversión de dependencias o límites de módulo cuando corresponda.",
                    f"{len(high_coupling_nodes)} nodo(s) tienen 10 o más relaciones.",
                    "high",
                )
            )

        explicit_complexities: dict[str, float] = {}
        graph = maps.get("dependency-graph", {})
        nodes = graph.get("nodes", [])
        if isinstance(nodes, list):
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                identifier = node.get("id")
                complexity = node.get("complexity")
                if (
                    isinstance(identifier, str)
                    and isinstance(complexity, (int, float))
                    and complexity >= 10
                ):
                    explicit_complexities[identifier] = float(complexity)
        if explicit_complexities:
            risks.append(
                finding(
                    "risk.high-complexity",
                    "Hay componentes con complejidad explícita elevada",
                    "La complejidad informada por el mapa puede dificultar pruebas y mantenimiento.",
                    ", ".join(
                        f"{node_id} (complejidad {value:g})"
                        for node_id, value in sorted(
                            explicit_complexities.items(),
                            key=lambda item: (-item[1], item[0]),
                        )[:10]
                    ),
                    "high",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Simplificar componentes de alta complejidad",
                    "Revisar rutas de decisión, dividir responsabilidades cohesivas y añadir pruebas de caracterización antes de refactorizar.",
                    f"{len(explicit_complexities)} nodo(s) reportan complejidad igual o superior a 10.",
                    "high",
                )
            )
        elif metrics["max_fan_out"] >= 8:
            risks.append(
                finding(
                    "risk.complexity-proxy",
                    "Hay posibles focos de complejidad estructural",
                    "No se dispone de complejidad ciclomática; el número de dependencias salientes se usa solo como proxy de concentración estructural.",
                    f"Máximo de dependencias salientes: {metrics['max_fan_out']}.",
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "risk",
                    "Validar focos de complejidad estructural",
                    "Medir complejidad en el código fuente de los nodos señalados; reducir el abanico de dependencias únicamente cuando corresponda a responsabilidades mezcladas.",
                    f"El mapa no informa complejidad ciclomática; máximo de dependencias salientes: {metrics['max_fan_out']}.",
                    "medium",
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
