import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when the external project configuration is invalid."""


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    config_path: Path
    project_name: str
    project_root: Path
    framework: str
    language: str
    pattern: str
    language_extensions: tuple[str, ...]
    feature_extensions: tuple[str, ...]
    parser_patterns: dict[str, tuple[str, ...]]
    paths: dict[str, tuple[Path, ...]]
    knowledge_output: Path
    reports_output: Path


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"'{name}' must be a YAML mapping.")
    return value


def _required_string(mapping: dict[str, Any], key: str, parent: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"'{parent}.{key}' must be a non-empty string.")
    return value.strip()


def _configured_paths(
    values: Any,
    project_root: Path,
) -> dict[str, tuple[Path, ...]]:
    if values is None:
        return {}
    if not isinstance(values, dict):
        raise ConfigurationError("'paths' must be a YAML mapping.")
    result: dict[str, tuple[Path, ...]] = {}
    for key, configured in values.items():
        if configured is None:
            result[key] = ()
            continue
        if isinstance(configured, str):
            configured = [configured]
        if not isinstance(configured, list) or not all(
            isinstance(item, str) and item.strip() for item in configured
        ):
            raise ConfigurationError(
                f"'paths.{key}' must be a path string or a list of path strings."
            )
        result[key] = tuple(
            (project_root / item).resolve() for item in configured
        )
    return result


def load_project_config(config_path: Path) -> ProjectConfig:
    config_path = config_path.expanduser().resolve()
    try:
        with config_path.open(encoding="utf-8") as config_file:
            raw = yaml.safe_load(config_file)
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to read project configuration '{config_path}': {exc}"
        ) from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML in project configuration '{config_path}': {exc}"
        ) from exc

    root_config = _mapping(raw, "configuration")
    project = _mapping(root_config.get("project"), "project")
    framework = _mapping(root_config.get("framework"), "framework")
    language = _mapping(root_config.get("language"), "language")
    pattern = _mapping(root_config.get("pattern"), "pattern")
    feature_config = _mapping(root_config.get("features", {}), "features")
    outputs = _mapping(root_config.get("outputs", {}), "outputs")
    project_root = (
        config_path.parent / _required_string(project, "root", "project")
    ).resolve()
    extensions = language.get("extensions", [])
    if isinstance(extensions, str):
        extensions = [extensions]
    if not isinstance(extensions, list) or not all(
        isinstance(item, str) and item.startswith(".") for item in extensions
    ):
        raise ConfigurationError(
            "'language.extensions' must be a list of file suffixes beginning with '.'."
        )
    feature_extensions = feature_config.get("extensions", [".feature"])
    if isinstance(feature_extensions, str):
        feature_extensions = [feature_extensions]
    if not isinstance(feature_extensions, list) or not all(
        isinstance(item, str) and item.startswith(".")
        for item in feature_extensions
    ):
        raise ConfigurationError(
            "'features.extensions' must be a list of file suffixes beginning with '.'."
        )

    parser_patterns_config = root_config.get("parser_patterns", {})
    if parser_patterns_config is None:
        parser_patterns_config = {}
    parser_patterns = _mapping(parser_patterns_config, "parser_patterns")
    normalized_patterns: dict[str, tuple[str, ...]] = {}
    for name, configured_patterns in parser_patterns.items():
        if isinstance(configured_patterns, str):
            configured_patterns = [configured_patterns]
        if not isinstance(configured_patterns, list) or not all(
            isinstance(item, str) and item for item in configured_patterns
        ):
            raise ConfigurationError(
                f"'parser_patterns.{name}' must be a regex or list of regexes."
            )
        for expression in configured_patterns:
            try:
                if re.compile(expression).groups < 1:
                    raise ConfigurationError(
                        f"'parser_patterns.{name}' regex must capture the value in group 1."
                    )
            except re.error as exc:
                raise ConfigurationError(
                    f"Invalid regex in 'parser_patterns.{name}': {exc}"
                ) from exc
        normalized_patterns[name] = tuple(configured_patterns)

    def output_path(key: str, default: str) -> Path:
        configured = outputs.get(key, default)
        if not isinstance(configured, str) or not configured.strip():
            raise ConfigurationError(f"'outputs.{key}' must be a path string.")
        return (config_path.parent / configured).resolve()

    return ProjectConfig(
        config_path=config_path,
        project_name=_required_string(project, "name", "project"),
        project_root=project_root,
        framework=_required_string(framework, "type", "framework"),
        language=_required_string(language, "type", "language"),
        pattern=_required_string(pattern, "type", "pattern"),
        language_extensions=tuple(extension.lower() for extension in extensions),
        feature_extensions=tuple(
            extension.lower() for extension in feature_extensions
        ),
        parser_patterns=normalized_patterns,
        paths=_configured_paths(root_config.get("paths", {}), project_root),
        knowledge_output=output_path("knowledge", "../knowledge"),
        reports_output=output_path("reports", "../outputs"),
    )
