from dataclasses import dataclass


@dataclass(slots=True)
class ProjectModel:
    name: str
    root: str
    framework: str
    language: str
    pattern: str
    adapter: str = ""
