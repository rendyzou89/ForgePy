from pathlib import Path


class FileBuilder:
    """
    Bertanggung jawab membuat file beserta isinya.
    """

    def write(self, file_path: Path, content: str) -> None:
        file_path.write_text(
            content,
            encoding="utf-8"
        )

        print(f"[OK] File dibuat : {file_path}")