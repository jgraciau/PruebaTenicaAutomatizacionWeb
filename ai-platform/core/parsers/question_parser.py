from core.common.models import SourceFile
from core.parsers.java_parser import parse_java


def parse(source: SourceFile) -> dict:
    return parse_java(source, "question")
