from typing import Any

from agents.architect.analyzers._utils import (
    components,
    duplicate_components,
    finding,
    isolated_components,
    relationships,
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

        duplicated = duplicate_components(
            architecture,
            ("tasks", "questions", "interactions", "models", "targets"),
        )
        if duplicated:
            duplicate_count = sum(len(items) - 1 for items in duplicated.values())
            findings.append(
                finding(
                    "debt.duplicate-components",
                    "Hay componentes con nombres duplicados",
                    "Los nombres repetidos pueden representar lógica duplicada o clases distintas con nombres ambiguos; validar sus responsabilidades antes de consolidar.",
                    "; ".join(
                        f"{category}: {len(items)}"
                        for category, items in sorted(duplicated.items())
                    ),
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "debt",
                    "Revisar componentes con nombres duplicados",
                    "Comparar implementación, consumidores y propósito de los componentes señalados; extraer o renombrar solo cuando la duplicación sea confirmada.",
                    f"{duplicate_count} posible(s) duplicado(s) adicional(es).",
                    "medium",
                )
            )

        unused: list[tuple[str, str]] = []
        connected_ids = {
            edge.get(endpoint)
            for edge in relationships(maps)
            for endpoint in ("source_id", "target_id")
            if isinstance(edge.get(endpoint), str)
        }
        for category in ("tasks", "questions", "interactions", "models"):
            for component in components(architecture, category):
                identifier = component.get("id")
                references = component.get("references")
                if (
                    isinstance(identifier, str)
                    and identifier not in connected_ids
                    and isinstance(references, list)
                    and not references
                ):
                    unused.append((category, identifier))
        if unused:
            findings.append(
                finding(
                    "debt.unused-components",
                    "Hay componentes candidatos a no utilizados",
                    "La ausencia de referencias en los mapas no prueba que un elemento esté muerto; la extracción puede omitir usos indirectos o reflexivos.",
                    ", ".join(
                        f"{category}: {identifier}"
                        for category, identifier in unused
                    ),
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "debt",
                    "Verificar componentes candidatos a no utilizados",
                    "Buscar referencias en el código fuente y revisar configuración, reflexión y puntos de entrada antes de eliminar cualquier componente.",
                    f"{len(unused)} componente(s) no tienen referencias registradas.",
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
