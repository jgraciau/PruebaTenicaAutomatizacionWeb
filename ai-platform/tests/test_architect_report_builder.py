import json

from agents.architect.reports.architect_report_builder import (
    ArchitectReportBuilder,
)


def test_report_builder_writes_all_requested_reports(tmp_path) -> None:
    result = {
        "maps": {"architecture-map": {"project": {"name": "Sample"}}},
        "analyses": {
            "architecture": {
                "findings": [
                    {
                        "title": "Connected map",
                        "description": "Architecture is mapped.",
                        "evidence": "3 edges",
                        "severity": "low",
                    }
                ]
            },
            "debt": {"findings": [], "recommendations": []},
            "risk": {"risks": []},
            "compliance": {"findings": [], "recommendations": []},
            "reuse": {"findings": [], "recommendations": []},
        },
        "scores": {
            "architecture_score": 90,
            "maintainability_score": 90,
            "reusability_score": 80,
            "screenplay_score": 80,
            "overall_score": 85,
            "score_scale": {"range": "0-100"},
            "scores": {
                "overall_quality": {
                    "score": 85,
                    "classification": "LOW",
                    "rationale": "Sample score",
                }
            },
        },
        "recommendations": [
            {
                "priority": "P2",
                "title": "Review source",
                "action": "Validate evidence",
                "category": "screenplay",
                "evidence": "Static maps",
            }
        ],
    }
    builder = ArchitectReportBuilder()

    written = builder.write(tmp_path, result)

    assert {path.name for path in written} == set(builder.REPORT_FILES.values())
    quality = json.loads((tmp_path / "quality-score.json").read_text(encoding="utf-8"))
    assert quality["score_values"]["overall_score"] == 85
    assert "## P2" in (tmp_path / "improvement-plan.md").read_text(
        encoding="utf-8"
    )
    assert "Connected map" in (tmp_path / "architecture-review.md").read_text(
        encoding="utf-8"
    )
