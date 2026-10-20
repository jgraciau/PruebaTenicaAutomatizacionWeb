import json
from pathlib import Path

import pytest

from adapters.generic_screenplay import GenericScreenplayAdapter
from adapters.playwright_screenplay import PlaywrightScreenplayAdapter
from adapters.registry import create_adapter
from adapters.serenity_screenplay import SerenityScreenplayAdapter
from core.project_config import ConfigurationError, load_project_config
from main import run_configured


def _write_config(
    config_directory: Path,
    project_root: Path,
    *,
    name: str,
    framework: str,
    language: str,
    extension: str,
    path_entries: dict[str, str],
) -> Path:
    config_directory.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    config = config_directory / "project.yaml"
    paths = "\n".join(f"  {key}: {value}" for key, value in path_entries.items())
    config.write_text(
        f"""project:
  name: {name}
  root: {project_root.as_posix()}
framework:
  type: {framework}
language:
  type: {language}
  extensions: [{extension}]
pattern:
  type: screenplay
paths:
{paths}
outputs:
  knowledge: { (config_directory / 'knowledge').as_posix() }
  reports: { (config_directory / 'reports').as_posix() }
""",
        encoding="utf-8",
    )
    return config


def _project_files(root: Path, extension: str) -> None:
    if extension == ".java":
        files = {
            "features/login.feature": (
                "Feature: Login\n"
                "  Scenario: user signs in\n"
                "    When user signs in\n"
            ),
            "glue/LoginSteps.java": (
                'class LoginSteps { @When("user signs in") '
                "void signIn() { actor.attemptsTo(SignIn.now()); } }"
            ),
            "actions/SignIn.java": (
                "class SignIn { void performAs() { "
                "actor.attemptsTo(ClickSignIn.now(), LoginQuestion.ask(), "
                "LoginData.load()); } }"
            ),
            "flow/ClickSignIn.java": (
                "class ClickSignIn { void performAs() { LoginPage.button.click(); } }"
            ),
            "answers/LoginQuestion.java": (
                "class LoginQuestion { String target = LoginPage.button; }"
            ),
            "pages/LoginPage.java": (
                'class LoginPage { Target button = Target.the("Sign in"); }'
            ),
            "data/LoginData.java": "class LoginData {}",
        }
    else:
        files = {
            "features/login.feature": (
                "Feature: Login\n"
                "  Scenario: user signs in\n"
                "    When user signs in\n"
            ),
            "glue/login_steps" + extension: (
                "class LoginSteps:\n"
                "    @when('user signs in')\n"
                "    def sign_in(self, actor):\n"
                "        actor.attempts_to(SignIn())\n"
            ),
            "actions/sign_in" + extension: (
                "class SignIn:\n"
                "    def perform_as(self, actor):\n"
                "        actor.attempts_to(ClickSignIn(), LoginQuestion(), LoginData())\n"
            ),
            "flow/click_sign_in" + extension: (
                "class ClickSignIn:\n"
                "    def perform_as(self, actor):\n"
                "        LoginPage.submit.click()\n"
            ),
            "answers/login_question" + extension: (
                "class LoginQuestion:\n"
                "    target = LoginPage.submit\n"
            ),
            "pages/login_page" + extension: (
                "class LoginPage:\n"
                "    submit = page.get_by_role('button', name='Sign in')\n"
            ),
            "data/login_data" + extension: "class LoginData:\n    pass\n",
        }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_configuration_resolves_project_and_configured_paths(tmp_path: Path) -> None:
    root = tmp_path / "project"
    config_path = _write_config(
        tmp_path / "platform" / "config",
        root,
        name="Configured",
        framework="playwright",
        language="python",
        extension=".py",
        path_entries={"features": "features", "tasks": "actions"},
    )

    config = load_project_config(config_path)

    assert config.project_root == root.resolve()
    assert config.paths["features"] == ((root / "features").resolve(),)
    assert config.paths["tasks"] == ((root / "actions").resolve(),)


