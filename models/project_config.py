from dataclasses import dataclass
from pathlib import Path, PureWindowsPath


@dataclass(slots=True)
class ProjectConfig:
    """
    Menyimpan konfigurasi project.
    """

    name: str
    location: Path

    def __post_init__(self) -> None:
        """Validate the name used to construct the project destination."""

        if not isinstance(self.name, str):
            raise TypeError("Project name must be a string.")

        if not self.name:
            raise ValueError("Project name must not be empty.")

        if self.name in {".", ".."}:
            raise ValueError("Project name must be one filesystem path segment.")

        if "/" in self.name or "\\" in self.name:
            raise ValueError("Project name must not contain path separators.")

        path_name = Path(self.name)
        windows_name = PureWindowsPath(self.name)

        if path_name.is_absolute() or windows_name.is_absolute():
            raise ValueError("Project name must not be an absolute path.")

        if windows_name.drive:
            raise ValueError("Project name must not be drive-qualified.")

        if len(path_name.parts) != 1 or len(windows_name.parts) != 1:
            raise ValueError("Project name must be one filesystem path segment.")

    @property
    def root(self) -> Path:
        return self.location / self.name
