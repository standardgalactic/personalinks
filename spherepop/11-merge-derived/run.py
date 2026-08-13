from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import BindOp, CollapseOp

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B C)"), {"A", "B", "C", "x"})
    bound = transition(base, BindOp("in:B,C"))
    merged = transition(bound, CollapseOp(classes=(frozenset({"B", "C"}),)))

    print("bound view        :", extensional_view(bound))
    print("merge-derived view:", extensional_view(merged))
    print("history length    :", len(merged.history))
