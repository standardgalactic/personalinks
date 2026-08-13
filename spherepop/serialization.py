from __future__ import annotations

import json
from typing import Any

from spherepop.model import (
    Atom,
    BindEvent,
    CollapseEvent,
    Config,
    Event,
    Expr,
    PopEvent,
    Quotient,
    RefuseEvent,
    Sphere,
)

CONFIG_SCHEMA_V1 = "spherepop.config.v1"


def config_to_dict(config: Config) -> dict[str, Any]:
    """Serialize a Config into the versioned spherepop.config.v1 dictionary.

    Contract:
    - Structural serialization only; no semantic interpretation.
    - Deterministic ordering for set-like collections.
    - Stable schema boundary for interchange and archival.
    """
    return {
        "schema": CONFIG_SCHEMA_V1,
        "sigma": _encode_expr(config.sigma),
        "history": [_encode_event(event) for event in config.history],
        "option_space": [_encode_option(option) for option in _sorted_options(config.option_space)],
        "collapse_log": [
            {
                "history_index": history_index,
                "classes": [sorted(cls) for cls in classes],
            }
            for history_index, classes in config.collapse_log
        ],
    }


def config_from_dict(payload: dict[str, Any]) -> Config:
    """Deserialize a Config from a spherepop.config.v1 dictionary.

    This performs only structural validation. It does not attempt to normalize,
    repair, or semantically validate admissibility/invariants.
    """
    if payload.get("schema") != CONFIG_SCHEMA_V1:
        raise ValueError(f"Unsupported or missing schema; expected '{CONFIG_SCHEMA_V1}'")

    sigma_raw = payload.get("sigma")
    if not isinstance(sigma_raw, dict):
        raise ValueError("Field 'sigma' must be an object")
    sigma = _decode_expr(sigma_raw)
    if not isinstance(sigma, Sphere):
        raise ValueError("Top-level 'sigma' must decode to a Sphere")

    history_raw = payload.get("history")
    if not isinstance(history_raw, list):
        raise ValueError("Field 'history' must be a list")
    history = tuple(_decode_event(item) for item in history_raw)

    option_space_raw = payload.get("option_space")
    if not isinstance(option_space_raw, list):
        raise ValueError("Field 'option_space' must be a list")
    option_space = frozenset(_decode_option(item) for item in option_space_raw)

    collapse_log_raw = payload.get("collapse_log")
    if not isinstance(collapse_log_raw, list):
        raise ValueError("Field 'collapse_log' must be a list")
    collapse_log = tuple(_decode_collapse_log_entry(item) for item in collapse_log_raw)

    return Config(
        sigma=sigma,
        history=history,
        option_space=option_space,
        collapse_log=collapse_log,
    )


def to_json(config: Config, *, indent: int = 2, sort_keys: bool = True) -> str:
    """Serialize a Config into canonical JSON for spherepop.config.v1."""
    return json.dumps(config_to_dict(config), indent=indent, sort_keys=sort_keys)


def from_json(data: str) -> Config:
    """Deserialize a Config from JSON text."""
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON value must be an object")
    return config_from_dict(payload)


def _encode_expr(expr: Expr) -> dict[str, Any]:
    if isinstance(expr, Atom):
        return {
            "kind": "atom",
            "name": _encode_atom_name(expr.name),
        }
    return {
        "kind": "sphere",
        "label": expr.label,
        "items": [_encode_expr(item) for item in expr.items],
    }


def _decode_expr(data: dict[str, Any]) -> Expr:
    kind = data.get("kind")
    if kind == "atom":
        if "name" not in data:
            raise ValueError("Atom is missing required field 'name'")
        return Atom(_decode_atom_name(data["name"]))
    if kind == "sphere":
        items_raw = data.get("items")
        if not isinstance(items_raw, list):
            raise ValueError("Sphere field 'items' must be a list")
        label_raw = data.get("label")
        if label_raw is not None and not isinstance(label_raw, str):
            raise ValueError("Sphere field 'label' must be a string or null")
        return Sphere(
            items=tuple(
                _decode_expr(item) for item in _expect_dict_list(items_raw, "sphere items")
            ),
            label=label_raw,
        )
    raise ValueError(f"Unknown expression kind: {kind!r}")


def _encode_atom_name(name: str | Quotient) -> str | dict[str, Any]:
    if isinstance(name, str):
        return name
    return {
        "kind": "quotient",
        "members": sorted(name.members),
    }


def _decode_atom_name(name: Any) -> str | Quotient:
    if isinstance(name, str):
        return name
    if isinstance(name, dict):
        if name.get("kind") != "quotient":
            raise ValueError(f"Unknown atom-name object kind: {name.get('kind')!r}")
        members = _decode_member_list(name.get("members"), field_name="quotient members")
        return Quotient(members=members)
    raise ValueError("Atom field 'name' must be a string or quotient object")


