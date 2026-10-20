"""Typed domain models used to assemble framework knowledge maps."""

from adapters.serenity_screenplay.legacy.models.architecture import ArchitectureModel
from adapters.serenity_screenplay.legacy.models.components import (
    FeatureModel,
    InteractionModel,
    QuestionModel,
    StepDefinitionModel,
    TaskModel,
)
from adapters.serenity_screenplay.legacy.models.dependency import DependencyModel

__all__ = [
    "ArchitectureModel",
    "DependencyModel",
    "FeatureModel",
    "InteractionModel",
    "QuestionModel",
    "StepDefinitionModel",
    "TaskModel",
]
