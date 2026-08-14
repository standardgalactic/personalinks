**Repair Defined**

A *repair operator* $\repair:\mathcal D\to\mathcal D$ is formally required [K
to satisfy three conditions:

1. **Improvement (R₁)** – The distance from the repaired state $\repair(d)$[12D[K
$\repair(d)$ to its target distinction $d^*$ cannot be larger than the orig[4D[K
original distance:
   \[
   \delta(\repair(d), d^*) \le \delta(d, d^*).
   \]

2. **Fixed‑point stability at the target (R₂)** – The distinguished state r[1D[K
remains unchanged under repair:
   \[
   \repair(d^*) = d^*.
   \]

3. **Non‑degradation when recoverability is zero (R₃)** – If no recoverabil[11D[K
recoverability exists for $d$ ($\reco(d)=0$), the operator must not map it [K
to a “better” state:
   \[
   \repair(d) \neq d^* \quad\text{whenever }\reco(d)=0.
   \]

**Admissible Repair**

A repair is called *admissible* if it preserves or improves a system’s abil[4D[K
ability to recover from future disturbances. Formally:

\[
\text{Admissibility: } V_R(\repair(d),t) \ge V_R(d,t)
\]

for every damaged state $d$ and any disturbance horizon $t$, where $V_R$ de[2D[K
denotes reachability volume (or analogous robustness metric).

**Existence of Repair**

The *Repair Existence Theorem* states that a repair operator satisfying the[3D[K
the three conditions above exists **iff** recoverability remains strictly p[1D[K
positive:

\[
\reco(d) > 0.
\]

- **Proof Sketch**:  
  - If $\repair$ is an improving mapping, it must use information recoverab[9D[K
recoverable from $d$, implying $\reco(d)>0$.  
  - Conversely, if $\reco(d)>0$, a reconstruction operator $\mathfrak{rec}$[16D[K
$\mathfrak{rec}$ (defined by the Recoverability Law) exists and can be set [K
as $\repair=\mathfrak{rec}$. The conditions R₁–R₃ then follow from properti[8D[K
properties of $\mathfrak{rec}$.

**Closure Property**

The *Repair Closure Theorem* asserts that composition of two admissible rep[3D[K
repairs is itself an admissible repair:

\[
(\repair_1 \circ \repair_2)(d) = \repair_1(\repair_2(d)),
\]

and the resulting operator retains:
- R₁ (improvement),  
- R₂ (fixed‑point stability at $d^*$), and  
- R₃ (non‑degradation when $\reco=0$).

Thus admissible repairs form a **monoid** under composition, with identity [K
being the trivial “do‑nothing” repair.

**Minimal Repair**

The *Minimal Repair Theorem* (sketch) guarantees that among all admissible [K
repairs achieving a bounded error $\epsilon = \delta(\repair(d), d^*)$, the[3D[K
there exists one that minimizes repair cost:

\[
\mathrm{Cost}(\repair, d)=\mu\bigl(\{y:\repair\text{ modifies distinction a[1D[K
at }y\}\bigr),
\]

where $\mu$ measures the set of points altered by the repair.

**Repair Conservation Law**

Admissible repair preserves historical continuity on the recoverability man[3D[K
manifold $\mathcal M_\reco$. Formally:

\[
d \;\text{and}\; \repair(d) \in \text{same connected component of }\mathcal[9D[K
}\mathcal M_\reco.
\]

**Entropy Relation (Repair–Entropy Theorem)**

For admissible repair of a subset $\Sigma \subset X$ within its superspace [K
$\Omega \supset \Sigma$, the following hold:

1. **Entropy Decrease on Damaged Region**:  
   \[
   \Delta S_\Sigma \le 0,
   \]
   reflecting that repair reduces disorder in the damaged region.

2. **Entropy Compensation**:  
   \[
   \Delta S_{\Omega\setminus\Sigma} \ge |\Delta S_\Sigma|,
   \]
   satisfying the second law of thermodynamics (Landauer’s principle, Benne[5D[K
Bennett 1982).

3. **Global Entropy Non‑decrease**:  
   \[
   \Delta S_\Omega \ge 0,
   \]
   ensuring that total system entropy does not decline.

**Interpretive Remarks**

- *Repair* is distinct from mere optimisation: it aims at restoring recover[7D[K
recoverability rather than optimizing a fixed performance metric.
- In biological healing, new structures may emerge; in scientific theory, c[1D[K
concepts can be replaced without sacrificing overall explanatory power.
- Engineering often conflates repair with self‑correction (optimisation), o[1D[K
overlooking the necessity of preserving distinguishability and system robus[5D[K
robustness.

**Related Frameworks**

The formalism builds on classic cybernetic insights:

- **Norbert Wiener’s control systems** emphasize feedback for maintaining s[1D[K
stability, aligning with the idea that repair acts as a corrective feedback[8D[K
feedback loop.
- **Arend Hintikka (1962) and W. Ross Ashby’s law of requisite variety**, a[1D[K
and **Heinz von Foerster’s cybernetic principle of self‑organization**, sim[3D[K
similarly treat repair as an essential component for preserving information[11D[K
information content and system adaptability.

These connections underscore that the notion of repair is not merely a prag[4D[K
pragmatic fix but a fundamental aspect of any evolving, self‑maintaining sy[2D[K
system.

