"""Test parser.py error handling and edge cases.

Coverage targets (parser.py):
- Line 25: Pop on empty tokens (unexpected end)
- Lines 47, 60, 65, 70: parse_expr edge cases
- Lines 77, 84, 87-88, 90: parse_one error branches
- Lines 96, 101, 109: Operation parsing errors
- Lines 128, 133, 141: parse_program error handling

These test the lab convenience parser for simple expressions and operations.
For Appendix G's formal grammar, see grammar.py and test_grammar.py.
"""

import pytest

from spherepop.model import Atom, BindOp, CollapseOp, PopOp, RefuseOp, Sphere
from spherepop.parser import (
    ParseError,
    parse_expr,
    parse_operation,
    parse_program,
    parse_sphere,
)


class TestTokenization:
    """Test basic tokenization and parsing."""

    def test_parse_empty_string(self):
        """Empty string causes unexpected end of input."""
        with pytest.raises(ParseError, match="unexpected end of input"):
            parse_expr("")

    def test_parse_whitespace_only(self):
        """Whitespace-only string causes unexpected end of input."""
        with pytest.raises(ParseError, match="unexpected end of input"):
            parse_expr("   \n  \t  ")

    def test_parse_single_atom(self):
        """Single atom parses correctly."""
        result = parse_expr("a")
        assert isinstance(result, Atom)
        assert result.name == "a"

    def test_parse_atom_with_whitespace(self):
        """Atoms with surrounding whitespace parse correctly."""
        result = parse_expr("  atom  ")
        assert isinstance(result, Atom)
        assert result.name == "atom"


class TestUnclosedSphere:
    """Test unclosed sphere syntax errors."""

    def test_parse_unclosed_sphere_simple(self):
        """Unclosed sphere raises error."""
        with pytest.raises(ParseError, match="missing '\\)' in sphere expression"):
            parse_expr("(a b")

    def test_parse_unclosed_sphere_nested(self):
        """Nested unclosed sphere raises error."""
        with pytest.raises(ParseError, match="missing '\\)' in sphere expression"):
            parse_expr("((a b)")

    def test_parse_unclosed_sphere_empty(self):
        """Empty unclosed sphere raises error."""
        with pytest.raises(ParseError, match="missing '\\)' in sphere expression"):
            parse_expr("(")

    def test_parse_multiple_unclosed(self):
        """Multiple unclosed spheres raise error."""
        with pytest.raises(ParseError, match="missing '\\)' in sphere expression"):
            parse_expr("((a")


class TestUnexpectedCloseParen:
    """Test unexpected close parenthesis errors."""

    def test_parse_unexpected_close_paren_start(self):
        """Close paren at start raises error."""
        with pytest.raises(ParseError, match="unexpected '\\)'"):
            parse_expr(")")

    def test_parse_unexpected_close_paren_after_atom(self):
        """Close paren after atom raises error."""
        with pytest.raises(ParseError, match="trailing tokens"):
            parse_expr("a)")

    def test_parse_unmatched_close_paren(self):
        """Unmatched close paren raises error."""
        with pytest.raises(ParseError, match="trailing tokens"):
            parse_expr("(a))")


class TestTrailingTokens:
    """Test trailing tokens after complete expression."""

    def test_parse_trailing_atom(self):
        """Trailing atom after valid expression raises error."""
        with pytest.raises(ParseError, match="trailing tokens after expression"):
            parse_expr("(a b) c")

    def test_parse_trailing_sphere(self):
        """Trailing sphere after valid expression raises error."""
        with pytest.raises(ParseError, match="trailing tokens after expression"):
            parse_expr("(a) (b)")

    def test_parse_trailing_paren(self):
        """Trailing paren after valid expression raises error."""
        with pytest.raises(ParseError, match="trailing tokens after expression"):
            parse_expr("a (")


class TestParseSphere:
    """Test parse_sphere() type enforcement."""

    def test_parse_sphere_with_sphere(self):
        """Sphere input parses correctly."""
        result = parse_sphere("(a b c)")
        assert isinstance(result, Sphere)
        assert len(result.items) == 3

    def test_parse_sphere_with_atom(self):
        """Atom input raises error (must be Sphere)."""
        with pytest.raises(ParseError, match="top-level expression must be a Sphere"):
            parse_sphere("a")

    def test_parse_sphere_empty(self):
        """Empty sphere parses correctly."""
        result = parse_sphere("()")
        assert isinstance(result, Sphere)
        assert len(result.items) == 0


