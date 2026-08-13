from spherepop import make_config, parse_sphere, transition
from spherepop.model import BindOp, RefuseOp
from spherepop.observers import regretful

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})

    narrow = transition(base, RefuseOp(frozenset({"a1", "a2"})))  # option_space -> {b1}
    unrestricted = transition(base, BindOp("ALL"))  # option_space unchanged -> {a1, a2, b1}
    incomparable = transition(base, BindOp("prefix:a"))  # option_space -> {a1, a2}

    print("narrow option_space      :", sorted(narrow.option_space))
    print("unrestricted option_space:", sorted(unrestricted.option_space))
    print("incomparable option_space:", sorted(incomparable.option_space))

    # A strict subset relative to a same-prefix sibling is regret.
    print("narrow regrets vs unrestricted:", regretful(base, narrow, unrestricted))

    # Two continuations that merely differ (neither's option_space contains
    # the other's) are not regret -- regret is specifically about being
    # strictly smaller, not merely different.
    print("narrow regrets vs incomparable:", regretful(base, narrow, incomparable))

    try:
        # A candidate that doesn't actually extend base can't be judged
        # against it: this raises rather than guessing at a shared ancestor.
        # (Note: this check is only non-vacuous once base itself has at
        # least one committed event -- an empty history is trivially a
        # prefix of anything.)
        committed_base = transition(base, BindOp("ALL"))
        unrestricted2 = transition(committed_base, BindOp("ALL"))
        unrelated = transition(make_config(parse_sphere("(X)"), {"z"}), RefuseOp(frozenset({"z"})))
        regretful(committed_base, unrelated, unrestricted2)
    except ValueError as exc:
        print("unrelated candidate rejected:", exc)
