from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import CollapseOp, PopOp
from spherepop.observers import divergent

if __name__ == "__main__":
    base = make_config(parse_sphere("(A (B C) D)"), {"x", "y"})

    # left resolves the nested scope; right leaves it nested. Their sigmas
    # differ in bracket structure, not just atom names.
    left = transition(base, PopOp(path=(1,)))
    right = base
    print("left sigma :", extensional_view(left)[0])
    print("right sigma:", extensional_view(right)[0])

    # COLLAPSE only quotients atoms by an equivalence relation; it cannot
    # restructure a Sphere's shape. So no policy over {A, B, C, D} can make
    # these confluent -- divergence here is a structural fact, not a naming
    # accident, and it survives regardless of which classes we try.
    identify_bc = CollapseOp(classes=(frozenset({"B", "C"}),))
    identify_ad = CollapseOp(classes=(frozenset({"A", "D"}),))
    print("divergent under B~C policy:", divergent(left, right, identify_bc))
    print("divergent under A~D policy:", divergent(left, right, identify_ad))
