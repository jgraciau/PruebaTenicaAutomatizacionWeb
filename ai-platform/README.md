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

The architecture report is an executive, Spanish-language view for product
owners: it summarizes scenarios, estimated step-to-code traceability, reusable
actions, validations, coverage by business flow, and scenario details with
recommended follow-ups. It states that results are static analysis, not proof
that tests passed.

Relationships include feature-to-scenario, scenario-to-step-definition,
step-definition-to-task, task-to-interaction/question/model, and
question/interaction-to-target. Feature-to-step matching is static and
heuristic; direct source references are recorded as evidence.

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
