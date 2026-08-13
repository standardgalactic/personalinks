from spherepop import make_config, parse_sphere, transition
from spherepop.model import RefuseOp

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A B C)"), {"o1", "o2", "o3"})
    out = transition(cfg, RefuseOp(refused=frozenset({"o2"})))
    print("before:", sorted(cfg.option_space))
    print("after :", sorted(out.option_space))
