import re
from typing import Any

from core.common.models import SourceFile

PACKAGE_RE = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.MULTILINE)
CLASS_RE = re.compile(r"\b(?:class|interface|record|enum)\s+(\w+)")
ANNOTATION_RE = re.compile(r"@(Given|When|Then|And|But)\s*\(\s*(\"(?:\\.|[^\"])*\")", re.MULTILINE)


def parse_java(source: SourceFile, root_relative: str) -> dict[str, Any]:
    package = PACKAGE_RE.search(source.content)
    classes = CLASS_RE.findall(source.content)
    return {
        "path": source.relative_path,
        "package": package.group(1) if package else "",
        "name": classes[0] if classes else source.path.stem,
        "classes": classes,
        "references": sorted(set(re.findall(r"\b(?:new\s+)?([A-Z][A-Za-z0-9_]*)\s*(?:\(|\.)", source.content))),
        "root": root_relative,
    }


def parse_steps(source: SourceFile) -> dict[str, Any]:
    base = parse_java(source, "")
    matches = [
        {"keyword": match.group(1), "expression": match.group(2)[1:-1]}
        for match in ANNOTATION_RE.finditer(source.content)
    ]
    base["definitions"] = matches
    base["line_count"] = len(source.content.splitlines())
    return base
