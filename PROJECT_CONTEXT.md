# ForgePy Project Context

## Project snapshot

- **Name:** ForgePy
- **Purpose:** generate a structured starter Python project from a CLI, then prepare its virtual environment, dependencies, Git repository, and VS Code configuration.
- **Protected stable branch policy:** treat `master` as protected and stable
- **Current stable release/tag:** `v0.6.0` (`Sprint 6 Stable`)
- **Current development area:** Sprint 7 CLI, represented by the CLI architecture and interactive-create commits after `v0.6.0`.

The stable tag and runtime metadata are not aligned: `config/version.py` reports `0.4.0`, builder headers include `v0.6.4`, and CLI source headers say `v0.7.2`. Other core and template headers still include `v0.4.0`. No release tag newer than `v0.6.0` exists.

## ForgePy Philosophy

ForgePy favors understandable automation, explicit architectural boundaries, compatibility-conscious evolution, and generated projects that remain easy for their owners to inspect. See [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) for the project-wide design and review policy.

## Implemented capabilities

- Parse and dispatch `create`, `list`, and `version` commands.
- Fall back to an interactive create workflow when no command is supplied.
- Register and list the single `basic` project template.
- Generate the configured folder layout and nine root files.
- Create `.venv`, upgrade `pip`, `setuptools`, and `wheel`, and install generated requirements.
- Initialize Git, stage generated content, and attempt an initial commit.
- Generate four VS Code configuration files.

## Repository structure

| Path | Current role |
| --- | --- |
| `builders/` | Folder/file creation and packaging-tool updates. |
| `cli/` | Parser, dispatcher, command contract, and commands. |
| `config/` | Version metadata and generated folder defaults. |
| `core/` | Project lifecycle and environment, Git, requirements, and VS Code services. |
| `models/` | `ProjectConfig` data model. |
| `templates/` | Basic template, registry, file mapping, rendered content, and VS Code JSON. |
| `utils/` | Present but currently contains no implemented utility behavior. |
| `main.py` | Executable application entry point. |

The root `README.md`, `requirements.txt`, and `config.py` are currently empty.

## Technical constraints

- Full generation is Windows-oriented: environment tools are addressed under `.venv/Scripts` with `.exe` filenames.
- ForgePy itself has no declared third-party runtime dependencies and no automated test suite. The generated `basic` project requires `PySide6`, `pandas`, and `openpyxl`, so the full create lifecycle attempts package installation and may require network access.
- Template lookup uses direct dictionary indexing; an unknown template is not converted into a friendly CLI error.
- Subprocess failures generally propagate because commands use `check=True`.
- Generation uses `exist_ok=True`, so an existing target can be written into rather than rejected.
- Generated template metadata requires Python `>=3.12`, but the ForgePy repository itself does not declare a supported Python range.
- `config.default_structure.DEFAULT_FILES` is defined but is not used by the current template workflow; `TemplateFiles.basic()` determines generated root files.

## Near-term priorities

- Finish and verify Sprint 7 CLI behavior without breaking interactive creation.
- Align version sources and release documentation.
- Establish tests for supported commands, template output, and failure handling.
- Document platform and Python support based on verified behavior.

## Long-term v1.0 direction

The repository does not define guaranteed v1.0 features. A realistic direction is a stable, documented CLI and template contract; predictable project-generation behavior; consistent versioning; and automated verification of the existing lifecycle. New templates and commands require separate approval.

## Project Resume

Use this section as the handoff point for a new developer or AI session.

| Item | Resume state |
| --- | --- |
| Stable baseline | `v0.6.0` (`Sprint 6 Stable`) |
| Current branch policy | Repository policy treats `master` as protected; use a feature branch for implementation |
| Active development area | Sprint 7 CLI |
| Implemented CLI | `create`, `list`, `version`, plus no-command interactive create |
| Implemented templates | `basic` only |
| Primary uncertainty | Conflicting tag, runtime, and source-header versions |
| Verification state | No automated test suite is configured; use supported manual checks |

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
```
