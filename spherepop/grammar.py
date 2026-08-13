"""Appendix G: A Minimal BNF Grammar for Spherepop.

A literal implementation of the paper's own concrete syntax, kept
deliberately separate from `spherepop.parser` -- the line-oriented
convenience command language (`POP 1`, `REFUSE a2`, ...) this lab has used
since the first experiments to drive Config transitions quickly. That
convenience syntax is *not* a claim to implement Appendix G; this module is.

The grammar, transcribed from the appendix:

    Lexical Domains
        <Identifier> ::= letter (letter | digit | "_")*
        <Label>      ::= <Identifier>
        <Value>      ::= <Identifier> | <Number>
        <Number>     ::= digit+

    Expressions and Spheres
        <Expr>   ::= <Value> | <Sphere>
        <Sphere> ::= "(" <Label> ":" <Expr>* ")"

    Events
        <Event> ::= <Pop> | <Collapse> | <Refusal> | <Binding>
        <Pop>      ::= "pop" "(" <Label> ")"
        <Collapse> ::= "collapse" "(" <Label> "," <Equiv> ")"
        <Refusal>  ::= "refuse" "(" <Label> "," <Set> ")"
        <Binding>  ::= "bind" "(" <Label> "," <Predicate> ")"

    Auxiliary Structures
        <Equiv>     ::= "{" <Pair> ("," <Pair>)* "}"
        <Pair>      ::= <Value> "~" <Value>
        <Set>       ::= "{" <Value> ("," <Value>)* "}"
        <Predicate> ::= <Identifier>

    Histories, Configurations, Evaluation
        <History> ::= <Event>*
        <Config>  ::= "<" <Expr> "," <History> ">"
        <Eval>    ::= <Config> "=>" <Config>

This module implements the lexical, expression, and event layers above and
translates parsed events into this codebase's (label-aware) Operation
dataclasses from `spherepop.model`. It does not re-implement <History>,
<Config>, or <Eval> as separate executable machinery: those correspond to
`spherepop.model.Config` and `spherepop.semantics.transition`/
`eval_program`, which already exist and are reused rather than re-specified
here as a second interpreter.

The appendix says predicates and equivalence relations are "treated
abstractly" at the grammar level. Concretely: a parsed <Predicate>
identifier is passed straight through to `spherepop.semantics._predicate`'s
existing string-spec surface (e.g. "ALL") rather than this module inventing
a second predicate language; a parsed <Equiv> (a set of pairwise `~`
relations) is closed under transitivity via union-find into the disjoint
`CollapseOp.classes` that codebase already expects, since `~` pairs and
disjoint classes are two different surface notations for the same
equivalence relation.
"""

from __future__ import annotations

from dataclasses import dataclass

from spherepop.model import Atom, BindOp, CollapseOp, Expr, Operation, PopOp, RefuseOp, Sphere


class GrammarError(ValueError):
    pass


_PUNCTUATION = set("():,{}~")


@dataclass(frozen=True)
class _Token:
    kind: str  # "IDENT" | "NUMBER" | "PUNCT"
    text: str


def _tokenize(source: str) -> list[_Token]:
    tokens: list[_Token] = []
    i, n = 0, len(source)
    while i < n:
        ch = source[i]
        if ch.isspace():
            i += 1
            continue
        if ch in _PUNCTUATION:
            tokens.append(_Token("PUNCT", ch))
            i += 1
            continue
        if ch.isdigit():
            j = i
            while j < n and source[j].isdigit():
                j += 1
            tokens.append(_Token("NUMBER", source[i:j]))
            i = j
            continue
        if ch.isalpha():
            j = i
            while j < n and (source[j].isalnum() or source[j] == "_"):
                j += 1
            tokens.append(_Token("IDENT", source[i:j]))
            i = j
            continue
        raise GrammarError(f"unexpected character {ch!r} at position {i}")
    return tokens


@dataclass
class _Cursor:
    tokens: list[_Token]
    index: int = 0

    def peek(self) -> _Token | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def pop(self) -> _Token:
        if self.index >= len(self.tokens):
            raise GrammarError("unexpected end of input")
        tok = self.tokens[self.index]
        self.index += 1
        return tok


def _expect(cur: _Cursor, kind: str, text: str) -> None:
    tok = cur.pop()
    if tok.kind != kind or tok.text != text:
        raise GrammarError(f"expected {text!r}, got {tok.text!r}")


def _parse_value(cur: _Cursor) -> str:
    tok = cur.pop()
    if tok.kind not in ("IDENT", "NUMBER"):
        raise GrammarError(f"expected a Value (Identifier or Number), got {tok.text!r}")
    return tok.text


def _parse_expr(cur: _Cursor) -> Expr:
    tok = cur.peek()
    if tok is None:
        raise GrammarError("unexpected end of input while parsing an Expr")
    if tok.kind == "PUNCT" and tok.text == "(":
        return _parse_sphere(cur)
    return Atom(_parse_value(cur))


def _parse_sphere(cur: _Cursor) -> Sphere:
    _expect(cur, "PUNCT", "(")
    label_tok = cur.pop()
    if label_tok.kind != "IDENT":
        raise GrammarError(f"expected a Label (Identifier) after '(', got {label_tok.text!r}")
    _expect(cur, "PUNCT", ":")
    items: list[Expr] = []
    while True:
        tok = cur.peek()
        if tok is None:
            raise GrammarError("missing ')' in sphere expression")
        if tok.kind == "PUNCT" and tok.text == ")":
            break
        items.append(_parse_expr(cur))
    cur.pop()  # consume ')'
    return Sphere(items=tuple(items), label=label_tok.text)


