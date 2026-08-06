"""
==================================================
ForgePy
Version : v0.7.2
Module  : CLI Parser
==================================================
"""

import argparse
from argparse import Namespace


class Parser:
    """
    Membaca command dan argumen dari terminal.
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="forgepy",
            description="ForgePy Python Project Generator",
        )

        # Default untuk mode interaktif:
        # python main.py
        self.parser.set_defaults(
            project_name=None,
            location=None,
            template="basic",
        )

        self._register_commands()

    def _register_commands(self) -> None:
        subparsers = self.parser.add_subparsers(
            dest="command",
            title="commands",
        )

        # ==========================
        # Create Command
        # ==========================

        create_parser = subparsers.add_parser(
            "create",
            help="Membuat project Python baru.",
        )

        create_parser.add_argument(
            "project_name",
            nargs="?",
            help="Nama project yang akan dibuat.",
        )

        create_parser.add_argument(
            "--location",
            "-l",
            help="Lokasi penyimpanan project.",
        )

        create_parser.add_argument(
            "--template",
            "-t",
            default="basic",
            help="Template project. Default: basic.",
        )

        # ==========================
        # Version Command
        # ==========================

        subparsers.add_parser(
            "version",
            help="Menampilkan versi ForgePy.",
        )

        # ==========================
        # List Command
        # ==========================

        subparsers.add_parser(
            "list",
            help="Menampilkan daftar template.",
        )

    def parse(self) -> Namespace:
        """
        Membaca argumen dari terminal.
        """

        return self.parser.parse_args()

    def show_help(self) -> None:
        """
        Menampilkan halaman bantuan.
        """

        self.parser.print_help()