"""
==================================================
ForgePy
Author  : Rendy Zou
Module  : VSCode Tasks Template
==================================================

Deskripsi:
- Template tasks.json untuk Visual Studio Code.
- Menyediakan task aplikasi jika tersedia dan install dependencies.
"""

import json


def build(entry_point: str | None = "app.py") -> str:

    tasks = []

    if entry_point is not None:
        tasks.append(
            {
                "label": "Run Application",
                "type": "shell",
                "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
                "args": [
                    entry_point
                ],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "reveal": "always"
                },
                "problemMatcher": []
            }
        )

    tasks.append(
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
    )

    task_configuration = {
        "version": "2.0.0",
        "tasks": tasks,
    }

    return json.dumps(
        task_configuration,
        indent=4,
        ensure_ascii=False,
    )
