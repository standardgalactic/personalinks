**Operational Semantics of Spherepop**

Below is a step‑by‑step formal description of the operational semantics tha[3D[K
that governs the Spherepop Calculus, following the historical interpretatio[13D[K
interpretation introduced in the previous chapters.

---

### 1. Semantic State

The machine’s runtime configuration is written as  

\[
(H,\mathcal{S}),
\]

where  

* **\(H\)** – the *current computational history*, a monotonically growing [K
record of all admissible repairs that have been performed so far.  
* **\(\mathcal{S}\)** – the set of *unresolved Spheres* (computational scop[4D[K
scopes) waiting to become ready.

No mutable global state is required; every change in computation is capture[7D[K
captured by extending \(H\) and \(\mathcal{S}\).

---

### 2. Cycle of Evaluation

At any instant the runtime repeatedly performs the same evaluation cycle:

1. **Locate** – Find a Sphere that satisfies the *Ready* condition (see §3)[3D[K
§3).  
2. **Verify** – Ensure all its dependencies are already resolved.  
3. **Pop Reduction** – Apply Pop to consume the ready Sphere and replace it[2D[K
it by its value throughout the remaining history (\(H\)).  
4. **Replay** – If a region has consumed an output from another, extend the[3D[K
the shared history with Replay (see §5).  
5. **Repeat** – Go back to step 1.

Because this loop is repeated until \(\mathcal{S}\) becomes empty, ordinary[8D[K
ordinary sequential evaluation appears as a special case of historical evol[4D[K
evolution.

---

### 3. Ready Spheres

A Sphere \(S=(B,I)\) (where \(B\) is its boundary and \(I\) the interior co[2D[K
computation) becomes *Ready* only when **every** dependency inside it has a[1D[K
already completed:

\[
\forall d\in\operatorname{Deps}(S),\qquad \operatorname{Resolved}(d).
\]

Thus, instead of searching for syntactic redexes, the runtime looks for com[3D[K
computational regions whose local histories have become complete.

---

### 4. Opening Spheres

When a new computational scope is encountered (by parser or compiler), the [K
runtime introduces it into the history:

\[
(H,\mathcal{S})
\;\longrightarrow\;
(H\;|\;\operatorname{Open}(S),\;\mathcal{S}\cup\{S\}).
\]

Opening does **not** immediately evaluate; it merely records that a bounded[7D[K
bounded environment exists for future evolution.

---

### 5. Pop Reduction

If \(S=(B,I)\) is Ready and its interior satisfies  

\[
I\Longrightarrow v,
\]

then the Pop rule replaces the Sphere by its value:

\[
(H,\mathcal{S}\cup\{S\})
\;\longrightarrow\;
(H\;|\;\operatorname{Pop}(S),\;( \mathcal{S}-\{S\})[v]).
\]

Here \([v]\) denotes *replacement of the Sphere by its resulting value thro[4D[K
throughout the remaining unresolved computational regions*. Crucially, this[4D[K
this replacement carries historical provenance, not just a plain substituti[10D[K
substitution.

---

### 6. Replay

When one computational region consumes the output of another, replay extend[6D[K
extends the shared history without mutating any part of it:

\[
(H,\mathcal{S})
\;\longrightarrow\;
(H\;|\;\operatorname{Replay},\;\mathcal{S}').
\]

Thus replay preserves causality and coherence: every subsequent continuatio[11D[K
continuation retains access to the computation that produced the value.

---

### 7. Refusal

If a proposed continuation \(e\) violates an admissibility relation, refusa[6D[K
refusal records this failure:

\[
\neg\operatorname{Adm}(H,e)
\;\Longrightarrow\;
(H,\mathcal{S})
\;\longrightarrow\;
(H\;|\;\operatorname{Refuse}(r),\;\mathcal{S}).
\]

The unresolved set \(\mathcal{S}\) remains unchanged, preserving historical[10D[K
historical coherence without requiring rollback or exception propagation as[2D[K
as primitive mechanisms.

---

### 8. Merge Scheduling

Multiple independent Ready Spheres can be evaluated simultaneously:

\[
(H,\mathcal{S})
\;\longrightarrow\;
(H\;|\;\operatorname{Merge}(S_1,\dots,S_n),\;\mathcal{S}''),
\]

where the scheduler respects dependency constraints and causality. Processo[8D[K
Processor scheduling is thus decoupled from semantic correctness.

---

### 9. Choice Reduction

Choice introduces non‑determinism while preserving a single historical grap[4D[K
graph:

* **Probabilistic Sampling** –  

  \[
  \operatorname{Choice}(p,t,u)
  \;\longrightarrow\;
  t \quad\text{(with probability }p),
  \]
  *or*  
  \[
  \operatorname{Choice}(p,t,u)
  \;\longrightarrow\;
  u \quad\text{(with probability }1-p).
  \]

* **Deferred Commitment** –  

  \[
  \operatorname{Choice}(p,t,u)
  \;\longrightarrow\;
  d:\operatorname{Dist}(A),
  \]

where \(d\) records the distribution of possible continuations without perf[4D[K
performing an immediate collapse. Both policies share identical historical [K
semantics but differ only in when commitment occurs.

---

### Operational Invariant

At every stage of execution, the following invariant holds:

1. **Uniqueness** – Each admitted event belongs to exactly one history.
2. **Monotonicity** – Every Pop removes one admissible computational bounda[6D[K
boundary; each Replay extends historical continuity.
3. **Historical Coherence** – Refusal preserves coherence without mutating [K
\(\mathcal{S}\).
4. **Associative Commutativity** – Merge over independent histories is asso[4D[K
associative and commutative, allowing flexible processor scheduling while p[1D[K
preserving causality.

---

### Summary

The operational semantics of Spherepop treats the *computational history* i[1D[K
itself as the semantic state rather than a static term. Evaluation becomes [K
the progressive construction of an irreversible historical object, where re[2D[K
reduction (Pop), extension (Replay), rejection (Refusal), and non‑determini[13D[K
non‑deterministic branching (Choice) all operate on this evolving record. T[1D[K
This shift from symbolic equality to repair‑based identity unifies equality[8D[K
equality with replay and refusal, providing a unified framework for reasoni[7D[K
reasoning about computational histories in distributed systems, incremental[11D[K
incremental compilation, proof assistants, and database replication.

---

**End of Operational Semantics Section**.

