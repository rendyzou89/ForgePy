"""
==================================================
ForgePy
Library Template Files
==================================================
"""

from templates.template_manager import TemplateManager


class LibraryFiles:
    """Build the minimal file mapping for a Python library project."""

    @staticmethod
    def build(
        project_name: str,
        package_name: str,
    ) -> dict[str, str]:
        template_manager = TemplateManager()

        return {
            "README.md": template_manager.get_readme(project_name),
            ".gitignore": template_manager.get_gitignore(),
            "requirements.txt": "",
            "pyproject.toml": template_manager.get_pyproject(project_name),
            f"{package_name}/__init__.py": "",
            "tests/__init__.py": "",
        }
