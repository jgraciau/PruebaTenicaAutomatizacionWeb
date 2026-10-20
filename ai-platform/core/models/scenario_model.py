from dataclasses import dataclass, field


@dataclass(slots=True)
class ScenarioModel:
    id: str
    feature_id: str
    name: str
    steps: list[str] = field(default_factory=list)
