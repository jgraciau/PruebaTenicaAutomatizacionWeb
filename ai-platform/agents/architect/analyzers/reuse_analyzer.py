from collections import defaultdict
from typing import Any

from agents.architect.analyzers._utils import (
    finding,
    recommendation,
    repeated_scenario_signatures,
    relationships,
)


class ReuseAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        edges = relationships(maps)
        consumers: dict[str, set[str]] = defaultdict(set)
        for edge in edges:
            source_id = edge.get("source_id")
            target_id = edge.get("target_id")
            if isinstance(source_id, str) and isinstance(target_id, str):
                consumers[target_id].add(source_id)
        shared = [
            (component_id, len(source_ids))
            for component_id, source_ids in consumers.items()
            if len(source_ids) > 1
        ]
        reusable_by_type: dict[str, list[tuple[str, int]]] = {
            "tasks": [],
            "questions": [],
            "interactions": [],
        }
        for category in reusable_by_type:
            values = architecture.get(category, [])
            if not isinstance(values, list):
                continue
            for component in values:
                if not isinstance(component, dict):
                    continue
                identifier = component.get("id")
                if not isinstance(identifier, str):
                    continue
                consumer_count = len(consumers.get(identifier, set()))
                if consumer_count > 1:
                    reusable_by_type[category].append(
                        (identifier, consumer_count)
                    )

        signatures = repeated_scenario_signatures(architecture)
        repeated_groups = sum(1 for count in signatures.values() if count > 1)
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, str]] = []
        findings.append(
            finding(
                "reuse.shared-components",
                "Se observan componentes compartidos",
                "Las relaciones estáticas sugieren consumidores múltiples; no demuestran reutilización entre proyectos.",
                f"{len(shared)} componente(s) tienen más de una relación registrada.",
                "low",
            )
        )
        for category, candidates in reusable_by_type.items():
            findings.append(
                finding(
                    f"reuse.{category}",
                    f"Oportunidades de reutilización de {category}",
                    "Se consideran reutilizables los componentes con más de un consumidor distinto registrado; comprobar contratos y semántica antes de extraer abstracciones.",
                    (
                        "; ".join(
                            f"{identifier} ({count} consumidores)"
                            for identifier, count in candidates
                        )
                        if candidates
                        else "No hay consumidores múltiples registrados."
                    ),
                    "low",
                )
            )
        if shared or repeated_groups:
            evidence = (
                f"{len(shared)} componente(s) compartidos "
                f"({sum(len(items) for items in reusable_by_type.values())} "
                "Tasks/Questions/Interactions reutilizables); "
                f"{repeated_groups} grupo(s) de escenarios con pasos idénticos."
            )
            recommendations.append(
                recommendation(
                    "reuse",
                    "Conservar y validar oportunidades de reutilización",
                    "Revisar los componentes y flujos compartidos antes de extraer abstracciones; parametrizar escenarios solo si su semántica coincide.",
                    evidence,
                    "low",
                )
            )
        return {
            "findings": findings,
            "risks": [],
            "recommendations": recommendations,
        }
