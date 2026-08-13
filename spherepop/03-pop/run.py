from spherepop import make_config, parse_sphere, render_expr, transition
from spherepop.model import PopOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A (B C) D)"), {"A", "B", "C", "D"})
    out = transition(cfg, PopOp(path=(1,)))
    print("before:", render_expr(cfg.sigma))
    print("after :", render_expr(out.sigma))
