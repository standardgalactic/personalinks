from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

from spherepop.model import (
    Atom,
    BindEvent,
    BindOp,
    CollapseEvent,
    CollapseOp,
    Config,
    Expr,
    Operation,
    PopEvent,
    PopOp,
    Quotient,
    RefuseEvent,
    RefuseOp,
    Sphere,
)
from spherepop.path_utils import (
    PathError,
    deepest_non_root_sphere,
    find_label_path,
    path_exists,
)
from spherepop.predicates import predicate as make_predicate
from spherepop.views import format_available_options, format_available_paths


class EvalError(ValueError):
    pass


def _pop_path(expr: Sphere, path: tuple[int, ...]) -> Sphere:
    if not path:
        raise EvalError("POP must target a nested Sphere path, not the root")

    def recurse(node: Expr, target: tuple[int, ...]) -> Expr:
        if not target:
            if not isinstance(node, Sphere):
                raise EvalError("POP target must be a Sphere")
            return node  # caller handles splicing

        if not isinstance(node, Sphere):
            raise EvalError("POP path traverses through non-Sphere")

        idx = target[0]
        if idx < 0 or idx >= len(node.items):
            raise EvalError("POP path is out of range")

        child = node.items[idx]
        if len(target) == 1:
            if not isinstance(child, Sphere):
                raise EvalError("POP target must be a Sphere")
            new_items = list(node.items[:idx]) + list(child.items) + list(node.items[idx + 1 :])
            # Rebuilding `node` (the parent) with the child's items spliced
            # in -- preserve node's own label, not the popped child's.
            return Sphere(tuple(new_items), label=node.label)

        new_child = recurse(child, target[1:])
        new_items = list(node.items)
        new_items[idx] = new_child
        return Sphere(tuple(new_items), label=node.label)

    popped = recurse(expr, path)
    if not isinstance(popped, Sphere):
        raise EvalError("POP must preserve top-level Sphere")
    return popped


def _quotient_map(classes: Iterable[frozenset[str]]) -> dict[str, Quotient]:
    mapping: dict[str, Quotient] = {}
    for cls in classes:
        quotient = Quotient(members=frozenset(cls))
        for member in cls:
            mapping[member] = quotient
    return mapping


def _rename_expr(expr: Expr, mapping: dict[str, Quotient]) -> Expr:
    if isinstance(expr, Atom):
        if isinstance(expr.name, str) and expr.name in mapping:
            return Atom(mapping[expr.name])
        return expr
    return Sphere(tuple(_rename_expr(item, mapping) for item in expr.items), label=expr.label)


def _flatten_option_names(option_space: frozenset[str | Quotient]) -> frozenset[str]:
    """All plain-string names present in an option space, unpacking any
    Quotient's members. Used to resolve a REFUSE's named targets against
    an option space that may already contain merged classes.
    """
    names: set[str] = set()
    for option in option_space:
        if isinstance(option, Quotient):
            names |= option.members
        else:
            names.add(option)
    return frozenset(names)


def _option_names_any_of(option: str | Quotient, names: frozenset[str]) -> bool:
    if isinstance(option, Quotient):
        return bool(option.members & names)
    return option in names


