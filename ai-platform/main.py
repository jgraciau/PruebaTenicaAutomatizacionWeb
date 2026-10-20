import argparse
import logging
import sys
from pathlib import Path

from core.builders.architecture_builder import ArchitectureBuilder
from core.builders.dependency_builder import DependencyBuilder
from core.builders.html_report_builder import render_html_report
from core.builders.report_builder import render_report
from core.builders.screenplay_builder import ScreenplayBuilder
from core.common.constants import DEFAULT_OUTPUT_DIR
from core.common.logger import get_logger
from core.common.serialization import write_json
from core.scanner.project_scanner import ProjectScanner
from core.scanner.project_profile import ProjectProfileAnalyzer

logger: logging.Logger = get_logger(__name__)


def run(root: Path, output: Path) -> int:
    profile = ProjectProfileAnalyzer().analyze(root)
    scanner = ProjectScanner()
    scan = scanner.scan(root, profile)
    if profile.readiness != "ready":
        logger.warning(
            "Project profile readiness is %s: %s",
            profile.readiness,
            "; ".join(profile.warnings) or "review detected conventions",
        )
    if scan.errors and not scan.project_files:
        logger.error("No files could be scanned. See scan diagnostics.")
    architecture = ArchitectureBuilder().build(scan)
    dependencies = DependencyBuilder().build(architecture)
    architecture = ArchitectureBuilder.add_quality_audit(architecture, dependencies)
    screenplay = ScreenplayBuilder().build(architecture, dependencies)
    try:
        write_json(output / "outputs" / "project-profile.json", profile.to_dict())
        write_json(output / "knowledge" / "architecture-map.json", architecture)
        write_json(output / "knowledge" / "screenplay-map.json", screenplay)
        write_json(output / "knowledge" / "dependency-map.json", dependencies)
        report_directory = output / "outputs"
        report_directory.mkdir(parents=True, exist_ok=True)
        (report_directory / "architecture-report.md").write_text(
            render_report(architecture, screenplay, dependencies), encoding="utf-8"
        )
        (report_directory / "architecture-report.html").write_text(
            render_html_report(architecture, screenplay, dependencies), encoding="utf-8"
        )
    except OSError as exc:
        logger.error("Unable to write output artifacts: %s", exc)
        return 2
    logger.info(
        "Generated maps and reports (JSON, Markdown, HTML in Spanish) in %s",
        output.resolve(),
    )
    return 1 if scan.errors and not scan.project_files else 0


def run_preflight(root: Path, output: Path) -> int:
    profile = ProjectProfileAnalyzer().analyze(root)
    try:
        write_json(output / "outputs" / "project-profile.json", profile.to_dict())
    except OSError as exc:
        logger.error("Unable to write project profile: %s", exc)
        return 2
    if profile.warnings:
        for warning in profile.warnings:
            logger.warning("%s", warning)
    logger.info(
        "Preflight profile written to %s (readiness=%s)",
        (output / "outputs" / "project-profile.json").resolve(),
        profile.readiness,
    )
    return 1 if not profile.scan.project_files else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract static knowledge from a Java/Screenplay project.")
    parser.add_argument("--root", type=Path, default=DEFAULT_OUTPUT_DIR.parent, help="Project root to scan (default: parent of ai-platform).")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory for knowledge/ and outputs/ (default: ai-platform).")
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate the project structure and write project-profile.json without building maps.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.preflight_only:
            return run_preflight(args.root, args.output)
        return run(args.root, args.output)
    except (OSError, ValueError) as exc:
        logger.exception("FKA failed: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
