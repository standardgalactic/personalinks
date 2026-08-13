"""Tests for configuration validation.

Tests the advisory validation layer that diagnoses Config structural
invariants without altering configurations.
"""

from __future__ import annotations

import pytest

from spherepop import make_config, parse_sphere, transition
from spherepop.model import (
    Atom,
    BindOp,
    CollapseEvent,
    CollapseOp,
    Config,
    Quotient,
    RefuseEvent,
    RefuseOp,
    Sphere,
)
from spherepop.validation import assert_valid_config, validate_config

# ============================================================================
# Valid Configurations
# ============================================================================


def test_validate_simple_config():
    """Valid simple config passes all checks."""
    cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    violations = validate_config(cfg)
    assert violations == []


def test_validate_after_refuse():
    """Config after REFUSE is valid (option_space subset)."""
    cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    cfg_refused = transition(cfg, RefuseOp(refused=frozenset({"C"})))

    violations = validate_config(cfg_refused)
    assert violations == []


def test_validate_after_bind():
    """Config after BIND is valid (option_space subset)."""
    # Option names must match sigma atoms
    sigma = Sphere((Atom("a1"), Atom("a2"), Atom("b1")), label="root")
    cfg = make_config(sigma, {"a1", "a2", "b1"})
    cfg_bound = transition(cfg, BindOp(predicate="prefix:a"))

    violations = validate_config(cfg_bound)
    assert violations == []


def test_validate_after_collapse():
    """Config after COLLAPSE is valid (quotients with provenance)."""
    cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    cfg_collapsed = transition(cfg, CollapseOp(classes=(frozenset({"B", "C"}),)))

    violations = validate_config(cfg_collapsed)
    assert violations == []


def test_validate_nested_sigma():
    """Config with deeply nested sigma is valid."""
    sigma = Sphere(
        (
            Atom("a"),
            Sphere((Atom("b"), Sphere((Atom("c"), Atom("d")), label="inner")), label="middle"),
        ),
        label="root",
    )
    cfg = make_config(sigma, {"a", "b", "c", "d"})

    violations = validate_config(cfg)
    assert violations == []


# ============================================================================
# Invariant 1: Sigma Well-Formedness
# ============================================================================


def test_validate_detects_invalid_expr_type():
    """Validation detects non-Expr in sigma tree.

    Note: This is a pathological case that can't happen through normal API
    but validates the defensive checking in validation logic.
    """
    # Construct malformed sphere by bypassing type checks
    # Use object.__setattr__ to bypass frozen dataclass protection
    bad_sphere = Sphere.__new__(Sphere)
    object.__setattr__(bad_sphere, "items", (Atom("a"), "not_an_expr"))  # type: ignore
    object.__setattr__(bad_sphere, "label", "root")

    cfg = Config(sigma=bad_sphere, option_space=frozenset({"a"}), history=())

    violations = validate_config(cfg)
    assert any("is invalid: got str" in v for v in violations)


# ============================================================================
# Invariant 2: Option Provenance
# ============================================================================


def test_validate_detects_option_not_in_sigma():
    """Validation detects options not corresponding to sigma atoms."""
    cfg = Config(
        sigma=Sphere((Atom("A"), Atom("B")), label="root"),
        option_space=frozenset({"X", "Y"}),  # Not in sigma
        history=(),
    )

    violations = validate_config(cfg)
    assert any("not found in sigma atoms" in v for v in violations)
    assert any("'X'" in v for v in violations)


def test_validate_detects_invalid_quotient_member():
    """Validation detects Quotient members without provenance."""
    # Manually create Quotient with unprovable members
    bad_quotient = Quotient(members=frozenset({"phantom1", "phantom2"}))
    cfg = Config(
        sigma=Sphere((Atom("A"),), label="root"),
        option_space=frozenset({bad_quotient}),
        history=(),  # No collapse event to establish provenance
    )

    violations = validate_config(cfg)
    assert any("not found in sigma atoms or collapse provenance" in v for v in violations)


def test_validate_accepts_quotient_with_collapse_provenance():
    """Validation accepts Quotient when collapse history establishes provenance."""
    cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    cfg_collapsed = transition(cfg, CollapseOp(classes=(frozenset({"A", "B"}),)))

    # After COLLAPSE, quotient members have provenance via CollapseEvent
    violations = validate_config(cfg_collapsed)
    assert violations == []


# ============================================================================
# Invariant 3: History Sequential
# ============================================================================


def test_validate_detects_non_sequential_history_index():
    """Validation detects history events with wrong indices."""
    cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    cfg_step1 = transition(cfg, RefuseOp(refused=frozenset({"B"})))

    # Manually corrupt history index
    bad_event = RefuseEvent(history_index=99, refused=frozenset({"A"}), label=None)
    cfg_bad = Config(
        sigma=cfg_step1.sigma,
        option_space=cfg_step1.option_space,
        history=cfg_step1.history + (bad_event,),
    )

    violations = validate_config(cfg_bad)
    assert any("history_index=99, expected 1" in v for v in violations)


