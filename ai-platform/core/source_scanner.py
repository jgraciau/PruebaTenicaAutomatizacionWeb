import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


_EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        ".gradle",
        ".idea",
        ".vscode",
        "__pycache__",
        ".pytest_cache",
        "build",
        "dist",
        "node_modules",
        "out",
        "target",
        "venv",
        ".venv",
    }
)


@dataclass(frozen=True, slots=True)
class SourceDocument:
    path: Path
    relative_path: str
    content: str


class SourceScanner:
    """Read configured source locations without interpreting their language."""

    def scan(
        self,
        locations: Iterable[Path],
        suffixes: Iterable[str],
        project_root: Path,
    ) -> tuple[list[SourceDocument], list[str]]:
        accepted_suffixes = {suffix.lower() for suffix in suffixes}
        documents: list[SourceDocument] = []
        errors: list[str] = []
        candidates: set[Path] = set()

        def record_walk_error(error: OSError) -> None:
            errors.append(f"Unable to enumerate {error.filename}: {error}")

        for location in locations:
            if not location.exists():
                errors.append(f"Configured source path does not exist: {location}")
                continue
            if location.is_file():
                if location.suffix.lower() in accepted_suffixes:
                    candidates.add(location)
                continue
            if not location.is_dir():
                errors.append(
                    f"Configured source is not a file or directory: {location}"
                )
                continue
            for current, children, names in os.walk(
                location,
                onerror=record_walk_error,
            ):
                children[:] = sorted(
                    child for child in children if child not in _EXCLUDED_DIRECTORIES
                )
                candidates.update(
                    Path(current) / name
                    for name in names
                    if Path(name).suffix.lower() in accepted_suffixes
                )
        for path in sorted(candidates, key=lambda item: item.as_posix().casefold()):
            try:
                content = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as exc:
                try:
                    relative = path.relative_to(project_root).as_posix()
                except ValueError:
                    relative = path.name
                errors.append(f"Unable to read {relative}: {exc}")
                continue
            try:
                relative_path = path.relative_to(project_root).as_posix()
            except ValueError:
                relative_path = path.name
            documents.append(SourceDocument(path, relative_path, content))
        return documents, errors
