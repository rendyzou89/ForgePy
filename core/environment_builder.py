import subprocess
import sys
from pathlib import Path


class EnvironmentBuilder:
    """
    Membuat Virtual Environment Python.
    """

    def create(self, project_path: Path) -> None:

        print("\n[INFO] Membuat Virtual Environment...")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(project_path / ".venv")
            ],
            check=True,
        )

        print("[OK] Virtual Environment berhasil dibuat.")