"""
==================================================
ForgePy
Module  : List Command
==================================================
"""

from argparse import Namespace

from cli.command import Command
from templates.template_engine.template_registry import TemplateRegistry


class ListCommand(Command):
    """
    Menampilkan seluruh template yang tersedia.
    """

    name = "list"
    summary = "List registered project templates."
    description = "List every project template currently registered in ForgePy."

    def execute(self, args: Namespace) -> None:
        del args

        registry = TemplateRegistry()
        templates = registry.list_templates()

        print("=" * 40)
        print(" ForgePy Templates ")
        print("=" * 40)

        if not templates:
            print("Belum ada template yang terdaftar.")
            return

        for key, template in templates.items():
            print(f"- {key}: {template.name}")
