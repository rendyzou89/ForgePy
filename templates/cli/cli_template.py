from pathlib import Path

from builders.file_builder import FileBuilder
from builders.folder_builder import FolderBuilder
from templates.cli.cli_files import CliFiles
from templates.template_engine.base_template import BaseTemplate
from templates.template_engine.package_name import normalize_package_name
from templates.template_engine.template_metadata import TemplateMetadata


class CliTemplate(BaseTemplate):
    """Generate a minimal standard-library command-line application."""

    _METADATA = TemplateMetadata(
        name="cli",
        description="Minimal command-line application template.",
        version="0.1.0",
        author="Rendy Zou",
        tags=("python", "cli", "argparse"),
    )

    def __init__(self) -> None:
        self._vscode_entry_point: str | None = None

    @property
    def metadata(self) -> TemplateMetadata:
        return self._METADATA

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def vscode_entry_point(self) -> str | None:
        return self._vscode_entry_point

    def create(
        self,
        project_path: Path,
    ) -> None:
        package_name = self._normalize_package_name(
            project_path.name,
        )

        FolderBuilder().create(
            project_path,
            [
                package_name,
                "tests",
            ],
        )

        file_builder = FileBuilder()
        files = CliFiles.build(
            project_name=project_path.name,
            package_name=package_name,
        )

        for filename, content in files.items():
            file_builder.write(
                project_path / filename,
                content,
            )

        self._vscode_entry_point = f"{package_name}/cli.py"

    @staticmethod
    def _normalize_package_name(project_name: str) -> str:
        return normalize_package_name(
            project_name,
            package_label="CLI",
        )
