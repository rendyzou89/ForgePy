# ForgePy Roadmap

This roadmap separates shipped work, active development, planned stabilization, and uncommitted ideas. It defines no guaranteed dates or features.

## Status Model

| Status | Meaning |
| --- | --- |
| Implemented | Confirmed by code and repository history. |
| In progress | Present after the stable tag and identified as the current development area. |
| Planned | A high-level readiness outcome inferred from documented gaps; scope still requires approval. |
| Idea | Exploratory only; not approved or scheduled. |

## Implemented — Stable Baseline Through v0.6.0

The latest stable tag is `v0.6.0` (`Sprint 6 Stable`).

### Milestone Evidence

| Repository point | Evidence |
| --- | --- |
| Modular generator foundation | Commit `0697387` has the subject `v0.2.5 - Modular project generator with template system`; `v0.2.5` is not present as a Git tag. |
| Stable Sprint 6 baseline | Tag `v0.6.0` points to commit `78c9924`, `Sprint 6 Stable`. |

| Milestone | Confirmed outcome |
| --- | --- |
| Project-generation foundation | `ProjectConfig` and `ProjectGenerator` create and coordinate a starter project. |
| Builder separation | Folder, file, and packaging-tool operations have focused builders. |
| Template system | `BaseTemplate`, `TemplateRegistry`, `TemplateFiles`, and the `basic` template are implemented. |
| Environment tooling | ForgePy creates `.venv`, upgrades packaging tools, and installs non-empty generated requirements. |
| Repository setup | ForgePy initializes Git, stages content, and attempts an initial commit. |
| Editor setup | ForgePy generates VS Code settings, launch, tasks, and extension recommendations. |

## Implemented — Sprint 7 CLI and User Configuration

The Sprint 7 CLI architecture, persistent configuration, its CLI command, and configuration-backed create defaults are present on `master` in commits after `v0.6.0`. No newer release tag exists.

| Area | Current implementation |
| --- | --- |
| Command model | Shared `Command` contract and one explicit command catalog used by parsing and dispatch. |
| Commands | `create`, `list`, `version`, and `config` with `show`, `set`, and `reset` actions. |
| Invocation | Creation resolves explicit arguments, persisted location/template defaults, and existing prompt/`basic` fallbacks in that order. |
| Compatibility | No subcommand continues to open the create workflow. |
| Version reporting | `config/version.py` is the canonical source and matches the `v0.6.0` release tag. |
| User configuration | `ConfigCommand` manages all four settings; `CreateCommand` consumes only `default_location` and `default_template`, while `author` and `license` remain unused. |

Sprint 7 behavior is covered by focused configuration and create-resolution tests; this document does not assign an unrecorded release number.

## Implemented — Sprint 8.1 Template Metadata

Sprint 8.1 introduced descriptive metadata as the registry and listing foundation for future templates. Commit `484278a` records the implementation, and merge commit `41de327` incorporates it into `master`; no newer release tag was created.

| Area | Sprint 8.1 outcome |
| --- | --- |
| Metadata model | Immutable `TemplateMetadata` values contain name, description, template version, author, and tags. |
| Registration | `TemplateRegistry.register()` validates template and metadata types, non-empty matching names, and uniqueness before preserving a registration. |
| Listing | `list` reads registry metadata and displays each template name and description. |
| Compatibility | That milestone added no template: `basic` remained the only template, its selector stayed stable, and its generated output was unchanged. |

Sprint 8.1 includes focused metadata, registry, and list-output tests plus the existing CLI regression suite.

## Implemented — Sprint 8.2 Library Template

Sprint 8.2 added the first additional built-in template without changing the shared generator lifecycle. Merge commit `72b8359` incorporates the work into `master`; no newer release tag was created.

| Area | Sprint 8.2 outcome |
| --- | --- |
| Built-in catalog | `TemplateRegistry` registers `basic` first and `library` second through the existing validated API. |
| Library metadata | `library` has its own name, description, template revision, author, and tags. |
| Generated layout | A normalized import-package directory and `tests/` each contain `__init__.py`, alongside a minimal set of shared root files. |
| Editor compatibility | Built-in templates explicitly declare an `app.py` entry point or no entry point; library VS Code JSON no longer references an absent application file. |
| Compatibility | The `basic` selector, metadata, generated folders/files, default selection, and existing VS Code behavior remain unchanged. |
| Verification | Focused tests cover registration, metadata, exact structures, package-name normalization, generator selection, and template-aware VS Code output. |

