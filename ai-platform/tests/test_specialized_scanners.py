from pathlib import Path

from core.scanner.feature_scanner import FeatureScanner
from core.scanner.interaction_scanner import InteractionScanner
from core.scanner.question_scanner import QuestionScanner
from core.scanner.step_scanner import StepScanner
from core.scanner.task_scanner import TaskScanner
from core.scanner.ui_scanner import UiScanner


def test_specialized_scanners_find_components_in_nested_packages(tmp_path: Path) -> None:
    paths = {
        "src/test/resources/features/a.feature": "Feature: A",
        "src/test/java/step_definitions/Steps.java": '@Given("works") void works() {}',
        "src/main/java/tasks/nested/TaskA.java": "class TaskA implements Task {}",
        "src/main/java/questions/nested/QuestionA.java": "class QuestionA implements Question<String> {}",
        "src/main/java/interactions/nested/InteractionA.java": "class InteractionA implements Interaction {}",
        "src/main/java/userInterfaces/Home.java": 'class Home { Target button = Target.the("button"); }',
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
