from typing import Any

from agents.architect.engines.prioritization_engine import PrioritizationEngine


class RecommendationEngine:
    _SOURCES = (
        ("architecture", "architecture"),
        ("risk", "risk"),
        ("debt", "debt"),
        ("compliance", "screenplay"),
        ("reuse", "reuse"),
    )

    def __init__(
        self,
        prioritization_engine: PrioritizationEngine | None = None,
    ) -> None:
        self.prioritization_engine = (
            prioritization_engine or PrioritizationEngine()
        )

    def build(
        self,
        analyses: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        consolidated: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for source, category in self._SOURCES:
            analysis = analyses.get(source, {})
            items = analysis.get("recommendations", [])
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", "")).strip()
                action = str(item.get("action", "")).strip()
                if not title or not action:
                    continue
                key = (title.casefold(), action.casefold())
                if key in seen:
                    continue
                seen.add(key)
                consolidated.append(
                    {
                        **item,
                        "category": category,
                        "title": title,
                        "action": action,
                        "severity": str(item.get("severity", "info")).lower(),
                        "source_analyzer": source,
                    }
                )
        return self.prioritization_engine.prioritize(consolidated)
