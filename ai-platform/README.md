# Screenplay Knowledge Platform (SKP)

SKP extracts a framework-neutral model of a configured Screenplay project. The
core contains universal project models, configuration loading, source reading,
relationship building, and reporting. Framework-specific discovery and
translation live behind interchangeable adapters.

## Requirements

Python 3.10 or later.

```powershell
python -m pip install -r requirements.txt
```

## Run

From this directory, run the configured project:

```powershell
python main.py
```

The default configuration is [config/project.yaml](config/project.yaml). Paths
under `project.root` are resolved relative to the configuration file; component
paths are resolved relative to the project root. Knowledge and report output
paths are resolved relative to the configuration file. To analyze another
repository, update this YAML file without changing platform code.

The CLI also accepts an alternate configuration and optional one-run overrides:

```powershell
python main.py --config "C:\work\other-project\skp.yaml"
python main.py --config "C:\work\other-project\skp.yaml" --preflight-only
```

`framework.type` selects Serenity, Playwright, or Selenium adapters. Unknown
framework names use the generic adapter. `language.extensions` controls which
source files are read; each component location is configured independently.
The generic adapter recognizes common class/function declarations, Gherkin
features and steps, Screenplay component references, and common locator
expressions. `features.extensions` can change the specification file suffix,
and `parser_patterns` can define capture-group regular expressions for
declarations, features, scenarios, steps, step definitions, targets, and actors
that use proprietary conventions. Framework-specific semantics not expressible
as configured patterns require a focused adapter.

## Configuration example

```yaml
project:
  name: Ecommerce Automation
  root: ../..

framework:
  type: serenity

language:
  type: java
  extensions: [.java]

pattern:
  type: screenplay

paths:
  features: test/resources/features
  tasks: src/main/java/tasks
  questions: src/main/java/questions
  interactions: src/main/java/interactions
  step_definitions: test/java/stepDefinitions
  user_interfaces: src/main/java/userInterfaces
  models: src/main/java/models

outputs:
  knowledge: ../knowledge
  reports: ../outputs
```

Each path can be a single path or a list of paths. A missing component path can
be omitted or set to an empty list.

## Generated artifacts

`knowledge/` contains `architecture-map.json`, `screenplay-map.json`,
`dependency-map.json`, `relationship-map.json`, and `dependency-graph.json`.
`outputs/` contains an analysis profile and the Markdown and HTML architecture
reports. Dependency data remains available as JSON knowledge maps; dependency
reports are not generated. JSON is UTF-8 and paths in the maps are
project-relative.

The Spanish-language HTML architecture report is organized for product owners.
It includes an executive reading, architecture observations, candidate technical
debt, risks, Screenplay compliance, reuse opportunities, dependency analysis,
and a prioritized improvement plan, in addition to scenario and flow coverage.
All findings come from the generated maps and distinguish missing relationships
from confirmed dead code. The report states that static traceability is not proof
that tests passed. If `outputs/quality-score.json` exists for the configured
project, its scores are shown with Spanish explanations; otherwise the report
shows a qualitative assessment. Invalid or mismatched score files are ignored
with a warning. The Markdown report remains a concise architecture summary.

Relationships include feature-to-scenario, scenario-to-step-definition,
step-definition-to-task, task-to-interaction/question/model, and
question/interaction-to-target. Feature-to-step matching is static and
heuristic; direct source references are recorded as evidence.

## Architect Agent

Run the Sprint 2 architectural analysis after generating the knowledge maps:

```powershell
python run_architect.py
```

The orchestrator loads the five maps from `knowledge/`, then runs the
architecture, risk, technical-debt, Screenplay-compliance, and reuse analyzers.
It calculates quality scores, consolidates recommendations into P1-P4
priorities, and writes the architecture review, debt, risk, compliance, reuse,
improvement-plan, and quality-score reports to `outputs/`.

Alternate knowledge and report directories can be supplied without changing
the project configuration:

```powershell
python run_architect.py --knowledge-dir "C:\work\skp\knowledge" --output-dir "C:\work\skp\outputs"
```

Missing maps are logged as `KnowledgeArtifactMissingException`; other maps are
still analyzed and reports are generated with the available evidence. Scores
are static-map heuristics, not a substitute for source review or test results.

## Compatibility

The original Java/Serenity FKA scanner, parsers, and report builders remain
under `adapters/serenity_screenplay/legacy`. The `run(root, output)` and
`run_preflight(root, output)` Python entry points in `main.py` are retained for
existing callers. New executions should use the YAML-driven `python main.py`
flow.

## Tests

```powershell
python -m pytest -q
```
