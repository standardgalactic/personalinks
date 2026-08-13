"""Read-only observers: propositions *about* histories, never events *in* them.

The four primitives in ``spherepop.semantics`` (POP, REFUSE, BIND, COLLAPSE)
are the only things that may append to a Config's history. Everything in
this module answers a question about one or more already-produced Configs
and returns a plain value (bool, or a small read-only structure) — it never
returns a Config for the caller to adopt as "the" continuation, and it never
mutates history_index bookkeeping or collapse_log in place.

    operations make history; experiments interrogate history.

Confluence, divergence, and regret are properties discovered about
histories under a stated policy or against a stated alternative — they are
deliberately *not* added as a fifth Operation, because doing so would erase
the distinction between the closed four-operator algebra and the questions
we ask of it.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from spherepop.model import CollapseOp, Config, Operation
from spherepop.semantics import EvalError, eval_program, history_is_prefix, transition
from spherepop.views import extensional_view


def admissible(op: Operation, config: Config) -> bool:
    """Whether `op` could be applied to `config` without raising.

    This attempts the transition and discards the result — it reports on
    admissibility without committing `op` to `config`'s history. Because
    Config is itself immutable, `config` is unaffected either way; the
    discipline here is about *usage*: callers must not treat this as a way
    to "peek" at the resulting sigma or option_space, only at whether the
    move is legal.
    """
    try:
        transition(config, op)
    except EvalError:
        return False
    return True


def confluent(left: Config, right: Config, policy: CollapseOp) -> bool:
    """Whether `left` and `right` can be explicitly identified under `policy`.

    Confluence is not something COLLAPSE produces as a side effect of
    ordinary evaluation — it is a claim about two independently-reached
    configurations, checked by applying the same stated policy to analysis
    copies of both and comparing the resulting extensional views. Neither
    `left` nor `right` is modified; `policy` is never appended to either
    history by this function.

    Examples:
        >>> from spherepop.model import Config, Sphere, Atom, CollapseOp, RefuseOp
        >>> from spherepop.semantics import transition
        >>> from spherepop.observers import confluent

        # Two paths reach different states
        >>> sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
        >>> cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

        >>> left = transition(cfg, RefuseOp(options=frozenset({"b"})))
        >>> right = transition(cfg, RefuseOp(options=frozenset({"c"})))
        >>> left.option_space  # {a, c}
        frozenset({'a', 'c'})
        >>> right.option_space  # {a, b}
        frozenset({'a', 'b'})

        # Policy that identifies all remaining options
        >>> policy = CollapseOp(classes=frozenset([
        ...     frozenset({"a", "b", "c"})  # Collapse everything
        ... ]))
        >>> confluent(left, right, policy)  # Both end up with single quotient
        True

        # But they're divergent without collapse
        >>> from spherepop.observers import divergent
        >>> divergent(left, right, CollapseOp(classes=frozenset()))
        True
    """
    left_after = transition(left, policy)
    right_after = transition(right, policy)
    return extensional_view(left_after) == extensional_view(right_after)


def divergent(left: Config, right: Config, policy: CollapseOp) -> bool:
    """Failure of confluence under `policy`.

    Divergence is not "no COLLAPSE could ever identify these" (that would
    require quantifying over all policies) — it is the negation of
    confluence under one stated policy, matching `confluent`'s scope.
    """
    return not confluent(left, right, policy)


def irreducibly_divergent(left: Config, right: Config, policies: Iterable[CollapseOp]) -> bool:
    """Whether `left` and `right` remain divergent under every policy in
    `policies`.

    This is divergence irreducible *relative to the given family* — not a
    proof of divergence under every policy that could ever be stated,
    which would require enumerating the full policy space. A structural
    divergence (different sigma shape; see experiment 16) is a case where
    this holds for essentially any atom-renaming policy, since COLLAPSE
    quotients atoms and cannot repair a difference in bracket structure —
    but that stronger claim is a fact about COLLAPSE's reach, not
    something this function tests directly.
    """
    return all(divergent(left, right, policy) for policy in policies)


def intensionally_equivalent(left: Config, right: Config) -> bool:
    """Whether `left` and `right` were reached by the exact same event
    sequence — identity of *how*, not just *what*."""
    return left.history == right.history


def extensionally_equivalent(left: Config, right: Config) -> bool:
    """Whether `left` and `right` look the same from the outside: same
    rendered sigma, same displayed option space — identity of *what*,
    indifferent to *how*. Two configurations can be extensionally
    equivalent while intensionally distinct (see experiment 20)."""
    return extensional_view(left) == extensional_view(right)


def regretful(base: Config, candidate: Config, alternative: Config) -> bool:
    """Whether `candidate` is a regretful continuation of `base`.

    Regret describes a history whose commitments leave a strictly smaller
    option space than another continuation reachable from the same prefix.
    `base` fixes what "the common prefix" means; both `candidate` and
    `alternative` must extend it (checked via `history_is_prefix`, the same
    prefix relation the core semantics already exposes). This raises rather
    than guessing at a shared ancestor, since silently comparing unrelated
    histories would misrepresent what regret is a claim about.

    Caveat: `history_is_prefix` treats an empty history as a prefix of any
    history, so a `base` with no committed events cannot rule out an
    unrelated `candidate` or `alternative` -- pass a `base` with at least
    one event already committed for this check to be non-vacuous.

    Examples:
        >>> from spherepop.model import Config, Sphere, Atom, RefuseOp
        >>> from spherepop.semantics import transition
        >>> from spherepop.observers import regretful

        # Start with three options
        >>> sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
        >>> base = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

        # Candidate: refuse two options, left with one
        >>> candidate = transition(base, RefuseOp(options=frozenset({"b", "c"})))
        >>> candidate.option_space
        frozenset({'a'})

        # Alternative: refuse only one option, left with two
        >>> alternative = transition(base, RefuseOp(options=frozenset({"c"})))
        >>> alternative.option_space
        frozenset({'a', 'b'})

        # Candidate is regretful: alternative has strictly more options
        >>> regretful(base, candidate, alternative)
        True

        # Not regretful if candidate has same or more options
        >>> regretful(base, alternative, candidate)
        False
    """
    if not history_is_prefix(base, candidate):
        raise ValueError("candidate does not continue from base")
    if not history_is_prefix(base, alternative):
        raise ValueError("alternative does not continue from base")
    return candidate.option_space < alternative.option_space


def equivalent_at(
    base: Config,
    ops_left: Iterable[Operation],
    ops_right: Iterable[Operation],
    k: int,
) -> bool:
    """Whether two *specific* operation sequences, replayed from `base`,
    agree at step k.

    This is a witness-level check over one stated pair of sequences, not
    Appendix F's `\u2248_k` (see `horizon_equivalent` for that): agreement of
    one pair of continuations does not establish that the full sets of
    k-step continuations coincide. Config does not retain a snapshot per
    history index, so agreement here is answered by replaying the first k
    operations of each sequence from the same base via `eval_program` and
    comparing extensional views. This is a read: it produces two
    disposable analysis Configs and returns a bool, and appends nothing to
    `base` itself.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    left = eval_program(base, list(ops_left)[:k])
    right = eval_program(base, list(ops_right)[:k])
    return extensional_view(left) == extensional_view(right)


