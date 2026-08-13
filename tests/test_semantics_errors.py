"""Test error handling and edge cases in spherepop.semantics.

Coverage targets (semantics.py):
- Lines 39-70: Error handling in transition() and _pop_path()
- Lines 134-135: _pop helper edge cases
- Lines 207, 224: _bind and _refuse edge cases
- Line 252: Invalid operation type handling

These tests complement test_regressions.py which covers successful paths.
"""

import pytest

from spherepop.model import (
    Atom,
    BindOp,
    CollapseOp,
    Config,
    PopOp,
    Quotient,
    RefuseOp,
    Sphere,
)
from spherepop.semantics import EvalError, transition


class TestPopErrors:
    """Test POP operation error handling."""

    def test_pop_with_both_path_and_label(self):
        """PopOp must specify at most one of path or label."""
        sigma = Sphere((Sphere((Atom("a"),), label="inner"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        op = PopOp(path=(0,), label="inner")
        with pytest.raises(EvalError, match="specify at most one of path or label"):
            transition(cfg, op)

    def test_pop_nonexistent_path(self):
        """POP with path that doesn't exist raises EvalError."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Path (0,) would be valid, but (5,) is out of range
        op = PopOp(path=(5,))
        with pytest.raises(EvalError, match="POP path does not exist"):
            transition(cfg, op)

    def test_pop_empty_path_rejected(self):
        """POP with empty path (targeting root) is rejected."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        op = PopOp(path=())
        with pytest.raises(EvalError, match="POP must target a nested Sphere path, not the root"):
            transition(cfg, op)

    def test_pop_target_not_sphere(self):
        """POP target must be a Sphere, not Atom or Quotient."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Path (0,) targets Atom("a"), not a Sphere
        op = PopOp(path=(0,))
        with pytest.raises(EvalError, match="POP target must be a Sphere"):
            transition(cfg, op)

    def test_pop_path_through_non_sphere(self):
        """POP path traversing through non-Sphere node is rejected."""
        sigma = Sphere((Sphere((Atom("a"),), label="inner"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Path (1, 0) tries to traverse through Atom("b")
        op = PopOp(path=(1, 0))
        with pytest.raises(EvalError, match="POP path does not exist"):
            transition(cfg, op)

    def test_pop_index_out_of_range(self):
        """POP with index beyond sphere items raises EvalError."""
        sigma = Sphere((Sphere((Atom("a"),), label="inner"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        # Path (0, 5) - inner sphere only has 1 item
        op = PopOp(path=(0, 5))
        with pytest.raises(EvalError, match="POP path does not exist"):
            transition(cfg, op)

    def test_pop_nonexistent_label(self):
        """POP with label that doesn't exist raises EvalError."""
        sigma = Sphere((Sphere((Atom("a"),), label="inner"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        op = PopOp(label="nonexistent")
        with pytest.raises(EvalError, match="no Sphere labeled 'nonexistent' found"):
            transition(cfg, op)

    def test_pop_ambiguous_label(self):
        """POP with duplicate label raises EvalError."""
        sigma = Sphere(
            (
                Sphere((Atom("a"),), label="duplicate"),
                Sphere((Atom("b"),), label="duplicate"),
            ),
            label="root",
        )
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        op = PopOp(label="duplicate")
        with pytest.raises(EvalError, match="label 'duplicate' is ambiguous"):
            transition(cfg, op)


class TestRefuseErrors:
    """Test REFUSE operation edge cases."""

    def test_refuse_empty_option_space(self):
        """REFUSE on already-empty option space raises EvalError."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset(), history=())

        op = RefuseOp(refused=frozenset({"a"}))
        with pytest.raises(EvalError, match="nonempty subset of the current option space"):
            transition(cfg, op)

    def test_refuse_nonexistent_options(self):
        """REFUSE of options not in current space raises EvalError."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Try to refuse 'x' which doesn't exist
        op = RefuseOp(refused=frozenset({"x", "y"}))
        with pytest.raises(EvalError, match="nonempty subset of the current option space"):
            transition(cfg, op)

    def test_refuse_partial_overlap(self):
        """REFUSE with partial overlap succeeds, refusing only present options."""
        sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

        # Request to refuse 'b' and 'x' - only 'b' exists
        op = RefuseOp(refused=frozenset({"b", "x"}))
        result = transition(cfg, op)

        assert result.option_space == frozenset({"a", "c"})
        assert len(result.history) == 1
        # Event records only what was actually refused
        assert result.history[0].refused == frozenset({"b"})

    def test_refuse_with_quotient_refuses_class(self):
        """Refusing one member of a Quotient refuses the whole class."""
        sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

        # First COLLAPSE {a, b} into equivalence class
        collapse_op = CollapseOp(classes=(frozenset({"a", "b"}),))
        cfg_collapsed = transition(cfg, collapse_op)

        # Now option_space has Quotient([a,b]) and "c"
        assert len(cfg_collapsed.option_space) == 2

        # REFUSE "a" should remove the entire Quotient
        refuse_op = RefuseOp(refused=frozenset({"a"}))
        result = transition(cfg_collapsed, refuse_op)

        # Only "c" remains
        assert result.option_space == frozenset({"c"})


class TestBindErrors:
    """Test BIND operation edge cases."""

    def test_bind_empty_result(self):
        """BIND with predicate matching nothing produces empty option_space."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Predicate that matches nothing
        op = BindOp(predicate="prefix:x")
        result = transition(cfg, op)

        assert result.option_space == frozenset()
        assert len(result.history) == 1

    def test_bind_on_empty_option_space(self):
        """BIND on empty option_space produces empty result (not an error)."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset(), history=())

        op = BindOp(predicate="prefix:a")
        result = transition(cfg, op)

        assert result.option_space == frozenset()
        assert len(result.history) == 1

    def test_bind_unknown_format_becomes_exact_match(self):
        """BIND with unknown format uses exact match (default behavior)."""
        sigma = Sphere((Atom("a"), Atom("invalidformat")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "invalidformat"}), history=())

        # Unknown format becomes exact match for "invalidformat"
        op = BindOp(predicate="invalidformat")
        result = transition(cfg, op)

        # Should match only the exact string "invalidformat"
        assert result.option_space == frozenset({"invalidformat"})


class TestCollapseErrors:
    """Test COLLAPSE operation edge cases."""

    def test_collapse_empty_classes(self):
        """COLLAPSE with empty class set is allowed (no-op mapping)."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        op = CollapseOp(classes=())
        result = transition(cfg, op)

        # No change to option_space or sigma
        assert result.option_space == cfg.option_space
        assert result.sigma == cfg.sigma
        # But history records the event
        assert len(result.history) == 1

    def test_collapse_preserves_top_level_sphere(self):
        """COLLAPSE must maintain Sphere at top level."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        op = CollapseOp(classes=(frozenset({"a", "b"}),))
        result = transition(cfg, op)

        assert isinstance(result.sigma, Sphere)
        assert result.sigma.label == "root"

    def test_collapse_on_already_quotient(self):
        """Successive COLLAPSE leaves existing Quotients unchanged (Q2b)."""
        sigma = Sphere((Atom("a"), Atom("b"), Atom("c")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b", "c"}), history=())

        # First COLLAPSE: {a, b} → Quotient
        op1 = CollapseOp(classes=(frozenset({"a", "b"}),))
        cfg1 = transition(cfg, op1)

        # Second COLLAPSE: {b, c} → another class
        # Current implementation doesn't merge with existing Quotient
        op2 = CollapseOp(classes=(frozenset({"b", "c"}),))
        cfg2 = transition(cfg1, op2)

        # Quotient([a,b]) remains untouched; new Quotient([c]) created
        # This tests provisional semantics per THEORY_STATUS.md Q2b
        assert len(cfg2.option_space) == 2
        has_quotient_ab = any(
            isinstance(o, Quotient) and {"a", "b"} == set(o.members) for o in cfg2.option_space
        )
        assert has_quotient_ab


class TestInvalidOperationType:
    """Test handling of invalid operation types."""

    def test_invalid_operation_type(self):
        """Passing non-Operation type raises EvalError."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        # Pass something that's not an Operation
        with pytest.raises(EvalError, match="Unsupported operation type"):
            transition(cfg, "not an operation")  # type: ignore

    def test_none_operation(self):
        """Passing None as operation raises EvalError."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        with pytest.raises(EvalError, match="Unsupported operation type"):
            transition(cfg, None)  # type: ignore


class TestEvalProgram:
    """Test eval_program with error conditions."""

    def test_eval_program_propagates_errors(self):
        """Errors in eval_program propagate from transition()."""
        from spherepop.semantics import eval_program

        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        # Invalid POP path
        ops = [PopOp(path=(99,))]
        with pytest.raises(EvalError, match="POP path does not exist"):
            eval_program(cfg, ops)

    def test_eval_program_stops_at_first_error(self):
        """eval_program stops at first error, doesn't continue."""
        from spherepop.semantics import eval_program

        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        ops = [
            RefuseOp(refused=frozenset({"a"})),  # Valid
            PopOp(path=(99,)),  # Invalid - stops here
            RefuseOp(refused=frozenset({"b"})),  # Never reached
        ]

        with pytest.raises(EvalError):
            eval_program(cfg, ops)

        # Original config unchanged
        assert len(cfg.history) == 0


class TestEdgeCaseInteractions:
    """Test interactions between operations in edge cases."""

    def test_refuse_all_options(self):
        """REFUSE removing all options produces empty option_space."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        op = RefuseOp(refused=frozenset({"a", "b"}))
        result = transition(cfg, op)

        assert result.option_space == frozenset()

    def test_bind_then_refuse_empty(self):
        """BIND to empty, then REFUSE raises error."""
        sigma = Sphere((Atom("a"),), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a"}), history=())

        # BIND removes everything
        bind_op = BindOp(predicate="prefix:x")
        cfg1 = transition(cfg, bind_op)
        assert cfg1.option_space == frozenset()

        # Now REFUSE on empty space fails
        refuse_op = RefuseOp(refused=frozenset({"a"}))
        with pytest.raises(EvalError, match="nonempty subset"):
            transition(cfg1, refuse_op)

    def test_collapse_single_element_class(self):
        """COLLAPSE with single-element classes is allowed."""
        sigma = Sphere((Atom("a"), Atom("b")), label="root")
        cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())

        # Single-element class {a}
        op = CollapseOp(classes=(frozenset({"a"}),))
        result = transition(cfg, op)

        # Creates Quotient with single member
        assert len(result.option_space) == 2
        has_single_quotient = any(
            isinstance(o, Quotient) and len(o.members) == 1 for o in result.option_space
        )
        assert has_single_quotient
