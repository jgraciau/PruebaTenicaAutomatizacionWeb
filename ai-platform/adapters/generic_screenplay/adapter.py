import re
from dataclasses import asdict
from typing import Any

from adapters.base import AdapterResult, ScreenplayAdapter
from core.models import (
    ActorModel,
    FeatureModel,
    InteractionModel,
    QuestionModel,
    ScenarioModel,
    StepDefinitionModel,
    TargetModel,
    TaskModel,
)
from core.models.project_model import ProjectModel
from core.source_scanner import SourceDocument, SourceScanner

_FEATURE_EXTENSION = ".feature"
_STEP_PATTERN = re.compile(
    r"""@(?:Given|When|Then|And|But|given|when|then|step)\s*"""
    r"""\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)')""",
    re.IGNORECASE,
)
_ATTRIBUTE_STEP_PATTERN = re.compile(
    r"""\[(?:Given|When|Then|And|But)\s*\(\s*"""
    r"""(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)')\s*\)\]""",
    re.IGNORECASE,
)
_CALL_STEP_PATTERN = re.compile(
    r"""\b(?:Given|When|Then|And|But)\s*\(\s*"""
    r"""(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)')""",
)
_DECLARATION_PATTERN = re.compile(
    r"^\s*(?:public\s+|private\s+|protected\s+|abstract\s+|static\s+)*"
    r"(?:class|interface|enum|def|struct|record|object|function|fn)\s+"
    r"([A-Za-z_$][\w$]*)",
    re.MULTILINE,
)
_SCENARIO_PATTERN = re.compile(
    r"^\s*(Scenario(?: Outline)?|Scenario Template):\s*(.+)$"
)
_BACKGROUND_PATTERN = re.compile(r"^\s*Background:\s*$")
_STEP_LINE_PATTERN = re.compile(
    r"^\s*(Given|When|Then|And|But|\*)\s+(.+)$", re.IGNORECASE
)
_ACTOR_PATTERN = re.compile(
    r"""(?:Actor\.named|actor\s*=\s*Actor|theActorCalled|actorCalled|actorNamed)"""
    r"""\s*\(\s*["']([^"']+)["']""",
    re.IGNORECASE,
)
_TARGET_ASSIGNMENT_PATTERN = re.compile(
    r"""\b(?:(?:Target|Locator|WebElement|By)\s+)?"""
    r"""(?P<symbol>[A-Za-z_$]\w*)\s*=\s*"""
    r"""(?:(?:page\.)?(?:Target\.(?:the|named)|get_by_role|getByRole|"""
    r"""get_by_text|getByText|get_by_label|getByLabel|locator|find_element)|"""
    r"""By\.(?:cssSelector|xpath|id|name|CSS_SELECTOR|XPATH|ID|NAME))\s*\(""",
    re.IGNORECASE,
)


