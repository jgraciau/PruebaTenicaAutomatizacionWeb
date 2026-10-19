from pathlib import Path

from core.common.file_utils import iter_source_files
from core.common.models import SourceFile


class QuestionScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (".java",))
        return [f for f in files if "questions" in f.relative_path.lower().split("/") and "Question<" in f.content]
