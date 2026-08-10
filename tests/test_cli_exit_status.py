"""Subprocess-level tests for ForgePy CLI exit-status behavior."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliExitStatusTests(unittest.TestCase):

    project_root = Path(__file__).resolve().parents[1]
    main_path = project_root / "main.py"

    def test_successful_commands_exit_zero(self) -> None:
        for arguments in (
            ("version",),
            ("list",),
            ("component", "list"),
        ):
            with self.subTest(arguments=arguments):
                result = self._run(*arguments)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_create_failures_exit_one_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)
            existing = location / "Existing"
            existing.mkdir()

            cases = (
                (
                    ("create", "nested/project", "-l", str(location),
                     "-t", "basic"),
                    "Project creation failed",
                ),
                (
                    ("create", "Existing", "-l", str(location),
                     "-t", "basic"),
                    "already exists",
                ),
                (
                    ("create", "Unknown", "-l", str(location),
                     "-t", "unknown"),
                    "Unknown project template",
                ),
                (
                    ("create", "___", "-l", str(location),
                     "-t", "library"),
                    "Project creation failed",
                ),
                (
                    ("create", "MissingLocation", "-l",
                     str(location / "missing"), "-t", "basic"),
                    "Project location does not exist",
                ),
            )

            for arguments, expected_text in cases:
                with self.subTest(arguments=arguments):
                    result = self._run(*arguments)

                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("[ERROR]", result.stdout)
                    self.assertIn(expected_text, result.stdout)
                    self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_config_and_component_failures_exit_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            missing_project = temporary_path / "missing"
            cases = (
                (
                    ("config", "set", "unsupported", "value"),
                    "Unknown ForgePy configuration setting",
                ),
                (
                    ("component", "installed", "--project",
                     str(missing_project)),
                    "Invalid project path",
                ),
                (
                    ("component", "add", "unknown", "--project",
                     str(temporary_path)),
                    "Unknown ForgePy component",
                ),
            )

            for arguments, expected_text in cases:
                with self.subTest(arguments=arguments):
                    result = self._run(*arguments, home=temporary_path)

                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(expected_text, result.stdout)
                    self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_argparse_failures_preserve_exit_two(self) -> None:
        for arguments in (
            ("unknown-command",),
            ("component", "add", "pytest"),
        ):
            with self.subTest(arguments=arguments):
                result = self._run(*arguments)

                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def _run(
        self,
        *arguments: str,
        home: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()

        if home is not None:
            environment["HOME"] = str(home)
            environment["USERPROFILE"] = str(home)

        return subprocess.run(
            [sys.executable, str(self.main_path), *arguments],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            env=environment,
            timeout=20,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
