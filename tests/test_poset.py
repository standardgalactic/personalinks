import unittest

from spherepop.poset import (
    OptionSpace,
    PosetError,
    extensionally_equivalent,
    minimal_elements,
    pop_minimal,
    preceq,
)


class PosetTests(unittest.TestCase):
    def test_preceq_is_reflexive_and_transitive(self):
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"x", "y"}))
        c = OptionSpace("c", frozenset({"x", "y", "z"}))
        self.assertTrue(preceq(a, a))
        self.assertTrue(preceq(a, b))
        self.assertTrue(preceq(b, c))
        self.assertTrue(preceq(a, c))  # transitivity

    def test_preceq_is_not_antisymmetric_at_object_identity(self):
        # Distinct labels, identical content: preceq holds both ways,
        # but these are not the same labeled scope.
        a = OptionSpace("scope-a", frozenset({"x", "y"}))
        b = OptionSpace("scope-b", frozenset({"x", "y"}))
        self.assertTrue(preceq(a, b))
        self.assertTrue(preceq(b, a))
        self.assertNotEqual(a, b)
        self.assertTrue(extensionally_equivalent(a, b))

    def test_extensionally_equivalent_requires_exact_content_equality(self):
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"x", "y"}))  # a strictly smaller, not equal
        self.assertTrue(preceq(a, b))
        self.assertFalse(preceq(b, a))
        self.assertFalse(extensionally_equivalent(a, b))

    def test_minimal_elements_basic_chain(self):
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"x", "y"}))
        c = OptionSpace("c", frozenset({"x", "y", "z"}))
        self.assertEqual(minimal_elements([a, b, c]), (a,))

    def test_minimal_elements_incomparable_different_content(self):
        # Disjoint local contexts: neither's content contains the other's.
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"y"}))
        c = OptionSpace("c", frozenset({"x", "y"}))
        self.assertEqual(set(minimal_elements([a, b, c])), {a, b})

    def test_minimal_elements_equal_content_different_labels_are_jointly_minimal(self):
        # The fix: two differently-labeled scopes with IDENTICAL content
        # must not disqualify one another. Neither's content is a
        # *strict* subset of the other's (they're equal), so both stay
        # minimal together.
        a = OptionSpace("scope-a", frozenset({"x"}))
        b = OptionSpace("scope-b", frozenset({"x"}))
        c = OptionSpace("c", frozenset({"x", "y"}))
        self.assertEqual(set(minimal_elements([a, b, c])), {a, b})

    def test_minimal_elements_strict_subset_still_excludes_equal_content_pair(self):
        # Equal-content scopes ARE excluded when something else has
        # strictly smaller content than both of them -- the equal-content
        # exception only protects scopes from disqualifying *each other*.
        a = OptionSpace("scope-a", frozenset({"x", "y"}))
        b = OptionSpace("scope-b", frozenset({"x", "y"}))
        smaller = OptionSpace("smaller", frozenset({"x"}))
        self.assertEqual(minimal_elements([a, b, smaller]), (smaller,))

    def test_pop_minimal_removes_only_the_named_label(self):
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"x", "y"}))
        result = pop_minimal([a, b], "a")
        self.assertEqual(result, (b,))
        # b's own content is untouched by the pop.
        self.assertEqual(result[0].content, frozenset({"x", "y"}))

    def test_pop_minimal_rejects_nonminimal_label(self):
        a = OptionSpace("a", frozenset({"x"}))
        b = OptionSpace("b", frozenset({"x", "y"}))
        with self.assertRaises(PosetError):
            pop_minimal([a, b], "b")

    def test_pop_minimal_rejects_unknown_label(self):
        a = OptionSpace("a", frozenset({"x"}))
        with self.assertRaises(PosetError):
            pop_minimal([a], "nonexistent")

    def test_pop_minimal_on_equal_content_pair_leaves_the_other_still_minimal(self):
        # After popping one of an equal-content minimal pair, the other
        # must remain a *valid* pop target -- it was never disqualified
        # by its sibling in the first place.
        a = OptionSpace("scope-a", frozenset({"x"}))
        b = OptionSpace("scope-b", frozenset({"x"}))
        after_a = pop_minimal([a, b], "scope-a")
        self.assertEqual(after_a, (b,))
        self.assertIn(b, minimal_elements(after_a))
        after_both = pop_minimal(after_a, "scope-b")
        self.assertEqual(after_both, ())


if __name__ == "__main__":
    unittest.main()
