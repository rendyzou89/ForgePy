# ForgePy Project Context

## Project snapshot

- **Name:** ForgePy
- **Purpose:** generate a structured starter Python project from a CLI, then prepare its virtual environment, dependencies, Git repository, and VS Code configuration.
- **Protected stable branch policy:** treat `master` as protected and stable
- **Current stable release/tag:** `v0.6.0` (`Sprint 6 Stable`)
- **Current development area:** Sprint 10.0, adding minimal GitHub Actions CI through the existing component architecture.

`config/version.py` is the canonical ForgePy version source and reports `0.6.0`, matching the `v0.6.0` stable release tag. No release tag newer than `v0.6.0` exists.

## ForgePy Philosophy

ForgePy favors understandable automation, explicit architectural boundaries, compatibility-conscious evolution, and generated projects that remain easy for their owners to inspect. See [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) for the project-wide design and review policy.

## Implemented capabilities

- Parse and dispatch `create`, `list`, `version`, and `config` commands through one shared catalog.
- Fall back to an interactive create workflow when no command is supplied.
- Register the `basic`, `library`, and `cli` project templates through one validated registration path with immutable metadata.
- Define immutable component metadata and manifest values, a validated existing-project context, an abstract identity/metadata/manifest/install contract, and an in-memory registry with deterministic built-in registration, explicit registration, lookup, and ordered listing.
- Provide built-in `pytest`, `ruff`, and `github-actions` components that exclusively create their declared standalone files in an explicitly supplied existing project.
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
- Validate project names as one generated-content-safe Windows destination segment, require a new resolved destination directly below the selected location, and reject existing destination files, directories, symlinks, or junctions before generation writes.
- Confine component-state reads, atomic writes, and same-directory temporary files to the resolved project root so `.forgepy` or `components.json` redirection cannot escape the project.
- Test configuration behavior, create-input precedence, destination safety, metadata and registration, all built-in entries, list output, generated structures and execution, and template-aware VS Code output with `unittest`.

The component foundation is exposed by the component CLI but remains independent from configuration, templates, builders, `ProjectGenerator`, and generated-project creation. Its `pytest`, `ruff`, and `github-actions` built-ins exclusively create their declared `pytest.ini`, `ruff.toml`, and `.github/workflows/ci.yml` files inside a validated existing project and reject existing targets. Installation uses the shared orchestrator; registry lookup still does not resolve manifest relationships.

`ConfigCommand` manages all persisted values. `CreateCommand` consumes only `default_location` and `default_template`; `author` and `license` remain unused. `ProjectGenerator` does not depend on `ConfigStore`. Before its established template and tooling stages, it requires a validated one-segment name and a nonexistent direct-child destination. `FileTemplate` performs the repeated template-local folder/file execution while each built-in retains its established layout, content, and editor requirement.

## Repository structure

| Path | Current role |
| --- | --- |
| `builders/` | Folder/file creation and packaging-tool updates. |
| `cli/` | Parser, dispatcher, command contract, and commands. |
| `components/` | Immutable component metadata and manifest, validated project context, minimal installation/state/validation contracts, the `pytest`, `ruff`, and `github-actions` built-ins, and an in-memory registry. |
| `config/` | Version metadata, generated folder defaults, and user-level JSON configuration. |
| `core/` | Project lifecycle and environment, Git, requirements, and VS Code services. |
| `models/` | `ProjectConfig` data model. |
| `templates/` | Basic, library, and CLI definitions; shared context/execution contracts; immutable metadata; template-owned file mappings; template-specific VS Code entry-point rules; registry; rendered content; and VS Code JSON. |
| `utils/` | Present but currently contains no implemented utility behavior. |
| `tests/` | Standard-library tests for component and template metadata/registries, configuration, create resolution, list output, template architecture and output snapshots, built-in structures, and VS Code compatibility. |
| `main.py` | Executable application entry point. |

The root `README.md`, `requirements.txt`, and `config.py` are currently empty.

## Technical constraints

- Full generation is Windows-oriented: environment tools are addressed under `.venv/Scripts` with `.exe` filenames.
- ForgePy itself has no declared third-party runtime dependencies. Automated coverage includes configuration, create-input resolution, metadata/registry behavior, list output, the shared template contract, exact normalized output snapshots, all built-in structures, generated CLI execution, and isolated template-aware VS Code generation through `ProjectGenerator`. The generated `basic` project requires `PySide6`, `pandas`, and `openpyxl`; `library` and `cli` have empty requirements files. The full lifecycle still upgrades packaging tools and may require network access.
- Template lookup uses direct dictionary indexing and retains `KeyError` for an unknown name, but now occurs after destination validation and before project-root creation so rejection leaves no generation artifact.
- Template metadata versioning has no release policy yet. The `basic` metadata records `0.6.0`, while `library` and `cli` start at `0.1.0`; these are independent from the ForgePy application and generated-project versions.
- Subprocess failures generally propagate because commands use `check=True`.
- Project generation rejects names that are unsafe for current generated Python/TOML strings or the supported Windows filename contract, including leading ASCII spaces and ordinary or superscript-digit reserved device stems, as well as existing targets, before template lookup or root creation. Accepted display names are preserved, while library and CLI package names remain separately normalized. Package-oriented generation can still reject a display name with no usable ASCII package identifier after root creation; preflighting that template-specific constraint and friendly CLI translation remain separate work.
- The generated `pyproject.toml` requires Python `>=3.12`, but the ForgePy repository itself does not declare a supported Python range.
- `ComponentRegistry` is in-memory, installation-state-agnostic, and resolution-agnostic; it registers `pytest`, `ruff`, then `github-actions` by default. `ComponentInstaller` coordinates explicit project context, state, direct validation, one hook, and post-success state recording without moving those responsibilities. `component add` delegates to that installer, while `component installed --project PATH` reads the project-local store without registry filtering or filesystem inference. The component system provides no discovery, transitive resolution, installation ordering, rollback, uninstall, local package installation, template association, or generation integration.
- `config.default_structure.DEFAULT_FILES` is defined but unused. `BasicFiles`, `LibraryFiles`, and `CliFiles` own their complete mappings and call `TemplateManager` directly for rendered content; `TemplateFiles.basic()` remains a compatibility facade.

## Near-term priorities

- Keep the Sprint 10.0 GitHub Actions component within the existing catalog and CLI flows without adding rollback or resolution.
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
| Active development area | Sprint 10.0 third built-in component |
| Implemented CLI | `create`, `list`, `version`, `config show/set/reset`, `component list/installed/add`, plus no-command interactive create |
| Implemented templates | `basic`, `library`, and `cli`, all with descriptive metadata |
| Component state | Registry with `pytest`, `ruff`, and `github-actions` built-ins, project-local installed names, direct validation, and shared library/CLI orchestration; no generation integration |
| Version source | `config/version.py`, aligned with the `v0.6.0` release tag |
| Verification state | `unittest` covers component orchestration, state, validation, component and template metadata/registries, configuration, create precedence, list output, template architecture and output snapshots, CLI execution, and isolated template-aware VS Code generation; the real external lifecycle remains a manual check |

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
