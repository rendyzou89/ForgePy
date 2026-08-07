# ForgePy Project Context

## Project snapshot

- **Name:** ForgePy
- **Purpose:** generate a structured starter Python project from a CLI, then prepare its virtual environment, dependencies, Git repository, and VS Code configuration.
- **Protected stable branch policy:** treat `master` as protected and stable
- **Current stable release/tag:** `v0.6.0` (`Sprint 6 Stable`)
- **Current development area:** Sprint 7.4 configuration-backed create defaults, building on the persistent configuration and CLI foundations.

`config/version.py` is the canonical ForgePy version source and reports `0.6.0`, matching the `v0.6.0` stable release tag. No release tag newer than `v0.6.0` exists.

## ForgePy Philosophy

ForgePy favors understandable automation, explicit architectural boundaries, compatibility-conscious evolution, and generated projects that remain easy for their owners to inspect. See [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) for the project-wide design and review policy.

## Implemented capabilities

- Parse and dispatch `create`, `list`, `version`, and `config` commands through one shared catalog.
- Fall back to an interactive create workflow when no command is supplied.
- Register and list the single `basic` project template.
- Generate the configured folder layout and nine root files.
- Create `.venv`, upgrade `pip`, `setuptools`, and `wheel`, and install generated requirements.
- Initialize Git, stage generated content, and attempt an initial commit.
- Generate four VS Code configuration files.
- Load, validate, update, reset, and atomically save user configuration at `~/.forgepy/config.json` through `ConfigStore`.
- Show, set, and reset persistent values through `python main.py config` without duplicating storage logic in the CLI.
- Resolve omitted create location and template values from `default_location` and `default_template`, after explicit CLI arguments and before the existing prompt/`basic` fallback.
- Test the configuration store, configuration CLI, and create-input precedence with `unittest` and isolated temporary home directories.

`ConfigCommand` manages all persisted values. `CreateCommand` consumes only `default_location` and `default_template`; `author` and `license` remain unused. `ProjectGenerator` does not depend on `ConfigStore`, and project-generation stages, folder layout, and generated files remain unchanged.

## Repository structure

| Path | Current role |
| --- | --- |
| `builders/` | Folder/file creation and packaging-tool updates. |
| `cli/` | Parser, dispatcher, command contract, and commands. |
| `config/` | Version metadata, generated folder defaults, and user-level JSON configuration. |
| `core/` | Project lifecycle and environment, Git, requirements, and VS Code services. |
| `models/` | `ProjectConfig` data model. |
| `templates/` | Basic template, registry, file mapping, rendered content, and VS Code JSON. |
| `utils/` | Present but currently contains no implemented utility behavior. |
| `tests/` | Standard-library automated tests for configuration storage, CLI management, and create-input resolution. |
| `main.py` | Executable application entry point. |

The root `README.md`, `requirements.txt`, and `config.py` are currently empty.

## Technical constraints

- Full generation is Windows-oriented: environment tools are addressed under `.venv/Scripts` with `.exe` filenames.
- ForgePy itself has no declared third-party runtime dependencies. Automated coverage currently focuses on user configuration, its CLI command, and create-input resolution. The generated `basic` project requires `PySide6`, `pandas`, and `openpyxl`, so the full create lifecycle attempts package installation and may require network access.
- Template lookup uses direct dictionary indexing; an unknown template is not converted into a friendly CLI error.
- Subprocess failures generally propagate because commands use `check=True`.
- Generation uses `exist_ok=True`, so an existing target can be written into rather than rejected.
- Generated template metadata requires Python `>=3.12`, but the ForgePy repository itself does not declare a supported Python range.
- `config.default_structure.DEFAULT_FILES` is defined but is not used by the current template workflow; `TemplateFiles.basic()` determines generated root files.

## Near-term priorities

- Finish and verify Sprint 7 CLI behavior without breaking interactive creation.
- Keep `author`, `license`, and the configuration store itself out of core generation and templates until a separate requirement explicitly defines that integration.
- Expand automated coverage to supported commands, template output, and failure handling.
- Document platform and Python support based on verified behavior.

## Long-term v1.0 direction

The repository does not define guaranteed v1.0 features. A realistic direction is a stable, documented CLI and template contract; predictable project-generation behavior; consistent versioning; and automated verification of the existing lifecycle. New templates and commands require separate approval.

## Project Resume

Use this section as the handoff point for a new developer or AI session.

| Item | Resume state |
| --- | --- |
| Stable baseline | `v0.6.0` (`Sprint 6 Stable`) |
| Current branch policy | Repository policy treats `master` as protected; use a feature branch for implementation |
| Active development area | Sprint 7.4 configuration-backed create defaults |
| Implemented CLI | `create`, `list`, `version`, `config show/set/reset`, plus no-command interactive create |
| Implemented templates | `basic` only |
| Version source | `config/version.py`, aligned with the `v0.6.0` release tag |
| Verification state | `unittest` covers configuration storage, CLI management, and create-input precedence; use documented checks for the generator lifecycle |

To resume work:

1. Read `AGENTS.md`, this file, `ENGINEERING_PRINCIPLES.md`, `ROADMAP.md`, and `ARCHITECTURE.md`.
2. Run `git status --short`; inspect recent history and tags; preserve all uncommitted work.
3. Re-read the source modules involved in the requested change rather than relying only on this summary.
4. Confirm whether version metadata or other known limitations changed since this document was written.
5. Create a feature branch from `master` for implementation work.
6. Keep the change focused, preserve current CLI compatibility, and satisfy the Definition of Done before review.

Safe read-only resume commands:

```powershell
git status --short --branch
git log -5 --oneline --decorate
git tag --list
python main.py --help
python main.py version
python main.py list
python main.py config --help
```
