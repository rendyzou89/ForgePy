"""
==================================================
ForgePy
Base Template
==================================================
"""

from abc import ABC, abstractmethod
from pathlib import Path

from templates.template_engine.template_metadata import TemplateMetadata


class BaseTemplate(ABC):
    """
    Seluruh template harus mewarisi class ini.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nama template.
        """
        pass

    @property
    def metadata(self) -> TemplateMetadata:
        """Return compatibility metadata for legacy template subclasses."""

        return TemplateMetadata(
            name=self.name,
            description="",
            version="",
            author="",
            tags=(),
        )

    @abstractmethod
    def create(
        self,
        project_path: Path,
    ) -> None:
        """
        Membuat project.
        """
        pass
