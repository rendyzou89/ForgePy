"""
==================================================
ForgePy
Module  : File Builder
==================================================
"""

from pathlib import Path

from builders.base_builder import BaseBuilder


class FileBuilder(BaseBuilder):

    def write(
        self,
        path: Path,
        content: str,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"[OK] File dibuat : {path}")
