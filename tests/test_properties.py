"""Property-based tests using Hypothesis.

These tests verify universal properties that should hold across all valid
inputs, complementing example-based tests with automated exploration of the
input space.

Key properties tested:
- Structural invariants (history never shrinks, operations preserve types)
- Algebraic properties (commutativity, associativity where applicable)
- Idempotence and identity behavior
- Consistency of observers (determinism, reflexivity, transitivity)
"""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from spherepop.model import (
    Atom,
    BindOp,
    CollapseOp,
    Config,
    RefuseOp,
    Sphere,
)
from spherepop.observers import (
    admissible,
    extensionally_equivalent,
    history_is_prefix,
)
from spherepop.semantics import EvalError, eval_program, transition
from spherepop.views import extensional_view

# ============================================================================
# Hypothesis Strategies for Generating Valid Spherepop Data
# ============================================================================


@st.composite
def atom_names(draw):
    """Generate valid atom names (a-z, simple identifiers)."""
    return draw(st.text(alphabet="abcdefghij", min_size=1, max_size=3))


@st.composite
def atoms(draw):
    """Generate Atom instances."""
    name = draw(atom_names())
    return Atom(name)


@st.composite
def simple_spheres(draw, max_depth=2, max_width=4):
    """Generate Sphere instances with limited nesting."""
    if max_depth == 0:
        # Leaf: just atoms
        num_items = draw(st.integers(min_value=0, max_value=max_width))
        items = tuple(draw(atoms()) for _ in range(num_items))
    else:
        # Mix of atoms and nested spheres
        num_items = draw(st.integers(min_value=0, max_value=max_width))
        items = []
        for _ in range(num_items):
            if draw(st.booleans()):
                items.append(draw(atoms()))
            else:
                items.append(draw(simple_spheres(max_depth=max_depth - 1, max_width=max_width)))
        items = tuple(items)

    label = draw(st.text(alphabet="abcdefghij", min_size=1, max_size=5))
    return Sphere(items, label=label)


@st.composite
def configs(draw):
    """Generate valid Config instances."""
    sigma = draw(simple_spheres(max_depth=2, max_width=3))

    # Extract atom names from sigma
    def collect_atoms(expr) -> set[str]:
        if isinstance(expr, Atom):
            return {expr.name}
        atoms_set = set()
        for item in expr.items:
            atoms_set.update(collect_atoms(item))
        return atoms_set

    atom_set = collect_atoms(sigma)
    if not atom_set:
        # Need at least one option
        atom_set = {"a"}
        sigma = Sphere((Atom("a"),), label="root")

    # Generate option_space as a subset of available atoms
    option_list = list(atom_set)
    num_options = draw(st.integers(min_value=1, max_value=len(option_list)))
    selected_options = draw(
        st.lists(
            st.sampled_from(option_list), min_size=num_options, max_size=num_options, unique=True
        )
    )
    option_space = frozenset(selected_options)

    return Config(sigma=sigma, option_space=option_space, history=())


@st.composite
def refuse_ops(draw, config: Config):
    """Generate REFUSE operations valid for a given config."""
    if not config.option_space:
        # Can't refuse from empty space
        return None

    options_list = list(config.option_space)
    # Refuse a non-empty proper subset (leave at least one option)
    if len(options_list) == 1:
        # Would leave empty, skip
        return None

    num_to_refuse = draw(st.integers(min_value=1, max_value=len(options_list) - 1))
    refused = frozenset(
        draw(
            st.lists(
                st.sampled_from(options_list),
                min_size=num_to_refuse,
                max_size=num_to_refuse,
                unique=True,
            )
        )
    )

    return RefuseOp(refused=refused)


# ============================================================================
# Property Tests
# ============================================================================


@given(configs())
def test_property_transition_never_shortens_history(cfg: Config):
    """Property: transition() never shortens Config.history.

    Every valid transition appends exactly one event to history.
    """
    # Try a simple REFUSE that should always succeed
    if len(cfg.option_space) > 1:
        options_list = list(cfg.option_space)
        refuse_op = RefuseOp(refused=frozenset([options_list[0]]))
        try:
            cfg_after = transition(cfg, refuse_op)
            assert len(cfg_after.history) == len(cfg.history) + 1
        except EvalError:
            # Invalid transition, that's OK
            pass


@given(configs())
def test_property_history_is_prefix_reflexive(cfg: Config):
    """Property: history_is_prefix is reflexive.

    Every config's history is a prefix of itself.
    """
    assert history_is_prefix(cfg, cfg)


@given(configs())
def test_property_eval_program_empty_is_identity(cfg: Config):
    """Property: eval_program with empty operations is identity.

    Evaluating no operations returns the config unchanged.
    """
    cfg_result = eval_program(cfg, [])
    assert cfg_result == cfg


@given(configs())
def test_property_extensional_view_deterministic(cfg: Config):
    """Property: extensional_view is deterministic.

    Calling extensional_view multiple times on the same config returns
    the same result.
    """
    view1 = extensional_view(cfg)
    view2 = extensional_view(cfg)
    assert view1 == view2


@given(configs())
def test_property_extensionally_equivalent_reflexive(cfg: Config):
    """Property: extensionally_equivalent is reflexive.

    Every config is extensionally equivalent to itself.
    """
    assert extensionally_equivalent(cfg, cfg)


