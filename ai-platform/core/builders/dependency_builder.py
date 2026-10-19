import re
from typing import Any


_CUCUMBER_TYPES = {
    "string": r'"[^"\\]*(?:\\.[^"\\]*)*"',
    "int": r"-?\d+",
    "float": r"-?\d+(?:\.\d+)?",
    "double": r"-?\d+(?:\.\d+)?",
    "word": r"\S+",
}


def _cucumber_expression_pattern(expression: str) -> str:
    pattern = re.escape(expression.strip())
    for name, replacement in _CUCUMBER_TYPES.items():
        placeholder = re.escape("{" + name + "}")
        pattern = pattern.replace(placeholder, replacement)
    return pattern


def _matches_expression(step_text: str, expression: str) -> bool:
    """Match exact regex or common Cucumber expressions; abstain on unsupported syntax."""
    expression = expression.strip()
    if (
        expression.startswith("^")
        or expression.endswith("$")
        or ".*" in expression
        or ".+" in expression
        or "([" in expression
    ):
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


class DependencyBuilder:
    """Build conservative, traceable links from static source references."""

    def build(self, architecture: dict[str, Any]) -> dict[str, Any]:
        steps = architecture["step_definitions"]
        tasks = architecture["tasks"]
        questions = architecture["questions"]
        interactions = architecture["interactions"]
        feature_links: list[dict[str, str]] = []
        for feature in architecture["features"]:
            for scenario in feature["scenarios"]:
                for gherkin_step in scenario["steps"]:
                    candidates = [
                        step for step in steps
                        if any(_matches_expression(gherkin_step["text"], definition["expression"])
                               for definition in step["definitions"])
                    ]
                    for step in candidates:
                        feature_links.append({
                            "feature": feature["path"],
                            "scenario": scenario["name"],
                            "step_definition": step["path"],
                            "gherkin_step": gherkin_step["text"],
                            "relation": "heuristic",
                            "evidence": "complete Gherkin step matched annotated expression",
                        })
        step_links = [
            _link(step["path"], task["path"], "step_definition", "task", "observed", "Java source references task type")
            for step in steps for task in tasks
            if task["name"] in step.get("references", [])
        ]
        task_interaction_links = [
            _link(task["path"], interaction["path"], "task", "interaction", "observed", "Java source references interaction type")
            for task in tasks for interaction in interactions
            if interaction["name"] in task.get("references", [])
        ]
        task_question_links = [
            _link(task["path"], question["path"], "task", "question", "observed", "Java source references question type")
            for task in tasks for question in questions
            if question["name"] in task.get("references", [])
        ]
        return {
            "feature_to_step_definition": sorted(feature_links, key=_link_key),
            "step_definition_to_task": sorted(step_links, key=_link_key),
            "task_to_interaction": sorted(task_interaction_links, key=_link_key),
            "task_to_question": sorted(task_question_links, key=_link_key),
            "notes": ["Feature-to-step matching supports common regex and Cucumber {string}, {int}, {float}, {double}, and {word} expressions. Unsupported parameter types are not guessed. Java type references are observed; feature links are heuristic."],
        }


def _link(source: str, target: str, source_type: str, target_type: str, relation: str, evidence: str) -> dict[str, str]:
    return {"source": source, "target": target, "source_type": source_type, "target_type": target_type, "relation": relation, "evidence": evidence}


def _link_key(link: dict[str, str]) -> tuple[str, str]:
    return link.get("source", link.get("feature", "")), link.get("target", link.get("step_definition", ""))
