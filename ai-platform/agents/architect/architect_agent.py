import json
import logging
from pathlib import Path
from time import perf_counter
from typing import Any

from adapters.serenity_screenplay.legacy.common.logger import get_logger
from agents.architect.analyzers.architecture_analyzer import ArchitectureAnalyzer
from agents.architect.analyzers.compliance_analyzer import ComplianceAnalyzer
from agents.architect.analyzers.debt_analyzer import DebtAnalyzer
from agents.architect.analyzers.reuse_analyzer import ReuseAnalyzer
from agents.architect.analyzers.risk_analyzer import RiskAnalyzer
from agents.architect.engines.recommendation_engine import RecommendationEngine
from agents.architect.engines.scoring_engine import ScoringEngine
from agents.architect.models.analysis_result import AnalysisResult
from agents.architect.reports.architect_report_builder import ArchitectReportBuilder


class KnowledgeArtifactMissingException(FileNotFoundError):
    """Raised and recorded when a required knowledge map is unavailable."""


class KnowledgeArtifactInvalidException(ValueError):
    """Raised and recorded when a knowledge map is invalid JSON or shape."""


class ArchitectAgent:
    REQUIRED_KNOWLEDGE_MAPS = (
        "architecture-map",
        "dependency-map",
        "relationship-map",
        "dependency-graph",
        "screenplay-map",
    )

    def __init__(
        self,
        knowledge_directory: Path | None = None,
        output_directory: Path | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        platform_root = Path(__file__).resolve().parents[2]
        self.knowledge_directory = (
            knowledge_directory or platform_root / "knowledge"
        ).expanduser().resolve()
        self.output_directory = (
            output_directory or platform_root / "outputs"
        ).expanduser().resolve()
        self.logger = logger or get_logger("skp.architect")
        self.report_builder = ArchitectReportBuilder()
        self.scoring_engine = ScoringEngine()
        self.recommendation_engine = RecommendationEngine()
        self.analyzers = {
            "architecture": ArchitectureAnalyzer(),
            "risk": RiskAnalyzer(),
            "debt": DebtAnalyzer(),
            "compliance": ComplianceAnalyzer(),
            "reuse": ReuseAnalyzer(),
        }
        self.result = AnalysisResult()

    @property
    def knowledge(self) -> dict[str, dict[str, Any]]:
        return self.result.maps

    @property
    def analysis(self) -> dict[str, Any]:
        return self.result.to_dict()

    def load_knowledge(self) -> dict[str, dict[str, Any]]:
        started = perf_counter()
        self.logger.info("Starting knowledge-map loading")
        self.result.maps.clear()
        errors: list[str] = []
        for map_name in self.REQUIRED_KNOWLEDGE_MAPS:
            artifact = self.knowledge_directory / f"{map_name}.json"
            try:
                with artifact.open(encoding="utf-8") as map_file:
                    data = json.load(map_file)
                if not isinstance(data, dict):
                    raise KnowledgeArtifactInvalidException(
                        f"KnowledgeArtifactInvalidException: '{artifact}' must contain a JSON object."
                    )
            except FileNotFoundError:
                error = KnowledgeArtifactMissingException(
                    f"KnowledgeArtifactMissingException: required map '{artifact}' was not found."
                )
                errors.append(str(error))
                self.logger.error("%s", error)
                self.result.maps[map_name] = {}
                continue
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                error = KnowledgeArtifactInvalidException(
                    f"KnowledgeArtifactInvalidException: unable to read '{artifact}': {exc}"
                )
                errors.append(str(error))
                self.logger.error("%s", error)
                self.result.maps[map_name] = {}
                continue
            except OSError as exc:
                errors.append(f"Unable to read knowledge map '{artifact}': {exc}")
                self.logger.error("Unable to read knowledge map '%s': %s", artifact, exc)
                self.result.maps[map_name] = {}
                continue
            self.result.maps[map_name] = data
        self.result.errors = errors
        self.logger.info(
            "Finished knowledge-map loading in %.3f seconds (%s errors)",
            perf_counter() - started,
            len(errors),
        )
        return self.result.maps

    def _run_analyzer(self, name: str) -> dict[str, list[dict[str, Any]]]:
        started = perf_counter()
        self.logger.info("Starting %s analysis", name)
        try:
            result = self.analyzers[name].analyze(self.knowledge)
        except Exception:
            self.logger.exception("%s analysis failed", name)
            raise
        elapsed = perf_counter() - started
        self.logger.info("Finished %s analysis in %.3f seconds", name, elapsed)
        self.result.analyses[name] = result
        return result

    def run_architecture_analysis(self) -> dict[str, list[dict[str, Any]]]:
        return self._run_analyzer("architecture")

    def run_risk_analysis(self) -> dict[str, list[dict[str, Any]]]:
        return self._run_analyzer("risk")

    def run_debt_analysis(self) -> dict[str, list[dict[str, Any]]]:
        return self._run_analyzer("debt")

    def run_compliance_analysis(self) -> dict[str, list[dict[str, Any]]]:
        return self._run_analyzer("compliance")

    def run_reuse_analysis(self) -> dict[str, list[dict[str, Any]]]:
        return self._run_analyzer("reuse")

    def calculate_scores(self) -> dict[str, Any]:
        started = perf_counter()
        self.logger.info("Starting scoring")
        scores = self.scoring_engine.calculate(
            self.knowledge,
            self.result.analyses,
        )
        self.result.scores = scores
        self.logger.info(
            "Finished scoring in %.3f seconds", perf_counter() - started
        )
        return scores

    def build_recommendations(self) -> list[dict[str, Any]]:
        started = perf_counter()
        self.logger.info("Starting recommendation generation")
        recommendations = self.recommendation_engine.build(
            self.analysis["analyses"]
        )
        self.result.recommendations = recommendations
        self.logger.info(
            "Finished recommendation generation in %.3f seconds (%s recommendations)",
            perf_counter() - started,
            len(recommendations),
        )
        return recommendations

    def generate_reports(self) -> list[Path]:
        started = perf_counter()
        self.logger.info("Starting report generation")
        reports = self.report_builder.write(
            self.output_directory,
            self.result.to_dict(),
        )
        self.logger.info(
            "Finished report generation in %.3f seconds (%s reports)",
            perf_counter() - started,
            len(reports),
        )
        return reports

    def execute(self) -> dict[str, Any]:
        started = perf_counter()
        self.logger.info("Starting Architect Agent analysis")
        try:
            self.load_knowledge()
            self.run_architecture_analysis()
            self.run_risk_analysis()
            self.run_debt_analysis()
            self.run_compliance_analysis()
            self.run_reuse_analysis()
            self.calculate_scores()
            self.build_recommendations()
            self.generate_reports()
            return self.result.to_dict()
        except Exception:
            self.logger.exception("Architect Agent analysis failed")
            raise
        finally:
            self.logger.info(
                "Finished Architect Agent analysis in %.3f seconds",
                perf_counter() - started,
            )
