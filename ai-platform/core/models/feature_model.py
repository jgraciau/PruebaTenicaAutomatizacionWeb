from dataclasses import dataclass, field

from core.models.scenario_model import ScenarioModel


@dataclass(slots=True)
class FeatureModel:
    id: str
    name: str
    source_path: str
    scenarios: list[ScenarioModel] = field(default_factory=list)
