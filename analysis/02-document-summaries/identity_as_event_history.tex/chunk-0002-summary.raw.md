**Projected Identity in the Spherepop Framework**

The notion of *identity* in the Spherepop ontology is not a primitive prope[5D[K
property but rather an equivalence class defined by irreversible trajectori[10D[K
trajectories. Below is a detailed exposition of how this works, linking it [K
to the earlier definitions and illustrating its implications.

---

### 1. Trajectory Category

- **Objects**: The objects of the category \(\mathcal{T}\) are *Spherepop s[1D[K
states* \((\Omega_t, H_t)\), where \(\Omega_t\) is a set of options at time[4D[K
time \(t\) and \(H_t\) is the associated history (event word).
- **Morphisms**: A morphism from \((\Omega_t, H_t)\) to \((\Omega_{t'}, H_{[3D[K
H_{t'})\) exists iff:
  - \(\Omega_{t'} \subseteq \Omega_t\) (the state at \(t'\) is a subset of [K
the current state),
  - \(H_{t'} = H_t \cdot w\) for some non‑empty word \(w\), preserving the [K
ordering,
  - The extension satisfies the axioms from Section \(\ref{sec:possibility-[31D[K
Section \(\ref{sec:possibility-preimage}\).

- **Composition**: Composition is simply concatenation of extensions, i.e.,[5D[K
i.e., following one trajectory after another.

- **Irreversibility**: There are no non‑trivial isomorphisms because \(\Ome[6D[K
\(\Omega\) can only shrink while \(H\) can only grow; thus a reverse morphi[6D[K
morphism would require identical states.

---

### 2. History Projection Functor

Define the history projection functor  
\[
\Pi_{\mathrm{hist}} : \mathcal{T} \longrightarrow \PathCat,
\]  
which maps each state to its event word \(H_t\) and each morphism (extensio[9D[K
(extension) to the corresponding prefix extension in \(\PathCat\). Functori[8D[K
Functoriality follows directly from concatenating histories matching compos[6D[K
composition of trajectories.

---

### 3. Projected Identity Definition

**Definition**: Two terminal states \((\Omega_k, H_k)\) and \((\Omega_k', H[1D[K
H_k')\) are *Spherepop‑identical* if their projected histories coincide:
\[
\Pi_{\mathrm{hist}}(\tau) = \Pi_{\mathrm{hist}}(\tau').
\]

Thus identity is defined in terms of the *minimal complete invariant*—the o[1D[K
ordered sequence of committed events—not directly on trajectories themselve[9D[K
themselves.

**Trajectory Equivalence**: For any two trajectories \(\tau, \tau' \in \mat[4D[K
\mathcal{T}\),
\[
\tau \sim \tau' \;\Longleftrightarrow\; \Pi_{\mathrm{hist}}(\tau) = \Pi_{\m[7D[K
\Pi_{\mathrm{hist}}(\tau').
\]
Objects in the Spherepop ontology are equivalence classes under this relati[6D[K
relation.

---

### 4. Compatibility with Normal Forms

If \(G_X\) is the ancestral event graph and \((\text{spherepop}(X))_{\text{[31D[K
\((\text{spherepop}(X))_{\text{nf}}\) its canonical linearisation, then
\[
\Pi_{\mathrm{hist}}(\tau) = (\text{spherepop}(X))_{\text{nf}},
\]
so the earlier identity condition \(X \equiv Y\) (equality of normal forms)[6D[K
forms) is recovered as a special case.

---

### 5. Non‑Injectivity and Loss of Preimage Information

**Proposition**: There exist distinct trajectories \(\tau \neq \tau'\) such[4D[K
such that \(\Pi_{\mathrm{hist}}(\tau) = \Pi_{\mathrm{hist}}(\tau')\).

*Example*: Consider \(\Omega_0 = \{a, b, c\}\). Two trajectories commit \(a[3D[K
\(a\) first and \(b\) second but differ in subsequent options:
- **Trajectory 1**: \(\{a,b,c\} \to \{b,c\} \to \{c\}\).
- **Trajectory 2**: A binding step removes \(c\) early, yielding \(\{a,b,c\[10D[K
\(\{a,b,c\} \to \{a,b\} \to \{b\} \to \varnothing\).

Both project to the history \((a, b)\), showing that identity preserves onl[3D[K
only the order of commitments, discarding all other structural details.

---

### 6. Relationship to Structural Identity

The hierarchy of projections provides a stratified notion of equivalence:

1. **Trajectory Equivalence**: Full trajectory equivalence (Section \(\ref{[16D[K
(Section \(\ref{sec:equivalences}\)).
2. **Event‑Word Identity**: Equality in the event word.
3. **Structural Isomorphism**: Equality at the observable state level.

Spherepop identity sits between trajectory equivalence and structural isomo[5D[K
isomorphism, retaining causal order while discarding full dynamics of possi[5D[K
possibility space.

---

### Summary

Identity in Spherepop is thus a *projected* concept: it groups together tra[3D[K
trajectories that share the same ordered history, capturing what can be kno[3D[K
known from present observations (the entropy \(\mathcal{R}(X)\)) but not ne[2D[K
necessarily their entire past histories. This aligns with the philosophical[13D[K
philosophical view that the past is determined yet often informationally in[2D[K
inaccessible from the present, and it formalizes how irreversible processes[9D[K
processes prune alternative pathways while preserving only the essential se[2D[K
sequence of commitments.

