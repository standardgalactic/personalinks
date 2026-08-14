**Bidirectional Historical Type Checking**

The core idea is to split dependent‑type judgment into two complementary ph[2D[K
phases:

1. **Synthesis (⇒)** – Determine a type for an *untyped* term `t` given onl[3D[K
only its body and the current context of known types `H`.

2. **Checking (←)** – Confirm that an already typed term `t : A` is well‑ty[7D[K
well‑typed with respect to the surrounding environment.

Both judgments are expressed as historical pairs:

\[
(H,\; \text{synthesis}) \quad\text{or}\quad (H, \; \text{checking}),
\]

where `H` records all provenance events required for that judgment.  
Because every rule now produces a *completed* history rather than just a ty[2D[K
type,
the kernel remains inside the trusted kernel and no external proof objects [K
are
required.

---

### 1. Typing Rules in Historical Form

All original inference rules of System F‑with‑histories (or dependent type [K
theory)
are reinterpreted as either synthesis or checking judgments, with `H` built[5D[K
built by
the primitive event constructors described earlier:

| Rule Type | Original Judgment | Historical Version |
|-----------|-------------------|--------------------|
| **Synthesis** – Variable introduction (`Γ ⊢ x : A`) | `x : A ∈ Γ` | `(Δ;e[5D[K
`(Δ;e_var) → (Γ, H)` where `e_var` records the variable binding. |
| **Synthesis** – Pi‑type formation (`Γ,x:A ⊢ t:B(x) ⇒ C ⇒ D`) | `t : ∀x:A.[5D[K
∀x:A.B` | `(H; e_pi(A,B,C))` where `e_pi` stores the abstraction and its su[2D[K
substitution history. |
| **Checking** – Application (`Γ,t:A ⊢ f(t') : C ⇒ D, H₁` ) | `f(t) : C ⇒ D[1D[K
D` | `(H₂; e_app(H₁,f,t'))` records the beta‑reduction event that applied `[1D[K
`t`. |
| **Synthesis** – Let (`Γ ⊢ x = t : A, H₃` ) | `let x=t in u:A` | `(H₄; e_l[3D[K
e_let(H₃,x,t))` where `e_let` records the substitution and provenance. |

*Every rule either* (a) **produces** a new event that extends `H`, *or* (b)[3D[K
(b)
**consumes** an existing history by replaying it to verify compatibility[13D[K
compatibility.

---

### 2. Algorithmic Structure

#### Step 1 – Synthesize the Type of an Expression  

```hs
synthesize(t, Γ) = 
    if t is a term with known shape:
        attempt all possible synthesis rules (e_var, e_pi, e_app, …)
        for each rule r that succeeds, update H := r(Hₚ) where r produces e[1D[K
events e_r.
        return (H, typed-term)
    else:
        report error “cannot synthesize type”
```

#### Step 2 – Check an Expression Against a Known Type  

```hs
check(t:A, Γ', t' : B, H') = 
    if t' is of the same shape as t but may differ in provenance:
        replay H' to obtain a complete history for t': (Hₜ, u)
        ensure that all events required by `t` are replay‑equivalent to tho[3D[K
those
          recorded in H'. If not, report mismatch.
    else if types do not match after unfolding dependent terms using histor[6D[K
histories:
        report type error “mismatch”
    else:
        return (Γ', t : A)   -- no further change needed
```

Both functions are **deterministic** because every possible reduction path [K
is fully
recorded in the history `H`. Consequently, a given term and context can lea[3D[K
lead to at most one final configuration `(H,t:A)`.

---

### 3. Determinism & Termination

Because each rule either *adds* or *consumes* exactly one event, the search[6D[K
search space
is linear in the size of the expression:

1. **Synthesis** only explores a bounded number of pattern matches (e.g., v[1D[K
variable,
   abstraction, application).  
2. **Checking** consumes histories that are replay‑equivalent to those prev[4D[K
previously
   generated; if a mismatch occurs early, the algorithm aborts immediately.[12D[K
immediately.

Thus we have:

```hs
theorem [Determinism]:
  For any term t and context Γ, synthesize(t,Γ) terminates in O(|t|).
```

---

### 4. Extending Historical Normalization

Normalization is extended to produce **both** the observable normal form `v[2D[K
`v` *and*
the complete history `H'`. This satisfies:

```hs
theorem [Normalization]:
  (H,t) ⟶* (H',u)
    ⇒   u = v (observable value), and
    ⇒   H' contains all events required to construct t.
```

Now the evaluator does **not** discard provenance; it records every beta‑ev[7D[K
beta‑event,
let-binding, or application as part of `H`. This eliminates hidden mutable [K
state
and makes proofs replayable.

---

### 5. Integration with Event Algebra

Historical reduction respects the event algebra’s ordering:

```hs
theorem [Event Order]:
  If (H,t) →* (H₁,u) and (H₁,u) →* (H₂,v), then H ⊂ H₁ ⊂ H₂,
  where “⊂” denotes a well‑formed subset of events.
```

Therefore, the type checker can verify that every intermediate configuratio[12D[K
configuration
represents an **admissible extension**:

1. Events are introduced via `Bind`, `Meld` (compatible), or `Collapse`
   (replay‑equivalent).  
2. The kernel rejects any attempt to introduce a cycle by disallowing event[5D[K
events
   that would reverse the history ordering.

---

### 6. Practical Benefits

| Benefit | How It Is Achieved |
|---------|-------------------|
| **Replayability** | Every check can replay `H` to verify consistency with[4D[K
with the current observable term. |
| **Incremental Compilation** | Only changes in provenance need re‑evaluati[11D[K
re‑evaluation; unchanged histories are cached. |
| **Distributed Verification** | Provenance is a first-class object that ca[2D[K
can be exchanged between kernel instances without sharing raw terms. |
| **Persistent Debugging** | The full history of every term can be inspecte[8D[K
inspected at runtime, providing step‑by‑step traces to users. |

---

### 7. Summary

The bidirectional historical type checker provides:

1. **Two clear judgments** (synthesize vs. check) that each produce a *comp[5D[K
*completed*
   history `H`.
2. **Deterministic search** guaranteed by the event algebra’s admissibility[13D[K
admissibility rules.
3. **Normalization with provenance**, so every reduction is both observable[10D[K
observable and
   reproducible.
4. A **kernel‑invariant** guarantee: type checking never relies on untyped
   side‑effects; all state lives inside immutable histories.

With this design, the kernel remains entirely internal to the trusted base,[5D[K
base,
and any extension (e.g., modules or external libraries) can be verifie[7D[K
verified by replaying
their historic events against existing provenance—exactly what modern proof[5D[K
proof assistants already do for proofs and certificates.  

The next chapter will formalize how these historical judgments are compiled[8D[K
compiled into a concrete execution engine that operates on the underlying e[1D[K
event algebra, ensuring that computation itself is an irreversible growth o[1D[K
of admissible history.
