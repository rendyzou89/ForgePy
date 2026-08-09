# ForgePy Architecture

## Overview

ForgePy is a layered command-line application. The CLI parses user input and selects a command, the create command delegates to `ProjectGenerator`, and the generator coordinates template rendering and setup services. The template registry keeps descriptive metadata alongside executable templates so listing does not invoke generation. Built-in templates separate per-generation context, template-owned file mappings, and explicit VS Code entry-point rules; their common execution layer delegates folder and file writes to the existing builders. An independent component package provides metadata, a declarative installation manifest, a validated existing-project context, minimal installation hooks, the `pytest`, `ruff`, and `github-actions` built-ins, and an in-memory registry. The component CLI lists that catalog, reads project-local installed state, and delegates explicit installation to `ComponentInstaller` without entering the generation flow.

## Directory structure

```text
ForgePy/
|-- builders/                 Reusable file-system and Python-tool builders
|-- cli/                      Argument parsing, dispatch, and command objects
|   `-- commands/             Implementations and the shared command catalog
|-- components/               Independent component contracts and registry
|   |-- base_component.py     Abstract identity/metadata/manifest/install contract
|   |-- component_context.py  Validated existing-project context
|   |-- component_installer.py Fixed single-component installation flow
|   |-- component_manifest.py Immutable declarative installation properties
|   |-- component_metadata.py Immutable descriptive component metadata
|   |-- component_registry.py In-memory built-in and explicit registration
|   |-- component_state.py    Project-local installed-name persistence
|   |-- component_validation.py Stateless direct relationship validation
|   |-- github_actions_component.py Built-in GitHub Actions CI workflow
|   |-- pytest_component.py    Built-in isolated pytest configuration
|   `-- ruff_component.py      Built-in isolated Ruff configuration
|-- config/                   Application and user configuration
|   |-- default_structure.py  Generated project layout defaults
|   |-- user_config.py        Persistent user configuration store
|   `-- version.py            Canonical ForgePy version metadata
|-- core/                     Project workflow and environment/tool integrations
|-- models/                   Project configuration data model
|-- templates/                Generated file content and template facade
|   |-- basic/                Basic template and its generated-file mapping
|   |-- cli/                  Minimal command-line application template
|   |-- library/              Minimal Python library template implementation
|   |-- template_engine/      Contracts for execution, context, metadata, registry, naming, and compatibility
|   `-- vscode/               VS Code JSON content generators
|-- utils/                    Reserved utility package; logger is currently empty
|-- main.py                   Application entry point
|-- config.py                 Empty root module
|-- README.md                 Project README; currently empty
|-- AGENTS.md                 Working rules for human and AI agents
|-- ARCHITECTURE.md           Current structure and dependency flows
|-- CONTRIBUTING.md           Contribution and review workflow
|-- ENGINEERING_PRINCIPLES.md Engineering policy and completion criteria
|-- PROJECT_CONTEXT.md        Current development and handoff context
|-- ROADMAP.md                Implemented, active, planned, and idea states
|-- tests/                    Standard-library automated tests
`-- requirements.txt          Runtime dependency file; currently empty
```

## Module responsibilities

| Area | Responsibility |
| --- | --- |
| `main.py` | Connects `Parser` to `Dispatcher`. |
| `cli/parser.py` | Defines CLI syntax, defaults, and subcommands. |
| `cli/command.py` | Defines command metadata, parser configuration, and execution contracts. |
| `cli/commands/__init__.py` | Registers the built-in commands in one explicit catalog. |
| `cli/commands/create_command.py` | Resolves project name, location, and template inputs before invoking project generation. |
| `cli/commands/config_command.py` | Adapts configuration actions, output, and ForgePy configuration errors for the CLI. |
| `cli/commands/component_command.py` | Lists registered components, presents project-local installed state, delegates add operations to `ComponentInstaller`, and adapts operational errors for the CLI. |
| `cli/dispatcher.py` | Builds command lookup from the shared catalog; defaults to `create`. |
| `cli/commands/` | Validates command-level input and invokes application services. |
| `models/project_config.py` | Validates the one-segment project name, stores the selected location, and derives the root path. |
| `core/project_generator.py` | Orchestrates the complete create workflow. |
| `core/environment_builder.py` | Creates `.venv` with the running Python interpreter. |
| `core/requirements_installer.py` | Installs the generated requirements with the new environment's `pip.exe`. |
| `core/git_builder.py` | Initializes Git, stages files, and attempts the initial commit. |
| `core/vscode_builder.py` | Renders and writes `.vscode` files for an explicit template entry-point requirement. |
| `builders/` | Creates folders/files and upgrades Python packaging tools. |
| `components/base_component.py` | Defines abstract component `name`, `metadata`, `manifest`, and minimal `install(context)` behavior. |
| `components/component_context.py` | Validates the existing project directory supplied explicitly to installation. |
| `components/component_installer.py` | Coordinates lookup, context, installed state, direct validation, one installation hook, and post-success state recording. |
| `components/component_manifest.py` | Defines immutable owned-file, dependency, and conflict declarations without resolution behavior. |
| `components/component_metadata.py` | Defines immutable descriptive metadata for component definitions. |
| `components/component_registry.py` | Registers the built-in catalog deterministically, validates explicit in-memory registrations, and provides lookup and immutable ordered listing. |
| `components/component_state.py` | Safely persists deterministic installed component names under an explicitly supplied existing project. |
| `components/component_validation.py` | Validates direct manifest dependencies and conflicts against caller-supplied installed names without side effects. |
| `components/github_actions_component.py` | Defines the built-in component that exclusively creates its declared `.github/workflows/ci.yml` in an existing project. |
| `components/pytest_component.py` | Defines the built-in component that exclusively creates its declared `pytest.ini` in an existing project. |
| `components/ruff_component.py` | Defines the built-in component that exclusively creates its declared `ruff.toml` in an existing project. |
| `templates/basic/basic_template.py` | Declares the basic metadata, folders, file mapping, and `app.py` VS Code default through shared execution hooks. |
| `templates/basic/basic_files.py` | Owns the complete basic-template mapping and renders its content through `TemplateManager`. |
| `templates/cli/cli_template.py` | Declares the normalized CLI context, folders, file mapping, and context-derived VS Code entry point. |
| `templates/cli/cli_files.py` | Owns the complete CLI mapping and renders root content and argparse application modules. |
| `templates/library/library_template.py` | Declares the normalized library context, folders, file mapping, and no-entry-point VS Code default. |
| `templates/library/library_files.py` | Owns the complete library mapping and renders root content plus empty package initializer files. |
| `templates/template_engine/base_template.py` | Defines the stable template name, metadata, creation, and VS Code entry-point contracts. |
| `templates/template_engine/file_template.py` | Implements the common context, folder, ordered-file-write, and VS Code entry-point-resolution lifecycle for built-ins. |
| `templates/template_engine/package_name.py` | Normalizes project names into ASCII Python package identifiers for package-oriented templates. |
| `templates/template_engine/template_context.py` | Carries the project path/name and optional normalized package name for one generation. |
| `templates/template_engine/template_metadata.py` | Defines immutable descriptive metadata for registered templates. |
| `templates/template_engine/template_registry.py` | Registers templates by metadata name and supplies template and metadata lookups. |
| `templates/template_engine/template_files.py` | Preserves the original `TemplateFiles.basic()` API as a facade over `BasicFiles`. |
| `templates/template_manager.py` | Provides one facade over generated root-file content. |
| `config/default_structure.py` | Supplies the basic generated-project directory list. |
| `config/user_config.py` | Loads, validates, updates, resets, and atomically saves user-level JSON configuration. |
| `config/version.py` | Supplies canonical application metadata. |
| `tests/test_component_registry.py` | Verifies component metadata, built-in and explicit registration, lookup, listing order, and rejection paths without installation side effects. |
| `tests/test_component_installer.py` | Verifies fixed installation sequencing, pre-install rejection, post-success recording, partial-success behavior, and boundary isolation. |
| `tests/test_component_state.py` | Verifies isolated project-local state loading, validation, deterministic atomic persistence, and registry independence. |
| `tests/test_component_validation.py` | Verifies direct dependency/conflict checks, aggregated failures, registry isolation, and validation without writes or installation. |
| `tests/test_github_actions_component.py` | Verifies GitHub Actions metadata, manifest, registration order, nested workflow creation, installer integration, isolation, and existing-target behavior. |
| `tests/test_pytest_component.py` | Verifies pytest metadata, manifest, deterministic registration, isolated installation, and existing-target behavior. |
| `tests/test_ruff_component.py` | Verifies Ruff metadata, manifest, deterministic registration, isolated installation, installer integration, and existing-target behavior. |
| `tests/test_config_command.py` | Verifies configuration parsing, dispatch, output, persistence, reset, and error handling with an isolated home. |
| `tests/test_create_command.py` | Verifies create-input precedence, prompting, configuration errors, and generator delegation without generating a project. |
| `tests/test_cli_template.py` | Verifies CLI metadata, registration, exact output, normalization, module execution, help, version, and editor-entry execution. |
| `tests/test_library_template.py` | Verifies library metadata, registration, exact output, name normalization, generator selection, and basic compatibility in temporary directories. |
| `tests/test_template_architecture.py` | Verifies context/entry-point separation, the basic mapping facade, exact pre-refactor template-output snapshots, and context-derived CLI entry points. |
| `tests/test_template_registry.py` | Verifies metadata, registration, lookup compatibility, and list output without generation or file-system effects. |
| `tests/test_user_config.py` | Verifies configuration behavior in temporary home directories. |
| `tests/test_vscode_builder.py` | Verifies template-aware editor output for all built-in templates in temporary directories. |

## Version Source

`config/version.py` is the canonical source for the ForgePy application version. `VersionCommand` imports `APP_NAME` and `VERSION` from that module and adds the conventional `v` prefix only when displaying the release. Module docstrings do not duplicate release numbers.

Versions rendered into generated projects, template metadata versions, and version fields required by VS Code JSON schemas are independent of the ForgePy release version. The `basic` metadata records `0.6.0`, while `library` and `cli` start at `0.1.0` as independent template revisions; this does not make `config/version.py` a template-version source.

## User Configuration

`ConfigStore` persists user-level settings at `~/.forgepy/config.json`. Its constructor accepts an alternate home directory so tests and library callers can isolate all file-system effects. `ConfigCommand` exposes the store without duplicating its validation or persistence rules.

```mermaid
flowchart LR
    CLI[config show / set / reset] --> Command[ConfigCommand]
    Command --> Store[ConfigStore]
    Create[CreateCommand] -->|location or template omitted| Store
    Store -->|default_location and default_template| Create
    Caller[Tests or library caller] --> Store
    Store --> Defaults[Safe defaults]
    Store --> Validation[Supported names and string values]
    Store --> File[~/.forgepy/config.json]
    File --> Store
