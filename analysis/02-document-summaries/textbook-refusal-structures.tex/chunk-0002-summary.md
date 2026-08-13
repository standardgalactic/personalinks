**Compilation as Graph Rewriting**

In Spherepop’s view, compilation is fundamentally a process of transforming[12D[K
transforming a *composition graph* \(G=(N,E)\) through a finite sequence of[2D[K
of rewrite operators \(\{R_1,R_2,\dots ,R_k\}\):

\[
G \;\Longrightarrow\; R_1(G) \;\Longrightarrow\; R_2(R_1(G)) \;\Longrightar[14D[K
\;\Longrightarrow\; \cdots \;\Longrightarrow\; R_k\!\cdots\!R_1(G).
\]

Each rewrite \(R\) produces a new graph that is observationally equivalent [K
to the original (i.e., it yields the same observable histories under the ch[2D[K
chosen notion of equivalence). This perspective unifies many traditionally [K
distinct compiler phases—optimizations, lowering steps, specialization, and[3D[K
and code generation—as successive structural transformations rather than se[2D[K
separate syntactic stages.

---

### Key Concepts

1. **Graph as the Core Object**  
   After parsing (which only converts source text into an AST for convenien[9D[K
convenience), every optimization step is understood as a graph transformati[12D[K
transformation that preserves computational behavior.

2. **Correctness via Observational Equivalence**  
   A rewrite \(R\) is operationally correct if it leaves the set of observa[7D[K
observable histories unchanged:
   \[
   \mathcal H(R(G))\cong\mathcal H(G),
   \]
   where \(\cong\) denotes equivalence depending on whether the computation[11D[K
computation is deterministic, probabilistic, symbolic, or repair‑aware.

3. **Inlining as Graph Substitution**  
   If a node \(f\) invokes another function represented by subgraph \(G_f\)[7D[K
\(G_f\), inlining replaces the call pattern with a direct substitution:
   \[
   G = C[f] \;\longrightarrow\; C[G_f].
   \]
   This shows that “calling” is just graph substitution, not a semantic rul[3D[K
rule about functions.

4. **Dead Graph Elimination**  
   Nodes whose outputs are never reachable from the designated output verti[5D[K
vertices (i.e., unreachable in reverse dependency) can be removed:
   \[
   G = C[G_f] \quad\text{with}\quad f\notin\operatorname{Reach}(G).
   \]
   This mirrors traditional dead‑code elimination but operates on graph str[3D[K
structure rather than textual statements.

5. **Constant Propagation**  
   When an operator receives only constant arguments, its output can be com[3D[K
computed at compile time:
   \[
   f(c_1,\dots ,c_n) \;\longrightarrow\; c,
   \]
   turning the computation into a single constant node without changing obs[3D[K
observable behavior.

6. **Common Subgraph Elimination**  
   Duplicate computations are represented by identical subgraphs. Replacing[9D[K
Replacing two occurrences of an isomorphic fragment with one shared node:
   \[
   \text{two copies} \;\longrightarrow\; \text{one shared node}.
   \]
   This mirrors traditional common subexpression elimination but makes shar[4D[K
sharing explicit in the graph.

---

### Unifying Compiler Techniques

All these optimizations—Inlining, Constant Propagation, Dead Code Eliminati[9D[K
Elimination, Common Subgraph Elimination, Partial Evaluation, Strength Redu[4D[K
Reduction, Loop Invariant Motion, etc.—are special cases of applying approp[6D[K
appropriate rewrite rules. The compiler’s task reduces to:

1. **Recognize patterns** (e.g., function calls, constant inputs).  
2. **Apply a corresponding graph transformation** (substitution or merging)[8D[K
merging).  
3. **Verify observational equivalence**.

This three‑step process simplifies the conceptual architecture: instead of [K
memorizing many distinct optimization heuristics, one studies an algebraic [K
system of graph transformations that naturally produce familiar optimizatio[11D[K
optimizations as instances.

---

### Progressive Refinement

The traditional pipeline—lexical analysis → parsing → semantic analysis → o[1D[K
optimization → instruction selection → register allocation → code generatio[9D[K
generation—is seen not as a series of unrelated phases but as successive **[2D[K
**graph refinement** steps. Each stage produces a computationally simpler o[1D[K
or more substrate‑friendly graph without altering the underlying meaning.

---

### Multiple Intermediate Representations

Different intermediate representations (AST, control‑flow graphs, data‑flow[9D[K
data‑flow graphs, SSA forms, netlists, etc.) are interpreted as different *[1D[K
*coordinate systems* on the same composition graph. The actual computation [K
is invariant; only the chosen structural view changes, analogous to how Car[3D[K
Cartesian, polar, or homogeneous coordinates describe the same geometric ob[2D[K
object differently.

---

### Instruction Selection

At the final stage, instruction selection becomes simply **operator replace[7D[K
replacement**: a node representing \(f(x,y)\) may be relabeled with the nat[3D[K
native machine operator for \(f\) if one exists. If not, it is replaced by [K
a subgraph implementing the same behavior (e.g., division → shift‑subtract [K
sequences). This uniform treatment of backends highlights that compilation [K
across disparate computational paradigms—Boolean circuits, arithmetic circu[5D[K
circuits, GPU kernels, neural accelerators—is just graph homomorphism betwe[5D[K
between operator libraries.

---

### Optimization via Local Identities

Simple identities like \(x+0 = x\) or \(x\land1 = x\) illustrate that many [K
optimizations arise from local equivalence relations. Each such identity re[2D[K
replaces a fragment with an equivalent smaller fragment, leaving the surrou[6D[K
surrounding computation untouched.

---

**Conclusion**

By framing compilation as graph rewriting—where variables, formatting, and [K
syntactic sugar vanish into abstract dependency structure—the approach reve[4D[K
reveals a unified, semantics‑driven view of compilers. This perspective not[3D[K
not only clarifies why different optimizations are often instances of simil[5D[K
similar rewrite rules but also suggests new ways to design cross‑domain com[3D[K
compilers that operate on the same underlying computation expressed as grap[4D[K
graphs.

