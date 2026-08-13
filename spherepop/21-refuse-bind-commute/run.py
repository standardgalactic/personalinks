from spherepop import (
    extensional_view,
    extensionally_equivalent,
    intensionally_equivalent,
    make_config,
    parse_sphere,
    transition,
)
from spherepop.model import BindOp, CollapseOp, RefuseOp

if __name__ == "__main__":
    # Part 1: REFUSE and BIND are independent per-element filters, so
    # applying them in either order lands on the same option_space --
    # but the two runs still commit different event sequences.
    base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    refuse_then_bind = transition(transition(base, RefuseOp(frozenset({"a2"}))), BindOp("prefix:a"))
    bind_then_refuse = transition(transition(base, BindOp("prefix:a")), RefuseOp(frozenset({"a2"})))

    print("REFUSE-then-BIND view:", extensional_view(refuse_then_bind))
    print("BIND-then-REFUSE view:", extensional_view(bind_then_refuse))
    print("extensionally equivalent:", extensionally_equivalent(refuse_then_bind, bind_then_refuse))
    print("intensionally equivalent:", intensionally_equivalent(refuse_then_bind, bind_then_refuse))

    # Part 2: that commutativity is specific to two plain filters. Once a
    # COLLAPSE sits between them, order changes the *extensional* result
    # too -- REFUSE-before-COLLAPSE removes a lone name; COLLAPSE-before-
    # REFUSE has already merged that name into a class, so the same
    # REFUSE now takes the whole class down with it.
    identify_a = CollapseOp(classes=(frozenset({"a1", "a2"}),))

    refuse_then_collapse = transition(transition(base, RefuseOp(frozenset({"a1"}))), identify_a)
    collapse_then_refuse = transition(transition(base, identify_a), RefuseOp(frozenset({"a1"})))

    print()
    print("REFUSE-then-COLLAPSE view:", extensional_view(refuse_then_collapse))
    print("COLLAPSE-then-REFUSE view:", extensional_view(collapse_then_refuse))
    print(
        "extensionally equivalent (order matters here):",
        extensionally_equivalent(refuse_then_collapse, collapse_then_refuse),
    )
