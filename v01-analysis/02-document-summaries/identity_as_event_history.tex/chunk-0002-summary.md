**Projected Identity in Spherepop**

The core idea behind projected identity in the Spherepop framework is that [K
objects are identified not by their raw trajectories through possibility‑sp[14D[K
possibility‑space, but rather by the *history* (the sequence of committed e[1D[K
events) they project onto a canonical path category \(\PathCat\). This reso[4D[K
resolves the tension between:

1. **Irreversibility** – In an irreversible system, many different past his[3D[K
histories can lead to the same present state.
2. **Informational poverty** – The present alone does not uniquely determin[8D[K
determine the full history.

---

### 1. Formal Setting

- **Category of Admissible Trajectories \(\mathcal{T}\):**  
  - *Objects*: Spherepop states \((\Omega_t, H_t)\), where \(\Omega_t\) is [K
the current option set and \(H_t\) is the accumulated event word.
  - *Morphisms* (irreversible extensions): A morphism from \((\Omega_t, H_t[3D[K
H_t)\) to \((\Omega_{t'}, H_{t'})\) exists iff  
    - \(\Omega_{t'} \subseteq \Omega_t\),  
    - \(H_{t'} = H_t \cdot w\) for some non‑empty word \(w\), and the exten[5D[K
extension satisfies all axioms of Section \(\ref{sec:possibility-preimage}\[41D[K
Section \(\ref{sec:possibility-preimage}\).

  No non‑trivial isomorphisms exist because \(\Omega\) can shrink only whil[4D[K
while \(H\) grows, preventing reversal.

- **History Projection Functor**  
  \[
    \Pi_{\mathrm{hist}} : \mathcal{T} \longrightarrow \PathCat
  \]
  maps each state to its event word and each extension morphism to the corr[4D[K
corresponding prefix in \(\PathCat\). Functoriality follows from concatenat[10D[K
concatenation of extensions matching concatenation of event words.

---

### 2. Definition of Projected Identity

**Definition (Projected identity):**  
Two terminal states \((\Omega_k, H_k)\) and \((\Omega_k', H_k')\) are *Sphe[5D[K
*Spherepop‑identical* iff their projected histories coincide:
\[
\Pi_{\mathrm{hist}}(\tau) = \Pi_{\mathrm{hist}}(\tau').
\]
Thus identity is defined by the equivalence classes of trajectories under t[1D[K
this history projection, not directly on the trajectories themselves.

**Definition (Trajectory Equivalence):**  
For \(\tau, \tau' \in \mathcal{T}\),
\[
\tau \sim \tau' \;\Longleftrightarrow\; \Pi_{\mathrm{hist}}(\tau) = \Pi_{\m[7D[K
\Pi_{\mathrm{hist}}(\tau').
\]
Objects are equivalence classes \([\tau]\); the event word is the minimal c[1D[K
complete invariant, preserving all identity‑relevant distinctions while dis[3D[K
discarding irrelevant preimage information.

---

### 3. Compatibility with Normal Forms

The projected identity reduces to the earlier normalised form when historie[8D[K
histories are already canonical:

- Let \(G_X\) be the ancestral event graph for a trajectory \(\tau\), and l[1D[K
let  
  \((\mathrm{spherepop}(X))_{\text{nf}}\) be its linearisation via Section [8D[K
Section \(\ref{sec:normalization}\).  
- Then projected identity coincides with:
\[
X \equiv Y \;\Longleftrightarrow\; (\mathrm{spherepop}(X))_{\text{nf}} = (\[2D[K
(\mathrm{spherepop}(Y))_{\text{nf}}.
\]

Thus the normal form serves as a canonical representative of each projected[9D[K
projected‑identity class.

---

### 4. Non‑Injectivity and Loss of Preimage Information

**Proposition (Non‑injectivity):**  
There exist distinct trajectories \(\tau \neq \tau'\) in \(\mathcal{T}\) wi[2D[K
with equal histories:
\[
\Pi_{\mathrm{hist}}(\tau) = \Pi_{\mathrm{hist}}(\tau').
\]

*Example:* Start from \(\Omega_0 = \{a, b, c\}\). Consider two trajectories[12D[K
trajectories both committing \(a\) then \(b\):

- **Trajectory 1:** \(\{a,b,c\} \to \{b,c\} \to \{c\}\) (options shrink as [K
events are taken).
- **Trajectory 2:** A binding step removes \(c\) early, leading to \(\{a,b,[8D[K
\(\{a,b,c\} \to \{a,b\} \to \{b\} \to \varnothing\).

Both project to the history \((a, b)\) under \(\Pi_{\mathrm{hist}}\), yet t[1D[K
they differ in intermediate options and structural constraints that were ne[2D[K
never committed.

**Interpretation:** The projection loses all information about alternative [K
possibilities (the “open” future states). Once a trajectory terminates, tho[3D[K
those alternatives cannot be recovered from the event word alone. This loss[4D[K
loss is precisely what makes history irreversible: only the ordered sequenc[7D[K
sequence of commitments remains informative.

---

### 5. Relationship to Structural Identity

The hierarchy of identity relations mirrors the stratified equivalence noti[4D[K
notions discussed earlier:

1. **Trajectory Equivalence** (full projection) – retains all dynamics.
2. **Event‑Word Equality** in \(\PathCat\) – retains only ordered commitmen[9D[K
commitments, discarding intermediate option space.
3. **Structural Isomorphism** (identity of observable states in \(\mathcal{[11D[K
\(\mathcal{S}\)) – equates objects solely by their present configuration.

Thus projected identity sits between full dynamical equivalence and mere st[2D[K
structural resemblance, embodying the philosophical insight that “the past [K
is determined but often informationally inaccessible from the present.”

---

**Conclusion:**  
Projected identity formalises Spherepop’s principle that identity is define[6D[K
defined by the irreversible trace of events rather than by the whole trajec[6D[K
trajectory. This captures both the informational poverty of the present sta[3D[K
state and the irreversibility inherent in dynamical systems, while preservi[8D[K
preserving a minimal complete invariant (the canonical event word) for each[4D[K
each equivalence class.

