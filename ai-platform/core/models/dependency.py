from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyModel:
    source: str
    target: str
    source_type: str
    target_type: str
    relation: str
    evidence: str
    feature: str = ""
    scenario: str = ""
    gherkin_step: str = ""

    def to_dict(self) -> dict[str, str]:
        result = {
            "source": self.source,
            "target": self.target,
            "source_type": self.source_type,
            "target_type": self.target_type,
            "relation": self.relation,
            "evidence": self.evidence,
        }
        if self.feature:
            result["feature"] = self.feature
            result["scenario"] = self.scenario
            result["gherkin_step"] = self.gherkin_step
        return result
