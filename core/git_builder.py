"""
==================================================
ForgePy
Author  : Rendy Zou
Module  : Git Builder
==================================================

Deskripsi:
- Menginisialisasi Git Repository.
- Membuat commit pertama.
"""

import shutil
import subprocess
from pathlib import Path


class GitBuilder:
    """
    Builder untuk menginisialisasi Git Repository.
    """

    def create(self, project_root: Path) -> None:

        if shutil.which("git") is None:
            print("[WARNING] Git tidak ditemukan.")
            return

        if (project_root / ".git").exists():
            print("[INFO] Git Repository sudah ada.")
            return

        print("\n[INFO] Inisialisasi Git Repository...")

        subprocess.run(
            ["git", "init"],
            cwd=project_root,
            check=True,
        )

        subprocess.run(
            ["git", "add", "."],
            cwd=project_root,
            check=True,
        )

        try:

            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "Initial project created by ForgePy",
                ],
                cwd=project_root,
                check=True,
            )

            print("[OK] Initial Commit berhasil dibuat.")

        except subprocess.CalledProcessError:

            print(
                "[WARNING] Initial Commit gagal.\n"
                "Pastikan Git user.name dan user.email sudah dikonfigurasi."
            )

        print("[OK] Git Repository berhasil dibuat.")
