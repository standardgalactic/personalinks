import unittest

from spherepop import make_config, parse_sphere, transition
from spherepop.model import BindOp, CollapseOp, PopOp, RefuseOp
from spherepop.observers import (
    admissible,
    confluent,
    divergent,
    equivalent_at,
    extensionally_equivalent,
    horizon_equivalent,
    intensionally_equivalent,
    irreducibly_divergent,
    regretful,
)


class ObserverTests(unittest.TestCase):
    def test_admissible_reports_without_mutating(self):
        flat = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
        before = (flat.history, flat.option_space, flat.sigma)
        self.assertFalse(admissible(PopOp(), flat))
        self.assertTrue(admissible(BindOp("ALL"), flat))
        self.assertEqual((flat.history, flat.option_space, flat.sigma), before)

    def test_confluent_identifies_under_stated_policy(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        left = transition(base, RefuseOp(frozenset({"a2"})))
        right = transition(base, RefuseOp(frozenset({"a1"})))
        identify_a = CollapseOp(classes=(frozenset({"a1", "a2"}),))
        self.assertTrue(confluent(left, right, identify_a))
        # applying the policy for analysis does not append it to either history
        self.assertEqual(len(left.history), 1)
        self.assertEqual(len(right.history), 1)

    def test_divergent_survives_unrelated_policy(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        left = transition(base, RefuseOp(frozenset({"a2"})))
        right = transition(base, RefuseOp(frozenset({"a1"})))
        unrelated = CollapseOp(classes=(frozenset({"b1", "b2"}),))
        self.assertTrue(divergent(left, right, unrelated))

    def test_divergent_is_negation_of_confluent(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        left = transition(base, RefuseOp(frozenset({"a2"})))
        right = transition(base, RefuseOp(frozenset({"a1"})))
        policy = CollapseOp(classes=(frozenset({"a1", "a2"}),))
        self.assertEqual(confluent(left, right, policy), not divergent(left, right, policy))

    def test_structural_divergence_survives_every_atom_policy(self):
        base = make_config(parse_sphere("(A (B C) D)"), {"x", "y"})
        left = transition(base, PopOp(path=(1,)))
        right = base
        self.assertTrue(divergent(left, right, CollapseOp(classes=(frozenset({"B", "C"}),))))
        self.assertTrue(divergent(left, right, CollapseOp(classes=(frozenset({"A", "D"}),))))

    def test_regretful_is_strict_subset_relative_to_common_prefix(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        narrow = transition(base, RefuseOp(frozenset({"a1", "a2"})))
        unrestricted = transition(base, BindOp("ALL"))
        incomparable = transition(base, BindOp("prefix:a"))

        self.assertTrue(regretful(base, narrow, unrestricted))
        self.assertFalse(regretful(base, narrow, incomparable))
        self.assertFalse(regretful(base, unrestricted, narrow))  # not smaller, so no regret

    def test_regretful_rejects_configs_without_common_prefix(self):
        # A base with at least one committed event, so the prefix check is
        # non-vacuous (an empty-history base is trivially a prefix of any
        # history -- see the caveat on regretful()).
        base0 = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        base = transition(base0, BindOp("ALL"))
        unrestricted = transition(base, BindOp("ALL"))
        unrelated = transition(make_config(parse_sphere("(X)"), {"z"}), RefuseOp(frozenset({"z"})))
        with self.assertRaises(ValueError):
            regretful(base, unrelated, unrestricted)

    def test_equivalent_at_prefix_then_parts_ways(self):
        base = make_config(parse_sphere("(A (B C) D)"), {"a1", "a2", "b1"})
        shared_prefix = [BindOp("contains:a"), RefuseOp(frozenset({"a2"}))]
        ops_left = shared_prefix + [PopOp(path=(1,))]
        ops_right = shared_prefix + [BindOp("ALL")]

        self.assertTrue(equivalent_at(base, ops_left, ops_right, 0))
        self.assertTrue(equivalent_at(base, ops_left, ops_right, 2))
        self.assertFalse(equivalent_at(base, ops_left, ops_right, 3))
        self.assertEqual(base.history, ())  # replay never touches base

    def test_equivalent_at_rejects_negative_k(self):
        base = make_config(parse_sphere("(A B)"), {"a1"})
        with self.assertRaises(ValueError):
            equivalent_at(base, [], [], -1)

    def test_irreducibly_divergent_over_a_policy_family(self):
        base = make_config(parse_sphere("(A (B C) D)"), {"x", "y"})
        left = transition(base, PopOp(path=(1,)))
        right = base
        policies = [
            CollapseOp(classes=(frozenset({"B", "C"}),)),
            CollapseOp(classes=(frozenset({"A", "D"}),)),
            CollapseOp(classes=(frozenset({"x", "y"}),)),
        ]
        self.assertTrue(irreducibly_divergent(left, right, policies))

    def test_irreducibly_divergent_fails_once_one_policy_identifies_them(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        left = transition(base, RefuseOp(frozenset({"a2"})))
        right = transition(base, RefuseOp(frozenset({"a1"})))
        policies = [
            CollapseOp(classes=(frozenset({"b1", "b2"}),)),  # unrelated: still divergent
            CollapseOp(classes=(frozenset({"a1", "a2"}),)),  # this one confluences them
        ]
        self.assertFalse(irreducibly_divergent(left, right, policies))

    def test_intensional_vs_extensional_equivalence(self):
        base = make_config(parse_sphere("(A (B C) D)"), {"A", "B", "C", "D"})
        h1 = transition(base, PopOp(path=(1,)))
        h2 = transition(base, BindOp("ALL"))
        h2 = transition(h2, PopOp(path=(1,)))
        self.assertFalse(intensionally_equivalent(h1, h2))
        self.assertTrue(extensionally_equivalent(h1, h2))

    def test_intensionally_equivalent_implies_extensionally_equivalent(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2"})
        left = transition(base, BindOp("ALL"))
        right = transition(base, BindOp("ALL"))
        self.assertTrue(intensionally_equivalent(left, right))
        self.assertTrue(extensionally_equivalent(left, right))

    def test_horizon_equivalent_reduces_to_extensional_at_k0(self):
        base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        other = transition(base, BindOp("ALL"))
        self.assertEqual(
            horizon_equivalent(base, other, [], 0), extensionally_equivalent(base, other)
        )

    def test_horizon_equivalent_can_hold_despite_differing_now(self):
        # Different right now (b1 vs c1), but under a candidate pool that
        # only cares about the "a" prefix, both futures coincide.
        left = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
        right = make_config(parse_sphere("(A B)"), {"a1", "a2", "c1"})
        self.assertFalse(extensionally_equivalent(left, right))
        candidate_ops = [BindOp("prefix:a")]
        self.assertTrue(horizon_equivalent(left, right, candidate_ops, 1))

    def test_horizon_equivalent_rejects_negative_k(self):
        base = make_config(parse_sphere("(A B)"), {"a1"})
        with self.assertRaises(ValueError):
            horizon_equivalent(base, base, [], -1)


if __name__ == "__main__":
    unittest.main()
