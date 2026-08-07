"""
==================================================
ForgePy
Module  : Version Command
==================================================
"""

import platform
from argparse import Namespace

from cli.command import Command
from config.version import APP_NAME, VERSION


class VersionCommand(Command):
    """
    Menampilkan informasi versi ForgePy.
    """

    name = "version"
    summary = "Show ForgePy and Python version information."
    description = "Show the configured ForgePy version and active Python version."

    def execute(self, args: Namespace) -> None:
        del args

        print(f"{APP_NAME} v{VERSION}")
        print(f"Python {platform.python_version()}")
