import re
from collections import defaultdict
from dataclasses import asdict
from typing import Any

from core.models import DependencyModel
from core.models.project_knowledge_model import ProjectKnowledge

_WORD_PATTERN = re.compile(r"[\wÀ-ÿ]+", re.UNICODE)


class KnowledgeBuilder:
    """Build stable maps and a framework-independent relationship graph."""

    def build(self, result: ProjectKnowledge) -> dict[str, dict[str, Any]]:
        project = asdict(result.project)
        categories: dict[str, list[dict[str, Any]]] = {
            "features": result.features,
            "step_definitions": result.step_definitions,
            "actors": result.actors,
            "tasks": result.tasks,
            "questions": result.questions,
            "interactions": result.interactions,
            "targets": result.targets,
            "models": result.models,
        }
        edges = self._relationships(result)
        nodes = [
            {
                "id": component["id"],
                "type": {
                    "features": "feature",
                    "step_definitions": "step_definition",
                    "actors": "actor",
                    "tasks": "task",
                    "questions": "question",
                    "interactions": "interaction",
                    "targets": "target",
                    "models": "model",
                }[component_type],
                "name": component["name"],
                "source_path": component.get("source_path", ""),
            }
            for component_type, components in categories.items()
            for component in components
        ]
        nodes.extend(
            {
                "id": scenario["id"],
                "type": "scenario",
                "name": scenario["name"],
                "source_path": feature["source_path"],
            }
            for feature in result.features
            for scenario in feature["scenarios"]
        )
        edges_as_dicts = [asdict(edge) for edge in edges]
        graph = {"nodes": nodes, "edges": edges_as_dicts}
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for edge in edges_as_dicts:
            grouped[edge["relation"]].append(edge)
        dependency_map = {
            "relationships": edges_as_dicts,
            "by_relation": dict(sorted(grouped.items())),
        }
        scenarios = [
            scenario
            for feature in result.features
            for scenario in feature["scenarios"]
        ]
        architecture = {
            "project": {
                **project,
                "source_files_scanned": result.source_files_scanned,
                "scan_errors": result.scan_errors,
            },
            **categories,
            "scenarios": scenarios,
        }
        screenplay = {
            "project": project,
            "component_types": {
                category: len(components) for category, components in categories.items()
            },
            "metrics": {
                "features": len(result.features),
                "scenarios": len(scenarios),
                "steps": sum(len(scenario["steps"]) for scenario in scenarios),
                "actors": len(result.actors),
                "tasks": len(result.tasks),
                "questions": len(result.questions),
                "interactions": len(result.interactions),
                "targets": len(result.targets),
                "models": len(result.models),
                "step_definitions": len(result.step_definitions),
            },
        }
        return {
            "architecture-map": architecture,
            "screenplay-map": screenplay,
            "dependency-map": dependency_map,
            "relationship-map": {"relationships": edges_as_dicts},
            "dependency-graph": graph,
        }

    @staticmethod
    def _relationships(result: ProjectKnowledge) -> list[DependencyModel]:
        nodes: dict[str, tuple[str, dict[str, Any]]] = {}
        for component_type in (
            "features",
            "step_definitions",
            "actors",
            "tasks",
            "questions",
            "interactions",
            "targets",
            "models",
        ):
            for component in getattr(result, component_type):
                nodes[component["id"]] = (component_type[:-1], component)
        for feature in result.features:
            for scenario in feature["scenarios"]:
                nodes[scenario["id"]] = ("scenario", scenario)

        relationships: list[DependencyModel] = []

        def add(
            source_id: str,
            target_id: str,
            relation: str,
            evidence: str,
        ) -> None:
            if source_id not in nodes or target_id not in nodes:
                return
            source_type, _ = nodes[source_id]
            target_type, _ = nodes[target_id]
            relationships.append(
                DependencyModel(
                    source_id=source_id,
                    target_id=target_id,
                    source_type=source_type,
                    target_type=target_type,
                    relation=relation,
                    evidence=evidence,
                )
            )

        for feature in result.features:
            for scenario in feature["scenarios"]:
                add(
                    feature["id"],
                    scenario["id"],
                    "contains",
                    "Scenario is declared in the feature source.",
                )
                matching_steps: dict[str, set[str]] = defaultdict(set)
                for step_text in scenario["steps"]:
                    for definition in result.step_definitions:
                        if any(
                            KnowledgeBuilder._matches_step(step_text, expression)
                            for expression in definition["expressions"]
                        ):
                            matching_steps[definition["id"]].add(step_text)
                for definition_id, matched_steps in matching_steps.items():
                    add(
                        scenario["id"],
                        definition_id,
                        "step_definition",
                        "Heuristic match for: " + "; ".join(sorted(matched_steps)),
                    )

        for definition in result.step_definitions:
            for reference_id in definition.get("references", []):
                target_type = nodes.get(reference_id, ("", {}))[0]
                relation = {
                    "actor": "uses_actor",
                    "task": "invokes_task",
                    "question": "asks_question",
                }.get(target_type)
                if not relation:
                    continue
                add(
                    definition["id"],
                    reference_id,
                    relation,
                    f"{target_type.capitalize()} reference found in the step-definition source.",
                )
        for task in result.tasks:
            task_references = set(task.get("references", []))
            interaction_ids = [
                reference_id
                for reference_id in task_references
                if nodes.get(reference_id, ("", {}))[0] == "interaction"
            ]
            target_ids = [
                reference_id
                for reference_id in task_references
                if nodes.get(reference_id, ("", {}))[0] == "target"
            ]
            for interaction_id in interaction_ids:
                for target_id in target_ids:
                    add(
                        interaction_id,
                        target_id,
                        "uses_target",
                        "Task source passes the Target reference to this Interaction.",
                    )
            for reference_id in task_references:
                target_type = nodes.get(reference_id, ("", {}))[0]
                relation = {
                    "interaction": "uses_interaction",
                    "question": "asks_question",
                    "model": "uses_model",
                }.get(target_type)
                if relation:
                    add(
                        task["id"],
                        reference_id,
                        relation,
                        f"{target_type.capitalize()} reference found in the task source.",
                    )
        for interaction in result.interactions:
            for reference_id in interaction.get("references", []):
                add(
                    interaction["id"],
                    reference_id,
                    "uses_target",
                    "Target reference found in the interaction source.",
                )
        for question in result.questions:
            for reference_id in question.get("references", []):
                add(
                    question["id"],
                    reference_id,
                    "queries_target",
                    "Target reference found in the question source.",
                )
        return relationships

    @staticmethod
    def _matches_step(step_text: str, expression: str) -> bool:
        normalized_expression = re.sub(r"\{[^}]+\}|<[^>]+>", " ", expression)
        expression_words = set(_WORD_PATTERN.findall(normalized_expression.casefold()))
        step_words = set(_WORD_PATTERN.findall(step_text.casefold()))
        if not expression_words or not step_words:
            return False
        if normalized_expression.strip().casefold() in step_text.casefold():
            return True
        return expression_words <= step_words
