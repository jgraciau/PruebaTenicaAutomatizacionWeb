import json
import logging
from pathlib import Path
from typing import Any

from agents.architect.architect_agent import ArchitectAgent


def _write_knowledge(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    maps: dict[str, dict[str, Any]] = {
        "architecture-map": {
            "project": {"name": "Test Project"},
            "features": [{"id": "feature:one"}],
            "scenarios": [
                {"id": "scenario:one", "steps": ["Given a user"]},
            ],
            "step_definitions": [{"id": "step:one"}],
            "tasks": [{"id": "task:one"}],
            "questions": [{"id": "question:one"}],
            "interactions": [{"id": "interaction:one"}],
            "targets": [{"id": "target:one"}],
            "models": [{"id": "model:one"}],
            "scan_errors": [],
        },
        "dependency-map": {
            "relationships": [
                {
                    "source_id": "step:one",
                    "target_id": "task:one",
                    "relation": "invokes_task",
                    "evidence": "Direct reference",
                },
                {
                    "source_id": "scenario:one",
                    "target_id": "step:one",
                    "relation": "step_definition",
                    "evidence": "Direct reference",
                },
                {
                    "source_id": "task:one",
                    "target_id": "question:one",
                    "relation": "asks_question",
                    "evidence": "Direct reference",
                },
                {
                    "source_id": "task:one",
                    "target_id": "interaction:one",
                    "relation": "uses_interaction",
                    "evidence": "Direct reference",
                },
                {
                    "source_id": "question:one",
                    "target_id": "target:one",
                    "relation": "queries_target",
                    "evidence": "Direct reference",
                },
                {
                    "source_id": "task:one",
                    "target_id": "model:one",
                    "relation": "uses_model",
                    "evidence": "Direct reference",
                },
            ]
        },
        "relationship-map": {
            "relationships": [
                {
                    "source_id": "scenario:one",
                    "target_id": "step:one",
                    "relation": "step_definition",
                    "evidence": "Direct reference",
                }
            ]
        },
        "dependency-graph": {
            "nodes": [{"id": "feature:one"}],
            "edges": [],
            "cycles": [],
        },
        "screenplay-map": {"metrics": {"scenarios": 1}},
    }
    for name, value in maps.items():
        (directory / f"{name}.json").write_text(
            json.dumps(value),
            encoding="utf-8",
        )


def test_architect_agent_runs_full_pipeline_and_generates_reports(
    tmp_path: Path,
) -> None:
    knowledge = tmp_path / "knowledge"
    output = tmp_path / "outputs"
    _write_knowledge(knowledge)
    logger = logging.getLogger(f"test.architect.{tmp_path}")

    result = ArchitectAgent(knowledge, output, logger).execute()

    assert list(result["analyses"]) == [
        "architecture",
        "risk",
        "debt",
        "compliance",
        "reuse",
    ]
    assert len(result["recommendations"]) > 0
    assert (output / "architecture-review.md").is_file()
    assert (output / "technical-debt-report.md").is_file()
    assert (output / "risk-report.md").is_file()
    assert (output / "screenplay-compliance-report.md").is_file()
    assert (output / "reuse-report.md").is_file()
    assert (output / "improvement-plan.md").is_file()
    score_file = json.loads(
        (output / "quality-score.json").read_text(encoding="utf-8")
    )
    assert score_file["project"] == "Test Project"
    assert score_file["score_values"]["overall_score"] == result["scores"]["overall_score"]
    assert score_file["score_values"]["reuse_score"] == result["scores"]["reuse_score"]


def test_missing_knowledge_map_is_logged_and_pipeline_continues(
    tmp_path: Path,
    caplog: Any,
) -> None:
    knowledge = tmp_path / "incomplete"
    _write_knowledge(knowledge)
    (knowledge / "dependency-graph.json").unlink()
    caplog.set_level(logging.ERROR)

    result = ArchitectAgent(
        knowledge,
        tmp_path / "reports",
        logging.getLogger("test.architect.missing"),
    ).execute()

    assert "KnowledgeArtifactMissingException" in result["errors"][0]
    assert "KnowledgeArtifactMissingException" in caplog.text
    assert (tmp_path / "reports" / "quality-score.json").exists()
