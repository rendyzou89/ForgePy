import unittest
from dataclasses import FrozenInstanceError

from components.base_component import BaseComponent
from components.component_metadata import ComponentMetadata
from components.component_registry import ComponentRegistry


def component_metadata(name: str = "example") -> ComponentMetadata:
    return ComponentMetadata(
        name=name,
        description="Example component.",
        version="1.0.0",
        author="Example Author",
        tags=("example",),
    )


class ExampleComponent(BaseComponent):

    def __init__(
        self,
        metadata: ComponentMetadata,
        name: str | None = None,
    ) -> None:
        self._metadata = metadata
        self._name = metadata.name if name is None else name

    @property
    def name(self) -> str:
        return self._name

    @property
    def metadata(self) -> ComponentMetadata:
        return self._metadata


class InvalidMetadataComponent(BaseComponent):

    @property
    def name(self) -> str:
        return "invalid-metadata"

    @property
    def metadata(self) -> ComponentMetadata:
        return object()  # type: ignore[return-value]


class ComponentMetadataTests(unittest.TestCase):

    def test_metadata_contains_the_required_fields(self) -> None:
        metadata = component_metadata()

        self.assertEqual(metadata.name, "example")
        self.assertEqual(metadata.description, "Example component.")
        self.assertEqual(metadata.version, "1.0.0")
        self.assertEqual(metadata.author, "Example Author")
        self.assertEqual(metadata.tags, ("example",))

    def test_metadata_is_immutable(self) -> None:
        metadata = component_metadata()

        with self.assertRaises(FrozenInstanceError):
            metadata.description = "Changed"  # type: ignore[misc]

    def test_metadata_normalizes_tags_to_an_immutable_tuple(self) -> None:
        source_tags = ["example"]
        metadata = ComponentMetadata(
            name="example",
            description="Example component.",
            version="1.0.0",
            author="Example Author",
            tags=source_tags,  # type: ignore[arg-type]
        )

        source_tags.append("changed")

        self.assertEqual(metadata.tags, ("example",))

    def test_metadata_rejects_empty_names(self) -> None:
        for name in ("", "   "):
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ValueError,
                    "name must not be empty",
                ):
                    component_metadata(name)

    def test_metadata_rejects_non_string_fields(self) -> None:
        values: dict[str, object] = {
            "name": "example",
            "description": "Example component.",
            "version": "1.0.0",
            "author": "Example Author",
            "tags": (),
        }

        for field_name in ("name", "description", "version", "author"):
            with self.subTest(field=field_name):
                invalid_values = values.copy()
                invalid_values[field_name] = object()

                with self.assertRaisesRegex(
                    TypeError,
                    f"{field_name} must be a string",
                ):
                    ComponentMetadata(**invalid_values)  # type: ignore[arg-type]

    def test_metadata_rejects_invalid_tags(self) -> None:
        for tags, message in (
            ("example", "iterable of strings"),
            (b"example", "iterable of strings"),
            (1, "iterable of strings"),
            (("example", 1), "only strings"),
        ):
            with self.subTest(tags=tags):
                with self.assertRaisesRegex(TypeError, message):
                    ComponentMetadata(
                        name="example",
                        description="Example component.",
                        version="1.0.0",
                        author="Example Author",
                        tags=tags,  # type: ignore[arg-type]
                    )


class ComponentRegistryTests(unittest.TestCase):

    def test_registry_starts_without_built_in_components(self) -> None:
        self.assertEqual(ComponentRegistry().list_components(), ())

    def test_registers_a_valid_component(self) -> None:
        registry = ComponentRegistry()
        component = ExampleComponent(component_metadata())

        registry.register(component)

        self.assertEqual(registry.list_components(), (component,))

    def test_get_returns_the_registered_component(self) -> None:
        registry = ComponentRegistry()
        component = ExampleComponent(component_metadata())
        registry.register(component)

        self.assertIs(registry.get("example"), component)

    def test_list_components_preserves_registration_order(self) -> None:
        registry = ComponentRegistry()
        first = ExampleComponent(component_metadata("first"))
        second = ExampleComponent(component_metadata("second"))

        registry.register(first)
        registry.register(second)

        self.assertEqual(registry.list_components(), (first, second))

    def test_rejects_duplicate_component_names(self) -> None:
        registry = ComponentRegistry()
        original = ExampleComponent(component_metadata())
        registry.register(original)

        with self.assertRaisesRegex(ValueError, "already registered"):
            registry.register(ExampleComponent(component_metadata()))

        self.assertIs(registry.get("example"), original)
        self.assertEqual(registry.list_components(), (original,))

    def test_rejects_an_object_that_is_not_a_component(self) -> None:
        registry = ComponentRegistry()

        with self.assertRaisesRegex(
            TypeError,
            "must inherit from BaseComponent",
        ):
            registry.register(object())  # type: ignore[arg-type]

        self.assertEqual(registry.list_components(), ())

    def test_rejects_components_with_empty_names(self) -> None:
        for name in ("", "   "):
            with self.subTest(name=name):
                registry = ComponentRegistry()
                component = ExampleComponent(
                    component_metadata("metadata-name"),
                    name=name,
                )

                with self.assertRaisesRegex(
                    ValueError,
                    "name must not be empty",
                ):
                    registry.register(component)

                self.assertEqual(registry.list_components(), ())

    def test_rejects_components_with_non_string_names(self) -> None:
        registry = ComponentRegistry()
        component = ExampleComponent(
            component_metadata(),
            name=object(),  # type: ignore[arg-type]
        )

        with self.assertRaisesRegex(TypeError, "name must be a string"):
            registry.register(component)

        self.assertEqual(registry.list_components(), ())

    def test_rejects_invalid_component_metadata(self) -> None:
        registry = ComponentRegistry()

        with self.assertRaisesRegex(
            TypeError,
            "metadata must be ComponentMetadata",
        ):
            registry.register(InvalidMetadataComponent())

        self.assertEqual(registry.list_components(), ())

    def test_rejects_component_and_metadata_name_mismatch(self) -> None:
        registry = ComponentRegistry()
        component = ExampleComponent(
            component_metadata("metadata-name"),
            name="component-name",
        )

        with self.assertRaisesRegex(ValueError, "must match"):
            registry.register(component)

        self.assertEqual(registry.list_components(), ())
        with self.assertRaises(KeyError):
            registry.get("metadata-name")

    def test_unknown_component_lookup_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            ComponentRegistry().get("unknown")


if __name__ == "__main__":
    unittest.main()