class TestOperationParsing:
    """Test parse_operation() command parsing."""

    def test_parse_operation_pop_no_args(self):
        """POP with no args uses default."""
        op = parse_operation("POP")
        assert isinstance(op, PopOp)
        assert op.path is None

    def test_parse_operation_pop_with_path(self):
        """POP with dotted path arg."""
        op = parse_operation("POP 0.1.2")
        assert isinstance(op, PopOp)
        assert op.path == (0, 1, 2)

    def test_parse_operation_pop_empty_path_becomes_none(self):
        """POP with whitespace-only path becomes None (default)."""
        op = parse_operation("POP   ")
        assert isinstance(op, PopOp)
        assert op.path is None

    def test_parse_operation_pop_invalid_path(self):
        """POP with non-numeric path raises error."""
        with pytest.raises(ParseError, match="invalid POP path"):
            parse_operation("POP abc")

    def test_parse_operation_pop_negative_index(self):
        """POP with negative index raises error."""
        with pytest.raises(ParseError, match="non-negative"):
            parse_operation("POP 0.-1")

    def test_parse_operation_refuse(self):
        """REFUSE with option names."""
        op = parse_operation("REFUSE a b c")
        assert isinstance(op, RefuseOp)
        assert op.refused == frozenset({"a", "b", "c"})

    def test_parse_operation_refuse_empty(self):
        """REFUSE with no options raises error (Appendix E)."""
        with pytest.raises(ParseError, match="REFUSE requires at least one target"):
            parse_operation("REFUSE")

    def test_parse_operation_refuse_comma_separated(self):
        """REFUSE accepts comma-separated options."""
        op = parse_operation("REFUSE a, b, c")
        assert isinstance(op, RefuseOp)
        assert op.refused == frozenset({"a", "b", "c"})

    def test_parse_operation_bind(self):
        """BIND with predicate."""
        op = parse_operation("BIND prefix:user")
        assert isinstance(op, BindOp)
        assert op.predicate == "prefix:user"

    def test_parse_operation_bind_no_predicate(self):
        """BIND with no predicate raises error."""
        with pytest.raises(ParseError, match="BIND requires a predicate"):
            parse_operation("BIND")

    def test_parse_operation_bind_with_spaces(self):
        """BIND predicate can contain spaces."""
        op = parse_operation("BIND in:a, b, c")
        assert isinstance(op, BindOp)
        assert op.predicate == "in:a, b, c"

    def test_parse_operation_collapse(self):
        """COLLAPSE with equivalence classes."""
        op = parse_operation("COLLAPSE a,b; c,d")
        assert isinstance(op, CollapseOp)
        assert len(op.classes) == 2
        assert frozenset({"a", "b"}) in op.classes
        assert frozenset({"c", "d"}) in op.classes

    def test_parse_operation_collapse_equals_separator(self):
        """COLLAPSE accepts = as separator."""
        op = parse_operation("COLLAPSE a=b; c=d")
        assert isinstance(op, CollapseOp)
        assert len(op.classes) == 2

    def test_parse_operation_collapse_no_classes(self):
        """COLLAPSE with no classes raises error."""
        with pytest.raises(ParseError, match="requires at least one equivalence class"):
            parse_operation("COLLAPSE")

    def test_parse_operation_collapse_single_member_class(self):
        """COLLAPSE class with single member raises error."""
        with pytest.raises(ParseError, match="at least two members"):
            parse_operation("COLLAPSE a")

    def test_parse_operation_collapse_multiple_classes(self):
        """COLLAPSE with multiple semicolon-separated classes."""
        op = parse_operation("COLLAPSE a,b,c; x,y; p,q,r,s")
        assert len(op.classes) == 3
        assert frozenset({"a", "b", "c"}) in op.classes
        assert frozenset({"x", "y"}) in op.classes
        assert frozenset({"p", "q", "r", "s"}) in op.classes

    def test_parse_operation_unknown_command(self):
        """Unknown command raises error."""
        with pytest.raises(ParseError, match="unknown operation"):
            parse_operation("UNKNOWN a b")

    def test_parse_operation_empty_line(self):
        """Empty line raises error."""
        with pytest.raises(ParseError, match="operation line cannot be empty"):
            parse_operation("")

    def test_parse_operation_whitespace_only(self):
        """Whitespace-only line raises error."""
        with pytest.raises(ParseError, match="operation line cannot be empty"):
            parse_operation("   \n\t  ")

    def test_parse_operation_lowercase_normalized(self):
        """Operation names are normalized to uppercase."""
        op = parse_operation("pop")
        assert isinstance(op, PopOp)


