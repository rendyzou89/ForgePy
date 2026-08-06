"""
==================================================
ForgePy
GitIgnore Template
==================================================
"""

def get_gitignore() -> str:
    return """__pycache__/
*.pyc
*.pyo
*.pyd

.venv/
venv/

.vscode/

.env

.idea/

dist/
build/

*.log
"""