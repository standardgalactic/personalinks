from spherepop import make_config, parse_sphere, transition
from spherepop.model import PopOp
from spherepop.views import history_view

if __name__ == "__main__":
    cfg0 = make_config(parse_sphere("(A (B C) D)"), {"A", "B", "C", "D"})
    cfg1 = transition(cfg0, PopOp(path=(1,)))
    print("history length:", len(cfg1.history))
    print("history:", history_view(cfg1))
