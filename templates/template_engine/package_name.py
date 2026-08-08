import keyword
import re


def normalize_package_name(
    project_name: str,
    *,
    package_label: str,
) -> str:
    """Return a stable ASCII Python package name for a project."""

    package_name = re.sub(
        r"[^a-z0-9_]+",
        "_",
        project_name.lower(),
    ).strip("_")

    if not package_name:
        raise ValueError(
            "Project name must contain letters or digits for the "
            f"{package_label} package."
        )

    if package_name[0].isdigit():
        package_name = f"_{package_name}"

    if keyword.iskeyword(package_name):
        package_name = f"{package_name}_"

    return package_name
