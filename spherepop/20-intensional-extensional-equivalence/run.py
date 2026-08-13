from spherepop import (
    extensionally_equivalent,
    intensionally_equivalent,
    make_config,
    parse_sphere,
    transition,
)
from spherepop.model import BindOp, PopOp

if __name__ == "__main__":
    base = make_config(parse_sphere("(A (B C) D)"), {"A", "B", "C", "D"})

    # h1 pops the nested scope directly. h2 takes a detour through a
    # no-op BIND ALL first, then pops. Different histories, same result.
    h1 = transition(base, PopOp(path=(1,)))
    h2 = transition(base, BindOp("ALL"))
    h2 = transition(h2, PopOp(path=(1,)))

    print("intensionally equivalent (same events):", intensionally_equivalent(h1, h2))
    print("extensionally equivalent (same view)   :", extensionally_equivalent(h1, h2))

    # Two runs that really do take the identical path are equivalent both ways.
    left = transition(base, BindOp("ALL"))
    right = transition(base, BindOp("ALL"))
    print("identical paths -- intensional:", intensionally_equivalent(left, right))
    print("identical paths -- extensional:", extensionally_equivalent(left, right))
