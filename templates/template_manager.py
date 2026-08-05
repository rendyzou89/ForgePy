from templates.app_template import build as build_app
from templates.readme_template import build as build_readme
from templates.gitignore_template import build as build_gitignore
from templates.requirements_template import build as build_requirements


class TemplateManager:
    """Mengelola seluruh template project."""

    def get_app(self, project_name: str) -> str:
        return build_app(project_name)

    def get_readme(self, project_name: str) -> str:
        return build_readme(project_name)

    def get_gitignore(self) -> str:
        return build_gitignore()

    def get_requirements(self) -> str:
        return build_requirements()