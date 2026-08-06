"""
==================================================
ForgePy
PyProject Template
==================================================
"""


def get_pyproject(project_name: str) -> str:
    return f"""[project]
name = "{project_name}"
version = "0.1.0"
description = ""
requires-python = ">=3.12"
"""