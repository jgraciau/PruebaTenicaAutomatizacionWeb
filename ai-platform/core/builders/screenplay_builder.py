from typing import Any


class ScreenplayBuilder:
    def build(self, architecture: dict[str, Any], dependencies: dict[str, Any]) -> dict[str, Any]:
        categories = ("features", "step_definitions", "tasks", "questions", "interactions", "user_interfaces", "models")
        metrics = {key: len(architecture[key]) for key in categories}
        metrics["scenarios"] = sum(len(feature["scenarios"]) for feature in architecture["features"])
        metrics["gherkin_steps"] = sum(
            len(scenario["steps"])
            for feature in architecture["features"]
            for scenario in feature["scenarios"]
        ) + sum(
            len(feature.get("background_steps", feature.get("background", [])))
            for feature in architecture["features"]
        )
        return {
            "patterns_detected": [
                {"pattern": "Cucumber Gherkin", "count": metrics["features"], "evidence": "Feature files and parsed scenarios"},
                {"pattern": "Cucumber Step Definitions", "count": metrics["step_definitions"], "evidence": "Java classes with Cucumber annotations or stepDefinitions path"},
                {"pattern": "Screenplay Tasks", "count": metrics["tasks"], "evidence": "Java classes in task package implementing Task"},
                {"pattern": "Screenplay Questions", "count": metrics["questions"], "evidence": "Java classes in questions package using Question<T>"},
                {"pattern": "Screenplay Interactions", "count": metrics["interactions"], "evidence": "Java classes in interactions package"},
                {"pattern": "Screenplay User Interfaces", "count": metrics["user_interfaces"], "evidence": "Java classes in userInterfaces package with Target"},
            ],
            "relationships": {
                "feature_to_step_definition": dependencies["feature_to_step_definition"],
                "step_definition_to_task": dependencies["step_definition_to_task"],
                "task_to_interaction": dependencies["task_to_interaction"],
                "task_to_question": dependencies["task_to_question"],
                "step_definition_to_model": dependencies.get(
                    "step_definition_to_model", []
                ),
            },
            "metrics": metrics,
            "relationship_semantics": {"observed": "direct Java type references extracted from source", "heuristic": "normalized text matching between Gherkin steps and Cucumber annotation expressions"},
        }
