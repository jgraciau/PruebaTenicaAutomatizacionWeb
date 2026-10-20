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
