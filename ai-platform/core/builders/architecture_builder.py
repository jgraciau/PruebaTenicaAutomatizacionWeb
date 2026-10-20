from collections import defaultdict
from dataclasses import asdict
from typing import Any

from core.common.models import ScanResult
from core.models import (
    ArchitectureModel,
    FeatureModel,
    InteractionModel,
    QuestionModel,
    StepDefinitionModel,
    TaskModel,
)
from core.parsers import (
    feature_parser,
    interaction_parser,
    model_parser,
    question_parser,
    step_parser,
    task_parser,
    ui_parser,
)


def _detect_frameworks(scan: ScanResult) -> list[str]:
    source_text = "\n".join(source.content for source in scan.project_files).lower()
    frameworks: list[str] = []
    if "serenity" in source_text:
        frameworks.append("Serenity BDD")
    if scan.features or "io.cucumber" in source_text:
        frameworks.append("Cucumber")
    if any(
        (scan.root / filename).is_file()
        for filename in (
            "build.gradle",
            "build.gradle.kts",
            "settings.gradle",
            "settings.gradle.kts",
        )
    ):
        frameworks.append("Gradle")
    if (scan.root / "pom.xml").is_file():
        frameworks.append("Maven")
    if scan.tasks or scan.questions or scan.interactions or scan.user_interfaces:
        frameworks.append("Screenplay")
    return frameworks


class ArchitectureBuilder:
    """Assemble typed parsed components into the stable architecture map."""

    def build(self, scan: ScanResult) -> dict[str, Any]:
        features = [
            asdict(FeatureModel(**feature_parser.FeatureParser().parse(source)))
            for source in scan.features
        ]
        steps = [
            asdict(StepDefinitionModel(**step_parser.parse(source)))
            for source in scan.step_definitions
        ]
        tasks = [asdict(TaskModel(**task_parser.parse(source))) for source in scan.tasks]
        questions = [
            asdict(QuestionModel(**question_parser.parse(source)))
            for source in scan.questions
        ]
        interactions = [
            asdict(InteractionModel(**interaction_parser.parse(source)))
            for source in scan.interactions
        ]
        user_interfaces = [ui_parser.parse(source) for source in scan.user_interfaces]
        models = [model_parser.parse(source) for source in scan.models]
        architecture = ArchitectureModel(
            project={
                "name": scan.root.name,
                "root": ".",
                "language": (
                    "Java"
                    if any(source.path.suffix.lower() == ".java" for source in scan.project_files)
                    else "Gherkin"
                    if scan.features
                    else "unknown"
                ),
                "frameworks": _detect_frameworks(scan),
                "source_files_scanned": len(scan.project_files),
                "scan_errors": list(scan.errors),
            },
            features=features,
            step_definitions=steps,
            tasks=tasks,
            questions=questions,
            interactions=interactions,
            user_interfaces=user_interfaces,
            models=models,
        )
        return asdict(architecture)

    @staticmethod
    def add_quality_audit(
        architecture: dict[str, Any], dependencies: dict[str, Any]
    ) -> dict[str, Any]:
        """Add deterministic orphan, duplicate and risk findings to an architecture map."""
        nodes: dict[str, str] = {}
        category_keys = (
            ("features", "feature"),
            ("step_definitions", "step_definition"),
            ("tasks", "task"),
            ("questions", "question"),
            ("interactions", "interaction"),
            ("user_interfaces", "user_interface"),
            ("models", "model"),
        )
        duplicate_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
        for category, node_type in category_keys:
            for item in architecture[category]:
                path = str(item["path"])
                name = str(item["name"])
                nodes[path] = node_type
                duplicate_groups[(category, name)].append(path)
        duplicate_findings = [
            {"component_type": category, "name": name, "paths": sorted(paths)}
            for (category, name), paths in sorted(duplicate_groups.items())
            if len(paths) > 1
        ]
        edges: list[tuple[str, str]] = []
        for links in dependencies.values():
            if not isinstance(links, list):
                continue
            for link in links:
                if not isinstance(link, dict):
                    continue
                source = link.get("feature", link.get("source", ""))
                target = link.get("step_definition", link.get("target", ""))
                if source in nodes and target in nodes:
                    edges.append((source, target))
        connected = {path for edge in edges for path in edge}
        orphaned = [
            {"component_type": nodes[path], "name": str(item["name"]), "path": path}
            for category, _ in category_keys
            for item in architecture[category]
            if (path := str(item["path"])) not in connected
        ]
        risks: list[dict[str, str]] = []
        if architecture["project"]["scan_errors"]:
            risks.append({
                "severity": "high",
                "code": "SOURCE_SCAN_ERRORS",
                "description": "Hay archivos fuente que no pudieron analizarse.",
            })
        if not architecture["features"]:
            risks.append({
                "severity": "high",
                "code": "NO_FEATURES",
                "description": "No se detectaron archivos Feature.",
            })
        if not architecture["step_definitions"]:
            risks.append({
                "severity": "high",
                "code": "NO_STEP_DEFINITIONS",
                "description": "No se detectaron definiciones de pasos Cucumber.",
            })
        if not architecture["tasks"]:
            risks.append({
                "severity": "medium",
                "code": "NO_TASKS",
                "description": "No se detectaron Tasks de Screenplay.",
            })
        if orphaned:
            risks.append({
                "severity": "medium",
                "code": "ORPHAN_COMPONENTS",
                "description": f"Se detectaron {len(orphaned)} componentes sin relaciones conocidas.",
            })
        if duplicate_findings:
            risks.append({
                "severity": "medium",
                "code": "DUPLICATE_COMPONENTS",
                "description": f"Se detectaron {len(duplicate_findings)} nombres duplicados dentro de categorías.",
            })
        architecture["quality"] = {
            "orphaned_components": sorted(orphaned, key=lambda item: item["path"]),
            "duplicate_components": duplicate_findings,
            "risks": risks,
        }
        return architecture
