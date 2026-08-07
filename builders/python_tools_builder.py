"""
==================================================
ForgePy
Module  : Python Tools Builder
==================================================
"""

import subprocess
from pathlib import Path

from builders.base_builder import BaseBuilder


class PythonToolsBuilder(BaseBuilder):
    """
    Mengupdate pip, setuptools, dan wheel
    pada Virtual Environment.
    """

    def update(
        self,
        project_path: Path,
    ) -> None:

        python = project_path / ".venv" / "Scripts" / "python.exe"

        if not python.exists():
            print("[WARNING] Virtual Environment belum tersedia.")
            return

        packages = [
            "pip",
            "setuptools",
            "wheel",
        ]

        for package in packages:

            print(f"[INFO] Mengupdate {package}...")

            subprocess.run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    package,
                ],
                check=True,
            )

            print(f"[OK] {package} berhasil diupdate.")
