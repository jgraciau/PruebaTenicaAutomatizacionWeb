from pathlib import Path

from core.common.file_utils import iter_source_files
from core.common.models import SourceFile


class StepScanner:
    ANNOTATIONS = ("@Given(", "@When(", "@Then(", "@And(", "@But(")

    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (".java",))
        return [f for f in files if "stepdefinitions" in f.relative_path.lower().replace("_", "") or any(a in f.content for a in self.ANNOTATIONS)]
