import json
from pathlib import Path
from typing import Any


class ArchitectReportBuilder:
    REPORT_FILES = {
        "architecture": "architecture-review.md",
        "debt": "technical-debt-report.md",
        "risk": "risk-report.md",
        "compliance": "screenplay-compliance-report.md",
        "reuse": "reuse-report.md",
        "improvement": "improvement-plan.md",
        "quality": "quality-score.json",
    }

    @staticmethod
    def _items(analysis: dict[str, Any], key: str) -> list[dict[str, Any]]:
        values = analysis.get(key, [])
        return [item for item in values if isinstance(item, dict)] if isinstance(
            values, list
        ) else []

    @staticmethod
    def _section_items(title: str, items: list[dict[str, Any]]) -> str:
        lines = [f"## {title}", ""]
        if not items:
            lines.extend(["No se registraron elementos en esta categoría.", ""])
            return "\n".join(lines)
        for item in items:
            lines.extend(
                [
                    f"### {item.get('title', 'Sin título')}",
                    "",
                    str(item.get("description", item.get("action", ""))),
                    "",
                    f"- **Evidencia:** {item.get('evidence', 'No especificada')}",
                    f"- **Severidad:** {str(item.get('severity', 'info')).upper()}",
                    "",
                ]
            )
        return "\n".join(lines)

    @staticmethod
    def _score_report(scores: dict[str, Any]) -> str:
        parts = ["## Puntuaciones (0-100)", ""]
        for name, value in scores.get("scores", {}).items():
            if isinstance(value, dict):
                parts.append(
                    f"- **{name}:** {value.get('score', 'N/A')}/100 "
                    f"({value.get('classification', 'N/A')}) — "
                    f"{value.get('rationale', '')}"
                )
        return "\n".join(parts + [""])

    def build(self, result: dict[str, Any]) -> dict[str, str]:
        project = result.get("maps", {}).get("architecture-map", {}).get(
            "project", {}
        )
        project_name = project.get("name", "Proyecto sin nombre")
        analyses = result.get("analyses", {})
        scores = result.get("scores", {})
        report_data = {
            "architecture": (
                f"# Revisión de arquitectura — {project_name}\n\n"
                "Valoración heurística derivada de knowledge maps; los componentes "
                "sin relaciones no se consideran automáticamente código muerto.\n\n"
                + self._score_report(scores)
                + self._section_items(
                    "Hallazgos",
                    self._items(analyses.get("architecture", {}), "findings"),
                )
            ),
            "debt": (
                f"# Informe de deuda técnica — {project_name}\n\n"
                "Los candidatos requieren validación en el código fuente.\n\n"
                + self._section_items(
                    "Hallazgos",
                    self._items(analyses.get("debt", {}), "findings"),
                )
                + self._section_items(
                    "Recomendaciones",
                    self._items(analyses.get("debt", {}), "recommendations"),
                )
            ),
            "risk": (
                f"# Informe de riesgos — {project_name}\n\n"
                "Riesgos estáticos, no resultados de ejecución.\n\n"
                + self._section_items(
                    "Riesgos",
                    self._items(analyses.get("risk", {}), "risks"),
                )
            ),
            "compliance": (
                f"# Cumplimiento Screenplay — {project_name}\n\n"
                "La presencia de categorías y relaciones no certifica "
                "responsabilidades internas ni comportamiento en ejecución.\n\n"
                + self._section_items(
                    "Hallazgos",
                    self._items(analyses.get("compliance", {}), "findings"),
                )
                + self._section_items(
                    "Recomendaciones",
                    self._items(analyses.get("compliance", {}), "recommendations"),
                )
            ),
            "reuse": (
                f"# Informe de reutilización — {project_name}\n\n"
                "Las relaciones compartidas son señales estáticas y no evidencian "
                "reutilización entre proyectos.\n\n"
                + self._section_items(
                    "Hallazgos",
                    self._items(analyses.get("reuse", {}), "findings"),
                )
                + self._section_items(
                    "Recomendaciones",
                    self._items(analyses.get("reuse", {}), "recommendations"),
                )
            ),
            "improvement": self._improvement_plan(project_name, result),
            "quality": json.dumps(
                {
                    "project": project_name,
                    "score_scale": scores.get("score_scale", {}),
                    "scores": scores.get("scores", {}),
                    "score_values": {
                        name: scores[name]
                        for name in (
                            "architecture_score",
                            "maintainability_score",
                            "reusability_score",
                            "screenplay_score",
                            "overall_score",
                        )
                        if name in scores
                    },
                    "limitations": [
                        "Las puntuaciones son heurísticas calculadas solo con knowledge maps.",
                        "No se analizaron cuerpos de métodos ni se ejecutaron pruebas.",
                        "La falta de una relación no demuestra código muerto.",
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        }
        return {
            self.REPORT_FILES[name]: content
            for name, content in report_data.items()
        }

    def _improvement_plan(
        self,
        project_name: str,
        result: dict[str, Any],
    ) -> str:
        lines = [
            f"# Plan de mejora — {project_name}",
            "",
            "Recomendaciones priorizadas mediante severidad estática; confirmar "
            "evidencia antes de aplicar cambios.",
            "",
        ]
        recommendations = result.get("recommendations", [])
        if not recommendations:
            return "\n".join(lines + ["No hay recomendaciones registradas.", ""])
        for priority in ("P1", "P2", "P3", "P4"):
            group = [
                item
                for item in recommendations
                if item.get("priority") == priority
            ]
            if not group:
                continue
            lines.extend([f"## {priority}", ""])
            for item in group:
                lines.extend(
                    [
                        f"### {item.get('title', 'Sin título')}",
                        "",
                        str(item.get("action", "")),
                        "",
                        f"- **Categoría:** {item.get('category', 'general')}",
                        f"- **Evidencia:** {item.get('evidence', 'No especificada')}",
                        "",
                    ]
                )
        return "\n".join(lines)

    def write(self, output_directory: Path, result: dict[str, Any]) -> list[Path]:
        output_directory.mkdir(parents=True, exist_ok=True)
        reports = self.build(result)
        written: list[Path] = []
        for filename, content in reports.items():
            destination = output_directory / filename
            destination.write_text(content, encoding="utf-8")
            written.append(destination)
        return written
