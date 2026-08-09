"""Project-local persistence for installed ForgePy component names."""

import json
import os
import tempfile
from collections.abc import Iterable, Mapping
from json import JSONDecodeError
from pathlib import Path

from components.component_context import ComponentContext


STATE_DIRECTORY_NAME = ".forgepy"
STATE_FILENAME = "components.json"
INSTALLED_KEY = "installed"


class ForgePyComponentStateError(Exception):
    """Base error for project-local component state operations."""


class ComponentStateFormatError(ForgePyComponentStateError):
    """Raised when persisted component state has an invalid format."""


class ComponentStateIOError(ForgePyComponentStateError):
    """Raised when component state cannot be read or written."""


class ComponentStateStore:
    """Load and persist installed component names under one project."""

    def __init__(self, project_path: Path) -> None:
        context = ComponentContext(project_path=project_path)
        self.project_path = context.project_path
        self.state_directory = self.project_path / STATE_DIRECTORY_NAME
        self.state_path = self.state_directory / STATE_FILENAME

    def load(self) -> frozenset[str]:
        """Return installed names, or an empty set when state is absent."""

        try:
            content = self.state_path.read_text(encoding="utf-8")
            data = json.loads(content)
        except FileNotFoundError:
            return frozenset()
        except UnicodeDecodeError as error:
            raise ComponentStateFormatError(
                "ForgePy component state is not valid UTF-8 at "
                f"'{self.state_path}'."
            ) from error
        except JSONDecodeError as error:
            raise ComponentStateFormatError(
                "ForgePy component state contains malformed JSON at "
                f"'{self.state_path}' "
                f"(line {error.lineno}, column {error.colno})."
            ) from error
        except OSError as error:
            raise ComponentStateIOError(
                "ForgePy could not read component state from "
                f"'{self.state_path}': {error}"
            ) from error

        return self._normalize_document(data)

    def save(self, installed_components: Iterable[str]) -> frozenset[str]:
        """Validate and atomically persist installed component names."""

        self.load()
        installed = self._normalize_names(installed_components)
        document = {INSTALLED_KEY: sorted(installed)}
        serialized = json.dumps(
            document,
            indent=4,
            ensure_ascii=False,
        ) + "\n"

        try:
            self.state_directory.mkdir(parents=True, exist_ok=True)
            temporary_path: Path | None = None

            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    newline="\n",
                    dir=self.state_directory,
                    prefix=f".{STATE_FILENAME}.",
                    suffix=".tmp",
                    delete=False,
                ) as temporary_file:
                    temporary_path = Path(temporary_file.name)
                    temporary_file.write(serialized)
                    temporary_file.flush()
                    os.fsync(temporary_file.fileno())

                temporary_path.replace(self.state_path)
            finally:
                if temporary_path is not None and temporary_path.exists():
                    temporary_path.unlink()
        except OSError as error:
            raise ComponentStateIOError(
                "ForgePy could not save component state to "
                f"'{self.state_path}': {error}"
            ) from error

        return installed

    def add(self, component_name: str) -> frozenset[str]:
        """Add one installed name while preserving existing state."""

        name = self._normalize_names((component_name,))
        installed = self.load().union(name)
        return self.save(installed)

    def is_installed(self, component_name: str) -> bool:
        """Return whether one valid component name is installed."""

        name = next(iter(self._normalize_names((component_name,))))
        return name in self.load()

    @classmethod
    def _normalize_document(cls, data: object) -> frozenset[str]:
        if not isinstance(data, Mapping):
            raise ComponentStateFormatError(
                "ForgePy component state must contain a JSON object."
            )

        if set(data) != {INSTALLED_KEY}:
            raise ComponentStateFormatError(
                "ForgePy component state must contain only an "
                f"'{INSTALLED_KEY}' field."
            )

        installed = data[INSTALLED_KEY]

        if not isinstance(installed, list):
            raise ComponentStateFormatError(
                "ForgePy component state 'installed' field must be a list."
            )

        try:
            return cls._normalize_names(installed)
        except (TypeError, ValueError) as error:
            raise ComponentStateFormatError(
                "ForgePy component state contains an invalid installed "
                f"component: {error}"
            ) from error

    @staticmethod
    def _normalize_names(
        installed_components: Iterable[str],
    ) -> frozenset[str]:
        if isinstance(installed_components, (str, bytes)):
            raise TypeError(
                "Installed components must be an iterable of strings."
            )

        try:
            installed = tuple(installed_components)
        except TypeError as error:
            raise TypeError(
                "Installed components must be an iterable of strings."
            ) from error

        for name in installed:
            if not isinstance(name, str):
                raise TypeError(
                    "Installed components must contain only strings."
                )
            if not name.strip():
                raise ValueError(
                    "Installed component names must not be empty."
                )

        return frozenset(installed)
