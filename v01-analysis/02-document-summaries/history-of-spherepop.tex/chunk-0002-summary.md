**Appendix F – Confluence, Divergence, and Regret as Properties of Historie[8D[K
Histories**

---

### Overview

In Spherepop we treat *histories*—finite sequences of irreversible events—a[8D[K
events—as the fundamental carriers of meaning.  Unlike conventional state‑o[7D[K
state‑oriented models that view a “failure” as an error to be undone, here [K
correctness is defined by how histories relate to one another rather than b[1D[K
by any single terminal configuration.

Below are formal definitions for **confluence**, **divergence**, and **regr[6D[K
**regret** on the category $\mathcal{H}$ of histories.  The purpose is to c[1D[K
characterize *correctness* (or non‑failure) in terms that avoid backtrackin[11D[K
backtracking, normalization, or error states altogether.

---

#### 1. Basic Notions

- **History**: A finite sequence of events $h = e_0e_1\ldots e_n$ where eac[3D[K
each event belongs to a predefined set $\mathcal{E} = \{\text{Pop}, \text{C[7D[K
\text{Collapse}, \text{Refusal}, \text{Binding}\}$.
- **Option Space at Horizon $k$**: For a history $h$, the *induced option s[1D[K
space* is
  $$O_h^k = \bigcup_{e\in h[:k]} O_e,$$
  where $O_e$ denotes the set of admissible extensions (values, labels) tha[3D[K
that could follow event $e$.
- **Extensional Equivalence at Horizon $k$$:**
  Two histories $h_1$ and $h_2$ are extensionally equivalent up to horizon [K
\(k\) if
  $$h_1[:k] = h_2[:k] \quad\text{and}\quad O_{h_1}^k = O_{h_2}^k.$$
  We write this as  
  $$h_1 \approx_k h_2.$$

---

#### 2. Confluence

A family of histories $\mathcal{H}_i = \{h_i\}_{i\in I}$ is **confluent** w[1D[K
with respect to a *collapse policy* $C$ if there exists a history $h_c$ suc[3D[K
such that for every $h_i\in\mathcal{H}_i$
$$h_i \cdot C \approx_0 h_c.$$
- **Interpretation**: Confluence does **not** require the histories to be i[1D[K
identical; it only requires that an explicit *collapse* can make them indis[5D[K
indistinguishable at horizon 0.  
- **No “backtracking”**: The collapse is a deliberate, irreversible act (e.[3D[K
(e.g., applying a specific binding rule), not a recovery from error.

---

#### 3. Divergence

A set of histories $\{h_1,\dots,h_m\}$ is said to be **divergent** if no co[2D[K
collapse policy $C$ exists such that
$$h_i \cdot C \approx_k h_c$$
for any horizon \(k\) and common suffix $h_c$.  
- **Why it matters**: Divergence reflects an inherent incompatibility of co[2D[K
commitments—some futures are incompatible regardless of how we compress the[3D[K
them later. It is a descriptive property, not a fault.

---

#### 4. Regret

A single history $h = e_0e_1\ldots e_n$ exhibits **regret** if there exists[6D[K
exists a prefix $p = e_0\ldots e_k$ and an alternative reachable path $h' =[1D[K
= p \cdot e'_k'\dots e'_m'$ satisfying
$$O_h^{n} \prec O_{h'}^{m}.$$
- **Formal condition**: There are events $\{e'_{j}\}$ that could follow the[3D[K
the regret‑inducing segment, expanding the admissible option space strictly[8D[K
strictly beyond what $h$ can achieve.
- **Regret is not an error**; it merely signals that a sequence of irrevers[8D[K
irreversible commitments has limited future flexibility.

---

#### 5. Correctness and Failure in This Framework

- **Correctness**: A history is deemed “correct” when its remaining option [K
space aligns with the intended goals (e.g., achieving maximal expressivity [K
without unnecessary constraints).
- **Failure (Divergence)**: Not all histories are failures; divergence simp[4D[K
simply indicates that no collapse can reconcile conflicting commitments, re[2D[K
reflecting a structural limitation rather than a bug.
- **Regret**: Recognizing regret is part of evaluation—*how* we have constr[6D[K
constrained the future matters more than *whether* we made an irreversible [K
decision.

---

### Intended Use

By shifting correctness from being tied to individual states (which may be [K
unattainable) to being defined by relationships among histories, Spherepop:[10D[K
Spherepop:

1. **Avoids backtracking** – No need to revert or “undo” actions; instead, [K
we acknowledge divergence.
2. **Eliminates error handling** – Regret is a normal state of progressive [K
commitment, not an anomaly.
3. **Facilitates learning and adaptation** – Systems can improve by selecti[7D[K
selecting paths that preserve as much future optionality as possible.

---

### References

- Wittgenstein 1953, *Philosophical Investigations* (lexical foundations).
- Church 1936, *An unsolvable problem of elementary number theory* (complet[8D[K
(completeness considerations).
- Turing 1936, *On computable numbers…* (algorithmic basis for events).

These references underpin the notion that historical transformations—rather[22D[K
transformations—rather than static states—are the meaningful carriers of me[2D[K
meaning in Spherepop.

