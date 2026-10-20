from pathlib import Path

from adapters.serenity_screenplay.legacy.common.models import SourceFile
from adapters.serenity_screenplay.legacy.parsers.model_parser import parse as parse_model
from adapters.serenity_screenplay.legacy.scanner.feature_scanner import FeatureScanner
from adapters.serenity_screenplay.legacy.scanner.interaction_scanner import InteractionScanner
from adapters.serenity_screenplay.legacy.scanner.model_scanner import ModelScanner
from adapters.serenity_screenplay.legacy.scanner.project_scanner import ProjectScanner
from adapters.serenity_screenplay.legacy.scanner.question_scanner import QuestionScanner
from adapters.serenity_screenplay.legacy.scanner.step_scanner import StepScanner
from adapters.serenity_screenplay.legacy.scanner.task_scanner import TaskScanner
from adapters.serenity_screenplay.legacy.scanner.ui_scanner import UiScanner


def test_specialized_scanners_find_components_in_nested_packages(tmp_path: Path) -> None:
    paths = {
        "src/test/resources/features/a.feature": "Feature: A",
        "src/test/java/step_definitions/Steps.java": '@Given("works") void works() {}',
        "src/main/java/tasks/nested/TaskA.java": "class TaskA implements Task {}",
        "src/main/java/questions/nested/QuestionA.java": "class QuestionA implements Question<String> {}",
        "src/main/java/interactions/nested/InteractionA.java": "class InteractionA implements Interaction {}",
        "src/main/java/userInterfaces/Home.java": 'class Home { Target button = Target.the("button"); Target empty = Target.empty(); Target named = Target.named("named"); }',
        "src/main/java/models/Invoice.java": "class Invoice {}",
        "src/test/java/models/InvoiceTest.java": "class InvoiceTest {}",
    }
    for relative, content in paths.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    assert [source.relative_path for source in FeatureScanner().scan(tmp_path)] == [
        "src/test/resources/features/a.feature"
    ]
    assert [source.path.stem for source in StepScanner().scan(tmp_path)] == ["Steps"]
    assert [source.path.stem for source in TaskScanner().scan(tmp_path)] == ["TaskA"]
    assert [source.path.stem for source in QuestionScanner().scan(tmp_path)] == ["QuestionA"]
    assert [source.path.stem for source in InteractionScanner().scan(tmp_path)] == ["InteractionA"]
    assert [source.path.stem for source in UiScanner().scan(tmp_path)] == ["Home"]
    assert [source.path.stem for source in ModelScanner().scan(tmp_path)] == ["Invoice"]

    scan = ProjectScanner().scan(tmp_path)
    assert [source.path.stem for source in scan.models] == ["Invoice"]
    assert [source.path.stem for source in scan.user_interfaces] == ["Home"]


def test_model_parser_extracts_java_identity_and_markers(tmp_path: Path) -> None:
    path = tmp_path / "src/main/java/models/Invoice.java"
    source = SourceFile(
        path,
        "src/main/java/models/Invoice.java",
        "package models;\n@Entity\nclass Invoice {}",
    )

    parsed = parse_model(source)

    assert parsed["package"] == "models"
    assert parsed["name"] == "Invoice"
    assert parsed["model_markers"] == ["@Entity"]
