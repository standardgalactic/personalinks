"""Path resolution and navigation utilities for Sphere expressions.

This module provides functions for navigating and querying the tree structure
of Sphere expressions using integer-indexed paths. Paths are represented as
tuples of integers, where each integer is an index into a Sphere's items.

Path Conventions
----------------

- The root Sphere is represented by the empty path ``()``
- A path ``(0,)`` refers to the first item of the root Sphere
- A path ``(1, 2)`` refers to the third item (index 2) of the second item
  (index 1) of the root Sphere
- The root Sphere itself cannot be POPped (only nested Spheres can be resolved)

Label Resolution
----------------

Spheres may carry optional labels (Appendix G). Label-based POP operations
resolve a label to a concrete path. Labels must be unique among non-root
Spheres to be unambiguous.

Examples
--------

    >>> from spherepop.model import Sphere, Atom
    >>> from spherepop.path_utils import path_exists, all_sphere_paths, expr_at
    >>>
    >>> # Build a nested structure
    >>> inner = Sphere((Atom("a"), Atom("b")))
    >>> outer = Sphere((Atom("x"), inner, Atom("y")))
    >>>
    >>> # Check path existence
    >>> path_exists(outer, ())  # Root always exists
    True
    >>> path_exists(outer, (1,))  # Second item (inner sphere)
    True
    >>> path_exists(outer, (5,))  # Out of range
    False
    >>>
    >>> # Find all Sphere paths
    >>> paths = all_sphere_paths(outer)
    >>> sorted(paths)
    [(), (1,)]
    >>>
    >>> # Navigate to an expression
    >>> expr = expr_at(outer, (1,))
    >>> expr == inner
    True

See Also
--------

- ``spherepop.semantics.transition`` : Uses these utilities for POP operations
- ``spherepop.model.Sphere`` : The tree structure being navigated
"""

from __future__ import annotations

from spherepop.model import Expr, Sphere


class PathError(ValueError):
    """Raised when a path operation fails (invalid path, label ambiguity, etc)."""

    pass


def path_exists(expr: Expr, path: tuple[int, ...]) -> bool:
    """Check whether a path is valid for a given expression.

    A path is valid if:
    1. Each step traverses through a Sphere (not an Atom)
    2. Each index is within the bounds of the Sphere's items

    Parameters
    ----------
    expr : Expr
        The root expression to check against.
    path : Tuple[int, ...]
        The path to validate (empty tuple for root).

    Returns
    -------
    bool
        True if the path can be traversed, False otherwise.

    Examples
    --------
    >>> from spherepop.model import Sphere, Atom
    >>> s = Sphere((Atom("a"), Atom("b")))
    >>> path_exists(s, ())
    True
    >>> path_exists(s, (0,))
    True
    >>> path_exists(s, (2,))  # Out of range
    False
    >>> path_exists(s, (0, 0))  # Can't traverse through Atom
    False
    """
    cursor = expr
    for idx in path:
        if not isinstance(cursor, Sphere):
            return False
        if idx < 0 or idx >= len(cursor.items):
            return False
        cursor = cursor.items[idx]
    return True


