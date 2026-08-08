"""Built-in pytest project-support component."""

from pathlib import Path

from components.base_component import BaseComponent
from components.component_context import ComponentContext
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata


class PytestComponent(BaseComponent):
    """Add an isolated pytest configuration to an existing project."""

    _METADATA = ComponentMetadata(
        name="pytest",
        description="Pytest configuration for an existing Python project.",
        version="0.1.0",
        author="ForgePy",
        tags=("testing", "pytest"),
    )
    _MANIFEST = ComponentManifest(files=(Path("pytest.ini"),))
    _CONFIGURATION = "[pytest]\ntestpaths = tests\n"

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