def horizon_equivalent(
    left: Config,
    right: Config,
    candidate_ops: Sequence[Operation],
    k: int,
) -> bool:
    """Appendix F's h1 \u2248_k h2: whether `left` and `right` admit exactly the
    same *set* of extensional outcomes reachable by k further events, not
    merely whether one chosen pair of continuations happens to agree
    (that weaker, witness-level question is `equivalent_at`).

    The paper quantifies over "admissible events" without fixing a
    concrete alphabet; this lab requires the caller to supply a finite
    `candidate_ops` pool to quantify over, since enumerating every
    syntactically expressible Operation (arbitrary REFUSE sets, arbitrary
    BIND predicates, ...) is unbounded. The result is therefore \u2248_k
    *relative to* `candidate_ops` -- widening the pool can only grow each
    side's reachable set, never shrink it, so equivalence relative to a
    smaller pool does not imply equivalence relative to a larger one.

    Exponential in k and len(candidate_ops); fine for the small pools and
    small k this lab works with, not intended for production-scale search.
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    def reachable(config: Config, remaining: int) -> set[tuple[str, tuple[str, ...]]]:
        if remaining == 0:
            return {extensional_view(config)}
        outcomes: set[tuple[str, tuple[str, ...]]] = set()
        for op in candidate_ops:
            try:
                nxt = transition(config, op)
            except EvalError:
                continue
            outcomes |= reachable(nxt, remaining - 1)
        return outcomes

    return reachable(left, k) == reachable(right, k)
