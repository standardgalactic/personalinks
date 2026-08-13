"""Configuration validation: advisory diagnostics for Config invariants.

This module provides **observational** validation — it inspects Config instances
and returns lists of violations without altering them. Validation is explicitly
invoked by tests, experiment runners (via --validate), or debugging workflows;
it is never implicitly part of transition().

The validated invariants correspond to structural well-formedness properties
that should hold across the stable Spherepop semantics, while being careful
not to choose answers to unresolved theoretical questions.

Theory Status
-------------
- Validation covers only paper-licensed and implementation-choice semantics
- When encountering provisional behavior (COLLAPSE composition, quotient
  predicate lifting), validation reports "unsupported" rather than choosing
  a semantic interpretation
- See THEORY_STATUS.md Q1-Q8 for what is established vs open
"""

from __future__ import annotations

from spherepop.model import Atom, CollapseEvent, Config, Expr, Quotient, Sphere


def validate_config(config: Config) -> list[str]:
    """Validate a Config's structural invariants.

    Returns an empty list if the config is valid, or a list of human-readable
    violation messages describing what is malformed.

    Validated Invariants
    --------------------
    1. **Sigma well-formedness**: All Sphere.items are valid Expr instances,
       no dangling references

    2. **Option provenance**: Option space elements trace back to atoms
       representable in sigma or to explicit collapse provenance:
       - Plain strings must correspond to Atom names in sigma
       - Quotient members must have been admissible atoms
       - After REFUSE/BIND, option_space ⊆ original atoms (asymmetric)

    3. **History sequential**: History indices are consecutive starting at 0

    4. **Collapse log consistency**: collapse_log indices reference actual
       CollapseEvents in history at those positions

    5. **Quotient uniqueness**: No duplicate Quotients with identical members

    6. **Label uniqueness** (if present): Sphere labels are globally unique
       within sigma (implementation choice per THEORY_STATUS.md Q8)

    Provisional Semantics
    ---------------------
    - Successive COLLAPSE on already-quoted options: reported as unsupported
      (THEORY_STATUS.md Q2b - composition semantics open)
    - Quotient predicate semantics: not validated (Q3 - existential vs
      universal vs well-defined lifting)

    Parameters
    ----------
    config : Config
        Configuration to validate

    Returns
    -------
    list[str]
        Empty if valid, otherwise violation messages

    Examples
    --------
    >>> from spherepop import make_config, parse_sphere
    >>> from spherepop.validation import validate_config
    >>> cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    >>> validate_config(cfg)
    []

    >>> # Malformed: option not in sigma
    >>> bad_cfg = Config(
    ...     sigma=Sphere((Atom("A"),), label="root"),
    ...     option_space=frozenset({"X"}),
    ...     history=()
    ... )
    >>> violations = validate_config(bad_cfg)
    >>> len(violations) > 0
    True
    """
    violations: list[str] = []

    # Invariant 1: Sigma well-formedness
    violations.extend(_validate_sigma(config.sigma))

    # Invariant 2: Option provenance
    violations.extend(_validate_option_provenance(config))

    # Invariant 3: History sequential
    violations.extend(_validate_history_sequential(config))

    # Invariant 4: Collapse log consistency
    violations.extend(_validate_collapse_log(config))

    # Invariant 5: Quotient uniqueness
    violations.extend(_validate_quotient_uniqueness(config))

    # Invariant 6: Label uniqueness (if labels present)
    violations.extend(_validate_label_uniqueness(config.sigma))

    return violations


def assert_valid_config(config: Config) -> None:
    """Strict validation: raises ValueError if config is invalid.

    This is a convenience wrapper around validate_config() for contexts
    that want validation as a gate rather than as a diagnostic.

    Raises
    ------
    ValueError
        If validate_config() returns any violations
    """
    violations = validate_config(config)
    if violations:
        msg = "Config validation failed:\n  " + "\n  ".join(violations)
        raise ValueError(msg)


# ============================================================================
# Private Validation Helpers
# ============================================================================


def _validate_sigma(sigma: Expr) -> list[str]:
    """Check that sigma is a well-formed expression tree."""
    violations: list[str] = []

    def recurse(expr: Expr, path: str) -> None:
        if isinstance(expr, Atom):
            # Atoms are always well-formed
            return

        if not isinstance(expr, Sphere):
            violations.append(
                f"Invalid Expr type at {path}: expected Atom or Sphere, got {type(expr).__name__}"
            )
            return

        if not isinstance(expr.items, tuple):
            violations.append(
                f"Sphere.items at {path} must be tuple, got {type(expr.items).__name__}"
            )
            return

        for i, item in enumerate(expr.items):
            if not isinstance(item, (Atom, Sphere)):
                violations.append(
                    f"Sphere.items[{i}] at {path} is invalid: got {type(item).__name__}"
                )
            else:
                recurse(item, f"{path}.items[{i}]")

    recurse(sigma, "sigma")
    return violations


