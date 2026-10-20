from typing import Any

from core.common.models import SourceFile
from core.parsers.java_parser import parse_java


def parse(source: SourceFile) -> dict[str, Any]:
    parsed = parse_java(source)
    parsed["model_markers"] = [
        marker
        for marker in ("@Data", "@Value", "@Entity", "@Embeddable", "@JsonProperty")
        if marker in source.content
    ]
    return parsed
