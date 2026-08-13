**Thesis**

Computation is fundamentally a process of constructing and manipulating *hi[3D[K
*histories*—partial orders that record causal containment of events. The ev[2D[K
event‑historical kernel provides an algebraic framework where histories, ra[2D[K
rather than abstract states, are the primary objects of computation. This p[1D[K
perspective unifies diverse systems (distributed logs, version control, con[3D[K
constraint solving) by emphasizing irreversible accumulation of causally or[2D[K
ordered events.

**Primitives and Definitions**

1. **History Poset (\(\mathcal{H}\))**  
   - A *history* \(H\) is a partially ordered set (poset) representing the [K
causal sequence of executed operations.  
   - The prefix order \(\leq\) satisfies \(H_1 \leq H_2\) iff there exists [K
an extension such that \(H_1\) appears as an initial segment of \(H_2\). Th[2D[K
This captures temporal and causal containment.

2. **Monotonic Extension Operator (\(\operatorname{ext}\))**  
   - Defined on pairs \((H, e)\) where \(e\) is a new event: \(\operatornam[14D[K
\(\operatorname{ext}(H,e)=H \cup \{e\}\) extended to the smallest consisten[9D[K
consistent history respecting causality.  
   - Monotonicity: if \(H_1 \leq H_2\), then \(\operatorname{ext}(H_1, e)\)[4D[K
e)\) extends to a history that is at least as long or equally constrained a[1D[K
as extending \(H_2\).

3. **Merge (Join) Operation (\(\sqcup\))**  
   - Two histories \(H_1\) and \(H_2\) are *compatible* when their causal d[1D[K
domains do not conflict. Their merge is the least upper bound:  
     \[
     H_1 \sqcup H_2 = \bigcap_{K \geq H_1, K \geq H_2} K,
     \]
     where “\(K \geq H\)” means \(H \leq K\). This yields a join‑semilattic[15D[K
join‑semilattice structure.

4. **Reduction Morphisms (\(\sigma:\mathcal{H}\to S\))**  
   - Capture snapshots or summaries of histories, mapping multiple distinct[8D[K
distinct histories onto the same reduced state while preserving essential c[1D[K
causal constraints (e.g., CRDT “state summary”).

**Formalism**

The event‑historical kernel is expressed as a *history algebra*:

- **Objects**: System interfaces or boundaries.
- **Morphisms**: Histories \(H\) are morphisms between these objects, order[5D[K
ordered by the prefix relation. Composition of histories corresponds to con[3D[K
concatenation:  
  \[
  (h_1; h_2) = \operatorname{ext}(\operatorname{last}(h_1), h_2).
  \]
- **Duality**: Forward extension (\(h_{u\to t}\)) and reduction map histori[7D[K
histories onto coarser states, revealing an initial‑object property: any st[2D[K
structure with the same operations admits a unique homomorphism from \(\mat[6D[K
\(\mathcal{H}\).

**Mechanisms**

1. **Deterministic Replay**  
   If event semantics are deterministic (no nondeterminism), replaying hist[4D[K
history \(H\) yields a unique state representation \(\sigma(H)\). Each caus[4D[K
causal step uniquely transforms the system’s state.

2. **Monotonic Growth**  
   Extending a history with an admissible event always produces a larger hi[2D[K
history (\(H \leq H'\)), preserving causality and ensuring that future hist[4D[K
histories are extensions of past ones.

3. **Convergent Merging**  
   Compatible histories merge into their least upper bound, guaranteeing mi[2D[K
minimal yet fully containing representations (e.g., Git’s “merge trees” or [K
CRDTs’ eventual convergence).

**Major Arguments**

- Viewing computation as the irreversible construction and manipulation of [K
histories shifts focus from state‑transformations to *event accumulation*, [K
revealing deeper structural principles such as deterministic replay, monoto[6D[K
monotonic extension, and convergent merging.
- This perspective aligns with distributed systems where append‑only logs n[1D[K
naturally embody these properties (CRDTs), showing that computational behav[5D[K
behavior can emerge without a global clock.

**Dependencies Between Concepts**

- **History ↔ State**: Reduction morphisms map histories onto observable st[2D[K
states; the dual representation clarifies how abstraction layers (snapshots[10D[K
(snapshots vs. full history) affect system reasoning.
- **Monotonicity & Convergence**: The prefix order ensures monotonic extens[6D[K
extension, while merge operations guarantee eventual convergence in distrib[7D[K
distributed contexts, linking local event processing to global consistency.[12D[K
consistency.

**Implications**

1. **Unified Model for Diverse Systems**  
   - Provides a common algebraic foundation for log‑based architectures (Gi[3D[K
(Git, append‑only databases), version control systems, and constraint solve[5D[K
solvers.
   - Demonstrates that seemingly disparate computational models share under[5D[K
underlying structural properties rooted in causal history accumulation.

2. **Abstraction & Scalability**  
   - Reduction maps enable efficient snapshots for monitoring or recovery w[1D[K
without storing full histories, reducing storage overhead while preserving [K
enough causality to reconstruct past states if needed.

3. **Predictive Power**  
   - The deterministic replay property allows forward simulation of system [K
evolution from partial histories, aiding verification and testing in distri[6D[K
distributed systems where global state is unattainable.

**Unresolved Problems**

- **Non‑Deterministic Semantics**: How do non‑deterministic or probabilisti[12D[K
probabilistic event models integrate while preserving causal containment?
- **Partial Order Extension Limits**: When does the prefix order fail to pr[2D[K
provide a meaningful extension (e.g., conflicting causality) and how should[6D[K
should such cases be handled?
- **Complexity of Merges in High‑Concurrency Environments**: Scalability is[2D[K
issues arise when many histories need merging simultaneously; mechanisms fo[2D[K
for efficient concurrent merge resolution remain open.

**Internal Tensions**

- **State vs. History Focus**: Treating history as primary conflicts with t[1D[K
traditional state‑centric approaches (e.g., Turing machines). Balancing the[3D[K
the benefits of abstraction without losing information about causal evoluti[7D[K
evolution is a tension.
- **Determinism Assumption**: Real-world systems often have nondeterministi[15D[K
nondeterministic operations; relaxing deterministic assumptions requires re[2D[K
redefining extensions and merges to accommodate conflict resolution strateg[7D[K
strategies.

**Connections Likely to Matter Elsewhere in Spherepop**

- **Physical Systems Analogy**: The algebra mirrors principles in physical [K
lattice models (Ising models, Markovian dynamics) where local interactions [K
build global structures. This suggests transferable insights for modeling e[1D[K
emergent properties across domains.
- **Causal Graphs & Causality Networks**: Histories can be viewed as causal[6D[K
causal graphs; the kernel’s operations align with graph‑theoretic concepts [K
like contraction and merging used in causal inference, indicating potential[9D[K
potential cross‑disciplinary applications (e.g., epidemiology, economics).

**Conclusion**

The event‑historical kernel offers a novel paradigm for understanding compu[5D[K
computation: it grounds computational processes in the irreversible accumul[7D[K
accumulation of causally ordered events. By formalizing histories as primar[6D[K
primary objects with well‑defined extensions and merges, this framework uni[3D[K
unifies diverse distributed systems models, enhances abstraction mechanisms[10D[K
mechanisms, and raises critical questions about non‑determinism, scalabilit[10D[K
scalability, and integration with broader physical and information theories[8D[K
theories across Spherepop’s domains.

