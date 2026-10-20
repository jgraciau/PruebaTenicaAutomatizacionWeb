from pathlib import Path

from adapters.serenity_screenplay.legacy.common.constants import JAVA_SUFFIX
from adapters.serenity_screenplay.legacy.common.file_utils import iter_source_files
from adapters.serenity_screenplay.legacy.common.models import SourceFile
from adapters.serenity_screenplay.legacy.scanner.classification import is_task


class TaskScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (JAVA_SUFFIX,))
        return [source for source in files if is_task(source)]
