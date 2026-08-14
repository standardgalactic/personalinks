**Summary Overview – Normalisation by Historical Evaluation (NbHE)**  

The document describes a kernel‑level evaluation strategy that couples *sem[4D[K
*semantic domain* with an explicit **historical context**. Below is a conci[5D[K
concise high‑level view of the main concepts:

1. **Historical Fibrations**  
   - The semantics are expressed as an indexed category \(\pi:\mathcal E\to[4D[K
E\to\mathcal H\) (or fibration).  
   - Each history \(H\) in the base category \(\mathcal H\) corresponds to [K
a *fiber* that contains exactly those constructions that can be replayed af[2D[K
after the history is known.  
   - This replaces ordinary context variables with immutable, traceable his[3D[K
histories.

2. **Comprehension**  
   - For a type \(A\) interpreted over a history \(H\), the comprehension o[1D[K
object \((H,A)\) represents extending the current history by an admissible [K
“declaration event.”  
   - Instead of adding arbitrary assumptions to a context, each new constru[7D[K
construction is recorded as a permanent step in the history.

3. **Soundness**  
   - If a term \(t\) is well‑typed as \(H\vdash t:A\), its semantic interpr[7D[K
interpretation \(\llbracket t \rrbracket\) lies in the appropriate semantic[8D[K
semantic object \(\llbracket A \rrbracket\).  
   - Any replay step (changing historical state) preserves denotational mea[3D[K
meaning, guaranteeing invariant semantics.

4. **Completeness**  
   - Every construction that can be produced by the full historical categor[7D[K
category can be represented as a replayable kernel derivation.  
   - This establishes equivalence between operational evaluation and semant[6D[K
semantic interpretation for all well‑formed histories.

5. **Historical Interpretation**  
   - The denotational model provides a *semantic foundation* where construc[8D[K
constructive histories become primitive mathematical objects, underpinning [K
computation, proof systems, dependent types, equality, and categorical stru[4D[K
structures in Spherepop.

6. **Four Viewpoints**  
   - **Syntax:** Formal language rules for constructing terms.  
   - **Operations/Algorithms:** How these constructions are performed compu[5D[K
computationally (replay‑aware reduction).  
   - **Semantics:** Meaning of the constructions expressed through historie[8D[K
histories.  
   - **Implementation:** Concrete kernel design elements that realise NbHE [K
in Spherepop’s operating environment.

7. **References**  
   The bibliography lists foundational works (Church 1940; Milner 1978; Awo[3D[K
Awodey 2010; Harper 2016, etc.) supporting the soundness and completeness o[1D[K
of the approach.

*End of summary.*

