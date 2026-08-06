"""
==================================================
ForgePy
Version : v0.4.0
Author  : Rendy Zou
Module  : VSCode Settings Template
==================================================

Deskripsi:
- Template settings.json untuk Visual Studio Code.
"""

import json


def build() -> str:

    settings = {
        "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",

        "python.analysis.typeCheckingMode": "basic",

        "python.analysis.autoImportCompletions": True,

        "editor.formatOnSave": True,

        "editor.tabSize": 4,

        "files.trimTrailingWhitespace": True,

        "files.insertFinalNewline": True,
    }

    return json.dumps(
    settings,
    indent=4,
    ensure_ascii=False,
)