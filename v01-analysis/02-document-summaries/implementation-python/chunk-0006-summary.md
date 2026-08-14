**Explanation**

The file **tests/test_spherepop.py** defines a set of unit‑test cases for t[1D[K
the public SpherePop API (functions such as `parse_program`, `make_config`,[14D[K
`make_config`, `transition`, etc.).  
Each test method demonstrates one or more specific behaviours described in [K
the code comments:

| Test | What it tests |
|------|----------------|
| **SpherepopTests** – `parse_program_and_operation_types` | Verifies that [K
parsing a program yields operations of the correct Python classes (`PopOp`,[9D[K
(`PopOp`, `RefuseOp`, etc.) and that a lone “POP” operation has no path arg[3D[K
argument. |
| **SpherepopTests** – `pop_resolves_scope_not_deletion` | Shows that a `Po[3D[K
`PopOp(path=(1,))` moves the child node *B* one step up (depth‑1) in a labe[4D[K
labeled tree but does not delete nodes; the resulting label structure remai[5D[K
remains unchanged and only the history length increases. |
| **SpherepopTests** – `pop_by_label_resolves_to_same_result_as_path` | Con[3D[K
Confirms that using `PopOp(label="B")` (which internally resolves to the sa[2D[K
same path `(1,)`) produces an identical transition as `PopOp(path=(1,))`. B[1D[K
Both result in moving node *B* up one level while leaving the option space [K
and history untouched. |
| **SpherepopTests** – `refuse_all_options` | Demonstrates that if you try [K
to refuse every available option (`RefuseOp(refused=frozenset({"a","b"}))`)[42D[K
(`RefuseOp(refused=frozenset({"a","b"}))`) the resulting configuration has [K
an empty option set, as expected. |
| **SpherepopTests** – `bind_then_refuse_empty` | Shows a cascade failure: [K
after `BindOp(predicate="prefix:x")` removes all options (empty space), att[3D[K
attempting to `RefuseOp(refused=frozenset({"a"}))` raises an `EvalError` be[2D[K
because the operation cannot be applied to an empty option set. |
| **SpherepopTests** – `collapse_single_element_class` | Tests that collaps[7D[K
collapsing a singleton class `{a}` creates a Quotient object with exactly o[1D[K
one member, which is allowed and observable via `history_view`. |

Each test method calls helper functions such as:

* **`make_config`** – builds an initial configuration from a labeled tree ([1D[K
(`parse_sphere`).  
* **`transition`** – applies the operation to that configuration, returning[9D[K
returning a new state (new sigma, updated option space, history log).  

The purpose of these tests is twofold:

1. **Validation** – ensure that each API call behaves according to its docu[4D[K
documented semantics (e.g., `PopOp` moves scope but does not delete nodes; [K
collapsing a singleton creates a valid Quotient).  
2. **Robustness** – verify error handling (empty option set, invalid operat[6D[K
operation arguments) and edge‑case interactions (refusing all options leads[5D[K
leads to an empty state).

If any of these expectations change in the future (e.g., `PopOp` were to ac[2D[K
actually delete nodes), the test suite would need updating accordingly. Oth[3D[K
Otherwise, they serve as living documentation for SpherePop’s operational s[1D[K
semantics.

---  

**How to run**

```bash
python -m unittest tests/test_spherepop.py
```

Running this command will execute all defined test methods and report any f[1D[K
failures or errors, confirming that the implementation adheres to the inten[5D[K
intended design.

