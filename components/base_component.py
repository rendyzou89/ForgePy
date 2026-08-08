"""Minimal contract for component definitions and installation."""

from abc import ABC, abstractmethod

from components.component_context import ComponentContext
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata


class BaseComponent(ABC):
    """Expose component identity, metadata, and installation behavior."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable component registration name."""

    @property
    @abstractmethod
    def metadata(self) -> ComponentMetadata:
        """Return descriptive metadata for this component."""

    @property
    @abstractmethod
    def manifest(self) -> ComponentManifest:
        """Return declarative installation properties for this component."""

    @abstractmethod
    def install(self, context: ComponentContext) -> None:
        """Install the component into the context's existing project."""
