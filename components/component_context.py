"""Validated project information supplied to component installations."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ComponentContext:
    """Identify the existing project directory a component may modify."""

    project_path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.project_path, Path):
            raise TypeError("Component project path must be a Path.")

        if not self.project_path.exists():
            raise ValueError("Component project path must exist.")

        if not self.project_path.is_dir():
            raise ValueError("Component project path must be a directory.")
