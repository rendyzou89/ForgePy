"""
==================================================
ForgePy
Version : v0.7.2
Module  : CLI Dispatcher
==================================================
"""

from argparse import Namespace

from cli.command import Command
from cli.commands.create_command import CreateCommand
from cli.commands.list_command import ListCommand
from cli.commands.version_command import VersionCommand


class Dispatcher:
    """
    Meneruskan argumen CLI ke command yang sesuai.
    """

    def __init__(self) -> None:
        self.commands: dict[str, Command] = {
            "create": CreateCommand(),
            "list": ListCommand(),
            "version": VersionCommand(),
        }

    def dispatch(self, args: Namespace) -> None:
        # Menjaga kompatibilitas:
        # `python main.py` langsung membuka wizard create.
        command_name = args.command or "create"

        command = self.commands.get(command_name)

        if command is None:
            print(f"[ERROR] Command tidak dikenal: {command_name}")
            return

        command.execute(args)