from pathlib import Path

from core.common.constants import FEATURE_SUFFIX
from core.common.file_utils import iter_source_files
from core.common.models import SourceFile


class FeatureScanner:
    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (FEATURE_SUFFIX,))
        return files
