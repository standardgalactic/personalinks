from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from spherepop.model import Atom, BindOp, CollapseOp, Expr, Operation, PopOp, RefuseOp, Sphere


class ParseError(ValueError):
    pass


@dataclass
class _Tokens:
    values: list[str]
    index: int = 0

    def peek(self) -> str | None:
        if self.index >= len(self.values):
            return None
        return self.values[self.index]

    def pop(self) -> str:
        if self.index >= len(self.values):
            raise ParseError("unexpected end of input")
        value = self.values[self.index]
        self.index += 1
        return value


def _tokenize_expr(source: str) -> list[str]:
    tokens: list[str] = []
    token: list[str] = []
    for ch in source:
        if ch in "()":
            if token:
                tokens.append("".join(token))
                token = []
            tokens.append(ch)
        elif ch.isspace():
            if token:
                tokens.append("".join(token))
                token = []
        else:
            token.append(ch)
    if token:
        tokens.append("".join(token))
    return tokens


def parse_expr(source: str) -> Expr:
    tokens = _Tokens(_tokenize_expr(source))

    def parse_one() -> Expr:
        tok = tokens.pop()
        if tok == "(":
            items: list[Expr] = []
            while tokens.peek() != ")":
                if tokens.peek() is None:
                    raise ParseError("missing ')' in sphere expression")
                items.append(parse_one())
            tokens.pop()  # consume ')'
            return Sphere(tuple(items))
        if tok == ")":
            raise ParseError("unexpected ')'")
        return Atom(tok)

    expr = parse_one()
    if tokens.peek() is not None:
        raise ParseError("trailing tokens after expression")
    return expr


def parse_sphere(source: str) -> Sphere:
    expr = parse_expr(source)
    if not isinstance(expr, Sphere):
        raise ParseError("top-level expression must be a Sphere '(...)'")
    return expr


def _parse_path(source: str) -> tuple[int, ...]:
    source = source.strip()
    if not source:
        raise ParseError("empty POP path")
    try:
        parts = tuple(int(p) for p in source.split("."))
    except ValueError as exc:
        raise ParseError(f"invalid POP path '{source}'") from exc
    if any(p < 0 for p in parts):
        raise ParseError("POP path indices must be non-negative")
    return parts


def _parse_classes(source: str) -> tuple[frozenset[str], ...]:
    if not source.strip():
        raise ParseError("COLLAPSE requires at least one equivalence class")
    classes = []
    for group in source.split(";"):
        members = [p.strip() for p in group.replace(",", "=").split("=") if p.strip()]
        if len(members) < 2:
            raise ParseError("each COLLAPSE class must have at least two members")
        classes.append(frozenset(members))
    return tuple(classes)


def parse_operation(line: str) -> Operation:
    text = line.strip()
    if not text:
        raise ParseError("operation line cannot be empty")

    head, *rest = text.split(maxsplit=1)
    tail = rest[0] if rest else ""
    keyword = head.upper()

    if keyword == "POP":
        return PopOp(path=_parse_path(tail) if tail else None)
    if keyword == "REFUSE":
        refused = [p.strip() for p in tail.replace(",", " ").split() if p.strip()]
        if not refused:
            # Appendix E: a refusal targets a nonempty subset. This is a
            # syntactic check (was anything named at all); transition()
            # separately enforces the semantic version (is any of it
            # still present in the current option space).
            raise ParseError("REFUSE requires at least one target (Appendix E: R must be nonempty)")
        return RefuseOp(refused=frozenset(refused))
    if keyword == "BIND":
        if not tail:
            raise ParseError("BIND requires a predicate expression")
        return BindOp(predicate=tail.strip())
    if keyword == "COLLAPSE":
        return CollapseOp(classes=_parse_classes(tail))

    raise ParseError(f"unknown operation '{head}'")


def parse_program(lines: Sequence[str]) -> list[Operation]:
    ops = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        ops.append(parse_operation(stripped))
    return ops