```

The supported defaults are `default_template = "basic"`, `default_location = ""`, `author = ""`, and `license = "MIT"`. Loading a missing file returns a new defaults dictionary without creating the directory. Saving creates the directory and atomically replaces the JSON file. Updates preserve other settings; reset is the explicit operation that replaces persisted content with defaults.

`config show` delegates to `ConfigStore.load()`, `config set KEY VALUE` delegates to `ConfigStore.update()`, and `config reset` delegates to `ConfigStore.reset()`. The command formats successful output and converts errors derived from `ForgePyConfigError` into concise CLI messages. A failed show or set does not replace malformed user data; reset is the explicit recovery operation that persists defaults.

When `--location` or `--template` is omitted, `CreateCommand` loads configuration once and resolves only `default_location` and `default_template`. Explicit arguments have priority. An empty configured location preserves the existing prompt, and an empty configured template falls back to `"basic"`. If the required read fails, the command reports the ForgePy configuration error and stops before prompting or generation. When both options are explicit, configuration is not read.

`author` and `license` remain persisted but unused. `ProjectGenerator`, builders, and templates do not import the store or receive its mapping, so the generation lifecycle and generated files are unchanged.

## Dependency flow

```mermaid
flowchart TD
    Main[main.py] --> Parser[Parser]
    Main --> Dispatcher[Dispatcher]
    Parser --> Namespace[argparse Namespace]
    Namespace --> Dispatcher

    Parser --> Catalog[Command catalog]
    Dispatcher --> Catalog
    Catalog --> Create[CreateCommand]
    Catalog --> List[ListCommand]
    Catalog --> Version[VersionCommand]
    Catalog --> Config[ConfigCommand]

    Dispatcher --> Create
    Dispatcher --> List
    Dispatcher --> Version
    Dispatcher --> Config
    Dispatcher --> Component[ComponentCommand]

    Create --> UserConfig
    Create --> Generator[ProjectGenerator]
    List --> Registry[TemplateRegistry]
    Registry --> TemplateMetadata[TemplateMetadata]
    Version --> VersionConfig[config.version]
    Config --> UserConfig[ConfigStore]
    Component --> ComponentRegistry
    Component --> ComponentInstaller
    ComponentInstaller --> ComponentRegistry
    ComponentInstaller --> ComponentContext
    ComponentInstaller --> ComponentStateStore
    ComponentInstaller --> ComponentValidation
    ComponentInstaller -->|install context| BaseComponent
    UserConfig --> ConfigFile[~/.forgepy/config.json]

    subgraph ComponentFoundation[Independent component foundation]
        ComponentRegistry[ComponentRegistry] --> BaseComponent[BaseComponent]
        ComponentRegistry --> PytestComponent[PytestComponent]
        PytestComponent --> BaseComponent
        ComponentRegistry --> ComponentMetadata[ComponentMetadata]
        ComponentRegistry --> ComponentManifest[ComponentManifest]
        BaseComponent --> ComponentMetadata
        BaseComponent --> ComponentManifest
        BaseComponent --> ComponentContext[ComponentContext]
    end

    Generator --> ProjectConfig[ProjectConfig]
    Generator --> Registry
    Registry --> Basic[BasicTemplate]
    Registry --> Library[LibraryTemplate]
    Registry --> Cli[CliTemplate]
    Basic --> TemplateMetadata
    Library --> TemplateMetadata
    Cli --> TemplateMetadata
    Basic --> FileTemplate[FileTemplate]
    Library --> FileTemplate
    Cli --> FileTemplate
    FileTemplate --> Context[TemplateContext]
    FileTemplate --> FolderBuilder[FolderBuilder]
    FileTemplate --> FileBuilder[FileBuilder]
    Basic --> BasicFiles[BasicFiles.build]
    Library --> LibraryFiles[LibraryFiles.build]
    Library --> PackageName[normalize_package_name]
    Cli --> CliFiles[CliFiles.build]
    Cli --> PackageName
    BasicFiles --> TemplateManager[TemplateManager]
    LibraryFiles --> TemplateManager
    CliFiles --> TemplateManager
    TemplateManager --> Content[Content template functions]
    Basic -->|app.py default| VSCodeRequirement[VS Code entry-point compatibility property]
    Library -->|None default| VSCodeRequirement
    Cli -->|context-derived package / cli.py| VSCodeRequirement

    Generator --> Environment[EnvironmentBuilder]
    Generator --> PythonTools[PythonToolsBuilder]
    Generator --> Requirements[RequirementsInstaller]
    Generator --> Git[GitBuilder]
    Generator -->|project root + selected template requirement| VSCode[VSCodeBuilder]
    VSCode --> VSCodeTemplates[templates.vscode]
