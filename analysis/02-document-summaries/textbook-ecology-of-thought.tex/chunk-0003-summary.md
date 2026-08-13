**Exploration under Partial Observability**

When an observer moves through a graph that is only partially observed—i.e.[13D[K
observed—i.e., the set  

\[
\mathcal{F}_n = \text{observed subgraph after } n\text{ steps}
\]

is known at each moment—the value of any move can no longer be judged solel[5D[K
solely by geometry. Instead it must incorporate **epistemic uncertainty** a[1D[K
about what remains hidden.

---

### 1. Epistemic Value

For a vertex \(v\) that is not yet in the observed subgraph, define its epi[3D[K
epistemic value as  

\[
\mathcal{E}(v \mid \mathcal{F}_n) = H(\mathcal{F}_n) - H(\mathcal{F}_n \cup[4D[K
\cup \{v\}),
\]

where \(H\) denotes the Shannon entropy of a graph’s topology (or any consi[5D[K
consistent probability distribution over unknown vertices and edges).  
*Interpretation*: visiting \(v\) reduces uncertainty, so \(\mathcal{E}(v)\)[18D[K
\(\mathcal{E}(v)\) measures how much information we expect to gain about th[2D[K
the surrounding structure.

---

### 2. Expected Information Gain

Because epistemic value is history‑dependent, the optimal next step must be[2D[K
be chosen according to **expected** information gain:

\[
\pi^* = \arg\max_{v\notin\mathcal{F}_n}
\;\mathbb{E}\big[\Delta\Omega(v) \mid \mathcal{F}_n\big],
\]

where  

\[
\Delta\Omega(v)=|N(v)\setminus R_n|
\]

is the size of new neighborhoods that become reachable after the move. This[4D[K
This expectation accounts for the fact that some vertices may be more infor[5D[K
informative in certain contexts (e.g., a bridge linking two previously unco[4D[K
unconnected clusters).

---

### 3. Consequences

* **No universal ordering** – There is no single ranking of all vertices in[2D[K
independent of \(\mathcal{F}_n\). The marginal opportunity contribution cha[3D[K
changes with the accumulated reachable set \(R_n\) because  

  \[
  \Delta\Omega(v)=|N(v)\setminus R_n|
  \]

  directly depends on what has already been explored. Hence, Proposition [C[14D[K
Proposition [Context Dependence] holds: any ordering that works for all his[3D[K
histories is impossible.

* **Community saturation** – For any finite community \(C\), after a suffic[6D[K
sufficiently large number of steps (\(n^*\)), the expected gain from visiti[6D[K
visiting another vertex inside \(C\) becomes negligible because neighboring[11D[K
neighboring vertices have already been examined, yielding diminishing margi[5D[K
marginal returns. This mirrors known phenomena such as “local search exhaus[6D[K
exhaustion”.

* **Trade‑off with exploitation** – Because \(\mathcal{E}(v)\) can vary dra[3D[K
dramatically across different histories (e.g., a community that has not yet[3D[K
yet been penetrated vs. one where most nodes are already discovered), the p[1D[K
problem naturally splits into an *exploration* component (maximizing uncert[6D[K
uncertainty reduction) and an *exploitation* component (leveraging known st[2D[K
structure).  

  A practical heuristic is to select vertices with high \(\Delta\Omega(v)\)[19D[K
\(\Delta\Omega(v)\) **and** low current coverage \(|R_n|\cap N(v)\), i.e., [K
“new‑to‑explore” nodes.

---

### 4. Practical Implication

In practice, an adaptive algorithm should maintain a data structure that tr[2D[K
tracks:

1. The size and overlap of each vertex’s neighborhood with the currently kn[2D[K
known reachable set.
2. A running estimate of entropy \(H(\mathcal{F}_n)\) to gauge remaining un[2D[K
uncertainty.
3. Which sub‑graphs (communities) have already been saturated, prompting pe[2D[K
periodic “exploratory pivots” into under‑explored regions.

When such a structure is updated after each step, the algorithm can reliabl[7D[K
reliably choose moves that maximize expected information gain without prema[5D[K
prematurely committing to a fixed ordering of vertices.

---

**Summary**

Exploration in partially observable graphs must be driven by **epistemic va[2D[K
value**, i.e., how much uncertainty we expect to reduce. This yields an inh[3D[K
inherently history‑dependent optimization problem where:

* No universal ranking exists,
* Communities eventually saturate, and
* The process naturally balances between exploring new regions (exploration[12D[K
(exploration) and exploiting known structures (exploitation).

These insights directly follow from the definitions of reachable opportunit[10D[K
opportunity volume \(\Omega(P)\), marginal opportunity contribution \(\Delt[7D[K
\(\Delta\Omega(v)\), and epistemic value \(H(\mathcal{F}_n)-H(\mathcal{F}_n[34D[K
\(H(\mathcal{F}_n)-H(\mathcal{F}_n\cup\{v\})\).

