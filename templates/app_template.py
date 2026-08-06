"""
==================================================
ForgePy
App Template
==================================================
"""


def get_app(project_name: str) -> str:
    return f'''"""
{project_name}
"""

def main():
    print("Welcome to {project_name}")


if __name__ == "__main__":
    main()
'''