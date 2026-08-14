**Preserving Future Options – The Core Idea**

The central thrust of this chapter is that agents preserve *future options*[8D[K
options* by maintaining admissible futures. In other words, an agent’s beha[4D[K
behavior should expand the set of worlds where further choices remain avail[5D[K
available rather than contract it.

---

### 1. Preference Orderings and Admissibility Potential  

**Key Result (Pref Emergence Theorem – \cref{thm:pref-emergence}):**  
Preference orderings are not independent constructs; they emerge from the *[1D[K
*admissibility potential* \(\Phi_A\) defined for a given environment. This [K
means that what an agent prefers is fundamentally shaped by how much it can[3D[K
can keep future worlds admissible.

---

### 2. Preference‑Directed Motion  

When \(\Phi_A\) exists, agents move in direction of its gradient:

**Gradient Pref Theorem – \cref{thm:gradient-pref}:**  
\[
\dot{x} = \nabla\Phi_A
\]
where \(x\) represents the agent’s state. This formalizes that agents act t[1D[K
to maximize their admissibility potential, analogous to maximizing expected[8D[K
expected utility in traditional frameworks but grounded directly in future‑[7D[K
future‑option preservation.

---

### 3. Reward vs. Future Admissibility Divergence  

**Reward–Admissibility Divergence Theorem – \cref{thm:reward-divergence}:**[31D[K
\cref{thm:reward-divergence}:**  
Immediate rewards and the preservation of admissible futures can diverge. A[1D[K
A policy that maximizes short‑term reward may reduce future options, highli[6D[K
highlighting a fundamental limitation in reward‑maximizing agents.

---

### 4. Preference Curvature and Decision Bottlenecks  

**Pref Curvature Theorem – \cref{thm:pref-curvature}:**  
Preference curvature identifies where decision bottlenecks arise by linking[7D[K
linking the shape of preference fields to admissibility curvature. This bri[3D[K
bridges local choice behavior with global future‑option preservation.

---

### 5. Collective Preference Fields and Interference  

**Pref Interference Theorem – \cref{thm:pref-interference}:**  
Collective preference fields become generatively admissible when individual[10D[K
individual preference gradients are largely aligned, ensuring that the grou[4D[K
group’s overall direction preserves future options rather than conflicting [K
with them.

---

### 6. Generative Admissibility and Boundary Flux  

The sign condition for a field to be *generatively admissible* is:

\[
\mathcal{L}_{\nabla\Phi_A}\Vol(\adm) \ge 0
\]

where \(\vol(\adm)\) denotes the volume of admissible futures. This transla[7D[K
translates into the Boundary‑Flux Theorem – a locally computable condition [K
that measures whether outward flux across the admissibility boundary preser[6D[K
preserves future options:

\[
\frac{d}{dt}\Vol(\mathcal{A}_t)=
\int_{\partial\mathcal{A}_t}\mathbf{p}\cdot\mathbf{n}\, dS
\]

with \(\mathbf{p} = -\nabla U\) the preference flow. If this flux is non‑ne[6D[K
non‑negative, future options are being conserved.

---

### 7. Exercises and Extensions  

- **Exercise on Reward–Admissibility Divergence:**  
Construct a two‑state example with reachability dynamics to illustrate how [K
immediate reward can diverge from preserving admissible futures. Compute \([2D[K
\(\Phi_A(x_1)\) and \(\Phi_A(x_2)\).

- **RL Extension:** Propose an RL objective that incorporates both reward \[1D[K
\(R\) and \(\Phi_A\). Discuss practical challenges in estimating \(\Phi_A\)[10D[K
\(\Phi_A\) from data.

- **Preference Interference Theorem Proof:** Show that if \(\nabla\Phi_i \c[2D[K
\cdot \nabla\Phi_j < 0\) for all distinct pairs, the collective field canno[5D[K
cannot be generatively admissible unless some weight \(w_i = 0\).

- **Governance Application:** Apply the Preference–Admissibility Equivalenc[10D[K
Equivalence Theorem to institutional governance dynamics. Identify conditio[8D[K
conditions where individual members have generatively admissible preference[10D[K
preferences yet the institution fails to do so.

---

### Summary

This chapter establishes that preserving future options is captured by a *a[2D[K
*admissibility potential* \(\Phi_A\) and its gradient‑driven motion, reward[6D[K
rewarding immediate gains at the cost of reduced future choices. By linking[7D[K
linking preference curvature, collective alignment, and boundary flux condi[5D[K
conditions, it provides both theoretical and practical tools for designing [K
agents (or institutions) that truly extend their own options rather than me[2D[K
merely optimizing short‑term outcomes.

---

*Note to readers:* The equations and references (\(\cref{}\)) are placehold[9D[K
placeholders intended for a LaTeX document. They will be replaced with actu[4D[K
actual citations once the full manuscript is finalized.
