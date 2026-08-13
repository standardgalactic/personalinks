from spherepop import (
    extensional_view,
    history_prefix_view,
    history_view,
    make_config,
    parse_sphere,
    transition,
)
from spherepop.model import BindOp, PopOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A (B C) D)"), {"alpha", "beta", "charlie"})
    cfg = transition(cfg, PopOp(path=(1,)))
    cfg = transition(cfg, BindOp("prefix:a"))
    print("extensional:", extensional_view(cfg))
    print("history all:", history_view(cfg))
    print("history prefix(1):", history_prefix_view(cfg, 1))
