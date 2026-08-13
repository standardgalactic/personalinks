from __future__ import annotations

import json

import pytest

from spherepop import make_config, parse_sphere, transition
from spherepop.model import (
    Atom,
    BindOp,
    CollapseEvent,
    CollapseOp,
    Config,
    PopOp,
    Quotient,
    RefuseOp,
    Sphere,
)
from spherepop.serialization import (
    CONFIG_SCHEMA_V1,
    config_from_dict,
    config_to_dict,
    from_json,
    to_json,
)
from spherepop.validation import validate_config


def _rich_config() -> Config:
    """Build a config that exercises nested structure + all event variants."""
    sigma = Sphere(
        items=(
            Atom("A"),
            Sphere(
                items=(
                    Atom("B"),
                    Sphere(items=(Atom("C"), Atom("D")), label="deep"),
                ),
                label="mid",
            ),
            Atom("E"),
        ),
        label="root",
    )
    cfg = make_config(sigma, {"A", "B", "C", "D", "E"})
    cfg = transition(cfg, PopOp(path=(1, 1)))
    cfg = transition(cfg, RefuseOp(refused=frozenset({"E"})))
    cfg = transition(cfg, BindOp(predicate="in:A,B,C,D"))
    cfg = transition(cfg, CollapseOp(classes=(frozenset({"B", "C"}),)))
    return cfg


def test_roundtrip_preserves_nested_sphere_and_all_event_subtypes() -> None:
    cfg = _rich_config()
    restored = from_json(to_json(cfg))
    assert restored == cfg


def test_roundtrip_preserves_quotient_valued_atoms_and_mixed_option_space() -> None:
    cfg = _rich_config()
    encoded = config_to_dict(cfg)
    mid_sphere = encoded["sigma"]["items"][1]
    assert mid_sphere["kind"] == "sphere"
    first_mid_atom = mid_sphere["items"][0]
    second_mid_atom = mid_sphere["items"][1]
    assert first_mid_atom["kind"] == "atom"
    assert second_mid_atom["kind"] == "atom"
    assert first_mid_atom["name"]["kind"] == "quotient"
    assert second_mid_atom["name"]["kind"] == "quotient"
    assert {"kind": "string", "value": "A"} in encoded["option_space"]
    assert {"kind": "string", "value": "D"} in encoded["option_space"]
    assert {"kind": "quotient", "members": ["B", "C"]} in encoded["option_space"]
    restored = config_from_dict(encoded)
    assert restored == cfg


def test_roundtrip_preserves_empty_history_and_nonempty_history() -> None:
    empty_cfg = make_config(parse_sphere("(A B)"), {"A", "B"})
    rich_cfg = _rich_config()

    assert config_from_dict(config_to_dict(empty_cfg)) == empty_cfg
    assert config_from_dict(config_to_dict(rich_cfg)) == rich_cfg


def test_roundtrip_preserves_collapse_log_contents() -> None:
    cfg = _rich_config()
    payload = config_to_dict(cfg)
    assert payload["collapse_log"] == [{"history_index": 3, "classes": [["B", "C"]]}]
    restored = config_from_dict(payload)
    assert restored.collapse_log == cfg.collapse_log


def test_serialization_is_deterministic_by_default() -> None:
    cfg = _rich_config()
    first = to_json(cfg)
    second = to_json(cfg)
    assert first == second


def test_semantically_invalid_but_structurally_valid_config_is_not_repaired() -> None:
    payload = {
        "schema": CONFIG_SCHEMA_V1,
        "sigma": {"kind": "sphere", "label": "root", "items": [{"kind": "atom", "name": "A"}]},
        "history": [{"kind": "REFUSE", "history_index": 9, "refused": ["A"], "label": None}],
        "option_space": [{"kind": "string", "value": "ghost"}],
        "collapse_log": [],
    }

    cfg = config_from_dict(payload)
    violations = validate_config(cfg)

    assert cfg.history[0].history_index == 9
    assert cfg.option_space == frozenset({"ghost"})
    assert any("expected 0" in msg for msg in violations)
    assert any("not found in sigma atoms" in msg for msg in violations)


