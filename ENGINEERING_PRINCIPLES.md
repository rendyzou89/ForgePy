# ForgePy Engineering Principles

This document defines how ForgePy should evolve. It describes engineering expectations, not additional implemented features. Repository behavior remains authoritative when documentation and code disagree.

## ForgePy Philosophy

ForgePy should make project setup repeatable without hiding the work it performs. A generated project should begin from useful, understandable defaults and remain ordinary Python code that its owner can inspect and change.

The project favors:

- **Clarity over cleverness:** prefer direct control flow and explicit registrations.
- **Focused automation:** automate a complete, visible setup sequence without turning ForgePy into a general build system.
- **Safe evolution:** improve one boundary at a time and preserve established CLI and template behavior.
- **Evidence over aspiration:** document implemented behavior as current and label proposals as planned or exploratory.
- **Ownership after generation:** generated files belong to the user; changes to generated output must be deliberate and reviewable.

## Design Principles

### Keep boundaries explicit

- `cli/` owns parsing, command selection, and command-level validation.
- `core/ProjectGenerator` owns project-generation sequencing.
- Builders and core tooling services own focused side effects.
- `components/` owns the independent component-definition, declarative manifest, and installation contracts, validated project context, built-in definitions, and in-memory registry.
- `templates/` owns registration metadata, per-generation context, rendered file definitions, and template-specific VS Code entry-point decisions.
- `models/` carries project data; `config/` owns application metadata, generated-layout defaults, and isolated user-configuration persistence.

Dependencies should follow those boundaries. Templates and builders must not depend back on the CLI.

### Separate decisions, content, and side effects

Template selection belongs to `TemplateRegistry`; `TemplateMetadata` describes registrations; `TemplateContext` carries project/package data; template-local mappings define content; and each built-in resolves an explicit VS Code entry point from a static default or generation context. Common `FileTemplate` execution delegates disk writes to focused builders. `ProjectGenerator` may forward explicit requirements while remaining orchestration-only. CLI prompting must not leak into builders or templates.

`ComponentRegistry` catalogs component definitions only. Registration validates contract types, component/metadata identity, and self-references but does not resolve manifest dependencies or conflicts. Registration and lookup do not invoke component installation, install packages, select templates, modify generated files, or trigger other side effects. A component installation receives only a validated context naming an existing project directory.

### Prefer small contracts

Extend commands through the shared `Command` metadata and integer-status `execute()` contract, override `configure_parser()` when arguments are required, and add built-in commands to the explicit catalog in `cli.commands`. Preserve the public `BaseTemplate` contract; built-in file templates use the focused `FileTemplate` hooks for context, folders, files, and VS Code entry-point resolution. Keep descriptive metadata in the template registry rather than builders or rendered content. Keep inputs explicit, use type hints, and pass `pathlib.Path` objects at file-system boundaries.

Extend the component catalog through `BaseComponent`, `ComponentMetadata`, `ComponentManifest`, `ComponentContext`, and explicit `ComponentRegistry.register()` calls; keep the default catalog limited to explicitly approved built-ins and keep relationship resolution and installation outside the registry.

### Preserve compatibility intentionally

The no-command interactive create flow, the `create`, `list`, `version`, and `config show/set/reset` commands, the `basic`, `library`, and `cli` template names and metadata selectors, and their established generated layouts are compatibility-sensitive. Create defaults resolve in the order explicit CLI value, persisted user setting, then the existing prompt or `basic` fallback. Change these contracts only through an explicit requirement with tests or documented migration verification.

### Make side effects visible

Environment creation, package installation, Git initialization, VS Code generation, and persistent configuration writes are observable side effects. New side effects must have clear ownership, failure behavior, and user-facing status.

### Keep portability claims evidence-based

The current implementation uses Windows virtual-environment executable paths. Do not claim broader platform support until paths and lifecycle behavior have been implemented and verified there.

### Prefer incremental change

Avoid speculative abstractions, unrelated cleanup, and large refactors. Add a new layer only when an implemented requirement needs it and the dependency direction remains clear.

## Definition of Done

A change is done only when all applicable items are true:

- [ ] The requested behavior and acceptance criteria are satisfied.
- [ ] The change stays within the established architectural boundaries, or an approved architectural change is documented.
- [ ] Existing CLI behavior, template names, and generated output remain compatible unless the change explicitly revises them.
- [ ] Python changes follow PEP 8, use appropriate type hints, `pathlib.Path`, and explicit UTF-8 text I/O.
- [ ] Tests cover the change, or supported manual verification is documented where no automated test infrastructure exists.
- [ ] Side effects and failure paths have been considered and verified in proportion to risk.
- [ ] User-facing behavior and architectural documentation are updated when affected.
- [ ] `git diff --check` passes and the final diff contains no unrelated changes, generated artifacts, or secrets.
- [ ] The pull request explains assumptions, verification results, compatibility impact, and known limitations.

## Code Review Checklist

Reviewers should confirm:

- [ ] The change solves the stated problem without expanding scope unnecessarily.
- [ ] CLI parsing, orchestration, builders, components, templates, configuration, and models retain clear responsibilities.
- [ ] Dependency flow remains inward and no avoidable circular dependency is introduced.
- [ ] External commands and file writes have explicit paths, predictable failures, and appropriate user feedback.
- [ ] Unknown, empty, existing-path, and missing-tool cases are considered where relevant.
- [ ] Compatibility-sensitive behavior is preserved or intentionally documented.
- [ ] Tests are focused and isolate file-system and subprocess effects; otherwise manual evidence is adequate and reproducible.
- [ ] Names, types, imports, encoding, and formatting follow repository conventions.
- [ ] The diff contains no unrelated refactor, sensitive value, or generated environment artifact.

## Documentation Checklist

When behavior or structure changes, confirm:

- [ ] Current behavior and planned behavior are clearly distinguished.
- [ ] CLI commands and examples use syntax the repository actually supports.
- [ ] Architecture diagrams, directory trees, lifecycle steps, and module responsibilities match the code.
- [ ] ForgePy version statements match `config/version.py` and the current release tag; template-metadata, generated-project, and schema versions are clearly distinguished.
- [ ] Platform and Python support claims are backed by repository configuration or verification.
- [ ] `PROJECT_CONTEXT.md` and `ROADMAP.md` reflect material changes to current work or priorities.
- [ ] `CONTRIBUTING.md` reflects any new setup, test, or review requirement.
- [ ] Links, headings, code fences, and lists render correctly in GitHub Markdown.

## Decision Rule

When principles conflict, protect user data and repository history first, preserve current behavior second, maintain architectural clarity third, and optimize convenience only after those concerns are satisfied. Stop and request direction when the product choice remains ambiguous.
