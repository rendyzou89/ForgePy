import subprocess
from pathlib import Path


class RequirementsInstaller:
    """
    Menginstal package dari requirements.txt
    menggunakan virtual environment yang baru dibuat.
    """

    def install(self, project_path: Path) -> None:

        requirements = project_path / "requirements.txt"

        if not requirements.exists():
            print("[WARNING] requirements.txt tidak ditemukan.")
            return

        # Jika requirements.txt kosong
        if requirements.read_text(encoding="utf-8").strip() == "":
            print("[INFO] requirements.txt kosong, tidak ada dependency yang di-install.")
            return

        pip = project_path / ".venv" / "Scripts" / "pip.exe"

        if not pip.exists():
            print("[WARNING] Virtual Environment belum tersedia.")
            return

        print("\n[INFO] Menginstal dependencies...")

        subprocess.run(
            [
                str(pip),
                "install",
                "-r",
                str(requirements),
            ],
            check=True,
        )

        print("[OK] Dependencies berhasil di-install.")