```

CLI and orchestration layers depend on lower-level services. Template content modules do not depend on the CLI or generator. Builders receive paths and content rather than parsing arguments or selecting templates. `ComponentCommand` is the only application connection to the component foundation; components remain disconnected from configuration, templates, builders, `ProjectGenerator`, and generated-project creation.

## Class relationships

- `Command` defines the shared name, help metadata, parser-configuration hook, and execution contract implemented by `CreateCommand`, `ListCommand`, `VersionCommand`, `ConfigCommand`, and `ComponentCommand`.
- `cli.commands.create_commands()` is the single built-in command catalog used by both `Parser` and `Dispatcher`.
- `Dispatcher` derives its CLI-name mapping from that catalog.
- `CreateCommand` resolves explicit, persisted, and interactive/default inputs before invoking `ProjectGenerator`; `ListCommand` reads descriptive metadata from `TemplateRegistry`, `VersionCommand` reads canonical application-version metadata, `ConfigCommand` delegates user-setting operations to `ConfigStore`, and `ComponentCommand` reads installed state or delegates add operations to `ComponentInstaller` while adapting operational errors for the CLI.
- `ProjectConfig` is a slotted dataclass used by `ProjectGenerator` to derive the target root. Its project name must be one non-empty filesystem segment: dot names, absolute and drive-qualified names, separators, and lexical multi-component names are rejected explicitly.
- `ComponentMetadata` is a frozen, slotted dataclass containing `name`, `description`, component `version`, `author`, and immutable `tags`. Construction validates scalar types, rejects empty or whitespace-only names, and snapshots tag iterables as tuples.
- `ComponentManifest` is a frozen, slotted dataclass containing owned or managed project-relative `pathlib.Path` entries, dependency names, and conflict names. Construction snapshots collections as tuples; rejects invalid or empty entries, duplicates, absolute paths, and lexical parent traversal; and performs no filesystem resolution.
- `ComponentContext` contains only a `pathlib.Path` for an existing project directory and rejects missing paths, files, and non-`Path` values before installation.
- `BaseComponent` exposes abstract `name`, `metadata`, `manifest`, and `install(context)` members. The hook defines no orchestration, rollback, discovery, or dependency behavior.
- `ComponentInstaller.install(name, project_path)` owns only the fixed sequence connecting registry lookup, context validation, project-local state loading, already-installed rejection, direct relationship validation, one installation hook, and state recording after hook success.
- `ComponentRegistry` deterministically registers `PytestComponent`, `RuffComponent`, then `GitHubActionsComponent`, stores component instances directly, requires matching component and metadata names, rejects self-dependency, self-conflict, and duplicate registrations before mutation, preserves registration order, and returns an immutable tuple from `list_components()`.
- `ComponentStateStore` uses an existing project path validated through `ComponentContext`, exposes load/save/add/membership operations, and atomically persists only installed component names at `.forgepy/components.json`. It resolves the project root, state directory, state file, and write-time temporary file and rejects any path that escapes its required in-project location. Missing state is empty; malformed state raises a component-state error and is not overwritten implicitly.
- `validate_component(component, installed_components)` checks only the selected component's direct manifest relationships against an explicit iterable of installed names. `ComponentValidationError` reports ordered missing dependencies and active conflicts together without installing or resolving anything.
- `PytestComponent` declares only `pytest.ini`, has no dependencies or conflicts, and installs by exclusively creating deterministic pytest configuration under `ComponentContext.project_path`. An existing target raises `FileExistsError` without modification.
- `RuffComponent` declares only `ruff.toml`, has no dependencies or conflicts, and installs by exclusively creating deterministic Ruff configuration under `ComponentContext.project_path`. An existing target raises `FileExistsError` without modification; no Ruff package or executable is installed.
- `GitHubActionsComponent` declares only `.github/workflows/ci.yml`, has no ForgePy component dependencies or conflicts, creates required parent directories, and exclusively writes a minimal deterministic Python CI workflow. The workflow installs pytest and Ruff on its GitHub Actions runner; local component installation installs no packages and modifies no project dependency files.
- `TemplateMetadata` is a frozen, slotted dataclass containing `name`, `description`, template `version`, `author`, and immutable `tags`. Construction validates scalar types, rejects empty or whitespace-only names, and snapshots tag iterables as tuples.
- `BaseTemplate` remains the stable public `name`, `create()`, metadata, and `vscode_entry_point` contract. Its compatibility defaults for legacy subclasses are unchanged.
- `FileTemplate` is an opt-in `BaseTemplate` implementation used by the three built-ins. It derives `name` from the class's immutable metadata, builds a `TemplateContext`, creates declared folders, writes the ordered template-owned mapping through `FileBuilder`, and assigns its resolved VS Code entry point only after all writes succeed. `_DEFAULT_VSCODE_ENTRY_POINT` supplies static behavior, while `_vscode_entry_point_for(context)` resolves context-derived paths.
- `TemplateContext` is a frozen, slotted value containing the project path and an optional normalized package name. `project_name` is derived from the path; package-oriented hooks use a checked accessor. Normalization policy remains in `normalize_package_name()` and the Library/CLI wrappers.
- The public `vscode_entry_point` contract remains unchanged: `BasicTemplate` exposes `app.py`, `LibraryTemplate` exposes `None`, and `CliTemplate` resolves `<normalized-package>/cli.py` from its completed generation context.
- `TemplateRegistry.register()` is the single extension path. It accepts only `BaseTemplate` instances with `TemplateMetadata`, rejects empty names, requires `metadata.name` to match `template.name`, and rejects duplicates before changing registry state. It stores the template and metadata together under the authoritative metadata name. `get()` still returns the executable `BaseTemplate`; `get_metadata()` and `list_metadata()` expose descriptive data separately.
- `list_templates()` and the public `templates` view retain their existing name-to-template dictionary shape for compatibility, but return defensive snapshots so callers cannot desynchronize registry state.
- `BaseBuilder` is the parent of `FileBuilder`, `FolderBuilder`, and `PythonToolsBuilder`; it currently defines no methods.
- Core builder-style services are coordinated directly by `ProjectGenerator` and do not inherit from `BaseBuilder`.

## Component registry foundation

ForgePy registers `PytestComponent`, `RuffComponent`, then `GitHubActionsComponent` by default. `ComponentRegistry` remains an installation- and resolution-agnostic in-memory catalog: `register(component)` validates its contract, component/metadata identity, and absence of self-references, then stores one `BaseComponent`; `get(name)` returns the registered instance or preserves the standard `KeyError`; and `list_components()` returns an immutable tuple in registration order. Registration does not install components, look up dependencies, evaluate relationships between components, or select installation order.

`ComponentMetadata`, `ComponentManifest`, `ComponentContext`, and `BaseComponent` are independent from `TemplateMetadata`, `TemplateContext`, `BaseTemplate`, and `TemplateRegistry`; neither registry imports or registers objects from the other system. `component list` presents registered metadata without invoking installation. `component installed --project PATH` presents every name stored for that project without registry filtering or filesystem inference. `component add NAME --project PATH` delegates the fixed installation and state-recording sequence to `ComponentInstaller`. The component system performs no discovery, dependency resolution, installation ordering, rollback, uninstall, package installation, template association, or generation integration.

Pre-install relationship validation is an explicit, separate call. The caller supplies the complete set of component names it considers installed; the validator does not discover, load, or persist that state. Validation checks direct declarations only, reports every missing dependency and active conflict for the selected component, performs no registry lookup or filesystem operation, and never invokes `install()`. It does not validate transitive relationships, version constraints, optional dependencies, or installation order.

## Project-local component state

`ComponentStateStore(project_path)` owns only `.forgepy/components.json` below the validated existing project. The persisted document has one field:

```json
{
    "installed": [
        "example",
        "pytest"
    ]
}
```

`load()` resolves and confines `.forgepy` and `components.json` before reading, then treats a genuinely missing in-project file as `frozenset()`. `save(names)` validates non-empty strings, removes duplicates, sorts names for deterministic JSON, creates `.forgepy` when required, revalidates its resolved location, places and verifies a temporary file in that same directory, flushes and `fsync()`s it, and atomically replaces the confined destination. Existing symlinks, junctions, or equivalent redirections that resolve the directory or file outside the project raise `ComponentStateIOError` without reading, writing, replacing, or removing the redirected target. `add(name)` loads before saving so malformed existing data remains untouched; `is_installed(name)` checks the loaded state. Format and I/O failures use ForgePy-specific component-state errors.

The store is not used by `ComponentRegistry`, validation, or concrete installation hooks. `ComponentInstaller` connects it to an installation sequence, while the read-only `component installed --project PATH` CLI action loads it directly for presentation. Registered names and installed names remain separate. There is no uninstall, rollback, discovery, project scanning, component version locking, dependency resolution, installation ordering, or transitive traversal.

## Component installation orchestration

`ComponentInstaller` connects the independent component contracts for library callers while leaving each dependency responsible for its existing behavior. A default installer creates `ComponentRegistry`; tests and callers may inject a registry. `install(name, project_path)` performs exactly:

1. Resolve `name` through `ComponentRegistry.get()`.
2. Build `ComponentContext` for the explicit existing project path.
3. Create `ComponentStateStore` for that project and load installed names.
4. Raise `ComponentAlreadyInstalledError` if state already contains the component name.
5. Call `validate_component(component, installed_names)` for direct relationships.
6. Call `component.install(context)` once.
7. After hook success, call `state_store.add(component.name)`.

Lookup, context, state-format, relationship-validation, installation-hook, and state-I/O errors propagate without being converted into resolution behavior. Failures through step 6 do not record the requested component. If step 7 fails, installed files may already exist while state remains unchanged; Sprint 9.7 surfaces that partial success and performs no rollback.

The orchestrator does not install dependencies, calculate ordering, traverse graphs, inspect projects, install packages, or implement rollback/uninstall. `ComponentRegistry`, `ComponentStateStore`, `validate_component()`, and concrete components remain unaware of orchestration. `ComponentCommand` delegates add operations to the installer and only maps lookup, context, already-installed, validation, state, target-file, and filesystem failures to friendly output. Handled errors retain ForgePy's existing zero-exit-status behavior.

## Template system

The registry registers `BasicTemplate`, `LibraryTemplate`, and `CliTemplate` in that order through `register()`. Each registration stores its executable instance and immutable `TemplateMetadata` under the stable metadata name. `get()` returns the corresponding creatable template for `basic`, `library`, or `cli`, while `get_metadata()` and `list_metadata()` provide presentation data without invoking `create()`. The legacy `list_templates()` mapping remains available.

Template metadata descriptions and tags are limited to implemented behavior. Template revisions are separate from the ForgePy application version and the version rendered into a generated project. `ListCommand` displays only metadata name and description, in registry order.

The three built-ins inherit the opt-in `FileTemplate` implementation. Its common `create()` method performs the previously duplicated work in this order:

1. Build a `TemplateContext` for the requested project path.
2. Ask the selected template for its ordered folder definition.
3. Delegate folder creation to the unchanged `FolderBuilder`.
4. Ask the selected template-owned mapping for rendered file content.
5. Delegate every ordered filename/content pair to the unchanged `FileBuilder`.
6. Resolve and publish the template's VS Code entry point only after every file write succeeds.

Metadata is not part of this per-generation context. `TemplateMetadata` remains registration and presentation data; `TemplateContext` carries the project path/name and optional normalized package name; and `BasicFiles`, `LibraryFiles`, and `CliFiles` own their complete output mappings. `FileTemplate` keeps VS Code entry-point defaults and context-based resolution separate from generated content without another tooling model.

`BasicFiles`, `LibraryFiles`, and `CliFiles` each instantiate `TemplateManager` and own their complete ordered mappings. They directly call the same README, Git-ignore, and pyproject renderers where output is shared. `TemplateFiles.basic()` remains available as a compatibility facade and delegates to `BasicFiles.build()`.

`BasicTemplate` supplies `config.default_structure.DEFAULT_FOLDERS`, delegates its nine-file mapping to `BasicFiles`, and declares the `app.py` VS Code default. Its mapping remains `README.md`, `.gitignore`, `requirements.txt`, `app.py`, `LICENSE`, `CHANGELOG.md`, `.env`, `.env.example`, and `pyproject.toml`, with content produced through `TemplateManager`.

`LibraryTemplate` builds a context with an import-package name derived from the project-root name. It lowercases the name, replaces runs of characters outside ASCII `[a-z0-9_]` with `_`, strips surrounding underscores, prefixes a leading digit, and suffixes a Python keyword. Its folder and file hooks produce this unchanged template-owned structure:

```text
<project-root>/
|-- <normalized-package>/
|   `-- __init__.py
|-- tests/
|   `-- __init__.py
|-- .gitignore
|-- README.md
|-- pyproject.toml
`-- requirements.txt
```

