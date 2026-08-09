"""Project destination validation and filesystem-safety tests."""

import os
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from core.project_generator import ProjectGenerator
from models.project_config import ProjectConfig


class ProjectNameContractTests(unittest.TestCase):
    """Verify names used as destination path segments."""

    def test_valid_project_name_constructs_one_direct_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory).resolve()
            config = ProjectConfig(name="Demo Project", location=location)

            self.assertEqual(config.root, location / "Demo Project")
            self.assertEqual(config.root.parent, location)

    def test_rejects_unsafe_project_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)
            absolute_name = str((location / "absolute").resolve())
            cases = (
                "",
                ".",
                "..",
                "group/project",
                "group\\project",
                absolute_name,
                "C:project",
            )

            for project_name in cases:
                with self.subTest(project_name=project_name):
                    with self.assertRaises(ValueError):
                        ProjectConfig(
                            name=project_name,
                            location=location,
                        )


class ProjectDestinationSafetyTests(unittest.TestCase):
    """Verify generation rejects unsafe destinations before writes."""

    def test_invalid_name_does_not_create_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)

            with patch(
                "core.project_generator.TemplateRegistry"
            ) as registry:
                with self.assertRaises(ValueError):
                    ProjectGenerator().create(
                        project_name="nested/project",
                        location=str(location),
                        template_name="unknown",
                    )

            self.assertEqual(tuple(location.iterdir()), ())
            registry.assert_not_called()

    def test_existing_directory_and_contents_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)
            destination = location / "Existing"
            destination.mkdir()
            existing_file = destination / "data.bin"
            original_content = b"\x00existing\xffcontent"
            existing_file.write_bytes(original_content)

            with patch(
                "core.project_generator.TemplateRegistry"
            ) as registry:
                with self.assertRaises(FileExistsError):
                    ProjectGenerator().create(
                        project_name="Existing",
                        location=str(location),
                        template_name="unknown",
                    )

            self.assertEqual(existing_file.read_bytes(), original_content)
            self.assertEqual(tuple(destination.iterdir()), (existing_file,))
            registry.assert_not_called()

    def test_existing_destination_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)
            destination = location / "Existing"
            original_content = b"existing file"
            destination.write_bytes(original_content)

            with patch(
                "core.project_generator.TemplateRegistry"
            ) as registry:
                with self.assertRaises(FileExistsError):
                    ProjectGenerator().create(
                        project_name="Existing",
                        location=str(location),
                        template_name="unknown",
                    )

            self.assertEqual(destination.read_bytes(), original_content)
            registry.assert_not_called()

    def test_existing_link_destination_is_rejected_without_outside_writes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            location = temporary_root / "projects"
            outside = temporary_root / "outside"
            location.mkdir()
            outside.mkdir()
            destination = location / "Linked"

            try:
                os.symlink(
                    outside,
                    destination,
                    target_is_directory=True,
                )
            except OSError as error:
                self.skipTest(
                    "Directory symlink creation is unavailable: "
                    f"{error}"
                )

            with patch(
                "core.project_generator.TemplateRegistry"
            ) as registry:
                with self.assertRaises(FileExistsError):
                    ProjectGenerator().create(
                        project_name="Linked",
                        location=str(location),
                        template_name="unknown",
                    )

            self.assertTrue(destination.is_symlink())
            self.assertEqual(destination.resolve(), outside.resolve())
            self.assertEqual(tuple(outside.iterdir()), ())
            registry.assert_not_called()

    def test_unknown_template_creates_no_project_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)
            destination = location / "UnknownTemplate"

            with ExitStack() as stack:
                template_create = stack.enter_context(
                    patch("templates.basic.basic_template.BasicTemplate.create")
                )
                stage_calls = self._patch_generation_stages(stack)

                with self.assertRaises(KeyError):
                    ProjectGenerator().create(
                        project_name=destination.name,
                        location=str(location),
                        template_name="unknown",
                    )

            self.assertFalse(destination.exists())
            self.assertEqual(tuple(location.iterdir()), ())
            template_create.assert_not_called()
            for stage_call in stage_calls:
                stage_call.assert_not_called()

    def test_valid_templates_still_generate_their_owned_files(self) -> None:
        cases = {
            "basic": Path("app.py"),
            "library": Path("valid_library/__init__.py"),
            "cli": Path("valid_cli/cli.py"),
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            location = Path(temporary_directory)

            for template_name, expected_file in cases.items():
                with self.subTest(template=template_name):
                    project_name = f"Valid-{template_name}"
                    destination = location / project_name

                    with ExitStack() as stack:
                        stage_calls = self._patch_generation_stages(stack)
                        stack.enter_context(redirect_stdout(StringIO()))
                        ProjectGenerator().create(
                            project_name=project_name,
                            location=str(location),
                            template_name=template_name,
                        )

                    self.assertTrue((destination / expected_file).is_file())
                    for stage_call in stage_calls:
                        stage_call.assert_called_once()

    @staticmethod
    def _patch_generation_stages(stack: ExitStack) -> tuple[Mock, ...]:
        stage_paths = (
            "core.project_generator.EnvironmentBuilder.create",
            "core.project_generator.PythonToolsBuilder.update",
            "core.project_generator.RequirementsInstaller.install",
            "core.project_generator.GitBuilder.create",
            "core.project_generator.VSCodeBuilder.create",
        )

        return tuple(
            stack.enter_context(patch(stage_path))
            for stage_path in stage_paths
        )


if __name__ == "__main__":
    unittest.main()
