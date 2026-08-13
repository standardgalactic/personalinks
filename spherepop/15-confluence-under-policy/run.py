from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import CollapseOp, RefuseOp
from spherepop.observers import confluent, divergent

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})

    # Two continuations that refuse different members of {a1, a2}: their raw
    # extensional views disagree, and no operation so far has claimed they
    # should be treated as "the same" outcome.
    left = transition(base, RefuseOp(frozenset({"a2"})))
    right = transition(base, RefuseOp(frozenset({"a1"})))
    print("left view (no policy) :", extensional_view(left))
    print("right view (no policy):", extensional_view(right))

    identify_a = CollapseOp(classes=(frozenset({"a1", "a2"}),))
    unrelated_policy = CollapseOp(classes=(frozenset({"b1", "b2"}),))

    print("confluent under a1~a2 policy   :", confluent(left, right, identify_a))
    print("divergent under unrelated policy:", divergent(left, right, unrelated_policy))

    # confluent()/divergent() never append the policy to left or right themselves.
    print("left history unchanged  :", len(left.history) == 1)
    print("right history unchanged :", len(right.history) == 1)
