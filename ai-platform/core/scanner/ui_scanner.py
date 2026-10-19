from pathlib import Path

from core.common.file_utils import iter_source_files
from core.common.models import SourceFile


class UiScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (".java",))
        return [f for f in files if "userinterfaces" in f.relative_path.lower().replace("_", "").split("/") and "Target.the(" in f.content]
