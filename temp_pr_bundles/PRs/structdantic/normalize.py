"""Normalize classes, instances, and mappings into `FieldView`s using.

providers.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from temp_pr_bundles.PRs.structdantic.fields import FieldView
from temp_pr_bundles.PRs.structdantic.providers.base import (
    register_default_providers,
    registry,
)

# ensure available for isinstance checks


def normalize_fields(obj: Any) -> dict[str, FieldView]:
    """Return a mapping of field name → FieldView from diverse inputs via.

    provider registry.
    """
    # Instances normalize via their class
    if (
        not isinstance(obj, (str, bytes))
        and hasattr(obj, "__class__")
        and not isinstance(obj, type)
        and not isinstance(obj, Mapping)
    ):
        obj = obj.__class__
    register_default_providers()
    prov = registry.pick(obj)
    if prov is None:
        raise TypeError(
            "Unsupported input for normalize_fields: expected mapping, class, or instance",
        )
    return prov.fields(obj)
