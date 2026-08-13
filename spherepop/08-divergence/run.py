from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import BindOp, RefuseOp

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B)"), {"alpha", "beta", "gamma"})
    left = transition(base, BindOp("contains:a"))
    right = transition(base, RefuseOp(frozenset({"alpha"})))
    print("left view :", extensional_view(left))
    print("right view:", extensional_view(right))
    print("divergent extensional view:", extensional_view(left) != extensional_view(right))
