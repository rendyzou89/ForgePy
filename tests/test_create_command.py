import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from cli.commands import create_commands
from cli.commands.create_command import CreateCommand
from cli.dispatcher import Dispatcher
from cli.parser import Parser
from config.user_config import ConfigStore


class CreateCommandConfigTests(unittest.TestCase):

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.home_directory = Path(
            self.temporary_directory.name,
        )
        self.store = ConfigStore(
            home_directory=self.home_directory,
        )
        self.command = CreateCommand(
            store=self.store,
        )

    def test_parser_distinguishes_omitted_and_explicit_template(
        self,
    ) -> None:
        with patch(
            "config.user_config.Path.home",
            side_effect=AssertionError(
                "Parsing must not resolve the real user home."
            ),
        ):
            with patch(
                "sys.argv",
                [
                    "forgepy",
                    "create",
                    "Example",
                    "--location",
                    "D:/Explicit",
                ],
            ):
                omitted = Parser().parse()

            with patch(
                "sys.argv",
                [
                    "forgepy",
                    "create",
                    "Example",
                    "--location",
                    "D:/Explicit",
                    "--template",
                    "basic",
                ],
            ):
                explicit = Parser().parse()

        self.assertIsNone(omitted.template)
        self.assertEqual(explicit.template, "basic")

    def test_explicit_location_overrides_stored_location(self) -> None:
        self.store.save(
            {
                "default_location": "D:/Stored",
                "default_template": "stored-template",
                "author": "Stored Author",
                "license": "Stored License",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location="D:/Explicit",
            template=None,
        )

        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Explicit",
            template_name="stored-template",
        )

    def test_stored_location_is_used_when_cli_location_is_absent(
        self,
    ) -> None:
        self.store.save(
            {
                "default_location": "D:/Stored",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location=None,
            template="basic",
        )

        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Stored",
            template_name="basic",
        )

    def test_explicit_template_overrides_stored_template(self) -> None:
        self.store.save(
            {
                "default_location": "D:/Stored",
                "default_template": "stored-template",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location=None,
            template="basic",
        )

        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Stored",
            template_name="basic",
        )

    def test_stored_template_is_used_when_cli_template_is_absent(
        self,
    ) -> None:
        self.store.save(
            {
                "default_template": "stored-template",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location="D:/Explicit",
            template=None,
        )

        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Explicit",
            template_name="stored-template",
        )

    def test_no_command_preserves_project_and_location_prompts(
        self,
    ) -> None:
        commands = tuple(
            self.command
            if isinstance(command, CreateCommand)
            else command
            for command in create_commands()
        )
        output = StringIO()

        with patch(
            "sys.argv",
            ["forgepy"],
        ):
            with patch(
                "builtins.input",
                side_effect=[
                    "Prompted Project",
                    "D:/Prompted",
                ],
            ) as prompt:
                with patch(
                    "cli.commands.create_command.ProjectGenerator",
                ) as generator:
                    with redirect_stdout(output):
                        args = Parser(
                            commands=commands,
                        ).parse()
                        self.assertIsNone(args.template)
                        Dispatcher(
                            commands=commands,
                        ).dispatch(args)

        prompt.assert_has_calls(
            [
                call("Project Name : "),
                call("Location : "),
            ]
        )
        self.assertEqual(prompt.call_count, 2)
        generator.return_value.create.assert_called_once_with(
            project_name="Prompted Project",
            location="D:/Prompted",
            template_name="basic",
        )
        self.assertFalse(self.store.config_directory.exists())

    def test_explicit_project_name_is_used_without_prompt(self) -> None:
        generator, prompt, _ = self._execute(
            project_name="Explicit Project",
            location="D:/Explicit",
            template="basic",
        )

        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Explicit Project",
            location="D:/Explicit",
            template_name="basic",
        )

    def test_empty_stored_defaults_use_prompt_and_basic_fallback(
        self,
    ) -> None:
        self.store.save(
            {
                "default_location": "",
                "default_template": "",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location=None,
            template=None,
            prompt_values=("D:/Prompted",),
        )

        prompt.assert_called_once_with("Location : ")
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Prompted",
            template_name="basic",
        )

    def test_explicit_empty_values_preserve_existing_fallbacks(
        self,
    ) -> None:
        self.store.save(
            {
                "default_location": "D:/Stored",
                "default_template": "stored-template",
            }
        )

        generator, prompt, _ = self._execute(
            project_name="Example",
            location="",
            template="",
            prompt_values=("D:/Prompted",),
        )

        prompt.assert_called_once_with("Location : ")
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Prompted",
            template_name="basic",
        )

    def test_malformed_configuration_aborts_without_fallback(
        self,
    ) -> None:
        malformed = b'{"default_location": "D:/Incomplete"'
        self.store.config_directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.store.config_path.write_bytes(malformed)

        generator, prompt, output = self._execute(
            project_name=None,
            location=None,
            template="basic",
        )

        self.assertIn(
            "[ERROR] ForgePy configuration contains malformed JSON",
            output,
        )
        self.assertIn(
            "python main.py config reset",
            output,
        )
        prompt.assert_not_called()
        generator.assert_not_called()
        self.assertEqual(
            self.store.config_path.read_bytes(),
            malformed,
        )

    def test_fully_explicit_values_do_not_read_configuration(self) -> None:
        malformed = b'{"default_template":'
        self.store.config_directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.store.config_path.write_bytes(malformed)

        with patch.object(
            self.store,
            "load",
            wraps=self.store.load,
        ) as load:
            generator, prompt, _ = self._execute(
                project_name="Example",
                location="D:/Explicit",
                template="basic",
            )

        load.assert_not_called()
        prompt.assert_not_called()
        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Explicit",
            template_name="basic",
        )
        self.assertEqual(
            self.store.config_path.read_bytes(),
            malformed,
        )

    def test_fully_explicit_default_catalog_does_not_resolve_home(
        self,
    ) -> None:
        output = StringIO()

        with patch(
            "config.user_config.Path.home",
            side_effect=AssertionError(
                "Fully explicit creation must not resolve the user home."
            ),
        ):
            with patch(
                "sys.argv",
                [
                    "forgepy",
                    "create",
                    "Example",
                    "--location",
                    "D:/Explicit",
                    "--template",
                    "basic",
                ],
            ):
                with patch(
                    "cli.commands.create_command.ProjectGenerator",
                ) as generator:
                    with redirect_stdout(output):
                        args = Parser().parse()
                        Dispatcher().dispatch(args)

        generator.return_value.create.assert_called_once_with(
            project_name="Example",
            location="D:/Explicit",
            template_name="basic",
        )

    def _execute(
        self,
        *,
        project_name: str | None,
        location: str | None,
        template: str | None,
        prompt_values: tuple[str, ...] = (),
    ) -> tuple[MagicMock, MagicMock, str]:
        args = Namespace(
            project_name=project_name,
            location=location,
            template=template,
        )
        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=prompt_values,
        ) as prompt:
            with patch(
                "cli.commands.create_command.ProjectGenerator",
            ) as generator:
                with redirect_stdout(output):
                    self.command.execute(args)

        return generator, prompt, output.getvalue()


if __name__ == "__main__":
    unittest.main()
