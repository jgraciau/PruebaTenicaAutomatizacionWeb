from core.common.models import SourceFile
from core.parsers.java_parser import parse_steps


def parse(source: SourceFile) -> dict:
    return parse_steps(source)
