**Spherepop‑29: Multi‑Timescale Continuation Theory – Unified Theoretical S[1D[K
Synthesis**

---

### 1. Thesis & Core Premise  
The document proposes a **scope‑portfolio framework** for managing multi‑ti[8D[K
multi‑timescale decision processes in a bounded rationality setting (see *“[2D[K
*“Operationalizes boredom as a scope‑selection problem”*). Its central thes[4D[K
thesis is that **local saturation of individual scopes does not guarantee f[1D[K
field‑wide progress**, and therefore mechanisms must be designed to detect,[7D[K
detect, recover from, and exploit cross‑scope dependencies. The theory oper[4D[K
operationalises “boredom” as the inability to find new rewarding work withi[5D[K
within any active scope, thereby motivating continual re‑allocation across [K
horizons.

---

### 2. Primitive Concepts & Definitions  

| Concept | Formal Definition (as introduced) |
|---|---|
| **Scope portfolio** \(T = \{(S_i ,\tau_i)\}_{i=1}^n\) | A collection of *[1D[K
*unresolved* scopes, each with a local option space \(O_i\) and horizon \(\[3D[K
\(\tau_i\). The global state at time \(t\) is the set of currently active u[1D[K
unresolved scopes. |
| **Local saturation** \(LocalSat(i,t)\) | Holds when the maximal expected [K
marginal compression gain (EMCG) for any action \(a\in O_i\) satisfies \(ma[4D[K
\(max_{a\in O_i} EMCG_i(a|F_t)\approx0\). Indicates that immediate progress[8D[K
progress within scope \(i\) is exhausted. |
| **Field saturation** \(FieldSat(t)\) | Holds when \(\forall i,\; max_{j}\[8D[K
max_{j}\, max_{a\in O_j} EMCG_j(a|F_t)\approx0\). Signals that no unresolve[9D[K
unresolved scope currently yields positive compression gains across the who[3D[K
whole portfolio. |
| **Spherepop operations** (POP, REFUSE, BIND, COLLAPSE) | - **POP**: Resol[5D[K
Resolves a ready local scope by committing its resources to external evalua[6D[K
evaluation.<br>- **REFUSE**: Discards continuation branches for scopes deem[4D[K
deemed insufficiently promising.<br>- **BIND**: Tightens constraints on unr[3D[K
unresolved scopes to prevent premature divergence.<br>- **COLLAPSE**: Merge[5D[K
Merges distinct but overlapping distinctions, reducing explicit tracking wh[2D[K
when they cease being differentially important. |

*(Sources: “Definition 2.2 (Scope portfolio)”, “Definition 2.3 (Local and f[1D[K
field saturation)”)*  

---

### 3. Formalism & Mathematical Claims  

1. **Proposition 2.4** – *Non‑implication of local from global*:  
   \[
   LocalSat(i,t)\;\not\Rightarrow\;FieldSat(t)
   \]
   If another scope \(j\) satisfies \(\max_{a\in O_j} EMCG_j(a|F_t) > 0\), [K
then progress is possible by switching scopes, restoring overall advancemen[10D[K
advancement. *(Source: “Proposition 2.4 (Scope‑switch recovery)”)*  

2. **Proposition 2.5** – *Operator‑drift recovery*:  
   A scope can move from \(EMCG_i(a|F_t)\approx0\) to \(EMCG_i(a|F_{t+\Delt[21D[K
\(EMCG_i(a|F_{t+\Delta t})>0\) without altering its option space, because i[1D[K
intervening work on other scopes reshapes the global state \(F\). *(Source:[9D[K
*(Source: “Proposition 2.5 (Operator‑drift recovery)”)*  

3. **Proposition 2.6** – *BIND as progress*:  
   Long‑horizon scopes may accumulate useful structure through BIND/REFUSE/[12D[K
BIND/REFUSE/COLLAPSE while remaining unresolved; such accumulation can cons[4D[K
constitute genuine progress without immediate POP. *(Source: “Proposition 2[14D[K
“Proposition 2.6 (BIND‑as‑progress)”)*  

---

### 4. Mechanisms & Policy Designs  

Four competing policy families are defined to resolve the tension between *[1D[K
**local vs. field saturation**:

| Policy | Design Principle |
|---|---|
| **Novelty‑only** | Selects the *longest‑idle* scope, preserving momentum [K
across horizons by maintaining a “boredom” buffer. |
| **Shortest‑task‑first (STF)** | Always picks the minimal horizon scope, f[1D[K
favoring rapid local saturation and quick feedback loops. |
| **Max‑EMCG** | Greedily maximizes immediate expected marginal compression[11D[K
compression gain per scope, driving the system toward locally optimal actio[5D[K
actions. |
| **EMCG/cost + anti‑starvation** | Balances gain‑per‑cost with periodic up[2D[K
updates to “slow” scopes (anti‑starvation), preventing starvation of long‑t[6D[K
long‑term horizons while keeping short‑term efficiency high. |

These policies are interdependent; the choice among them reflects trade‑off[9D[K
trade‑offs between **local freshness**, **global stability**, and **resourc[9D[K
**resource allocation fairness**.

---

### 5. Connections to Related Concepts  

- **Operationalizing boredom**: The document extends this notion by treatin[7D[K
treating “boredom” as a diagnostic signal (no new rewarding work within any[3D[K
any active scope) rather than a purely subjective feeling.  
- **Local vs. field saturation**: Distinguishes from the *Asymptotic Satura[6D[K
Saturation Theorem* in Appendix B, which addresses reintegration dynamics w[1D[K
without focusing on portfolio scheduling.  
- **EMCG, \(F_t = C(H_t)\), and progress stability**: Directly maps to metr[4D[K
metrics tracked: time‑to‑local saturation, starvation rates, and recovery l[1D[K
latencies for long‑term horizons.

---

### 6. Unresolved Problems & Internal Tensions  

1. **Longitudinal systemic relevance** – The claim that *LocalSat(i,t) does[4D[K
does not imply FieldSat(t)* raises the question of whether meaningful syste[5D[K
systemic progress can ever be achieved when individual scopes remain unsatu[6D[K
unsaturated; no theoretical justification for eventual integration is provi[5D[K
provided yet.  
2. **Progress without POP** – Proposition 2.6 suggests that useful structur[8D[K
structure may accumulate via BIND/REFUSE/COLLAPSE even if POP never occurs,[7D[K
occurs, creating tension with earlier statements about preserving deep thre[4D[K
threads indefinitely. This requires empirical validation or a more formal a[1D[K
account of “latent progress.”  

These open issues highlight the experimental nature of the specification an[2D[K
and point to areas where further theoretical development (e.g., cross‑horiz[11D[K
cross‑horizon convergence criteria) or empirical testing is needed.

---

### 7. Implications for Cluster & Cross‑Corpus Synthesis  

- **Cluster synthesis**: The framework naturally partitions the portfolio i[1D[K
into *local* vs. *global* dimensions, enabling clustering of scopes by satu[4D[K
saturation status and policy sensitivity.  
- **Cross‑corpus implications**: By formalising local/field saturation and [K
scope‑switch recovery mechanisms, the theory provides a common vocabulary f[1D[K
for integrating multi‑scale models from other domains (e.g., reinforcement [K
learning’s “curiosity” signals, hierarchical Bayesian inference’s “model ev[2D[K
evidence”).  

---

**References (as per fragment summaries)**  
- Definition 2.2 (Scope portfolio) – *“Definition 2.2 (Scope portfolio)”*  [K

- Definition 2.3 (Local and field saturation) – *“Definition 2.3 (Local and[3D[K
and field saturation)”*  
- Proposition 2.4 (Scope‑switch recovery) – *“Proposition 2.4 (Scope‑switch[13D[K
(Scope‑switch recovery)”*  
- Proposition 2.5 (Operator‑drift recovery) – *“Proposition 2.5 (Operator‑d[11D[K
(Operator‑drift recovery)”*  
- Proposition 2.6 (BIND‑as‑progress) – *“Proposition 2.6 (BIND‑as‑progress)[18D[K
(BIND‑as‑progress)”*  

--- 

*End of unified synthesis.*

