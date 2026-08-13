"""Test views.py formatting and presentation functions.

Coverage targets (views.py):
- Lines 77-79: format_available_paths() edge cases
- Line 83: format_available_options() empty case
- Lines 108-109: format_available_options() large set formatting

These test read-only presentation functions that produce human-readable
output for errors and debugging.
"""

import pytest

from spherepop.model import Atom, Config, Quotient, Sphere
from spherepop.views import (
    extensional_view,
    format_available_options,
    format_available_paths,
    history_prefix_view,
    history_view,
    make_sphere,
    render_event,
    render_expr,
    representative,
)


class TestRepresentative:
    """Test representative() Quotient display function."""

    def test_representative_plain_string(self):
        """Plain strings pass through unchanged."""
        assert representative("option_a") == "option_a"
        assert representative("x") == "x"
        assert representative("zebra") == "zebra"

    def test_representative_quotient_picks_first_sorted(self):
        """Quotients display lexicographically first member."""
        q = Quotient(members=frozenset({"zebra", "apple", "banana"}))
        assert representative(q) == "apple"

    def test_representative_quotient_deterministic(self):
        """Same members produce same representative regardless of order."""
        q1 = Quotient(members=frozenset({"z", "x", "y"}))
        q2 = Quotient(members=frozenset({"x", "y", "z"}))
        assert representative(q1) == representative(q2) == "x"

    def test_representative_quotient_single_member(self):
        """Single-member Quotient returns that member."""
        q = Quotient(members=frozenset({"only"}))
        assert representative(q) == "only"


class TestRenderExpr:
    """Test render_expr() tree rendering."""

    def test_render_atom(self):
        """Atom renders as its name."""
        atom = Atom("a")
        assert render_expr(atom) == "a"

    def test_render_quotient_atom(self):
        """Atom with Quotient name renders representative."""
        q = Quotient(members=frozenset({"b", "a", "c"}))
        atom = Atom(q)
        assert render_expr(atom) == "a"  # Sorted first

    def test_render_empty_sphere(self):
        """Empty Sphere renders as empty parens."""
        sphere = Sphere(())
        assert render_expr(sphere) == "()"

    def test_render_nested_sphere(self):
        """Nested Spheres render recursively."""
        inner = Sphere((Atom("a"), Atom("b")))
        outer = Sphere((inner, Atom("c")))
        assert render_expr(outer) == "((a b) c)"


class TestRenderEvent:
    """Test render_event() history formatting."""

    def test_render_event_sorted_keys(self):
        """Events render with sorted keys for determinism."""
        from spherepop.model import PopEvent

        event = PopEvent(history_index=0, path=(0,), label=None)
        rendered = render_event(event)
        assert rendered.startswith("PopEvent(")
        assert "history_index=0" in rendered
        assert "path=(0,)" in rendered

    def test_render_event_preserves_repr(self):
        """Event rendering uses repr for values."""
        from spherepop.model import RefuseEvent

        event = RefuseEvent(history_index=1, refused=frozenset({"a", "b"}), label="test")
        rendered = render_event(event)
        assert "'test'" in rendered or '"test"' in rendered  # String repr


class TestHistoryView:
    """Test history_view() rendering."""

    def test_history_view_empty(self):
        """Empty history renders as empty tuple."""
        cfg = Config(sigma=Sphere((Atom("a"),)), option_space=frozenset({"a"}), history=())
        assert history_view(cfg) == ()

    def test_history_view_multiple_events(self):
        """Multiple events render in order."""
        from spherepop.model import PopEvent, RefuseEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(0,), label=None),
                RefuseEvent(history_index=1, refused=frozenset({"b"}), label=None),
            ),
        )
        result = history_view(cfg)
        assert len(result) == 2
        assert "PopEvent" in result[0]
        assert "RefuseEvent" in result[1]


class TestExtensionalView:
    """Test extensional_view() rendering."""

    def test_extensional_view_plain_strings(self):
        """Plain string options render sorted."""
        cfg = Config(
            sigma=Sphere((Atom("a"), Atom("b"))),
            option_space=frozenset({"b", "a", "c"}),
            history=(),
        )
        expr_render, opts = extensional_view(cfg)
        assert expr_render == "(a b)"
        assert opts == ("a", "b", "c")

    def test_extensional_view_with_quotients(self):
        """Quotients render via representative."""
        q = Quotient(members=frozenset({"z", "x", "y"}))
        cfg = Config(sigma=Sphere((Atom("a"),)), option_space=frozenset({"a", q}), history=())
        expr_render, opts = extensional_view(cfg)
        # q's representative is "x"
        assert opts == ("a", "x") or opts == ("x", "a")  # Sorted by repr


