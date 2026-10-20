import json
from pathlib import Path

from core.builders.architecture_builder import ArchitectureBuilder
from core.builders.dependency_builder import DependencyBuilder, _matches_expression
from core.builders.html_report_builder import render_html_report
from core.builders.screenplay_builder import ScreenplayBuilder
from core.common.models import ScanResult, SourceFile
from main import run


def _source(root: Path, relative: str, content: str) -> SourceFile:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return SourceFile(path, relative, content)


def test_builders_create_stable_maps_and_relationships(tmp_path: Path) -> None:
    feature = _source(tmp_path, "features/login.feature", "Feature: Login\nScenario: valid\n Given the user logs in")
    step = _source(tmp_path, "stepDefinitions/LoginSteps.java", 'class LoginSteps { @Given("the user logs in") void login() { actor.attemptsTo(SignIn.now()); LoginCredentials.load(); } }')
    task = _source(tmp_path, "tasks/SignIn.java", "package tasks; class SignIn implements Task { void run() { actor.attemptsTo(ClickButton.now(), ScrollToCenter.now()); } }")
    interaction = _source(tmp_path, "interactions/ClickButton.java", "package interactions; class ClickButton implements Task {}")
    second_interaction = _source(tmp_path, "interactions/ScrollToCenter.java", "package interactions; class ScrollToCenter implements Task {}")
    model = _source(tmp_path, "models/LoginCredentials.java", "package models; class LoginCredentials {}")
    scan = ScanResult(
        tmp_path,
        (feature, step, task, interaction, second_interaction, model),
        (feature,),
        (step,),
        (task,),
        (),
        (interaction, second_interaction),
        (),
        (model,),
        (),
    )
    architecture = ArchitectureBuilder().build(scan)
    dependency = DependencyBuilder().build(architecture)
    screenplay = ScreenplayBuilder().build(architecture, dependency)
    assert architecture["project"]["name"] == tmp_path.name
    assert len(dependency["feature_to_step_definition"]) == 1
    assert dependency["feature_to_step_definition"][0]["relation"] == "heuristic"
    assert not _matches_expression("el usuario inicia sesión", "inicia sesión")
    assert _matches_expression('el usuario carga el Excel "1"', 'el usuario carga el Excel {string}')
    assert not _matches_expression("usuario actualiza dirección en ciudad", "actualiza dirección en (.*)")
    assert _matches_expression("el usuario carga archivo.csv", r"el usuario carga (.*)")
    assert len(dependency["step_definition_to_task"]) == 1
    assert len(dependency["task_to_interaction"]) == 2
    assert len(dependency["step_definition_to_model"]) == 1
    assert {
        chain["interaction"] for chain in dependency["dependency_chain"]
    } == {interaction.relative_path for interaction in (interaction, second_interaction)}
    assert screenplay["metrics"]["scenarios"] == 1


def test_background_steps_are_counted_and_linked(tmp_path: Path) -> None:
    feature = _source(
        tmp_path,
        "features/background.feature",
        "Feature: Background\nBackground:\n Given a signed-in user\nScenario: opens page\n When the page opens",
    )
    step = _source(
        tmp_path,
        "stepDefinitions/BackgroundSteps.java",
        'class BackgroundSteps { @Given("a signed-in user") void signedIn() {} @When("the page opens") void opens() {} }',
    )
    scan = ScanResult(
        tmp_path,
        (feature, step),
        (feature,),
        (step,),
        (),
        (),
        (),
        (),
        (),
        (),
    )
    architecture = ArchitectureBuilder().build(scan)
    dependencies = DependencyBuilder().build(architecture)
    screenplay = ScreenplayBuilder().build(architecture, dependencies)

    assert screenplay["metrics"]["gherkin_steps"] == 2
    assert {link["scenario"] for link in dependencies["feature_to_step_definition"]} == {
        "Background",
        "opens page",
    }


