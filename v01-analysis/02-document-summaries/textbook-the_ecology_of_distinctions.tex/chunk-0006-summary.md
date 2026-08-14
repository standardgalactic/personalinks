**Admissibility Manifold – A Formal Treatment**

---

### 1.  What the manifold is

For a given initial state \(x\) at time \(t_{0}\) and a later horizon time [K
\(t> t_{0}\),

* **Reachability set** \(\reach(x,t)\) = all states reachable from \(x\) in[2D[K
in the interval \([t_{0},t]\).

* **Future‑reachability function**  
  \[
    F(y,t,\tau)=V_R\bigl(y,t,t+\tau\bigr)
  \]
  measures how much volume of future reachability can be obtained starting [K
at state \(y\) after an additional time interval \(\tau>0\).

* **Threshold‑admissibility**  
  Fix a fraction \(\alpha\in(0,1)\) and a horizon \(\tau>0\). A state \(y\i[5D[K
\(y\in\reach(x,t)\) is called \((\alpha,\tau)\)-admissible if
  \[
    F(y,t,\tau)\;\ge\;\alpha\;V_R(x,t_{0},t).
  \]

* **Admissibility manifold**  
  The admissibility manifold (or “future‑reachability surface”) is the clos[4D[K
closure of all such states:
  \[
    \adm(x,t)=\overline{
      \{\,y\in\reach(x,t):\;F(y,t,\tau)\ge\alpha V_R(x,t_{0},t)\,\}}.
  \]
  Geometrically it separates *admissible* (future‑rich) states from the res[3D[K
rest of the reachable set.

---

### 2.  Why we need this manifold

| Misreading | What it confuses with | Why it fails |
|------------|----------------------|--------------|
| **Admissibility = utility** | Preference satisfaction by a rational agent[5D[K
agent | Admissibility is defined solely on *future reachability*; an agent [K
may prefer a trajectory that looks inadmissible because of other values (e.[3D[K
(e.g., safety, cost). The manifold quantifies the volume that remains open [K
for future use, not any personal payoff. |
| **Admissibility = survival** | “Anything that exists is admissible” | Sur[3D[K
Survival alone does not guarantee future openness. A system could survive i[1D[K
indefinitely along a trajectory that quickly collapses its reachable set (e[2D[K
(e.g., entering a deep attractor). Admissibility distinguishes between *hea[4D[K
*healthy* and *pathological* persistence by measuring the retained volume o[1D[K
of futures, not mere existence. |

Thus the manifold is **independent** of any agent’s preferences or utility [K
functions.

---

### 3.  Existence Theorem (Proof Sketch)

Let \((X,\Phi)\) be a compact dynamical system with continuous future‑reach[12D[K
future‑reachability \(F(\cdot,t,\tau)\).

* Because \(F\) is continuous on the compact set \(\reach(x,t)\), it attain[6D[K
attains its maximum at some state \(y^{*}\in\reach(x,t)\).  
  Set \(V^{*}=F(y^{*},t,\tau)\).

* Since we are in a bounded system, there exists a reachable trajectory tha[3D[K
that does **not** vanish completely: \(\max V_R >0\) for any non‑empty reac[4D[K
reachability set. Consequently \(V^{*}\ge0\).  

* If the total reachable volume at time \(t\) is \(V_R(x,t_{0},t)>0\), we c[1D[K
can choose a small enough threshold, e.g.,  
  \(\alpha < V^{*}/V_R(x,t_{0},t)\), so that \(F(y^{*},t,\tau)\ge\alpha V_R[3D[K
V_R(x,t_{0},t)\).  

Hence there exists at least one state inside the reachability set satisfyin[9D[K
satisfying the admissibility condition, proving \(\adm(x,t)\neq\varnothing\[27D[K
\(\adm(x,t)\neq\varnothing\) whenever \(\reach(x,t)\neq\varnothing\) and \([2D[K
\(V_R>0\).

---

### 4.  Interpretation via Future Reachability

* **Extractive vs. generative trajectories** – If a state lies on the bound[5D[K
boundary of \(\adm\) but is not in its interior, reaching it “extracts” fut[3D[K
future possibility beyond the threshold; such states are called *extractive[11D[K
*extractive*.  
  The figure (Fig.\ref{fig:adm-manifold}) illustrates that only those point[5D[K
points inside the gold‑colored admissibility manifold guarantee a future re[2D[K
reachable volume at least \(\alpha\) of what was initially available.

* **Metric for cost** – When an agent prefers inadmissible states, the “cos[4D[K
“cost” is precisely how much of the retained future reachability (\(F(y,t,\[10D[K
(\(F(y,t,\tau)\)) they forfeit by choosing such a trajectory. This cost can[3D[K
can be measured and incorporated into multi‑stage decision models (see Chap[4D[K
Chapter \ref{ch:geometry-futures}).

---

### 5.  Next Steps

* **Projection–Admissibility Gap Theorem** – Shows that a naïve feasibility[11D[K
feasibility check discards the volume of futures captured by \(\adm\) but r[1D[K
retains spurious constraints, leading to sub‑optimal long‑term plans.

* **Geometry and Topology of Futures** – Extends the manifold into higher‑o[8D[K
higher‑order invariants (curvature, topology) so that preservation criteria[8D[K
criteria can be derived as strategic outcomes rather than arbitrary value j[1D[K
judgments.

---

### 6.  References & Figures

| Item | Location |
|------|-----------|
| Formal definitions of \(F\) and \(\adm\) | Section 14.1–2 |
| Admissibility Existence Theorem proof | Section 14.3, Remark 14.4 |
| Visual illustration (Fig.\ref{fig:adm-manifold}) | Section 14.5 |
| Related cost analysis | Chapter \ref{ch:geometry-futures} |

--- 

**Key Take‑away:** The admissibility manifold is a rigorously defined subse[5D[K
subset of reachable states that preserves at least a fraction \(\alpha\) of[2D[K
of the original future reachability volume. It provides a principled, prefe[5D[K
preference‑independent criterion for distinguishing “future‑rich” from “ext[4D[K
“extractive” trajectories and opens the door to measuring long‑term cost in[2D[K
in dynamical systems.

