from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProjectConfig:
    """
    Menyimpan konfigurasi project.
    """

    name: str
    location: Path

    @property
    def root(self) -> Path:
        return self.location / self.name