from abc import ABC, abstractmethod
from core.models import ProjectKnowledge
from core.project_config import ProjectConfig


AdapterResult = ProjectKnowledge


class ScreenplayAdapter(ABC):
    """Port implemented by adapters that translate project sources to SKP data."""

    def __init__(self, config: ProjectConfig) -> None:
        self.config = config

    @abstractmethod
    def analyze(self) -> AdapterResult:
        """Discover and translate configured project artifacts."""
