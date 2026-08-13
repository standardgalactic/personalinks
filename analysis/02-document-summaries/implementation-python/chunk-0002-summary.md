**Regretful continuation check**

```python
def regretful(
    base: Config,
    candidate: Config,
    alternative: Config,
) -> bool:
    """
    Return True iff *candidate* is a **regretful** continuation of *base*.
    
    A configuration X is called “regretful” for another configuration Y whe[3D[K
when:

      1. The two histories share exactly the same prefix (i.e., they are
         extensions of one common initial Config).
      
      2. After that shared prefix, `candidate` ends up with a **smaller**
         option space** than `alternative`.  
         
    Both *base* and *candidate* must be reachable from the same history
    (checked by `history_is_prefix`). The purpose of this function is to
    expose a structural property – that some later commit “wastes” options
    that could have been retained if we had taken an alternative path.
    
    Parameters
    ----------
    base : Config
        The shared prefix (the “what”) up to which the two histories agree.[6D[K
agree.
    
    candidate : Config
        A continuation of *base* that we want to test for regret. Its optio[5D[K
option
        space must be strictly smaller than `alternative` after the same
        prefix.
    
    alternative : Config
        Another reachable continuation from *base*. It serves as the refere[6D[K
reference
        against which we measure regret – its post‑prefix option space is t[1D[K
the
        baseline we compare against.
    
    Returns
    -------
    bool
        True if and only if `candidate` is regretful with respect to `alter[6D[K
`alternative`.
    """
    # --------------------------------------------------------------
    # 1️⃣ Verify that both candidate and alternative are extensions of *base[5D[K
*base*.
    # --------------------------------------------------------------
    if not (history_is_prefix(base, candidate) and history_is_prefix(base, [K
alternative)):
        raise ValueError(
            "Both candidate and alternative must be reachable from the same[4D[K
same "
            f"prefix Config (`{base}`)."
        )

    # --------------------------------------------------------------
    # 2️⃣ Compare the *post‑prefix* option spaces.
    # --------------------------------------------------------------
    left_options = set(candidate.option_space)
    right_options = set(alternative.option_space)

    # Regret is defined only when candidate’s space shrinks:
    return len(left_options) < len(right_options)
```

### How it works

| Step | What we do |
|------|-------------|
| **Prefix check** (`history_is_prefix`) | Guarantees that `candidate` and [K
`alternative` diverge *after* the same initial sequence of operations. With[4D[K
Without this, any option‑space comparison would be meaningless because they[4D[K
they might have come from different ancestors. |
| **Option‑space size** (set cardinality) | Since `option_space` is a froze[5D[K
frozen set of atoms or quotients, comparing lengths tells us whether `candi[6D[K
`candidate` has *lost* some options relative to `alternative`. A regretful [K
continuation must lose at least one option; the inequality (`<`) enforces t[1D[K
this. |
| **Return** | The function returns `True` exactly when both conditions are[3D[K
are satisfied – otherwise it’s not a regretful path under that shared prefi[5D[K
prefix. |

### Example

```python
from spherepop.model import Config, Atom, CollapseOp
from spherepop.observers import transition, regretful

# Build two histories from the same base sigma.
sigma = (Atom("a"), Atom("b"), Atom("c"))  # label="root"

base_cfg = Config(sigma=sigma, history=())

# Path A: collapse all three atoms → single quotient "abc"
candidate_cfg = transition(base_cfg, CollapseOp(classes={frozenset({"a","b"[38D[K
CollapseOp(classes={frozenset({"a","b","c"})}))

# Path B: only collapse the first two atoms → quotients {"ab", "c"}
alternative_cfg = transition(base_cfg, CollapseOp(classes={frozenset({"a","[36D[K
CollapseOp(classes={frozenset({"a","b"}), frozenset({"c"})}))

print(regretful(base_cfg, candidate_cfg, alternative_cfg))
# --> True  (candidate ends with one option vs. alternative’s two)
```

In this tiny world, `candidate` loses the distinctness of “c” compared to `[1D[K
`alternative`, so it is **regretful**.

---

*The function above encapsulates the formal notion of regret as used in sph[3D[K
spherepop: a configuration that after sharing an initial prefix yields a st[2D[K
strictly smaller reachable option space than another possible continuation.[13D[K
continuation.*

