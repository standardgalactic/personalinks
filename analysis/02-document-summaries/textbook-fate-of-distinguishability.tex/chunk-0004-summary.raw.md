**Objects as Stable Fate Regions**

*What this chapter shows*

1. **Fate‑Uniformity is the primitive property of an object.**  
   An *object* (relative to a given admissible fate region and operator fam[3D[K
family) is defined as a connected, open subset \(U\subseteq\distPairs\) who[3D[K
whose images under the fate map are constant:
   \[
   \forall p,q\in U,\;\fateMap(p)=\fateMap(q).
   \]
   Hence every point in an object shares the same survival‑ratio, repair‑ef[9D[K
repair‑efficiency, collapse status and transport distances – i.e. it is a “[1D[K
“same‑fate” block.

2. **Stability requires interior fate placement.**  
   For an object to survive perturbations (the usual notion of stability), [K
its entire fate profile must lie inside the admissible region:
   \[
   \fateMap(U)\subseteq\operatorname{int}(\admRegion).
   \]
   If it were on the boundary, arbitrarily small changes could push it out.[4D[K
out.

3. **Boundaries are singular strata.**  
   By definition a fate‑singularity (the set where the fate map is disconti[8D[K
discontinuous) separates stable from unstable regions. Consequently every o[1D[K
object boundary lies in the *singular set* \(\sset\).

4. **Objecthood as an ecological achievement, not primitive.**  
   Because objects emerge only when a region of uniform fate also satisfies[9D[K
satisfies the stability condition, they are best understood as outcomes of [K
ecological (operator‑family) dynamics rather than fundamental ontological e[1D[K
entities.

---

### Formal Definitions

| Symbol | Meaning |
|---|---|
| \(\fateMap:\distPairs\to\fateSpace\) | Maps each distinction pair to its [K
fate profile in the abstract space of possible futures. |
| \(\fateUnif(U)\) | \(U\) is *fate‑uniform* if \(\forall p,q\in U,\;\fateM[10D[K
U,\;\fateMap(p)=\fateMap(q)\). |
| \(\admRegion\) | A closed admissible fate region (e.g., the set of future[6D[K
futures compatible with some survival constraints and repair efficiency thr[3D[K
thresholds). |
| \(\transfam=\{T_i\}\) | An admissible operator family satisfying \(T^*(\a[8D[K
\(T^*(\admRegion)\subseteq\admRegion\) for every \(T_i\). |

---

### The Object Stability Theorem

**Statement.**  
Let \(\admRegion\) be a closed, admissible fate region and let \(\transfam\[12D[K
\(\transfam\) be an admissible operator family such that each transformatio[13D[K
transformation preserves the admissibility (i.e., \(T^*(\admRegion)\subsete[25D[K
\(T^*(\admRegion)\subseteq\admRegion\)). Then a connected \(\fateUnif\) sub[3D[K
subset \(U\subset\distPairs\) is *stable* under all perturbations in \(\tra[6D[K
\(\transfam\) **iff**
\[
\fateMap(U)\subseteq\operatorname{int}(\admRegion).
\]

**Proof Sketch.**

- **(⇒) Stability ⇒ interior placement:**  
  Assume \(U\) is stable but its fate profile lies on the boundary of \(\ad[5D[K
\(\admRegion\). Because \(\admRegion\) is closed, any point in the closure [K
can be approached from inside by small perturbations that keep it admissibl[9D[K
admissible. By continuity of \(\fateMap\) and the fact that points arbitrar[8D[K
arbitrarily close to \(\partial\admRegion\) map out‑of‑region, there exist [K
\(T_\varepsilon\in\transfam\) with sufficiently small \(\varepsilon>0\) suc[3D[K
such that  
  \[
  T_\varepsilon^*(\fateMap(U))\notin\admRegion,
  \]  
  contradicting stability.

- **(⇐) Interior placement ⇒ stability:**  
  If \(\fateMap(U)\subseteq\operatorname{int}(\admRegion)\), then for any \[1D[K
\(T_\varepsilon\) with small support, the pull‑back of each fate class insi[4D[K
inside \(U\) stays within the interior. Hence no perturbation can push a pa[2D[K
pair out of \(\admRegion\); the region is stable.

---

### Consequences

1. **Objects as emergent outcomes** – They are not primitive but arise from[4D[K
from the interplay between *fate uniformity* (the geometric condition) and [K
*stability* (the dynamical condition).

2. **Boundary = fate singularity** – The edge of every object lies in \(\ss[5D[K
\(\sset\), confirming that the “edge” is a manifestation of the underlying [K
discontinuity of the fate map.

3. **Object identity without physics‑intrinsic categories** – By grounding [K
objects solely on fate geometry, we avoid positing an independent ontologic[9D[K
ontological status for objects; instead, they are recognitions of stable re[2D[K
regions in the fate landscape.

---

### Summary

- **Fate‑uniformity** captures the homogeneity that makes something a candi[5D[K
candidate object.  
- **Stability (interior fate placement)** ensures that this uniform block c[1D[K
cannot be perturbed into an unphysical region by admissible dynamics.  
- **Object boundaries** are precisely those points where the fate map cease[5D[K
ceases to be continuous, i.e., singular strata.

Thus objects emerge as *stable fate regions*—the familiar entities of scien[5D[K
science and everyday life—that we can understand fully in terms of the geom[4D[K
geometry defined by the continuation action \(\contAction[\fateTraj]\) on f[1D[K
fate trajectories.

