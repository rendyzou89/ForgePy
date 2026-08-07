"""
==================================================
ForgePy
Module  : Create Command
==================================================
"""

from argparse import ArgumentParser, Namespace

from cli.command import Command
from core.project_generator import ProjectGenerator


class CreateCommand(Command):
    """
    Membuat project baru melalui ProjectGenerator.
    """

    name = "create"
    summary = "Create a new Python project."
    description = (
        "Create a Python project from a registered ForgePy template. "
        "When the project name or location is omitted, ForgePy prompts "
        "for it before starting project generation."
    )

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
                "ForgePy prompts for it when omitted."
            ),
        )

        parser.add_argument(
            "--template",
            "-t",
            default="basic",
            metavar="NAME",
            help="Registered project template to use (default: %(default)s).",
        )

    def execute(self, args: Namespace) -> None:
        project_name = getattr(
            args,
            "project_name",
            None,
        )

        if not project_name:
            project_name = input(
                "Project Name : "
            ).strip()

        location = getattr(
            args,
            "location",
            None,
        )

        if not location:
            location = input(
                "Location : "
            ).strip()

        template_name = getattr(
            args,
            "template",
            "basic",
        ) or "basic"

        if not project_name:
            print("[ERROR] Nama project tidak boleh kosong.")
            return

        if not location:
            print("[ERROR] Lokasi project tidak boleh kosong.")
            return

        generator = ProjectGenerator()

        generator.create(
            project_name=project_name,
            location=location,
            template_name=template_name,
        )
