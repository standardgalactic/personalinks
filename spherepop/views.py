"""Derived read-only views.

Views are presentation/comparison functions that don't modify state.
The key principle: views.representative() is the ONLY place that may
choose which Quotient member to display for presentation.
"""

from __future__ import annotations

from spherepop.model import Atom, Config, Expr, Quotient, Sphere


def representative(value: str | Quotient) -> str:
    """The one place in this codebase permitted to pick a single member to
    stand in for a whole equivalence class, for display purposes only.

    This choice (sorted-first member) carries no semantic weight: it never
    feeds back into model.py or semantics.py, and it is not what equality,
    hashing, or admissibility checks use to compare Quotients.

    Examples:
        >>> from spherepop.model import Quotient
        >>> from spherepop.views import representative

        # Plain string passes through unchanged
        >>> representative("option_a")
        'option_a'

        # Quotient: pick lexicographically first member
        >>> q = Quotient(members=frozenset({"zebra", "apple", "banana"}))
        >>> representative(q)
        'apple'

        # Display choice is deterministic but semantically arbitrary
        >>> q2 = Quotient(members=frozenset({"x", "y", "z"}))
        >>> representative(q2)
        'x'

        # Equality and hashing use ALL members, not representatives
        >>> q3 = Quotient(members=frozenset({"z", "x", "y"}))
        >>> q2 == q3  # True: same members
        True
        >>> representative(q2) == representative(q3)  # Also 'x'
        True
    """
    if isinstance(value, Quotient):
        return sorted(value.members)[0]
    return value


def render_expr(expr: Expr) -> str:
    if isinstance(expr, Atom):
        return representative(expr.name)
    return "(" + " ".join(render_expr(item) for item in expr.items) + ")"


def render_event(event: object) -> str:
    attrs = event.__dict__
    details = ", ".join(f"{k}={attrs[k]!r}" for k in sorted(attrs.keys()))
    return f"{type(event).__name__}({details})"


def history_view(config: Config) -> tuple[str, ...]:
    return tuple(render_event(event) for event in config.history)


def extensional_view(config: Config) -> tuple[str, tuple[str, ...]]:
    # Sort by each option's display representative -- option_space itself
    # may hold a mix of plain strings and Quotients, which are not
    # mutually orderable.
    return render_expr(config.sigma), tuple(sorted(representative(o) for o in config.option_space))


def history_prefix_view(config: Config, length: int) -> tuple[str, ...]:
    if length < 0:
        raise ValueError("length must be non-negative")
    return tuple(render_event(event) for event in config.history[:length])


def make_sphere(*atoms: str) -> Sphere:
    return Sphere(tuple(Atom(a) for a in atoms))


def format_available_paths(expr: Sphere) -> str:
    """Format available Sphere paths for error messages.

    Helper for creating actionable error messages when a path is invalid.
    """
    from spherepop.path_utils import all_sphere_paths

    paths = [p for p in all_sphere_paths(expr) if p]  # Exclude root
    if not paths:
        return "no nested Spheres available (only root)"
    return f"valid paths: {', '.join(str(p) for p in sorted(paths))}"


def format_available_options(option_space: frozenset[str | Quotient]) -> str:
    """Format option space for error messages.

    Helper for creating actionable error messages when operations fail.
    """
    if not option_space:
        return "option space is empty"
    options = [representative(opt) for opt in option_space]
    if len(options) <= 5:
        return f"available options: {{{', '.join(sorted(options))}}}"
    sorted_opts = sorted(options)
    return f"available options: {{{', '.join(sorted_opts[:5])}, ... ({len(options)} total)}}"
