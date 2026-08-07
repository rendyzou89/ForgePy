"""
==================================================
ForgePy
Template Registry
==================================================
"""

from dataclasses import dataclass

from templates.basic.basic_template import BasicTemplate
from templates.library.library_template import LibraryTemplate
from templates.template_engine.base_template import BaseTemplate
from templates.template_engine.template_metadata import TemplateMetadata


@dataclass(frozen=True, slots=True)
class _TemplateRegistration:
    template: BaseTemplate
    metadata: TemplateMetadata


class TemplateRegistry:

    def __init__(self) -> None:

        self._registrations: dict[str, _TemplateRegistration] = {}

        self.register(BasicTemplate())
        self.register(LibraryTemplate())

    @property
    def templates(self) -> dict[str, BaseTemplate]:
        """Return a compatibility snapshot of registered templates."""

        return {
            name: registration.template
            for name, registration in self._registrations.items()
        }

    def register(
        self,
        template: BaseTemplate,
    ) -> None:
        """Register a template using its metadata name as the lookup key."""

        if not isinstance(template, BaseTemplate):
            raise TypeError("Template must inherit from BaseTemplate.")

        template_name = template.name

        if not isinstance(template_name, str):
            raise TypeError("Template name must be a string.")

        if not template_name.strip():
            raise ValueError("Template name must not be empty.")

        metadata = template.metadata

        if not isinstance(metadata, TemplateMetadata):
            raise TypeError("Template metadata must be TemplateMetadata.")

        if not metadata.name.strip():
            raise ValueError("Template metadata name must not be empty.")

        if template_name != metadata.name:
            raise ValueError(
                "Template name and metadata name must match."
            )

        if metadata.name in self._registrations:
            raise ValueError(
                f"Template '{metadata.name}' is already registered."
            )

        self._registrations[metadata.name] = _TemplateRegistration(
            template=template,
            metadata=metadata,
        )

    def get(
        self,
        name: str,
    ) -> BaseTemplate:

        return self._registrations[name].template

    def get_metadata(
        self,
        name: str,
    ) -> TemplateMetadata:
        """Return metadata for one registered template."""

        return self._registrations[name].metadata

    def list_templates(self) -> dict[str, BaseTemplate]:

        return self.templates

    def list_metadata(self) -> tuple[TemplateMetadata, ...]:
        """Return registered metadata in registration order."""

        return tuple(
            registration.metadata
            for registration in self._registrations.values()
        )