def all_sphere_paths(expr: Expr, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    """Find all paths that lead to Sphere nodes in an expression tree.

    This recursively traverses the expression tree and returns paths to
    every Sphere encountered, including the root (represented by the prefix).
    Atom nodes are not included in the results.

    Parameters
    ----------
    expr : Expr
        The root expression to search.
    prefix : Tuple[int, ...], optional
        Internal parameter for recursion (the path to this expr from root).

    Returns
    -------
    list[Tuple[int, ...]]
        Paths to all Sphere nodes. The empty path ``()`` represents the root
        if it's a Sphere. Order is depth-first: parent before children.

    Examples
    --------
    >>> from spherepop.model import Sphere, Atom
    >>> inner = Sphere((Atom("a"),))
    >>> outer = Sphere((inner, Atom("b")))
    >>> paths = all_sphere_paths(outer)
    >>> sorted(paths)
    [(), (0,)]
    """
    out: list[tuple[int, ...]] = []
    if isinstance(expr, Sphere):
        out.append(prefix)
        for idx, child in enumerate(expr.items):
            out.extend(all_sphere_paths(child, prefix + (idx,)))
    return out


def deepest_non_root_sphere(expr: Sphere) -> tuple[int, ...]:
    """Find the deepest nested non-root Sphere in an expression.

    This is used as a default when a POP operation doesn't specify a path
    or label: it resolves the most deeply nested Sphere. If multiple Spheres
    are tied for deepest, the lexicographically smallest path is chosen.

    Parameters
    ----------
    expr : Sphere
        The root Sphere to search.

    Returns
    -------
    Tuple[int, ...]
        Path to the deepest non-root Sphere.

    Raises
    ------
    PathError
        If there are no nested Spheres (only the root exists).

    Examples
    --------
    >>> from spherepop.model import Sphere, Atom
    >>> inner1 = Sphere((Atom("a"),))
    >>> inner2 = Sphere((Atom("b"),))
    >>> outer = Sphere((inner1, inner2))
    >>> deepest_non_root_sphere(outer)  # Both at depth 1, choose first
    (0,)
    >>>
    >>> deeper = Sphere((Atom("x"),))
    >>> middle = Sphere((deeper,))
    >>> root = Sphere((middle,))
    >>> deepest_non_root_sphere(root)  # Deepest is at depth 2
    (0, 0)

    Notes
    -----
    The root Sphere itself (path ``()``) is never returned, even if it's
    the only Sphere. This matches the semantics that the root cannot be
    POPped.
    """
    paths = [p for p in all_sphere_paths(expr) if p]  # Exclude root (empty path)
    if not paths:
        raise PathError("POP requires at least one nested Sphere to resolve")
    # Sort by depth (length) descending, then lexicographically ascending
    paths.sort(key=lambda p: (-len(p), p))
    return paths[0]


def find_label_path(expr: Sphere, label: str) -> tuple[int, ...]:
    """Resolve a label to the path of the Sphere carrying that label.

    This implements Appendix G's label-based POP resolution: ``pop(Label)``
    finds the Sphere with the given label and returns its path. The root
    Sphere is excluded from the search (it cannot be POPped, so a label on
    the root is not a valid POP target).

    **Theory Status**: Global label uniqueness is an **implementation choice**
    for concrete-syntax convenience, not a theoretical requirement. See
    THEORY_STATUS.md Q8. Appendix G does not mandate unique labels; scoped
    labels (e.g., ``root.left.x`` vs ``root.right.x``) would be plausible.

    Parameters
    ----------
    expr : Sphere
        The root Sphere to search.
    label : str
        The label to find.

    Returns
    -------
    Tuple[int, ...]
        Path to the Sphere carrying the label.

    Raises
    ------
    PathError
        If no Sphere has the label, or if multiple Spheres have it (ambiguous).

    Examples
    --------
    >>> from spherepop.model import Sphere, Atom
    >>> inner = Sphere((Atom("a"),), label="inner")
    >>> outer = Sphere((inner, Atom("b")), label="outer")
    >>> find_label_path(outer, "inner")
    (0,)

    Notes
    -----
    A label on the root Sphere is ignored (will raise PathError even if
    it matches) because the root cannot be POPped.
    """
    # Find all non-root Spheres with the given label
    matches = [
        p
        for p in all_sphere_paths(expr)
        if p  # Exclude root
        and isinstance(expr_at(expr, p), Sphere)
        and expr_at(expr, p).label == label  # type: ignore[union-attr]
    ]
    if not matches:
        raise PathError(f"no Sphere labeled {label!r} found")
    if len(matches) > 1:
        raise PathError(f"label {label!r} is ambiguous: {len(matches)} spheres carry it")
    return matches[0]


def expr_at(expr: Expr, path: tuple[int, ...]) -> Expr:
    """Navigate to the expression at a given path.

    This traverses the tree following the path indices and returns the
    expression at that location. The path must be valid (use :func:`path_exists`
    to check first, or catch the assertion failure).

    Parameters
    ----------
    expr : Expr
        The root expression to start from.
    path : Tuple[int, ...]
        The path to navigate (empty tuple returns the root itself).

    Returns
    -------
    Expr
        The expression (Atom or Sphere) at the path.

    Raises
    ------
    AssertionError
        If the path is invalid (traverses through an Atom or uses out-of-range index).

    Examples
    --------
    >>> from spherepop.model import Sphere, Atom
    >>> s = Sphere((Atom("a"), Atom("b")))
    >>> expr_at(s, ())  # Root
    Sphere(items=(Atom(name='a'), Atom(name='b')), label=None)
    >>> expr_at(s, (1,))  # Second item
    Atom(name='b')

    Notes
    -----
    This function uses assertions for path validation (assumes the caller
    has already verified the path is valid). For user-facing code, prefer
    checking with :func:`path_exists` first or using operations that raise
    :class:`PathError` explicitly.
    """
    cursor = expr
    for idx in path:
        assert isinstance(cursor, Sphere), f"Cannot traverse through non-Sphere at {path}"
        assert 0 <= idx < len(cursor.items), f"Index {idx} out of range at {path}"
        cursor = cursor.items[idx]
    return cursor
