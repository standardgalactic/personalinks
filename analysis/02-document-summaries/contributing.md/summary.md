**Theoretical Synthesis for “contributing.md”**

---

### 1. Thesis  

Spherepop is a formal, algebraic system built around four primitive operati[7D[K
operations—**POP**, **REFUSE**, **BIND**, and **COLLAPSE**—that together co[2D[K
constitute a closed algebra (the *Closed Algebra Principle*). Each primitiv[8D[K
primitive corresponds to a specific operation on the state of a computation[11D[K
computational sphere, and all higher‑level behaviours are derived from thes[4D[K
these primitives. The project follows a strict “provisional semantics” poli[4D[K
policy: any gap in the theoretical grounding must be documented in `THEORY_[8D[K
`THEORY_STATUS.md` so that future work can address it. Observers are requir[6D[K
required to be pure functions that return only non‑configuration data, ensu[4D[K
ensuring referential transparency and enabling formal verification.

---

### 2. Primitives / Definitions  

| Primitive | Formal Definition (derived from Appendix A) |
|-----------|--------------------------------------------|
| **POP**   | Removal of a datum from the observable set; mathematically ex[2D[K
expressed as `x → POP(x) = empty`. |
| **REFUSE**| Negation of an acceptance condition on a reference point; for[3D[K
formally `r ↦ REFUSE(r) = ¬acceptance(r)`. |
| **BIND**  | Association of two variables under a binding relation; writte[6D[K
written `a ↔ BIND(a,b) ⇔ (a,b) ∈ BindingRelation`. |
| **COLLAPSE**| Collapse of a set of mutually dependent states into a singl[5D[K
single canonical form; symbolically `S ↦ COLLAPSE(S) = CanonicalForm(S)`. |[1D[K
|

These primitives satisfy the *Closed Algebra* property: no additional primi[5D[K
primitive can be added without an extensive justification and discussion, a[1D[K
as evidenced by Appendix B’s “Plan B” section.

---

### 3. Formalism  

The system is expressed in a deterministic state‑transition lattice (DSL) g[1D[K
governed by:

1. **Transition Rules** – Each primitive maps directly to a rule that updat[5D[K
updates the internal configuration:
   - `POP(state, x)` → `state \ {x}`  
   - `REFUSE(state, r)` → `state ∧ ¬acceptance(r)`  
   - `BIND(state, (a,b))` → `state ∪ {(a ↔ b)}`  
   - `COLLAPSE(state)` → `CanonicalForm(state)`

2. **Observer Interface** – Pure functions returning non‑configuration valu[4D[K
values:
   ```python
   def observer_fn(config: Config) -> Observation:
       # pure computation, no side effects
       return observation_value
   ```

3. **Experimental Manifestation** – Experiments are encoded as self‑contain[12D[K
self‑contained modules (`run.py`) with a manifest entry describing the prop[4D[K
proposition, invariant, and expected output.

---

### 4. Mechanisms  

- **Workflow Engine**: Orchestrates development by enforcing:
  - Issue creation for nontrivial changes,
  - Test addition (including experimental tests via `@pytest.mark.experimen[23D[K
`@pytest.mark.experimental`),
  - Linting (`ruff`, `mypy`) verification,
  - Conventional commit messages, and
  - Updated documentation where public APIs change.

- **Verification Suite**: The script `python -m spherepop.lab verify` check[5D[K
checks that every experiment respects its invariant (e.g., `C0`, `Ω`, diver[5D[K
divergence properties) by comparing against the expected output files (`exp[5D[K
(`expected.txt?`).

---

### 5. Major Arguments  

1. **Closed Algebra Sufficiency** – By limiting to four primitives, the sys[3D[K
system avoids over‑parameterisation while retaining full expressive power f[1D[K
for its intended domain (e.g., logical consistency proofs in distributed sy[2D[K
systems). Any extension would require a new primitive to be justified and d[1D[K
documented.

2. **Observer Pattern Guarantees Predictability** – Pure observers eliminat[8D[K
eliminate hidden state dependencies, enabling:
   - Formal reasoning about system behaviour,
   - Automated property testing,
   - Compatibility with formal verification tools (e.g., model checkers).

3. **Provisional Semantics & Theory Status Tracking** – The policy ensures [K
that unresolved theoretical questions do not block implementation progress;[9D[K
progress; each gap is explicitly recorded for future investigation.

---

### 6. Dependencies Between Concepts  

- **POP ↔ REFUSE**: `REFUSE` can be seen as a conditional form of `POP` (re[3D[K
(removing only if the condition fails). Their interaction is formalised in [K
Appendix C.
- **BIND & COLLAPSE**: Binding establishes relationships that may later col[3D[K
collapse into canonical forms, crucial for handling equivalence classes acr[3D[K
across multiple experiments.
- **Observer Semantics ↔ Experiment Manifests**: Observers are used to asse[4D[K
assert properties of experimental outcomes; thus each manifest entry must r[1D[K
reference a documented observer or its provisional status.

---

### 7. Implications  

1. **Scalability** – Because the primitives are stateless and composable, S[1D[K
Spherepop can be applied in multi‑agent systems where distributed coordinat[9D[K
coordination is required without centralised state management.
2. **Verification Feasibility** – The combination of pure observers and a v[1D[K
verification script makes it possible to certify that experimental runs sat[3D[K
satisfy logical invariants (e.g., consistency under different `COLLAPSE` po[2D[K
policies).
3. **Community Governance** – The requirement for issues, tests, and docume[6D[K
documentation reviews creates an explicit feedback loop that mitigates spec[4D[K
speculative changes and encourages collaborative theorisation.

---

### 8. Unresolved Problems  

- **Plan B (Poset Semantics)** – Integration of a poset‑based semantics wou[3D[K
would require refactoring core algebraic structures; this remains under dis[3D[K
discussion in Appendix B.
- **Observer Composition** – Certain observer combinations may not yet have[4D[K
have proven compositional properties, necessitating further work on the `TH[3D[K
`THEORY_STATUS.md` entries (e.g., Q2b).
- **Closed Algebra Extension** – Adding a fifth primitive would demand exte[4D[K
extensive justification and community consensus before being codified.

---

### 9. Internal Tensions  

1. **Provisional vs. Paper‑Licensed Claims** – The “provisional semantics” [K
policy forces developers to defer conclusions until formal proof exists, cr[2D[K
creating tension between rapid implementation (for experimental validation)[11D[K
validation) and rigorous documentation.
2. **Observability vs. State Preservation** – While observers must be pure,[5D[K
pure, preserving the internal state required for `POP`, `REFUSE`, etc., can[3D[K
can lead to performance trade‑offs that need careful balancing in high‑thro[9D[K
high‑throughput scenarios.

---

### 10. Citations  

- **Paper**: “The History of Spherepop” (defines POP, REFUSE, BIND, COLLAPS[7D[K
COLLAPSE).  
- **Appendices A‑G** (contain detailed algebraic proofs and definitions for[3D[K
for each primitive).  
- **THEORY_STATUS.md** – tracks provisional vs. paper‑licensed concepts; us[2D[K
used to flag unresolved issues such as Plan B and composition theory gaps.

---

*End of Synthesis.*
