from dataclasses import dataclass, field
from typing import Any

from core.models.components import (
    FeatureModel,
    InteractionModel,
    QuestionModel,
    StepDefinitionModel,
    TaskModel,
)


@dataclass(slots=True)
class ArchitectureModel:
    project: dict[str, Any]
    features: list[FeatureModel] = field(default_factory=list)
    step_definitions: list[StepDefinitionModel] = field(default_factory=list)
    tasks: list[TaskModel] = field(default_factory=list)
    questions: list[QuestionModel] = field(default_factory=list)
    interactions: list[InteractionModel] = field(default_factory=list)
    user_interfaces: list[dict[str, Any]] = field(default_factory=list)
    models: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        from dataclasses import asdict

        return asdict(self)
