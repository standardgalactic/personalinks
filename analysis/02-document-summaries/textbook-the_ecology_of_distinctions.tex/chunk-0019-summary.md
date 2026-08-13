**Admissibility Volume and Entropy**

*Definition – Admissibility Volume.*  
For a given future state set \(\mathcal{A}\subset S\) (the space of all pos[3D[K
possible future states), the admissibility volume is  

\[
V_A(\mathcal A)=\mu(R_t\cap\mathcal A),
\]

where \(R_t\) denotes the reachable region after time \(t\).  
- Large \(V_A\) ⇒ many viable futures → high flexibility.  
- Small \(V_A\) ⇒ few or no viable futures → fragility.  
- Vanishing \(V_A\) (i.e., \(V_A\to0\)) signals collapse of viability.

*Monotonicity Property.*  

If \(\mathcal A_1\subseteq\mathcal A_2\), then the admissibility volume can[3D[K
cannot increase:

\[
V_A(\mathcal A_1)\le V_A(\mathcal A_2).
\]

**Proof Sketch.**  
Because \(R_t\) is a subset of reachable states, intersecting with a larger[6D[K
larger set can only add points to \(R_t\cap\mathcal A\). Hence the measure [K
(volume) cannot drop.

---

**Admissibility Entropy**

Volume alone depends on dimension and units; entropy provides an invariant [K
measure:

*Definition – Admissibility Entropy.*  
The admissibility entropy is  

\[
S_A=\log V_A.
\]

*Interpretation.*  
\(S_A\) counts the “effective number” of distinct admissible futures (analo[6D[K
(analogous to thermodynamic entropy).

*Additivity for Independent Systems.*  

If \(\mathcal A_1\) and \(\mathcal A_2\) are independent, then  

\[
V_A(\mathcal A_1\times\mathcal A_2)=V_A(\mathcal A_1)\,V_A(\mathcal A_2),
\]

so  

\[
S_A(\mathcal A_1\times\mathcal A_2)=\log V_A(\mathcal A_1)+\log V_A(\mathca[11D[K
V_A(\mathcal A_2)
= S_A(\mathcal A_1)+S_A(\mathcal A_2).
\]

Thus entropy behaves like a conserved quantity (analogous to reachability/t[14D[K
reachability/thermodynamic entropy).

---

**Local Admissibility Structure**

Global volume ignores the fine‑grained geometry of admissibility; we need s[1D[K
sensitivity near states:

*Definition – Admissibility Potential.*  
For a state \(x\),

\[
\Psi(x)=-\log V_A(x),
\]

where \(V_A(x)\) is the local admissible volume in a neighbourhood of \(x\)[5D[K
\(x\).

*Interpretation.*  

- Large \(\Psi\) ⇒ future possibilities are scarce (high fragility).  
- Small \(\Psi\) ⇒ many futures remain viable.

---

**Admissibility Curvature**

Curvature quantifies how quickly admissibility changes under small perturba[8D[K
perturbations:

*Definition – Admissibility Curvature Tensor.*  
\[
K_{ij}=\nabla_i\nabla_j\Psi.
\]

Equivalently, \(K_{ij}= *\,\nabla_i\nabla_j(\log V_A)\); it is the Hessian [K
of \(\Psi\).

*Definition – Scalar Admissibility Curvature.*  
\[
K_A = g^{ij}K_{ij},
\]

where \(g^{ij}\) is the metric (inner product on state space).

---

**Interpretation of Curvature**

- **Positive curvature (\(K_{ij}\ge0\))** ⇒ locally convex \(\Psi\) → futur[5D[K
future possibility contracts.  
  *Proof.* Convexity of a concave function means nearby states have smaller[7D[K
smaller admissible volume.

- **Negative curvature (\(K_{ij}\le0\))** ⇒ locally concave \(\Psi\) → futu[4D[K
future possibility expands.  

Hence, positive curvature signals fragility; negative curvature signals gen[3D[K
generativity.

---

**Boundary Geometry**

The topology of \(\mathcal A\) is governed by its boundary:

*Definition – Admissibility Boundary.*  
\[
\partial\mathcal A=\{x\in S : x\notin\mathcal A,\text{ but }\exists p\in\ma[7D[K
p\in\mathcal A\text{ with }|p-x|\to0\}.
\]

*Near‑boundary distance.*

*Definition – Boundary Distance.*  
\[
d_A(x)=\min_{y\in\partial\mathcal A}|x-y|.
\]

*Proposition.* Near the boundary, small perturbations may leave \(\mathcal [K
A\). Larger \(d_A(x)\) means a larger admissible neighbourhood.

---

**Admissibility Gradient**

The gradient points in the direction of maximal increase of volume:

*Definition – Admissibility Gradient.*  
\[
\nabla V_A.
\]

*Proposition.* It maximizes local growth of admissible volume (first‑order [K
measure of robustness).

*Proof Sketch.* By multivariable calculus, \(\nabla\) gives the direction o[1D[K
of steepest ascent for a differentiable scalar field.

---

**Generative Admissibility**

The principle is not merely preservation but expansion:

*Definition – Generative Admissibility.*  
A system is generatively admissible if  

\[
\frac{dV_A}{dt}\ge0.
\]

This implies monotonic growth of admissibility entropy (\(\frac{dS_A}{dt}\g[20D[K
(\(\frac{dS_A}{dt}\ge0\)).

---

**Collapse Condition**

Opposite regime:

*Definition – Admissibility Collapse.*  
\(V_A(t)\to0\) signals complete loss of viable futures.

*Theorem (Collapse Theorem).* If \(V_A(t)\to0\), then  

\[
S_A(t)=\log V_A(t)\to -\infty,
\]

indicating total collapse of future possibility.

---

**Admissibility vs. Reachability**

- *Reachability:* “Which futures can be reached?”  
- *Admissibility:* “Which futures should remain reachable?”

We define **admissible reachability volume**:  

\[
V_{AR}=\mu(R_t\cap\mathcal A).
\]

This metric captures the subset of reachable states that are already admiss[6D[K
admissible, emphasizing preservation rather than mere attainability.

---

**Summary**

The framework integrates:

1. **Volume & Entropy** – global and invariant measures of viability.  
2. **Curvature** – local sensitivity to fragility vs. generativity.  
3. **Boundary Distance** – robustness near the edge of \(\mathcal A\).  
4. **Gradient** – direction for generative motion.  
5. **Generative Condition** – ensures future possibility does not shrink (m[2D[K
(monotonic entropy increase).  
6. **Collapse** – when \(V_A\) vanishes, indicating inevitable breakdown.

These concepts collectively allow us to characterize the stability and dyna[4D[K
dynamical behaviour of control systems in terms of their viability rather t[1D[K
than just reachability.

