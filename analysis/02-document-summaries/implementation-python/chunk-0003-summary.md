**Summary**

The `validate_config` function (and its supporting helper functions) checks[6D[K
checks that a *Spherepop* configuration satisfies several structural invari[6D[K
invariants:

| Invariant | What it guarantees |
|-----------|---------------------|
| **Sigma well‑formedness** (`_validate_sigma`) | Every expression under th[2D[K
the top‑level `sigma` is either an atom or a sphere whose `items` attribute[9D[K
attribute is a tuple of atoms (or spheres). No dangling references. |
| **Option provenance** (`_validate_option_provenance`) | Each element in `[1D[K
`option_space`: <br>• If it’s a plain string, that name must appear as the [K
name of an atom defined in `sigma`. <br>• If it’s a `Quotient`, each member[6D[K
member of its `members` set must be either (a) originally present in `sigma[6D[K
`sigma.items` or (b) have already been collapsed by a previous `CollapseEve[12D[K
`CollapseEvent` in the history. |
| **History sequential** (`_validate_history_sequential`) | History indices[7D[K
indices are consecutive starting at 0, i.e., if there are *n* events then `[1D[K
`history_index = list(range(n))`. This ensures that every later event follo[5D[K
follows chronologically from earlier ones. |
| **Collapse log consistency** (`_validate_collapse_log`) | Every entry in [K
`collapse_log` (a tuple `(history_index, classes)`) must reference an exist[5D[K
existing `CollapseEvent` at the indicated history index. |
| **Quotient uniqueness** (`_validate_quotient_uniqueness`) | No two quotie[6D[K
quotients share exactly the same set of members; this prevents duplicate wa[2D[K
ways of representing the same collapsed state. |
| **Label uniqueness (optional)** (`_validate_label_uniqueness`) | If the `[1D[K
`sigma` carries a label, that label must be globally unique within the sigm[4D[K
sigma (i.e., no two spheres may have identical labels). |

**How validation works**

1. **Collect atoms from `sigma`.**  
   `_collect_atoms` recursively walks the expression tree and gathers every[5D[K
every plain‑string atom name present in `sigma`.

2. **Track collapsed members via history.**  
   By scanning through each `CollapseEvent` (which records which classes ha[2D[K
have been collapsed), we build a set of “collapsed” member names.

3. **Validate each option space element.**  
   - For a plain string, check membership in the collected sigma atoms.  
   - For a `Quotient`, verify that every inner name is either an original s[1D[K
sigma atom or a previously‑collapsed class (i.e., present in the collapsed [K
set).

4. **Collect violations.**  
   Any failure triggers a descriptive error message such as:
   ```
   Option 'X' not found in sigma atoms: ('A', 'B', 'C')
   ```

**Provisional semantics**

The module deliberately *does not* enforce any semantic interpretation for [K
unresolved theoretical issues:

- **COLLAPSE composition** (when collapsing already‑quoted options) is repo[4D[K
reported as “unsupported” because the paper leaves its composition law open[4D[K
open.
- **Quotient predicate lifting** is left unvalidated, following Q3 in THEOR[5D[K
THEORY_STATUS.md.

**Usage**

```python
from spherepop import make_config, parse_sphere

cfg = make_config(parse_sphere("(A B C)"), {"A", "B", "C"})
if validate_config(cfg):
    raise ValueError("Invalid configuration")
```

If `validate_config` returns an empty list, the config passes all structura[9D[K
structural checks; otherwise you receive a clear error message indicating e[1D[K
exactly which invariant failed. This observational validation is intended f[1D[K
for testing, debugging, or any workflow where safety of invariants matters [K
but no semantic decision must be taken on open questions.