`LibraryFiles.build()` renders the existing root content directly through `TemplateManager` and adds an empty requirements file and both empty initializer files. The original project name remains in README and pyproject content; normalization applies only to the import-package directory.

`LibraryTemplate` and `CliTemplate` delegate package-name normalization to `templates/template_engine/package_name.py`. The helper lowercases the project name, replaces runs outside ASCII `[a-z0-9_]` with `_`, strips surrounding underscores, prefixes a leading digit, and suffixes a Python keyword. `LibraryTemplate` retains its existing private wrapper, while `CliTemplate` exposes the same local call boundary.

`CliTemplate` stores the same normalized package data in its context. Its folder and file hooks produce this unchanged template-owned structure:

```text
<project-root>/
|-- <normalized-package>/
|   |-- __init__.py
|   |-- __main__.py
|   `-- cli.py
|-- tests/
|   `-- __init__.py
|-- .gitignore
|-- README.md
|-- pyproject.toml
`-- requirements.txt
```

`CliFiles.build()` renders the existing root content directly through `TemplateManager` and writes empty requirements and initializer files. Its generated `cli.py` uses `argparse`, exposes help and version options, returns success with no arguments, and can run directly. Package `__main__.py` delegates to that interface, enabling `python -m <normalized-package>`. The generated application version is a fixed `0.1.0` independent of ForgePy and template metadata.

VS Code files are not part of a template's file mapping. `FileTemplate` exposes each built-in's explicit optional entry point through the existing `vscode_entry_point` property. Static templates use `_DEFAULT_VSCODE_ENTRY_POINT`; CLI resolves its package-relative path from `TemplateContext` after successful file writes. `ProjectGenerator` forwards the property to `VSCodeBuilder` after the rest of project setup. The builder still calls the functions in `templates/vscode/` and writes four JSON files under `.vscode/`.

For `basic`, the entry point is `app.py`; its existing launch configuration and `Run Application` task are preserved. For `library`, the entry point is `None`; `launch.json` has an empty `configurations` list and `tasks.json` retains only `Install Requirements`. The CLI entry point starts as `None` and resolves to `<normalized-package>/cli.py` only after writing it; the unchanged launch and run-task renderers then target that real, directly executable file. Shared settings, requirements tasks, and extension recommendations remain unchanged. The builder does not inspect the generated filesystem to choose a profile.

## CLI flow

```mermaid
flowchart LR
    Args[Command-line arguments] --> Parse[Parser.parse]
    Catalog[Command catalog] --> Parse
    Parse --> Dispatch[Dispatcher.dispatch]
    Catalog --> Dispatch
    Dispatch -->|create or no command| Create[CreateCommand]
    Dispatch -->|list| List[ListCommand]
    Dispatch -->|version| Version[VersionCommand]
    Dispatch -->|config| Config[ConfigCommand]
    Dispatch -->|component| Component[ComponentCommand]
    Create --> Resolve[Resolve create inputs]
    Resolve -->|location or template omitted| Store[ConfigStore]
    Store --> Resolve
    Resolve -->|project name or location still empty| Prompt[Interactive prompts]
    Prompt --> Resolve
    Resolve --> Generator[ProjectGenerator.create]
    List --> Registry[TemplateRegistry.list_metadata]
    Registry --> TemplateInfo[TemplateMetadata name + description]
    Version --> Metadata[config.version + platform]
    Config -->|show / set / reset| Store[ConfigStore]
    Store --> UserFile[~/.forgepy/config.json]
    Component -->|list| ComponentRegistry[ComponentRegistry]
    Component -->|add NAME + PATH| Installer[ComponentInstaller]
    Installer --> ComponentContext[ComponentContext]
    Installer --> ComponentState[ComponentStateStore]
    Installer --> ComponentValidation[validate_component]
    Installer --> Install[BaseComponent.install]
