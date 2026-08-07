"""
==================================================
ForgePy
Module  : CLI Parser
==================================================
"""

import argparse
from argparse import Namespace
from collections.abc import Iterable

from cli.command import Command
from cli.commands import create_commands


class Parser:
    """
    Membaca command dan argumen dari terminal.
    """

    def __init__(
        self,
        commands: Iterable[Command] | None = None,
    ) -> None:
        self.commands = tuple(
            create_commands()
            if commands is None
            else commands
        )

        self.parser = argparse.ArgumentParser(
            prog="forgepy",
            description=(
                "Create structured Python projects and prepare their "
                "development tooling with ForgePy."
            ),
            epilog=(
                "Run 'python main.py COMMAND --help' for command-specific "
                "usage from this repository."
            ),
        )

        # Default untuk mode interaktif:
        # python main.py
        self.parser.set_defaults(
            project_name=None,
            location=None,
            template=None,
        )

        self._register_commands()

    def _register_commands(self) -> None:
        subparsers = self.parser.add_subparsers(
            dest="command",
            title="commands",
            description="Available ForgePy commands",
            metavar="COMMAND",
        )

        for command in self.commands:
            command.validate_registration()

            command_parser = subparsers.add_parser(
                command.name,
                help=command.summary,
                description=command.description,
            )

            command.configure_parser(command_parser)

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
