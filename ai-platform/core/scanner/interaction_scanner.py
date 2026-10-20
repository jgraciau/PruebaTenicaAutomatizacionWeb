from pathlib import Path

from core.common.constants import JAVA_SUFFIX
from core.common.file_utils import iter_source_files
from core.common.models import SourceFile
from core.scanner.classification import is_interaction


class InteractionScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (JAVA_SUFFIX,))
        return [source for source in files if is_interaction(source)]
