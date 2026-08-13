from spherepop import make_config, parse_sphere, transition
from spherepop.model import BindOp, CollapseOp, PopOp, RefuseOp
from spherepop.observers import (
    admissible,
    confluent,
    divergent,
    equivalent_at,
    extensionally_equivalent,
    intensionally_equivalent,
    irreducibly_divergent,
    regretful,
)

if __name__ == "__main__":
    base = make_config(parse_sphere("(A (B C) D)"), {"a1", "a2", "b1"})
    committed = transition(base, BindOp("ALL"))
    other = transition(committed, RefuseOp(frozenset({"a2"})))
    policy = CollapseOp(classes=(frozenset({"a1", "a2"}),))

    snapshot = (committed.sigma, committed.history, committed.option_space, committed.collapse_log)

    # Run every observer in the module against `committed`, in a way that
    # touches each of its arguments (as base, as candidate, as either side
    # of a comparison), and discard every result.
    admissible(PopOp(path=(1,)), committed)
    confluent(committed, other, policy)
    divergent(committed, other, policy)
    irreducibly_divergent(committed, other, [policy])
    regretful(committed, other, committed)
    equivalent_at(committed, [PopOp(path=(1,))], [BindOp("ALL")], 1)
    intensionally_equivalent(committed, other)
    extensionally_equivalent(committed, other)

    after = (committed.sigma, committed.history, committed.option_space, committed.collapse_log)
    print("every field unchanged after the full observer battery:", snapshot == after)
    print("committed history length still:", len(committed.history))
