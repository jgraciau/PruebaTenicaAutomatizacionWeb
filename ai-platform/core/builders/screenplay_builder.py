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
        )
        patterns = [
            ("Cucumber Gherkin", "Cucumber Gherkin", metrics["features"], "Feature files and parsed scenarios", "Archivos Feature y escenarios analizados"),
            ("Cucumber Step Definitions", "Definiciones de pasos Cucumber", metrics["step_definitions"], "Java classes with Cucumber annotations or stepDefinitions path", "Clases Java con anotaciones Cucumber o ubicadas en stepDefinitions"),
            ("Screenplay Tasks", "Tasks de Screenplay", metrics["tasks"], "Java classes in task package implementing Task", "Clases Java del paquete tasks que implementan Task"),
            ("Screenplay Questions", "Questions de Screenplay", metrics["questions"], "Java classes in questions package using Question<T>", "Clases Java del paquete questions que usan Question<T>"),
            ("Screenplay Interactions", "Interactions de Screenplay", metrics["interactions"], "Java classes in interactions package", "Clases Java del paquete interactions"),
            ("Screenplay User Interfaces", "Interfaces de usuario Screenplay", metrics["user_interfaces"], "Java classes in userInterfaces package with Target", "Clases Java del paquete userInterfaces con Target"),
        ]
        return {
            "patterns_detected": [
                {"pattern": pattern, "pattern_es": pattern_es, "count": count, "evidence": evidence, "evidence_es": evidence_es}
                for pattern, pattern_es, count, evidence, evidence_es in patterns
            ],
            "relationships": {
                "feature_to_step_definition": dependencies["feature_to_step_definition"],
                "step_definition_to_task": dependencies["step_definition_to_task"],
                "task_to_interaction": dependencies["task_to_interaction"],
                "task_to_question": dependencies["task_to_question"],
            },
            "metrics": metrics,
            "relationship_semantics": {
                "observed": "referencias directas a tipos Java extraídas del código fuente",
                "heuristic": "coincidencia textual normalizada entre pasos Gherkin y expresiones de anotaciones Cucumber",
                "observed_en": "direct Java type references extracted from source",
                "heuristic_en": "normalized text matching between Gherkin steps and Cucumber annotation expressions",
            },
        }