def _encode_event(event: Event) -> dict[str, Any]:
    if isinstance(event, PopEvent):
        return {
            "kind": "POP",
            "history_index": event.history_index,
            "path": list(event.path),
            "label": event.label,
        }
    if isinstance(event, RefuseEvent):
        return {
            "kind": "REFUSE",
            "history_index": event.history_index,
            "refused": sorted(event.refused),
            "label": event.label,
        }
    if isinstance(event, BindEvent):
        return {
            "kind": "BIND",
            "history_index": event.history_index,
            "predicate": event.predicate,
            "label": event.label,
        }
    return {
        "kind": "COLLAPSE",
        "history_index": event.history_index,
        "classes": [sorted(cls) for cls in event.classes],
        "label": event.label,
    }


def _decode_event(data: Any) -> Event:
    if not isinstance(data, dict):
        raise ValueError("Each history event must be an object")
    kind = data.get("kind")
    history_index = data.get("history_index")
    if not isinstance(history_index, int):
        raise ValueError(f"History event {kind!r} must include integer 'history_index'")
    if history_index < 0:
        raise ValueError("History event 'history_index' must be non-negative")
    label = data.get("label")
    if label is not None and not isinstance(label, str):
        raise ValueError("History event 'label' must be a string or null")

    if kind == "POP":
        path_raw = data.get("path")
        if not isinstance(path_raw, list) or not all(isinstance(p, int) for p in path_raw):
            raise ValueError("POP event field 'path' must be a list of integers")
        if any(p < 0 for p in path_raw):
            raise ValueError("POP event field 'path' cannot contain negative indices")
        return PopEvent(history_index=history_index, path=tuple(path_raw), label=label)
    if kind == "REFUSE":
        refused = _decode_member_list(data.get("refused"), field_name="REFUSE refused")
        return RefuseEvent(history_index=history_index, refused=refused, label=label)
    if kind == "BIND":
        predicate = data.get("predicate")
        if not isinstance(predicate, str):
            raise ValueError("BIND event field 'predicate' must be a string")
        return BindEvent(history_index=history_index, predicate=predicate, label=label)
    if kind == "COLLAPSE":
        classes_raw = data.get("classes")
        if not isinstance(classes_raw, list):
            raise ValueError("COLLAPSE event field 'classes' must be a list")
        classes = tuple(
            _decode_member_list(group, field_name="COLLAPSE class")
            for group in _expect_list_of_lists(classes_raw, "COLLAPSE classes")
        )
        if any(len(cls) < 2 for cls in classes):
            raise ValueError("COLLAPSE event classes must each contain at least two members")
        return CollapseEvent(history_index=history_index, classes=classes, label=label)

    raise ValueError(f"Unknown event kind: {kind!r}")


def _encode_option(option: str | Quotient) -> dict[str, Any]:
    if isinstance(option, str):
        return {"kind": "string", "value": option}
    return {"kind": "quotient", "members": sorted(option.members)}


def _decode_option(data: Any) -> str | Quotient:
    if not isinstance(data, dict):
        raise ValueError("Each option_space element must be an object")
    kind = data.get("kind")
    if kind == "string":
        value = data.get("value")
        if not isinstance(value, str):
            raise ValueError("Option kind 'string' must include string field 'value'")
        return value
    if kind == "quotient":
        members = _decode_member_list(data.get("members"), field_name="option quotient members")
        return Quotient(members=members)
    raise ValueError(f"Unknown option kind: {kind!r}")


def _decode_collapse_log_entry(data: Any) -> tuple[int, tuple[frozenset[str], ...]]:
    if not isinstance(data, dict):
        raise ValueError("Each collapse_log entry must be an object")
    history_index = data.get("history_index")
    if not isinstance(history_index, int):
        raise ValueError("collapse_log entry field 'history_index' must be an integer")
    if history_index < 0:
        raise ValueError("collapse_log entry field 'history_index' must be non-negative")
    classes_raw = data.get("classes")
    if not isinstance(classes_raw, list):
        raise ValueError("collapse_log entry field 'classes' must be a list")
    classes = tuple(
        _decode_member_list(group, field_name="collapse_log class")
        for group in _expect_list_of_lists(classes_raw, "collapse_log classes")
    )
    if any(len(cls) < 2 for cls in classes):
        raise ValueError("collapse_log classes must each contain at least two members")
    return (history_index, classes)


def _decode_member_list(value: Any, *, field_name: str) -> frozenset[str]:
    if not isinstance(value, list):
        raise ValueError(f"Field '{field_name}' must be a list")
    if not all(isinstance(member, str) for member in value):
        raise ValueError(f"Field '{field_name}' must contain only strings")
    if len(set(value)) != len(value):
        raise ValueError(f"Field '{field_name}' cannot contain duplicate members")
    return frozenset(value)


def _expect_dict_list(value: list[Any], field_name: str) -> list[dict[str, Any]]:
    if not all(isinstance(item, dict) for item in value):
        raise ValueError(f"Field '{field_name}' must contain only objects")
    return value


def _expect_list_of_lists(value: list[Any], field_name: str) -> list[list[Any]]:
    if not all(isinstance(item, list) for item in value):
        raise ValueError(f"Field '{field_name}' must contain only lists")
    return value


def _sorted_options(options: frozenset[str | Quotient]) -> list[str | Quotient]:
    return sorted(options, key=_option_sort_key)


def _option_sort_key(option: str | Quotient) -> tuple[str, str]:
    if isinstance(option, str):
        return ("0", option)
    return ("1", ",".join(sorted(option.members)))
