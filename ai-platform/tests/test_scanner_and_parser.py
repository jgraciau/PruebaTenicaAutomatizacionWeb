from pathlib import Path

from core.common.models import SourceFile
from core.scanner.project_scanner import ProjectScanner
from core.parsers.feature_parser import FeatureParser
from core.parsers.step_parser import parse as parse_step


def test_scanner_classifies_artifacts_and_skips_generated(tmp_path: Path) -> None:
    (tmp_path / "src/test/resources/features").mkdir(parents=True)
    (tmp_path / "src/test/java/stepDefinitions").mkdir(parents=True)
    (tmp_path / "src/main/java/tasks").mkdir(parents=True)
    (tmp_path / "build/tasks").mkdir(parents=True)
    (tmp_path / "src/test/resources/features/sample.feature").write_text("Feature: Sample\n Scenario: works\n  Given a user", encoding="utf-8")
    (tmp_path / "src/test/java/stepDefinitions/Steps.java").write_text('package steps; @Given("a user") public void user() {}', encoding="utf-8")
    (tmp_path / "src/main/java/tasks/SignIn.java").write_text("package tasks; class SignIn implements Task {}", encoding="utf-8")
    (tmp_path / "build/tasks/Generated.java").write_text("class Generated implements Task {}", encoding="utf-8")
    result = ProjectScanner().scan(tmp_path)
    assert len(result.features) == 1
    assert len(result.step_definitions) == 1
    assert len(result.tasks) == 1
    assert all("build/" not in item.relative_path for item in result.project_files)


def test_feature_parser_reads_scenario_steps_and_background(tmp_path: Path) -> None:
    path = tmp_path / "sample.feature"
    text = "Feature: Sample\n Background:\n  Given shared context\n Scenario: works\n  When submit\n  Then success"
    path.write_text(text, encoding="utf-8")
    parsed = FeatureParser().parse(SourceFile(path, "sample.feature", text))
    assert parsed["name"] == "Sample"
    assert parsed["background"] == ["shared context"]
    assert [step["text"] for step in parsed["scenarios"][0]["steps"]] == ["submit", "success"]


def test_step_parser_extracts_cucumber_annotation(tmp_path: Path) -> None:
    path = tmp_path / "Steps.java"
    source = SourceFile(path, "Steps.java", 'class Steps { @When("I submit {string}") void submit() {} }')
    parsed = parse_step(source)
    assert parsed["definitions"] == [{"keyword": "When", "expression": "I submit {string}"}]
    assert parsed["name"] == "Steps"
