from pathlib import Path

from core.common.file_utils import iter_source_files
from core.common.logger import get_logger
from core.common.models import ScanResult, SourceFile

logger = get_logger(__name__)


def _is_step_definition(source: SourceFile) -> bool:
    return "stepdefinitions" in source.relative_path.lower().replace("_", "") or any(
        token in source.content for token in ("@Given(", "@When(", "@Then(", "@And(", "@But(")
    )


def _is_screenplay(source: SourceFile, component: str, markers: tuple[str, ...]) -> bool:
    path_parts = source.relative_path.lower().replace("_", "").split("/")
    in_package = component in path_parts
    in_semantic_package = component.rstrip("s") in path_parts
    return (in_package or in_semantic_package) and any(marker in source.content for marker in markers)


class ProjectScanner:
    """Discover Java/Gherkin files and classify framework artifacts."""

    def scan(self, root: Path) -> ScanResult:
        root = root.resolve()
        files, errors = iter_source_files(root, (".java", ".feature"))
        java_files = [f for f in files if f.path.suffix.lower() == ".java"]
        feature_files = [f for f in files if f.path.suffix.lower() == ".feature"]
        steps = [f for f in java_files if _is_step_definition(f)]
        tasks = [f for f in java_files if not _is_step_definition(f) and _is_screenplay(f, "tasks", ("implements Task", "extends Task"))]
        questions = [f for f in java_files if _is_screenplay(f, "questions", ("implements Question", "implements Question<", "Question<"))]
        interactions = [f for f in java_files if _is_screenplay(f, "interactions", ("implements Interaction", "implements Task", "Interaction.call", "Interaction.where"))]
        uis = [f for f in java_files if _is_screenplay(f, "userinterfaces", ("Target.the(", "Target.empty()", "Target.named("))]
        models = [f for f in java_files if "models" in f.relative_path.lower().split("/")]
        logger.info("Discovered %d source files (%d feature, %d Java)", len(files), len(feature_files), len(java_files))
        return ScanResult(root, tuple(files), tuple(feature_files), tuple(steps), tuple(tasks), tuple(questions), tuple(interactions), tuple(uis), tuple(models), tuple(errors))
