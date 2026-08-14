**State, Continuations and Mutation in Spherepop**

In a pure functional setting every operation produces *no* side‑effects; th[2D[K
they are only transformations on values.  In practice we need to talk about[5D[K
about:

| Concept | Traditional Presentation | Spherepop (Merge → Collapse) View |
|---------|--------------------------|-----------------------------------|
| **State** | A monad `State S A ≅ (S → (A × S))` – a stateful computation [K
reads the current state and returns both a result and an updated state. | T[1D[K
The *state* is simply a region of effect atoms, i.e. an element of $\Sigma$[8D[K
$\Sigma$ (the space of admissible regions).  Running a computation updates [K
the region by **collapsing** the accumulated effects: \[ S_{t+1}= \operator[9D[K
\operatorname{collapse}(S_t\oplus\Delta_t) .\] The history is therefore a l[1D[K
list of *regions* rather than a mutable cell. |
| **Continuation‑Passing Style (CPS)** | A function has type `A → (A → R) →[1D[K
→ R`; the continuation tells what will happen next in the overall computati[9D[K
computation chain. | A CPS argument packages future merge–collapse steps as[2D[K
as a promise of *what happens after*.  The continuation is itself a transfo[7D[K
transformer that may later decide when to collapse intermediate results, ef[2D[K
effectively controlling the staging of collapse. |
| **Mutation** | In imperative languages variables are updated “in‑place”; [K
the old value disappears from the state representation. | Mutation correspo[8D[K
corresponds precisely to a *collapsed* region: \[ S_{t+1}= \operatorname{co[16D[K
\operatorname{collapse}(S_t\oplus\Delta_t) \] where the prior region is ove[3D[K
overwritten and its history is discarded.  Thus mutation is “collapse witho[5D[K
without history”. |

---

### How These Ideas Fit Together

1. **State as a Region**  
   - Think of each possible state value $s$ as an element of $\Sigma$.  
   - A computation that changes this value does so by *merging* the current[7D[K
current region with a new effect atom $\Delta_t$, then *collapsing* to prod[4D[K
produce a fresh region.  
   - No part of the old state is retained, but its whole history can still [K
be recovered from the sequence of merged regions (the event log).  

2. **Continuations as Staged Collapse**  
   - In CPS we pass not just a result but also an entire continuation – ano[3D[K
another function waiting to receive data later.  
   - This lets us decide *when* the next merge–collapse will occur: early ([1D[K
(eager) or deferred until after further computations.  
   - The continuation thus controls the **timing** of collapse, turning imp[3D[K
imperative “next step” into a compositional rule.

3. **Mutation as Untracked Collapse**  
   - Mutation discards the ability to replay earlier states because it coll[4D[K
collapses them without recording an event log entry.  
   - In Spherepop terms this is a *collapse* that skips the region‑accumula[15D[K
region‑accumulation stage, breaking referential transparency for that part [K
of the program.  
   - The consequence is precisely what we observe in mutation: loss of the [K
ability to reconstruct past states and a corresponding increase in debuggin[8D[K
debugging complexity.

---

### Takeaway

All three constructs—**state**, **continuations**, and **mutation**—are man[3D[K
manifestations of the same underlying principle:

> *Merge builds structure; collapse interprets it.*  

In Spherepop we make this explicit: state updates are just region‑level mer[3D[K
merges, CPS continuations are staged merge‑collapse promises, and mutation [K
is a special case where the merge step discards history altogether. This pe[2D[K
perspective aligns computation with an append‑only event log and preserves [K
compositional reasoning across different control forms.

