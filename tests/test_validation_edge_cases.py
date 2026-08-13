"""Additional validation tests targeting edge case coverage gaps.

Extends test_validation.py to hit specific uncovered branches:
- Lines 151-154: Expr type validation
- Lines 257-260: collapse_log structure validation
- Lines 288-292: Duplicate quotient detection (Python prevents naturally)

These are defensive edge cases that can't occur through normal API but
validate the invariant checking is comprehensive.
"""

from spherepop.model import Atom, CollapseEvent, Config, Quotient, Sphere
from spherepop.validation import validate_config


class TestExprTypeValidation:
    """Test sigma must be Atom or Sphere, not other types."""

    def test_sigma_as_string_rejected(self):
        """sigma as plain string is detected."""
        cfg = Config(
            sigma="not an expr",  # type: ignore
            option_space=frozenset(),
            history=(),
        )

        violations = validate_config(cfg)
        assert any("Invalid Expr type" in v and "expected Atom or Sphere" in v for v in violations)

    def test_sigma_as_dict_rejected(self):
        """sigma as dict is detected."""
        cfg = Config(
            sigma={"not": "expr"},  # type: ignore
            option_space=frozenset(),
            history=(),
        )

        violations = validate_config(cfg)
        assert any("Invalid Expr type" in v for v in violations)

    def test_sphere_items_not_tuple_rejected(self):
        """Sphere.items as list instead of tuple is detected."""
        bad_sphere = Sphere.__new__(Sphere)
        object.__setattr__(bad_sphere, "items", [Atom("a")])  # type: ignore - list not tuple
        object.__setattr__(bad_sphere, "label", "root")

        cfg = Config(sigma=bad_sphere, option_space=frozenset({"a"}), history=())

        violations = validate_config(cfg)
        assert any("Sphere.items" in v and "must be tuple" in v for v in violations)


class TestOptionSpaceTypeValidation:
    """Test option_space elements must be str or Quotient."""

    def test_option_space_with_integer_rejected(self):
        """option_space containing integer is detected."""
        cfg = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a", 123}),  # type: ignore
            history=(),
        )

        violations = validate_config(cfg)
        assert any("Invalid option_space element type" in v for v in violations)

    def test_option_space_with_none_rejected(self):
        """option_space containing None is detected."""
        cfg = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a", None}),  # type: ignore
            history=(),
        )

        violations = validate_config(cfg)
        assert any("Invalid option_space element type" in v for v in violations)


class TestCollapseLogStructureValidation:
    """Test collapse_log structure validation."""

    def test_collapse_log_entry_not_tuple_rejected(self):
        """collapse_log entry that is not a tuple is detected."""
        cfg = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(CollapseEvent(history_index=0, classes=(), label=None),),
            collapse_log=("not a tuple",),  # type: ignore - should be tuple of tuples
        )

        violations = validate_config(cfg)
        assert any("collapse_log entry has invalid structure" in v for v in violations)

    def test_collapse_log_entry_wrong_length_rejected(self):
        """collapse_log entry with wrong number of elements is detected."""
        cfg = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(CollapseEvent(history_index=0, classes=(), label=None),),
            collapse_log=((0,),),  # type: ignore - should be (index, classes) tuple
        )

        violations = validate_config(cfg)
        assert any("collapse_log entry has invalid structure" in v for v in violations)

    def test_collapse_log_entry_three_elements_rejected(self):
        """collapse_log entry with three elements is detected."""
        cfg = Config(
            sigma=Sphere((Atom("a"),), label="root"),
            option_space=frozenset({"a"}),
            history=(CollapseEvent(history_index=0, classes=(), label=None),),
            collapse_log=((0, (), "extra"),),  # type: ignore - too many elements
        )

        violations = validate_config(cfg)
        assert any("collapse_log entry has invalid structure" in v for v in violations)


class TestDuplicateQuotientValidation:
    """Test duplicate Quotient detection.

    Note: Python's frozenset automatically deduplicates equal Quotients
    because they use dataclass equality (based on members). These tests
    document that the validation logic exists, even though it can't be
    triggered through normal Python operations.
    """

    def test_python_prevents_duplicate_quotients_naturally(self):
        """Verify frozenset deduplicates equal Quotients automatically."""
        q1 = Quotient(members=frozenset({"a", "b"}))
        q2 = Quotient(members=frozenset({"a", "b"}))

        # Equal quotients
        assert q1 == q2
        assert hash(q1) == hash(q2)

        # frozenset deduplicates
        space = frozenset({q1, q2})
        assert len(space) == 1

    def test_validation_accepts_deduplicated_quotients(self):
        """Config with naturally deduplicated Quotients is valid."""
        q1 = Quotient(members=frozenset({"a", "b"}))
        q2 = Quotient(members=frozenset({"a", "b"}))

        cfg = Config(
            sigma=Sphere((Atom("a"), Atom("b")), label="root"),
            option_space=frozenset({q1, q2}),  # Automatically becomes single element
            history=(CollapseEvent(history_index=0, classes=(frozenset({"a", "b"}),), label=None),),
        )

        violations = validate_config(cfg)
        # Should be valid - frozenset deduplicated automatically
        assert violations == []

    def test_validation_rejects_distinct_quotients_with_overlap(self):
        """Validation accepts distinct Quotients even with overlapping members."""
        q1 = Quotient(members=frozenset({"a", "b"}))
        q2 = Quotient(members=frozenset({"b", "c"}))  # Different set

        cfg = Config(
            sigma=Sphere((Atom("a"), Atom("b"), Atom("c")), label="root"),
            option_space=frozenset({q1, q2}),
            history=(
                CollapseEvent(history_index=0, classes=(frozenset({"a", "b"}),), label=None),
                CollapseEvent(history_index=1, classes=(frozenset({"b", "c"}),), label=None),
            ),
        )

        violations = validate_config(cfg)
        # This is valid - different Quotients can coexist
        assert violations == []


class TestMalformedNestedStructures:
    """Test deeply nested malformed structures."""

    def test_nested_invalid_expr_detected(self):
        """Invalid Expr deep in nested Sphere is detected."""
        bad_inner = Sphere.__new__(Sphere)
        object.__setattr__(bad_inner, "items", (Atom("a"), 42))  # type: ignore
        object.__setattr__(bad_inner, "label", "inner")

        outer = Sphere((bad_inner,), label="root")

        cfg = Config(sigma=outer, option_space=frozenset({"a"}), history=())

        violations = validate_config(cfg)
        assert any("items[1]" in v and "invalid" in v for v in violations)
