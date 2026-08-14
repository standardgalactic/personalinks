**Appendix A – Methodological Commitments**

1. **Irreversibility as Primitive**  
   - In Spherepop we take “causal commitment” (an irreversible action) to b[1D[K
be a basic notion rather than something derived from reversibility.  
   - This inversion leads directly to the design choices of *event‑based* h[1D[K
history, replayable computation, and explicit branching.

2. **Conservatism About Meaning**  
   - Meaning is not inferred from behavior or patterns; it enters the syste[5D[K
system only through *explicit events*.  
   - All inference remains in the form of views (non‑authoritative represen[8D[K
representations) that can be replaced without altering the authoritative se[2D[K
semantic record.

3. **Constructive Stance Toward Abstraction**  
   - Any abstraction—whether a data type, control structure, or interface c[1D[K
convention—is treated as an act that *ignores* certain distinctions, and th[2D[K
those ignored distinctions must be recorded in trace form.  
   - This ensures that every “shortcut” has a concrete counterpart (e.g., h[1D[K
hidden state is always accompanied by a commit event).

These commitments guide all design decisions: replay replaces mutable state[5D[K
state as the primary execution model; identity is grounded in trace rather [K
than appearance; and any speculative or alternative path must be explicitly[10D[K
explicitly marked to prevent silent merging.

---

**Appendix B – Relation to Formal Calculi**

Spherepop can be formalized as an extension of typed lambda calculus:

| Primitive | Interpretation |
|-----------|----------------|
| **Sphere (Σ)** | Represents the act of introducing a new object, relation[8D[K
relation, or equivalence—i.e., an *event* that permanently changes the spac[4D[K
space of possibilities. |
| **Pop (π)**    | Models the computation over a prefix of events, yielding[8D[K
yielding derived structures such as views or speculative branches. |
| **Trace (Γ)**  | Guarantees that every state reachable from a given event[5D[K
event history can be reconstructed via replay, preserving causality and non[3D[K
non‑ergodicity. |

Key formal properties:

- **Reduction ≠ Rewrite**: Reduction is interpreted as the *application* of[2D[K
of an event to its pre‑history, not merely syntactic transformation.
- **Branching = Non‑Authoritative Views**: Speculative branches are kept se[2D[K
separate (marked with a branching token) and must be committed via new Sphe[4D[K
Sphere events to become authoritative.
- **Type Safety & Adequacy**: By constraining abstraction to explicit commi[5D[K
commitments, the calculus retains soundness (no hidden state) while allowin[7D[K
allowing expressive computation.

Related work demonstrates that such a reinterpretation preserves type safet[5D[K
safety, compositional semantics, and adequacy without sacrificing performan[9D[K
performance or expressiveness—showing Spherepop’s formal feasibility beyond[6D[K
beyond its conceptual framework.

---

**Appendix C – Replay, Speculation, and Branching**

1. **Replay as Interpretation**  
   - Given any prefix of events (Γ₀), the system deterministically reconstr[8D[K
reconstructs all objects, relations, and equivalences derived from Γ₀.  
   - This enables late‑joining observers to step through execution history,[8D[K
history, audit decisions, or simulate alternative runs without altering exi[3D[K
existing authority.

2. **Speculation via Branching Histories**  
   - When exploring counterfactual scenarios (e.g., “what if we had chosen [K
a different algorithm?”), a speculative branch is created that carries the [K
label *non‑authoritative*.  
   - The branch may evolve independently but must be committed through a su[2D[K
subsequent Sphere event (e.g., “recorded policy change”) to become part of [K
the authoritative history.

3. **Preservation of Asymmetry**  
   - Branches do not silently merge back into reality; they remain separate[8D[K
separate until an explicit commit occurs, ensuring that only intentional ac[2D[K
actions affect the semantic integrity of the system.

These mechanisms collectively enforce a disciplined separation between *wha[4D[K
*what is observed* and *how it influences future state*, aligning with Sphe[4D[K
Spherepop’s core principle that meaning changes solely at explicit boundari[8D[K
boundaries.

