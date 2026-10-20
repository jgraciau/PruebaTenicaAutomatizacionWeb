import re
from collections import defaultdict
from typing import Any

from adapters.serenity_screenplay.legacy.models import DependencyModel

_CUCUMBER_TYPES: dict[str, str] = {
    "string": r'"[^"\\]*(?:\\.[^"\\]*)*"',
    "int": r"-?\d+",
    "float": r"-?\d+(?:\.\d+)?",
    "double": r"-?\d+(?:\.\d+)?",
    "word": r"\S+",
}


def _cucumber_expression_pattern(expression: str) -> str:
    pattern = re.escape(expression.strip())
    for name, replacement in _CUCUMBER_TYPES.items():
        pattern = pattern.replace(re.escape("{" + name + "}"), replacement)
    return pattern


def _matches_expression(step_text: str, expression: str) -> bool:
    """Match exact regex or common Cucumber expressions; abstain on unsupported syntax."""
    expression = expression.strip()
    if expression.startswith("^") or expression.endswith("$") or ".*" in expression or ".+" in expression or "([" in expression:
        try:
            return re.fullmatch(expression, step_text, flags=re.IGNORECASE) is not None
        except re.error:
            return False
    if re.search(r"\{(?!string\}|int\}|float\}|double\}|word\})", expression):
        return False
    try:
        return re.fullmatch(_cucumber_expression_pattern(expression), step_text, flags=re.IGNORECASE) is not None
    except re.error:
        return False


def _component_link(
    source: dict[str, Any],
    target: dict[str, Any],
    source_type: str,
    target_type: str,
    evidence: str,
) -> dict[str, str]:
    return DependencyModel(
        source=str(source["path"]),
        target=str(target["path"]),
        source_type=source_type,
        target_type=target_type,
        relation="observed",
        evidence=evidence,
    ).to_dict()


def _matched_feature_links(architecture: dict[str, Any]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []

    def add_links(
        feature: dict[str, Any],
        scenario_name: str,
        step: dict[str, Any],
    ) -> None:
        for step_definition in architecture["step_definitions"]:
            if any(
                _matches_expression(step["text"], definition["expression"])
                for definition in step_definition["definitions"]
            ):
                links.append(
                    DependencyModel(
                        source=feature["path"],
                        target=step_definition["path"],
                        source_type="feature",
                        target_type="step_definition",
                        relation="heuristic",
                        evidence="complete Gherkin step matched annotated expression",
                        feature=feature["path"],
                        scenario=scenario_name,
                        gherkin_step=step["text"],
                    ).to_dict()
                )

    for feature in architecture["features"]:
        for scenario in feature["scenarios"]:
            for step in scenario["steps"]:
                add_links(feature, scenario["name"], step)
        background_steps = feature.get("background_steps")
        if background_steps is None:
            background_steps = [
                {"text": text} for text in feature.get("background", [])
            ]
        for step in background_steps:
            add_links(feature, "Background", step)
    return sorted(links, key=_link_key)


class DependencyBuilder:
    """Build traceable observed references and heuristic feature-step links."""

    def build(self, architecture: dict[str, Any]) -> dict[str, Any]:
        steps = architecture["step_definitions"]
        tasks = architecture["tasks"]
        questions = architecture["questions"]
        interactions = architecture["interactions"]
        user_interfaces = architecture["user_interfaces"]
        models = architecture["models"]

        feature_links = _matched_feature_links(architecture)
        step_task_links = [
            _component_link(step, task, "step_definition", "task", "Java source references task type")
            for step in steps for task in tasks
            if task["name"] in step.get("references", [])
        ]
        step_question_links = [
            _component_link(step, question, "step_definition", "question", "Java source references question type")
            for step in steps for question in questions
            if question["name"] in step.get("references", [])
        ]
        step_model_links = [
            _component_link(step, model, "step_definition", "model", "Java source references model type")
            for step in steps for model in models
            if model["name"] in step.get("references", [])
        ]
        task_interaction_links = [
            _component_link(task, interaction, "task", "interaction", "Java source references interaction type")
            for task in tasks for interaction in interactions
            if interaction["name"] in task.get("references", [])
        ]
        task_question_links = [
            _component_link(task, question, "task", "question", "Java source references question type")
            for task in tasks for question in questions
            if question["name"] in task.get("references", [])
        ]
        task_ui_links = [
            _component_link(task, ui, "task", "user_interface", "Java source references user-interface type")
            for task in tasks for ui in user_interfaces
            if ui["name"] in task.get("references", [])
        ]
        task_model_links = [
            _component_link(task, model, "task", "model", "Java source references model type")
            for task in tasks for model in models
            if model["name"] in task.get("references", [])
        ]
        interaction_ui_links = [
            _component_link(interaction, ui, "interaction", "user_interface", "Java source references user-interface type")
            for interaction in interactions for ui in user_interfaces
            if ui["name"] in interaction.get("references", [])
        ]

        collections = {
            "feature_to_step_definition": feature_links,
            "step_definition_to_task": sorted(step_task_links, key=_link_key),
            "step_definition_to_question": sorted(step_question_links, key=_link_key),
            "step_definition_to_model": sorted(step_model_links, key=_link_key),
            "task_to_interaction": sorted(task_interaction_links, key=_link_key),
            "task_to_question": sorted(task_question_links, key=_link_key),
            "task_to_user_interface": sorted(task_ui_links, key=_link_key),
            "task_to_model": sorted(task_model_links, key=_link_key),
            "interaction_to_user_interface": sorted(interaction_ui_links, key=_link_key),
        }
        collections["dependency_chain"] = _build_dependency_chains(collections)
        collections["notes"] = [
            "Las asociaciones Feature → Step Definition son heurísticas y requieren validación; las referencias directas de tipos Java son observadas.",
            "Los vínculos hacia User Interfaces y Models solo se incluyen cuando se encuentran referencias directas en el código fuente.",
        ]
        return collections


def _build_dependency_chains(collections: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    tasks_by_step: dict[str, list[dict[str, str]]] = defaultdict(list)
    interactions_by_task: dict[str, list[dict[str, str]]] = defaultdict(list)
    for link in collections["step_definition_to_task"]:
        tasks_by_step[link["source"]].append(link)
    for link in collections["task_to_interaction"]:
        interactions_by_task[link["source"]].append(link)

    chains: list[dict[str, Any]] = []
    for feature_link in collections["feature_to_step_definition"]:
        step_path = feature_link["target"]
        for task_link in tasks_by_step.get(step_path, []):
            task_path = task_link["target"]
            matching_interactions = interactions_by_task.get(task_path, [])
            for interaction_link in matching_interactions or [None]:
                chains.append(
                    {
                        "feature": feature_link["feature"],
                        "scenario": feature_link["scenario"],
                        "step_definition": step_path,
                        "task": task_path,
                        "interaction": (
                            interaction_link["target"]
                            if interaction_link is not None
                            else None
                        ),
                        "evidence": (
                            "Feature→Step heurístico; Step→Task y Task→Interaction observados."
                            if interaction_link is not None
                            else "Feature→Step heurístico; Step→Task observado; Interaction no detectada."
                        ),
                    }
                )
    return sorted(
        chains,
        key=lambda item: (
            item["feature"],
            item["scenario"],
            item["step_definition"],
            item["task"],
            item["interaction"] or "",
        ),
    )


def _link_key(link: dict[str, str]) -> tuple[str, str]:
    return link.get("source", link.get("feature", "")), link.get("target", link.get("step_definition", ""))
