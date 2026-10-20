from typing import Any

from agents.architect.analyzers.compliance_analyzer import ComplianceAnalyzer
from agents.architect.analyzers.debt_analyzer import DebtAnalyzer
from agents.architect.analyzers.risk_analyzer import RiskAnalyzer
from agents.architect.analyzers.reuse_analyzer import ReuseAnalyzer


def test_debt_analyzer_detects_unlinked_duplicate_and_unused_components() -> None:
    maps: dict[str, dict[str, Any]] = {
        "architecture-map": {
            "tasks": [
                {"id": "task:1", "name": "SubmitOrder", "references": []},
                {"id": "task:2", "name": "SubmitOrder", "references": []},
            ],
            "questions": [],
            "interactions": [],
            "targets": [],
            "models": [],
            "scenarios": [],
        },
        "dependency-map": {"relationships": []},
    }

    result = DebtAnalyzer().analyze(maps)

    finding_ids = {item["id"] for item in result["findings"]}
    assert "debt.unlinked-components" in finding_ids
    assert "debt.duplicate-components" in finding_ids
    assert "debt.unused-components" in finding_ids


def test_risk_analyzer_detects_complexity_coupling_and_dependencies() -> None:
    edges = [
        {"source_id": "node:hub", "target_id": f"node:{index}"}
        for index in range(10)
    ]
    maps: dict[str, dict[str, Any]] = {
        "architecture-map": {"project": {"scan_errors": []}},
        "dependency-map": {"relationships": edges},
        "dependency-graph": {
            "nodes": [
                {"id": "node:hub", "complexity": 12},
                *[{"id": f"node:{index}"} for index in range(10)],
            ],
            "edges": edges,
        },
    }

    result = RiskAnalyzer().analyze(maps)

    risk_ids = {item["id"] for item in result["risks"]}
    assert "risk.high-dependency" in risk_ids
    assert "risk.high-coupling" in risk_ids
    assert "risk.high-complexity" in risk_ids


def test_compliance_analyzer_reports_srp_evidence_limit_and_candidates() -> None:
    maps: dict[str, dict[str, Any]] = {
        "architecture-map": {
            "tasks": [
                {
                    "id": "task:split",
                    "responsibilities": ["submit", "notify"],
                }
            ],
        },
        "dependency-map": {"relationships": []},
    }

    result = ComplianceAnalyzer().analyze(maps)

    finding_ids = {item["id"] for item in result["findings"]}
    assert "compliance.srp-candidates" in finding_ids
    assert "compliance.missing-components" in finding_ids


def test_reuse_analyzer_identifies_shared_task_question_and_interaction() -> None:
    maps: dict[str, dict[str, Any]] = {
        "architecture-map": {
            "tasks": [{"id": "task:shared", "name": "SharedTask"}],
            "questions": [{"id": "question:shared", "name": "SharedQuestion"}],
            "interactions": [
                {"id": "interaction:shared", "name": "SharedInteraction"}
            ],
            "scenarios": [],
        },
        "dependency-map": {
            "relationships": [
                {"source_id": "step:one", "target_id": "task:shared"},
                {"source_id": "step:two", "target_id": "task:shared"},
                {"source_id": "task:one", "target_id": "question:shared"},
                {"source_id": "task:two", "target_id": "question:shared"},
                {
                    "source_id": "task:one",
                    "target_id": "interaction:shared",
                },
                {
                    "source_id": "task:two",
                    "target_id": "interaction:shared",
                },
            ]
        },
    }

    result = ReuseAnalyzer().analyze(maps)

    finding_ids = {item["id"] for item in result["findings"]}
    assert {"reuse.tasks", "reuse.questions", "reuse.interactions"} <= finding_ids
    assert len(result["recommendations"]) == 1