class GenericScreenplayAdapter(ScreenplayAdapter):
    """Translate configured source folders into the universal SKP vocabulary."""

    target_patterns = (
        re.compile(r"""Target\.(?:the|named)\s*\(\s*["']([^"']+)["']"""),
        re.compile(r"""(?:get_by_role|getByRole)\s*\(\s*["']([^"']+)["']"""),
        re.compile(r"""(?:get_by_text|getByText)\s*\(\s*["']([^"']+)["']"""),
        re.compile(r"""(?:locator|find_element)\s*\(\s*["']([^"']+)["']"""),
        re.compile(
            r"""By\.(?:cssSelector|xpath|id|name|CSS_SELECTOR|XPATH|ID|NAME)\s*,\s*["']([^"']+)["']"""
        ),
    )

    def analyze(self) -> AdapterResult:
        if not self.config.project_root.is_dir():
            return AdapterResult(
                project=self._project_metadata(),
                scan_errors=[
                    f"Project root is not a directory: {self.config.project_root}"
                ],
            )

        scanner = SourceScanner()
        errors: list[str] = []
        source_suffixes = self.config.language_extensions or self._default_extensions(
            self.config.language
        )
        source_documents = self._scan_paths(
            scanner,
            (
                "tasks",
                "questions",
                "interactions",
                "step_definitions",
                "user_interfaces",
                "models",
            ),
            source_suffixes,
            errors,
        )
        feature_documents = self._scan_paths(
            scanner,
            ("features",),
            self.config.feature_extensions or (_FEATURE_EXTENSION,),
            errors,
        )

        tasks = self._components("tasks", source_documents["tasks"])
        questions = self._components("questions", source_documents["questions"])
        interactions = self._components(
            "interactions", source_documents["interactions"]
        )
        models = self._components("models", source_documents["models"])
        step_definitions = self._step_definitions(
            source_documents["step_definitions"]
        )
        targets = self._targets(source_documents["user_interfaces"])
        actors = self._actors(source_documents)
        features = self._features(feature_documents["features"])

        self._add_references(
            tasks,
            [*questions, *interactions, *models, *targets],
        )
        self._add_references(questions, targets)
        self._add_references(interactions, targets)
        self._add_references(
            step_definitions,
            [*tasks, *actors, *questions],
        )
        for component in [
            *tasks,
            *questions,
            *interactions,
            *step_definitions,
            *models,
        ]:
            component.pop("_source_text", None)

        return AdapterResult(
            project=self._project_metadata(),
            source_files_scanned=sum(
                len(documents)
                for documents in source_documents.values()
            )
            + len(feature_documents["features"]),
            features=features,
            step_definitions=step_definitions,
            actors=actors,
            tasks=tasks,
            questions=questions,
            interactions=interactions,
            targets=targets,
            models=models,
            scan_errors=errors,
        )

    def _project_metadata(self) -> ProjectModel:
        return ProjectModel(
            name=self.config.project_name,
            root=".",
            framework=self.config.framework,
            language=self.config.language,
            pattern=self.config.pattern,
            adapter=self.__class__.__name__,
        )

    @staticmethod
    def _default_extensions(language: str) -> tuple[str, ...]:
        known_extensions = {
            "java": (".java",),
            "python": (".py",),
            "javascript": (".js", ".jsx"),
            "typescript": (".ts", ".tsx"),
            "csharp": (".cs",),
            "c#": (".cs",),
        }
        return known_extensions.get(language.casefold(), ())

    def _scan_paths(
        self,
        scanner: SourceScanner,
        keys: tuple[str, ...],
        suffixes: tuple[str, ...],
        errors: list[str],
    ) -> dict[str, list[SourceDocument]]:
        result: dict[str, list[SourceDocument]] = {}
        for key in keys:
            documents, scan_errors = scanner.scan(
                self.config.paths.get(key, ()),
                suffixes,
                self.config.project_root,
            )
            result[key] = documents
            errors.extend(scan_errors)
        return result

    def _components(
        self,
        component_type: str,
        documents: list[SourceDocument],
    ) -> list[dict[str, Any]]:
        component_model = {
            "tasks": TaskModel,
            "questions": QuestionModel,
            "interactions": InteractionModel,
        }.get(component_type)
        components: list[dict[str, Any]] = []
        for document in documents:
            name = self._symbol_name(document)
            component_id = f"{component_type[:-1]}:{document.relative_path}"
            if component_model is not None:
                component = component_model(
                    id=component_id,
                    name=name,
                    source_path=document.relative_path,
                )
                data = asdict(component)
            else:
                data = {
                    "id": f"model:{document.relative_path}",
                    "name": name,
                    "source_path": document.relative_path,
                    "references": [],
                }
            data["_source_text"] = document.content
            components.append(data)
        return components

    def _symbol_name(self, document: SourceDocument) -> str:
        patterns = [
            re.compile(expression, re.MULTILINE)
            for expression in self.config.parser_patterns.get("declarations", ())
        ]
        patterns.append(_DECLARATION_PATTERN)
        for pattern in patterns:
            declaration = pattern.search(document.content)
            if declaration:
                return declaration.group(1)
        return document.path.stem

    def _features(self, documents: list[SourceDocument]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for document in documents:
            feature_patterns = [
                re.compile(expression, re.MULTILINE)
                for expression in self.config.parser_patterns.get("feature", ())
            ]
            feature_patterns.append(
                re.compile(r"^\s*Feature:\s*(.+)$", re.MULTILINE)
            )
            feature_match = next(
                (
                    match
                    for pattern in feature_patterns
                    if (match := pattern.search(document.content))
                ),
                None,
            )
            feature_name = (
                feature_match.group(1).strip()
                if feature_match
                else document.path.stem
            )
            feature_id = f"feature:{document.relative_path}"
            scenarios: list[ScenarioModel] = []
            background_steps: list[str] = []
            active_scenario: ScenarioModel | None = None
            in_background = False
            custom_scenario_patterns = [
                re.compile(expression)
                for expression in self.config.parser_patterns.get("scenarios", ())
            ]
            custom_step_patterns = [
                re.compile(expression)
                for expression in self.config.parser_patterns.get("steps", ())
            ]
            for line_number, line in enumerate(document.content.splitlines(), start=1):
                if _BACKGROUND_PATTERN.match(line):
                    active_scenario = None
                    in_background = True
                    continue
                scenario_match = next(
                    (
                        (match, True)
                        for pattern in custom_scenario_patterns
                        if (match := pattern.match(line))
                    ),
                    None,
                )
                if scenario_match is None:
                    default_match = _SCENARIO_PATTERN.match(line)
                    scenario_match = (
                        (default_match, False) if default_match else None
                    )
                if scenario_match:
                    match, is_custom = scenario_match
                    active_scenario = ScenarioModel(
                        id=f"scenario:{document.relative_path}:{line_number}",
                        feature_id=feature_id,
                        name=match.group(1 if is_custom else 2).strip(),
                        steps=list(background_steps),
                    )
                    scenarios.append(active_scenario)
                    in_background = False
                    continue
                step_match = next(
                    (
                        match
                        for pattern in custom_step_patterns
                        if (match := pattern.match(line))
                    ),
                    None,
                )
                if step_match:
                    step_text = step_match.group(1).strip()
                else:
                    default_step_match = _STEP_LINE_PATTERN.match(line)
                    step_text = (
                        default_step_match.group(2).strip()
                        if default_step_match
                        else ""
                    )
                if step_text and active_scenario is not None:
                    active_scenario.steps.append(step_text)
                elif step_text and in_background:
                    background_steps.append(step_text)
            result.append(
                asdict(
                    FeatureModel(
                        id=feature_id,
                        name=feature_name,
                        source_path=document.relative_path,
                        scenarios=scenarios,
                    )
                )
            )
        return result

    def _step_definitions(
        self,
        documents: list[SourceDocument],
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for document in documents:
            expressions = [
                self._capture_expression(match)
                for pattern in (
                    _STEP_PATTERN,
                    _ATTRIBUTE_STEP_PATTERN,
                    _CALL_STEP_PATTERN,
                    *(
                        re.compile(expression)
                        for expression in self.config.parser_patterns.get(
                            "step_definitions", ()
                        )
                    ),
                )
                for match in pattern.finditer(document.content)
            ]
            if expressions:
                component = StepDefinitionModel(
                    id=f"step_definition:{document.relative_path}",
                    name=self._symbol_name(document),
                    source_path=document.relative_path,
                    expressions=list(dict.fromkeys(expressions)),
                )
                data = asdict(component)
                data["_source_text"] = document.content
                result.append(data)
        return result

    @staticmethod
    def _capture_expression(match: re.Match[str]) -> str:
        return next(
            (value for value in match.groups() if value is not None),
            "",
        )

    def _targets(
        self,
        documents: list[SourceDocument],
    ) -> list[dict[str, Any]]:
        targets: list[dict[str, Any]] = []
        for document in documents:
            assignments = [
                (match.start(), match.group("symbol"))
                for match in _TARGET_ASSIGNMENT_PATTERN.finditer(document.content)
            ]
            matches = [
                match
                for pattern in (
                    *self.target_patterns,
                    *(
                        re.compile(expression)
                        for expression in self.config.parser_patterns.get(
                            "targets", ()
                        )
                    ),
                )
                for match in pattern.finditer(document.content)
            ]
            for index, match in enumerate(matches, start=1):
                target_name = match.group(1)
                symbols = [
                    symbol
                    for position, symbol in assignments
                    if position < match.start()
                ]
                targets.append(
                    asdict(
                        TargetModel(
                            id=f"target:{document.relative_path}:{index}",
                            name=target_name,
                            source_path=document.relative_path,
                            selector=target_name,
                            symbol=symbols[-1] if symbols else "",
                        )
                    )
                )
        return targets

    def _actors(
        self,
        source_documents: dict[str, list[SourceDocument]],
    ) -> list[dict[str, str]]:
        actors: dict[str, dict[str, str]] = {}
        all_documents = [
            document
            for documents in source_documents.values()
            for document in documents
        ]
        actor_patterns = [
            _ACTOR_PATTERN,
            *(
                re.compile(expression)
                for expression in self.config.parser_patterns.get("actors", ())
            ),
        ]
        for document in all_documents:
            for pattern in actor_patterns:
                for match in pattern.finditer(document.content):
                    actor_name = match.group(1)
                    actor_id = f"actor:{actor_name.casefold()}"
                    actors[actor_id] = asdict(
                        ActorModel(
                            id=actor_id,
                            name=actor_name,
                            source_path=document.relative_path,
                        )
                    )
        return list(actors.values())

    @staticmethod
    def _add_references(
        sources: list[dict[str, Any]],
        targets: list[dict[str, Any]],
    ) -> None:
        for source in sources:
            source_text = source.get("_source_text", "")
            source["references"] = [
                target["id"]
                for target in targets
                if target["id"] != source["id"]
                and any(
                    value
                    and re.search(
                        rf"\b{re.escape(value)}\b",
                        source_text,
                        re.IGNORECASE,
                    )
                    for value in (
                        target.get("symbol", ""),
                        target.get("name", ""),
                        target.get("selector", ""),
                    )
                )
            ]
