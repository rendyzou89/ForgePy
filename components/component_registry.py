"""In-memory registration for component definitions."""

from components.base_component import BaseComponent
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata


class ComponentRegistry:
    """Validate and store explicitly registered components."""

    def __init__(self) -> None:
        self._components: dict[str, BaseComponent] = {}

    def register(self, component: BaseComponent) -> None:
        """Register one component under its validated metadata name."""

        if not isinstance(component, BaseComponent):
            raise TypeError("Component must inherit from BaseComponent.")

        component_name = component.name

        if not isinstance(component_name, str):
            raise TypeError("Component name must be a string.")

        if not component_name.strip():
            raise ValueError("Component name must not be empty.")

        metadata = component.metadata

        if not isinstance(metadata, ComponentMetadata):
            raise TypeError(
                "Component metadata must be ComponentMetadata."
            )

        if component_name != metadata.name:
            raise ValueError(
                "Component name and metadata name must match."
            )

        manifest = component.manifest

        if not isinstance(manifest, ComponentManifest):
            raise TypeError(
                "Component manifest must be ComponentManifest."
            )

        if component_name in manifest.dependencies:
            raise ValueError("A component must not depend on itself.")

        if component_name in manifest.conflicts:
            raise ValueError("A component must not conflict with itself.")

        if component_name in self._components:
            raise ValueError(
                f"Component '{component_name}' is already registered."
            )

        self._components[component_name] = component

    def get(self, name: str) -> BaseComponent:
        """Return the component registered under ``name``."""

        return self._components[name]

    def list_components(self) -> tuple[BaseComponent, ...]:
        """Return registered components in registration order."""

        return tuple(self._components.values())
