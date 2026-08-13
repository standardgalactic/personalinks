from spherepop import history_view, make_config, parse_sphere
from spherepop.model import BindOp, PopOp
from spherepop.observers import admissible

if __name__ == "__main__":
    # A flat Sphere has no nested Sphere to resolve, so POP is inadmissible.
    flat = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    nested = make_config(parse_sphere("(A (B C) D)"), {"A", "B", "C", "D"})

    before = flat.history
    print("POP admissible on flat sphere  :", admissible(PopOp(), flat))
    print("POP admissible on nested sphere:", admissible(PopOp(), nested))
    print("BIND ALL admissible on flat    :", admissible(BindOp("ALL"), flat))

    # The check never commits anything: history is unchanged either way.
    print("flat history unchanged by check:", flat.history == before)
    print("flat history view              :", history_view(flat))
