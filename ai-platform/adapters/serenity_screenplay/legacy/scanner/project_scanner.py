import logging
from pathlib import Path

from core.common.constants import JAVA_SUFFIX
from core.common.logger import get_logger
from core.common.models import ScanResult
from core.scanner.project_profile import ProjectProfile, ProjectProfileAnalyzer

logger: logging.Logger = get_logger(__name__)


class ProjectScanner:
    """Discover Java/Gherkin files and classify framework artifacts."""

    def scan(
        self,
        root: Path,
        profile: ProjectProfile | None = None,
    ) -> ScanResult:
        profile = profile or ProjectProfileAnalyzer().analyze(root)
        if profile.scan.root != root.resolve():
            raise ValueError("The project profile root does not match the scan root.")
        scan = profile.scan
        logger.info(
            "Discovered %d source files (%d feature, %d Java)",
            len(scan.project_files),
            len(scan.features),
            sum(
                source.path.suffix.lower() == JAVA_SUFFIX
                for source in scan.project_files
            ),
        )
        return scan
