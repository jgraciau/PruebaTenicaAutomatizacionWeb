from typing import Any

from agents.architect.analyzers._utils import (
    finding,
    isolated_components,
    repeated_scenario_signatures,
    recommendation,
)


class DebtAnalyzer:
    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        isolated = isolated_components(maps)
        total_isolated = sum(len(items) for items in isolated.values())
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, str]] = []
        if total_isolated:
            summary = ", ".join(
                f"{name}: {len(items)}"
                for name, items in isolated.items()
                if items
            )
            findings.append(
                finding(
                    "debt.unlinked-components",
                    "Candidatos a deuda por falta de vínculos",
                    "Los componentes sin relaciones registradas requieren validación; el mapa no prueba que estén sin uso.",
                    summary,
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "debt",
                    "Clasificar los componentes sin vínculos",
                    "Confirmar referencias reales y distinguir código obsoleto de relaciones no detectadas antes de modificarlo.",
                    summary,
                    "medium",
                )
            )

        signatures = repeated_scenario_signatures(architecture)
        repeated = max(signatures.values(), default=0)
        if repeated > 1:
            findings.append(
                finding(
                    "debt.repeated-scenarios",
                    "Se repiten secuencias completas de pasos",
                    "Los escenarios con secuencia idéntica pueden requerir cambios coordinados.",
                    f"La secuencia más repetida aparece {repeated} veces.",
                    "low",
                )
            )
            recommendations.append(
                recommendation(
                    "debt",
                    "Evaluar parametrización de escenarios repetidos",
                    "Comparar intención y datos de las secuencias repetidas antes de considerar Scenario Outline.",
                    f"Máximo de repeticiones exactas: {repeated}.",
                    "low",
                )
            )

        return {
            "findings": findings,
            "risks": [],
            "recommendations": recommendations,
        }