def test_quality_audit_reports_orphans_duplicates_and_risks() -> None:
    architecture = {
        "project": {"scan_errors": []},
        "features": [],
        "step_definitions": [],
        "tasks": [{"path": "tasks/OrphanTask.java", "name": "OrphanTask"}],
        "questions": [],
        "interactions": [],
        "user_interfaces": [{"path": "ui/Home.java", "name": "Home"}],
        "models": [
            {"path": "models/FirstProfile.java", "name": "Profile"},
            {"path": "models/SecondProfile.java", "name": "Profile"},
        ],
    }
    dependencies = {
        "feature_to_step_definition": [],
        "step_definition_to_task": [],
        "task_to_interaction": [],
        "task_to_question": [],
    }

    audited = ArchitectureBuilder.add_quality_audit(architecture, dependencies)
    quality = audited["quality"]

    assert {item["component_type"] for item in quality["orphaned_components"]} == {
        "task",
        "user_interface",
        "model",
    }
    assert quality["duplicate_components"] == [
        {
            "component_type": "models",
            "name": "Profile",
            "paths": ["models/FirstProfile.java", "models/SecondProfile.java"],
        }
    ]
    assert {risk["code"] for risk in quality["risks"]} == {
        "NO_FEATURES",
        "NO_STEP_DEFINITIONS",
        "ORPHAN_COMPONENTS",
        "DUPLICATE_COMPONENTS",
    }


def test_cli_generates_json_and_report(tmp_path: Path) -> None:
    source_root = tmp_path / "repo"
    _source(source_root, "src/test/resources/features/a.feature", "Feature: A\nScenario: B\n Given a thing")
    output = tmp_path / "out"
    assert run(source_root, output) == 0
    architecture = json.loads((output / "knowledge/architecture-map.json").read_text(encoding="utf-8"))
    assert set(architecture) == {
        "project",
        "features",
        "step_definitions",
        "tasks",
        "questions",
        "interactions",
        "user_interfaces",
        "models",
        "quality",
    }
    assert len(architecture["features"]) == 1
    assert architecture["project"]["language"] == "Gherkin"
    assert architecture["project"]["frameworks"] == ["Cucumber"]
    assert (output / "knowledge/screenplay-map.json").exists()
    assert (output / "knowledge/dependency-map.json").exists()
    markdown_report = (output / "outputs/architecture-report.md").read_text(encoding="utf-8")
    assert "# Reporte de arquitectura" in markdown_report
    assert "## Inventario de componentes" in markdown_report
    assert "## Hallazgos de calidad" in markdown_report
    assert "Definición de paso → Modelo" in markdown_report
    html_report = (output / "outputs/architecture-report.html").read_text(encoding="utf-8")
    assert "<!doctype html>" in html_report.lower()
    assert "<svg" in html_report
    assert '<html lang="es">' in html_report
    assert "Inventario de componentes" in html_report
    assert "Distribución de relaciones" in html_report


def test_html_report_escapes_project_content_and_handles_zero_links() -> None:
    architecture = {
        "project": {
            "name": "<unsafe & project>",
            "root": ".",
            "source_files_scanned": 0,
            "frameworks": [],
            "scan_errors": [],
        }
    }
    screenplay = {
        "metrics": {"features": 0, "scenarios": 0, "gherkin_steps": 0, "tasks": 0,
                    "questions": 0, "interactions": 0, "user_interfaces": 0, "models": 0},
        "patterns_detected": [],
    }
    dependencies = {
        "feature_to_step_definition": [], "step_definition_to_task": [],
        "task_to_interaction": [], "task_to_question": [],
    }
    report = render_html_report(architecture, screenplay, dependencies)
    assert "&lt;unsafe &amp; project&gt;" in report
    assert "<unsafe & project>" not in report
    assert "Sin vínculos" in report
    assert '<html lang="es">' in report
    assert 'stroke-dasharray="nan' not in report


def test_missing_root_returns_error_without_crashing(tmp_path: Path) -> None:
    assert run(tmp_path / "absent", tmp_path / "output") == 1


def test_invalid_utf8_is_reported(tmp_path: Path) -> None:
    (tmp_path / "Bad.java").write_bytes(b"class Bad { \xff }")
    result = __import__("core.scanner.project_scanner", fromlist=["ProjectScanner"]).ProjectScanner().scan(tmp_path)
    assert result.project_files == ()
    assert "Unable to read Bad.java" in result.errors[0]
