from typing import Any


class PrioritizationEngine:
    _PRIORITY_ORDER = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}
    _SEVERITY_PRIORITY = {
        "critical": "P1",
        "high": "P1",
        "medium": "P2",
        "low": "P3",
        "info": "P4",
    }

    def prioritize(
        self,
        recommendations: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        prioritized = [
            {
                **item,
                "priority": self._SEVERITY_PRIORITY.get(
                    str(item.get("severity", "info")).lower(),
                    "P4",
                ),
            }
            for item in recommendations
        ]
        return sorted(
            prioritized,
            key=lambda item: (
                self._PRIORITY_ORDER[item["priority"]],
                str(item.get("category", "")),
                str(item.get("title", "")),
            ),
        )
