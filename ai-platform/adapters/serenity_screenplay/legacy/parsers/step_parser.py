from adapters.serenity_screenplay.legacy.common.models import SourceFile
from adapters.serenity_screenplay.legacy.parsers.java_parser import parse_steps


def parse(source: SourceFile) -> dict:
    return parse_steps(source)
