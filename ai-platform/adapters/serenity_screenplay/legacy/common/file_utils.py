import os
from pathlib import Path
from typing import Iterable

from core.common.constants import EXCLUDED_DIRS
from core.common.logger import get_logger
from core.common.models import SourceFile

logger = get_logger(__name__)


def iter_source_files(root: Path, suffixes: Iterable[str]) -> tuple[list[SourceFile], list[str]]:
    """Read supported files deterministically, pruning excluded trees during traversal."""
    files: list[SourceFile] = []
    errors: list[str] = []
    if not root.exists():
        return files, [f"Project root does not exist: {root}"]
    if not root.is_dir():
        return files, [f"Project root is not a directory: {root}"]
    allowed = {suffix.lower() for suffix in suffixes}
    candidates: list[Path] = []

    def record_walk_error(exc: OSError) -> None:
        message = f"Unable to enumerate {exc.filename or root}: {exc}"
        logger.warning(message)
        errors.append(message)

    for directory, subdirectories, filenames in os.walk(root, onerror=record_walk_error):
        subdirectories[:] = sorted(
            name for name in subdirectories if name not in EXCLUDED_DIRS
        )
        base = Path(directory)
        candidates.extend(
            base / filename for filename in filenames
            if Path(filename).suffix.lower() in allowed
        )

    for path in sorted(candidates, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            message = f"Unable to read {relative}: {exc}"
            logger.warning(message)
            errors.append(message)
            continue
        files.append(SourceFile(path, relative, content))
    return files, errors