class TestParseProgram:
    """Test parse_program() full program parsing."""

    def test_parse_program_single_operation(self):
        """Program with single operation."""
        ops = parse_program(["POP 0.1"])
        assert len(ops) == 1
        assert isinstance(ops[0], PopOp)

    def test_parse_program_multiple_operations(self):
        """Program with multiple operations."""
        ops = parse_program(["POP 0", "REFUSE x", "BIND ALL"])
        assert len(ops) == 3
        assert isinstance(ops[0], PopOp)
        assert isinstance(ops[1], RefuseOp)
        assert isinstance(ops[2], BindOp)

    def test_parse_program_empty_lines(self):
        """Program with empty lines (skipped)."""
        ops = parse_program(["POP", "", "REFUSE a", "   ", "BIND ALL"])
        assert len(ops) == 3

    def test_parse_program_comments(self):
        """Program with comment lines (skipped)."""
        ops = parse_program(["# This is a comment", "POP", "  # Another comment", "REFUSE a"])
        assert len(ops) == 2

    def test_parse_program_empty_list(self):
        """Empty program returns empty list."""
        ops = parse_program([])
        assert ops == []

    def test_parse_program_invalid_operation(self):
        """Program with invalid operation raises error."""
        with pytest.raises(ParseError, match="unknown operation"):
            parse_program(["INVALID"])

    def test_parse_program_stops_at_first_error(self):
        """Program parsing stops at first error."""
        with pytest.raises(ParseError):
            parse_program(
                [
                    "POP",
                    "INVALID",  # Error here
                    "REFUSE a",  # Never reached
                ]
            )


class TestEdgeCases:
    """Test additional edge cases."""

    def test_parse_expr_deeply_nested(self):
        """Deeply nested spheres parse correctly."""
        result = parse_expr("(((a)))")
        assert isinstance(result, Sphere)
        assert isinstance(result.items[0], Sphere)
        assert isinstance(result.items[0].items[0], Sphere)

    def test_parse_expr_mixed_nesting(self):
        """Mixed atom and sphere nesting."""
        result = parse_expr("(a (b c) d)")
        assert isinstance(result, Sphere)
        assert len(result.items) == 3
        assert isinstance(result.items[0], Atom)
        assert isinstance(result.items[1], Sphere)
        assert isinstance(result.items[2], Atom)

    def test_tokenize_special_chars_in_atoms(self):
        """Atoms can contain various characters."""
        result = parse_expr("(user_id-123)")
        assert isinstance(result, Sphere)
        assert result.items[0].name == "user_id-123"

    def test_parse_empty_sphere_nested(self):
        """Empty nested spheres."""
        result = parse_expr("(() ())")
        assert isinstance(result, Sphere)
        assert len(result.items) == 2
        assert all(isinstance(item, Sphere) and len(item.items) == 0 for item in result.items)

    def test_parse_operation_refuse_many_options(self):
        """REFUSE with many options."""
        op = parse_operation("REFUSE " + " ".join(f"opt{i}" for i in range(100)))
        assert isinstance(op, RefuseOp)
        assert len(op.refused) == 100

    def test_parse_operation_pop_single_index(self):
        """POP with single index."""
        op = parse_operation("POP 5")
        assert op.path == (5,)

    def test_parse_operation_collapse_mixed_separators(self):
        """COLLAPSE with mixed comma and equals separators."""
        op = parse_operation("COLLAPSE a,b=c")
        assert frozenset({"a", "b", "c"}) in op.classes
