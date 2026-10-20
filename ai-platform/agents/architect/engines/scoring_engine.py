from typing import Any

from agents.architect.analyzers._utils import (
    components,
    cycle_affected_count,
    dependency_metrics,
    isolated_components,
    relationships,
)


class ScoringEngine:
    _BANDS = (
        (80, "LOW"),
        (60, "MEDIUM"),
        (40, "HIGH"),
        (0, "CRITICAL"),
    )

    @classmethod
    def _classification(cls, score: int) -> str:
        return next(label for floor, label in cls._BANDS if score >= floor)

    @staticmethod
    def _score(value: float) -> int:
        return max(0, min(100, round(value)))

    def calculate(
        self,
        maps: dict[str, dict[str, Any]],
        analyses: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        architecture = maps.get("architecture-map", {})
        graph = maps.get("dependency-graph", {})
        metrics = dependency_metrics(maps)
        edges = graph.get("edges", [])
        if not isinstance(edges, list) or not edges:
            edges = relationships(maps)
        nodes = graph.get("nodes", [])
        if not isinstance(nodes, list):
            nodes = []
        scan_errors = architecture.get("scan_errors", [])
        project = architecture.get("project", {})
        if not scan_errors and isinstance(project, dict):
            scan_errors = project.get("scan_errors", [])
        disconnected_count = sum(
            len(items) for items in isolated_components(maps).values()
        )
        component_total = sum(
            len(components(architecture, name))
            for name in ("tasks", "questions", "interactions", "targets", "models")
        )
        cycle_count = cycle_affected_count(maps)
        scan_error_count = (
            len(scan_errors)
            if isinstance(scan_errors, list)
            else int(bool(scan_errors))
        )
        degree_penalty = min(25, max(0, metrics["max_degree"] - 6) * 2)
        architecture_score = self._score(
            100
            - min(45, cycle_count * 15)
            - min(30, scan_error_count * 10)
            - degree_penalty
            - (5 if not nodes and not edges else 0)
        )
        maintainability_score = self._score(
            100
            - (
                35 * disconnected_count / component_total
                if component_total
                else 20
            )
            - min(30, scan_error_count * 10)
        )
        shared_recommendations = analyses.get("reuse", {}).get(
            "recommendations", []
        )
        reuse_score = self._score(
            55
            + min(35, len(shared_recommendations) * 10)
            + min(10, len(edges) // 10)
            - (10 if component_total == 0 else 0)
        )
        expected_components = (
            "features",
            "step_definitions",
            "tasks",
            "questions",
            "interactions",
            "targets",
            "models",
        )
        present = sum(
            bool(components(architecture, name))
            for name in expected_components
        )
        relation_types = {edge.get("relation") for edge in relationships(maps)}
        expected_relations = {
            "step_definition",
            "invokes_task",
            "asks_question",
            "uses_interaction",
            "queries_target",
            "uses_model",
        }
        relation_coverage = len(relation_types & expected_relations) / len(
            expected_relations
        )
        screenplay_score = self._score(
            60 * present / len(expected_components)
            + 40 * relation_coverage
        )
        overall_score = self._score(
            (
                architecture_score
                + maintainability_score
                + reuse_score
                + screenplay_score
            )
            / 4
        )
        values = {
            "architecture_score": architecture_score,
            "maintainability_score": maintainability_score,
            "reuse_score": reuse_score,
            "reusability_score": reuse_score,
            "screenplay_score": screenplay_score,
            "overall_score": overall_score,
        }
        labels = {
            "architecture_score": "architecture",
            "maintainability_score": "maintainability",
            "reusability_score": "reusability",
            "screenplay_score": "screenplay_compliance",
            "overall_score": "overall_quality",
        }
        rationale = {
            "architecture_score": (
                f"Basado en {len(nodes)} nodos, {len(edges)} relaciones, "
                f"{cycle_count} ciclos y {scan_error_count} errores de análisis."
            ),
            "maintainability_score": (
                f"Penaliza {disconnected_count} componentes sin relación "
                f"entre {component_total} componentes Screenplay inventariados."
            ),
            "reusability_score": (
                f"Señal heurística basada en relaciones ({len(edges)}) "
                "y recomendaciones de componentes compartidos."
            ),
            "screenplay_score": (
                f"{present}/{len(expected_components)} categorías presentes; "
                f"{len(relation_types & expected_relations)}/"
                f"{len(expected_relations)} tipos de relación registrados."
            ),
            "overall_score": (
                "Media aritmética de arquitectura, mantenibilidad, reutilización "
                "y estructura Screenplay."
            ),
        }
        scores = {
            labels[name]: {
                "score": values[name],
                "classification": self._classification(values[name]),
                "rationale": rationale[name],
            }
            for name in labels
        }
        return {
            **values,
            "score_scale": {
                "range": "0-100",
                "classification_semantics": (
                    "Una puntuación baja indica mayor riesgo; las puntuaciones son "
                    "heurísticas basadas únicamente en knowledge maps."
                ),
                "bands": {
                    "CRITICAL": "0-39",
                    "HIGH": "40-59",
                    "MEDIUM": "60-79",
                    "LOW": "80-100",
                },
            },
            "scores": scores,
        }
