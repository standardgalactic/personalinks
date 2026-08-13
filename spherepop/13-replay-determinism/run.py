from spherepop import (
    eval_program,
    extensional_view,
    history_view,
    make_config,
    parse_program,
    parse_sphere,
)

if __name__ == "__main__":
    program = parse_program(
        [
            "# comments and blank lines are ignored",
            "BIND contains:a",
            "",
            "REFUSE a2",
            "POP 1",
        ]
    )

    base = make_config(parse_sphere("(A (B C) D)"), {"a1", "a2", "b1"})
    run1 = eval_program(base, program)
    run2 = eval_program(base, program)

    print("run1 extensional:", extensional_view(run1))
    print("run2 extensional:", extensional_view(run2))
    print("same extensional :", extensional_view(run1) == extensional_view(run2))
    print("same history     :", history_view(run1) == history_view(run2))
