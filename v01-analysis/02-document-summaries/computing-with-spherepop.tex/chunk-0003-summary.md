**Durable Theoretical Information Extracted**

1. **Parameterized Complexity Framework**
   - *Quantities*: Depth of merge chains, number of primitive regions, voxe[4D[K
voxel resolution ($n^3$), mesh polygon count, implicit level‑set resolution[10D[K
resolution.
   - *Resource‑Constrained Evaluation*: Allows incomplete evaluation simila[6D[K
similar to approximate inference in probabilistic programming.

2. **Evaluation Time for Voxel Spherepop**
   - For a voxel representation with resolution $n^3$, each collapse step e[1D[K
evaluates in time \(O(n^3)\).
   - Under sparsity, complexity drops significantly due to reduced geometri[8D[K
geometric detail.

3. **Mesh Implementations**
   - With bounded polygon count, evaluation scales proportionally to surfac[6D[K
surface complexity (i.e., number of polygons).

4. **Implicit Representations**
   - Depend on discretization and step size for partial differential equati[6D[K
equation (PDE) solvers used in collapse.

5. **Semantic Foundations**
   - Spherepop inherits undecidability and worst‑case complexity from class[5D[K
classical computation.
   - It is semantically rigorous yet geometrically grounded, comparable to [K
symbolic models in expressive power.

6. **Open Problems & Research Directions**
   - **Collapse Operator Hierarchy**: Investigate whether there exists a st[2D[K
strict hierarchy \(C_0 \prec C_1 \prec \dots\) of collapse operators ordere[6D[K
ordered by expressiveness.
   - **Semantic Stability & Confluence**: Determine under what conditions e[1D[K
evaluation order does not affect the final semantic result (i.e., achieve c[1D[K
confluence).
   - **Geometric Invariants of Normal Forms**: Characterize the set of norm[4D[K
normal forms \(\mathcal{N}\) and assess properties such as convexity, smoot[5D[K
smoothness, contractibility, and uniqueness.
   - **Resource‑Bounded Semantics**: Develop bounded‑resource models analog[6D[K
analogous to those in functional and logic programming.
   - **Continuous Collapse & Differentiable Structure**: Analyze how differ[6D[K
differentiable manifolds of regions arise when \(\mathcal{G}\) is a Banach [K
manifold; explore potential fractal or intricate limiting surfaces.
   - **Monoidal & Cartesian Structure**: Identify whether merge can be mode[4D[K
modeled as a monoidal operator and collapse as a quotient functor, establis[8D[K
establishing categorical equivalence with known rewriting systems (e.g., in[2D[K
interaction nets).
   - **Comparisons with Established Models**: Determine formal equivalences[12D[K
equivalences/inequivalences between Spherepop and existing computational mo[2D[K
models such as lambda calculus or neural networks.
   - **Geometric Interpretation via Energy Minimization**: Express collapse[8D[K
collapse in variational form using energy functionals \(E(A)\) and gradient[8D[K
gradient descent to explore convergence properties.

7. **Implementation Strategies**
   - *Discrete Representations*: Voxel/surface approximations with threshol[8D[K
thresholding/smoothing operators for merge and collapse.
   - *Implicit Representations*: Level‑set functions solved via PDEs (e.g.,[6D[K
(e.g., curvature flow), enabling continuous, differentiable collapse.

These points encapsulate the core theoretical concepts, open questions, and[3D[K
and methodological directions derived from the document.

