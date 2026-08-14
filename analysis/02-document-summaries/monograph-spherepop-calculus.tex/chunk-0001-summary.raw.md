**Summary**

The paper develops a categorical semantics for SPC (a probabilistic core ca[2D[K
calculus) by situating its type‑forming operations within symmetric monoida[7D[K
monoidal categories.  

- **Merge** is interpreted as the tensor product, capturing independent par[3D[K
parallel computations and ensuring associativity/symmetry required of a mon[3D[K
monoidal structure.  
- **Sphere/Pop** encode the exponential (currying) adjunction: entering a `[1D[K
`Sphere` opens a scope (abstraction), while `Pop` instantiates it with an a[1D[K
argument, mirroring the internal hom in cartesian closed categories.  
- **Choice** is modeled as a convex mixture of morphisms (Markov kernels), [K
providing probabilistic branching and fitting into the distribution monad f[1D[K
framework.  

Both algebraic nondeterminism and categorical concurrency are uniformly rep[3D[K
represented via these equational properties.

---

**Denotational Semantics**

The semantics is defined in the presheaf topos $[\mathsf{Sphere}^{op}, \mat[4D[K
\mathsf{Set}]$, which supplies:

1. **Subobject classifier** – truth sphere,  
2. **Finite limits and colimits**,  
3. **Exponentials** (propositions = subspheres, proofs = morphisms preservi[8D[K
preserving truth).  

The **distribution monad $\mathcal{D}$** maps objects to probability measur[6D[K
measures; its unit is a Dirac measure, and the Kleisli extension implements[10D[K
implements probabilistic bind.

**Core clauses**

- **Sphere**:  
  \[
  \llbracket \mathrm{Sphere}(x{:}A.\,t) \rrbracket
  :\; \llbracket \Gamma \rrbracket \to \llbracket A \rrbracket \Rightarrow [K
\llbracket B \rrbracket.
  \]

- **Pop**:  
  \[
  \llbracket \mathrm{Pop}(t,u) \rrbracket
  =\; \mathsf{ev} \circ \langle \llbracket t \rrbracket , \llbracket u \rrb[4D[K
\rrbracket\rangle.
  \]

- **Merge**:  
  \[
  \llbracket \mathrm{Merge}(t,u) \rrbracket
  =\; \langle \llbracket t \rrbracket , \llbracket u \rrbracket\rangle .
  \]

**Probabilities and Choice (Option B)**

For a probability \(p:\llbracket\Gamma\rrbracket\to[0,1]\) and terms \(t,u\[6D[K
\(t,u\) of type \(A\), the semantics of `Choice` is:

\[
\llbracket \mathrm{Choice}(p,t,u) \rrbracket
= \big(\lambda \gamma.\; p(\gamma)\cdot\delta_{\llbracket t\rangle(\gamma)}[17D[K
t\rangle(\gamma)} + (1-p(\gamma))\cdot\delta_{\llbracket u\rangle(\gamma)}\[18D[K
u\rangle(\gamma)}\big).
\]

---

**Sphere/Pop as Exponentials**

- **Abstraction**: A context \(\Gamma\vdash f:A\to B\) yields a morphism  
  \[
  \mathsf{Sphere}(f):B^{A}.
  \]
- **Application (Pop)**: Instantiates the scope, producing  
  \[
  \Gamma\vdash\mathsf{Pop}(\mathsf{Sphere}(f),a):B.
  \]

The β‑ and η‑laws of SPC reproduce the expected adjunction laws of exponent[8D[K
exponentials in a cartesian closed category.

---

**Merge as Tensor**

In a symmetric monoidal category, `Merge` corresponds to the tensor product[7D[K
product:

\[
\Gamma\vdash M:A,\;\Delta\vdash N:B \;\Rightarrow\; \Gamma,\Delta\vdash M\o[3D[K
M\otimes N:A\otimes B.
\]

Associativity and symmetry ensure well‑behaved parallel composition.

---

**Choice as Convex Mixture**

`Choice(p,M,N)` is interpreted as a convex combination:

\[
\llbracket \mathrm{Choice}(p,M,N) \rrbracket
= p\cdot\llbracket M\rbracket + (1-p)\cdot\llbracket N\rbracket.
\]

Generalizing to finite distributions yields a convex algebra structure, ena[3D[K
enabling probabilistic reasoning within the type system.

---

**Distribution Monad Structure**

The distribution monad $\mathcal{D}$ maps objects to probability measures a[1D[K
and morphisms to Markov kernels. Its unit is the Dirac measure, while the K[1D[K
Kleisli extension defines semantics for `Choice`. For independent channels [K
combined by `Merge`, semantics inherit product‑measure structures.

---

**Meta‑Theory**

Key results include:

- **Preservation**: If $\Gamma\vdash M:A$ and $M\to M'$, then $\Gamma\vdash[13D[K
$\Gamma\vdash M':A$. Proven by induction on derivations for Sphere/Pop, Mer[3D[K
Merge, and Choice reductions.  
- **Progress**: If $\emptyset\vdash M:A$, either \(M\) is a value or there [K
exists \(M'\) such that $M\to M'$. Probabilistic branching ensures at least[5D[K
least one reducible step with non‑zero probability.

These results confirm the compositional, well‑typed nature of SPC within it[2D[K
its categorical framework.

