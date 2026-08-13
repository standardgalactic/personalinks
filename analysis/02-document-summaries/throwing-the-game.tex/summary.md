**Thesis**

Refusal is not merely a change in preference; it performs an irreversible p[1D[K
pruning of possible futures, thereby directly reducing the variational free[4D[K
free‑energy associated with surprise and accelerating stabilization. This d[1D[K
distinguishes refusal from conventional preference shifts, which only rewei[5D[K
reweight probabilities without altering the support of the model.

---

**Primitives & Definitions**

1. **Variational Free Energy (VE)**  
   \[
   E^* = D(P_{\text{data}} \| P_{\text{model}})
          = \mathbb{E}_{q(s_t)}[-\log p(o_{1:t}, s_t)]
            + \mathbb{E}_{q(s_t)}[\log q(s_t)]
          = D_{\mathrm{KL}}\!\bigl(q(s_t)\,\|\,p(s_t|o_{1:t})\bigr) - \log [K
p(o_{1:t}),
   \]
   where minimising \(E^*\) reduces uncertainty (surprise) and thus lowers [K
expected free energy.

2. **Active Inference**  
   Extends VE minimisation to actions by selecting policies that minimise e[1D[K
expected future VE, as articulated in Friston (2005), Barrett & Ochsner (20[11D[K
Ochsner (2020).

3. **Spherepop Constraint (Inadmissibility Prior)**  
   Refusal is encoded as hard constraints \(C_\alpha\) on admissible trajec[6D[K
trajectories \(\tau\):
   \[
   p(\tau | C_\alpha) \propto p(\tau)\,\mathbf{1}\{\tau \text{ does not beg[3D[K
begin with }\alpha\},
   \]
   i.e., entire trajectory regions are set to zero probability, unlike ordi[4D[K
ordinary preference changes that adjust relative weights.

---

**Formalism**

- **Refusal Operation**:  
  For a refusal event \(r\) at time \(t_1\) followed by another event \(\be[5D[K
\(\beta\) at \(t_2\),
  \[
  \Future_2 = \llbracket \mathbf{Refuse}(\beta)\rrbracket(
                \llbracket \mathbf{Refuse}(\alpha)\rrbracket(\Future_0)).
  \]
- **Closure**: The operation yields a *closed* future space \(\mathcal{F}(h[15D[K
\(\mathcal{F}(h)\) invariant under further prediction updates.

---

**Mechanisms**

1. **Irreversible Pruning of Futures**  
   By eliminating whole branches, refusals remove possibilities that contri[6D[K
contribute to surprise:
   \[
   E^*_{\text{active}} = D(P_{\text{data}} \| P_{\text{model}}) + \alpha N_[2D[K
N_{\text{removed}},
   \]
   where \(N_{\text{removed}}\) counts eliminated futures and \(\alpha>0\) [K
weights the optionality cost.

2. **Reduction in Expected Surprise**  
   The posterior over future states becomes more constrained, lowering surp[4D[K
surprise and consequently VE.

3. **Compensatory Cost**  
   Refusal incurs non‑physical costs (e.g., reputation loss), appearing as [K
an extra expected utility loss \(U_{\text{extra}}\) that may offset the VE [K
reduction if discounted appropriately.

4. **Stabilisation via Refusal**  
   Repeated refusals drive \(\mathcal{F}(h)\) to a stable subset invariant [K
under further updates, effectively reaching a local minimum of the augmente[8D[K
augmented free‑energy functional.

---

**Major Arguments**

- **Refusal ≠ Preference Change**: Unlike preference changes (which only re[2D[K
reweight probabilities), refusal contracts the state‑space manifold by remo[4D[K
removing entire branches, directly reducing surprise.
- **Free Energy as a Unified Objective**: Incorporating \(N_{\text{removed}[19D[K
\(N_{\text{removed}}\) into VE makes refusals part of the optimisation land[4D[K
landscape rather than an external cost function.
- **Predictive Planning Extension**: Dynamic prior updates after refusal:
  \[
  P'(h') = \frac{P(h')}{\sum_{h''\in\text{survivors}} P(h'')},
  \]
  mirrors “inverse planning’’ in active inference, reflecting reduced uncer[5D[K
uncertainty for surviving branches.

---

**Dependencies Between Concepts**

- **Spherepop & Free Energy**: Spherepop events must be encoded as constrai[8D[K
constraints within the generative model; otherwise they cannot affect VE.
- **Active Inference Compatibility**: For refusal to align with free‑energy[11D[K
free‑energy minimisation, the model must include relevant world invariants [K
so that refusals reduce overall free energy across a broader class of model[5D[K
models.
- **Reversibility & Stability**: If a refusal raises expected VE (e.g., eli[3D[K
eliminating high‑reward trajectories), it signals an unresolved tension; su[2D[K
such cases require explicit handling or redefinition of VE.

---

**Implications**

1. **Decision Theory**: Refusal transforms decision problems into “bounded [K
choice’’ scenarios, simplifying agent behaviour.
2. **Social Cognition**: Rejection (refusal) signals commitment that cannot[6D[K
cannot be undone without reputational costs—captured by the cost term \(\al[5D[K
\(\alpha\).
3. **Neural Correlates**: Areas associated with surprise and prediction err[3D[K
error (insula, ACC) show reduced activation when refusals contract future s[1D[K
space.
4. **Model Extensions**:
   - Introduce a *collapse term* into VE to formalise optionality loss.
   - Use dynamic prior updates post‑refusal to reflect reduced uncertainty.[12D[K
uncertainty.

---

**Unresolved Problems**

- **Turing‑Test for Genuine Refusal**: How can we empirically distinguish g[1D[K
genuine irreversible policy modification from behavioural imitation?
- **Ethical & Philosophical Issues**: Does refusal preserve agency and resp[4D[K
responsibility, or does it risk reinforcing discriminatory norms? (See Ansc[4D[K
Anscombe 1957; Bratman 1987.)
- **Structural Properties**:
  - Commutativity of successive refusals.
  - Partial revocation mechanisms without re‑optimisation loops.

---

**Connections Likely to Matter Elsewhere in Spherepop**

- **General Predictive Coding Framework**: Refusal can be viewed as a speci[5D[K
special case of predictive coding where future states are conditionally era[3D[K
erased, influencing broader theoretical applications (e.g., self‑modeling, [K
identity formation).
- **Cognitive Architectures**: Embedding refusal constraints may bridge gap[3D[K
gaps between symbolic reasoning and connectionist models by providing expli[5D[K
explicit inadmissibility priors.
- **Interdisciplinary Links**:
  - *Ethics*: Refusal as a mechanism for moral agency aligns with discussio[9D[K
discussions on responsibility (Anscombe) and consent (Bratman).
  - *Computer Science*: Designing systems that support irreversible commitm[7D[K
commitments without external locking mechanisms could inform secure distrib[7D[K
distributed consensus protocols.

---

*End of extracted theoretical content.*

