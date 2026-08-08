# ForgePy Project Context

## Project snapshot

- **Name:** ForgePy
- **Purpose:** generate a structured starter Python project from a CLI, then prepare its virtual environment, dependencies, Git repository, and VS Code configuration.
- **Protected stable branch policy:** treat `master` as protected and stable
- **Current stable release/tag:** `v0.6.0` (`Sprint 6 Stable`)
- **Current development area:** Sprint 8.4, modularizing the implemented template architecture without changing generated output.

`config/version.py` is the canonical ForgePy version source and reports `0.6.0`, matching the `v0.6.0` stable release tag. No release tag newer than `v0.6.0` exists.

## ForgePy Philosophy

ForgePy favors understandable automation, explicit architectural boundaries, compatibility-conscious evolution, and generated projects that remain easy for their owners to inspect. See [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) for the project-wide design and review policy.

## Implemented capabilities

- Parse and dispatch `create`, `list`, `version`, and `config` commands through one shared catalog.
- Fall back to an interactive create workflow when no command is supplied.
- Register the `basic`, `library`, and `cli` project templates through one validated registration path with immutable metadata.
- Generate all three built-in file templates through a shared execution layer that keeps registry metadata, project/package context, file mappings, and VS Code entry-point resolution distinct.
- List registered template names and descriptions without invoking project generation.
- Generate a minimal library layout with a normalized import-package directory, `tests/`, empty package initializers, shared README/Git-ignore/pyproject content, and an empty requirements file.
- Generate a minimal command-line package with `__main__.py`, an argparse interface, empty requirements, and executable module, help, version, and editor entry points.
- The `basic` template generates the configured folder layout and nine root files.
- Create `.venv`, upgrade `pip`, `setuptools`, and `wheel`, and install generated requirements.
- Initialize Git, stage generated content, and attempt an initial commit.
- Generate four VS Code files matched to the selected template: `basic` targets `app.py`, `library` declares no application entry point, and `cli` targets its generated package `cli.py`.
- Load, validate, update, reset, and atomically save user configuration at `~/.forgepy/config.json` through `ConfigStore`.
- Show, set, and reset persistent values through `python main.py config` without duplicating storage logic in the CLI.
- Resolve omitted create location and template values from `default_location` and `default_template`, after explicit CLI arguments and before the existing prompt/`basic` fallback.
- Test configuration behavior, create-input precedence, metadata and registration, all built-in entries, list output, generated structures and execution, and template-aware VS Code output with `unittest`.

`ConfigCommand` manages all persisted values. `CreateCommand` consumes only `default_location` and `default_template`; `author` and `license` remain unused. `ProjectGenerator` does not depend on `ConfigStore`. Its shared lifecycle is unchanged. `FileTemplate` now performs the repeated template-local folder/file execution while each built-in retains its established layout, content, and editor requirement.

## Repository structure

| Path | Current role |
| --- | --- |
| `builders/` | Folder/file creation and packaging-tool updates. |
| `cli/` | Parser, dispatcher, command contract, and commands. |
| `config/` | Version metadata, generated folder defaults, and user-level JSON configuration. |
| `core/` | Project lifecycle and environment, Git, requirements, and VS Code services. |
| `models/` | `ProjectConfig` data model. |
| `templates/` | Basic, library, and CLI definitions; shared context/execution contracts; immutable metadata; template-owned file mappings; template-specific VS Code entry-point rules; registry; rendered content; and VS Code JSON. |
| `utils/` | Present but currently contains no implemented utility behavior. |
| `tests/` | Standard-library tests for configuration, create resolution, metadata/registry behavior, list output, template architecture and output snapshots, built-in structures, and VS Code compatibility. |
| `main.py` | Executable application entry point. |

The root `README.md`, `requirements.txt`, and `config.py` are currently empty.

## Technical constraints

- Full generation is Windows-oriented: environment tools are addressed under `.venv/Scripts` with `.exe` filenames.
- ForgePy itself has no declared third-party runtime dependencies. Automated coverage includes configuration, create-input resolution, metadata/registry behavior, list output, the shared template contract, exact normalized output snapshots, all built-in structures, generated CLI execution, and isolated template-aware VS Code generation through `ProjectGenerator`. The generated `basic` project requires `PySide6`, `pandas`, and `openpyxl`; `library` and `cli` have empty requirements files. The full lifecycle still upgrades packaging tools and may require network access.
- Template lookup uses direct dictionary indexing; an unknown template is not converted into a friendly CLI error.
- Template metadata versioning has no release policy yet. The `basic` metadata records `0.6.0`, while `library` and `cli` start at `0.1.0`; these are independent from the ForgePy application and generated-project versions.
- Subprocess failures generally propagate because commands use `check=True`.
- Generation uses `exist_ok=True`, so an existing target can be written into rather than rejected.
- The generated `pyproject.toml` requires Python `>=3.12`, but the ForgePy repository itself does not declare a supported Python range.
- `config.default_structure.DEFAULT_FILES` is defined but unused. `BasicFiles`, `LibraryFiles`, and `CliFiles` own their complete mappings and call `TemplateManager` directly for rendered content; `TemplateFiles.basic()` remains a compatibility facade.

## Near-term priorities

- Finish and verify the Sprint 8.4 template-architecture refactor without changing established output or the shared project lifecycle.
- Keep further templates beyond `basic`, `library`, and `cli` subject to separate approval and compatibility review.
- Keep persisted `author` and `license` values, and the configuration store itself, out of core generation and templates until a separate requirement explicitly defines that integration.
- Continue expanding automated coverage across supported commands, lifecycle stages, and failure handling.
- Document platform and Python support based on verified behavior.

## Long-term v1.0 direction

The repository does not define guaranteed v1.0 features. A realistic direction is a stable, documented CLI and template contract; predictable project-generation behavior; consistent versioning; and automated verification of the existing lifecycle. New templates and commands require separate approval.

## Project Resume

Use this section as the handoff point for a new developer or AI session.

| Item | Resume state |
| --- | --- |
| Stable baseline | `v0.6.0` (`Sprint 6 Stable`) |
| Current branch policy | Repository policy treats `master` as protected; use a feature branch for implementation |
| Active development area | Sprint 8.4 modular template architecture |
| Implemented CLI | `create`, `list`, `version`, `config show/set/reset`, plus no-command interactive create |
| Implemented templates | `basic`, `library`, and `cli`, all with descriptive metadata |
| Version source | `config/version.py`, aligned with the `v0.6.0` release tag |
| Verification state | `unittest` covers configuration, create precedence, metadata/registry behavior, list output, template architecture and output snapshots, all structures, CLI execution, and isolated template-aware VS Code generation; the real external lifecycle remains a manual check |

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
