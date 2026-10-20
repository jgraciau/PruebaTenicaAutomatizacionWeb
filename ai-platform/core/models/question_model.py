from dataclasses import dataclass, field


@dataclass(slots=True)
class QuestionModel:
    id: str
    name: str
    source_path: str
    references: list[str] = field(default_factory=list)
