from __future__ import annotations

from abc import ABCMeta
from dataclasses import replace
from typing import Any

from temp_pr_bundles.PRs.structdantic.match import satisfies
from temp_pr_bundles.PRs.structdantic.policy import POLICY_PRAGMATIC, TypeCompatPolicy
from temp_pr_bundles.PRs.structdantic.traits import TraitSpec

_ABC_CACHE: dict[tuple[int, TypeCompatPolicy], type] = {}


def abc_for(
    trait: TraitSpec,
    policy: TypeCompatPolicy = POLICY_PRAGMATIC,
    *,
    name: str | None = None,
) -> type:
    """Create a runtime ABC whose subclass checks delegate to `satisfies`."""
    policy = replace(policy)
    key = (id(trait), policy)
    cached = _ABC_CACHE.get(key)
    if cached is not None:
        return cached

    abc_name = name or f"{trait.name or 'Trait'}ABC"

    class _TraitABC(metaclass=ABCMeta):
        pass

    _TraitABC.__name__ = abc_name

    @classmethod
    def __subclasshook__(cls, candidate: Any):
        try:
            return bool(satisfies(candidate, trait, policy))
        except Exception:
            return NotImplemented

    _TraitABC.__subclasshook__ = __subclasshook__  # type: ignore[attr-defined]
    _ABC_CACHE[key] = _TraitABC
    return _TraitABC


def duckissubclass(
    candidate: Any,
    trait: TraitSpec,
    policy: TypeCompatPolicy = POLICY_PRAGMATIC,
) -> bool:
    return bool(satisfies(candidate, trait, policy))


def duckisinstance(
    obj: Any,
    trait: TraitSpec,
    policy: TypeCompatPolicy = POLICY_PRAGMATIC,
) -> bool:
    return bool(satisfies(obj, trait, policy))
