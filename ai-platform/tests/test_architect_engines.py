from agents.architect.engines.recommendation_engine import RecommendationEngine
from agents.architect.engines.scoring_engine import ScoringEngine


def test_scoring_engine_returns_bounded_scores_and_quality_dimensions() -> None:
    result = ScoringEngine().calculate(
        {
            "architecture-map": {
                "features": [{"id": "feature:1"}],
                "step_definitions": [{"id": "step:1"}],
                "tasks": [{"id": "task:1"}],
                "questions": [{"id": "question:1"}],
                "interactions": [{"id": "interaction:1"}],
                "targets": [{"id": "target:1"}],
                "models": [{"id": "model:1"}],
                "scan_errors": [],
            },
            "dependency-graph": {
                "nodes": [{"id": "task:1"}],
                "edges": [],
                "cycles": [],
            },
            "dependency-map": {
                "relationships": [
                    {"relation": "step_definition"},
                    {"relation": "invokes_task"},
                    {"relation": "asks_question"},
                    {"relation": "uses_interaction"},
                    {"relation": "queries_target"},
                    {"relation": "uses_model"},
                ]
            },
        },
        {"reuse": {"findings": []}, "debt": {"findings": []}},
    )

    for name in (
        "architecture_score",
        "maintainability_score",
        "reusability_score",
        "screenplay_score",
        "overall_score",
    ):
        assert 0 <= result[name] <= 100
    assert set(result["scores"]) == {
        "architecture",
        "maintainability",
        "reusability",
        "screenplay_compliance",
        "overall_quality",
    }


def test_scoring_engine_penalizes_cycles_detected_from_relationships() -> None:
    result = ScoringEngine().calculate(
        {
            "architecture-map": {"scan_errors": []},
            "dependency-graph": {
                "nodes": [{"id": "component:a"}, {"id": "component:b"}],
                "edges": [],
            },
            "dependency-map": {
                "relationships": [
                    {
                        "source_id": "component:a",
                        "target_id": "component:b",
                        "relation": "uses_model",
                    },
                    {
                        "source_id": "component:b",
                        "target_id": "component:a",
                        "relation": "uses_model",
                    },
                ]
            },
        },
        {},
    )

    assert result["architecture_score"] == 70


def test_recommendations_are_consolidated_deduplicated_and_prioritized() -> None:
    analyses = {
        "architecture": {
            "recommendations": [
                {
                    "title": "Check graph",
                    "action": "Review cycles",
                    "severity": "high",
                },
                {
                    "title": "Check graph",
                    "action": "Review cycles",
                    "severity": "high",
                },
            ]
        },
        "debt": {
            "recommendations": [
                {
                    "title": "Inspect components",
                    "action": "Validate references",
                    "severity": "medium",
                }
            ]
        },
        "compliance": {
            "recommendations": [
                {
                    "title": "Review roles",
                    "action": "Inspect source",
                    "severity": "low",
                }
            ]
        },
    }

    result = RecommendationEngine().build(analyses)

    assert [item["priority"] for item in result] == ["P1", "P2", "P3"]
    assert len(result) == 3
    assert {item["category"] for item in result} == {
        "architecture",
        "debt",
        "screenplay",
    }
