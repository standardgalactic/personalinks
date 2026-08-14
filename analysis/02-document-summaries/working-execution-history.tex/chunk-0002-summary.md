**Interpretation of the Document**

The document presents an event‑historical perspective on computation. Its c[1D[K
core thesis is that computation should not be viewed merely as a transforma[10D[K
transformation between static states but rather as the irreversible constru[7D[K
construction and extension of histories through events. Here’s how to under[5D[K
understand its major ideas:

---

### 1. Event Histories vs. Static States

- **Traditional view**: Programs are seen as mapping from one well‑defined [K
state to another.
- **Event‑historical view**: Execution is a monotonic accumulation of event[5D[K
event sequences (history). The system's current configuration arises from t[1D[K
the cumulative effect of these past events, not directly from any particula[9D[K
particular snapshot.

---

### 2. Fundamental Operations

1. **Extension** – New events are appended to an existing history.
2. **Merge/Join** – When compatible branches diverge and later converge, th[2D[K
they are reconciled using join‑like operations that preserve causal orderin[7D[K
ordering (similar to set‑intersection in a partial order).
3. **Abstraction** – Reduction mappings compress histories into summaries o[1D[K
or derived representations (e.g., states, logs).

These operations together form an *operational kernel* for computation.

---

### 3. Common Structure Across Domains

The kernel is not confined to any single domain:

- **Distributed Systems**: Event‑ordered logs and CRDTs (Conflict-Free Repl[4D[K
Replicated Data Types) embody this structure.
- **Version Control**: Git’s commit graph reflects extensions and merges of[2D[K
of branches.
- **Constraint Solving**: Languages that express constraints (e.g., Prolog,[7D[K
Prolog, Oz) operate by propagating constraint updates through a lattice of [K
admissible configurations.
- **Physical Systems**: Lattice models like the Ising model evolve via loca[4D[K
local updates that reshape possible futures, analogous to event propagation[11D[K
propagation.

---

### 4. Mathematical Foundation

The shared structure can be described mathematically:

- **Partially Ordered Space** – Event histories form a poset under prefix e[1D[K
extension (a *semilattice*‑like ordering).
- **Join Operations** – Merges of compatible branches are join construction[12D[K
constructions preserving causal relations.
- **Reduction Mapping** – Abstractions discard some historical detail while[5D[K
while preserving essential distinctions relevant to the observer.

---

### 5. Implications

1. **Emergent Properties**: System behavior emerges from cumulative, locall[6D[K
locally constrained transitions rather than pre‑defined static states.
2. **State as Derived**: What we call a “state” is actually a compressed vi[2D[K
view of an underlying history; stability results from the historical accumu[6D[K
accumulation that produces observable effects.
3. **Unified Perspective**: Diverse computational and physical systems shar[4D[K
share this structural principle, suggesting deeper connections between algo[4D[K
algorithmic theory and physics.

---

### 6. Conclusion

By redefining computation around event histories:

- We gain a richer understanding of how complex behaviors arise (e.g., stab[4D[K
stability in distributed systems).
- Stateful abstractions become meaningful summaries rather than fundamental[11D[K
fundamental objects.
- This view bridges gaps between traditional programming paradigms, concurr[7D[K
concurrency theory, and physical models governed by local interactions.

Thus, the document advocates for an *event‑historical kernel* as a unifying[8D[K
unifying framework that clarifies computation’s true nature across many dis[3D[K
disciplines.
