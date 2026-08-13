from spherepop import make_config, parse_sphere, regretful, transition
from spherepop.model import BindOp, RefuseOp

if __name__ == "__main__":
    # A base with a committed event, so the common-prefix check below is
    # non-vacuous (see the caveat on regretful()).
    base0 = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    base = transition(base0, BindOp("ALL"))

    candidate1 = transition(base, RefuseOp(frozenset({"a1", "a2"})))  # -> {b1}
    alternative1 = transition(base, BindOp("ALL"))  # -> unchanged {a1, a2, b1}
    print("step 1 regret:", regretful(base, candidate1, alternative1))

    # Extend both branches with an identical, shape-preserving step: regret
    # persists, because neither side's option_space changed relative to
    # the other.
    candidate2 = transition(candidate1, BindOp("ALL"))
    alternative2 = transition(alternative1, BindOp("ALL"))
    print(
        "step 2 regret (after identical further step):", regretful(base, candidate2, alternative2)
    )

    # But regret is a claim about *this* alternative, not an absolute
    # property of candidate2. If the alternative branch itself narrows in
    # a way that stops containing candidate2's options, the strict-subset
    # relation can disappear even though candidate2 never changed.
    alternative3 = transition(alternative2, RefuseOp(frozenset({"b1"})))  # -> {a1, a2}
    print("candidate2 option_space  :", sorted(candidate2.option_space))
    print("alternative3 option_space:", sorted(alternative3.option_space))
    print(
        "regret vs narrowed alternative (now incomparable):",
        regretful(base, candidate2, alternative3),
    )
