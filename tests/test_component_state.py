import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from components.component_registry import ComponentRegistry
from components.component_state import (
    ComponentStateFormatError,
    ComponentStateIOError,
    ComponentStateStore,
)


class ComponentStateStoreTests(unittest.TestCase):

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.temporary_path = Path(self.temporary_directory.name)
        self.project_path = self.temporary_path / "project"
        self.outside_path = self.temporary_path / "outside"
        self.project_path.mkdir()
        self.outside_path.mkdir()
        self.store = ComponentStateStore(self.project_path)

    def test_missing_state_returns_empty_installed_set(self) -> None:
        self.assertEqual(self.store.load(), frozenset())
        self.assertFalse(self.store.state_directory.exists())

    def test_save_creates_state_directory(self) -> None:
        self.store.save(())

        self.assertTrue(self.store.state_directory.is_dir())
        self.assertTrue(self.store.state_path.is_file())

    def test_save_and_load_round_trip(self) -> None:
        saved = self.store.save(("pytest", "lint"))

        self.assertEqual(saved, frozenset(("pytest", "lint")))
        self.assertEqual(self.store.load(), saved)

    def test_persisted_names_have_deterministic_order(self) -> None:
        self.store.save(("zeta", "alpha", "middle"))

        data = json.loads(self.store.state_path.read_text(encoding="utf-8"))
        self.assertEqual(
            data,
            {"installed": ["alpha", "middle", "zeta"]},
        )

    def test_duplicate_names_are_normalized_on_save_and_load(self) -> None:
        self.store.save(("pytest", "pytest"))
        self.assertEqual(self.store.load(), frozenset(("pytest",)))

        self.store.state_path.write_text(
            '{"installed": ["lint", "lint"]}\n',
            encoding="utf-8",
        )
        self.assertEqual(self.store.load(), frozenset(("lint",)))

    def test_add_installed_component_preserves_existing_names(self) -> None:
        self.store.save(("pytest",))

        installed = self.store.add("lint")

        self.assertEqual(installed, frozenset(("pytest", "lint")))
        self.assertEqual(self.store.load(), installed)

    def test_membership_check_reads_installed_state(self) -> None:
        self.store.save(("pytest",))

        self.assertTrue(self.store.is_installed("pytest"))
        self.assertFalse(self.store.is_installed("lint"))

    def test_malformed_json_raises_clear_error(self) -> None:
        self._write_raw(b'{"installed": ["pytest"]')

        with self.assertRaisesRegex(
            ComponentStateFormatError,
            "malformed JSON",
        ):
            self.store.load()

    def test_invalid_top_level_structure_is_rejected(self) -> None:
        for data in ([], {"unexpected": []}, {"installed": [], "extra": 1}):
            with self.subTest(data=data):
                self._write_json(data)

                with self.assertRaises(ComponentStateFormatError):
                    self.store.load()

    def test_invalid_installed_entry_is_rejected(self) -> None:
        for entry in (None, 1, "", "   "):
            with self.subTest(entry=entry):
                self._write_json({"installed": [entry]})

                with self.assertRaises(ComponentStateFormatError):
                    self.store.load()

    def test_writes_preserve_malformed_existing_data(self) -> None:
        malformed = b'{"installed": ["pytest"]'
        self._write_raw(malformed)

        for operation in (
            lambda: self.store.save(("lint",)),
            lambda: self.store.add("lint"),
        ):
            with self.subTest(operation=operation):
                with self.assertRaises(ComponentStateFormatError):
                    operation()

                self.assertEqual(
                    self.store.state_path.read_bytes(),
                    malformed,
                )

    def test_atomic_write_failure_preserves_existing_valid_state(self) -> None:
        self.store.save(("pytest",))
        original = self.store.state_path.read_bytes()
        original_replace = Path.replace

        def fail_for_temporary_file(source: Path, target: Path) -> Path:
            if target == self.store.state_path:
                raise OSError("replace failed")
            return original_replace(source, target)

        with patch.object(Path, "replace", fail_for_temporary_file):
            with self.assertRaisesRegex(
                ComponentStateIOError,
                "could not save",
            ):
                self.store.save(("lint",))

        self.assertEqual(self.store.state_path.read_bytes(), original)

    def test_state_store_writes_nothing_outside_project(self) -> None:
        self.store.add("pytest")

        self.assertEqual(tuple(self.outside_path.iterdir()), ())
        self.assertEqual(
            self.store.state_path.relative_to(self.project_path),
            Path(".forgepy/components.json"),
        )

    def test_registry_remains_installation_state_agnostic(self) -> None:
        registry = ComponentRegistry()

        self.store.add("external")

        self.assertEqual(
            tuple(component.name for component in registry.list_components()),
            ("pytest",),
        )
        with self.assertRaises(KeyError):
            registry.get("external")

    def _write_json(self, data: object) -> None:
        self._write_raw(
            (json.dumps(data) + "\n").encode("utf-8")
        )

    def _write_raw(self, content: bytes) -> None:
        self.store.state_directory.mkdir(parents=True, exist_ok=True)
        self.store.state_path.write_bytes(content)


if __name__ == "__main__":
    unittest.main()
