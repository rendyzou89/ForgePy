"""
==================================================
ForgePy
Module  : Base Command
==================================================
"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class Command(ABC):
    """
    Kontrak dasar untuk seluruh command ForgePy.
    """

    name: str = ""
    summary: str = ""
    description: str = ""

    def validate_registration(self) -> None:
        """
        Memastikan metadata command lengkap sebelum didaftarkan.
        """

        for field in (
            "name",
            "summary",
            "description",
        ):
            if not getattr(self, field):
                raise ValueError(
                    f"Command '{type(self).__name__}' harus memiliki {field}."
                )

    def configure_parser(
        self,
        parser: ArgumentParser,
    ) -> None:
        """
        Mendaftarkan argumen khusus command.

        Command tanpa argumen dapat menggunakan implementasi default.
        """
        del parser

    @abstractmethod
    def execute(self, args: Namespace) -> None:
        """
        Menjalankan command.
        """
        raise NotImplementedError
