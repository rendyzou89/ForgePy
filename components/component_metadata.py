"""Descriptive metadata for ForgePy components."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ComponentMetadata:
    """Describe a component without defining installation behavior."""

    name: str
    description: str
    version: str
    author: str
    tags: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in (
            "name",
            "description",
            "version",
            "author",
        ):
            if not isinstance(getattr(self, field_name), str):
                raise TypeError(
                    f"Component metadata {field_name} must be a string."
                )

        if not self.name.strip():
            raise ValueError(
                "Component metadata name must not be empty."
            )

        if isinstance(self.tags, (str, bytes)):
            raise TypeError(
                "Component metadata tags must be an iterable of strings."
            )

        try:
            normalized_tags = tuple(self.tags)
        except TypeError as error:
            raise TypeError(
                "Component metadata tags must be an iterable of strings."
            ) from error

        if not all(isinstance(tag, str) for tag in normalized_tags):
            raise TypeError(
                "Component metadata tags must contain only strings."
            )

        object.__setattr__(self, "tags", normalized_tags)
