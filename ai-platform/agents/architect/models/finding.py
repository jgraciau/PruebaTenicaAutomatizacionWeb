"""Model for an evidence-backed architecture finding."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Finding:
    id: str
    title: str
    description: str
    evidence: str
    severity: str = "medium"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
