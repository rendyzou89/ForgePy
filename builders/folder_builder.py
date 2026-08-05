from pathlib import Path


class FolderBuilder:
    """
    Bertanggung jawab membuat struktur folder project.
    """

    def create(self, base_path: Path, folders: list[str]) -> None:
        """
        Membuat semua folder yang diberikan.

        Parameters
        ----------
        base_path : Path
            Folder utama project.

        folders : list[str]
            Daftar nama folder.
        """

        for folder in folders:
            path = base_path / folder
            path.mkdir(parents=True, exist_ok=True)

            print(f"[OK] Folder dibuat : {path}")