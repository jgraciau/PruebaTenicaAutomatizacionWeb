from dataclasses import dataclass, field


@dataclass(slots=True)
class TaskModel:
    id: str
    name: str
    source_path: str
    references: list[str] = field(default_factory=list)
