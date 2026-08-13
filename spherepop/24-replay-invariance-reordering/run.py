from spherepop import (
    admissible,
    eval_program,
    extensional_view,
    make_config,
    parse_program,
    parse_sphere,
)
from spherepop.model import PopOp

if __name__ == "__main__":
    # Part 1: REFUSE and BIND are independent option-space filters, so a
    # whole program replays to the same extensional result whether they
    # run in the order written or swapped -- reordering commuting steps
    # doesn't disturb the outcome.
    base1 = make_config(parse_sphere("(A (B C) D)"), {"a1", "a2", "b1"})
    program_a = parse_program(["REFUSE a2", "BIND prefix:a", "POP 1"])
    program_b = parse_program(["BIND prefix:a", "REFUSE a2", "POP 1"])
    result_a = eval_program(base1, program_a)
    result_b = eval_program(base1, program_b)
    print("program A view:", extensional_view(result_a))
    print("program B view:", extensional_view(result_b))
    print(
        "replay-invariant under REFUSE/BIND reordering:",
        extensional_view(result_a) == extensional_view(result_b),
    )

    # Part 2: POP targets a *position* in the current sigma, not a stable
    # name, so two POPs do not commute the way REFUSE/BIND do. Popping
    # path (1,) first changes what lives at every later index; popping
    # path (2,) first targets a position that doesn't even exist yet on
    # the original sigma.
    base2 = make_config(parse_sphere("(A (B (C D)) E)"), {"z"})
    forward = eval_program(base2, [PopOp(path=(1,)), PopOp(path=(2,))])
    print()
    print("POP(1) then POP(2):", extensional_view(forward)[0])
    print("POP(2) admissible on the *original* sigma:", admissible(PopOp(path=(2,)), base2))
    try:
        eval_program(base2, [PopOp(path=(2,)), PopOp(path=(1,))])
    except Exception as exc:  # EvalError
        print("POP(2) then POP(1) raises:", exc)
