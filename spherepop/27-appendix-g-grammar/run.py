from spherepop import eval_program, extensional_view, make_config
from spherepop.grammar import parse_event, parse_sphere

if __name__ == "__main__":
    # This sigma and these events are written in Appendix G's own concrete
    # syntax, not the lab's convenience command language -- and they run
    # through the exact same transition()/eval_program() as everything else.
    sigma = parse_sphere("(outer: A (inner: B C) D)")
    print("parsed sigma label:", sigma.label)
    print("parsed inner label:", sigma.items[1].label)

    cfg = make_config(sigma, {"a1", "a2", "b1"})
    program = [
        parse_event("refuse(outer, {a2})"),
        parse_event("bind(outer, ALL)"),
        parse_event("collapse(outer, {a1~b1})"),
        parse_event("pop(inner)"),
    ]
    out = eval_program(cfg, program)

    print("final view:", extensional_view(out))
    print("event labels, in order:", [e.label for e in out.history])

    # The Label on refuse/bind/collapse is recorded (Appendix G provenance)
    # but does not yet partition option_space by label -- that is Appendix
    # B's poset-of-option-spaces semantics, a separate planned rewrite.
    # REFUSE/BIND/COLLAPSE here all still acted on one global option space
    # regardless of which label was named.
