**Key Points Extracted**

1. **Core Structure – String Diagrams**
   - *Definition*: Spherepop histories are encoded as string diagrams where[5D[K
where sequential composition is vertical stacking and parallel processes ar[2D[K
are horizontal juxtaposition.
   - *Illustration*: Figure \ref{fig:string} shows a simple history \((\tex[7D[K
\((\text{spherepop}(D)) = (E_1, E_3)\) with \(E_1\) as “split” and \(E_3\) [K
as “merge”.

2. **Ontological Distinction – Historical Identity**
   - Spherepop treats causal relations—not mere morphisms—as the primary cr[2D[K
criterion for identity, distinguishing it from standard monoidal categories[10D[K
categories.

3. **Integrated Representations**
   - String diagrams are complementary to Petri‑net representations; an eve[3D[K
event‑word and normal‑form apparatus provide a canonical symbolic encoding [K
(e.g., normal form).

4. **Higher‑Categorical Framework**
   - The causal history category \(\mathcal{H}\) has morphisms that are irr[3D[K
irreversible events, forming directed causal chains.
   - Rewriting operations act as 2‑morphisms in a bicategory/2‑category:  
     \[
       (E_i, E_j) \;\Rightarrow\; (E_j, E_i)
       \quad\text{when } E_i \parallel E_j,
       \]
     allowing reordering of independent events.
   - **Coherence** is ensured by confluence results linking different commu[5D[K
commutation sequences.

5. **Derived Functor / Normalization**
   - The normalization functor extracts the canonical representative from e[1D[K
equivalence classes, analogous to a derived functor in category theory.

6. **Sheaf‑Theoretic Interpretation**
   - Large histories are assembled by gluing compatible local histories def[3D[K
defined on overlapping subgraphs.
   - This mirrors sheaf conditions: verify compatibility (overlap verificat[9D[K
verification) and stitch global sections.

7. **Operational Analogy – Distributed Computation**
   - Processors hold only their local scope of events; consistency is achie[5D[K
achieved through overlap verification, analogous to assembling global descr[5D[K
descriptions in a distributed system.

8. **Embedding into a Broader Framework**
   - Spherepop can be embedded into derived causal categories where objects[7D[K
objects are terminal nodes of event diagrams, morphisms are irreversible pr[2D[K
processes, and 2‑morphisms capture rewriting equivalences.
   - Normalization functors provide canonical representatives for all histo[5D[K
histories.

**Dependencies & Open Questions**

- **String Diagram ↔ Petri Net**: Understanding how to convert between thes[4D[K
these representations preserves both the causal structure and locality cons[4D[K
constraints.
- **Rewriting System Axiomatization**: Formally proving termination and con[3D[K
confluence for arbitrary event graphs remains an open problem in formalizin[10D[K
formalizing Spherepop completely.