def test_validate_detects_missing_history_index():
    """Validation detects events missing history_index attribute."""

    # Create event-like object without history_index
    class FakeEvent:
        pass

    cfg = Config(
        sigma=Sphere((Atom("A"),), label="root"),
        option_space=frozenset({"A"}),
        history=(FakeEvent(),),  # type: ignore
    )

    violations = validate_config(cfg)
    assert any("missing history_index" in v for v in violations)


# ============================================================================
# Invariant 4: Collapse Log Consistency
# ============================================================================


def test_validate_detects_collapse_log_out_of_range():
    """Validation detects collapse_log indices beyond history length."""
    cfg = Config(
        sigma=Sphere((Atom("A"),), label="root"),
        option_space=frozenset({"A"}),
        history=(),
        collapse_log=((99, ()),),  # No events in history
    )

    violations = validate_config(cfg)
    assert any("collapse_log contains index 99" in v for v in violations)


def test_validate_detects_collapse_log_pointing_to_non_collapse():
    """Validation detects collapse_log pointing to non-CollapseEvent."""
    cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    cfg_refused = transition(cfg, RefuseOp(refused=frozenset({"B"})))

    # Manually add collapse_log pointing to RefuseEvent
    cfg_bad = Config(
        sigma=cfg_refused.sigma,
        option_space=cfg_refused.option_space,
        history=cfg_refused.history,
        collapse_log=((0, ()),),  # Points to RefuseEvent, not CollapseEvent
    )

    violations = validate_config(cfg_bad)
    assert any("points to RefuseEvent, not CollapseEvent" in v for v in violations)


# ============================================================================
# Invariant 5: Quotient Uniqueness
# ============================================================================


def test_validate_detects_duplicate_quotients():
    """Validation would detect duplicate Quotients, but frozenset prevents it.

    Note: Because Quotient uses dataclass equality (based on members), Python's
    frozenset automatically deduplicates equal Quotients. This test documents
    that the validation logic exists, even though it can't be triggered through
    normal Python operations.
    """
    q1 = Quotient(members=frozenset({"A", "B"}))
    q2 = Quotient(members=frozenset({"A", "B"}))

    # Verify Python semantics: equal quotients hash equal
    assert q1 == q2
    assert hash(q1) == hash(q2)

    # Therefore frozenset automatically deduplicates
    assert len(frozenset({q1, q2})) == 1

    # So this config is actually valid (only 1 quotient despite 2 references)
    cfg = Config(
        sigma=Sphere((Atom("A"), Atom("B")), label="root"),
        option_space=frozenset({q1, q2}),
        history=(CollapseEvent(history_index=0, classes=(frozenset({"A", "B"}),), label=None),),
    )

    violations = validate_config(cfg)
    assert violations == []  # Valid because frozenset deduplicated


# ============================================================================
# Invariant 6: Label Uniqueness
# ============================================================================


def test_validate_detects_duplicate_labels():
    """Validation detects non-unique Sphere labels (implementation choice Q8)."""
    sigma = Sphere(
        (
            Sphere((Atom("a"),), label="dup"),
            Sphere((Atom("b"),), label="dup"),  # Duplicate label
        ),
        label="root",
    )
    cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

    violations = validate_config(cfg)
    assert any("Label 'dup' appears at multiple paths" in v for v in violations)


def test_validate_accepts_none_labels():
    """Validation accepts Spheres with label=None (no uniqueness requirement)."""
    sigma = Sphere(
        (
            Sphere((Atom("a"),), label=None),
            Sphere((Atom("b"),), label=None),
        ),
        label="root",
    )
    cfg = make_config(sigma, {"a", "b"})

    violations = validate_config(cfg)
    assert violations == []


# ============================================================================
# Strict Validation Wrapper
# ============================================================================


def test_assert_valid_config_passes_valid():
    """assert_valid_config doesn't raise for valid config."""
    cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    assert_valid_config(cfg)  # Should not raise


def test_assert_valid_config_raises_invalid():
    """assert_valid_config raises ValueError for invalid config."""
    cfg = Config(
        sigma=Sphere((Atom("A"),), label="root"),
        option_space=frozenset({"X"}),  # Not in sigma
        history=(),
    )

    with pytest.raises(ValueError, match="Config validation failed"):
        assert_valid_config(cfg)


# ============================================================================
# Integration: Validation Throughout Normal Operations
# ============================================================================


def test_validate_sequence_of_operations():
    """Validation passes at each step of normal operation sequence."""
    sigma = Sphere((Atom("a1"), Atom("a2"), Atom("b1"), Atom("c1")), label="root")
    cfg = make_config(sigma, {"a1", "a2", "b1", "c1"})
    assert validate_config(cfg) == []

    cfg = transition(cfg, RefuseOp(refused=frozenset({"c1"})))
    assert validate_config(cfg) == []

    cfg = transition(cfg, BindOp(predicate="prefix:a"))
    assert validate_config(cfg) == []

    cfg = transition(cfg, CollapseOp(classes=(frozenset({"a1", "a2"}),)))
    assert validate_config(cfg) == []


def test_validate_does_not_alter_config():
    """Validation is purely observational - never alters config."""
    cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    original_sigma = cfg.sigma
    original_space = cfg.option_space
    original_history = cfg.history

    validate_config(cfg)

    assert cfg.sigma is original_sigma
    assert cfg.option_space is original_space
    assert cfg.history is original_history