class TestHistoryPrefixView:
    """Test history_prefix_view() truncation."""

    def test_history_prefix_view_negative_length(self):
        """Negative length raises ValueError."""
        cfg = Config(sigma=Sphere((Atom("a"),)), option_space=frozenset({"a"}), history=())
        with pytest.raises(ValueError, match="non-negative"):
            history_prefix_view(cfg, -1)

    def test_history_prefix_view_zero_length(self):
        """Zero length returns empty tuple."""
        from spherepop.model import PopEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )
        assert history_prefix_view(cfg, 0) == ()

    def test_history_prefix_view_partial(self):
        """Partial prefix returns first N events."""
        from spherepop.model import PopEvent, RefuseEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(0,), label=None),
                RefuseEvent(history_index=1, refused=frozenset({"b"}), label=None),
                PopEvent(history_index=2, path=(1,), label=None),
            ),
        )
        result = history_prefix_view(cfg, 2)
        assert len(result) == 2
        assert "PopEvent" in result[0]
        assert "RefuseEvent" in result[1]

    def test_history_prefix_view_exceeds_length(self):
        """Prefix longer than history returns full history."""
        from spherepop.model import PopEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )
        result = history_prefix_view(cfg, 100)
        assert len(result) == 1


class TestMakeSphere:
    """Test make_sphere() convenience constructor."""

    def test_make_sphere_empty(self):
        """Empty args produce empty Sphere."""
        sphere = make_sphere()
        assert sphere.items == ()

    def test_make_sphere_multiple(self):
        """Multiple args produce Sphere with Atom children."""
        sphere = make_sphere("a", "b", "c")
        assert len(sphere.items) == 3
        assert all(isinstance(item, Atom) for item in sphere.items)
        assert [item.name for item in sphere.items] == ["a", "b", "c"]


class TestFormatAvailablePaths:
    """Test format_available_paths() error message formatting."""

    def test_format_available_paths_no_nested_spheres(self):
        """Sphere with no nested Spheres reports none available."""
        # Only root - no nested Spheres
        expr = Sphere((Atom("a"), Atom("b")))
        result = format_available_paths(expr)
        assert "no nested Spheres available" in result
        assert "only root" in result

    def test_format_available_paths_single_nested(self):
        """Single nested Sphere lists that path."""
        inner = Sphere((Atom("a"),), label="inner")
        expr = Sphere((inner, Atom("b")), label="root")
        result = format_available_paths(expr)
        assert "valid paths:" in result
        assert "(0,)" in result

    def test_format_available_paths_multiple_nested(self):
        """Multiple nested Spheres list all paths."""
        inner1 = Sphere((Atom("a"),), label="inner1")
        inner2 = Sphere((Atom("b"),), label="inner2")
        expr = Sphere((inner1, inner2), label="root")
        result = format_available_paths(expr)
        assert "valid paths:" in result
        assert "(0,)" in result
        assert "(1,)" in result

    def test_format_available_paths_deeply_nested(self):
        """Deeply nested Spheres show all paths."""
        deepest = Sphere((Atom("a"),), label="deep")
        middle = Sphere((deepest,), label="middle")
        expr = Sphere((middle,), label="root")
        result = format_available_paths(expr)
        assert "(0,)" in result
        assert "(0, 0)" in result


class TestFormatAvailableOptions:
    """Test format_available_options() error message formatting."""

    def test_format_available_options_empty(self):
        """Empty option space reports empty."""
        result = format_available_options(frozenset())
        assert "option space is empty" in result

    def test_format_available_options_single(self):
        """Single option shows that option."""
        result = format_available_options(frozenset({"a"}))
        assert "available options:" in result
        assert "{a}" in result or "{'a'}" in result

    def test_format_available_options_few(self):
        """Few options (≤5) show all."""
        result = format_available_options(frozenset({"a", "b", "c"}))
        assert "available options:" in result
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_format_available_options_many(self):
        """Many options (>5) truncate with count."""
        large_set = frozenset(f"option_{i}" for i in range(20))
        result = format_available_options(large_set)
        assert "available options:" in result
        assert "..." in result
        assert "20 total" in result
        # Should show first 5 sorted
        assert "option_0" in result
        assert "option_1" in result

    def test_format_available_options_with_quotients(self):
        """Quotients display via representative."""
        q1 = Quotient(members=frozenset({"z", "x", "y"}))
        q2 = Quotient(members=frozenset({"b", "a", "c"}))
        result = format_available_options(frozenset({q1, q2, "d"}))
        # Representatives: "x" (from q1), "a" (from q2), "d"
        assert "a" in result
        assert "x" in result
        assert "d" in result

    def test_format_available_options_exactly_five(self):
        """Exactly 5 options show all without truncation."""
        opts = frozenset({"a", "b", "c", "d", "e"})
        result = format_available_options(opts)
        assert "..." not in result
        assert "total" not in result
        for opt in opts:
            assert opt in result

    def test_format_available_options_six_triggers_truncation(self):
        """Six options trigger truncation."""
        opts = frozenset({"a", "b", "c", "d", "e", "f"})
        result = format_available_options(opts)
        assert "..." in result
        assert "6 total" in result
