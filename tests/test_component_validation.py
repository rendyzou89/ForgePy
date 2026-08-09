import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from components.base_component import BaseComponent
from components.component_context import ComponentContext
from components.component_manifest import ComponentManifest
from components.component_metadata import ComponentMetadata
from components.component_registry import ComponentRegistry
from components.component_validation import (
    ComponentValidationError,
    validate_component,
)


class ValidationComponent(BaseComponent):

    def __init__(self, manifest: ComponentManifest) -> None:
        self._manifest = manifest
        self.install_calls = 0

    @property
    def name(self) -> str:
        return "validation"

    @property
    def metadata(self) -> ComponentMetadata:
        return ComponentMetadata(
            name=self.name,
            description="Validation test component.",
            version="1.0.0",
            author="ForgePy Tests",
            tags=("validation",),
        )

    @property
    def manifest(self) -> ComponentManifest:
        return self._manifest

    def install(self, context: ComponentContext) -> None:
        self.install_calls += 1
        (context.project_path / "installed.txt").write_text(
            "installed\n",
            encoding="utf-8",
        )


class ComponentValidationTests(unittest.TestCase):

    def test_accepts_component_without_dependencies_or_conflicts(self) -> None:
        component = ValidationComponent(ComponentManifest())

        validate_component(component, ())

    def test_accepts_satisfied_dependency(self) -> None:
        component = ValidationComponent(
            ComponentManifest(dependencies=("required",))
        )

        validate_component(component, ("required",))

    def test_rejects_missing_dependency(self) -> None:
        component = ValidationComponent(
            ComponentManifest(dependencies=("required",))
        )

        with self.assertRaises(ComponentValidationError) as context:
            validate_component(component, ())

        self.assertEqual(
            context.exception.missing_dependencies,
            ("required",),
        )
        self.assertEqual(context.exception.active_conflicts, ())
        self.assertIn("missing dependencies: required", str(context.exception))

    def test_accepts_inactive_conflict(self) -> None:
        component = ValidationComponent(
            ComponentManifest(conflicts=("incompatible",))
        )

        validate_component(component, ("unrelated",))

    def test_rejects_active_conflict(self) -> None:
        component = ValidationComponent(
            ComponentManifest(conflicts=("incompatible",))
        )

        with self.assertRaises(ComponentValidationError) as context:
            validate_component(component, ("incompatible",))

        self.assertEqual(context.exception.missing_dependencies, ())
        self.assertEqual(
            context.exception.active_conflicts,
            ("incompatible",),
        )
        self.assertIn("active conflicts: incompatible", str(context.exception))

    def test_reports_multiple_dependencies_and_conflicts(self) -> None:
        component = ValidationComponent(
            ComponentManifest(
                dependencies=("first", "second", "third"),
                conflicts=("legacy", "alternative", "inactive"),
            )
        )

        with self.assertRaises(ComponentValidationError) as context:
            validate_component(
                component,
                ("first", "legacy", "alternative"),
            )

        self.assertEqual(
            context.exception.missing_dependencies,
            ("second", "third"),
        )
        self.assertEqual(
            context.exception.active_conflicts,
            ("legacy", "alternative"),
        )

    def test_registry_remains_resolution_agnostic(self) -> None:
        registry = ComponentRegistry()
        component = ValidationComponent(
            ComponentManifest(
                dependencies=("not-registered",),
                conflicts=("also-not-registered",),
            )
        )

        registry.register(component)

        self.assertIs(registry.get("validation"), component)
        self.assertEqual(component.install_calls, 0)

    def test_validation_does_not_write_or_install(self) -> None:
        component = ValidationComponent(
            ComponentManifest(dependencies=("required",))
        )

        with TemporaryDirectory() as temporary_directory:
            project_path = Path(temporary_directory)

            with self.assertRaises(ComponentValidationError):
                validate_component(component, ())

            self.assertEqual(tuple(project_path.iterdir()), ())
            self.assertEqual(component.install_calls, 0)


if __name__ == "__main__":
    unittest.main()
