**The operational semantics of the Spherepop Calculus**

Below is an informal yet complete description of how evaluation in the Sphe[4D[K
Spherepop language is captured by its runtime model.  The key idea is that [K
*history* – not just syntactic reduction – becomes the fundamental semantic[8D[K
semantic state, so all ordinary notions (reduction, substitution, type‑chec[9D[K
type‑checking, etc.) are re‑expressed as operations on computational histor[6D[K
histories.

---

### 1. Semantic State

At any instant the machine holds a **state**

\[
(H,\mathcal S),
\]

* \(H\) = the current *computational history*: a chronological record of al[2D[K
all events that have been recorded (open spheres, pops, replays, refusals, [K
merges, etc.).  
* \(\mathcal S\) = the set of *unresolved computational regions* (Spheres).[10D[K
(Spheres).  Each element is a bounded context whose computation has not yet[3D[K
yet terminated.

No mutable global state is primitive; every change to the system is recorde[7D[K
recorded by extending \(H\) and/or updating \(\mathcal S\).

---

### 2. Evaluation Cycle

The runtime repeatedly performs the same cyclic process:

1. **Locate** – search \(\mathcal S\) for a *Ready* sphere (see §3).  
2. **Verify** – confirm that every dependency of the selected sphere is alr[3D[K
already resolved.  
3. **Pop Reduction** – if verification succeeds, replace the whole ready sp[2D[K
sphere by its result and update \(H\).  
4. **Replay** – whenever an event consumes a value produced elsewhere (e.g.[5D[K
(e.g., function application), extend the history with replay information.  [K

5. **Repeat** – go back to step 1.

Because each iteration only *extends* the existing historical record, evalu[5D[K
evaluation is inherently non‑destructive and can be reversed at any point.

---

### 3. Ready Spheres

A sphere \(S = (B,I)\) becomes ready when all of its internal dependencies [K
are already resolved:

\[
\forall d \in \operatorname{Deps}(S),\qquad
\text{Resolved}(d).
\]

*The notion of “dependency” is purely historical*: a dependency is any sub‑[4D[K
sub‑computation that must finish before \(S\) may be closed.*

---

### 4. Opening Spheres

When the parser/compiler encounters a new scope (e.g., the start of a funct[5D[K
function body), it introduces a fresh sphere:

\[
(H,\mathcal S) \;\longrightarrow\; 
(H\;\|\;\operatorname{Open}(S),\;\mathcal S\cup\{S\}).
\]

Opening does **not** perform any computation itself; it merely records that[4D[K
that the bounded region exists and will eventually become admissible.

---

### 5. Pop Reduction

If a ready sphere \(S\) contains an interior reduction:

\[
I \Longrightarrow v,
\]

then we replace its entry in \(\mathcal S\) with the resulting value, **car[5D[K
**carrying provenance**:

\[
(H,\mathcal S) \;\longrightarrow\;
(H\;\|\;\operatorname{Pop}(S),\;(\mathcal S-\{S\})[v]).
\]

Here \([v]\) denotes a *historical substitution*: the sphere is removed, an[2D[K
and its value \(v\) propagates into any other unresolved region that previo[6D[K
previously depended on it.

---

### 6. Replay

Whenever one computation consumes another’s output (e.g., applying a functi[6D[K
function to an argument), we extend history with replay information:

\[
(H,\mathcal S) \;\longrightarrow\;
(H\;\|\;\operatorname{Replay},\;\mathcal S').
\]

Replay is monotonic – it never deletes work, only records new dependencies.[13D[K
dependencies.

---

### 7. Refusal

If a proposed continuation fails an admissibility check:

\[
\neg\operatorname{Adm}(H,e),
\]

the runtime marks the failure and leaves \(\mathcal S\) unchanged:

\[
(H,\mathcal S) \;\longrightarrow\;
(H\;\|\;\operatorname{Refuse}(r),\;\mathcal S).
\]

Thus inadmissible continuations are *recorded* but never cause rollback.

---

### 8. Merge Scheduling

If several ready spheres \(S_1,\dots,S_n\) are mutually independent, they m[1D[K
may be evaluated concurrently:

\[
(H,\mathcal S) \;\longrightarrow\;
(H\;\|\;\operatorname{Merge}(S_1,\dots,S_n),\;\mathcal S').
\]

Because merge is associative and commutative over independent histories, th[2D[K
the scheduler has considerable freedom (e.g., parallel execution).  The cru[3D[K
crucial invariant remains: causality among dependencies is preserved.

---

### 9. Choice Reduction

Choice introduces nondeterministic branches:

\[
\operatorname{Choice}(p,t,u)
\]

reduces to \(t\) with probability \(p\) and to \(u\) with probability \(1-p[5D[K
\(1-p\) **or** it expands to a distribution object that propagates without [K
immediate collapse.

Both policies share the same historical semantics: they only affect the *fu[3D[K
*future* history (e.g., branching continuations) but never alter past event[5D[K
events already recorded in \(H\).

---

### 10. The Operational Invariant

At every step of evaluation, the following invariant holds:

| Property | Description |
|---|---|
| **Uniqueness** | Every admitted event belongs to exactly one history. |
| **Monotonicity** | History \(H\) grows monotonically (no back‑tracking). [K
|
| **Termination** | Each Pop reduces a single admissible boundary. |
| **Continuity** | Each Replay extends historical continuity without erasin[6D[K
erasing earlier work. |
| **Coherence** | Each Refusal preserves coherence; no inadmissible event i[1D[K
is merged into history. |
| **Independence** | Each Merge respects causal independence among its argu[4D[K
arguments. |
| **Nondeterminism** | Choice merely delays or resolves commitment, not alt[3D[K
altering the underlying graph. |

Traditional operational semantics often lists isolated reduction rules (e.g[4D[K
(e.g., β‑reduction for λ‑calculus).  In Spherepop we capture *all* such rul[3D[K
rules as operations on this single evolving history.

---

### Why This Matters

By replacing static equality with a notion of **repair**—the completion of [K
computational histories—we gain:

1. **Clearer meaning for identity**: two values are equal when their produc[6D[K
producing histories have been reconciled, not merely because they syntactic[9D[K
syntactically coincide.
2. **Unified treatment of concurrency and incrementalism**: replaying histo[5D[K
history naturally expresses version‑control merging, incremental compilatio[10D[K
compilation, database replication, etc., without extra mechanisms.
3. **Natural handling of failure**: refusals record why a branch cannot con[3D[K
continue, preserving the full context for later recovery or analysis.

In short, Spherepop’s operational semantics is a *historical* calculus: eve[3D[K
every reduction step records how we arrived at a state, allowing us to reas[4D[K
reason about entire computational trajectories—what made them possible and [K
when they may safely be collapsed.