def test_rejects_unknown_schema_version() -> None:
    with pytest.raises(ValueError, match="Unsupported or missing schema"):
        config_from_dict({"schema": "spherepop.config.v999"})


def test_rejects_unknown_expression_kind() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["sigma"] = {"kind": "portal", "items": [], "label": None}
    with pytest.raises(ValueError, match="Unknown expression kind"):
        config_from_dict(payload)


def test_rejects_unknown_option_kind() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["option_space"] = [{"kind": "mystery"}]
    with pytest.raises(ValueError, match="Unknown option kind"):
        config_from_dict(payload)


def test_rejects_incorrect_field_types() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["history"] = "not-a-list"
    with pytest.raises(ValueError, match="Field 'history' must be a list"):
        config_from_dict(payload)


def test_rejects_malformed_quotient_members() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["option_space"] = [{"kind": "quotient", "members": ["A", "A"]}]
    with pytest.raises(ValueError, match="cannot contain duplicate members"):
        config_from_dict(payload)


def test_rejects_invalid_event_fields() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["history"] = [{"kind": "POP", "history_index": -1, "path": [0], "label": None}]
    with pytest.raises(ValueError, match="must be non-negative"):
        config_from_dict(payload)

    payload["history"] = [
        {"kind": "REFUSE", "history_index": 0, "refused": ["A", "A"], "label": None}
    ]
    with pytest.raises(ValueError, match="cannot contain duplicate members"):
        config_from_dict(payload)

    payload["history"] = [
        {"kind": "COLLAPSE", "history_index": 0, "classes": [["A"]], "label": None}
    ]
    with pytest.raises(ValueError, match="at least two members"):
        config_from_dict(payload)


def test_rejects_invalid_collapse_log_fields() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["collapse_log"] = [{"history_index": -1, "classes": [["A", "B"]]}]
    with pytest.raises(ValueError, match="must be non-negative"):
        config_from_dict(payload)

    payload["collapse_log"] = [{"history_index": 0, "classes": [["A"]]}]
    with pytest.raises(ValueError, match="at least two members"):
        config_from_dict(payload)


def test_rejects_unknown_event_kind() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["history"] = [{"kind": "UNKNOWN", "history_index": 0}]
    with pytest.raises(ValueError, match="Unknown event kind"):
        config_from_dict(payload)


def test_rejects_invalid_json() -> None:
    with pytest.raises(ValueError, match="Invalid JSON payload"):
        from_json("{invalid-json}")


def test_rejects_non_object_top_level_json() -> None:
    with pytest.raises(ValueError, match="Top-level JSON value must be an object"):
        from_json("[]")


def test_config_schema_marker_is_present() -> None:
    payload = json.loads(to_json(make_config(parse_sphere("(A)"), {"A"})))
    assert payload["schema"] == CONFIG_SCHEMA_V1


def test_event_encoding_explicitly_covers_all_event_subtypes() -> None:
    cfg = _rich_config()
    payload = config_to_dict(cfg)
    kinds = [event["kind"] for event in payload["history"]]
    assert kinds == ["POP", "REFUSE", "BIND", "COLLAPSE"]
    assert isinstance(cfg.history[-1], CollapseEvent)
    assert isinstance(cfg.option_space, frozenset)
    assert any(isinstance(option, Quotient) for option in cfg.option_space)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("sigma", None, "Field 'sigma' must be an object"),
        ("option_space", None, "Field 'option_space' must be a list"),
        ("collapse_log", None, "Field 'collapse_log' must be a list"),
    ],
)
def test_rejects_non_list_or_non_object_top_level_fields(
    field: str, value: object, message: str
) -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload[field] = value
    with pytest.raises(ValueError, match=message):
        config_from_dict(payload)


def test_rejects_top_level_sigma_that_decodes_to_atom() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["sigma"] = {"kind": "atom", "name": "A"}
    with pytest.raises(ValueError, match="Top-level 'sigma' must decode to a Sphere"):
        config_from_dict(payload)


