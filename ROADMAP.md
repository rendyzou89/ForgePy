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

## In Progress — Sprint 7 CLI

Two commits after `v0.6.0` establish the current development area on `master`; no newer release tag exists.

| Area | Current implementation |
| --- | --- |
| Command model | Abstract `Command` contract with dispatcher registration. |
| Commands | `create`, `list`, and `version`. |
| Invocation | Argument-based creation and interactive prompting. |
| Compatibility | No subcommand continues to open the create workflow. |

Sprint 7 completion should be based on verified CLI behavior and consistent documentation; this document does not assign an unrecorded release number.

## Planned — Stabilization Toward v1.0

These are outcome-oriented priorities, not guaranteed feature commitments.

### Repository Consistency

- Establish one authoritative version source and reconcile the `v0.6.0` tag, `0.4.0` runtime value, `v0.6.4` builder headers, and `v0.7.2` CLI headers.
- Populate or intentionally resolve the empty root README and project metadata.

### Verification and Failure Behavior

- Establish automated coverage for CLI routing, template output, builders, and subprocess boundaries.
- Define predictable validation for unknown templates, missing tools, failed subprocesses, and existing target paths.
- Retain documented manual checks until automated infrastructure covers them.

### Compatibility and Support

- Document supported Python and operating-system ranges based on verified behavior.
- Stabilize the CLI contract, `basic` template name and output, and project-generation lifecycle.
- Provide migration notes for any intentionally incompatible pre-1.0 change.

### v1.0 Readiness Gate

ForgePy is ready for a v1.0 proposal when the current public behavior is consistently versioned, documented, tested, and supported with predictable failures. Passing this gate does not imply additional templates or commands.

## Ideas — Not Scheduled

- Evaluate portability beyond the current Windows-oriented virtual-environment paths.
- Evaluate additional commands or templates only after a concrete use case and compatibility review.

Ideas become planned work only after maintainer approval, defined acceptance criteria, and an identified verification approach.
