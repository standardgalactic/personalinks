**Theoretical Reconstruction of *prototypes‑roadmap.tex***

---

### 1. Thesis & Core Intent

The document sets out to formalize an **event‑driven, deterministic kernel [K
calculus** (hereafter *Spherepop Calculus*) that separates **authoritative [K
semantics** (the true state stored in the arbiter/log source) from **derive[8D[K
**derived views** (JSON graphs, diffs, etc.). The thesis is:

> By grounding all manipulations of events in a deterministic replay and to[2D[K
total causal order, we can guarantee that any sequence of operations leads [K
to an invariant logical outcome while preserving strict separation between [K
kernel state and user‑visible representations.

---

### 2. Primitive Definitions & Conventions

| Concept | Formal Definition (excerpted) |
|---------|------------------------------|
| **Spherepop Calculus** | An algebraic framework for *authoritatively mani[4D[K
manipulating* events in the kernel; it defines a set of primitive operation[9D[K
operations that map directly to concrete event types. |
| **Utility Operations** (`POP, MERGE, LINK, UNLINK, COLLAPSE, SETMETA`) | [K
Primitive primitives that correspond to specific event manipulations (e.g.,[6D[K
(e.g., `MERGE` and `COLLAPSE` are intended to preserve confluence). |
| **Proposal Generators** | Utilities that *produce* candidate event sequen[6D[K
sequences without committing them; they act as “draft” producers for kernel[6D[K
kernels. |
| **View Generators** | Observational utilities generating derived represen[8D[K
representations such as JSON graphs or diff snapshots of the kernel state. [K
|
| **Overlay Managers** | Tools for handling speculative branches: creation,[9D[K
creation, rebasing, and discarding overlays to maintain incremental develop[7D[K
development phases (Phase I–IV). |
| **Phase I–IV Stages** | Incremental implementation roadmap: <br>1️⃣ Minima[6D[K
Minimal connectivity<br>2️⃣ Object/relationship tools<br>3️⃣ Canonicalization[16D[K
Canonicalization & refactorization<br>4️⃣ Semantic query & analysis. |

*Source: “The algebraic foundation for authoritatively manipulating events [K
in the kernel.” – chunk‑0001-summary.md*

---

### 3. Formalism & Mathematical Guarantees

- **Deterministic Replay**: The calculus ensures that replaying a sequence [K
of operations yields exactly the same kernel state, regardless of execution[9D[K
execution order (exactly as stated in *chunk‑0001*).  
- **Total Causal Order**: Every event is assigned a total causal precedence[10D[K
precedence relative to all other events; this prevents nondeterminism arisi[5D[K
arising from concurrent updates.  
- **Canonicalization Utilities** (`spmerge`, `spcollapse`): Must preserve *[1D[K
**confluence**, guaranteeing that equivalent sequences of operations collap[6D[K
collapse into the same logical outcome (explicitly noted in *chunk‑0001*). [K
 

---

### 4. Mechanisms & Process Flow

| Step | Tool / Utility | Purpose |
|------|----------------|---------|
| **Connection/Replay** | `sp`, `sp-replay` | Establish contracts for conne[5D[K
connecting to an arbiter/log source; enable deterministic playback of event[5D[K
events. |
| **Normalization & Replay Determinism** | `sppop`, `splink` (examples) | D[1D[K
Demonstrate that generated events are *representatively normalized* and rep[3D[K
reproducible across runs, satisfying the “deterministic replay” requirement[11D[K
requirement. |
| **Preview‑Commit Workflow** | New utilities for merge/collapse (preview m[1D[K
mode) | Allow inspection of speculative overlays without automatic commit, [K
preserving safety during incremental development. |
| **Composition via Streams** | Standard stream interfaces | Ensure composa[7D[K
composable utility pipelines while maintaining strict separation between *a[2D[K
*authoritative proposals* and *non‑authoritative views*. |

*Source: “Tools like `sp` and `sp-replay` establish basic contracts for con[3D[K
connecting to an arbiter/log source.” – chunk‑0001-summary.md*

---

### 5. Mapping to the Running Abstract & Roadmap

- **Deterministic replay**, **total causal order**, **ABI stability**, and [K
**strict separation of semantics/views** are re‑stated as design constraint[10D[K
constraints directly from the abstract (chunk‑0002).  
- The three utility classes map onto functional categories: **batch object [K
creation/canonicalization tools**, **JSON graph producers/diffs/summaries**[27D[K
producers/diffs/summaries**, and **speculative branch manipulation**, respe[5D[K
respectively.  
- Phases I–IV correspond to incremental implementation steps outlined in th[2D[K
the abstract’s roadmap.

*Source: “The three utility classes (proposal generators, view generators, [K
overlay managers) map onto the functional categories introduced in the abst[4D[K
abstract… Phase I–IV correspond to incremental phases of implementation.” –[1D[K
– chunk‑0001-summary.md*

---

### 6. Major Arguments & Design Rationale

1. **Separation of Concerns**: By enforcing a strict separation between ker[3D[K
kernel state (authoritative semantics) and derived views, we avoid hidden m[1D[K
mutable caches that could break deterministic replay.  
2. **Determinism as a Non‑Goal for Ambiguity Resolution**: The document exp[3D[K
explicitly states that automatic conflict resolution is *non‑goal*; instead[7D[K
instead, developers must resolve ambiguities manually through preview commi[5D[K
commits. This mitigates the risk of nondeterministic behavior while preserv[7D[K
preserving conservative design principles.  
3. **Hidden Mutable Caches vs. Time‑Dependent Behavior**: Any mechanism lev[3D[K
leveraging mutable caches would violate invariants required for determinist[11D[K
deterministic replay; thus, these are intentionally excluded from early pha[3D[K
phases (Phase I–II), with plans to address them only after canonicalization[16D[K
canonicalization is stable.

---

### 7. Dependencies Between Concepts

- **Utility Operations** depend on the definition of *event types* (presume[8D[K
(presumed by Spherepop Calculus).  
- **Overlay Managers** rely on Phase‑specific constraints (e.g., Phase III [K
requires prior stabilization of canonicalization utilities).  
- **View Generators** are dependent on successful replay determinism establ[6D[K
established by `sppop`/`splink`.  

---

### 8. Implications for Future Work

1. **Canonicalization Tools**: Must be extended to handle non‑confluent equ[3D[K
equivalence cases (addressing the unresolved question about “Canonicalizati[15D[K
“Canonicalization vs. Ambiguity”).  
2. **Conflict Resolution Mechanisms**: Potential future modules could provi[5D[K
provide heuristic conflict resolution, but this must not compromise the cor[3D[K
core guarantee of deterministic replay.  
3. **Hidden Mutable Caches**: A research direction to explore safe caching [K
strategies that do not interfere with causal invariants (tied to “Hidden Mu[2D[K
Mutable Caches vs. Time‑Dependent Behavior”).  

---

### 9. Unresolved Problems & Internal Tensions

| Issue | Summary |
|-------|---------|
| **Canonicalization vs. Ambiguity** | No guidance on handling non‑confluen[12D[K
non‑confluent merges; potential for divergent outcomes under ambiguous equi[4D[K
equivalence cases. |
| **Implicit Semantics & Automatic Conflict Resolution** | These are explic[6D[K
explicitly *non‑goals*, creating tension with user expectations of automati[8D[K
automatic, safe event resolution. |
| **Hidden Mutable Caches vs. Time‑Dependent Behavior** | The abstract stat[4D[K
states these are incompatible with deterministic replay; however, no mechan[6D[K
mechanism is provided to manage caches without violating invariants. |

*Source: “While merge/collapse utilities are introduced as preserving confl[5D[K
confluence, there is no explicit guidance on handling non‑confluent equival[7D[K
equivalence cases.” – chunk‑0001-summary.md*

---

### 10. Citations & Attribution

All claims reproduced herein are directly supported by the fragment summari[7D[K
summaries:

- **Deterministic replay**, **total causal order**, **strict separation of [K
semantics/views** → *chunk‑0001* (thesis statement).  
- **Canonicalization utilities (`spmerge`, `spcollapse`)** → *chunk‑0001* ([1D[K
(formal structure claim).  
- **Preview‑commit workflow** → *chunk‑0001* (mechanisms description).  
- **Separation of utility classes** → *chunk‑0001* (connections to abstract[8D[K
abstract).  

No additional claims or citations have been introduced.

---

**End of Unified Synthesis**.
