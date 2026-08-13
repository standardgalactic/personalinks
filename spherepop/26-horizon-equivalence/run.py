from spherepop import extensionally_equivalent, horizon_equivalent, make_config, parse_sphere
from spherepop.model import BindOp, RefuseOp

if __name__ == "__main__":
    # Two configs that look different right now...
    left = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    right = make_config(parse_sphere("(A B)"), {"a1", "a2", "c1"})
    print("extensionally equivalent now:", extensionally_equivalent(left, right))

    # ...but under a candidate pool that only ever asks about the "a"
    # prefix, every reachable 1-step future looks the same either way.
    a_only_pool = [BindOp("prefix:a")]
    print("horizon-equivalent (k=1, a-only pool):", horizon_equivalent(left, right, a_only_pool, 1))

    # Widen the pool to something that *can* see the b1/c1 difference:
    # equivalence at the same horizon disappears.
    wider_pool = [BindOp("prefix:a"), RefuseOp(frozenset({"a1"})), RefuseOp(frozenset({"a2"}))]
    print("horizon-equivalent (k=1, wider pool):", horizon_equivalent(left, right, wider_pool, 1))

    # k=0 is exactly extensional equivalence of the current configs.
    print("horizon-equivalent (k=0):", horizon_equivalent(left, right, [], 0))
