**Thesis**

*spmerge* is a lightweight, user‑facing utility that operates solely as an [K
*event‑proposal layer* atop the kernel’s replayed state. Its purpose is to [K
**suggest** semantic equivalence between existing objects by emitting expli[5D[K
explicit `MERGE` or `COLLAPSE` events without ever altering authoritative d[1D[K
data structures. The design enforces strict determinism (given a fixed even[4D[K
event‑log prefix and invocation, spmerge must produce an identical sequence[8D[K
sequence of proposals) and explicitly avoids heuristic inference, mutation [K
of kernel state, or reliance on external data sources.

---

**Primitives & Definitions**

1. **spmerge** – A command that takes as input an explicit list of object i[1D[K
identifiers already present in the kernel’s replayed history. It never writ[4D[K
writes to the authoritative store; its only action is to *propose* equivale[8D[K
equivalence via events.
2. **Merge event (`MERGE(o_a, o_b)`)** – Proposes a pairwise semantic equiv[5D[K
equivalence between two specific objects identified by `o_a` and `o_b`. The[3D[K
The selection of which pair to merge is left entirely to the kernel’s polic[5D[K
policy, ensuring no inference beyond explicit user request.
3. **Batch merge** – For a set `{o₁,…,oₙ}` of objects, spmerge automaticall[12D[K
automatically generates a sequence of `MERGE` events that together form a *[1D[K
*spanning tree* over the supplied set (deterministic ordering but semantica[9D[K
semantically irrelevant because all topologically equivalent trees are conj[4D[K
conjoined).
4. **Region collapse (`COLLAPSE(S, o_r)`)** – Proposes equivalence for an e[1D[K
entire region identified by a finite set `S` of objects; exactly one repres[6D[K
representative `o_r ∈ S` is chosen as the canonical node representing the w[1D[K
whole region.
5. **Replayed kernel state** – The operational context for spmerge: it only[4D[K
only uses identifiers that already exist in the kernel’s history replay, wi[2D[K
with no external data dependencies.

---

**Formalism**

- *Graph‑theoretic spanning tree*: The batch‑merge process explicitly build[5D[K
builds a spanning tree over the supplied object set `{o₁,…,oₙ}`. This is an[2D[K
an instantiation of graph theory where each node corresponds to an existing[8D[K
existing object and edges encode merge proposals.
- *Quotient (setoid) construction*: Region collapse can be viewed as select[6D[K
selecting a vertex label for the equivalence class; `S` represents all obje[4D[K
objects under consideration, and `o_r` designates the representative elemen[6D[K
element.

---

**Mechanisms & Processes**

1. **Input Handling**
   - Receives an explicit list of object identifiers that must already exis[4D[K
exist in replayed kernel state.
2. **Event Proposal Generation**
   - *Pairwise merge*: For each user‑requested pair `(o_a, o_b)`, emits a s[1D[K
single `MERGE(o_a, o_b)` event.
   - *Batch merge*: Automatically orders merges to produce a spanning tree;[5D[K
tree; ordering is deterministic but semantically irrelevant due to confluen[8D[K
confluence (any equivalent spanning tree yields the same overall equivalenc[10D[K
equivalence class).
3. **Region Collapse**
   - For a designated region `S` of objects, emits one `COLLAPSE(S, o_r)` e[1D[K
event where `o_r ∈ S` serves as the canonical representative.
4. **Determinism Guarantee**
   - Given a fixed prefix of the event log and an invocation, spmerge must [K
reproduce exactly the same sequence of proposal events (bit‑for‑bit).
5. **Preview Workflow**
   - Runs in non‑committing mode to construct speculative overlays that dis[3D[K
display “before/after” equivalence classes without persisting changes.

---

**Major Arguments**

- **Non‑inference & Non‑mutation**: By refusing to perform heuristic infere[6D[K
inference or mutate authoritative state, spmerge preserves semantic fidelit[7D[K
fidelity and avoids unintended side effects.
- **Determinism as a Design Principle**: Deterministic behavior guarantees [K
reproducibility across invocations, which is crucial for auditability in di[2D[K
distributed systems where many independent merge proposals may be generated[9D[K
generated concurrently.
- **Explicit Non‑Goals Clarify Scope**: The document’s running abstract emp[3D[K
emphasizes that spmerge does *not*:
  - Perform inference beyond explicit user requests,
  - Mutate kernel state (i.e., write to persistent data structures),
  - Engage in heuristic auto‑merging or redundant proposals.

---

**Dependencies Between Concepts**

- **Batch Merge ↔ Spanning Tree**: The requirement for a spanning tree dire[4D[K
directly ties the batch merge mechanism to graph theory; it ensures that an[2D[K
any two equivalent trees (due to confluence) yield identical semantic impac[5D[K
impact.
- **Region Collapse ↔ Representative Selection**: Dependency on kernel poli[4D[K
policy for selecting `o_r` means that collapse decisions are ultimately del[3D[K
delegated to the underlying system, preserving consistency across region bo[2D[K
boundaries.

---

**Implications**

1. **Scalability & Auditability**: Because spmerge only proposes events and[3D[K
and relies on existing identifiers, it scales without additional metadata o[1D[K
overhead; each proposal can be traced back to a replayed kernel state, faci[4D[K
facilitating auditing.
2. **Integration with Existing Systems**: The deterministic nature allows s[1D[K
seamless integration into pipelines that rely on reproducible merges (e.g.,[6D[K
(e.g., version control systems), while the explicit non‑mutation policy pre[3D[K
prevents accidental data corruption.
3. **Limitations in Heuristic Guidance**: Since spmerge cannot infer semant[6D[K
semantic equivalence beyond explicit requests, users must provide sufficien[9D[K
sufficient guidance to avoid redundant or erroneous proposals.

---

**Unresolved Problems & Internal Tensions**

- **Representative Selection (Pairwise Merge)**: The document does not spec[4D[K
specify how the kernel chooses which pair `(o_a, o_b)` to merge when multip[6D[K
multiple equivalences are possible. This leaves an implicit assumption abou[4D[K
about kernel policy that may vary across implementations.
- **Redundant Proposal Detection**: There is no explicit definition or dete[4D[K
detection criteria for “redundant” proposals (e.g., merging already equival[7D[K
equivalent objects). The abstract mentions this as an error condition but d[1D[K
does not spell out how to identify it, leaving ambiguity in usage.
- **Semantic Irrelevance of Ordering (Batch Merge)**: While deterministic o[1D[K
ordering guarantees reproducibility, the claim that ordering is semanticall[11D[K
semantically irrelevant due to confluence may be misinterpreted. Users migh[4D[K
might expect a particular topological order to affect outcome, which could [K
lead to confusion if not documented clearly.

---

**Citations**

- “spmerge … proposes semantic equivalence between objects in Spherepop OS [K
by generating MERGE or COLLAPSE events.” → quoted as *“proposes semantic eq[2D[K
equivalence”*.
- “It does not perform inference, mutate kernel state, or engage in heurist[7D[K
heuristic auto‑merging.” → echoed by the quote *“does not mutate authoritat[10D[K
authoritative state.”*.
- “Determinism guarantee: given a fixed event log prefix and invocation, it[2D[K
it must generate an identical proposal stream bit‑for‑bit.” → supported by [K
the quote *“must reproduce the exact same sequence of proposals (bit‑for‑bi[11D[K
(bit‑for‑bit).”*.
- “Error conditions include non‑existent identifiers, redundant merges, or [K
empty target sets, all resulting in failure fast.” – implied but not explic[6D[K
explicitly quoted; remains an open issue for clarification.

