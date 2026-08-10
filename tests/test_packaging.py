"""Regression tests for ForgePy distribution metadata."""

import tomllib
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import main as application_entry
from components.component_registry import ComponentRegistry
from config.version import VERSION
from templates.template_engine.template_registry import TemplateRegistry


class PackagingMetadataTests(unittest.TestCase):

    project_root = Path(__file__).resolve().parents[1]
    pyproject_path = project_root / "pyproject.toml"
    manifest_path = project_root / "MANIFEST.in"
    required_packages = (
        "builders",
        "cli",
        "components",
        "config",
        "core",
        "models",
        "templates",
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.metadata = tomllib.loads(
            cls.pyproject_path.read_text(encoding="utf-8")
        )

    def test_packaging_metadata_is_parseable_and_standard(self) -> None:
        self.assertEqual(
            self.metadata["build-system"]["build-backend"],
            "setuptools.build_meta",
        )
        self.assertEqual(self.metadata["project"]["name"], "forgepy")

    def test_required_runtime_packages_are_discovered_exclusively(self) -> None:
        discovery = self.metadata["tool"]["setuptools"]["packages"]["find"]

        self.assertEqual(
            discovery["include"],
            [f"{package}*" for package in self.required_packages],
        )
        self.assertIn("tests*", discovery["exclude"])

        for package in self.required_packages:
            with self.subTest(package=package):
                self.assertTrue(
                    (self.project_root / package / "__init__.py").is_file()
                )

    def test_distribution_uses_the_canonical_application_version(self) -> None:
        project = self.metadata["project"]
        dynamic_version = self.metadata["tool"]["setuptools"]["dynamic"]

        self.assertIn("version", project["dynamic"])
        self.assertEqual(
            dynamic_version["version"]["attr"],
            "config.version.VERSION",
        )
        self.assertEqual(VERSION, "0.6.0")

    def test_console_script_delegates_to_existing_main(self) -> None:
        self.assertEqual(
            self.metadata["project"]["scripts"]["forgepy"],
            "main:main",
        )

        arguments = object()
        parser = Mock()
        parser.parse.return_value = arguments
        dispatcher = Mock()
        dispatcher.dispatch.return_value = 7

        with patch("main.Parser", return_value=parser):
            with patch("main.Dispatcher", return_value=dispatcher):
                self.assertEqual(application_entry.main(), 7)

        dispatcher.dispatch.assert_called_once_with(arguments)

    def test_built_ins_remain_available_from_packaged_modules(self) -> None:
        self.assertEqual(
            tuple(TemplateRegistry().list_templates()),
            ("basic", "library", "cli"),
        )
        self.assertEqual(
            tuple(
                component.name
                for component in ComponentRegistry().list_components()
            ),
            ("pytest", "ruff", "github-actions"),
        )

    def test_distribution_declares_no_python_runtime_dependencies(self) -> None:
        self.assertEqual(self.metadata["project"]["dependencies"], [])

    def test_sdist_manifest_excludes_only_repository_packages(self) -> None:
        directives = self.manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()

        self.assertEqual(directives, ["prune tests", "prune utils"])
        self.assertTrue((self.project_root / "main.py").is_file())
        self.assertTrue(self.pyproject_path.is_file())

        for package in self.required_packages:
            with self.subTest(package=package):
                self.assertTrue((self.project_root / package).is_dir())


if __name__ == "__main__":
    unittest.main()
