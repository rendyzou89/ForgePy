from pathlib import Path

from config.default_structure import DEFAULT_FOLDERS

from builders.folder_builder import FolderBuilder
from builders.file_builder import FileBuilder

from models.project_config import ProjectConfig

from templates.template_manager import TemplateManager


def main() -> None:
    print("=" * 40)
    print(" Python Project Generator ")
    print("=" * 40)

    project_name = input("Project Name : ").strip()
    location = input("Location : ").strip()

    # Membuat konfigurasi project
    config = ProjectConfig(
        name=project_name,
        location=Path(location)
    )

    # Membuat folder utama project
    config.root.mkdir(parents=True, exist_ok=True)

    # Membuat struktur folder
    folder_builder = FolderBuilder()
    folder_builder.create(
        config.root,
        DEFAULT_FOLDERS
    )

    # Menyiapkan template
    template_manager = TemplateManager()

    # Membuat file dari template
    file_builder = FileBuilder()

    file_builder.write(
        config.root / "README.md",
        template_manager.get_readme(config.name),
    )

    file_builder.write(
        config.root / ".gitignore",
        template_manager.get_gitignore(),
    )

    file_builder.write(
        config.root / "requirements.txt",
        template_manager.get_requirements(),
    )

    file_builder.write(
        config.root / "app.py",
        template_manager.get_app(config.name),
    )

    print()
    print("=" * 40)
    print("Project berhasil dibuat.")
    print(config.root)
    print("=" * 40)


if __name__ == "__main__":
    main()