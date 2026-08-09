import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from cli.commands import create_commands
from cli.dispatcher import Dispatcher
from cli.parser import Parser
from config.version import VERSION


class ComponentCommandTests(unittest.TestCase):

    def test_component_help_lists_supported_actions(self) -> None:
        output = StringIO()

        with patch("sys.argv", ["forgepy", "component", "--help"]):
            with redirect_stdout(output):
                with self.assertRaises(SystemExit) as context:
                    Parser().parse()

        self.assertEqual(context.exception.code, 0)
        self.assertIn("list", output.getvalue())
        self.assertIn("add", output.getvalue())

    def test_component_list_displays_name_and_description(self) -> None:
        output = self._run_cli("component", "list")

        self.assertIn("ForgePy Components", output)
        self.assertIn("pytest", output)
        self.assertIn(
            "Pytest configuration for an existing Python project.",
            output,
        )

    def test_component_add_installs_pytest_into_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory) / "project"
            project_path.mkdir()

            output = self._run_cli(
                "component",
                "add",
                "pytest",
                "--project",
                str(project_path),
            )

            self.assertIn("[OK] Component 'pytest' added", output)
            self.assertEqual(
                (project_path / "pytest.ini").read_text(encoding="utf-8"),
                "[pytest]\ntestpaths = tests\n",
            )

    def test_component_add_rejects_unknown_component(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = self._run_cli(
                "component",
                "add",
                "unknown",
                "--project",
                temporary_directory,
            )

        self.assertIn("[ERROR] Unknown ForgePy component: 'unknown'.", output)
        self.assertNotIn("Traceback", output)

    def test_component_add_rejects_invalid_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory) / "missing"
            output = self._run_cli(
                "component",
                "add",
                "pytest",
                "--project",
                str(missing_path),
            )

        self.assertIn("[ERROR] Invalid project path", output)
        self.assertIn("must exist", output)
        self.assertNotIn("Traceback", output)

    def test_component_add_refuses_existing_pytest_ini(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)
            target_path = project_path / "pytest.ini"
            target_path.write_text("existing\n", encoding="utf-8")

            output = self._run_cli(
                "component",
                "add",
                "pytest",
                "--project",
                str(project_path),
            )

            self.assertIn("[ERROR] Component installation refused", output)
            self.assertIn("already exists", output)
            self.assertEqual(
                target_path.read_text(encoding="utf-8"),
                "existing\n",
            )

    def test_component_add_writes_nothing_outside_supplied_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            project_path = root_path / "project"
            outside_path = root_path / "outside"
            project_path.mkdir()
            outside_path.mkdir()

            self._run_cli(
                "component",
                "add",
                "pytest",
                "--project",
                str(project_path),
            )

            self.assertEqual(tuple(outside_path.iterdir()), ())
            self.assertEqual(
                tuple(path.name for path in project_path.iterdir()),
                ("pytest.ini",),
            )

    def test_existing_cli_commands_remain_registered(self) -> None:
        command_names = tuple(command.name for command in create_commands())

        self.assertEqual(
            command_names,
            ("create", "version", "list", "config", "component"),
        )

    def test_forgepy_version_remains_unchanged(self) -> None:
        self.assertEqual(VERSION, "0.6.0")

    @staticmethod
    def _run_cli(*arguments: str) -> str:
        output = StringIO()

        with patch("sys.argv", ["forgepy", *arguments]):
            with redirect_stdout(output):
                args = Parser().parse()
                Dispatcher().dispatch(args)

        return output.getvalue()


if __name__ == "__main__":
    unittest.main()