def test_rejects_missing_atom_name_and_bad_atom_name_variants() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["sigma"] = {"kind": "sphere", "label": None, "items": [{"kind": "atom"}]}
    with pytest.raises(ValueError, match="missing required field 'name'"):
        config_from_dict(payload)

    payload["sigma"] = {
        "kind": "sphere",
        "label": None,
        "items": [{"kind": "atom", "name": {"kind": "mystery", "members": ["A", "B"]}}],
    }
    with pytest.raises(ValueError, match="Unknown atom-name object kind"):
        config_from_dict(payload)

    payload["sigma"] = {
        "kind": "sphere",
        "label": None,
        "items": [{"kind": "atom", "name": 42}],
    }
    with pytest.raises(ValueError, match="must be a string or quotient object"):
        config_from_dict(payload)


def test_rejects_invalid_sphere_items_and_label_types() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["sigma"] = {"kind": "sphere", "label": None, "items": "bad"}
    with pytest.raises(ValueError, match="Sphere field 'items' must be a list"):
        config_from_dict(payload)

    payload["sigma"] = {
        "kind": "sphere",
        "label": 9,
        "items": [{"kind": "atom", "name": "A"}],
    }
    with pytest.raises(ValueError, match="Sphere field 'label' must be a string or null"):
        config_from_dict(payload)

    payload["sigma"] = {"kind": "sphere", "label": None, "items": [1, 2]}
    with pytest.raises(ValueError, match="Field 'sphere items' must contain only objects"):
        config_from_dict(payload)


def test_rejects_additional_event_payload_type_errors() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))

    payload["history"] = [1]
    with pytest.raises(ValueError, match="Each history event must be an object"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "POP", "history_index": "x", "path": [0], "label": None}]
    with pytest.raises(ValueError, match="must include integer 'history_index'"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "POP", "history_index": 0, "path": [0], "label": 99}]
    with pytest.raises(ValueError, match="must be a string or null"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "POP", "history_index": 0, "path": "bad", "label": None}]
    with pytest.raises(ValueError, match="must be a list of integers"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "POP", "history_index": 0, "path": [-1], "label": None}]
    with pytest.raises(ValueError, match="cannot contain negative indices"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "BIND", "history_index": 0, "predicate": 123, "label": None}]
    with pytest.raises(ValueError, match="must be a string"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "COLLAPSE", "history_index": 0, "classes": "bad", "label": None}]
    with pytest.raises(ValueError, match="must be a list"):
        config_from_dict(payload)

    payload["history"] = [{"kind": "COLLAPSE", "history_index": 0, "classes": [123], "label": None}]
    with pytest.raises(ValueError, match="must contain only lists"):
        config_from_dict(payload)


def test_rejects_option_and_collapse_log_shape_errors() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["option_space"] = [1]
    with pytest.raises(ValueError, match="Each option_space element must be an object"):
        config_from_dict(payload)

    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["option_space"] = [{"kind": "string", "value": 1}]
    with pytest.raises(ValueError, match="must include string field 'value'"):
        config_from_dict(payload)

    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["collapse_log"] = [1]
    with pytest.raises(ValueError, match="Each collapse_log entry must be an object"):
        config_from_dict(payload)

    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["collapse_log"] = [{"history_index": "x", "classes": []}]
    with pytest.raises(ValueError, match="must be an integer"):
        config_from_dict(payload)

    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["collapse_log"] = [{"history_index": 0, "classes": "bad"}]
    with pytest.raises(ValueError, match="must be a list"):
        config_from_dict(payload)

    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))
    payload["collapse_log"] = [{"history_index": 0, "classes": [1]}]
    with pytest.raises(ValueError, match="must contain only lists"):
        config_from_dict(payload)


def test_rejects_member_lists_with_wrong_types() -> None:
    payload = config_to_dict(make_config(parse_sphere("(A)"), {"A"}))

    payload["option_space"] = [{"kind": "quotient", "members": "bad"}]
    with pytest.raises(ValueError, match="must be a list"):
        config_from_dict(payload)

    payload["option_space"] = [{"kind": "quotient", "members": ["A", 2]}]
    with pytest.raises(ValueError, match="must contain only strings"):
        config_from_dict(payload)
