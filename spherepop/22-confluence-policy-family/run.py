from spherepop import extensional_view, irreducibly_divergent, make_config, parse_sphere, transition
from spherepop.model import CollapseOp, PopOp, RefuseOp

if __name__ == "__main__":
    policy_family = [
        CollapseOp(classes=(frozenset({"B", "C"}),)),
        CollapseOp(classes=(frozenset({"A", "D"}),)),
        CollapseOp(classes=(frozenset({"a1", "a2"}),)),
    ]

    # Structural divergence: no atom-renaming policy can fix a difference
    # in bracket structure, so this survives the whole family.
    structural_base = make_config(parse_sphere("(A (B C) D)"), {"x", "y"})
    structural_left = transition(structural_base, PopOp(path=(1,)))
    structural_right = structural_base
    print(
        "structural left/right sigmas:",
        extensional_view(structural_left)[0],
        "/",
        extensional_view(structural_right)[0],
    )
    print(
        "irreducibly divergent over family:",
        irreducibly_divergent(structural_left, structural_right, policy_family),
    )

    # Naming divergence: divergent under most of the family, but the last
    # policy in the family happens to be exactly the one that identifies
    # them -- so it is divergent under *some* policies without being
    # irreducibly divergent over this family.
    naming_base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    naming_left = transition(naming_base, RefuseOp(frozenset({"a2"})))
    naming_right = transition(naming_base, RefuseOp(frozenset({"a1"})))
    print(
        "irreducibly divergent over same family:",
        irreducibly_divergent(naming_left, naming_right, policy_family),
    )
