"""
==================================================
ForgePy
Version : v0.4.0
Author  : Rendy Zou
Module  : VSCode Launch Template
==================================================

Deskripsi:
- Template launch.json untuk Visual Studio Code.
- Digunakan agar project dapat dijalankan dengan tombol F5.
"""

import json


def build() -> str:

    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: app.py",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/app.py",
                "console": "integratedTerminal",
                "justMyCode": True,
            }
        ],
    }

    return json.dumps(
        launch,
        indent=4,
        ensure_ascii=False,
    )