from spherepop import make_config, parse_sphere, transition
from spherepop.model import BindOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A B C)"), {"alpha", "beta", "axis"})
    out = transition(cfg, BindOp(predicate="prefix:a"))
    print("before:", sorted(cfg.option_space))
    print("after :", sorted(out.option_space))
