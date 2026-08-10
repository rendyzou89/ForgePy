"""Shared execution for templates backed by folders and file mappings."""

from abc import abstractmethod
from pathlib import Path
from typing import ClassVar

from builders.file_builder import FileBuilder
from builders.folder_builder import FolderBuilder
from templates.template_engine.base_template import BaseTemplate
from templates.template_engine.template_context import TemplateContext
from templates.template_engine.template_metadata import TemplateMetadata


class FileTemplate(BaseTemplate):
    """Write template-owned folders and files from focused subclass hooks."""

    _METADATA: ClassVar[TemplateMetadata]
    _DEFAULT_VSCODE_ENTRY_POINT: ClassVar[str | None]

    def __init__(self) -> None:
        self._vscode_entry_point: str | None = (
            self._DEFAULT_VSCODE_ENTRY_POINT
        )

    @property
    def metadata(self) -> TemplateMetadata:
        return self._METADATA

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def vscode_entry_point(self) -> str | None:
        return self._vscode_entry_point

    def preflight(self, project_path: Path) -> None:
        """Build context to validate template-specific inputs."""

        self._build_context(project_path)

    def create(self, project_path: Path) -> None:
        context = self._build_context(project_path)

        FolderBuilder().create(
            context.project_path,
            list(self._folders(context)),
        )

        file_builder = FileBuilder()

        for filename, content in self._files(context).items():
            file_builder.write(
                context.project_path / filename,
                content,
            )

        self._vscode_entry_point = self._vscode_entry_point_for(context)

    def _build_context(self, project_path: Path) -> TemplateContext:
        return TemplateContext(project_path=project_path)

    @abstractmethod
    def _folders(self, context: TemplateContext) -> tuple[str, ...]:
        """Return template-owned folders in creation order."""

    @abstractmethod
    def _files(self, context: TemplateContext) -> dict[str, str]:
        """Return template-owned file content in write order."""

    def _vscode_entry_point_for(
        self,
        context: TemplateContext,
    ) -> str | None:
        del context
        return self._DEFAULT_VSCODE_ENTRY_POINT
