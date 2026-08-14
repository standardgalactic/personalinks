**Compilation as Graph Rewriting**

The idea behind *Spherepop* is to view compilation not as a series of synta[5D[K
syntactic transformations applied at different textual stages, but rather a[1D[K
as **a sequence of rewrite operations on an underlying composition (depende[8D[K
(dependency) graph**. This perspective unifies many disparate compiler tech[4D[K
techniques into a single conceptual framework:

1. **Composition Graph as the Core Object**  
   - Let \( G = (N, E) \) be a directed acyclic or cyclic graph where nodes[5D[K
nodes represent computations and edges denote data dependencies.
   - Every program can be expressed as such a graph; variable names, format[6D[K
formatting, and syntactic sugar are all *derived* properties that disappear[9D[K
disappear when we focus on the graph structure.

2. **Rewrite Operators**  
   - A compiler is modeled as applying a finite sequence of rewrite operato[7D[K
operators \( R_1, R_2, \dots, R_k \) to the composition graph:
     \[
     G \;\Longrightarrow\; R_1(G) \;\Longrightarrow\; R_2(R_1(G)) \;\Longri[9D[K
\;\Longrightarrow\; \cdots \;\Longrightarrow\; R_k\!\cdots\!R_1(G).
     \]
   - Each rewrite produces a new graph that is *observationally equivalent*[11D[K
equivalent* to the original (see correctness below).

3. **Correctness of Rewriting**  
   - Let \( \mathcal{H}(G) \) be the set of observable histories generated [K
by executing graph \( G \). A rewrite \( R \) is operationally correct if:
     \[
     \mathcal{H}(R(G)) \cong \mathcal{H}(G),
     \]
     where “\(\cong\)” denotes observational equivalence (deterministic out[3D[K
output, distributional equality for probabilistic models, etc.).  
   - This guarantee means the semantics—what the program does—is preserved [K
regardless of how we transform its representation.

4. **Examples of Rewrite Rules**  

   | Rewrite Rule | Description |
   |--------------|-------------|
   | **Inlining** | If a node \( f \) calls another function represented by[2D[K
by subgraph \( G_f \), replace the call with an in‑line copy:
     \[
     C[f] \;\longrightarrow\; C[G_f],
     \]
     where \( C \) is the surrounding context. |
   | **Dead Graph Elimination** | Remove any node that never feeds into obs[3D[K
observable outputs (reachability analysis). Only reachable components affec[5D[K
affect observable histories. |
   | **Constant Propagation** | When all inputs to an operator are known co[2D[K
constants, evaluate its output at compile time and replace it with a consta[6D[K
constant node:
     \[
     f(c_1,\dots,c_n) \;\longrightarrow\; c,
     \]
     where \( c \) is the computed constant. |
   | **Common Subgraph Elimination** | Identify duplicate subgraphs (e.g., [K
repeated calls to the same function) and merge them into a single shared no[2D[K
node, reducing overall graph size without changing observable behavior. |

5. **Progressive Refinement View**  
   - Traditional pipelines—lexical analysis → parsing → semantic analysis →[1D[K
→ optimization → instruction selection → register allocation → code generat[7D[K
generation—are seen as successive graph transformations that progressively [K
simplify the representation while preserving its computational content.
   - Each stage can be viewed as applying specific rewrite operators tailor[6D[K
tailored to expose inefficiencies (e.g., dead code) or opportunities for sh[2D[K
sharing subcomputations.

6. **Inter‑Paradigm Compilation**  
   - Because the same graph structure is used across different execution mo[2D[K
models, translating between paradigms (Boolean circuits → arithmetic circui[6D[K
circuits → GPU kernels, etc.) reduces to applying appropriate operator libr[4D[K
libraries—i.e., homomorphisms of rewrite operators.
   - This abstraction allows compilers to target diverse hardware backends [K
without fundamentally changing the underlying computation.

**Why This Matters**

- **Semantic Over Syntactic**: By focusing on observable behavior rather th[2D[K
than textual representation, optimizations become reasoned about at a highe[5D[K
higher level (graph equivalence), reducing reliance on ad‑hoc heuristics.
- **Unified Treatment of Techniques**: Many seemingly distinct optimization[12D[K
optimization passes—dead code elimination, inlining, constant folding—are a[1D[K
all special cases of graph rewriting, simplifying the compiler’s design and[3D[K
and maintenance.
- **Scalability Across Domains**: The same rewrite machinery can be applied[7D[K
applied to symbolic programs (e.g., theorem proving), hardware circuits, or[2D[K
or neural networks, enabling a unified compilation strategy across disparat[8D[K
disparate computational paradigms.

In essence, *Spherepop* recasts compilers as **graph rewriting systems**, w[1D[K
where the program’s meaning is captured by its dependency graph and optimiz[7D[K
optimizations are simply systematic transformations preserving that meaning[7D[K
meaning. This shift from text‑centric to graph‑centric thinking provides bo[2D[K
both conceptual clarity and a powerful framework for building more flexible[8D[K
flexible, generalizable compilation tools.