def parse_expr(source: str) -> Expr:
    """Parse a single <Expr>: either a <Value> (as an Atom) or a <Sphere>.

    Examples:
        >>> from spherepop.grammar import parse_expr

        # Simple atom (value)
        >>> atom = parse_expr("myvalue")
        >>> atom
        Atom(name='myvalue')

        # Number as atom
        >>> num = parse_expr("42")
        >>> num
        Atom(name='42')

        # Sphere with label and contents
        >>> sphere = parse_expr("(root: a b c)")
        >>> sphere.label
        'root'
        >>> len(sphere.items)
        3

        # Nested sphere
        >>> nested = parse_expr("(outer: (inner: x y) z)")
        >>> nested.label
        'outer'
        >>> nested.items[0].label  # First item is a sphere
        'inner'
    """
    cur = _Cursor(_tokenize(source))
    expr = _parse_expr(cur)
    if cur.peek() is not None:
        raise GrammarError("trailing tokens after expression")
    return expr


def parse_sphere(source: str) -> Sphere:
    """Parse a top-level <Sphere>: `"(" <Label> ":" <Expr>* ")"`."""
    expr = parse_expr(source)
    if not isinstance(expr, Sphere):
        raise GrammarError('top-level expression must be a Sphere "(Label: ...)"')
    return expr


def _parse_set(cur: _Cursor) -> frozenset[str]:
    _expect(cur, "PUNCT", "{")
    values = [_parse_value(cur)]
    while (tok := cur.peek()) is not None and tok.kind == "PUNCT" and tok.text == ",":
        cur.pop()
        values.append(_parse_value(cur))
    _expect(cur, "PUNCT", "}")
    return frozenset(values)


def _parse_pair(cur: _Cursor) -> tuple[str, str]:
    left = _parse_value(cur)
    _expect(cur, "PUNCT", "~")
    right = _parse_value(cur)
    return (left, right)


def _pairs_to_classes(pairs: list[tuple[str, str]]) -> tuple[frozenset[str], ...]:
    """Close a set of pairwise `~` relations under transitivity via
    union-find, producing the disjoint equivalence classes
    `CollapseOp.classes` already expects. `a~b, b~c` yields one class
    `{a, b, c}`, not two overlapping pairs -- `~` and disjoint classes are
    two notations for the same equivalence relation, not different ones.
    """
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in pairs:
        union(a, b)

    groups: dict[str, set[str]] = {}
    for name in parent:
        groups.setdefault(find(name), set()).add(name)
    return tuple(frozenset(members) for members in groups.values())


def _parse_equiv(cur: _Cursor) -> tuple[frozenset[str], ...]:
    _expect(cur, "PUNCT", "{")
    pairs = [_parse_pair(cur)]
    while (tok := cur.peek()) is not None and tok.kind == "PUNCT" and tok.text == ",":
        cur.pop()
        pairs.append(_parse_pair(cur))
    _expect(cur, "PUNCT", "}")
    return _pairs_to_classes(pairs)


def parse_event(source: str) -> Operation:
    """Parse a single <Event> into this codebase's (label-aware) Operation.

    Implements Appendix G's event grammar:
        <Event> ::= <Pop> | <Collapse> | <Refusal> | <Binding>

    Examples:
        >>> from spherepop.grammar import parse_event

        # POP: remove nested scope
        >>> pop_op = parse_event("pop(inner)")
        >>> pop_op
        PopOp(label='inner')

        # REFUSE: remove specific options
        >>> refuse_op = parse_event("refuse(root, {a, b})")
        >>> refuse_op
        RefuseOp(refused=frozenset({'a', 'b'}), label='root')

        # BIND: filter by predicate
        >>> bind_op = parse_event("bind(root, ALL)")
        >>> bind_op
        BindOp(predicate='ALL', label='root')

        # COLLAPSE: create equivalence classes
        >>> collapse_op = parse_event("collapse(root, {x~y, y~z})")
        >>> collapse_op.classes  # Transitively closed: {x,y,z}
        (frozenset({'x', 'y', 'z'}),)

        # Separate classes remain separate
        >>> collapse_op2 = parse_event("collapse(root, {a~b, c~d})")
        >>> len(collapse_op2.classes)  # Two classes: {a,b} and {c,d}
        2
    """
    cur = _Cursor(_tokenize(source))
    keyword_tok = cur.pop()
    if keyword_tok.kind != "IDENT":
        raise GrammarError(f"expected an event keyword, got {keyword_tok.text!r}")
    keyword = keyword_tok.text

    _expect(cur, "PUNCT", "(")
    label_tok = cur.pop()
    if label_tok.kind != "IDENT":
        raise GrammarError(f"expected a Label after '(', got {label_tok.text!r}")
    label = label_tok.text

    if keyword == "pop":
        _expect(cur, "PUNCT", ")")
        op: Operation = PopOp(label=label)
    elif keyword == "refuse":
        _expect(cur, "PUNCT", ",")
        targets = _parse_set(cur)
        _expect(cur, "PUNCT", ")")
        op = RefuseOp(refused=targets, label=label)
    elif keyword == "bind":
        _expect(cur, "PUNCT", ",")
        pred_tok = cur.pop()
        if pred_tok.kind != "IDENT":
            raise GrammarError(f"expected a Predicate (Identifier), got {pred_tok.text!r}")
        _expect(cur, "PUNCT", ")")
        op = BindOp(predicate=pred_tok.text, label=label)
    elif keyword == "collapse":
        _expect(cur, "PUNCT", ",")
        classes = _parse_equiv(cur)
        _expect(cur, "PUNCT", ")")
        op = CollapseOp(classes=classes, label=label)
    else:
        raise GrammarError(f"unknown event keyword {keyword!r}")

    if cur.peek() is not None:
        raise GrammarError("trailing tokens after event")
    return op
