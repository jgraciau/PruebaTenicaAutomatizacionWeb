"""Model for an actionable architecture recommendation."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Recommendation:
    category: str
    title: str
    action: str
    evidence: str
    severity: str = "medium"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
