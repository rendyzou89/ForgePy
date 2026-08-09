import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from components.component_context import ComponentContext
from components.component_registry import ComponentRegistry
from components.pytest_component import PytestComponent


class PytestComponentTests(unittest.TestCase):

    def test_metadata_describes_the_pytest_component(self) -> None:
        metadata = PytestComponent().metadata

        self.assertEqual(metadata.name, "pytest")
        self.assertEqual(
            metadata.description,
            "Pytest configuration for an existing Python project.",
        )
        self.assertEqual(metadata.version, "0.1.0")
        self.assertEqual(metadata.author, "ForgePy")
        self.assertEqual(metadata.tags, ("testing", "pytest"))

    def test_manifest_declares_only_pytest_ini(self) -> None:
        manifest = PytestComponent().manifest

        self.assertEqual(manifest.files, (Path("pytest.ini"),))
        self.assertEqual(manifest.dependencies, ())
        self.assertEqual(manifest.conflicts, ())

    def test_default_registry_registers_pytest_first_deterministically(self) -> None:
        first_registry = ComponentRegistry()
        second_registry = ComponentRegistry()

        self.assertIsInstance(first_registry.get("pytest"), PytestComponent)
        self.assertEqual(first_registry.list_components()[0].name, "pytest")
        self.assertEqual(second_registry.list_components()[0].name, "pytest")

    def test_install_creates_the_declared_configuration(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)
            component = PytestComponent()

            component.install(ComponentContext(project_path))

            configuration_path = project_path / "pytest.ini"
            self.assertEqual(
                configuration_path.read_text(encoding="utf-8"),
                "[pytest]\ntestpaths = tests\n",
            )

    def test_manifest_files_match_installed_component_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)
            component = PytestComponent()

            component.install(ComponentContext(project_path))

            installed_files = tuple(
                path.relative_to(project_path)
                for path in project_path.rglob("*")
                if path.is_file()
            )
            self.assertEqual(installed_files, component.manifest.files)

    def test_install_does_not_overwrite_an_existing_target(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)
            configuration_path = project_path / "pytest.ini"
            configuration_path.write_text("user content\n", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                PytestComponent().install(ComponentContext(project_path))

            self.assertEqual(
                configuration_path.read_text(encoding="utf-8"),
                "user content\n",
            )

    def test_repeated_install_rejects_the_existing_owned_target(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)
            component = PytestComponent()
            context = ComponentContext(project_path)
            component.install(context)
            original_content = (project_path / "pytest.ini").read_bytes()

            with self.assertRaises(FileExistsError):
                component.install(context)

            self.assertEqual(
                (project_path / "pytest.ini").read_bytes(),
                original_content,
            )

    def test_install_writes_nothing_outside_the_project(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            project_path = temporary_path / "project"
            outside_path = temporary_path / "outside"
            project_path.mkdir()
            outside_path.mkdir()

            PytestComponent().install(ComponentContext(project_path))

            self.assertEqual(tuple(outside_path.iterdir()), ())
            self.assertEqual(
                tuple(path.name for path in project_path.iterdir()),
                ("pytest.ini",),
            )


if __name__ == "__main__":
    unittest.main()
