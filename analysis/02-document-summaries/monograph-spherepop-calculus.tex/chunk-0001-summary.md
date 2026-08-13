**Summary**

The paper presents a categorical (denotational) semantics for a typed λ‑cal[5D[K
λ‑calculus with probabilistic branching, concurrency, and coinduction – dub[3D[K
dubbed **SPC** (Stateful Probabilistic Concurrent Calculus).  

* **Core structure:**  
  - The operational language includes the type constructors **Sphere**, **P[3D[K
**Pop**, **Merge**, and **Choice**.  
  - **Sphere/Pop** encode abstractions and applications as morphisms in the[3D[K
the exponential of a cartesian closed category, while **Merge** is interpre[8D[K
interpreted as the tensor product (⊗) in a symmetric monoidal category, giv[3D[K
giving rise to parallel composition.  
  - **Choice** represents probabilistic branching via convex mixtures; it c[1D[K
can be generalized to finite distributions.

* **Categorical semantics:**  
  - The domain of interpretation is the presheaf topos $[\mathsf{Sphere}^{o[20D[K
$[\mathsf{Sphere}^{op}, \mathsf{Set}]$, which supplies a subobject classifi[8D[K
classifier, limits/colimits, and exponentials.  
  - Objects are interpreted as subspheres (propositions), morphisms as proo[4D[K
proofs that preserve truth, and higher‑order types as presheaves of such ob[2D[K
objects.

* **Distribution monad:**  
  - $\mathsf{Prob}$ is modeled as the presheaf of real numbers in $[0,1]$. [K
 
  - The semantics of probabilistic binding (Choice) is given by convex line[4D[K
linear combinations, making SPC a *convex algebra*.

* **Meta‑theoretic results:**  
  - Preservation and progress properties hold for terms, with special care [K
taken for probabilistic branching to ensure that non‑zero probability reduc[5D[K
reducts always exist.  

Overall, the semantics shows how SPC’s type system internalizes both catego[6D[K
categorical concurrency (via Merge) and probabilistic reasoning (via Choice[6D[K
Choice), all expressed within a well‑behaved symmetric monoidal structure d[1D[K
derived from standard cartesian closed category theory.

