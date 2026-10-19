from typing import Any

from core.common.models import ScanResult
from core.parsers import feature_parser, interaction_parser, question_parser, step_parser, task_parser, ui_parser
from core.parsers.java_parser import parse_java


class ArchitectureBuilder:
    def build(self, scan: ScanResult) -> dict[str, Any]:
        features = [feature_parser.FeatureParser().parse(source) for source in scan.features]
        steps = [step_parser.parse(source) for source in scan.step_definitions]
        tasks = [task_parser.parse(source) for source in scan.tasks]
        questions = [question_parser.parse(source) for source in scan.questions]
        interactions = [interaction_parser.parse(source) for source in scan.interactions]
        uis = [ui_parser.parse(source) for source in scan.user_interfaces]
        models = [parse_java(source, "model") for source in scan.models]
        return {
            "project": {"name": scan.root.name, "root": ".", "language": "Java", "frameworks": ["Serenity BDD", "Cucumber", "Gradle", "Screenplay"], "source_files_scanned": len(scan.project_files), "scan_errors": list(scan.errors)},
            "features": features,
            "step_definitions": steps,
            "tasks": tasks,
            "questions": questions,
            "interactions": interactions,
            "user_interfaces": uis,
            "models": models,
        }
