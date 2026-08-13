**Spherepop – A Unified Theoretical Framework**

---

### 1. Functorial Representation of History  

* **Abstract Causal Index Category (Η).**  
  - Objects = “causal nodes” that denote distinct events or states.  
  - Morphisms = possible temporal or logical influence (e.g., *split → merg[4D[K
merge*).  

* **Realization Functors (𝑹)ᶦ:**  
  Each functor \(F: \mathcal{H} \rightarrow \mathcal{C}\) maps the abstract[8D[K
abstract causal structure onto concrete regions in a target category of rea[3D[K
realized objects. The translation preserves relational wiring, so terminal [K
objects (final states) are identified consistently across different realiza[7D[K
realizations.

---

### 2. Identity Criterion  

Two histories are identical when their normalized causal structures are iso[3D[K
isomorphic as **causal categories**, and the functors coincide on all corre[5D[K
corresponding morphisms under such an isomorphism. This recovers classical [K
“normal‑form identity” in a categorical language, demanding agreement not o[1D[K
only at terminal values but throughout the entire relational pattern.

---

### 3. Abstraction via Natural Transformations  

Natural transformations between realizations provide systematic reinterpret[11D[K
reinterpretations of a history that alter which concrete objects are assign[6D[K
assigned to nodes while preserving the underlying causal relations. Thus th[2D[K
the framework naturally supports a hierarchy of increasingly abstract descr[5D[K
descriptions without losing essential causal information.

---

### 4. Merge Events as Pushout Constructions  

* **Pushout Definition (Category Theory).**  
  Given morphisms \(f: R \rightarrow B\) and \(g: R \rightarrow C\), the pu[2D[K
pushout is an object \(D\) with maps \(B \rightarrow D\) and \(C \rightarro[10D[K
\rightarrow D\) that make the diagram commute, and \(D\) is universal for t[1D[K
this property.

* **Spherepop Interpretation.**  
  In a merge event (e.g., *split → merge*), objects such as \(B\) and \(C\)[5D[K
\(C\) originate from a common ancestor \(R\). The merge completes the pusho[5D[K
pushout square:

  \[
  \begin{tikzcd}
    R \arrow[r] \arrow[d] & C \arrow[d] \\
    B \arrow[r]           & D
  \end{tikzcd}
  \]

  Here \(D\) is uniquely determined by the common ancestor and the commutin[8D[K
commuting squares, embodying that identity depends on the full causal histo[5D[K
history rather than just the pair of descendant objects.

---

### 5. Entropy Landscape Interpretation  

* **Configuration Space (\(\mathcal{M}\)).**  
  Points represent possible structural states of a system.

* **Entropy Functional \(S\).**  
  Measures informational or thermodynamic complexity; irreversible events t[1D[K
typically increase \(S\).

* **Historical Trajectories.**  
  The history of an object is modeled as a directed path through \(\mathcal[10D[K
\(\mathcal{M}\) that generally moves toward higher entropy, reflecting the [K
directionality imposed by physical irreversibility.

---

### Integrated Structure  

Together these ideas provide:

1. **Categorical structure** capturing causal precedence via functors;  
2. **Pushouts** formalizing merge events as universal completions of commut[6D[K
commuting squares;  
3. **Entropy landscapes** giving an intuitive, physically grounded picture [K
of how histories evolve toward increasingly complex states.

---

### Rewriting Rules and Normalization  

The normalization procedure (Section \ref{sec:normalization}) can be captur[6D[K
captured by a rewriting system acting on Spherepop expressions:

* **Rule:** If two adjacent events \(E_i\) and \(E_j\) are independent (\(E[4D[K
(\(E_i \parallel E_j\)), their order may be swapped:
  \[
  (E_i, E_j) \;\longrightarrow\; (E_j, E_i).
  \]

**Normalization Process**

1. **Parse the Expression:** Convert to underlying event word representatio[13D[K
representation.  
2. **Construct Event Graph:** Identify all events and independence relation[8D[K
relations to build the causal graph of dependencies among events.  
3. **Apply Rewriting Rules Iteratively:**
   - Scan linearly; for each adjacent independent pair, apply the rule.
   - Continue until no further swaps are possible.  
4. **Resulting Normal Form:** The event word obtained is in its normal form[4D[K
form (canonical order). Two Spherepop expressions represent identical objec[5D[K
objects precisely when they normalize to the same normal form.

**Properties**

- **Confluence:** Any two sequences of rewrites lead to the same normal for[3D[K
form, ensuring result independence from rewrite ordering.
- **Termination:** No infinite descending chain exists; each rewrite reduce[6D[K
reduces adjacent non‑independent pairs until a fixed point is reached.

---

### Durable Theoretical Information Extracted  

1. **Analogy to Mazurkiewicz Trace Equivalence**  
   Spherepop defines a “commutation analogue” of the commutation relations [K
used in Mazurkiewicz trace equivalence (Mazurkiewicz 1987), establishing a [K
parallelism between event sequences modulo independent actions.

2. **Rewriting System Components**  
   Besides commutation, the system includes *split* (\(\text{split}(R) \rig[4D[K
\rightarrow A,B\)) and *merge* (\(\text{merge}(A,B) \rightarrow D\)) rules [K
for restructuring compound symbolic descriptions into standardized forms th[2D[K
that can be processed by commutation.

3. **Normalization Algorithm Phases**  
   - **Parsing & Graph Construction:** Builds an event graph from the symbo[5D[K
symbolic expression, creating vertices for each region and directed edges f[1D[K
for events.  
   - **Topological Ordering:** Computes a topological ordering of the DAG r[1D[K
representing causality; always possible for acyclic graphs.  
   - **Commutation Application:** Applies commutation rules to align the ev[2D[K
event word with the computed order, yielding Spherepop’s normal form.

4. **Confluence Property**  
   Proven because independence relation \(\parallel\) is symmetric and comm[4D[K
commutation rules satisfy the diamond property: any two applicable commutat[8D[K
commutations can be applied sequentially, and their combined result joins a[1D[K
after finitely many additional steps.

5. **Implications for Historical Identity**  
   Confluence guarantees that two expressions represent the same historical[10D[K
historical object precisely when they normalize to identical forms, providi[7D[K
providing a sound and complete decision procedure for causal identity withi[5D[K
within the system.

6. **Connections to Other Formalisms**  
   - **Trace Theory (Mazurkiewicz):** Identifies event sequences modulo ind[3D[K
independent commutation; Spherepop normal form selection mirrors this class[5D[K
classification of traces.  
   - **Petri Nets:** Maps regions ↔ places, events ↔ transitions, split ↔ m[1D[K
multi‑output transition, merge ↔ multi‑input transition; DAG property align[5D[K
aligns with acyclic firing sequences in Petri nets.  
   - **String Diagrams (Baez & Stay):** Geometric representations where spl[3D[K
splits are boxes with one input/output wire and merges are boxes with two i[1D[K
inputs/one output, visualizing sequential vs parallel composition.

7. **Higher‑Categorical Embedding**  
   Spherepop histories can be viewed as objects in a derived category where[5D[K
where:
   - Morphisms = irreversible causal events,
   - 2‑morphisms (commutation steps) encode rewriting equivalences between [K
histories,
   - Normalization acts as the derived functor extracting canonical represe[7D[K
representatives from equivalence classes.

8. **Sheaf Theory Interpretation**  
   Large histories assembled from overlapping subgraphs satisfy sheaf condi[5D[K
conditions: local descriptions on intersecting regions must agree, analogou[8D[K
analogous to gluing sections over open sets in topology.

9. **Derived Causal Categories**  
   Embedding Spherepop into derived causal categories with:
   - Objects = terminal nodes of event diagrams,
   - Morphisms = irreversible processes,
   - 2‑morphisms = rewriting equivalences,
   - Normalization as canonical global sections (complete histories).

These points collectively establish the foundational theoretical structure,[10D[K
structure, equivalence relations, and higher‑level categorial interpretatio[13D[K
interpretations that underpin Spherepop as a formal model for causal comput[6D[K
computation.