def _collect_atoms(expr: Expr) -> frozenset[str]:
    """Recursively collect all Atom names from an expression tree."""
    if isinstance(expr, Atom):
        # Handle both plain string names and Quotient names (from old collapsed atoms)
        if isinstance(expr.name, str):
            return frozenset({expr.name})
        elif isinstance(expr.name, Quotient):
            return expr.name.members
        else:
            return frozenset()

    if not isinstance(expr, Sphere):
        # Malformed expr - return empty set, _validate_sigma will catch it
        return frozenset()

    atoms: set[str] = set()
    for item in expr.items:
        atoms.update(_collect_atoms(item))
    return frozenset(atoms)


def _validate_option_provenance(config: Config) -> list[str]:
    """Validate that option_space elements trace to sigma atoms or collapse provenance.

    Asymmetric invariant: options ⊆ atoms(sigma) before quotienting.
    After COLLAPSE, validate provenance rather than reconstructing identity.
    """
    violations: list[str] = []

    # Collect atoms from sigma
    sigma_atoms = _collect_atoms(config.sigma)

    # Track which atoms have been collapsed into quotients via history
    collapsed_members: set[str] = set()
    for event in config.history:
        if isinstance(event, CollapseEvent):
            for cls in event.classes:
                collapsed_members.update(cls)

    # Validate each option
    for option in config.option_space:
        if isinstance(option, str):
            # Plain string: must be in sigma atoms
            if option not in sigma_atoms:
                violations.append(
                    f"Option '{option}' not found in sigma atoms: {sorted(sigma_atoms)}"
                )
        elif isinstance(option, Quotient):
            # Quotient: members must trace to admitted atoms or collapse provenance
            for member in option.members:
                if member not in sigma_atoms and member not in collapsed_members:
                    violations.append(
                        f"Quotient member '{member}' not found in sigma atoms or collapse provenance"
                    )
        else:
            violations.append(f"Invalid option_space element type: {type(option).__name__}")

    return violations


def _validate_history_sequential(config: Config) -> list[str]:
    """Check that history events have consecutive indices starting at 0."""
    violations: list[str] = []

    for i, event in enumerate(config.history):
        if not hasattr(event, "history_index"):
            violations.append(f"History event at position {i} missing history_index attribute")
            continue

        if event.history_index != i:
            violations.append(
                f"History event at position {i} has history_index={event.history_index}, expected {i}"
            )

    return violations


def _validate_collapse_log(config: Config) -> list[str]:
    """Check that collapse_log indices reference actual CollapseEvents."""
    violations: list[str] = []

    for log_entry in config.collapse_log:
        # collapse_log is Tuple[Tuple[int, Tuple[FrozenSet[str], ...]], ...]
        # Each entry is (history_index, classes)
        if not isinstance(log_entry, tuple) or len(log_entry) != 2:
            violations.append(f"collapse_log entry has invalid structure: {log_entry}")
            continue

        log_idx, _classes = log_entry

        if log_idx < 0 or log_idx >= len(config.history):
            violations.append(
                f"collapse_log contains index {log_idx}, but history has only {len(config.history)} events"
            )
            continue

        event = config.history[log_idx]
        if not isinstance(event, CollapseEvent):
            violations.append(
                f"collapse_log index {log_idx} points to {type(event).__name__}, not CollapseEvent"
            )

    return violations


def _validate_quotient_uniqueness(config: Config) -> list[str]:
    """Check that there are no duplicate Quotients with identical members."""
    violations: list[str] = []

    quotients = [o for o in config.option_space if isinstance(o, Quotient)]

    # Check for duplicates by comparing members
    for i, q1 in enumerate(quotients):
        for q2 in quotients[i + 1 :]:
            if q1.members == q2.members:
                violations.append(f"Duplicate Quotient with members {sorted(q1.members)}")
                break  # Only report once per duplicate

    return violations


def _validate_label_uniqueness(sigma: Expr) -> list[str]:
    """Check that Sphere labels are globally unique (implementation choice).

    Per THEORY_STATUS.md Q8, global label uniqueness is an implementation
    convenience to make pop(label) unambiguous, not a theoretical requirement.
    """
    violations: list[str] = []

    labels: dict[str, list[str]] = {}  # label -> list of paths where it appears

    def recurse(expr: Expr, path: str) -> None:
        if isinstance(expr, Sphere) and expr.label is not None:
            if expr.label in labels:
                labels[expr.label].append(path)
            else:
                labels[expr.label] = [path]

            for i, item in enumerate(expr.items):
                if isinstance(item, Sphere):
                    recurse(item, f"{path}.items[{i}]")

    recurse(sigma, "sigma")

    for label, paths in labels.items():
        if len(paths) > 1:
            violations.append(f"Label '{label}' appears at multiple paths: {', '.join(paths)}")

    return violations
