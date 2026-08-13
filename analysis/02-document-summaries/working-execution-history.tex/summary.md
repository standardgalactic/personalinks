**Thesis**

In this framework, *time* is not an external coordinate but a direct attrib[6D[K
attribute of how histories evolve. Execution time measures the raw length ([1D[K
(number of events) in a history, while causal time captures the discrete na[2D[K
nature of event addition within a causally ordered process. The monotonic e[1D[K
extension operator guarantees that execution time monotonically increases, [K
embodying irreversible construction central to computation.

**Primitives and Definitions**

1. **Execution Time**: For any admissible history \(H\) in \(\mathcal{H}\),[16D[K
\(\mathcal{H}\), the execution time \(t(H)\) is defined as the cardinality [K
of the set of events:
   \[
   t(H) = |H|.
   \]

2. **Causal Time**: For two events \(e_1, e_2 \in H\) with \(e_1 < e_2\), t[1D[K
the causal time interval between them is one step:
   \[
   \Delta_c(e_1, e_2) = t(\operatorname{ext}(H_{\text{prefix before }e_1}, [K
e_2)) - t(H_{\text{prefix before }e_1}) = 1.
   \]

3. **Irreversibility Property**: Given \(H' = \operatorname{ext}(H, e)\), t[1D[K
there is no operation to retract \(e\) from \(H'\) without violating the pr[2D[K
prefix ordering; thus history length (execution time) monotonically increas[7D[K
increases.

**Formalism**

The causal containment captured by the prefix relation yields a discrete te[2D[K
temporal notion. The extension operator \(\operatorname{ext}\) appends even[4D[K
events exclusively, ensuring that execution proceeds forward and no reverse[7D[K
reverse operations exist to alter past histories without breaking causality[9D[K
causality.

**Mechanisms**

1. **Prefix Ordering**: Extending a history by one event always increases i[1D[K
its execution time by exactly one unit, making time intrinsically tied to t[1D[K
the sequence of event additions.
2. **Irreversibility**: The inability to remove events ensures that histori[7D[K
historical progression is unidirectional, reflecting fundamental computatio[10D[K
computational processes like distributed logs and version‑control graphs wh[2D[K
where each commit adds a single step to the overall timeline.

**Major Arguments**

- Time emerges directly from how histories grow and are ordered, distinguis[10D[K
distinguishing between raw execution length and causal intervals.
- This perspective aligns with practical systems (e.g., Git) where each add[3D[K
addition represents one unit of time, reinforcing that computational behavi[6D[K
behavior is history‑driven rather than externally imposed.
- Reduction morphisms compress histories into states or snapshots, preservi[8D[K
preserving causal order without capturing actual elapsed time.

**Dependencies Between Concepts**

- **Execution Time vs. Causal Time**: Execution time measures the total num[3D[K
number of events, while causal time reflects discrete event additions in a [K
causally ordered process.
- **Irreversibility and Prefix Ordering**: The monotonic extension operator[8D[K
operator guarantees that execution time monotonically increases, embodying [K
irreversible construction central to computation.

**Implications**

1. Computational behavior is fundamentally history‑driven, influencing how [K
we reason about program correctness, concurrency control, and emergent glob[4D[K
global structures.
2. This framework provides a unified view applicable across distributed sys[3D[K
systems, version control, constraint programming, and physical lattice dyna[4D[K
dynamics where local interactions accumulate into complex behaviors.

**Unresolved Problems**

- How to formalize the abstraction from histories to states without losing [K
essential causal relationships that drive system behavior.
- Extending these concepts to non‑deterministic or probabilistic computatio[10D[K
computational models while preserving the irreversibility principle.

**Internal Tensions**

- Balancing the granularity of execution time (raw length) with the coarser[7D[K
coarser perspective offered by state representations, which may obscure tem[3D[K
temporal details but preserve causal order.
- Addressing potential ambiguities when reducing histories to states across[6D[K
across different domains where "time" can be interpreted variably (e.g., co[2D[K
computational steps vs. physical elapsed time).

**Connections Likely to Matter Elsewhere in Spherepop**

- The event‑historical kernel aligns with broader scientific principles gov[3D[K
governing the emergence of complex behavior, suggesting applications beyond[6D[K
beyond computation into fields like distributed systems theory, version con[3D[K
control design, and even statistical physics models such as Ising models wh[2D[K
where local constraints accumulate to produce global structures.

