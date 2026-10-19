import re
from typing import Any

from core.common.models import SourceFile


class FeatureParser:
    STEP_KEYWORDS = {"Given", "When", "Then", "And", "But", "*", "Dado", "Dada", "Dados", "Dadas", "Cuando", "Entonces", "Y", "Pero"}

    def parse(self, source: SourceFile) -> dict[str, Any]:
        feature = ""
        background: list[str] = []
        scenarios: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        in_background = False
        in_examples = False
        for line_number, raw in enumerate(source.content.splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r"^(Feature|Característica|Caracteristica):\s*(.+)$", line, re.IGNORECASE)
            if match:
                feature = match.group(2).strip()
                continue
            match = re.match(r"^(Scenario Outline|Scenario Template|Scenario|Esquema del escenario|Plantilla del escenario|Escenario):\s*(.+)$", line, re.IGNORECASE)
            if match:
                current = {"name": match.group(2).strip(), "line": line_number, "steps": [], "examples": []}
                scenarios.append(current)
                in_background = False
                in_examples = False
                continue
            match = re.match(r"^(Background|Antecedentes):", line, re.IGNORECASE)
            if match:
                in_background = True
                current = None
                continue
            if current is not None and line.lower().startswith(("examples:", "example:", "ejemplos:", "ejemplo:")):
                in_examples = True
                continue
            if line.startswith("|") and current is not None and in_examples:
                current["examples"].append(line)
                continue
            keyword_match = re.match(r"^(Given|When|Then|And|But|Dado|Dada|Dados|Dadas|Cuando|Entonces|Y|Pero|\*)\s+(.+)$", line, re.IGNORECASE)
            if keyword_match:
                step = {"keyword": keyword_match.group(1), "text": keyword_match.group(2).strip(), "line": line_number}
                if current is not None:
                    current["steps"].append(step)
                elif in_background:
                    background.append(step["text"])
        return {"path": source.relative_path, "name": feature or source.path.stem, "background": background, "scenarios": scenarios}
