from dataclasses import dataclass


@dataclass(slots=True)
class ActorModel:
    id: str
    name: str
    source_path: str = ""
