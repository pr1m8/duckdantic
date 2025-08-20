"""Structdantic — structural typing helpers for (and beyond) Pydantic v2.

Provides field normalization, declarative trait specs, a pragmatic type
comparer, and matching utilities, with Google-style docstrings suitable
for auto-documentation.
"""

from __future__ import annotations

from strucdantic.algebra import intersect, minus, union
from strucdantic.cache import clear_cache, get_cache_stats, normalize_fields_cached
from strucdantic.compare import TraitRelation, compare_traits
from strucdantic.fields import FieldAliasSet, FieldOrigin, FieldView
from strucdantic.match import explain, satisfies
from strucdantic.naming import auto_name, short_type_token
from strucdantic.normalize import normalize_fields
from strucdantic.policy import POLICY_PRAGMATIC, AliasMode, TypeCompatPolicy
from strucdantic.registry import TraitRegistry
from strucdantic.shapes import ShapeOrigin, shape_id_token
from strucdantic.traits import FieldSpec, TraitSpec

__all__ = [
    "POLICY_PRAGMATIC",
    "AliasMode",
    "FieldAliasSet",
    "FieldOrigin",
    "FieldSpec",
    "FieldView",
    "ShapeOrigin",
    "TraitRegistry",
    "TraitRelation",
    "TraitSpec",
    "TypeCompatPolicy",
    "auto_name",
    "clear_cache",
    "compare_traits",
    "explain",
    "get_cache_stats",
    "intersect",
    "minus",
    "normalize_fields",
    "normalize_fields_cached",
    "satisfies",
    "shape_id_token",
    "short_type_token",
    "union",
]
__version__ = "0.0.3"
