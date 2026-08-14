**Summary**

The paper unifies three hierarchical levels of description for an evolving [K
system:

1. **Trajectory Category \(\mathcal{T}\)** – contains all possible historie[8D[K
histories (possibility‑history pairs) with full option‑space geometry.  
2. **Free History Category \(\PathCat\)** – obtained by the first projectio[9D[K
projection \(\Pi_{\text{hist}}:\mathcal{T}\to\PathCat\) which forgets the i[1D[K
internal evolution of the option space and retains only the ordered sequenc[7D[K
sequence of committed events (the “history word”).  
3. **Observable State Category \(\mathcal{S}\)** – obtained by projecting h[1D[K
histories onto observable states via the Collapse functor \(\Collapse:\Path[17D[K
\(\Collapse:\PathCat\to\mathcal{S}\), which reconstructs a state from its h[1D[K
history by composing associated transformations.

Both projections are functors:

- \(\Pi_{\text{hist}}\) respects composition because concatenating two traj[4D[K
trajectories yields the concatenated event word.  
- \(\Collapse\) also respects composition because replaying a concatenated [K
history is equivalent to replaying each part in turn.

**Global Commutative Diagram**

The overall map from trajectories directly to observable states is

\[
\Pi_{\text{hist}}:\mathcal{T}\longrightarrow\PathCat,\qquad
\Collapse:\PathCat\longrightarrow\mathcal{S},
\]

and their composition \(\Collapse\circ\Pi_{\mathrm{hist}}\) gives a functor[7D[K
functor from \(\mathcal{T}\) to \(\mathcal{S}\).

The diagram is commutative:

```
    mathcal{T}
     ↙   ↘
  Pi_hist ──► PathCat
     ▲       ▼
     │       │
Collapse ◄──► mathcal{S}
```

**Irreversibility**

Because information is lost at each step, neither projection has a right in[2D[K
inverse:

- No functor \(R:\mathcal{S}\to\PathCat\) can recover the full trajectory f[1D[K
from a state.  
- No functor \(Q:\PathCat\to\mathcal{T}\) can recover the full history from[4D[K
from an event word.

This reflects genuine irreversibility: once option space is forgotten, no a[1D[K
amount of information in \(\mathcal{S}\) or \(\PathCat\) can reconstruct th[2D[K
the lost possibility structure.

**Path Functionals**

Entropy \(S\) and responsibility \(\mathcal{R}\) are defined on trajectorie[11D[K
trajectories:

\[
S(\tau)=\log\frac{|\Omega_0|}{|\Omega_k|},\qquad
\mathcal{R}(\tau)=\sum_{j=1}^{k}\rho(E_{i_j}),
\]

and they factor through \(\Pi_{\mathrm{hist}}\) only in the sense that both[4D[K
both measures depend on the same ordered event word. They do **not** factor[6D[K
factor completely, showing that entropy and responsibility capture properti[8D[K
properties beyond mere identity.

**Stratified Ontology**

The three‑level structure with two scalar measures (entropy and responsibil[11D[K
responsibility) reflects a stratified ontology:

- **Level 1 (deepest):** Trajectory \(\mathcal{T}\) – full possibility geom[4D[K
geometry.  
- **Level 2:** Free History \(\PathCat\) – ordered commitment record.  
- **Level 3:** Observable State \(\mathcal{S}\) – current configuration.

Information is conserved at the trajectory level, progressively lost throug[6D[K
through the projections, and any remaining “shadow” effects of entropy or r[1D[K
responsibility are visible only at higher levels (history and state).

**Key Take‑aways**

- The diagram encapsulates a one‑way flow: richer description → coarser.  
- Irreversibility is formalized by the non‑existence of right inverses for [K
the projections.  
- Path functionals illustrate that not all trajectory information can be ca[2D[K
captured solely by identity; entropy and responsibility add extra, non‑reco[8D[K
non‑recoverable dimensions to the ontology.  

This framework provides a categorical foundation for understanding how poss[4D[K
possibility evolves into observable reality while preserving essential inva[4D[K
invariant structures across the hierarchy.
