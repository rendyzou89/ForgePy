"""Minimal orchestration for installing one registered component."""

from pathlib import Path

from components.component_context import ComponentContext
from components.component_registry import ComponentRegistry
from components.component_state import ComponentStateStore
from components.component_validation import validate_component


class ComponentInstallationError(Exception):
    """Base error for component installation orchestration."""


class ComponentAlreadyInstalledError(ComponentInstallationError):
    """Raised when project-local state already records a component."""


class ComponentInstaller:
    """Coordinate one explicit component installation in fixed order."""

    def __init__(self, registry: ComponentRegistry | None = None) -> None:
        self._registry = (
            ComponentRegistry()
            if registry is None
            else registry
        )

    def install(self, name: str, project_path: Path) -> None:
        """Install and then record one component for an existing project."""

        component = self._registry.get(name)
        context = ComponentContext(project_path=project_path)
        state_store = ComponentStateStore(project_path)
        installed_components = state_store.load()

        if component.name in installed_components:
            raise ComponentAlreadyInstalledError(
                f"Component '{component.name}' is already installed."
            )

        validate_component(component, installed_components)
        component.install(context)
        state_store.add(component.name)
