"""Contract tests for ForgePy repository-level continuous integration."""

import re
import unittest
from pathlib import Path


class RepositoryCIContractTests(unittest.TestCase):

    project_root = Path(__file__).resolve().parents[1]
    workflow_path = project_root / ".github" / "workflows" / "ci.yml"

    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = cls.workflow_path.read_text(encoding="utf-8")

    def test_repository_workflow_exists_with_master_triggers(self) -> None:
        self.assertTrue(self.workflow_path.is_file())
        self.assertRegex(
            self.workflow,
            re.compile(r"push:\s+branches:\s+- master", re.MULTILINE),
        )
        self.assertRegex(
            self.workflow,
            re.compile(
                r"pull_request:\s+branches:\s+- master",
                re.MULTILINE,
            ),
        )

    def test_workflow_uses_the_windows_cpython_matrix(self) -> None:
        self.assertIn("runs-on: windows-latest", self.workflow)
        self.assertIn("uses: actions/checkout@v5", self.workflow)
        self.assertIn("uses: actions/setup-python@v6", self.workflow)
        for python_version in ("3.12", "3.13", "3.14"):
            with self.subTest(python_version=python_version):
                self.assertIn(f'- "{python_version}"', self.workflow)

    def test_every_matrix_entry_runs_required_validation(self) -> None:
        required_commands = (
            "python -m unittest discover -s tests -v",
            "python -m compileall -q components cli templates core config "
            "builders models tests",
            "python -m unittest tests.test_packaging -v",
        )

        for command in required_commands:
            with self.subTest(command=command):
                self.assertIn(command, self.workflow)

    def test_python_312_builds_and_inspects_distributions(self) -> None:
        self.assertGreaterEqual(
            self.workflow.count("if: matrix.python-version == '3.12'"),
            3,
        )
        self.assertIn("python -m build", self.workflow)
        self.assertIn("zipfile.ZipFile", self.workflow)
        self.assertIn("tarfile.open", self.workflow)
        self.assertIn('metadata["Version"] == VERSION', self.workflow)
        self.assertIn("forgepy = main:main", self.workflow)
        self.assertIn('assert "tests" not in wheel_roots', self.workflow)
        self.assertIn('assert "pyproject.toml" in relative_names', self.workflow)
        self.assertIn('assert "utils" not in sdist_roots', self.workflow)

    def test_python_312_installs_wheel_and_runs_installed_cli(self) -> None:
        self.assertIn("python -m venv $validationRoot", self.workflow)
        self.assertIn("pip install $wheel.FullName --no-deps", self.workflow)
        self.assertIn("Push-Location $env:RUNNER_TEMP", self.workflow)
        for command in (
            "& $forgepy --help",
            "& $forgepy version",
            "& $forgepy list",
            "& $forgepy component list",
        ):
            with self.subTest(command=command):
                self.assertIn(command, self.workflow)


if __name__ == "__main__":
    unittest.main()
