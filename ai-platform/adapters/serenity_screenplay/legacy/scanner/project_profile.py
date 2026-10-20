import logging
from dataclasses import dataclass
from pathlib import Path

from adapters.serenity_screenplay.legacy.common.constants import FEATURE_SUFFIX, JAVA_SUFFIX
from adapters.serenity_screenplay.legacy.common.file_utils import iter_source_files
from adapters.serenity_screenplay.legacy.common.logger import get_logger
from adapters.serenity_screenplay.legacy.common.models import ScanResult, SourceFile
from adapters.serenity_screenplay.legacy.scanner.classification import (
    is_interaction,
    is_question,
    is_step_definition,
    is_task,
    is_user_interface,
)
from adapters.serenity_screenplay.legacy.scanner.model_scanner import ModelScanner

logger: logging.Logger = get_logger(__name__)

_SCREENPLAY_MARKERS = (
    "implements Task",
    "extends Task",
    "Question<",
    "implements Interaction",
    "extends Interaction",
    "OnStage",
    "Actor",
)


def _unique_directories(sources: tuple[SourceFile, ...]) -> list[str]:
    return sorted({str(Path(source.relative_path).parent).replace("\\", "/") for source in sources})


@dataclass(frozen=True, slots=True)
class ProjectProfile:
    """Preflight findings and source inventory used to configure the full scan."""

    scan: ScanResult
    frameworks: tuple[str, ...]
    readiness: str
    conventions: dict[str, list[str]]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "project": self.scan.root.name,
            "root": str(self.scan.root),
            "readiness": self.readiness,
            "frameworks": list(self.frameworks),
            "inventory": {
                "source_files": len(self.scan.project_files),
                "features": len(self.scan.features),
                "step_definitions": len(self.scan.step_definitions),
                "tasks": len(self.scan.tasks),
                "questions": len(self.scan.questions),
                "interactions": len(self.scan.interactions),
                "user_interfaces": len(self.scan.user_interfaces),
                "models": len(self.scan.models),
            },
            "conventions": self.conventions,
            "warnings": [*self.warnings, *self.scan.errors],
            "scan_plan": {
                "language_extensions": [JAVA_SUFFIX, FEATURE_SUFFIX],
                "component_paths": self.conventions,
                "auto_adapted": True,
                "source_files_modified": False,
            },
        }


class ProjectProfileAnalyzer:
    """Validate project structure and infer safe runtime classification rules."""

    def analyze(self, root: Path) -> ProjectProfile:
        root = root.resolve()
        files, errors = iter_source_files(root, (JAVA_SUFFIX, FEATURE_SUFFIX))
        java_files = tuple(
            source
            for source in files
            if source.path.suffix.lower() == JAVA_SUFFIX
        )
        features = tuple(
            source
            for source in files
            if source.path.suffix.lower() == FEATURE_SUFFIX
        )
        steps = tuple(source for source in java_files if is_step_definition(source))
        tasks = tuple(source for source in java_files if is_task(source))
        questions = tuple(source for source in java_files if is_question(source))
        interactions = tuple(
            source for source in java_files if is_interaction(source)
        )
        user_interfaces = tuple(
            source for source in java_files if is_user_interface(source)
        )
        models = tuple(
            source for source in java_files if ModelScanner.is_model(source)
        )
        scan = ScanResult(
            root=root,
            project_files=tuple(files),
            features=features,
            step_definitions=steps,
            tasks=tasks,
            questions=questions,
            interactions=interactions,
            user_interfaces=user_interfaces,
            models=models,
            errors=tuple(errors),
        )
        frameworks = self._frameworks(root, files, features, java_files)
        warnings: list[str] = []
        if not java_files:
            warnings.append("No se encontraron archivos Java.")
        if not features:
            warnings.append("No se encontraron archivos Gherkin Feature.")
        if not steps:
            warnings.append("No se detectaron Step Definitions Cucumber.")
        if not tasks and not questions and not interactions:
            warnings.append("No se detectaron componentes Screenplay.")
        readiness = (
            "ready"
            if java_files and features and steps and (tasks or questions or interactions)
            else "partial"
            if java_files or features
            else "unsupported"
        )
        conventions = {
            "features": _unique_directories(features),
            "step_definitions": _unique_directories(steps),
            "tasks": _unique_directories(tasks),
            "questions": _unique_directories(questions),
            "interactions": _unique_directories(interactions),
            "user_interfaces": _unique_directories(user_interfaces),
            "models": _unique_directories(models),
        }
        logger.info(
            "Project preflight: %s (%s), %d Java, %d Feature, frameworks=%s",
            root.name,
            readiness,
            len(java_files),
            len(features),
            ", ".join(frameworks) or "none detected",
        )
        return ProjectProfile(
            scan=scan,
            frameworks=frameworks,
            readiness=readiness,
            conventions=conventions,
            warnings=tuple(warnings),
        )

    @staticmethod
    def _frameworks(
        root: Path,
        files: list[SourceFile],
        features: tuple[SourceFile, ...],
        java_files: tuple[SourceFile, ...],
    ) -> tuple[str, ...]:
        source_text = "\n".join(source.content for source in files).lower()
        detected: list[str] = []
        if "serenity" in source_text:
            detected.append("Serenity BDD")
        if features or "io.cucumber" in source_text or "@given" in source_text:
            detected.append("Cucumber")
        if any(
            (root / filename).is_file()
            for filename in (
                "build.gradle",
                "build.gradle.kts",
                "settings.gradle",
                "settings.gradle.kts",
            )
        ):
            detected.append("Gradle")
        if (root / "pom.xml").is_file():
            detected.append("Maven")
        if any(
            marker in source.content
            for source in java_files
            for marker in _SCREENPLAY_MARKERS
        ):
            detected.append("Screenplay")
        return tuple(detected)
