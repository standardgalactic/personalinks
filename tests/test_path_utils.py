"""Tests for spherepop.path_utils module."""

from __future__ import annotations

import unittest

from spherepop.model import Atom, Sphere
from spherepop.path_utils import (
    PathError,
    all_sphere_paths,
    deepest_non_root_sphere,
    expr_at,
    find_label_path,
    path_exists,
)


class TestPathExists(unittest.TestCase):
    """Tests for path_exists function."""

    def test_root_path_exists(self) -> None:
        """Empty path always refers to root and exists."""
        s = Sphere((Atom("a"),))
        self.assertTrue(path_exists(s, ()))

    def test_valid_single_step_path(self) -> None:
        """Valid single-step path exists."""
        s = Sphere((Atom("a"), Atom("b")))
        self.assertTrue(path_exists(s, (0,)))
        self.assertTrue(path_exists(s, (1,)))

    def test_invalid_out_of_range(self) -> None:
        """Out-of-range index returns False."""
        s = Sphere((Atom("a"), Atom("b")))
        self.assertFalse(path_exists(s, (2,)))
        self.assertFalse(path_exists(s, (-1,)))

    def test_cannot_traverse_through_atom(self) -> None:
        """Cannot traverse through an Atom."""
        s = Sphere((Atom("a"),))
        self.assertFalse(path_exists(s, (0, 0)))

    def test_nested_sphere_path(self) -> None:
        """Can traverse through nested Spheres."""
        inner = Sphere((Atom("a"), Atom("b")))
        outer = Sphere((inner, Atom("c")))
        self.assertTrue(path_exists(outer, (0,)))
        self.assertTrue(path_exists(outer, (0, 0)))
        self.assertTrue(path_exists(outer, (0, 1)))
        self.assertFalse(path_exists(outer, (0, 2)))


class TestAllSpherePaths(unittest.TestCase):
    """Tests for all_sphere_paths function."""

    def test_single_sphere_returns_root_only(self) -> None:
        """Sphere with only Atoms returns just the root path."""
        s = Sphere((Atom("a"), Atom("b")))
        paths = all_sphere_paths(s)
        self.assertEqual(paths, [()])

    def test_nested_sphere_returns_both(self) -> None:
        """Nested Sphere returns paths to both."""
        inner = Sphere((Atom("a"),))
        outer = Sphere((inner, Atom("b")))
        paths = all_sphere_paths(outer)
        self.assertIn((), paths)  # Root
        self.assertIn((0,), paths)  # Inner
        self.assertEqual(len(paths), 2)

    def test_multiple_nested_spheres(self) -> None:
        """Multiple nested Spheres all get paths."""
        inner1 = Sphere((Atom("a"),))
        inner2 = Sphere((Atom("b"),))
        outer = Sphere((inner1, inner2))
        paths = all_sphere_paths(outer)
        self.assertIn((), paths)
        self.assertIn((0,), paths)
        self.assertIn((1,), paths)
        self.assertEqual(len(paths), 3)

    def test_atom_at_root_returns_empty_list(self) -> None:
        """Atom at root returns no paths (no Spheres)."""
        a = Atom("x")
        paths = all_sphere_paths(a)
        self.assertEqual(paths, [])