```

### Startup and dispatch

1. `main()` creates `Parser` and parses `sys.argv` through `argparse`.
2. `Dispatcher` selects `create`, `list`, `version`, `config`, or `component`.
3. With no subcommand, the dispatcher selects `create` for interactive compatibility.
4. The selected command receives the parsed `Namespace`.

### Configuration workflow

`ConfigCommand` owns the nested `show`, `set`, and `reset` syntax. It lazily creates a default `ConfigStore` only when a configuration action executes; tests inject a store rooted in a temporary home directory.

1. `show` loads the effective configuration and displays every supported setting. A missing file produces defaults without creating the configuration directory.
2. `set KEY VALUE` asks the store to validate and persist one setting while preserving the others.
3. `reset` explicitly persists all safe defaults, including when recovery from malformed content is required.
4. Store errors are displayed with a ForgePy error prefix and no traceback.

`ConfigCommand` manages all four persistent values. Separately, `CreateCommand` may read only `default_location` and `default_template` while resolving omitted create options. Neither command passes the store or configuration mapping into `ProjectGenerator`.

### Create workflow

`CreateCommand` uses these independent precedence rules before calling `ProjectGenerator.create()`:

1. Project name: explicit positional argument, then the existing prompt.
2. Location: explicit `--location`, then non-empty `default_location`, then the existing prompt.
3. Template: explicit `--template`, then non-empty `default_template`, then `"basic"`.

Argparse uses `None` for an omitted template so an explicit `--template basic` remains distinguishable from omission. The store is loaded only when location or template is omitted. A malformed or unreadable required configuration aborts resolution with a clear error; it is not overwritten or silently replaced by the fallback.

The generator then executes these stages in order:

1. Resolve the requested parent location and confirm that it is an existing directory.
2. Validate the project-name segment, require the resolved destination to remain directly below that location, and reject an existing file, directory, symlink, or junction.
3. Create the new project root exclusively.
4. Look up and create the selected template.
5. Create `.venv`.
6. Upgrade `pip`, `setuptools`, and `wheel`.
7. Install packages from `requirements.txt` when present and non-empty.
8. Initialize Git and attempt an initial commit.
9. Write Visual Studio Code configuration.
10. Print the resulting project path.

All destination checks occur before the project root or template files are created. Existing destinations are never merged with ForgePy output. Template lookup still follows root creation and retains its existing `KeyError` semantics.

```mermaid
sequenceDiagram
    participant C as CreateCommand
    participant UC as ConfigStore
    participant G as ProjectGenerator
    participant TR as TemplateRegistry
    participant T as Selected BaseTemplate
    participant TC as TemplateContext
    participant F as BasicFiles / LibraryFiles / CliFiles
    participant TM as TemplateManager / content functions
    participant B as FolderBuilder / FileBuilder
    participant E as Environment tooling
    participant R as RequirementsInstaller
    participant Git as GitBuilder
    participant V as VSCodeBuilder

    opt Location or template omitted
        C->>UC: load()
        break ConfigStore raises ForgePyConfigError
            UC-->>C: configuration error
            C->>C: Report error and return before generation
        end
        UC-->>C: validated settings
    end
    C->>C: Resolve CLI, persisted, and prompt/basic values
    C->>G: create(name, location, template)
    G->>G: Resolve location and validate a new direct-child destination
    G->>G: Create project root exclusively
    G->>TR: get(template_name)
    TR-->>G: Selected template instance
    G->>T: create(project root)
    T->>TC: Build project/package context
    TC-->>T: Immutable generation data
    T->>B: Create template folders
    T->>F: Build project file mapping
    F->>TM: Render root-file content
    TM-->>F: Rendered strings
    F-->>T: Complete filename/content mapping
    loop Each mapped file
        T->>B: Write UTF-8 content
    end
    T->>T: Resolve VS Code entry point
    G->>E: Create .venv
    G->>E: Upgrade pip, setuptools, wheel
    G->>R: Install non-empty requirements
    G->>Git: Initialize and attempt initial commit
    T-->>G: vscode_entry_point
    G->>V: Write .vscode for explicit entry point
    G-->>C: Print completion and project path
