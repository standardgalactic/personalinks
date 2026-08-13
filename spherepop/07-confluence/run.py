from spherepop import extensional_view, make_config, parse_sphere, transition
from spherepop.model import BindOp, RefuseOp

if __name__ == "__main__":
    base = make_config(parse_sphere("(A B)"), {"a1", "a2", "b1"})
    left = transition(transition(base, BindOp("prefix:a")), RefuseOp(frozenset({"a2"})))
    right = transition(transition(base, RefuseOp(frozenset({"b1"}))), BindOp("prefix:a"))
    print("left view :", extensional_view(left))
    print("right view:", extensional_view(right))
    print("confluent extensional view:", extensional_view(left) == extensional_view(right))
