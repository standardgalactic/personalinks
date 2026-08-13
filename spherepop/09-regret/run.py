from spherepop import history_view, make_config, parse_sphere, transition
from spherepop.model import BindOp, RefuseOp

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    refused = transition(base, RefuseOp(frozenset({"a2"})))
    then_bound = transition(refused, BindOp("prefix:a"))
    direct_bound = transition(base, BindOp("prefix:a"))
    print("history with regret path:", history_view(then_bound))
    print("history direct path     :", history_view(direct_bound))
    print("histories distinct      :", then_bound.history != direct_bound.history)
