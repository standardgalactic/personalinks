**Durable Theoretical Information Extracted**

1. **Core Structure – String Diagrams**
   - *Definition*: In Spherepop, event histories are represented by “string[7D[K
“string diagrams” where:
     - **Sequential composition** → vertical stacking of diagram components[10D[K
components.
     - **Parallel processes** → horizontal juxtaposition.
   - *Illustration*: Figure \ref{fig:string} shows a simple history \((\tex[7D[K
\((\text{spherepop}(D)) = (E_1, E_3)\) with \(E_1\) as “split” and \(E_3\) [K
as “merge”.

2. **Ontological Distinction – Historical Identity**
   - *Spherepop* differs from standard monoidal categories by treating **hi[4D[K
**historical identity** as the primary ontological criterion.
   - This means that causal relations, rather than mere morphisms, dictate [K
what counts as the same entity over time.

3. **Integrated Representations**
   - String diagrams and Petri‑net representations are presented as complem[7D[K
complementary visual/geometric encodings of the same underlying structure.
   - An additional layer—**event‑word and normal‑form apparatus**—provides [K
a canonical symbolic encoding (e.g., normal form).

4. **Higher‑Categorical Framework**
   - The causal history category \(\mathcal{H}\) (Section \ref{sec:functors[26D[K
(Section \ref{sec:functors}) has morphisms that are irreversible events, fo[2D[K
forming directed causal chains.
   - Rewriting operations from Appendix \ref{app:rewriting} act as **2‑morp[8D[K
**2‑morphisms** in a bicategory/2‑category:
     \[
       (E_i, E_j) \;\Rightarrow\; (E_j, E_i)
       \quad\text{when } E_i \parallel E_j,
       \]
     allowing re‑ordering of independent events.
   - **Coherence** is captured by the confluence result: any two sequences [K
of commutation steps relating the same pair of event chains are linked by h[1D[K
higher‑order equivalences.

5. **Derived Functor / Normalization**
   - The rewriting structure suggests that objects (event graphs) can be vi[2D[K
viewed as objects in a **derived category**.
   - The **normalization functor** (Section \ref{sec:normalization}) extrac[6D[K
extracts the canonical representative from equivalence classes of descripti[9D[K
descriptions, analogous to a derived functor.

6. **Sheaf‑Theoretic Interpretation**
   - Large histories are assembled by gluing compatible local histories def[3D[K
defined on overlapping subgraphs.
   - This is precisely the condition in sheaf theory for assembling global [K
sections:
     *Local knowledge* (processors) → **open sets** = hereditary sub‑DAGs,
     *Consistent local records* → **sections** = compatible local histories[9D[K
histories.
   - The resulting structure is a **sheaf over the causal graph**, with nor[3D[K
normal form providing the canonical global section.

7. **Operational Analogy – Distributed Computation**
   - In practice, different processors hold only their local scope of event[5D[K
events; consistency on overlaps (overlap verification) and subsequent gluin[5D[K
gluing produce the full computational history.
   - This mirrors the assembly process in sheaves: verify compatibility on [K
intersections and stitch together global descriptions.

8. **Embedding into a Broader Framework**
   - Spherepop can be embedded into a broader class of **derived causal cat[3D[K
categories** where:
     * Objects = terminal nodes of event diagrams,
     * Morphisms = irreversible processes,
     * 2‑morphisms = rewriting equivalences (commutations),
     * Normalization functors extract canonical representatives.
   - This programmatic direction is outlined in the essay’s concluding rema[4D[K
remarks.

---

These points capture the essential theoretical constructs—definitions, equa[4D[K
equations (via commutation relations), distinctions (historical identity vs[2D[K
vs. standard categories), mechanisms (higher‑categorical structure, derived[7D[K
derived functors), arguments (coherence and confluence as global consistenc[10D[K
consistency), conjectures (embedding into derived causal categories), depen[5D[K
dependencies (between string diagrams, Petri nets, event words), and unreso[6D[K
unresolved questions (how to fully axiomatize the rewriting system for all [K
histories).

