"""Built-in Ruff project-support component."""

from pathlib import Path

from components.base_component import BaseComponent
from components.component_context import ComponentContext
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata


class RuffComponent(BaseComponent):
    """Add an isolated Ruff configuration to an existing project."""

    _METADATA = ComponentMetadata(
        name="ruff",
        description="Ruff configuration for an existing Python project.",
        version="0.1.0",
        author="ForgePy",
        tags=("linting", "ruff"),
    )
    _MANIFEST = ComponentManifest(files=(Path("ruff.toml"),))
    _CONFIGURATION = 'line-length = 88\ntarget-version = "py312"\n'

    @property
    def name(self) -> str:
        return self._METADATA.name

    @property
    def metadata(self) -> ComponentMetadata:
        return self._METADATA

    @property
    def manifest(self) -> ComponentManifest:
        return self._MANIFEST

    def install(self, context: ComponentContext) -> None:
        target_path = context.project_path / self._MANIFEST.files[0]

        with target_path.open("x", encoding="utf-8", newline="\n") as file:
            file.write(self._CONFIGURATION)
