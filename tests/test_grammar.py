import unittest

from spherepop import eval_program, extensional_view, make_config, render_expr, transition
from spherepop.grammar import GrammarError, parse_event, parse_expr, parse_sphere
from spherepop.model import Atom, BindOp, CollapseOp, PopOp, RefuseOp, Sphere


class GrammarTests(unittest.TestCase):
    def test_parse_sphere_carries_a_real_label(self):
        sp = parse_sphere("(outer: A (inner: B C) D)")
        self.assertEqual(sp.label, "outer")
        self.assertEqual(render_expr(sp), "(A (B C) D)")
        inner = sp.items[1]
        self.assertIsInstance(inner, Sphere)
        self.assertEqual(inner.label, "inner")

    def test_parse_expr_atom_is_unlabeled_value(self):
        self.assertEqual(parse_expr("x1"), Atom("x1"))
        self.assertEqual(parse_expr("42"), Atom("42"))

    def test_parse_sphere_rejects_bare_atom_at_top_level(self):
        with self.assertRaises(GrammarError):
            parse_sphere("x1")

    def test_parse_sphere_requires_colon_after_label(self):
        with self.assertRaises(GrammarError):
            parse_sphere("(outer A B)")

    def test_parse_event_pop(self):
        op = parse_event("pop(inner)")
        self.assertEqual(op, PopOp(label="inner"))

    def test_parse_event_refuse(self):
        op = parse_event("refuse(outer, {a1, a2})")
        self.assertIsInstance(op, RefuseOp)
        self.assertEqual(op.label, "outer")
        self.assertEqual(op.refused, frozenset({"a1", "a2"}))

    def test_parse_event_bind(self):
        op = parse_event("bind(outer, ALL)")
        self.assertEqual(op, BindOp(predicate="ALL", label="outer"))

    def test_parse_event_collapse_closes_pairs_transitively(self):
        # a~b, b~c should merge into one class {a,b,c}, not two overlapping
        # pairs -- ~ and disjoint classes are the same equivalence relation.
        op = parse_event("collapse(outer, {a~b, b~c})")
        self.assertIsInstance(op, CollapseOp)
        self.assertEqual(op.label, "outer")
        self.assertEqual(op.classes, (frozenset({"a", "b", "c"}),))

    def test_parse_event_collapse_multiple_disjoint_pairs(self):
        op = parse_event("collapse(outer, {a~b, x~y})")
        self.assertIsInstance(op, CollapseOp)
        self.assertEqual(set(op.classes), {frozenset({"a", "b"}), frozenset({"x", "y"})})

    def test_parse_event_unknown_keyword(self):
        with self.assertRaises(GrammarError):
            parse_event("merge(outer, {a,b})")

    def test_grammar_labeled_pop_runs_through_ordinary_transition(self):
        sigma = parse_sphere("(outer: A (inner: B C) D)")
        cfg = make_config(sigma, {"x"})
        out = transition(cfg, parse_event("pop(inner)"))
        self.assertEqual(render_expr(out.sigma), "(A B C D)")
        # inner's label dissolves with it; outer's persists on the rebuilt root.
        self.assertEqual(out.sigma.label, "outer")

    def test_grammar_events_compose_with_eval_program(self):
        sigma = parse_sphere("(outer: A (inner: B C) D)")
        cfg = make_config(sigma, {"a1", "a2", "b1"})
        program = [
            parse_event("refuse(outer, {a2})"),
            parse_event("bind(outer, ALL)"),
            parse_event("pop(inner)"),
        ]
        out = eval_program(cfg, program)
        self.assertEqual(extensional_view(out), ("(A B C D)", ("a1", "b1")))
        # Appendix G provenance: each event records the label it named.
        self.assertEqual([e.label for e in out.history], ["outer", "outer", "inner"])

    def test_tokenize_unexpected_character(self):
        """Tokenizer rejects unexpected characters."""
        with self.assertRaises(GrammarError):
            parse_expr("(root: $ invalid)")

    def test_parse_expr_unexpected_end(self):
        """Parser rejects unexpected end of input."""
        with self.assertRaises(GrammarError):
            parse_expr("(root:")

    def test_parse_sphere_non_ident_label(self):
        """Sphere label must be identifier."""
        with self.assertRaises(GrammarError):
            parse_expr("(123: A B)")

    def test_parse_sphere_missing_close_paren(self):
        """Sphere requires closing paren."""
        with self.assertRaises(GrammarError):
            parse_expr("(root: A B")

    def test_parse_expr_trailing_tokens(self):
        """Parser rejects trailing tokens."""
        with self.assertRaises(GrammarError):
            parse_expr("(root: A) extra")

    def test_parse_event_non_ident_keyword(self):
        """Event keyword must be identifier."""
        with self.assertRaises(GrammarError):
            parse_event("123(root)")

    def test_parse_event_non_ident_label(self):
        """Event label must be identifier."""
        with self.assertRaises(GrammarError):
            parse_event("pop(123)")

    def test_parse_event_bind_non_ident_predicate(self):
        """BIND predicate must be identifier."""
        with self.assertRaises(GrammarError):
            parse_event("bind(root, 123)")

    def test_parse_event_trailing_tokens(self):
        """Parser rejects trailing tokens after event."""
        with self.assertRaises(GrammarError):
            parse_event("pop(root) extra")


if __name__ == "__main__":
    unittest.main()
