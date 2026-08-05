def build() -> str:
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