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
        template_metadata = registry.list_metadata()

        print("=" * 40)
        print(" ForgePy Templates ")
        print("=" * 40)

        if not template_metadata:
            print("Belum ada template yang terdaftar.")
            return

        for metadata in template_metadata:
            print(f"- {metadata.name}: {metadata.description}")
