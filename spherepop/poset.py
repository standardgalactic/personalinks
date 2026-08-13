from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from spherepop.model import Quotient


class PosetError(ValueError):
    pass


@dataclass(frozen=True)
class OptionSpace:
    label: str
    content: frozenset[str | Quotient]


def preceq(a: OptionSpace, b: OptionSpace) -> bool:
    return a.content <= b.content


def extensionally_equivalent(a: OptionSpace, b: OptionSpace) -> bool:
    return a.content == b.content


def minimal_elements(poset: Sequence[OptionSpace]) -> tuple[OptionSpace, ...]:
    result = []
    for x in poset:
        if not any(other.content < x.content for other in poset if other is not x):
            result.append(x)
    return tuple(result)


def pop_minimal(poset: Sequence[OptionSpace], label: str) -> tuple[OptionSpace, ...]:
    by_label = {space.label: space for space in poset}
    if label not in by_label:
        raise PosetError(f"no scope labeled {label!r} in this poset")
    target = by_label[label]
    if target not in minimal_elements(poset):
        raise PosetError(f"scope {label!r} is not currently minimal -- cannot pop it")
    return tuple(space for space in poset if space.label != label)
