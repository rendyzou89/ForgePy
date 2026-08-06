"""
==================================================
ForgePy
Version : v0.7.2
Module  : Create Command
==================================================
"""

from argparse import Namespace

from cli.command import Command
from core.project_generator import ProjectGenerator


class CreateCommand(Command):
    """
    Membuat project baru melalui ProjectGenerator.
    """

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