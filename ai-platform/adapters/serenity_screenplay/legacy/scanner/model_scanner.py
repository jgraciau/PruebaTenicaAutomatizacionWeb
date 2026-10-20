from pathlib import Path

from adapters.serenity_screenplay.legacy.common.constants import JAVA_SUFFIX
from adapters.serenity_screenplay.legacy.common.file_utils import iter_source_files
from adapters.serenity_screenplay.legacy.common.models import SourceFile


class ModelScanner:
    """Find Java model classes using package path or common data-model conventions."""

    MODEL_MARKERS = ("@Data", "@Value", "@Entity", "@Embeddable", "@JsonProperty")

    @classmethod
    def is_model(cls, source: SourceFile) -> bool:
        relative_parts = source.relative_path.split("/")
        parts = {part.lower() for part in relative_parts[:-1]}
        is_test_source = any(part in {"test", "tests"} for part in parts)
        is_test_class = source.path.stem.endswith(("Test", "Tests"))
        if is_test_source and is_test_class:
            return False
        in_models_package = "models" in parts or "model" in parts
        has_model_marker = any(marker in source.content for marker in cls.MODEL_MARKERS)
        return in_models_package or has_model_marker

    def scan(self, root: Path) -> list[SourceFile]:
        files, _ = iter_source_files(root, (JAVA_SUFFIX,))
        return [source for source in files if self.is_model(source)]