Sprint 8.2 introduced no further template types, release number, or delivery date.

## Implemented — Sprint 8.3 CLI Template

Sprint 8.3 added a minimal standard-library command-line application template on the existing registry and editor-configuration contracts. Merge commit `f9ae27c` incorporates the work into `master`; no newer release tag was created.

| Area | Sprint 8.3 outcome |
| --- | --- |
| Built-in catalog | `TemplateRegistry` registers `cli` after the established `basic` and `library` templates. |
| CLI metadata | `cli` has a factual description, independent template revision, author, and Python/CLI/argparse tags. |
| Generated layout | A normalized package contains `__init__.py`, `__main__.py`, and `cli.py`; `tests/` has an initializer and shared root files remain minimal. |
| Runtime behavior | The generated package runs with `python -m`, and argparse provides help and version output without third-party dependencies. |
| Editor compatibility | The template publishes its generated `cli.py` path so VS Code launch and run tasks reference a real executable file. |
| Compatibility | The existing templates, default selection, CLI/configuration architecture, builders, and generator lifecycle remain unchanged. |
| Verification | Focused tests cover registration, metadata, exact output, normalization, subprocess execution, editor JSON, and existing-template regressions. |

Sprint 8.3 introduced no additional ForgePy command, release number, or delivery date.

## In Progress — Sprint 8.4 Template Architecture

Sprint 8.4 separates the implemented templates' metadata, generation context, file mappings, and context-aware VS Code entry-point resolution without adding another template or changing generated output.

| Area | Current implementation |
| --- | --- |
| Shared execution | `FileTemplate` owns the repeated folder creation, ordered file-writing loop, and post-write VS Code entry-point resolution for all three built-ins. |
| Generation data | Immutable `TemplateContext` keeps project and optional normalized package data separate from registry metadata. |
| File ownership | `BasicFiles`, `LibraryFiles`, and `CliFiles` own complete mappings and call `TemplateManager` directly for the root content they share. |
| VS Code entry points | Per-template defaults and the CLI context hook preserve the existing `vscode_entry_point` compatibility property. |
| Compatibility | Registry APIs, CLI/configuration behavior, generator sequencing, builders, generated files, and VS Code output remain unchanged. |
| Verification | Independent snapshots cover every template-owned file; dedicated VS Code tests cover the four editor files and entry-point behavior for each built-in. |

Sprint 8.4 introduces no new template, command, ForgePy version, or delivery date.

## Planned — Stabilization Toward v1.0

These are outcome-oriented priorities, not guaranteed feature commitments.

### Repository Consistency

- Keep the canonical application version synchronized with release tags without duplicating it in module headers.
- Populate or intentionally resolve the empty root README and project metadata.

### Verification and Failure Behavior

- Continue expanding automated coverage across builders, the full generator lifecycle, and subprocess failure boundaries.
- Define predictable validation for unknown templates, missing tools, failed subprocesses, and existing target paths.
- Retain documented manual checks until automated infrastructure covers them.

### Compatibility and Support

- Document supported Python and operating-system ranges based on verified behavior.
- Stabilize the CLI contract, all three built-in template names and outputs, and the project-generation lifecycle.
- Define a template-metadata version policy before independently evolving template revisions.
- Provide migration notes for any intentionally incompatible pre-1.0 change.

### v1.0 Readiness Gate

ForgePy is ready for a v1.0 proposal when the current public behavior is consistently versioned, documented, tested, and supported with predictable failures. Passing this gate does not imply additional templates or commands.

## Ideas — Not Scheduled

- Evaluate portability beyond the current Windows-oriented virtual-environment paths.
- Evaluate further commands or templates beyond `basic`, `library`, and `cli` only after a concrete use case and compatibility review.

Ideas become planned work only after maintainer approval, defined acceptance criteria, and an identified verification approach.