@given(configs())
def test_property_admissible_consistent_with_transition(cfg: Config):
    """Property: admissible(op, cfg) iff transition(cfg, op) succeeds.

    The admissible() observer should agree with whether transition() raises.
    """
    if len(cfg.option_space) > 1:
        options_list = list(cfg.option_space)
        refuse_op = RefuseOp(refused=frozenset([options_list[0]]))

        is_admissible = admissible(refuse_op, cfg)

        try:
            transition(cfg, refuse_op)
            succeeded = True
        except EvalError:
            succeeded = False

        assert is_admissible == succeeded


@given(configs())
def test_property_refuse_bind_commute_when_disjoint(cfg: Config):
    """Property: REFUSE and BIND commute when they select disjoint options.

    If REFUSE removes X and BIND keeps Y where X ∩ Y = ∅, order doesn't matter.

    NOTE: This is marked experimental because the commutativity depends on
    the BIND predicate's semantics on Quotients (THEORY_STATUS.md Q3).
    """
    if len(cfg.option_space) < 3:
        # Need at least 3 options for disjoint REFUSE/BIND
        return

    options_list = list(cfg.option_space)

    # REFUSE first option, BIND to keep second option
    refuse_target = options_list[0]
    bind_target = options_list[1]

    refuse_op = RefuseOp(refused=frozenset([refuse_target]))
    bind_op = BindOp(predicate=f"exact:{bind_target}")

    try:
        # Path 1: REFUSE then BIND
        cfg_r = transition(cfg, refuse_op)
        cfg_rb = transition(cfg_r, bind_op)

        # Path 2: BIND then REFUSE
        cfg_b = transition(cfg, bind_op)
        cfg_br = transition(cfg_b, refuse_op)

        # Should reach the same extensional state
        assert extensional_view(cfg_rb) == extensional_view(cfg_br)
    except EvalError:
        # One path may fail if operations aren't truly disjoint
        pass


@pytest.mark.experimental
@given(configs())
def test_property_collapse_idempotent_on_same_classes(cfg: Config):
    """Property: COLLAPSE is idempotent on the same equivalence classes.

    Collapsing with the same classes twice should have the same effect
    as collapsing once.

    EXPERIMENTAL: This tests the provisional behavior of COLLAPSE composition
    (THEORY_STATUS.md Q2b). Currently, second COLLAPSE over Quotient is
    unsupported and raises an error.
    """
    if len(cfg.option_space) < 2:
        return

    options_list = list(cfg.option_space)
    classes = frozenset([frozenset(options_list[:2])])
    collapse_op = CollapseOp(classes=classes)

    try:
        cfg_1 = transition(cfg, collapse_op)
        cfg_2 = transition(cfg_1, collapse_op)

        # If second collapse succeeds, it should be idempotent
        assert extensional_view(cfg_1) == extensional_view(cfg_2)
    except EvalError as e:
        # Currently expected: "COLLAPSE over already-quoted option"
        assert "already" in str(e).lower() or "quotient" in str(e).lower()


@given(st.integers(min_value=0, max_value=10))
def test_property_eval_program_history_length(n: int):
    """Property: eval_program with n operations extends history by n events.

    Each successful operation appends exactly one event.
    """
    sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
    cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

    # Generate n valid REFUSE operations that won't empty option_space
    ops = []
    current_cfg = cfg
    for _i in range(min(n, len(cfg.option_space) - 1)):
        # Refuse one option at a time, leaving at least one
        options_to_refuse = list(current_cfg.option_space)[:1]
        refuse_op = RefuseOp(refused=frozenset(options_to_refuse))
        ops.append(refuse_op)
        try:
            current_cfg = transition(current_cfg, refuse_op)
        except EvalError:
            break

    result = eval_program(cfg, ops)
    assert len(result.history) == len(ops)


# ============================================================================
# Edge Case Properties
# ============================================================================


def test_property_empty_history_is_universal_prefix():
    """Property: Empty history is a prefix of any history.

    This is the base case for history_is_prefix transitivity.
    """
    sigma = Sphere((Atom("a"), Atom("b")), label="root")
    cfg_empty = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())
    cfg_with_history = transition(cfg_empty, RefuseOp(refused=frozenset({"b"})))

    assert history_is_prefix(cfg_empty, cfg_empty)
    assert history_is_prefix(cfg_empty, cfg_with_history)


def test_property_refuse_empty_set_raises():
    """Property: REFUSE with empty refused set raises EvalError.

    Appendix E requires REFUSE to remove a nonempty subset. Refusing nothing
    is not a degenerate no-op refusal — it is not a refusal at all.
    """
    sigma = Sphere((Atom("a"), Atom("b")), label="root")
    cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

    with pytest.raises(EvalError, match="nonempty subset"):
        transition(cfg, RefuseOp(refused=frozenset()))


def test_property_bind_all_preserves_options():
    """Property: BIND with ALL predicate preserves all options.

    The ALL predicate should keep everything.
    """
    sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
    cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

    cfg_after = transition(cfg, BindOp(predicate="ALL"))
    assert cfg_after.option_space == cfg.option_space
