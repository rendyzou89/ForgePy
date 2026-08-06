"""
==================================================
ForgePy
Template Files
==================================================
"""

from templates.template_manager import TemplateManager


class TemplateFiles:

    @staticmethod
    def basic(project_name: str) -> dict[str, str]:

        tm = TemplateManager()

        return {

            "README.md":
                tm.get_readme(project_name),

            ".gitignore":
                tm.get_gitignore(),

            "requirements.txt":
                tm.get_requirements(),

            "app.py":
                tm.get_app(project_name),

            "LICENSE":
                tm.get_license(),

            "CHANGELOG.md":
                tm.get_changelog(),

            ".env":
                tm.get_env(),

            ".env.example":
                tm.get_env_example(),

            "pyproject.toml":
                tm.get_pyproject(project_name),

        }