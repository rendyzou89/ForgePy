"""CLI access to registered ForgePy components."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from cli.command import Command
from components.component_installer import (
    ComponentAlreadyInstalledError,
    ComponentInstaller,
)
from components.component_registry import ComponentRegistry
from components.component_state import (
    ComponentStateStore,
    ForgePyComponentStateError,
)
from components.component_validation import ComponentValidationError


class ComponentCommand(Command):
    """List available or installed components, or install one."""

    name = "component"
    summary = "List, inspect, or add ForgePy components."
    description = (
        "List registered ForgePy components, inspect project-local installed "
        "state, or add one to an existing project."
    )

    def __init__(self, registry: ComponentRegistry | None = None) -> None:
        self._registry = registry

    def configure_parser(self, parser: ArgumentParser) -> None:
        actions = parser.add_subparsers(
            dest="component_action",
            title="component actions",
            description="Available component actions",
            metavar="ACTION",
            required=True,
        )

        actions.add_parser(
            "list",
            help="List registered built-in components.",
            description=(
                "List registered built-in component names and descriptions."
            ),
        )

        installed_parser = actions.add_parser(
            "installed",
            help="List components recorded as installed in a project.",
            description=(
                "List component names recorded in an explicitly supplied "
                "existing project directory."
            ),
        )
        installed_parser.add_argument(
            "--project",
            required=True,
            type=Path,
            metavar="PATH",
            help="Path to an existing project directory.",
        )

        add_parser = actions.add_parser(
            "add",
            help="Add a registered component to an existing project.",
            description=(
                "Add a registered component to an explicitly supplied "
                "existing project directory."
            ),
        )
        add_parser.add_argument(
            "component_name",
            metavar="NAME",
            help="Registered component name.",
        )
        add_parser.add_argument(
            "--project",
            required=True,
            type=Path,
            metavar="PATH",
            help="Path to an existing project directory.",
        )

    def execute(self, args: Namespace) -> int:
        action = getattr(args, "component_action", None)

        if action == "list":
            self._list()
            return 0
        elif action == "installed":
            return self._installed(args.project)
        elif action == "add":
            return self._add(args.component_name, args.project)
        else:
            print(f"[ERROR] Unknown component action: '{action}'.")
            return 1

    def _list(self) -> None:
        print("=" * 40)
        print(" ForgePy Components ")
        print("=" * 40)

        for component in self._get_registry().list_components():
            metadata = component.metadata
            print(f"- {metadata.name}: {metadata.description}")

    @staticmethod
    def _installed(project_path: Path) -> int:
        try:
            installed_components = ComponentStateStore(project_path).load()
        except ForgePyComponentStateError as error:
            print(f"[ERROR] {error}")
            return 1
        except (TypeError, ValueError) as error:
            print(f"[ERROR] Invalid project path '{project_path}': {error}")
            return 1

        if not installed_components:
            print("No installed components.")
            return 0

        print("Installed components:")
        for component_name in sorted(installed_components):
            print(f"- {component_name}")

        return 0

    def _add(self, name: str, project_path: Path) -> int:
        try:
            self._get_registry().get(name)
        except KeyError:
            print(f"[ERROR] Unknown ForgePy component: '{name}'.")
            return 1

        try:
            ComponentInstaller(
                registry=self._get_registry(),
            ).install(
                name=name,
                project_path=project_path,
            )
        except ComponentAlreadyInstalledError as error:
            print(f"[ERROR] {error}")
            return 1
        except ComponentValidationError as error:
            print(f"[ERROR] {error}")
            return 1
        except ForgePyComponentStateError as error:
            print(f"[ERROR] {error}")
            return 1
        except (TypeError, ValueError) as error:
            print(f"[ERROR] Invalid project path '{project_path}': {error}")
            return 1
        except FileExistsError as error:
            target = error.filename or str(project_path)
            print(
                "[ERROR] Component installation refused because the target "
                f"already exists: '{target}'."
            )
            return 1
        except OSError as error:
            print(f"[ERROR] Component installation failed: {error}")
            return 1

        print(
            f"[OK] Component '{name}' added to project "
            f"'{project_path}'."
        )
        return 0

    def _get_registry(self) -> ComponentRegistry:
        if self._registry is None:
            self._registry = ComponentRegistry()

        return self._registry