def test_configuration_reports_invalid_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "project.yaml"
    config_path.write_text("project: [", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Invalid YAML"):
        load_project_config(config_path)


def test_adapter_registry_selects_specialized_and_generic_adapters(
    tmp_path: Path,
) -> None:
    root = tmp_path / "project"
    config_path = _write_config(
        tmp_path / "config",
        root,
        name="Adapters",
        framework="serenity",
        language="java",
        extension=".java",
        path_entries={},
    )
    config = load_project_config(config_path)
    assert isinstance(create_adapter(config), SerenityScreenplayAdapter)

    playwright_path = _write_config(
        tmp_path / "playwright-config",
        root,
        name="Playwright",
        framework="playwright",
        language="python",
        extension=".py",
        path_entries={},
    )
    assert isinstance(
        create_adapter(load_project_config(playwright_path)),
        PlaywrightScreenplayAdapter,
    )

    generic_path = _write_config(
        tmp_path / "generic-config",
        root,
        name="Proprietary",
        framework="proprietary",
        language="custom",
        extension=".src",
        path_entries={},
    )
    assert isinstance(
        create_adapter(load_project_config(generic_path)),
        GenericScreenplayAdapter,
    )


@pytest.mark.parametrize(
    ("framework", "language", "extension", "expected_adapter"),
    [
        ("serenity", "java", ".java", "SerenityScreenplayAdapter"),
        ("selenium", "java", ".java", "SeleniumScreenplayAdapter"),
        ("playwright", "python", ".py", "PlaywrightScreenplayAdapter"),
    ],
)
def test_same_engine_builds_universal_maps_for_multiple_projects(
    tmp_path: Path,
    framework: str,
    language: str,
    extension: str,
    expected_adapter: str,
) -> None:
    project_root = tmp_path / f"{framework}-project"
    _project_files(project_root, extension)
    path_entries = {
        "features": "features",
        "step_definitions": "glue",
        "tasks": "actions",
        "questions": "answers",
        "interactions": "flow",
        "user_interfaces": "pages",
        "models": "data",
    }
    config_path = _write_config(
        tmp_path / f"{framework}-config",
        project_root,
        name=f"{framework.title()} Project",
        framework=framework,
        language=language,
        extension=extension,
        path_entries=path_entries,
    )

    assert run_configured(config_path) == 0

    knowledge = config_path.parent / "knowledge"
    architecture = json.loads(
        (knowledge / "architecture-map.json").read_text(encoding="utf-8")
    )
    dependency_map = json.loads(
        (knowledge / "dependency-map.json").read_text(encoding="utf-8")
    )
    graph = json.loads(
        (knowledge / "dependency-graph.json").read_text(encoding="utf-8")
    )
    relationships = {
        edge["relation"] for edge in dependency_map["relationships"]
    }

    assert architecture["project"]["adapter"] == expected_adapter
    assert architecture["project"]["root"] == "."
    assert len(architecture["features"]) == 1
    assert len(architecture["scenarios"]) == 1
    assert len(architecture["tasks"]) == 1
    assert len(architecture["questions"]) == 1
    assert len(architecture["interactions"]) == 1
    assert len(architecture["targets"]) == 1
    assert len(architecture["models"]) == 1
    assert {
        "contains",
        "step_definition",
        "invokes_task",
        "uses_interaction",
        "uses_target",
        "asks_question",
        "uses_model",
        "queries_target",
    } <= relationships
    assert graph["nodes"]
    assert graph["edges"]
    architecture_html = (
        config_path.parent / "reports" / "architecture-report.html"
    ).read_text(encoding="utf-8")
    architecture_markdown = (
        config_path.parent / "reports" / "architecture-report.md"
    ).read_text(encoding="utf-8")
    assert "Reporte para producto" in architecture_html
    assert "Resumen ejecutivo" in architecture_html
    assert "Detalle por escenario" in architecture_html
    assert "próximas acciones" in architecture_html.lower()
    assert "no ejecuta pruebas" in architecture_html.lower()
    assert "Resumen para producto" in architecture_markdown
    assert "Trazabilidad estimada" in architecture_markdown
    assert "no ejecuta pruebas" in architecture_markdown.lower()
    assert project_root.as_posix() not in architecture_html
    for name in (
        "architecture-report.md",
        "architecture-report.html",
    ):
        assert (config_path.parent / "reports" / name).is_file()
    assert not (
        config_path.parent / "reports" / "dependency-report.md"
    ).exists()
    assert not (
        config_path.parent / "reports" / "dependency-report.html"
    ).exists()


def test_scanner_only_reads_configured_locations(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    configured = project_root / "configured" / "Task.py"
    unconfigured = project_root / "elsewhere" / "NotATask.py"
    configured.parent.mkdir(parents=True)
    unconfigured.parent.mkdir(parents=True)
    configured.write_text("class Task: pass", encoding="utf-8")
    unconfigured.write_text("class NotATask: pass", encoding="utf-8")
    config_path = _write_config(
        tmp_path / "config",
        project_root,
        name="Configured Paths",
        framework="generic",
        language="python",
        extension=".py",
        path_entries={"tasks": "configured"},
    )

    result = create_adapter(load_project_config(config_path)).analyze()

    assert [task["name"] for task in result.tasks] == ["Task"]


def test_generic_adapter_accepts_project_specific_parser_patterns(
    tmp_path: Path,
) -> None:
    root = tmp_path / "project"
    config_path = _write_config(
        tmp_path / "config",
        root,
        name="Proprietary Project",
        framework="proprietary",
        language="custom",
        extension=".src",
        path_entries={
            "features": "specs",
            "step_definitions": "glue",
            "tasks": "behaviors",
            "user_interfaces": "controls",
        },
    )
    config_text = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        config_text
        + """features:
  extensions: [.story]
parser_patterns:
  declarations: '^component\\s+(\\w+)'
  feature: '^Capability:\\s*(.+)$'
  scenarios: '^Case:\\s*(.+)$'
  steps: '^\\s*When\\s+(.+)$'
  step_definitions: 'ACTION\\("([^"]+)"\\)'
  targets: 'CONTROL\\("([^"]+)"\\)'
""",
        encoding="utf-8",
    )
    custom_files = {
        "specs/login.story": (
            "Capability: Login\nCase: sign in\nWhen user signs in\n"
        ),
        "glue/login.src": 'component LoginSteps\nACTION("user signs in")',
        "behaviors/sign_in.src": "component SignIn\nLoginButton",
        "controls/login.src": 'component LoginControls\nCONTROL("LoginButton")',
    }
    for relative, content in custom_files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    assert run_configured(config_path) == 0
    architecture = json.loads(
        (config_path.parent / "knowledge" / "architecture-map.json").read_text(
            encoding="utf-8"
        )
    )

    assert architecture["features"][0]["name"] == "Login"
    assert architecture["scenarios"][0]["name"] == "sign in"
    assert architecture["features"][0]["scenarios"][0]["steps"] == [
        "user signs in"
    ]
    assert architecture["tasks"][0]["name"] == "SignIn"
    assert architecture["targets"][0]["name"] == "LoginButton"


def test_generic_feature_parser_propagates_background_steps(tmp_path: Path) -> None:
    root = tmp_path / "project"
    config_path = _write_config(
        tmp_path / "config",
        root,
        name="Background Feature",
        framework="generic",
        language="python",
        extension=".py",
        path_entries={"features": "features"},
    )
    feature = root / "features" / "account.feature"
    feature.parent.mkdir(parents=True)
    feature.write_text(
        "Feature: Account\n"
        "  Background:\n"
        "    Given a signed-in user\n"
        "  Scenario: opens profile\n"
        "    When the profile opens\n"
        "  Scenario: sees account\n"
        "    Then account details are visible\n",
        encoding="utf-8",
    )

    result = create_adapter(load_project_config(config_path)).analyze()

    assert [scenario["steps"] for scenario in result.features[0]["scenarios"]] == [
        ["a signed-in user", "the profile opens"],
        ["a signed-in user", "account details are visible"],
    ]
