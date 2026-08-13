"""Predicate logic for BIND operations.

This module defines the predicate DSL used by the BIND operation to filter
option spaces. Predicates are stated over plain strings but generalized to
handle Quotient elements (equivalence classes from COLLAPSE).

Predicate Syntax
----------------

The predicate DSL supports:

- ``"ALL"``: Matches any option (identity predicate)
- ``"prefix:X"``: Matches options starting with X
- ``"contains:X"``: Matches options containing X as a substring
- ``"in:A,B,C"``: Matches options in the explicit set {A, B, C}
- Exact match: Any other string matches only that exact option

Examples
--------

    >>> from spherepop.predicates import string_test, predicate
    >>> from spherepop.model import Quotient
    >>>
    >>> # String predicates
    >>> test = string_test("prefix:user")
    >>> test("user_id")
    True
    >>> test("admin")
    False
    >>>
    >>> # Quotient handling (existential semantics)
    >>> pred = predicate("prefix:user")
    >>> q = Quotient(frozenset({"user_id", "admin"}))
    >>> pred(q)  # True because "user_id" matches
    True

Quotient Handling
-----------------

When a BIND predicate encounters a Quotient (an option merged by a prior
COLLAPSE), it applies existential semantics: the Quotient is admitted if
*any* of its members would match the predicate.

This is a provisional modeling choice pending clarification in Appendix G.
The alternative (universal semantics: admit only if *all* members match)
would be more restrictive but potentially more intuitive for some use cases.

See Also
--------

- ``spherepop.semantics.transition`` : Uses predicates in BindOp handling
- ``spherepop.model.Quotient`` : Equivalence classes handled by predicates
"""

from __future__ import annotations

from collections.abc import Callable

from spherepop.model import Quotient


def string_test(spec: str) -> Callable[[str], bool]:
    """Build a predicate function that tests plain strings.

    This is the core predicate logic for BIND operations, stated over
    individual option names (plain strings). For handling Quotients, see
    :func:`predicate`.

    Parameters
    ----------
    spec : str
        Predicate specification using the DSL syntax:
        - ``"ALL"`` → matches everything
        - ``"prefix:X"`` → matches strings starting with X
        - ``"contains:X"`` → matches strings containing X
        - ``"in:A,B,C"`` → matches strings in {A, B, C}
        - Any other string → exact match only

    Returns
    -------
    Callable[[str], bool]
        A function that tests whether a string satisfies the predicate.

    Examples
    --------
    >>> test = string_test("prefix:user")
    >>> test("user_id")
    True
    >>> test("user_name")
    True
    >>> test("admin")
    False

    >>> test_in = string_test("in:a1,a2,a3")
    >>> test_in("a1")
    True
    >>> test_in("a4")
    False
    """
    if spec == "ALL":
        return lambda _: True
    if spec.startswith("prefix:"):
        prefix = spec.split(":", 1)[1]
        return lambda option: option.startswith(prefix)
    if spec.startswith("contains:"):
        chunk = spec.split(":", 1)[1]
        return lambda option: chunk in option
    if spec.startswith("in:"):
        members = {p.strip() for p in spec.split(":", 1)[1].split(",") if p.strip()}
        return lambda option: option in members
    return lambda option: option == spec


def predicate(spec: str) -> Callable[[str | Quotient], bool]:
    """Build a predicate function that handles both strings and Quotients.

    This generalizes :func:`string_test` to work with option-space elements
    that may be plain strings or Quotient equivalence classes (from prior
    COLLAPSE operations).

    For Quotients, this uses **existential semantics**: a Quotient is
    admitted if the predicate would admit *any* one of its members.

    **Theory Status**: This is **PROVISIONAL** semantics. The paper
    (Appendix E) does not specify how predicates should lift to quotient
    classes. See THEORY_STATUS.md Q3 for three plausible alternatives:
    existential (current), universal, or well-defined-on-classes.

    Parameters
    ----------
    spec : str
        Predicate specification (same DSL as :func:`string_test`).

    Returns
    -------
    Callable[[str | Quotient], bool]
        A function that tests option-space elements (strings or Quotients).

    Examples
    --------
    >>> from spherepop.model import Quotient
    >>> pred = predicate("prefix:user")
    >>> pred("user_id")  # Plain string
    True
    >>> pred("admin")
    False
    >>> q = Quotient(frozenset({"user_id", "admin"}))
    >>> pred(q)  # Quotient - existential: any member matches
    True

    Notes
    -----
    The existential reading for Quotients means that if even one member
    of a merged class would pass the predicate, the entire class is kept.
    This may be surprising in cases where you expect all members to match.

    Alternative (not implemented): Universal semantics would require *all*
    members to match before admitting the Quotient. This would make
    ``predicate("prefix:user")`` reject ``Quotient({"user_id", "admin"})``
    because "admin" doesn't match.

    See Also
    --------
    THEORY_STATUS.md : Full discussion of BIND predicate semantics
    """
    test = string_test(spec)

    def pred(option: str | Quotient) -> bool:
        if isinstance(option, Quotient):
            # Existential semantics: admit if any member matches
            return any(test(member) for member in option.members)
        return test(option)

    return pred
