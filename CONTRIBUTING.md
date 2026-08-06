# Contributing to ForgePy

Thank you for improving ForgePy. Keep contributions focused on the behavior and architecture present in the repository, and discuss substantial product changes with the maintainers before implementation.

## ForgePy Philosophy

Prefer clear, focused automation; explicit module boundaries; visible side effects; and backward-compatible, evidence-based evolution. Read [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) before changing behavior or architecture.

## Development setup

ForgePy currently uses only the Python standard library and has an empty root `requirements.txt`.

Prerequisites are Git, Python with the standard-library `venv` module, and PowerShell for the commands below. The complete generation workflow currently assumes Windows executables under `.venv\Scripts`. The repository does not yet declare a supported Python version range for ForgePy itself.

The generated `basic` project is separate from ForgePy's empty root requirements file: it declares `PySide6`, `pandas`, and `openpyxl`. A full create run also upgrades packaging tools, so it may require network access.

```powershell
git clone <repository-url>
cd ForgePy
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python main.py --help
```

The implementation and generated VS Code configuration currently assume Windows-style virtual-environment paths.

## Coding style

- Follow PEP 8 and use four-space indentation.
- Add type annotations to public functions and methods.
- Use `pathlib.Path` for file-system paths and UTF-8 for text files.
- Use `snake_case` for modules, functions, methods, and variables; `PascalCase` for classes; and uppercase for constants.
- Order imports as standard library, then project-local modules.
- Keep commands, builders, templates, and orchestration separate.
- Keep builders single-purpose and leave workflow sequencing to `ProjectGenerator`.
- Generate file contents in `templates/`; do not embed large templates in CLI or orchestration modules.
- Preserve the existing console-message prefixes for user-visible status.

## Branching strategy

Repository policy treats `master` as the protected stable branch. Create a short-lived feature branch from it for every ForgePy implementation change. Use a descriptive prefix:

- `feature/` for user-visible additions
- `fix/` for defect corrections
- `docs/` for documentation
- `refactor/` for behavior-preserving restructuring
- `test/` for test-only work

Keep branches limited to one logical change. Synchronize with the default branch before final review, and do not rewrite shared branch history.

Examples include `feature/cli-validation`, `fix/template-lookup`, `docs/project-context`, and `test/basic-template`.

## Commit convention

Use Conventional Commits for changes to the ForgePy repository:

```text
<type>(<optional-scope>): <imperative summary>
```

Supported common types include `feat`, `fix`, `docs`, `refactor`, `test`, `build`, and `chore`. Useful scopes include `cli`, `core`, `builders`, and `templates`.

Examples:

```text
fix(templates): report an unknown template
test(cli): cover default create dispatch
docs: document project architecture
```

Keep the subject concise. Use the body to explain motivation, trade-offs, or migration details when they are not obvious from the diff.

The generator's fixed initial-commit message belongs to newly generated projects and is separate from this contribution convention.

## Testing requirements

The repository does not currently contain an automated test suite or configured test framework. Contributions that change behavior should introduce or update focused automated tests as the test infrastructure is established. At minimum, verify the affected behavior directly and describe the command and result in the pull request.

Relevant coverage includes:

- CLI parsing and dispatch for `create`, `list`, and `version`
- validation of interactive and explicit create inputs
- template registry lookup and listing
- the exact folders and files produced by `BasicTemplate`
- generated text and JSON content
- subprocess success and failure paths without invoking real package installation or Git operations in unit tests
- behavior around missing locations, tools, requirements, and virtual environments

Tests that create files should use an isolated temporary directory and must not write generated projects into the repository. External commands should be mocked in unit tests. Run the full available suite before submitting; if no automated test covers the change, include the manual verification performed.

### Supported manual checks

These read-only commands exercise paths currently supported by the repository:

```powershell
python main.py --help
python main.py version
python main.py list
```

`python main.py` and `python main.py create <name> --location <existing-path> --template basic` are also supported, but they start or perform a side-effectful generation lifecycle. Run them only with deliberate input in an isolated temporary parent directory; creation may build an environment, install packages, and initialize Git.

## Pull request rules

- Open one pull request per logical change.
- Explain the problem, the chosen solution, and any user-visible effect.
- Link the relevant issue or discussion when one exists.
- Include tests for changed behavior and documentation for changed interfaces.
- Update documentation whenever behavior, CLI syntax, generated output, or architectural contracts change.
- Report platform assumptions, external commands, and manual verification.
- Keep generated artifacts, virtual environments, logs, editor state, and secrets out of the diff.
- Avoid unrelated formatting or refactoring.
- Confirm that `git diff` contains only intentional changes.
- Obtain review before merging; do not merge with unresolved review comments or failing checks.
- Require passing tests or clearly documented manual verification before merging.

## Definition of Done

Before requesting review, confirm:

- [ ] The requested scope and acceptance criteria are complete.
- [ ] No unrelated refactor or architectural movement is included.
- [ ] Existing commands, interactive behavior, template names, and generated output remain compatible unless explicitly changed.
- [ ] Tests pass, or supported manual verification commands and results are documented.
- [ ] Relevant behavior and architecture documentation is updated.
- [ ] `git diff --check` passes and `git status --short` shows only intended files.
- [ ] The pull request explains assumptions, compatibility impact, limitations, and verification.

## Code Review Checklist

- [ ] The change is focused and matches the stated problem.
- [ ] CLI, core orchestration, builders, templates, models, and configuration retain clear responsibilities.
- [ ] File-system and subprocess side effects are explicit and have appropriate failure handling.
- [ ] Type hints, `pathlib.Path`, UTF-8 I/O, naming, and imports follow project conventions.
- [ ] Compatibility-sensitive behavior is preserved or accompanied by an approved migration explanation.
- [ ] Tests isolate external commands and temporary files; manual checks are reproducible when tests are unavailable.
- [ ] No secret, generated environment, editor state, or unrelated formatting change is present.

## Documentation Checklist

- [ ] Current, in-progress, planned, and exploratory behavior are not conflated.
- [ ] CLI examples were verified against supported syntax.
- [ ] Directory trees, dependency diagrams, lifecycles, and module descriptions match the code.
- [ ] Stable tags and inconsistent runtime/header versions are distinguished accurately.
- [ ] Platform or Python support claims have evidence.
- [ ] `PROJECT_CONTEXT.md`, `ROADMAP.md`, and `ARCHITECTURE.md` are updated when their facts change.
- [ ] Markdown links, headings, tables, lists, and code fences render correctly on GitHub.

## Adding a template

A new template contribution should implement `BaseTemplate`, keep rendered content separate from file writes, register the template in `TemplateRegistry`, and add coverage for registry listing and generated output. Do not change the existing `basic` template contract incidentally.
