"""
==================================================
ForgePy
Module  : Config Command
==================================================
"""

import json
from argparse import ArgumentParser, Namespace

from cli.command import Command
from config.user_config import (
    ConfigStore,
    ForgePyConfigError,
    UnknownConfigSettingError,
)


class ConfigCommand(Command):
    """
    Manage persistent ForgePy user configuration.
    """

    name = "config"
    summary = "Show or update ForgePy user configuration."
    description = (
        "Inspect or update the persistent ForgePy configuration stored "
        "under the current user's home directory."
    )

    def __init__(
        self,
        store: ConfigStore | None = None,
    ) -> None:
        self._store = store

    def configure_parser(
        self,
        parser: ArgumentParser,
    ) -> None:
        actions = parser.add_subparsers(
            dest="config_action",
            title="config actions",
            description="Available configuration actions",
            metavar="ACTION",
            required=True,
        )

        actions.add_parser(
            "show",
            help="Show every supported configuration setting.",
            description=(
                "Show the effective ForgePy user configuration. "
                "Missing files use safe defaults without being created."
            ),
        )

        set_parser = actions.add_parser(
            "set",
            help="Set and persist one supported configuration value.",
            description=(
                "Update one supported ForgePy configuration setting "
                "while preserving all other values."
            ),
        )
        set_parser.add_argument(
            "setting",
            metavar="KEY",
            help=(
                "Setting to update. Supported keys: "
                f"{self._supported_settings_text()}."
            ),
        )
        set_parser.add_argument(
            "value",
            metavar="VALUE",
            help="String value to persist for the selected setting.",
        )

        actions.add_parser(
            "reset",
            help="Reset and persist all settings to their defaults.",
            description=(
                "Replace the persisted ForgePy user configuration "
                "with the safe defaults."
            ),
        )

    def execute(self, args: Namespace) -> None:
        action = getattr(
            args,
            "config_action",
            None,
        )

        try:
            if action == "show":
                self._show()
            elif action == "set":
                self._set(
                    setting=args.setting,
                    value=args.value,
                )
            elif action == "reset":
                self._reset()
            else:
                print(
                    "[ERROR] Unknown ForgePy configuration action: "
                    f"'{action}'."
                )
        except UnknownConfigSettingError as error:
            print(f"[ERROR] {error}")
            print(
                "Supported settings: "
                f"{self._supported_settings_text()}."
            )
        except ForgePyConfigError as error:
            print(f"[ERROR] {error}")

    def _show(self) -> None:
        config = self._get_store().load()

        print("=" * 40)
        print(" ForgePy Configuration ")
        print("=" * 40)

        for setting, value in config.items():
            print(
                f"{setting} = "
                f"{self._display_value(value)}"
            )

    def _set(
        self,
        setting: str,
        value: str,
    ) -> None:
        updated = self._get_store().update(
            setting,
            value,
        )

        print(
            "[OK] ForgePy configuration updated: "
            f"{setting} = {self._display_value(updated[setting])}"
        )

    def _reset(self) -> None:
        self._get_store().reset()
        print("[OK] ForgePy configuration reset to defaults.")

    def _get_store(self) -> ConfigStore:
        if self._store is None:
            self._store = ConfigStore()

        return self._store

    @staticmethod
    def _display_value(value: str) -> str:
        return json.dumps(
            value,
            ensure_ascii=False,
        )

    @staticmethod
    def _supported_settings_text() -> str:
        return ", ".join(
            ConfigStore.defaults()
        )
