"""
==================================================
ForgePy
Module  : Create Command
==================================================
"""

import subprocess
from argparse import ArgumentParser, Namespace

from cli.command import Command
from config.user_config import ConfigStore, ForgePyConfigError
from core.project_generator import (
    ProjectGenerator,
    ProjectPreflightError,
    UnknownProjectTemplateError,
)


class CreateCommand(Command):
    """
    Membuat project baru melalui ProjectGenerator.
    """

    name = "create"
    summary = "Create a new Python project."
    description = (
        "Create a Python project from a registered ForgePy template. "
        "ForgePy prompts for an omitted project name and resolves omitted "
        "location or template values from user configuration before using "
        "the existing interactive or basic fallback."
    )

    def __init__(
        self,
        store: ConfigStore | None = None,
    ) -> None:
        self._store = store

    def configure_parser(
        self,
        parser: ArgumentParser,
    ) -> None:
        parser.add_argument(
            "project_name",
            nargs="?",
            metavar="PROJECT_NAME",
            help=(
                "Name of the project to create. "
                "ForgePy prompts for it when omitted."
            ),
        )

        parser.add_argument(
            "--location",
            "-l",
            metavar="PATH",
            help=(
                "Existing parent directory for the new project. "
                "When omitted, ForgePy uses configured default_location "
                "before prompting."
            ),
        )

        parser.add_argument(
            "--template",
            "-t",
            metavar="NAME",
            help=(
                "Registered project template to use. When omitted, "
                "ForgePy uses configured default_template, then basic."
            ),
        )

    def execute(self, args: Namespace) -> int:
        location = getattr(
            args,
            "location",
            None,
        )
        template_name = getattr(
            args,
            "template",
            None,
        )

        user_config: dict[str, str] = {}

        if location is None or template_name is None:
            try:
                user_config = self._get_store().load()
            except ForgePyConfigError as error:
                print(f"[ERROR] {error}")
                print(
                    "[INFO] Run 'python main.py config reset' or supply "
                    "both --location and --template explicitly."
                )
                return 1

        project_name = getattr(
            args,
            "project_name",
            None,
        )

        if not project_name:
            project_name = input(
                "Project Name : "
            ).strip()

        if location is None:
            location = user_config[
                "default_location"
            ]

        if not location:
            location = input(
                "Location : "
            ).strip()

        if template_name is None:
            template_name = user_config[
                "default_template"
            ]

        template_name = template_name or "basic"

        if not project_name:
            print("[ERROR] Nama project tidak boleh kosong.")
            return 1

        if not location:
            print("[ERROR] Lokasi project tidak boleh kosong.")
            return 1

        generator = ProjectGenerator()

        try:
            generator.create(
                project_name=project_name,
                location=location,
                template_name=template_name,
            )
        except UnknownProjectTemplateError:
            print(f"[ERROR] Unknown project template: '{template_name}'.")
            return 1
        except (
            ProjectPreflightError,
            OSError,
            subprocess.SubprocessError,
        ) as error:
            print(f"[ERROR] Project creation failed: {error}")
            return 1

        return 0

    def _get_store(self) -> ConfigStore:
        if self._store is None:
            self._store = ConfigStore()

        return self._store
