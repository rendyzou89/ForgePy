"""
==================================================
ForgePy
Author  : Rendy Zou
Module  : VSCode Launch Template
==================================================

Deskripsi:
- Template launch.json untuk Visual Studio Code.
- Menambahkan konfigurasi F5 hanya jika template memiliki entry point.
"""

import json


def build(entry_point: str | None = "app.py") -> str:

    configurations = []

    if entry_point is not None:
        configurations.append(
            {
                "name": f"Python: {entry_point}",
                "type": "debugpy",
                "request": "launch",
                "program": f"${{workspaceFolder}}/{entry_point}",
                "console": "integratedTerminal",
                "justMyCode": True,
            }
        )

    launch = {
        "version": "0.2.0",
        "configurations": configurations,
    }

    return json.dumps(
        launch,
        indent=4,
        ensure_ascii=False,
    )
