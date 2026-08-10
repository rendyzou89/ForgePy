import subprocess
from pathlib import Path


REQUIREMENTS_INSTALL_TIMEOUT_SECONDS = 900


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

        try:
            subprocess.run(
                [
                    str(pip),
                    "install",
                    "-r",
                    str(requirements),
                ],
                check=True,
                timeout=REQUIREMENTS_INSTALL_TIMEOUT_SECONDS,
            )
        except subprocess.SubprocessError as error:
            print(f"[ERROR] Requirements installation failed: {error}")
            raise

        print("[OK] Dependencies berhasil di-install.")
