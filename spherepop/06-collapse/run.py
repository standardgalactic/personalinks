from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import CollapseOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    out = transition(cfg, CollapseOp(classes=(frozenset({"B", "C"}),)))
    # sorted() directly on option_space breaks once it can hold a mix of
    # plain strings and Quotients (not mutually orderable) -- extensional_view
    # sorts by each option's display representative instead. See experiment
    # 19 for why the Quotient itself, not its representative, is what
    # option_space actually holds after a COLLAPSE.
    print("before:", extensional_view(cfg))
    print("after :", extensional_view(out))
