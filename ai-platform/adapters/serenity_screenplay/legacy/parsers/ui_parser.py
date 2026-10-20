from typing import Any

from adapters.serenity_screenplay.legacy.common.models import SourceFile
from adapters.serenity_screenplay.legacy.parsers.java_parser import parse_java


def parse(source: SourceFile) -> dict[str, Any]:
    return parse_java(source)
