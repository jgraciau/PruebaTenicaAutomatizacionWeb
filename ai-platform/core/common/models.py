from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceFile:
    path: Path
    relative_path: str
    content: str


@dataclass(frozen=True, slots=True)
class ScanResult:
    root: Path
    project_files: tuple[SourceFile, ...]
    features: tuple[SourceFile, ...]
    step_definitions: tuple[SourceFile, ...]
    tasks: tuple[SourceFile, ...]
    questions: tuple[SourceFile, ...]
    interactions: tuple[SourceFile, ...]
    user_interfaces: tuple[SourceFile, ...]
    models: tuple[SourceFile, ...]
    errors: tuple[str, ...] = ()
