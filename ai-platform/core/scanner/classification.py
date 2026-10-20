import re

from core.common.models import SourceFile

_STEP_ANNOTATION_RE = re.compile(r"@(Given|When|Then|And|But)\s*\(")
_TASK_RE = re.compile(r"\b(?:implements|extends)\s+Task\b")
_QUESTION_RE = re.compile(r"\bQuestion\s*(?:<|\b)")


def _package_parts(source: SourceFile) -> set[str]:
    return {
        part.lower().replace("_", "")
        for part in source.relative_path.split("/")[:-1]
    }


def _in_package(source: SourceFile, component: str) -> bool:
    parts = _package_parts(source)
    package = component.lower().replace("_", "")
    return package in parts or package.rstrip("s") in parts


def is_step_definition(source: SourceFile) -> bool:
    return (
        "stepdefinitions" in _package_parts(source)
        or bool(_STEP_ANNOTATION_RE.search(source.content))
    )


def is_task(source: SourceFile) -> bool:
    return (
        not is_step_definition(source)
        and _in_package(source, "tasks")
        and bool(_TASK_RE.search(source.content))
    )


def is_question(source: SourceFile) -> bool:
    return (
        _in_package(source, "questions")
        and bool(_QUESTION_RE.search(source.content))
    )


def is_interaction(source: SourceFile) -> bool:
    markers = (
        "implements Interaction",
        "implements Task",
        "Interaction.call",
        "Interaction.where",
    )
    return _in_package(source, "interactions") and any(
        marker in source.content for marker in markers
    )


def is_user_interface(source: SourceFile) -> bool:
    return (
        _in_package(source, "userInterfaces")
        and bool(
            re.search(
                r"\bTarget\s*\.\s*(?:the|empty|named)\s*\(",
                source.content,
            )
        )
    )
