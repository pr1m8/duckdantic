"""Duckdantic — structural typing helpers for (and beyond) Pydantic v2.

Provides field normalization, declarative trait specs, a pragmatic type
comparer, and matching utilities, with Google-style docstrings suitable
for auto-documentation.
"""

from __future__ import annotations

from duckdantic.adapters.abc import abc_for, duckisinstance, duckissubclass
from duckdantic.algebra import intersect, minus, union
from duckdantic.build.methods import MethodSpec, methods_explain, methods_satisfy
from duckdantic.cache import clear_cache, get_cache_stats, normalize_fields_cached
from duckdantic.compare import TraitRelation, compare_traits
from duckdantic.fields import FieldAliasSet, FieldOrigin, FieldView
from duckdantic.match import explain, satisfies
from duckdantic.models import (
    Duck,
    DuckModel,
    DuckRootModel,
    DuckType,
    as_duck,
    is_duck_of,
)
from duckdantic.naming import auto_name, short_type_token
from duckdantic.normalize import normalize_fields
from duckdantic.policy import POLICY_PRAGMATIC, AliasMode, TypeCompatPolicy
from duckdantic.registry import TraitRegistry
from duckdantic.shapes import ShapeOrigin, shape_id_token
from duckdantic.traits import FieldSpec, TraitSpec

__all__ = [
    "POLICY_PRAGMATIC",
    "AliasMode",
    "Duck",
    "DuckModel",
    "DuckRootModel",
    "DuckType",
    "FieldAliasSet",
    "FieldOrigin",
    "FieldSpec",
    "FieldView",
    "MethodSpec",
    "ShapeOrigin",
    "TraitRegistry",
    "TraitRelation",
    "TraitSpec",
    "TypeCompatPolicy",
    "abc_for",
    "as_duck",
    "auto_name",
    "clear_cache",
    "compare_traits",
    "duckisinstance",
    "duckissubclass",
    "explain",
    "get_cache_stats",
    "intersect",
    "is_duck_of",
    "methods_explain",
    "methods_satisfy",
    "minus",
    "normalize_fields",
    "normalize_fields_cached",
    "satisfies",
    "shape_id_token",
    "short_type_token",
    "union",
]
__version__ = "0.0.3"
