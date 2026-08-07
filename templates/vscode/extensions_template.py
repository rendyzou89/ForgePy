"""
==================================================
ForgePy
Author  : Rendy Zou
Module  : VSCode Extensions Template
==================================================

Deskripsi:
- Merekomendasikan extension Visual Studio Code.
"""

import json


def build() -> str:

    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.debugpy",
            "ms-python.vscode-pylance",
            "ms-python.black-formatter",
            "charliermarsh.ruff",
            "eamodio.gitlens"
        ]
    }

    return json.dumps(
        extensions,
        indent=4,
        ensure_ascii=False,
    )
