"""
==================================================
ForgePy
Version : v0.4.0
Author  : Rendy Zou
Module  : VSCode Tasks Template
==================================================

Deskripsi:
- Template tasks.json untuk Visual Studio Code.
- Menyediakan task menjalankan aplikasi dan install dependencies.
"""

import json


def build() -> str:

    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Application",
                "type": "shell",
                "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
                "args": [
                    "app.py"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "reveal": "always"
                },
                "problemMatcher": []
            },
            {
                "label": "Install Requirements",
                "type": "shell",
                "command": "${workspaceFolder}\\.venv\\Scripts\\pip.exe",
                "args": [
                    "install",
                    "-r",
                    "requirements.txt"
                ],
                "presentation": {
                    "reveal": "always"
                },
                "problemMatcher": []
            }
        ]
    }

    return json.dumps(
        tasks,
        indent=4,
        ensure_ascii=False,
    )