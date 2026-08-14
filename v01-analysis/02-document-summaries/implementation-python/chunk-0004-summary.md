Below is a self‑contained “quick start” guide for the **SpherePop** simulat[7D[K
simulation framework.  
It explains what each part of the code does (both in `parser.py` and in `mo[3D[K
`model.py`) and shows how to run tests, modify configurations, and extend t[1D[K
the system.

---

## 1️⃣ High‑level Overview

| File | Purpose |
|------|---------|
| **parser.py** | Converts a human‑readable *sphere* string (e.g. `(A B)` )[1D[K
) into an internal data structure (`Sphere`), raises `ParseError`s for malf[4D[K
malformed input, and parses individual operations such as `BindOp`, `PopOp`[7D[K
`PopOp`, etc. |
| **model.py** | Holds the runtime objects: `Atom`, `CollapseOp`, `PopOp`, [K
`RefuseOp`, plus a generic `Operation`. Provides methods to evolve a config[6D[K
configuration (a set of atoms) forward in time using any combination of the[3D[K
these operations. |

Together they let you:

* Define a world topology with **spatial relations** (`A B` means “A and B [K
are neighbours”).  
* Apply *operations* that mutate the configuration (pop, refuse, bind all, [K
etc.).  
* Reason about convergence/divergence between two possible futures.

---

## 2️⃣ Core Concepts

### Configurations
A **configuration** is a mapping `Atom → {History}` where:

* `History` = list of operations that led to the presence of an atom.  
* The initial state (`()` history) means “no operation has generated this a[1D[K
atom yet”.

The model can be thought of as a *state machine*: each time you call `.evol[6D[K
`.evolve(op)` on a config, the op is appended to its atoms’ histories and m[1D[K
may cause previously hidden branches (or disappearations) in other parts of[2D[K
of the world.

### Operations
| Operation | What it does |
|-----------|--------------|
| **BindOp(expr)** – *All* | Keep every atom that satisfies `expr`. Equival[7D[K
Equivalent to a wildcard “select all”. |
| **PopOp(path)** – *Partial* | Removes atoms at the given path in the tree[4D[K
tree (e.g. `(1,)` removes B from `(A, B, C)`, leaving `A,C`). |
| **RefuseOp(atoms)** – *Negative* | Refuses any of the listed atoms (they [K
are removed forever). |
| **CollapseOp(classes)** – *Set* | Collapses a set of atoms into one “supe[5D[K
“super‑atom”. Future ops that mention only the collapsed atom will treat it[2D[K
it as if all members were present. |

---

## 3️⃣ Running Tests

The test suite lives in `tests/` and can be executed with:

```bash
python -m unittest discover tests/
```

All tests cover edge cases (empty input, malformed expressions, divergent v[1D[K
vs convergent futures) and are written using pytest.

If you add new functionality, write a small test that asserts the expected [K
behaviour of your parser or model code. The existing tests already cover mo[2D[K
most error‑handling paths in `parser.py`.

---

## 4️⃣ How to Use It

### Step 1 – Install

```bash
pip install -r requirements.txt   # includes numpy for performance (optiona[8D[K
(optional)
```

### Step 2 – Minimal Example

```python
from spherepop.model import parse_sphere, Atom, PopOp, BindOp, Sphere

# Define a simple world: A and B are neighbours.
world = parse_sphere("(A B)"), {"a1", "a2"}   # first arg = topology, secon[5D[K
second = initial atoms

# Evolve it with two possible futures:
future_1 = world[0].evolve(PopOp((1,)))      # Pop B → (A)
future_2 = world[0].evolve(BindOp("ALL"))    # Keep all current atoms → (A,[3D[K
(A,B)

print(future_1.history)   # Shows which operations led to the final state
print(future_2.history)   # Same for the “all” future
```

### Step 3 – Using Policies

Policies let you decide *which* futures are “acceptable”. Example:

```python
from spherepop.model import collapse_op, is_confluent

# Collapse A and B into a single entity:
policy = collapse_op(classes=(frozenset({"a1", "b1"}),))

# Check if the two alternatives converge under this policy:
if is_confluent(future_1, future_2, policy):
    print("They are confluent – no further divergence.")
else:
    print("They diverge; we need a more specific rule.")
```

### Step 4 – Extending

#### Adding New Operations
If you want to support custom ops (e.g., “flip the state of A”), add them i[1D[K
in `parser.py`:

```python
# Inside parse_operation:
elif name == "FlipOp":
    return FlipOperation(parse_expr(args[0]))
```

Then implement a matching class in `model.py` (`FlipOperation`) and expose [K
it via `.evolve()`.

#### Adding New Topologies

To let the parser recognise custom bracketing (e.g., “(A-B)”), modify the t[1D[K
token‑regex for `parse_sphere`:

```python
# In parse_program or parse_expr, add a branch:
elif match.group("bracket"):   # e.g. "(A-B)"
    return [Atom(atom.name) for atom in tokenize_atom(match.group("atom"))][35D[K
tokenize_atom(match.group("atom"))]
```

Then test that your custom grammar still raises meaningful `ParseError`s on[2D[K
on malformed strings.

---

## 5️⃣ Common Pitfalls & Gotchas

| Issue | Why it Happens | Fix |
|-------|----------------|-----|
| **`unexpected end of input`** after a token you expected | You missed whi[3D[K
whitespace or parentheses around an atom. | Ensure each atom is quoted and [K
separated by spaces/parens (e.g., `"(A B)"`). |
| **Operation not recognised** (`ParseError: invalid operation name`) | Typ[3D[K
Typo in the op string (`PopOp` vs `popop`). | Double‑check spelling against[7D[K
against the enum list defined at the top of `parser.py`. |
| **Wrong tree path returned** (e.g., `PopOp((0,))` on `(A B)` removes A in[2D[K
instead of B) | The parser treats path numbers as *depth* not *position*. |[1D[K
| Use zero‑based index that matches your intended position: for a leaf at i[1D[K
index 1 use `(1,)`. |
| **Collapsing an already single atom** (`CollapseOp(classes=(frozenset({"a[35D[K
(`CollapseOp(classes=(frozenset({"a"}),))`) | No effect, but can be confusi[7D[K
confusing. | Only collapse groups with ≥2 atoms; otherwise the operation is[2D[K
is a no‑op. |

---

## 6️⃣ Extending Documentation

If you add new classes or functions (e.g., `FlipOperation` in Appendix G), [K
remember to:

1. **Update** the docstring at the top of that module with any new usage ex[2D[K
examples.
2. Add a brief “Tested Cases” section showing what behaviours your code cov[3D[K
covers (similar to how `BindOp`, `PopOp`, etc., are tested).

---

## 7️⃣ Quick Reference Cheat‑Sheet

```python
# Create a world from a string + initial atoms
world = parse_sphere("(A B C)", {"a1", "b2", "c3"})

# Evolve with a PopOp (removes the second atom)
future = world[0].evolve(PopOp((1,)))

# Evolve with a CollapseOp (treat A & B as one entity)
future_collapsed = future.evolve(collapse_op(classes=(frozenset({"a1","b2"}[56D[K
future.evolve(collapse_op(classes=(frozenset({"a1","b2"}),))))

# Check if two futures are confluent under policy
if is_confluent(future, future_collapsed, collapse_op(classes=(frozenset({"[33D[K
collapse_op(classes=(frozenset({"a1","b2"}),))):
    print("They converge.")
else:
    print("They diverge – need a finer policy.")
```

---

### 🎯 TL;DR

* `parser.py` converts strings like `(A B)` into an internal tree (`Sphere`[9D[K
(`Sphere`) and parses operation tokens.
* Errors (empty input, unexpected end) raise explicit `ParseError`s with he[2D[K
helpful messages.
* Use the provided test suite to verify your own custom parsers or operatio[8D[K
operations.

Feel free to dive into any of the example files—`tests/test_parser.py`, `te[3D[K
`tests/test_model.py`, or `example_worlds/*.py`—to see concrete usage. Happ[4D[K
Happy modeling!

