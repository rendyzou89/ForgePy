"""
==================================================
ForgePy
Module  : CLI Dispatcher
==================================================
"""

from argparse import Namespace
from collections.abc import Iterable

from cli.command import Command
from cli.commands import DEFAULT_COMMAND, create_commands


class Dispatcher:
    """
    Meneruskan argumen CLI ke command yang sesuai.
    """

    def __init__(
        self,
        commands: Iterable[Command] | None = None,
    ) -> None:
        registered_commands = tuple(
            create_commands()
            if commands is None
            else commands
        )

        for command in registered_commands:
            command.validate_registration()

        self.commands: dict[str, Command] = {
            command.name: command
            for command in registered_commands
        }

        if len(self.commands) != len(registered_commands):
            raise ValueError("Nama command harus unik.")

        if DEFAULT_COMMAND not in self.commands:
            raise ValueError(
                f"Default command '{DEFAULT_COMMAND}' belum terdaftar."
            )

    def dispatch(self, args: Namespace) -> None:
        # Menjaga kompatibilitas:
        # `python main.py` langsung membuka wizard create.
        command_name = getattr(
            args,
            "command",
            None,
        ) or DEFAULT_COMMAND

        command = self.commands.get(command_name)

        if command is None:
            print(f"[ERROR] Command tidak dikenal: {command_name}")
            return

        command.execute(args)
