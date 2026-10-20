from dataclasses import dataclass, field


@dataclass(slots=True)
class StepDefinitionModel:
    id: str
    name: str
    source_path: str
    expressions: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
