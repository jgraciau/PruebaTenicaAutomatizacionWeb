from dataclasses import dataclass, field
from typing import Any

from core.models.project_model import ProjectModel


@dataclass(slots=True)
class ProjectKnowledge:
    project: ProjectModel
    source_files_scanned: int = 0
    features: list[dict[str, Any]] = field(default_factory=list)
    step_definitions: list[dict[str, Any]] = field(default_factory=list)
    actors: list[dict[str, Any]] = field(default_factory=list)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    questions: list[dict[str, Any]] = field(default_factory=list)
    interactions: list[dict[str, Any]] = field(default_factory=list)
    targets: list[dict[str, Any]] = field(default_factory=list)
    models: list[dict[str, Any]] = field(default_factory=list)
    scan_errors: list[str] = field(default_factory=list)
