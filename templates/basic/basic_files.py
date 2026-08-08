"""Generated file mapping owned by the basic template."""

from templates.template_manager import TemplateManager


class BasicFiles:
    """Build the established basic-template file mapping."""

    @staticmethod
    def build(project_name: str) -> dict[str, str]:
        template_manager = TemplateManager()

        return {
            "README.md": template_manager.get_readme(project_name),
            ".gitignore": template_manager.get_gitignore(),
            "requirements.txt": template_manager.get_requirements(),
            "app.py": template_manager.get_app(project_name),
            "LICENSE": template_manager.get_license(),
            "CHANGELOG.md": template_manager.get_changelog(),
            ".env": template_manager.get_env(),
            ".env.example": template_manager.get_env_example(),
            "pyproject.toml": template_manager.get_pyproject(project_name),
        }
