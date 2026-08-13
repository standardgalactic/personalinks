from spherepop import extensional_view, make_config, parse_sphere, representative, transition
from spherepop.model import CollapseOp, Quotient

if __name__ == "__main__":
    cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
    out = transition(cfg, CollapseOp(classes=(frozenset({"B", "C"}),)))

    print("rendered sigma:", extensional_view(out)[0])
    print("displayed options:", extensional_view(out)[1])

    # The option space holds the class, not the string chosen to display it.
    quotient = Quotient(members=frozenset({"B", "C"}))
    print("Quotient(B,C) in option_space:", quotient in out.option_space)
    print('"B" in option_space directly :', "B" in out.option_space)
    print('"C" in option_space directly :', "C" in out.option_space)

    # Two Quotients are equal purely by membership -- construction order,
    # and which member views.representative happens to pick, are irrelevant
    # to identity.
    same_class_different_order = Quotient(members=frozenset({"C", "B"}))
    print("Quotient(B,C) == Quotient(C,B):", quotient == same_class_different_order)
    print("representative(...) is just a display pick:", representative(quotient))
