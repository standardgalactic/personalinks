"""Direct tests for internal functions to complete coverage.

Tests internal implementation details that are hard to trigger through
the public API but important for defensive programming.

These tests import and call private functions directly (violating
encapsulation) specifically to achieve complete branch coverage of
defensive checks.
"""

import pytest

from spherepop.model import Atom, Config, PopEvent, Sphere
from spherepop.semantics import EvalError, _pop_path, history_is_prefix


class TestPopPathInternal:
    """Direct tests for _pop_path internal defensive checks."""

    def test_pop_path_target_not_sphere_at_recursion_end(self):
        """Internal check: target node at recursion end must be Sphere."""
        # Create structure where path ends at an Atom
        sigma = Sphere((Atom("a"), Atom("b")), label="root")

        # Path (0,) ends at Atom("a"), not a Sphere
        # This is caught by line 44 in recurse() when target is empty
        with pytest.raises(EvalError, match="POP target must be a Sphere"):
            _pop_path(sigma, (0,))

    def test_pop_path_traverses_through_atom(self):
        """Internal check: path cannot traverse through Atom."""
        # Create structure with Atom that path tries to traverse
        sigma = Sphere((Atom("a"), Atom("b")), label="root")

        # Path (0, 0) tries to traverse through Atom("a")
        # This is caught by line 48 when node is not Sphere
        with pytest.raises(EvalError, match="POP path traverses through non-Sphere"):
            _pop_path(sigma, (0, 0))

    def test_pop_path_index_negative(self):
        """Internal check: negative indices rejected."""
        inner = Sphere((Atom("a"),), label="inner")
        sigma = Sphere((inner,), label="root")

        # Path with negative index
        with pytest.raises(EvalError, match="POP path is out of range"):
            _pop_path(sigma, (-1,))

    def test_pop_path_index_out_of_bounds(self):
        """Internal check: out-of-bounds indices rejected."""
        inner = Sphere((Atom("a"),), label="inner")
        sigma = Sphere((inner,), label="root")

        # Path (5,) - index 5 doesn't exist
        with pytest.raises(EvalError, match="POP path is out of range"):
            _pop_path(sigma, (5,))

    def test_pop_path_deep_traversal_through_atom(self):
        """Internal check: deep path through Atom rejected."""
        # Nested structure
        deepest = Sphere((Atom("a"),), label="deep")
        middle = Sphere((deepest, Atom("b")), label="middle")
        sigma = Sphere((middle,), label="root")

        # Path (0, 1, 0) tries to traverse through Atom("b")
        with pytest.raises(EvalError, match="POP path traverses through non-Sphere"):
            _pop_path(sigma, (0, 1, 0))

    def test_pop_path_result_not_sphere_defensive_check(self):
        """Internal check: result must be Sphere (line 70).

        This is a defensive assertion that should never trigger through
        normal code paths - the function guarantees a Sphere result.
        Cannot be triggered without patching the function itself.
        """
        # This defensive check (line 70) protects against internal
        # bugs in the recursion. It cannot be triggered through
        # valid inputs because recurse() always returns Sphere when
        # called from valid path.
        #
        # We document it exists but cannot test it without mocking.
        pass

    def test_pop_path_valid_single_level(self):
        """Valid single-level POP for comparison."""
        inner = Sphere((Atom("a"), Atom("b")), label="inner")
        sigma = Sphere((inner, Atom("c")), label="root")

        result = _pop_path(sigma, (0,))

        # Inner sphere contents promoted
        assert isinstance(result, Sphere)
        assert len(result.items) == 3
        assert result.label == "root"

    def test_pop_path_valid_multi_level(self):
        """Valid multi-level POP for comparison."""
        deepest = Sphere((Atom("x"),), label="deep")
        middle = Sphere((deepest,), label="middle")
        sigma = Sphere((middle,), label="root")

        result = _pop_path(sigma, (0, 0))

        # Deepest sphere contents promoted through middle
        assert isinstance(result, Sphere)
        middle_result = result.items[0]
        assert isinstance(middle_result, Sphere)


class TestHistoryIsPrefix:
    """Tests for history_is_prefix utility function."""

    def test_history_is_prefix_longer_old_history(self):
        """history_is_prefix returns False when old history is longer."""
        cfg_old = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(0,), label=None),
                PopEvent(history_index=1, path=(1,), label=None),
                PopEvent(history_index=2, path=(2,), label=None),
            ),
        )

        cfg_new = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )

        # Old history (3 events) > new history (1 event)
        assert history_is_prefix(cfg_old, cfg_new) is False

    def test_history_is_prefix_true_case(self):
        """history_is_prefix returns True when old is prefix."""
        cfg_old = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )

        cfg_new = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(0,), label=None),
                PopEvent(history_index=1, path=(1,), label=None),
            ),
        )

        assert history_is_prefix(cfg_old, cfg_new) is True

    def test_history_is_prefix_equal_histories(self):
        """history_is_prefix returns True when histories are equal."""
        cfg1 = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )

        cfg2 = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )

        assert history_is_prefix(cfg1, cfg2) is True

    def test_history_is_prefix_false_mismatch(self):
        """history_is_prefix returns False when histories diverge."""
        cfg_old = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )

        cfg_new = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(1,), label=None),  # Different path
            ),
        )

        assert history_is_prefix(cfg_old, cfg_new) is False


class TestGrammarInternals:
    """Direct tests for grammar.py internal error paths."""

    def test_cursor_pop_unexpected_end(self):
        """Test _Cursor.pop() when out of tokens (line 121)."""
        from spherepop.grammar import GrammarError, _Cursor

        # Create empty cursor
        cur = _Cursor([])

        with pytest.raises(GrammarError, match="unexpected end of input"):
            cur.pop()

    def test_parse_value_invalid_token_type(self):
        """Test _parse_value() with non-IDENT/NUMBER token (line 136)."""
        from spherepop.grammar import GrammarError, _Cursor, _Token

        # Create cursor with PUNCT token where value expected
        cur = _Cursor([_Token("PUNCT", "{")])

        from spherepop.grammar import _parse_value

        with pytest.raises(GrammarError, match="expected a Value"):
            _parse_value(cur)

    def test_parse_expr_peek_none(self):
        """Test _parse_expr() when peek() returns None (line 143)."""
        from spherepop.grammar import GrammarError, _Cursor

        # Empty cursor causes peek() to return None
        cur = _Cursor([])

        from spherepop.grammar import _parse_expr

        with pytest.raises(GrammarError, match="unexpected end of input while parsing"):
            _parse_expr(cur)
