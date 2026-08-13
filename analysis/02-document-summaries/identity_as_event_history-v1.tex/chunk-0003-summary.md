**Durable Theoretical Information Extracted**

1. **Spherepop Analogy to Mazurkiewicz Trace Equivalence**  
   - Spherepop defines a “commutation analogue” of the commutation relation[8D[K
relations used in Mazurkiewicz trace equivalence (Mazurkiewicz 1987). This [K
establishes that both frameworks operate on event sequences modulo independ[8D[K
independent actions.

2. **Rewriting System Components**  
   - Besides commutation, the system includes *split* ($\text{split}(R) \ri[3D[K
\rightarrow A,B$) and *merge* ($\text{merge}(A,B) \rightarrow D$) rules for[3D[K
for restructuring split/merge expressions in event graphs. These structural[10D[K
structural transformations convert compound symbolic descriptions into stan[4D[K
standardized forms that can be processed by commutation.

3. **Normalization Algorithm Phases**  
   - The algorithm proceeds through three conceptual phases:  
     a. **Parsing & Graph Construction:** Explicitly builds an event graph [K
from the symbolic expression, creating vertices for each region and directe[7D[K
directed edges for events.  
     b. **Topological Ordering:** Computes a topological ordering of the DA[2D[K
DAG (directed acyclic graph) representing causality; such ordering is alway[5D[K
always possible for graphs that are DAGs.  
     c. **Commutation Application:** Applies commutation rules to align the[3D[K
the event word with the computed topological order, yielding the Spherepop [K
normal form.

4. **Confluence Property**  
   - The commutation rewriting system is proven confluent (Proposition [Con[17D[K
(Proposition [Confluence]): all rewrite paths from a given initial state co[2D[K
converge to the same normal form regardless of the application order. Confl[5D[K
Confluence follows because:
     * Independence relation $\parallel$ is symmetric.
     * Commutation rules satisfy the diamond property: any two applicable c[1D[K
commutations can be applied sequentially, and their combined result joins a[1D[K
after finitely many additional steps.  
   - This guarantees that the normal form is unique and independent of the [K
specific rewriting strategy used.

5. **Implications for Historical Identity**  
   - Confluence ensures that two Spherepop expressions represent the same h[1D[K
historical object precisely when they normalize to identical forms, providi[7D[K
providing a sound and complete decision procedure for causal identity withi[5D[K
within the system.

6. **Connections to Other Formalisms**  
   - **Trace Theory (Mazurkiewicz):** Identifies event sequences modulo ind[3D[K
independent commutation; Spherepop normal form selection mirrors this class[5D[K
classification of traces.  
   - **Petri Nets:** Provides a direct mapping where regions ↔ places, even[4D[K
events ↔ transitions, split ↔ multi‑output transition, merge ↔ multi‑input [K
transition. The DAG property of Spherepop graphs aligns with the acyclic na[2D[K
nature required for Petri net firing sequences.  
   - **String Diagrams (Baez & Stay):** Offers geometric representations: s[1D[K
splits as boxes with one input/output wire and merges as boxes with two inp[3D[K
inputs/one output, visualizing sequential vs parallel composition.

7. **Figure Illustration (Fig. string)**  
   - Demonstrates a string‑diagram representation of a split event $E_1$ fo[2D[K
followed by a merge event $E_3$. The vertical stacking of components mirror[6D[K
mirrors the topological ordering phase, while horizontal juxtaposition capt[4D[K
captures parallel processes.

8. **Higher‑Categorical Embedding**  
   - Spherepop histories can be viewed as objects in a derived category whe[3D[K
where:
     * Morphisms are irreversible causal events.
     * 2‑morphisms (commutation steps) encode rewriting equivalences betwee[6D[K
between histories.
     * Normalization acts as the derived functor extracting canonical repre[5D[K
representatives from equivalence classes.

9. **Sheaf Theory Interpretation**  
   - Large histories assembled from overlapping subgraphs satisfy sheaf con[3D[K
conditions: local descriptions on intersecting regions must agree, analogou[8D[K
analogous to gluing sections over open sets in topology. This captures dist[4D[K
distributed computation where processors hold only partial event knowledge [K
and assemble a global history via consistency checks.

10. **Derived Causal Categories**  
    - The conceptual framework suggests embedding Spherepop into derived ca[2D[K
causal categories with:
      * Objects corresponding to terminal nodes of event diagrams.
      * Morphisms representing irreversible processes.
      * 2‑morphisms reflecting rewriting equivalences.
      * Normalization providing canonical global sections (complete histori[7D[K
histories).

These points collectively establish the foundational theoretical structure,[10D[K
structure, equivalence relations, and higher‑level categorial interpretatio[13D[K
interpretations that underpin Spherepop as a formal model for causal comput[6D[K
computation.

