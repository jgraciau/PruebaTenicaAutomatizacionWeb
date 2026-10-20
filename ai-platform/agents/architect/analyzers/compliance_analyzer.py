from typing import Any

from agents.architect.analyzers._utils import finding, recommendation, relationships


class ComplianceAnalyzer:
    _EXPECTED_COMPONENTS = (
        "features",
        "step_definitions",
        "tasks",
        "questions",
        "interactions",
        "targets",
        "models",
    )
    _EXPECTED_RELATIONS = (
        "step_definition",
        "invokes_task",
        "asks_question",
        "uses_interaction",
        "queries_target",
        "uses_model",
    )

    def analyze(self, maps: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        architecture = maps.get("architecture-map", {})
        edges = relationships(maps)
        relation_types = {str(edge.get("relation")) for edge in edges}
        missing_components = [
            name
            for name in self._EXPECTED_COMPONENTS
            if not isinstance(architecture.get(name), list)
            or not architecture.get(name)
        ]
        missing_relations = [
            relation for relation in self._EXPECTED_RELATIONS
            if relation not in relation_types
        ]
        findings: list[dict[str, Any]] = []
        recommendations: list[dict[str, str]] = []
        if missing_components:
            findings.append(
                finding(
                    "compliance.missing-components",
                    "Faltan categorías esperadas en los mapas",
                    "La ausencia de una categoría limita la comprobación estática de la estructura Screenplay.",
                    ", ".join(missing_components),
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "screenplay",
                    "Completar el inventario de componentes Screenplay",
                    "Verificar las rutas configuradas y la extracción de las categorías ausentes antes de interpretar el resultado como incumplimiento.",
                    ", ".join(missing_components),
                    "medium",
                )
            )
        if missing_relations:
            findings.append(
                finding(
                    "compliance.missing-relations",
                    "No hay evidencia de todos los tipos de relación esperados",
                    "Los mapas no registran todas las direcciones de relación utilizadas para revisar la estructura Screenplay.",
                    ", ".join(missing_relations),
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "screenplay",
                    "Revisar cobertura de relaciones Screenplay",
                    "Comprobar si las relaciones ausentes reflejan una limitación del extractor o una estructura que deba investigarse.",
                    ", ".join(missing_relations),
                    "medium",
                )
            )

        srp_candidates: list[str] = []
        for category in ("tasks", "questions", "interactions"):
            values = architecture.get(category, [])
            if not isinstance(values, list):
                continue
            for component in values:
                if not isinstance(component, dict):
                    continue
                responsibilities = component.get("responsibilities")
                if isinstance(responsibilities, list) and len(responsibilities) > 1:
                    srp_candidates.append(
                        str(component.get("id", component.get("name", category)))
                    )
        if srp_candidates:
            findings.append(
                finding(
                    "compliance.srp-candidates",
                    "Hay componentes con múltiples responsabilidades declaradas",
                    "La metadata indica más de una responsabilidad; se debe confirmar si existe una violación del principio de responsabilidad única en el código.",
                    ", ".join(srp_candidates),
                    "medium",
                )
            )
            recommendations.append(
                recommendation(
                    "screenplay",
                    "Revisar responsabilidades de componentes",
                    "Validar cohesión y motivos de cambio de cada componente señalado y separar responsabilidades únicamente cuando el código lo justifique.",
                    f"{len(srp_candidates)} componente(s) declaran responsabilidades múltiples.",
                    "medium",
                )
            )
        else:
            findings.append(
                finding(
                    "compliance.srp-unverified",
                    "El principio SRP no se puede certificar con los mapas",
                    "Los knowledge maps no incluyen responsabilidades internas suficientes para demostrar que cada clase tiene un único motivo de cambio.",
                    "Se requiere inspección de código fuente para validar SRP.",
                    "low",
                )
            )

        findings.append(
            finding(
                "compliance.static-boundary",
                "El mapa no valida responsabilidades internas",
                "La presencia de componentes y relaciones no demuestra que la implementación respete las responsabilidades Screenplay.",
                "Los knowledge maps representan estructura estática, no cuerpos de métodos ni resultados de ejecución.",
                "low",
            )
        )
        recommendations.append(
            recommendation(
                "screenplay",
                "Validar responsabilidades en el código",
                "Revisar responsabilidades internas de Tasks, Questions e Interactions y las definiciones de pasos; los mapas por sí solos no certifican cumplimiento.",
                "La evidencia disponible es estática.",
                "low",
            )
        )
        return {
            "findings": findings,
            "risks": [],
            "recommendations": recommendations,
        }
