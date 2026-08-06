"""
==================================================
ForgePy
Version : v0.7.2
Module  : Base Command
==================================================
"""

from abc import ABC, abstractmethod
from argparse import Namespace


class Command(ABC):
    """
    Kontrak dasar untuk seluruh command ForgePy.
    """

    @abstractmethod
    def execute(self, args: Namespace) -> None:
        """
        Menjalankan command.
        """
        raise NotImplementedError