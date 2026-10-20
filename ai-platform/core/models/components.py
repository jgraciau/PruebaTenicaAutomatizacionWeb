from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FeatureModel:
    path: str
    name: str
    scenarios: list[dict[str, Any]] = field(default_factory=list)
    background: list[str] = field(default_factory=list)
    background_steps: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class StepDefinitionModel:
    path: str
    package: str
    name: str
    classes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    definitions: list[dict[str, str]] = field(default_factory=list)
    line_count: int = 0


@dataclass(slots=True)
class TaskModel:
    path: str
    package: str
    name: str
    classes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


@dataclass(slots=True)
class QuestionModel:
    path: str
    package: str
    name: str
    classes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InteractionModel:
    path: str
    package: str
    name: str
    classes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
