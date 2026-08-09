"""Built-in GitHub Actions CI component."""

from pathlib import Path

from components.base_component import BaseComponent
from components.component_context import ComponentContext
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata


class GitHubActionsComponent(BaseComponent):
    """Add a minimal Python CI workflow to an existing project."""

    _METADATA = ComponentMetadata(
        name="github-actions",
        description="GitHub Actions CI for an existing Python project.",
        version="0.1.0",
        author="ForgePy",
        tags=("ci", "github-actions", "python"),
    )
    _MANIFEST = ComponentManifest(
        files=(Path(".github/workflows/ci.yml"),),
    )
    _WORKFLOW = (
        "name: CI\n"
        "\n"
        "on:\n"
        "  push:\n"
        "  pull_request:\n"
        "\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-python@v5\n"
        "        with:\n"
        '          python-version: "3.12"\n'
        "      - name: Install CI tools\n"
        "        run: python -m pip install pytest ruff\n"
        "      - name: Run Ruff\n"
        "        run: ruff check .\n"
        "      - name: Run pytest\n"
        "        run: pytest\n"
    )

    @property
    def name(self) -> str:
        return self._METADATA.name

    @property
    def metadata(self) -> ComponentMetadata:
        return self._METADATA

    @property
    def manifest(self) -> ComponentManifest:
        return self._MANIFEST

    def install(self, context: ComponentContext) -> None:
        target_path = context.project_path / self._MANIFEST.files[0]
        project_root = context.project_path.resolve()
        resolved_target = target_path.resolve(strict=False)

        try:
            resolved_target.relative_to(project_root)
        except ValueError as error:
            raise OSError(
                "GitHub Actions workflow target resolves outside the "
                f"project: '{resolved_target}'."
            ) from error

        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open("x", encoding="utf-8", newline="\n") as file:
            file.write(self._WORKFLOW)
