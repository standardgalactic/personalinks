from spherepop.poset import OptionSpace, PosetError, minimal_elements, pop_minimal


def pop_sequence(
    poset: tuple[OptionSpace, ...], labels: tuple[str, ...]
) -> tuple[OptionSpace, ...]:
    out = poset
    for label in labels:
        out = pop_minimal(out, label)
    return out


if __name__ == "__main__":
    # Two distinct labels with equal minimal content should be jointly minimal.
    # Popping either first should leave the same extensional remainder.
    base = (
        OptionSpace("alpha", frozenset({"x"})),
        OptionSpace("beta", frozenset({"x"})),
        OptionSpace("gamma", frozenset({"x", "y"})),
    )

    minimals = tuple(space.label for space in minimal_elements(base))
    left_then_right = pop_sequence(base, ("alpha", "beta"))
    right_then_left = pop_sequence(base, ("beta", "alpha"))

    print("initial minimal labels:", minimals)
    print("left_then_right:", tuple(space.label for space in left_then_right))
    print("right_then_left:", tuple(space.label for space in right_then_left))
    print("commute on equal-content minimals:", left_then_right == right_then_left)

    # Non-minimal POP remains invalid.
    try:
        pop_minimal(base, "gamma")
    except PosetError as err:
        print("non-minimal rejection:", str(err))
