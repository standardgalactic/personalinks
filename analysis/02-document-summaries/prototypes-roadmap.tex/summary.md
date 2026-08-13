**Central Thesis**

Spherepop calculus defines a minimal, strictly deterministic operational se[2D[K
semantics for the operating‑system kernel. Its core invariants—deterministi[23D[K
invariants—deterministic replay of events, total causal ordering across all[3D[K
all processes, ABI stability for event structures, and a strict separation [K
between authoritative semantic changes (events) and derived views—are prese[5D[K
preserved by designating utilities as “non‑authoritative observers” that op[2D[K
operate solely on already‑committed event logs. Consequently, the roadmap e[1D[K
envisions utilities not as general purpose programs but as structured consu[5D[K
consumers/produces of events and replayed state, guaranteeing that any side[4D[K
side effects are explicit proposals rather than hidden state changes.

**Definitions & Primitive Concepts**

1. **Event Types (Spherepop Calculus primitives)**  
   - **POP**: introduces a new semantic object handle.  
   - **MERGE**: induces equivalence between existing objects.  
   - **LINK**: creates a typed relation between objects.  
   - **UNLINK**: removes an established typed relation.  
   - **COLLAPSE**: performs bulk equivalence over a defined region of the l[1D[K
log.  
   - **SETMETA**: attaches non‑semantic metadata (e.g., version tags) to ev[2D[K
events.

2. **Utility Classes**  
   - **Proposal Generators**: emit candidate event sequences without commit[6D[K
committing them.  
   - **View Generators**: consume replayed state and produce observational [K
representations such as JSON graphs, diffs, or summaries.  
   - **Overlay Managers**: manipulate speculative branches (creating, rebas[5D[K
rebasing, or discarding overlays) entirely outside the authoritative log.

3. **Kernel Invariants**  
   - **Deterministic Replay**: identical inputs to the same event prefix mu[2D[K
must yield identical proposals/views.  
   - **Total Causal Order**: all events are ordered causally; no hidden sta[3D[K
state influences kernel decisions.  
   - **ABI Stability**: utilities interact via stable, documented event lay[3D[K
layouts (no undocumented padding or reinterpretation).  
   - **View Non‑Interference**: derived views cannot feed back into kernel [K
decision logic.

**Mathematical Claims & Formal Structures**

- The utility model is built on a deterministic rewrite system where each p[1D[K
primitive operation corresponds to a unique rewrite rule applied to the cur[3D[K
current state of the event log.  
- Replay determinism follows from the Church–Turing interpretation: any seq[3D[K
sequence of POP/MERGE/LINK events can be reconstructed from an initial snap[4D[K
snapshot by sequentially applying the corresponding rules.

**Important Equations / Formal Structures**

1. **Replay Determinism Equation**:  
   \[
   \text{Result}(P, S) = f(P', S') \quad\text{where } P' \subseteq P \text{[6D[K
\text{ and } S' \text{ is a prefix of the original log } S.
   \]  
   This formalizes that any utility invocation (event prefix \(P\) plus sta[3D[K
state snapshot \(S\)) must produce identical results regardless of executio[8D[K
execution timing.

2. **View Separation Constraint**:  
   - Views \(V\) derived from replayed state \(R\) satisfy:  
     \[
     V \subseteq \text{Replay}(R) \quad\text{and}\quad V \notin \text{Cause[11D[K
\text{CausedBy}(R).
     \]  
   This ensures that no view influences future kernel decisions.

**Mechanisms & Processes**

1. **Proposal Generation** – Batch POP/MERGE/LINK events are emitted as a p[1D[K
proposal stream, then optionally submitted via the arbiter for commitment. [K
 
2. **Overlay Management** – Speculative overlays are created by linking non[3D[K
non‑authoritative event sequences; they can be re‑based or discarded withou[6D[K
without affecting the authoritative log.  
3. **View Production** – Consuming replayed state through structured parser[6D[K
parsers (e.g., `spdiff`, `spsnap`) yields diff representations, JSON serial[6D[K
serializations, or textual summaries that are observable but non‑causal.

**Philosophical Commitments**

- **Determinism & Reversibility**: Actions must be reversible; any change i[1D[K
is a proposal that can be undone by discarding the overlay.  
- **Separation of Concerns**: Semantic changes (authoritative) and derived [K
representations (views) remain conceptually distinct, preserving clarity ab[2D[K
about what influences kernel behavior versus what merely observes it.

**Connections to Computation**

- Spherepop utilities embody a functional programming paradigm over event s[1D[K
streams: pure functions that map an input prefix \((P, S)\) to an output vi[2D[K
view \(V\).  
- They illustrate how high‑level reasoning (e.g., “batch merge all deprecat[8D[K
deprecated objects”) can be expressed as sequences of primitive rewrite ope[3D[K
operations without hidden mutable state.

**Connections to Other Likely Parts of Spherepop**

1. **Overlay Protocol**: Utilities that manipulate speculative branches wil[3D[K
will later interact with the overlay management layer, enabling multi‑branc[11D[K
multi‑branch debugging or experimental deployments.  
2. **Query Language (spgrep)**: Phase III introduces a view‑centric query s[1D[K
system that builds on the same event‑order guarantees, allowing users to ex[2D[K
express path queries over replayed state as pure functions.

**Unresolved Questions**

- How will utilities evolve to support higher‑level abstractions (e.g., inc[3D[K
incremental diffing) while preserving invariants?  
- What is the optimal policy for handling edge cases where multiple valid m[1D[K
merge paths exist (non‑confluence)?  

**Contradictions, Ambiguities, or Weaknesses**

- The roadmap’s strict separation can become a weakness if utilities inadve[6D[K
inadvertently leak view information back into kernel logic. Explicit docume[6D[K
documentation and static analysis tools are required to enforce this constr[6D[K
constraint.  
- Phase I only provides a minimal utility set; later phases may introduce m[1D[K
more complex composition pipelines that could otherwise blur the line betwe[5D[K
between proposals and views.

**Concepts Likely to Survive Compression**

- **Replay‑Only Paradigm**: All utilities should be defined as functions ma[2D[K
mapping from replayed prefixes, ensuring no hidden state or timing dependen[8D[K
dependencies.  
- **Overlay Discipline**: Non‑authoritative overlays must remain explicit; [K
any auto‑commit behavior will be rejected in later phases.  
- **View Generators as Observers**: The role of derived representations (di[3D[K
(diffs, JSON) is to highlight changes without influencing kernel decisions—[10D[K
decisions—this invariant should persist across the entire utility ecosystem[9D[K
ecosystem.

In summary, the roadmap envisions Spherepop utilities as disciplined, repla[5D[K
replay‑only tools that honor deterministic semantics and strict separation [K
between state change proposals and observational views. Their success hinge[5D[K
hinges on maintaining these invariants rather than on increasing convenienc[10D[K
convenience or functionality beyond what can be expressed deterministically[17D[K
deterministically through primitive event operations.

