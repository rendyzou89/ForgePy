"""
==================================================
ForgePy
Basic Template
==================================================
"""

from pathlib import Path

from builders.file_builder import FileBuilder
from builders.folder_builder import FolderBuilder

from config.default_structure import DEFAULT_FOLDERS

from templates.template_engine.base_template import BaseTemplate
from templates.template_engine.template_files import TemplateFiles


class BasicTemplate(BaseTemplate):

    @property
    def name(self) -> str:
        return "basic"

    def create(
        self,
        project_path: Path,
    ) -> None:

        FolderBuilder().create(
            project_path,
            DEFAULT_FOLDERS,
        )

        fb = FileBuilder()

        files = TemplateFiles.basic(
            project_path.name,
        )

        for filename, content in files.items():

            fb.write(
                project_path / filename,
                content,
            )