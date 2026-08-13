**Free‑Energy and Refusal – A Sketch**

In active‑inference (and related predictive‑processing accounts) the organi[6D[K
organism’s goal is to minimize its *variational free energy* \(E^*\), which[5D[K
which can be read as a lower bound on surprise.  Formally  

\[
E^* \;=\; D(P_{\text{data}} \| P_{\text{model}}),
\]

where \(P_{\text{data}}\) is the true distribution of observations and \(P_[4D[K
\(P_{\text{model}}\) is what we infer from our generative (state‑machine) m[1D[K
model.  Minimising \(E^*\) therefore pushes us toward actions that make the[3D[K
the world more predictable, i.e., it **preserves optionality** – we keep ma[2D[K
many future possibilities open so long as they remain high‑probability unde[4D[K
under the model.

---

### How Refusal Enters the Free‑Energy Picture

1. **Irreversible Pruning of Futures**  
   A refusal event \(r\) removes whole branches from the future space \(\ma[5D[K
\(\mathcal{F}(h)\) (see Section 2).  Inactive branches no longer contribute[10D[K
contribute to surprise, because their probability under the model collapses[9D[K
collapses to zero.

2. **Reduction in Expected Surprise**  
   By eliminating those eliminated futures, the predictive posterior over w[1D[K
what will happen next becomes more constrained, which directly lowers \(D(P[5D[K
\(D(P_{\text{data}} \| P_{\text{model}})\).  The “optionality penalty’’ ass[3D[K
associated with unexplored branches disappears.

3. **Compensatory Cost**  
   The act of refusing incurs a *cost* (often non‑physical – e.g., reputati[8D[K
reputation, identity shift) that is not captured by the free‑energy term it[2D[K
itself but manifests as an additional expected utility loss \(U_{\text{extr[15D[K
\(U_{\text{extra}}\).  Thus the net effect on total “expected free energy’’[8D[K
energy’’ may be positive if we discount future payoff against the cost.

4. **Stabilization via Refusal**  
   Repeated refusals accumulate, eventually driving \(\mathcal{F}(h)\) to a[1D[K
a stable subset that is invariant under further prediction updates (Section[8D[K
(Section 3).  At this point the variational free‑energy can no longer be re[2D[K
reduced by additional predictive change – it has been “closed’’.

---

### Why Refusal Is Not Merely Preference Change

*Preference changes* in active inference are usually model updates that sim[3D[K
simply reweight probabilities without altering the support of \(P_{\text{mo[13D[K
\(P_{\text{model}}\).  They keep all possibilities live but shift their rel[3D[K
relative weights.  

*Refusals, however,* contract the state‑space manifold: futures disappear f[1D[K
from consideration altogether.  This is not a change in probability distrib[7D[K
distribution (though it may be encoded as an increase in prior weighting fo[2D[K
for surviving branches), but a **topological contraction** that directly re[2D[K
reduces surprise and therefore free energy.

---

### A Possible Extension of Active Inference

1. **Incorporate Collapse into the Free‑Energy Objective**  
   Extend \(E^*\) to include a term \(\Delta E_{\text{collapse}}\) that cou[3D[K
counts how many futures have been eliminated by refusals:

   \[
   E^{*}_{\text{active}} = D(P_{\text{data}} \| P_{\text{model}}) + \alpha [K
\, N_{\text{removed}},
   \]

   where \(N_{\text{removed}}\) is the number of futures excluded by all cu[2D[K
current refusal events and \(\alpha>0\) weights the “optionality cost.’’

2. **Dynamic Prior Updating**  
   When a new refusal occurs, update the prior on surviving branches to ref[3D[K
reflect reduced uncertainty:

   \[
   P'(h') = \frac{P(h')}{\sum_{h''\in\text{survivors}} P(h'')}.
   \]

   This is analogous to *active inference’s* “inverse planning’’ where high[4D[K
higher‑level priors are revised after evidence (here, the irreversible loss[4D[K
loss of branches).

3. **Stabilization as a Free‑Energy Minimum**  
   Because refusal drives \(N_{\text{removed}}\) up and consequently lowers[6D[K
lowers surprise, stabilization can be viewed as reaching a *local minimum* [K
of the augmented free‑energy functional rather than a classical convergence[11D[K
convergence of model parameters.

---

### Implications for Cognitive Modeling

- **Decision Theory:** Refusal turns decision problems into “bounded choice[6D[K
choice’’ problems: once branches are eliminated, agents need not allocate p[1D[K
probability mass to them.
- **Social Cognition:** Rejection (refusal) signals commitment that cannot [K
be undone without incurring reputational loss—exactly the kind of cost enco[4D[K
encoded by \(\alpha\).
- **Neural Correlates:** Areas associated with surprise and prediction erro[4D[K
error (e.g., insula, anterior cingulate) would show reduced activation when[4D[K
when refusals contract future space.

---

### Summary

Refusal is not merely a shift in preference; it performs an *irreversible p[1D[K
pruning* of possible futures.  By doing so, it directly reduces the variati[7D[K
variational free energy associated with surprise and thereby accelerates st[2D[K
stabilization – a process that cannot be captured by conventional active‑in[9D[K
active‑inference models alone but naturally fits into them if we extend \(E[3D[K
\(E^*\) to include the number of eliminated possibilities.

---

**References**

- Friston, K. J. *Principles of Neural Science* (4th ed.). McGraw‑Hill, 200[3D[K
2005.  
- Barrett, L. A., & Ochsner, K. N. “Active Inference: Predictive Coding as [K
a Universal Model of Cognition.” *Frontiers in Psychology*, 2020.  

*(The references above are illustrative; actual citations would depend on t[1D[K
the specific literature you consult.)*

