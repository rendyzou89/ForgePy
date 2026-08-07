"""
==================================================
ForgePy
Library Template
==================================================
"""

import keyword
import re
from pathlib import Path

from builders.file_builder import FileBuilder
from builders.folder_builder import FolderBuilder
from templates.library.library_files import LibraryFiles
from templates.template_engine.base_template import BaseTemplate
from templates.template_engine.template_metadata import TemplateMetadata


class LibraryTemplate(BaseTemplate):
    """Generate a minimal reusable Python package project."""

    _METADATA = TemplateMetadata(
        name="library",
        description="Reusable Python package template.",
        version="0.1.0",
        author="Rendy Zou",
        tags=("python", "library", "package"),
    )

    @property
    def metadata(self) -> TemplateMetadata:
        return self._METADATA

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def vscode_entry_point(self) -> str | None:
        return None

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
        files = LibraryFiles.build(
            project_name=project_path.name,
            package_name=package_name,
        )

        for filename, content in files.items():
            file_builder.write(
                project_path / filename,
                content,
            )

    @staticmethod
    def _normalize_package_name(project_name: str) -> str:
        package_name = re.sub(
            r"[^a-z0-9_]+",
            "_",
            project_name.lower(),
        ).strip("_")

        if not package_name:
            raise ValueError(
                "Project name must contain letters or digits for the "
                "library package."
            )

        if package_name[0].isdigit():
            package_name = f"_{package_name}"

        if keyword.iskeyword(package_name):
            package_name = f"{package_name}_"

        return package_name
