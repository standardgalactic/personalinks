from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Quotient:
    """An equivalence class produced by COLLAPSE: an element of O/\u2261_C.

    This carries only its membership -- no "representative" field. Two
    Quotient values built from the same set of members are equal and
    hash-equal (dataclass equality over `members`), regardless of which
    member anyone later chooses to display. Picking a representative for
    display is exclusively `views.representative`'s job; nothing in
    model.py or semantics.py may treat one member as more the class than
    another.
    """

    members: frozenset[str]


@dataclass(frozen=True)
class Atom:
    # A plain option/atom name, or a Quotient if this position has been
    # identified with others by a prior COLLAPSE.
    name: str | Quotient


@dataclass(frozen=True)
class Sphere:
    items: tuple[Expr, ...]
    # Appendix G: <Sphere> ::= "(" <Label> ":" <Expr>* ")" -- a sphere is a
    # labeled enclosure. Optional and defaulted to None here so the lab's
    # existing unlabeled convenience syntax ("(A B C)", via spherepop.parser)
    # keeps working unchanged; spherepop.grammar's parser, which implements
    # Appendix G's own concrete syntax literally, always supplies a label.
    label: str | None = None


Expr = Atom | Sphere


@dataclass(frozen=True)
class PopOp:
    # Exactly one of path/label should be given; neither means "auto-select
    # the deepest non-root sphere" (a lab convenience default -- Appendix
    # G's own grammar requires an explicit Label always). Mutual-exclusion
    # is enforced in semantics.transition, not here, to keep error
    # reporting consistent with the rest of the primitive checks (EvalError).
    path: tuple[int, ...] | None = None
    label: str | None = None


@dataclass(frozen=True)
class RefuseOp:
    refused: frozenset[str]
    # Appendix G's <Refusal> ::= "refuse" "(" <Label> "," <Set> ")" takes a
    # Label. Recorded here and on the resulting event for provenance; it
    # does not yet select among multiple option spaces -- REFUSE still acts
    # on Config's single global option_space (see README: Plan A vs Plan B).
    label: str | None = None


@dataclass(frozen=True)
class BindOp:
    predicate: str
    label: str | None = None


@dataclass(frozen=True)
class CollapseOp:
    classes: tuple[frozenset[str], ...]
    label: str | None = None


Operation = PopOp | RefuseOp | BindOp | CollapseOp


@dataclass(frozen=True)
class PopEvent:
    history_index: int
    path: tuple[int, ...]
    label: str | None = None


@dataclass(frozen=True)
class RefuseEvent:
    history_index: int
    refused: frozenset[str]
    label: str | None = None


@dataclass(frozen=True)
class BindEvent:
    history_index: int
    predicate: str
    label: str | None = None


@dataclass(frozen=True)
class CollapseEvent:
    history_index: int
    classes: tuple[frozenset[str], ...]
    label: str | None = None


Event = PopEvent | RefuseEvent | BindEvent | CollapseEvent


@dataclass(frozen=True)
class Config:
    sigma: Sphere
    history: tuple[Event, ...]
    # Elements are plain option strings, or Quotients once COLLAPSE has
    # merged some of them into an equivalence class.
    option_space: frozenset[str | Quotient]
    collapse_log: tuple[tuple[int, tuple[frozenset[str], ...]], ...] = ()


def make_config(sigma: Sphere, option_space: frozenset[str] | set[str]) -> Config:
    return Config(sigma=sigma, history=(), option_space=frozenset(option_space), collapse_log=())
