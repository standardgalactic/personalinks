from spherepop import make_config, parse_sphere
from spherepop.model import BindOp, PopOp, RefuseOp
from spherepop.observers import equivalent_at

if __name__ == "__main__":
    base = make_config(parse_sphere("(A (B C) D)"), {"a1", "a2", "b1"})

    shared_prefix = [BindOp("contains:a"), RefuseOp(frozenset({"a2"}))]
    ops_left = shared_prefix + [PopOp(path=(1,))]
    ops_right = shared_prefix + [BindOp("ALL")]

    print("equivalent at k=0:", equivalent_at(base, ops_left, ops_right, 0))
    print("equivalent at k=1:", equivalent_at(base, ops_left, ops_right, 1))
    print("equivalent at k=2:", equivalent_at(base, ops_left, ops_right, 2))
    # At k=3 the sequences part ways: left has popped the nested scope,
    # right has only re-bound the (already-settled) option space.
    print("equivalent at k=3:", equivalent_at(base, ops_left, ops_right, 3))

    # base itself is untouched by any of this replay.
    print("base history still empty:", base.history == ())