def transition(config: Config, op: Operation) -> Config:
    """Apply a single operation to a Config, returning a new Config.

    The four primitive operations (POP, REFUSE, BIND, COLLAPSE) are the only
    operations that append to Config.history. This is the sole entry point
    for mutating transitions — all other functions are read-only observers.

    Examples:
        >>> from spherepop.model import Config, Sphere, Atom, PopOp, RefuseOp
        >>> from spherepop.semantics import transition

        # POP: Remove nested scope, promoting its contents
        >>> sigma = Sphere((Sphere((Atom("a"), Atom("b")), label="inner"),), label="root")
        >>> cfg = Config(sigma=sigma, option_space=frozenset({"a", "b"}), history=())
        >>> cfg_popped = transition(cfg, PopOp(label="inner"))
        >>> cfg_popped.sigma
        Sphere(items=(Atom(name='a'), Atom(name='b')), label='root')

        # REFUSE: Remove unwanted options
        >>> cfg_refused = transition(cfg, RefuseOp(options=frozenset({"b"})))
        >>> cfg_refused.option_space
        frozenset({'a'})

        # BIND: Filter by predicate
        >>> from spherepop.model import BindOp
        >>> cfg_bound = transition(cfg, BindOp(predicate="prefix:a"))
        >>> cfg_bound.option_space  # Only options starting with 'a'
        frozenset({'a'})

        # COLLAPSE: Create equivalence classes
        >>> from spherepop.model import CollapseOp
        >>> cfg_collapsed = transition(cfg, CollapseOp(classes=frozenset([frozenset({"a", "b"})])))
        >>> len(cfg_collapsed.option_space)  # Now a single Quotient
        1

    Args:
        config: Current configuration (immutable).
        op: Operation to apply (POP, REFUSE, BIND, or COLLAPSE).

    Returns:
        New Config with operation applied and appended to history.

    Raises:
        EvalError: If operation cannot be applied (e.g., invalid path,
                   empty result, malformed operation).
    """
    history_index = len(config.history)

    if isinstance(op, PopOp):
        if op.path is not None and op.label is not None:
            raise EvalError(
                "PopOp: specify at most one of path or label. "
                f"Received both: path={op.path}, label={op.label!r}"
            )
        try:
            if op.label is not None:
                path = find_label_path(config.sigma, op.label)
            elif op.path is not None:
                path = op.path
            else:
                path = deepest_non_root_sphere(config.sigma)
        except PathError as e:
            # Convert PathError to EvalError with added context
            paths_info = format_available_paths(config.sigma)
            raise EvalError(f"{e}. {paths_info}") from e
        if not path_exists(config.sigma, path):
            paths_info = format_available_paths(config.sigma)
            raise EvalError(f"POP path does not exist: {path}. {paths_info}")
        sigma_prime = _pop_path(config.sigma, path)
        pop_event = PopEvent(history_index=history_index, path=path, label=op.label)
        return replace(config, sigma=sigma_prime, history=config.history + (pop_event,))

    if isinstance(op, RefuseOp):
        # Resolve the requested names against whatever is actually present
        # -- including names living inside an already-merged Quotient.
        # Refusing one member of a Quotient refuses the whole class (a
        # Quotient is the atomic option-space element post-COLLAPSE), but
        # the recorded event names only what was actually requested and
        # present, not every member swept out along with it.
        #
        # op.label is recorded on the event for Appendix G provenance but
        # does not (yet) select among multiple option spaces: REFUSE still
        # acts on Config's single global option_space. Partitioning
        # option spaces by label is Appendix B's poset semantics, out of
        # scope for this increment -- see README.
        present_names = _flatten_option_names(config.option_space)
        refused = frozenset(present_names & op.refused)
        if not refused:
            # Appendix E: a refusal event is (O_h, R) with R a *nonempty*
            # subset of O_h. A REFUSE whose requested targets are all
            # already absent from the current option space is not a
            # degenerate no-op refusal -- it is not a refusal at all.
            options_info = format_available_options(config.option_space)
            requested = ", ".join(sorted(op.refused))
            raise EvalError(
                f"REFUSE requires a nonempty subset of the current option space (Appendix E). "
                f"Requested: {{{requested}}}, but {options_info}"
            )
        option_prime = frozenset(
            o for o in config.option_space if not _option_names_any_of(o, refused)
        )
        refuse_event = RefuseEvent(history_index=history_index, refused=refused, label=op.label)
        return replace(config, option_space=option_prime, history=config.history + (refuse_event,))

    if isinstance(op, BindOp):
        # See the label note on the RefuseOp branch above: recorded, not
        # yet partitioning.
        pred = make_predicate(op.predicate)
        option_prime = frozenset(o for o in config.option_space if pred(o))
        bind_event = BindEvent(history_index=history_index, predicate=op.predicate, label=op.label)
        return replace(config, option_space=option_prime, history=config.history + (bind_event,))

    if isinstance(op, CollapseOp):
        mapping = _quotient_map(op.classes)
        sigma_prime_expr = _rename_expr(config.sigma, mapping)
        assert isinstance(sigma_prime_expr, Sphere), "COLLAPSE must preserve top-level Sphere"
        # Theory Status: Composing successive COLLAPSE operations is OPEN.
        # The paper (Appendix C) specifies COLLAPSE as irreversible identification
        # but does not define composition law for overlapping relations.
        # Current: mapping's keys are plain strings, so an option that is already
        # a Quotient from an earlier COLLAPSE is left untouched here rather than
        # merged into new classes.
        # Mathematically natural extension: take equivalence closure (transitive).
        # See THEORY_STATUS.md Q2b.
        option_prime = frozenset(
            mapping[o] if isinstance(o, str) and o in mapping else o for o in config.option_space
        )
        collapse_event = CollapseEvent(
            history_index=history_index, classes=op.classes, label=op.label
        )
        return replace(
            config,
            sigma=sigma_prime_expr,
            option_space=option_prime,
            history=config.history + (collapse_event,),
            collapse_log=config.collapse_log + ((history_index, op.classes),),
        )

    raise EvalError(
        f"Unsupported operation type: {type(op).__name__}. "
        f"Valid operation types: PopOp, RefuseOp, BindOp, CollapseOp"
    )


def eval_program(config: Config, operations: Iterable[Operation]) -> Config:
    current = config
    for op in operations:
        current = transition(current, op)
    return current


def history_is_prefix(old: Config, new: Config) -> bool:
    old_hist = old.history
    new_hist = new.history
    if len(old_hist) > len(new_hist):
        return False
    return old_hist == new_hist[: len(old_hist)]
