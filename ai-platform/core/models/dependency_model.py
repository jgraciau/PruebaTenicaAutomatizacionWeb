from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyModel:
    source_id: str
    target_id: str
    source_type: str
    target_type: str
    relation: str
    evidence: str
