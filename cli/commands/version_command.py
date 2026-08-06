"""
==================================================
ForgePy
Version : v0.7.2
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

    def execute(self, args: Namespace) -> None:
        del args

        print(f"{APP_NAME} v{VERSION}")
        print(f"Python {platform.python_version()}")