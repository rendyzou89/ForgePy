"""Per-generation data used by file-based templates."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TemplateContext:
    """Keep project and optional package names together during generation."""

    project_path: Path
    package_name: str | None = None

    @property
    def project_name(self) -> str:
        return self.project_path.name

    def require_package_name(self) -> str:
        """Return the package name for package-oriented templates."""

        if self.package_name is None:
            raise ValueError("Template context does not define a package name.")

        return self.package_name