```

The current implementation uses Windows executable paths such as `.venv/Scripts/python.exe` and `.venv/Scripts/pip.exe`.

## Known limitations and technical debt

- The full generation lifecycle assumes Windows `.venv/Scripts/*.exe` paths.
- Automated coverage includes component metadata and registry behavior, user configuration, create-input resolution, project-name and destination safety, template metadata and registry behavior, list output, shared template contracts, exact normalized template-owned file snapshots, all built-in structures, generated CLI subprocess behavior, template-aware VS Code behavior, and isolated selection through `ProjectGenerator`; the real external lifecycle and other application areas remain uncovered.
- `author` and `license` are persisted but not applied to generated content.
- `TemplateRegistry.get()` raises `KeyError` for unknown names rather than producing a command-level error.
- Template metadata has no independent versioning policy yet; `basic` records `0.6.0`, while `library` and `cli` start at `0.1.0` as template-specific revisions.
- Most subprocess failures propagate; only the initial Git commit has local error handling.
- `BaseBuilder` has no behavioral contract, and core builder-style services do not share its inheritance hierarchy.
- `ComponentRegistry` is in-memory and installation-state-agnostic, with `pytest`, `ruff`, and `github-actions` registered by default. `ComponentInstaller` coordinates explicit library and CLI add calls without moving behavior into the registry, store, validator, or component. Discovery, transitive dependency resolution, installation ordering, rollback, package installation, template association, and generation integration remain undefined.
- `config.default_structure.DEFAULT_FILES` is currently unused. `BasicFiles`, `LibraryFiles`, and `CliFiles` own their mappings; `TemplateFiles.basic()` is retained only as a compatibility facade.
- `CliTemplate` retains per-instance resolved entry-point state. `vscode_entry_point` reports `None` before the generated `cli.py` has been written and is recomputed for each successful `create()` call.
- The compatibility `TemplateFiles.basic()` facade creates a deliberate template-engine-to-Basic dependency until an explicit compatibility change removes the older API.
- The root README, requirements file, root `config.py`, and utility logger are empty.

## Safe extension rules

Apply the design principles and Definition of Done in [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) to every architectural change.

### Commands

- Implement the `Command` metadata and `execute(args)` contract; override `configure_parser()` only when the command accepts arguments.
- Add the command to `cli.commands.create_commands()`. Parser and dispatcher registration then follow automatically.
- Keep argument parsing out of core services and preserve the no-command interactive create fallback.
- Add tests or documented manual checks for dispatch, validation, and existing commands.

### Templates

- Preserve `BaseTemplate` for custom execution models. File-mapping built-ins should use `FileTemplate` and provide only focused context, folder, file, and VS Code entry-point hooks rather than repeating builder loops. Subclasses that override `__init__()` must call `super().__init__()`.
- Provide `TemplateMetadata` with a non-empty stable `name`; factual string `description`; string template `version` and `author`; and an iterable of string `tags` stored as a tuple. Keep its name aligned with `BaseTemplate.name` and register through `TemplateRegistry.register()`.
- Build normalized package data in `TemplateContext` without moving naming policy out of `normalize_package_name()`. Keep complete ordered mappings in the owning template package and reuse established rendered content directly through `TemplateManager`.
- Declare `_DEFAULT_VSCODE_ENTRY_POINT` for static behavior or override `_vscode_entry_point_for(context)` for a derived path. Use the real generated path or `None`, and do not infer it from the filesystem.
- Do not change the `basic`, `library`, or `cli` names or output contracts incidentally.
- Verify metadata registration, registry listing and selection, generated folders/files, and template-matched VS Code JSON in an isolated location.

### Components

- Register only `BaseComponent` implementations with valid `ComponentMetadata` and matching non-empty names.
- Keep the default `ComponentRegistry` catalog limited to the explicitly approved `pytest`, `ruff`, and `github-actions` components, registered in that order, until another built-in is separately approved.
- Keep persistence, discovery, dependency handling, package installation, template association, and generation integration outside the component CLI.

### User Configuration

- Keep persistence and validation in `ConfigStore`; `ConfigCommand` should contain only CLI parsing, presentation, and error adaptation.
- Resolve `default_location` and `default_template` in `CreateCommand` with explicit CLI values first and existing prompt/basic behavior last.
- Keep `ProjectGenerator`, builders, and templates independent of `ConfigStore`; applying `author` or `license` requires a separate explicit requirement.
- Add supported settings to the defaults and validation schema together.
- Preserve malformed files on load/update failures, and use injected temporary home directories in tests.

### Core lifecycle

- Keep sequencing in `ProjectGenerator` and side effects in focused builders/services.
- Preserve stage order and existing user-visible behavior unless a reviewed requirement explicitly changes them.
- Avoid circular dependencies from templates or builders back into the CLI.
