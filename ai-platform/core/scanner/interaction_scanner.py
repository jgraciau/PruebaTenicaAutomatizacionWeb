from pathlib import Path

from core.common.file_utils import iter_source_files
from core.common.models import SourceFile


class InteractionScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (".java",))
        return [f for f in files if "interactions" in f.relative_path.lower().split("/") and any(x in f.content for x in ("Interaction", "implements Task"))]
