from dataclasses import dataclass


@dataclass(slots=True)
class TargetModel:
    id: str
    name: str
    source_path: str
    selector: str = ""
    symbol: str = ""
