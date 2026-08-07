"""
==================================================
ForgePy
Module  : Folder Builder
==================================================
"""

from pathlib import Path

from builders.base_builder import BaseBuilder


class FolderBuilder(BaseBuilder):

    def create(
        self,
        root: Path,
        folders: list[str],
    ) -> None:

        for folder in folders:

            path = root / folder

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

            print(f"[OK] Folder dibuat : {path}")
