"""CLI access to registered ForgePy components."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from cli.command import Command
from components.component_context import ComponentContext
from components.component_registry import ComponentRegistry


class ComponentCommand(Command):
    """List components or install one into an existing project."""

    name = "component"
    summary = "List or add ForgePy components."
    description = (
        "List registered ForgePy components or add one to an existing "
        "project."
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

    def execute(self, args: Namespace) -> None:
        action = getattr(args, "component_action", None)

        if action == "list":
            self._list()
        elif action == "add":
            self._add(args.component_name, args.project)
        else:
            print(f"[ERROR] Unknown component action: '{action}'.")

    def _list(self) -> None:
        print("=" * 40)
        print(" ForgePy Components ")
        print("=" * 40)

        for component in self._get_registry().list_components():
            metadata = component.metadata
            print(f"- {metadata.name}: {metadata.description}")

    def _add(self, name: str, project_path: Path) -> None:
        try:
            component = self._get_registry().get(name)
        except KeyError:
            print(f"[ERROR] Unknown ForgePy component: '{name}'.")
            return

        try:
            context = ComponentContext(project_path=project_path)
            component.install(context)
        except (TypeError, ValueError) as error:
            print(f"[ERROR] Invalid project path '{project_path}': {error}")
            return
        except FileExistsError as error:
            target = error.filename or str(project_path)
            print(
                "[ERROR] Component installation refused because the target "
                f"already exists: '{target}'."
            )
            return
        except OSError as error:
            print(f"[ERROR] Component installation failed: {error}")
            return

        print(
            f"[OK] Component '{name}' added to project "
            f"'{project_path}'."
        )

    def _get_registry(self) -> ComponentRegistry:
        if self._registry is None:
            self._registry = ComponentRegistry()

        return self._registry
