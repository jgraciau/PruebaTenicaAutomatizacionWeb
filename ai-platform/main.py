import argparse
import json
import logging
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import Sequence

from adapters.registry import create_adapter
from core.knowledge_builder import KnowledgeBuilder
from core.project_config import ConfigurationError, ProjectConfig, load_project_config
from core.reporting import render_html_report, render_markdown_report

logger = logging.getLogger("skp")
_DEFAULT_CONFIG = Path(__file__).resolve().parent / "config" / "project.yaml"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _apply_overrides(
    config: ProjectConfig,
    root: Path | None,
    output: Path | None,
) -> ProjectConfig:
    overrides: dict[str, object] = {}
    if root is not None:
        new_root = root.expanduser().resolve()
        rebased_paths = {
            key: tuple(
                (
                    new_root / path.relative_to(config.project_root)
                ).resolve()
                if path.is_relative_to(config.project_root)
                else path
                for path in locations
            )
            for key, locations in config.paths.items()
        }
        overrides["project_root"] = new_root
        overrides["paths"] = rebased_paths
    if output is not None:
        output = output.expanduser().resolve()
        overrides["knowledge_output"] = output / "knowledge"
        overrides["reports_output"] = output / "outputs"
    return replace(config, **overrides)


def run_configured(
    config_path: Path,
    root: Path | None = None,
    output: Path | None = None,
    preflight_only: bool = False,
) -> int:
    config = _apply_overrides(
        load_project_config(config_path),
        root,
        output,
    )
    result = create_adapter(config).analyze()
    readiness = (
        "ready"
        if result.source_files_scanned
        and not result.scan_errors
        and (result.features or result.tasks or result.questions or result.interactions)
        else "partial"
        if result.source_files_scanned
        else "unsupported"
    )
    profile = {
        "project": asdict(result.project),
        "readiness": readiness,
        "source_files_scanned": result.source_files_scanned,
        "component_counts": {
            "features": len(result.features),
            "step_definitions": len(result.step_definitions),
            "tasks": len(result.tasks),
            "questions": len(result.questions),
            "interactions": len(result.interactions),
            "targets": len(result.targets),
            "models": len(result.models),
        },
        "scan_errors": result.scan_errors,
        "configured_paths": {
            name: [
                path.relative_to(config.project_root).as_posix()
                if path.is_relative_to(config.project_root)
                else path.name
                for path in paths
            ]
            for name, paths in config.paths.items()
        },
    }
    for error in result.scan_errors:
        logger.warning("%s", error)
    try:
        config.reports_output.mkdir(parents=True, exist_ok=True)
        _write_json(config.reports_output / "project-profile.json", profile)
        if preflight_only:
            logger.info(
                "Configuration preflight written to %s (readiness=%s)",
                config.reports_output / "project-profile.json",
                readiness,
            )
            return 0 if readiness != "unsupported" else 1

        maps = KnowledgeBuilder().build(result)
        config.knowledge_output.mkdir(parents=True, exist_ok=True)
        for name, data in maps.items():
            _write_json(config.knowledge_output / f"{name}.json", data)
        (config.reports_output / "architecture-report.md").write_text(
            render_markdown_report(maps),
            encoding="utf-8",
        )
        quality_score = None
        quality_score_path = config.reports_output / "quality-score.json"
        if quality_score_path.is_file():
            try:
                candidate = json.loads(
                    quality_score_path.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError) as exc:
                logger.warning(
                    "Ignoring invalid optional quality score %s: %s",
                    quality_score_path,
                    exc,
                )
            else:
                if (
                    isinstance(candidate, dict)
                    and candidate.get("project") == result.project.name
                    and isinstance(candidate.get("scores"), dict)
                ):
                    quality_score = candidate
                else:
                    logger.warning(
                        "Ignoring quality score %s because it does not match project %s",
                        quality_score_path,
                        result.project.name,
                    )
        (config.reports_output / "architecture-report.html").write_text(
            render_html_report(maps, quality_score=quality_score),
            encoding="utf-8",
        )
    except OSError as exc:
        logger.error("Unable to write SKP artifacts: %s", exc)
        return 2

    logger.info(
        "Generated SKP knowledge and reports in %s and %s",
        config.knowledge_output,
        config.reports_output,
    )
    return 0 if readiness != "unsupported" else 1


def run(root: Path, output: Path) -> int:
    """Backward-compatible entry point for the original Serenity FKA maps."""
    from adapters.serenity_screenplay.legacy.builders.architecture_builder import (
        ArchitectureBuilder,
    )
    from adapters.serenity_screenplay.legacy.builders.dependency_builder import (
        DependencyBuilder,
    )
    from adapters.serenity_screenplay.legacy.builders.html_report_builder import (
        render_html_report as render_legacy_html,
    )
    from adapters.serenity_screenplay.legacy.builders.report_builder import (
        render_report,
    )
    from adapters.serenity_screenplay.legacy.builders.screenplay_builder import (
        ScreenplayBuilder,
    )
    from adapters.serenity_screenplay.legacy.common.serialization import write_json
    from adapters.serenity_screenplay.legacy.scanner.project_profile import (
        ProjectProfileAnalyzer,
    )
    from adapters.serenity_screenplay.legacy.scanner.project_scanner import (
        ProjectScanner,
    )

    profile = ProjectProfileAnalyzer().analyze(root)
    scan = ProjectScanner().scan(root, profile)
    if profile.readiness != "ready":
        logger.warning(
            "Legacy profile readiness is %s: %s",
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
            render_report(architecture, screenplay, dependencies),
            encoding="utf-8",
        )
        (report_directory / "architecture-report.html").write_text(
            render_legacy_html(architecture, screenplay, dependencies),
            encoding="utf-8",
        )
    except OSError as exc:
        logger.error("Unable to write legacy output artifacts: %s", exc)
        return 2
    return 1 if scan.errors and not scan.project_files else 0


def run_preflight(root: Path, output: Path) -> int:
    """Backward-compatible preflight for callers using the original FKA API."""
    from adapters.serenity_screenplay.legacy.common.serialization import write_json
    from adapters.serenity_screenplay.legacy.scanner.project_profile import (
        ProjectProfileAnalyzer,
    )

    profile = ProjectProfileAnalyzer().analyze(root)
    try:
        write_json(output / "outputs" / "project-profile.json", profile.to_dict())
    except OSError as exc:
        logger.error("Unable to write project profile: %s", exc)
        return 2
    if profile.warnings:
        for warning in profile.warnings:
            logger.warning("%s", warning)
    return 1 if not profile.scan.project_files else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate framework-independent Screenplay knowledge maps."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=_DEFAULT_CONFIG,
        help="Project YAML configuration (default: config/project.yaml).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Optional project root override; configured paths are rebased to it.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output directory override with knowledge/ and outputs/ subfolders.",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate configured sources and write project-profile.json only.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args(argv)
    try:
        return run_configured(
            args.config,
            root=args.root,
            output=args.output,
            preflight_only=args.preflight_only,
        )
    except (ConfigurationError, OSError, ValueError) as exc:
        logger.error("SKP failed: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
