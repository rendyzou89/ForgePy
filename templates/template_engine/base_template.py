"""
==================================================
ForgePy
Base Template
==================================================
"""

from abc import ABC, abstractmethod
from pathlib import Path


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

    @abstractmethod
    def create(
        self,
        project_path: Path,
    ) -> None:
        """
        Membuat project.
        """
        pass