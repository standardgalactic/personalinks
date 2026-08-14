**Admissibility and Feasibility – A Conceptual Overview**

In many dynamical‑systems settings—control theory, planning under uncertain[9D[K
uncertainty, or even economic modeling—the notions of *admissibility* and *[1D[K
*feasibility* are not nested on the same dimension.  

- **Feasibility** asks whether a particular state (or trajectory) can be re[2D[K
reached at all from an initial condition given time and system dynamics. It[2D[K
It is purely a question of existence: “Is there any way to get here?”  
- **Admissibility**, however, adds a *future‑reachability* constraint: even[4D[K
even if we could reach the candidate state now, does it preserve enough fut[3D[K
future options? This notion depends on how much volume of reachable states [K
remains after we extend forward in time.

The formal construction below separates these two ideas entirely:

---

### 1. Reachability Volume Function  

For a given state \(y\in X\) and elapsed time \(t\), define the **future re[2D[K
reachability function**  

\[
F(y,t,\tau)=V_R(y,t,t+\tau),
\]

where \(V_R(\cdot)\) denotes the *reachability volume*—the amount of future[6D[K
future state space that can be reached from a point in \(X\) within an addi[4D[K
additional \(\tau>0\) time units. This function is assumed to be continuous[10D[K
continuous for all admissible \(t,\tau>0\).

---

### 2. Admissibility Threshold  

Fix two positive constants: a *fraction* \(\alpha\in(0,1)\) and a horizon l[1D[K
length \(\tau>0\). A state \(y\) is called **\((\alpha,\tau)\)-admissible**[32D[K
**\((\alpha,\tau)\)-admissible** from an initial condition \(x\) at time \([2D[K
\(t_0\) if:

1. \(y\) lies in the reachable set from \(x\) over the interval \([t_0,t]\)[11D[K
\([t_0,t]\): \(y\in\operatorname{reach}(x,t_0,t)\), and  
2. The future reachability volume preserved after extending another \(\tau\[7D[K
\(\tau\) units of time meets the threshold:

   \[
   F(y,t,\tau) \ge \alpha\; V_R(x,t_0,t).
   \]

In words, reaching \(y\) does not “extract” more than a fraction \((1-\alph[10D[K
\((1-\alpha)\) of the future reachability volume that was available when we[2D[K
we started.

---

### 3. The Admissibility Manifold  

The **admissibility manifold** associated with \((x,t_0)\) and parameters \[1D[K
\((\alpha,\tau)\) is defined as

\[
\boxed{\;
\adm(x,t_0)=
\overline{\{
y \in \operatorname{reach}(x,t_0,t)
    : F(y,t,\tau) \ge \alpha V_R(x,t_0,t)
\}}
\;}
\]

- The closure (denoted by the over‑bar) guarantees that limit points on the[3D[K
the boundary are included, reflecting the fact that a trajectory may asympt[6D[K
asymptotically approach an admissible state.
- By construction,  

  \[
  \adm(x,t_0)\subseteq \operatorname{reach}(x,t_0,t),
  \]

  meaning every point in the manifold is *feasible*, but not necessarily *a[2D[K
*admissible*.

---

### 4. Interpretation of the Geometry  

Visually (see Figure \(\ref{fig:adm-manifold}\)):

- The **reachable set** for a finite time interval is colored teal.
- Points inside the admissibility manifold are shaded gold and represent “f[2D[K
“future‑preserving” states—reaching them does not collapse future possibili[9D[K
possibilities below fraction \(\alpha\) of current reachability volume.
- States that lie in the reachable region but *outside* the gold set (extra[6D[K
(extractive points) have trajectories where \(F(y,t,\tau)<\alpha V_R(x,t_0,[10D[K
V_R(x,t_0,t)\); these are called **extractive** because they “sacrifice” a [K
disproportionate amount of future potential.

---

### 5. Existence Guarantees  

The formal guarantee that the admissibility manifold is non‑empty when both[4D[K
both feasibility and a positive reachable volume exist follows from continu[7D[K
continuity arguments:

> **Admissibility Existence Theorem**:  
> For a compact dynamical system \((X,\Phi)\) with continuous \(F(y,t,\tau)[13D[K
\(F(y,t,\tau)\) for all \(t,\tau>0\), if the reachable set is non‑empty (\([3D[K
(\(\operatorname{reach}(x,t_0,t)\neq\varnothing\)) and has positive reachab[7D[K
reachability volume (\(V_R(x,t_0,t)>0\)), then there exists at least one st[2D[K
state in the admissibility manifold for any choice \(\alpha\in(0,1),\tau>0\[24D[K
\(\alpha\in(0,1),\tau>0\).

*Proof Sketch*:  
- Since \(F(y,t,\tau)\) attains a maximum on the compact reachable set, let[3D[K
let \(y^*\) be a point where this supremum is achieved: \(V_R(y^*,t,\tau)=V[19D[K
\(V_R(y^*,t,\tau)=V^*>0\).  
- Because \(\alpha V_R(x,t_0,t)>0\) (by assumption), we have \(V^* > 0\) au[2D[K
automatically implies that the admissibility condition holds for some \(y\)[5D[K
\(y\) inside the reachable set. Hence the manifold is non‑empty.

---

### 6. Why Not Confuse Admissibility with Utility?  

A common misreading equates “admissible” with “preferred by a rational agen[4D[K
agent.” This conflates *structural* future reachability (a property of the [K
system’s dynamics) with *subjective* utility or preference satisfaction, wh[2D[K
which is independent:

- An admissible state may be **disliked** if it leads to sub‑optimal outcom[6D[K
outcomes for an individual whose preferences are not aligned with preservin[9D[K
preserving future possibilities.
- Conversely, a trajectory that maximizes immediate reward could still be i[1D[K
inadmissible because it dramatically reduces the volume of reachable states[6D[K
states beyond time \(\tau\).

Thus, admissibility captures *future viability*, not merely utility.

---

### 7. Why Not Reduce Admissibility to “Survival”?  

Some might think any surviving state is automatically admissible: after all[3D[K
all, a system exists if and only if it can at least persist for one time un[2D[K
unit. However:

- Survival alone does **not** guarantee that future trajectories retain eno[3D[K
enough open volume. A trajectory could survive indefinitely but become *ext[4D[K
*extractive*—it narrows the reachable space so much that \(F(y,t,\tau)<\alp[18D[K
\(F(y,t,\tau)<\alpha V_R(x,t_0,t)\) for all larger \(\tau\).
- The admissibility manifold isolates those states whose future remains **n[3D[K
**non‑extractive**, preserving a fraction \(\alpha\) of current reachabilit[11D[K
reachability.

---

### 8. Extending the Manifold Conceptually  

The formal definition presented here is a stepping stone toward richer geom[4D[K
geometric structures:

- In **Chapter \(\ref{ch:geometry-futures}\)**, curvature and topological f[1D[K
features (e.g., winding number or genus) are added to the volume measure.
- This leads to the question of whether admissibility can be derived as an [K
*intrinsic strategic criterion* (reflecting rational expectations about fut[3D[K
future payoffs) rather than a value judgment imposed ex‑ante.

---

### 9. Summary  

The **Admissibility Manifold** \(\adm(x,t_0)\) provides a rigorous, agent‑a[7D[K
agent‑agnostic partition of the reachable set that respects structural cons[4D[K
constraints on *future possibility*. It separates what can be reached from [K
what remains open for future development, offering both a geometric intuiti[7D[K
intuition (via Figure \(\ref{fig:adm-manifold}\)) and an existence guarante[8D[K
guarantee through the Admissibility Existence Theorem. This distinction is [K
crucial when:

- Designing robust control policies that avoid “future‑contracting” states.[7D[K
states.
- Analyzing economic or strategic settings where preserving long‑ter[8D[K
long‑term viability matters more than immediate utility.

By formalizing admissibility in this way, we can systematically study how t[1D[K
trajectories evolve not only into the present but also into a meaningful po[2D[K
portion of the future state space.

