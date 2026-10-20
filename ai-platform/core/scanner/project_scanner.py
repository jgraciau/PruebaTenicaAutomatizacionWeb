import logging
from pathlib import Path

from core.common.constants import FEATURE_SUFFIX, JAVA_SUFFIX
from core.common.file_utils import iter_source_files
from core.common.logger import get_logger
from core.common.models import ScanResult
from core.scanner.classification import (
    is_interaction,
    is_question,
    is_step_definition,
    is_task,
    is_user_interface,
)
from core.scanner.model_scanner import ModelScanner

logger: logging.Logger = get_logger(__name__)


class ProjectScanner:
    """Discover Java/Gherkin files and classify framework artifacts."""

    def scan(self, root: Path) -> ScanResult:
        root = root.resolve()
        files, errors = iter_source_files(root, (JAVA_SUFFIX, FEATURE_SUFFIX))
        java_files = [f for f in files if f.path.suffix.lower() == JAVA_SUFFIX]
        feature_files = [f for f in files if f.path.suffix.lower() == FEATURE_SUFFIX]
        steps = [source for source in java_files if is_step_definition(source)]
        tasks = [source for source in java_files if is_task(source)]
        questions = [source for source in java_files if is_question(source)]
        interactions = [source for source in java_files if is_interaction(source)]
        uis = [source for source in java_files if is_user_interface(source)]
        models = [f for f in java_files if ModelScanner.is_model(f)]
        logger.info(
            "Discovered %d source files (%d feature, %d Java)",
            len(files),
            len(feature_files),
            len(java_files),
        )
        return ScanResult(
            root,
            tuple(files),
            tuple(feature_files),
            tuple(steps),
            tuple(tasks),
            tuple(questions),
            tuple(interactions),
            tuple(uis),
            tuple(models),
            tuple(errors),
        )
