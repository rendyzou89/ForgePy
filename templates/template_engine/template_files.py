"""Compatibility facade for the original basic-template file API."""

from templates.basic.basic_files import BasicFiles


class TemplateFiles:

    @staticmethod
    def basic(project_name: str) -> dict[str, str]:
        return BasicFiles.build(project_name)
