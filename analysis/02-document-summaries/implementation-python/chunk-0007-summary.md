```python
        # Should show first 5 sorted (assuming natural ordering):
        assert "a" in result
        assert "b" in result
        assert "c" in result
        assert "d" in result
        assert "e" in result

    def test_format_available_options_with_labels(self):
        """Options with labels are still sorted and represented."""
        opts = frozenset({Atom("c", label="choice_c"), Atom("a")})
        result = format_available_options(opts)
        # Should show labels but sort by name:
        assert "'choice_c'" in result
        assert "'a'" in result

    def test_format_available_options_empty_repr(self):
        """Options with empty repr (e.g., frozenset) are shown as is."""
        opts = frozenset({frozenset(), Atom("b")})
        result = format_available_options(opts)
        # Should show the empty set without trying to stringify it:
        assert "'{}'" in result
        assert "'b'" in result

class TestFormatAvailableLabels:
    """Test format_available_labels() error message formatting."""

    def test_format_available_labels_empty(self):
        """Empty option space reports no labels."""
        result = format_available_labels(frozenset())
        assert "no available labels" in result

    def test_format_available_labels_single(self):
        """Single label shows that label."""
        result = format_available_labels(frozenset({"a"}))
        assert "available labels:" in result
        assert "'a'" in result

    def test_format_available_labels_few(self):
        """Few labels (≤5) show all."""
        result = format_available_labels(frozenset({"a", "b", "c"}))
        assert "available labels:" in result
        for label in {"a", "b", "c"}:
            assert f"'{label}'" in result

    def test_format_available_labels_many(self):
        """Many labels (>5) truncate with count."""
        large_set = frozenset(f"{i}" for i in range(20))
        result = format_available_labels(large_set)
        assert "..." in result
        assert "20 total" in result
        # Should show first 5 sorted alphabetically:
        for label in ["a", "b", "c", "d", "e"]:
            assert f"'{label}'" in result

    def test_format_available_labels_with_quotients(self):
        """Quotients display via representative."""
        q1 = Quotient(members=frozenset({"z", "x", "y"}))
        q2 = Quotient(members=frozenset({"b", "a", "c"}))
        result = format_available_labels(frozenset({q1, q2, "d"}))
        # Representatives: "a" (from q2), "b" (from q1), "d"
        for label in {"a", "b", "d"}:
            assert f"'{label}'" in result

    def test_format_available_labels_exactly_five(self):
        """Exactly 5 labels show all without truncation."""
        opts = frozenset({"a", "b", "c", "d", "e"})
        result = format_available_labels(opts)
        # Should not truncate:
        for label in {"a", "b", "c", "d", "e"}:
            assert f"'{label}'" in result

    def test_format_available_labels_six_triggers_truncation(self):
        """Six labels trigger truncation."""
        opts = frozenset({"a", "b", "c", "d", "e", "f"})
        result = format_available_labels(opts)
        assert "..." in result
        assert "6 total" in result

    def test_format_available_labels_empty_repr(self):
        """Labels with empty repr are shown as is."""
        opts = frozenset({frozenset(), Atom("b")})
        result = format_available_labels(opts)
        # Should show the empty set without trying to stringify it:
        assert "'{}'" in result
        assert "'b'" in result

class TestFormatOptionSpaceSummary:
    """Test format_option_space_summary() error message formatting."""

    def test_format_option_space_summary_empty(self):
        """Empty option space reports no options."""
        result = format_option_space_summary(frozenset())
        assert "option space is empty" in result

    def test_format_option_space_summary_single(self):
        """Single option shows that option with label None."""
        result = format_option_space_summary(frozenset({Atom("a")}))
        assert "'a (None)'" in result

    def test_format_option_space_summary_few(self):
        """Few options show each with its label, sorted by name."""
        opts = frozenset([Atom("b", label="choice_b"), Atom("a")])
        result = format_option_space_summary(opts)
        for opt_name, label in [("a", None), ("b", "choice_b")]:
            assert f"'{opt_name} ({label})'" in result

    def test_format_option_space_summary_many(self):
        """Many options (>5) truncate with count."""
        large_set = frozenset(f"option_{i}" for i in range(20))
        result = format_option_space_summary(large_set)
        assert "..." in result
        assert "20 total" in result
        # Should show first 5 sorted alphabetically:
        for opt_name, label in [("option_0", None), ("option_1", None), ("o[3D[K
("option_2", None),
                                ("option_3", None), ("option_4", None)]:
            assert f"'{opt_name} ({label})'" in result

    def test_format_option_space_summary_with_labels(self):
        """Options with explicit labels are displayed as such."""
        opts = frozenset([Atom("c", label="choice_c"), Atom("a")])
        result = format_option_space_summary(opts)
        assert "'a (None)'" in result
        assert "'c (choice_c)'" in result

    def test_format_option_space_summary_empty_repr(self):
        """Options with empty repr (e.g., frozenset) are shown as is."""
        opts = frozenset({frozenset(), Atom("b")})
        result = format_option_space_summary(opts)
        assert "'{} (None)'" in result
        assert "'b (None)'" in result

class TestFormatHistorySummary:
    """Test format_history_summary() error message formatting."""

    def test_format_history_summary_empty(self):
        """Empty history renders as empty tuple."""
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(),
        )
        result = format_history_summary(cfg)
        assert "no history recorded" in result

    def test_format_history_summary_single(self):
        """Single PopEvent shows that path."""
        from spherepop.model import PopEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )
        result = format_history_summary(cfg)
        assert "(0,) " in result  # Note trailing space

    def test_format_history_summary_multiple(self):
        """Multiple PopEvents show each path."""
        from spherepop.model import PopEvent, RefuseEvent

        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(
                PopEvent(history_index=0, path=(0,), label=None),
                PopEvent(history_index=1, path=(1,), label=None),
            ),
        )
        result = format_history_summary(cfg)
        assert "(0,) (1,) " in result  # Note trailing space

    def test_format_history_summary_deeply_nested(self):
        """Deeply nested histories show all paths."""
        inner1 = PopEvent(history_index=0, path=(0,), label=None)
        inner2 = PopEvent(history_index=1, path=(1,), label=None)
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(inner1, inner2),
        )
        result = format_history_summary(cfg)
        assert "(0,) (1,) " in result

    def test_format_history_summary_with_quotients(self):
        """Quotient histories display via representative path."""
        q = Quotient(members=frozenset({"z", "x", "y"}))
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({"a"}),
            history=(PopEvent(history_index=0, path=(q,), label=None),),
        )
        result = format_history_summary(cfg)
        # Representative is index 0
        assert "(0,) " in result

class TestFormatExtensionalSummary:
    """Test format_extensional_summary() error message formatting."""

    def test_format_extensional_summary_plain_strings(self):
        """Plain string option space renders sorted."""
        cfg = Config(
            sigma=Sphere((Atom("a"), Atom("b"))),
            option_space=frozenset({"b", "a", "c"}),
            history=(),
        )
        result = format_extensional_summary(cfg)
        assert "(a b) " in result  # Note trailing space

    def test_format_extensional_summary_with_quotients(self):
        """Quotient option spaces render via representative."""
        q = Quotient(members=frozenset({"z", "x", "y"}))
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({q}),
            history=(),
        )
        result = format_extensional_summary(cfg)
        # Representative is the first element 'z'
        assert "(z) " in result

    def test_format_extensional_summary_empty(self):
        """Empty extensional space renders as empty tuple."""
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset(),
            history=(),
        )
        result = format_extensional_summary(cfg)
        assert "no extensional options" in result

    def test_format_extensional_summary_many(self):
        """Many extensional options (>5) truncate with count."""
        opts = frozenset(f"opt_{i}" for i in range(20))
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=opts,
            history=(),
        )
        result = format_extensional_summary(cfg)
        assert "..." in result
        assert f"{len(opts)} total" in result

class TestFormatLabelSummary:
    """Test format_label_summary() error message formatting."""

    def test_format_label_summary_empty(self):
        """Empty label space renders as empty tuple."""
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset(),
            history=(),
        )
        result = format_label_summary(cfg)
        assert "no labels recorded" in result

    def test_format_label_summary_single(self):
        """Single label shows that label with None as no name."""
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({Atom("b", label="choice_b")}),
            history=(),
        )
        result = format_label_summary(cfg)
        assert "'choice_b' " in result  # Note trailing space

    def test_format_label_summary_multiple(self):
        """Multiple labels show each with its name, sorted by name."""
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset([Atom("b", label="choice_b"), Atom("a", [K
label="choice_a")]),
            history=(),
        )
        result = format_label_summary(cfg)
        assert "'choice_a' 'choice_b' " in result  # Note trailing space

    def test_format_label_summary_deeply_nested(self):
        """Deeply nested labels show all, sorted by name."""
        inner1 = Atom("c", label="inner_c")
        inner2 = Atom("b", label="inner_b")
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset([inner1, inner2]),
            history=(),
        )
        result = format_label_summary(cfg)
        assert "'inner_b' 'inner_c' " in result

    def test_format_label_summary_with_quotients(self):
        """Quotient labels display via representative name."""
        q = Quotient(members=frozenset({"z", "x", "y"}))
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({q}),
            history=(),
        )
        result = format_label_summary(cfg)
        # Representative is the first element 'z'
        assert "'z' " in result

class TestFormatErrorMessages:
    """Test error message formatting for consistency."""

    def test_pop_event_no_path(self):
        event = PopEvent(history_index=-1, path=None, label=None)
        msg = format_error_message(event)
        assert "PopEvent requires a valid path" in msg

    def test_refuse_event_no_path(self):
        event = RefuseEvent(history_index=-1, path=None, label=None)
        msg = format_error_message(event)
        assert "RefuseEvent requires a valid path" in msg

    def test_choice_mismatch(self):
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({Atom("b", label="choice_b")}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )
        event = RefuseEvent(history_index=1, path=(1,), label=None)
        msg = format_error_message(event)
        assert "RefuseEvent does not match PopEvent (history_index mismatch[8D[K
mismatch)" in msg

    def test_pop_event_history_mismatch(self):
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({}),
            history=(PopEvent(history_index=-1, path=(0,), label=None),),
        )
        event = PopEvent(history_index=0, path=(0,), label=None)
        msg = format_error_message(event)
        assert "PopEvent does not match existing history (history_index mis[3D[K
mismatch)" in msg

    def test_refuse_event_no_history(self):
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({}),
            history=tuple(),
        )
        event = RefuseEvent(history_index=0, path=(0,), label=None)
        msg = format_error_message(event)
        assert "RefuseEvent requires a preceding PopEvent" in msg

    def test_choice_mismatch_label(self):
        cfg = Config(
            sigma=Sphere((Atom("a"),)),
            option_space=frozenset({Atom("b", label="choice_b")}),
            history=(PopEvent(history_index=0, path=(0,), label=None),),
        )
        event = RefuseEvent(history_index=1, path=(1,), label='wrong_label'[19D[K
label='wrong_label')
        msg = format_error_message(event)
        assert "RefuseEvent with label 'wrong_label' does not match PopEven[7D[K
PopEvent (label mismatch)" in msg

    def test_pop_event_wrong_type(self):
        wrong_event = 42
        msg = format_error_message(wrong_event)
        assert "'PopEvent' object has no attribute 'history_index'" in msg

    def test_refuse_event_wrong_type(self):
        wrong_event = 42
        msg = format_error_message(wrong_event)
        assert "'RefuseEvent' object has no attribute 'history_index'" in m[1D[K
msg

if __name__ == '__main__':
    unittest.main()
```

