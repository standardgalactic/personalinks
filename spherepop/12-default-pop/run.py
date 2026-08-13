from spherepop import make_config, parse_sphere, render_expr, transition
from spherepop.model import PopOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A (B (C D)) E)"), {"A", "B", "C", "D", "E"})

    first = transition(cfg, PopOp())  # default: deepest non-root sphere
    second = transition(first, PopOp())  # default updates with the new shape

    print("before        :", render_expr(cfg.sigma))
    print("after pop #1  :", render_expr(first.sigma), "path:", first.history[-1].path)
    print("after pop #2  :", render_expr(second.sigma), "path:", second.history[-1].path)
