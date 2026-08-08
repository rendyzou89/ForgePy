"""Minimal contract for component definitions."""

from abc import ABC, abstractmethod

from components.component_metadata import ComponentMetadata


class BaseComponent(ABC):
    """Expose component identity and metadata without execution behavior."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable component registration name."""

    @property
    @abstractmethod
    def metadata(self) -> ComponentMetadata:
        """Return descriptive metadata for this component."""
