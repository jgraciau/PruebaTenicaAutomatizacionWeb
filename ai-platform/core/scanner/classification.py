import re

from core.common.models import SourceFile

_STEP_ANNOTATION_RE = re.compile(r"@(Given|When|Then|And|But)\s*\(")
_TASK_RE = re.compile(r"\b(?:implements|extends)\s+Task\b")
_QUESTION_RE = re.compile(
    r"\b(?:implements|extends)\s+Question\s*(?:<|\b)"
)
_INTERACTION_RE = re.compile(
    r"\b(?:implements|extends)\s+Interaction\b|Interaction\s*\.\s*(?:call|where)\s*\("
)


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
        and not _in_package(source, "interactions")
        and bool(_TASK_RE.search(source.content))
    )


def is_question(source: SourceFile) -> bool:
    return bool(_QUESTION_RE.search(source.content)) or (
        _in_package(source, "questions")
        and "Question" in source.content
    )


def is_interaction(source: SourceFile) -> bool:
    return bool(_INTERACTION_RE.search(source.content)) or (
        _in_package(source, "interactions")
        and "implements Task" in source.content
    )


def is_user_interface(source: SourceFile) -> bool:
    has_target = bool(
        re.search(
            r"\bTarget\s*\.\s*(?:the|empty|named)\s*\(",
            source.content,
        )
    )
    return has_target
