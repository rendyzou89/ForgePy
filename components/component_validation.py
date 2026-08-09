"""Stateless pre-install validation for component relationships."""

from collections.abc import Iterable

from components.base_component import BaseComponent


class ComponentValidationError(ValueError):
    """Report unsatisfied direct relationships for one component."""

    def __init__(
        self,
        component_name: str,
        missing_dependencies: tuple[str, ...] = (),
        active_conflicts: tuple[str, ...] = (),
    ) -> None:
        self.component_name = component_name
        self.missing_dependencies = missing_dependencies
        self.active_conflicts = active_conflicts

        failures: list[str] = []

        if missing_dependencies:
            failures.append(
                "missing dependencies: "
                f"{', '.join(missing_dependencies)}"
            )

        if active_conflicts:
            failures.append(
                "active conflicts: "
                f"{', '.join(active_conflicts)}"
            )

        super().__init__(
            f"Component '{component_name}' cannot be installed; "
            f"{'; '.join(failures)}."
        )


def validate_component(
    component: BaseComponent,
    installed_components: Iterable[str],
) -> None:
    """Validate direct dependencies and conflicts against explicit state."""

    installed = _installed_component_names(installed_components)
    manifest = component.manifest
    missing_dependencies = tuple(
        name
        for name in manifest.dependencies
        if name not in installed
    )
    active_conflicts = tuple(
        name
        for name in manifest.conflicts
        if name in installed
    )

    if missing_dependencies or active_conflicts:
        raise ComponentValidationError(
            component_name=component.name,
            missing_dependencies=missing_dependencies,
            active_conflicts=active_conflicts,
        )


def _installed_component_names(
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

    if not all(isinstance(name, str) for name in installed):
        raise TypeError(
            "Installed components must contain only strings."
        )

    return frozenset(installed)
