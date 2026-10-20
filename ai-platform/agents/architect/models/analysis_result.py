"""Aggregate result produced by the Architect Agent pipeline."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AnalysisResult:
    maps: dict[str, dict[str, Any]] = field(default_factory=dict)
    analyses: dict[str, dict[str, Any]] = field(default_factory=dict)
    scores: dict[str, Any] = field(default_factory=dict)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "maps": self.maps,
            "analyses": self.analyses,
            "scores": self.scores,
            "recommendations": self.recommendations,
            "errors": self.errors,
        }
