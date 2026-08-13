"""Tests for spherepop.predicates module."""

from __future__ import annotations

import unittest

from spherepop.model import Quotient
from spherepop.predicates import predicate, string_test


class TestStringTest(unittest.TestCase):
    """Tests for string_test function."""

    def test_all_predicate(self) -> None:
        """ALL predicate matches everything."""
        test = string_test("ALL")
        self.assertTrue(test("anything"))
        self.assertTrue(test(""))
        self.assertTrue(test("user_id"))

    def test_prefix_predicate(self) -> None:
        """prefix: predicate matches strings with given prefix."""
        test = string_test("prefix:user")
        self.assertTrue(test("user"))
        self.assertTrue(test("user_id"))
        self.assertTrue(test("user_name"))
        self.assertFalse(test("admin"))
        self.assertFalse(test("use"))  # Doesn't match prefix
        self.assertFalse(test(""))

    def test_contains_predicate(self) -> None:
        """contains: predicate matches strings containing substring."""
        test = string_test("contains:_id")
        self.assertTrue(test("user_id"))
        self.assertTrue(test("admin_id"))
        self.assertTrue(test("_id"))
        self.assertTrue(test("a_id_b"))
        self.assertFalse(test("user"))
        self.assertFalse(test("id"))  # Must contain "_id", not just "id"

    def test_in_predicate(self) -> None:
        """in: predicate matches strings in explicit set."""
        test = string_test("in:a1,a2,a3")
        self.assertTrue(test("a1"))
        self.assertTrue(test("a2"))
        self.assertTrue(test("a3"))
        self.assertFalse(test("a4"))
        self.assertFalse(test("a"))
        self.assertFalse(test(""))

    def test_in_predicate_with_spaces(self) -> None:
        """in: predicate strips whitespace from members."""
        test = string_test("in: a1 , a2 , a3 ")
        self.assertTrue(test("a1"))
        self.assertTrue(test("a2"))
        self.assertTrue(test("a3"))
        self.assertFalse(test(" a1"))  # Doesn't match " a1" with space
        self.assertFalse(test("a1 "))

    def test_in_predicate_empty_members(self) -> None:
        """in: predicate ignores empty members."""
        test = string_test("in:a1,,a2,")
        self.assertTrue(test("a1"))
        self.assertTrue(test("a2"))
        self.assertFalse(test(""))

    def test_exact_match_predicate(self) -> None:
        """Any other string is treated as exact match."""
        test = string_test("user_id")
        self.assertTrue(test("user_id"))
        self.assertFalse(test("user"))
        self.assertFalse(test("user_id_2"))
        self.assertFalse(test("admin"))


class TestPredicate(unittest.TestCase):
    """Tests for predicate function (handles Quotients).

    Note: Quotient handling uses EXPERIMENTAL semantics.
    See THEORY_STATUS.md Q3 for discussion of alternatives.
    """

    def test_predicate_on_plain_strings(self) -> None:
        """Predicate works on plain strings like string_test."""
        pred = predicate("prefix:user")
        self.assertTrue(pred("user_id"))
        self.assertTrue(pred("user_name"))
        self.assertFalse(pred("admin"))

    def test_predicate_on_quotient_existential_true(self) -> None:
        """Quotient is admitted if any member matches (existential).

        **Theory Status**: EXPERIMENTAL - This tests provisional existential
        semantics for BIND predicates on Quotients. See THEORY_STATUS.md Q3.
        The paper (Appendix E) does not specify how predicates should lift
        to quotient classes. Alternatives: universal, well-defined on classes.
        """
        pred = predicate("prefix:user")
        q = Quotient(frozenset({"user_id", "admin"}))
        # Should be True because "user_id" matches even though "admin" doesn't
        self.assertTrue(pred(q))

    def test_predicate_on_quotient_existential_false(self) -> None:
        """Quotient is rejected if no members match."""
        pred = predicate("prefix:user")
        q = Quotient(frozenset({"admin", "guest"}))
        # Should be False because neither "admin" nor "guest" matches
        self.assertFalse(pred(q))

    def test_predicate_all_on_quotient(self) -> None:
        """ALL predicate admits any Quotient."""
        pred = predicate("ALL")
        q = Quotient(frozenset({"anything", "everything"}))
        self.assertTrue(pred(q))

    def test_predicate_exact_match_on_quotient(self) -> None:
        """Exact match predicate checks if target is in Quotient members."""
        pred = predicate("user_id")
        q1 = Quotient(frozenset({"user_id", "admin"}))
        q2 = Quotient(frozenset({"admin", "guest"}))
        self.assertTrue(pred(q1))  # "user_id" is a member
        self.assertFalse(pred(q2))  # "user_id" is not a member

    def test_predicate_contains_on_quotient(self) -> None:
        """contains: predicate with Quotient - existential semantics."""
        pred = predicate("contains:_id")
        q1 = Quotient(frozenset({"user_id", "admin"}))  # "user_id" contains "_id"
        q2 = Quotient(frozenset({"user", "admin"}))  # Neither contains "_id"
        self.assertTrue(pred(q1))
        self.assertFalse(pred(q2))

    def test_predicate_in_on_quotient(self) -> None:
        """in: predicate with Quotient - existential semantics."""
        pred = predicate("in:a1,a2,a3")
        q1 = Quotient(frozenset({"a1", "b1"}))  # "a1" is in the set
        q2 = Quotient(frozenset({"b1", "b2"}))  # Neither is in the set
        self.assertTrue(pred(q1))
        self.assertFalse(pred(q2))

    def test_predicate_empty_quotient(self) -> None:
        """Empty Quotient (edge case) - should never match."""
        # This is a degenerate case that shouldn't happen in practice
        # (Quotients are built from nonempty classes) but test it anyway
        pred = predicate("ALL")
        q = Quotient(frozenset())
        # Existential over empty set is False (no member matches)
        self.assertFalse(pred(q))


if __name__ == "__main__":
    unittest.main()