class TestDeepestNonRootSphere(unittest.TestCase):
    """Tests for deepest_non_root_sphere function."""

    def test_single_nested_sphere(self) -> None:
        """Single nested Sphere is deepest."""
        inner = Sphere((Atom("a"),))
        outer = Sphere((inner,))
        path = deepest_non_root_sphere(outer)
        self.assertEqual(path, (0,))

    def test_multiple_at_same_depth_returns_first(self) -> None:
        """Multiple Spheres at same depth: return lexicographically first."""
        inner1 = Sphere((Atom("a"),))
        inner2 = Sphere((Atom("b"),))
        outer = Sphere((inner1, inner2))
        path = deepest_non_root_sphere(outer)
        self.assertEqual(path, (0,))  # (0,) comes before (1,)

    def test_deeply_nested_sphere(self) -> None:
        """Deepest Sphere wins even if others exist."""
        deep = Sphere((Atom("a"),))
        middle = Sphere((deep,))
        shallow = Sphere((Atom("b"),))
        outer = Sphere((middle, shallow))
        path = deepest_non_root_sphere(outer)
        self.assertEqual(path, (0, 0))  # Depth 2 beats depth 1

    def test_no_nested_spheres_raises(self) -> None:
        """Sphere with no nested Spheres raises PathError."""
        s = Sphere((Atom("a"), Atom("b")))
        with self.assertRaises(PathError) as cm:
            deepest_non_root_sphere(s)
        self.assertIn("at least one nested Sphere", str(cm.exception))


class TestFindLabelPath(unittest.TestCase):
    """Tests for find_label_path function."""

    def test_find_labeled_sphere(self) -> None:
        """Finds the Sphere with the given label."""
        inner = Sphere((Atom("a"),), label="inner")
        outer = Sphere((inner, Atom("b")), label="outer")
        path = find_label_path(outer, "inner")
        self.assertEqual(path, (0,))

    def test_label_not_found_raises(self) -> None:
        """Non-existent label raises PathError."""
        s = Sphere((Atom("a"),), label="foo")
        with self.assertRaises(PathError) as cm:
            find_label_path(s, "bar")
        self.assertIn("no Sphere labeled 'bar'", str(cm.exception))

    def test_ambiguous_label_raises(self) -> None:
        """Duplicate label raises PathError."""
        inner1 = Sphere((Atom("a"),), label="dup")
        inner2 = Sphere((Atom("b"),), label="dup")
        outer = Sphere((inner1, inner2))
        with self.assertRaises(PathError) as cm:
            find_label_path(outer, "dup")
        self.assertIn("ambiguous", str(cm.exception))

    def test_label_on_root_is_ignored(self) -> None:
        """Label on root Sphere is not found (root can't be POPped)."""
        s = Sphere((Atom("a"),), label="root_label")
        with self.assertRaises(PathError):
            find_label_path(s, "root_label")

    def test_find_deeply_nested_label(self) -> None:
        """Can find labels in deeply nested structures."""
        deep = Sphere((Atom("a"),), label="target")
        middle = Sphere((deep,))
        outer = Sphere((middle,))
        path = find_label_path(outer, "target")
        self.assertEqual(path, (0, 0))


class TestExprAt(unittest.TestCase):
    """Tests for expr_at function."""

    def test_root_path_returns_root(self) -> None:
        """Empty path returns the root expression itself."""
        s = Sphere((Atom("a"),))
        result = expr_at(s, ())
        self.assertEqual(result, s)

    def test_single_step_to_atom(self) -> None:
        """Single step can navigate to an Atom."""
        a = Atom("target")
        s = Sphere((a, Atom("other")))
        result = expr_at(s, (0,))
        self.assertEqual(result, a)

    def test_single_step_to_sphere(self) -> None:
        """Single step can navigate to a nested Sphere."""
        inner = Sphere((Atom("a"),))
        outer = Sphere((inner,))
        result = expr_at(outer, (0,))
        self.assertEqual(result, inner)

    def test_multi_step_path(self) -> None:
        """Multi-step path navigates through structure."""
        target = Atom("target")
        inner = Sphere((target,))
        outer = Sphere((inner,))
        result = expr_at(outer, (0, 0))
        self.assertEqual(result, target)

    def test_invalid_path_raises(self) -> None:
        """Invalid path raises AssertionError."""
        s = Sphere((Atom("a"),))
        # Out of range
        with self.assertRaises(AssertionError):
            expr_at(s, (5,))
        # Traverse through Atom
        with self.assertRaises(AssertionError):
            expr_at(s, (0, 0))


if __name__ == "__main__":
    unittest.main()
