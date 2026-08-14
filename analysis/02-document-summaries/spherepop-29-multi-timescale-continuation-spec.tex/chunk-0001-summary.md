**1. Definitions and primitive concepts introduced**

- **Scope portfolio**: “A portfolio is \(T = \{(S_i , \tau_i)\}_{i=1}^n\), [K
where each unresolved scope \(S_i\) has a local option space \(O_i\) and ho[2D[K
horizon \(\tau_i\).”  
  *[source: “Definition 2.2 (Scope portfolio)”]*  

- **Local saturation** (\(LocalSat(i,t)\)): “\(max EMCG_i(a|F_t) \approx 0\[2D[K
0\) for all \(a\in O_i\).”  
  *[source: “Definition 2.3 (Local and field saturation)”]*  

- **Field saturation** (\(FieldSat(t)\)): “\(max_{i} max EMCG_i(a|F_t) \app[4D[K
\approx 0\).”  
  *[source: “Definition 2.3 (Local and field saturation)”]*  

- **POP, REFUSE, BIND, COLLAPSE**: Operational semantics of Spherepop opera[5D[K
operations—e.g., POP resolves a ready local scope; REFUSE removes continuat[9D[K
continuation branches; BIND tightens constraints; COLLAPSE merges distincti[9D[K
distinctions no longer worth explicit tracking.  
  *[source: “Event Semantics in This Experiment Family”]*  

**2. Mathematical claims and formal structures**

- **Proposition 2.4**: “LocalSat(i,t) does not imply FieldSat(t). If anothe[6D[K
another scope \(j\) satisfies \(\max_{a\in O_j} EMCG_j(a|F_t) > 0\), switch[6D[K
switching scopes restores progress.”  
  *[source: “Proposition 2.4 (Scope-switch recovery)”]*  

- **Proposition 2.5**: “A scope can transition from \(EMCG_i(a|F_t)\approx0[23D[K
\(EMCG_i(a|F_t)\approx0\) to \(EMCG_i(a|F_{t+\Delta t})>0\) without changin[7D[K
changing \(O_i\), due to intervening work on other scopes that modifies \(F[3D[K
\(F\).”  
  *[source: “Proposition 2.5 (Operator‑drift recovery)”]*  

- **Proposition 2.6**: “Long‑horizon scopes can accumulate useful structure[9D[K
structure through BIND/REFUSE/COLLAPSE while remaining unresolved; progress[8D[K
progress does not require immediate POP.”  
  *[source: “Proposition 2.6 (BIND‑as‑progress)”]*  

**3. Mechanisms and processes**

- **Novelty‑only policy**: Chooses the longest‑idle scope to maintain momen[5D[K
momentum across horizons.  
- **Shortest‑task‑first policy**: Always selects the minimal horizon scope,[6D[K
scope, favoring rapid local saturation.  
- **Max‑EMCG policy**: Greedily maximizes immediate expected marginal compr[5D[K
compression gain per scope.  
- **EMCG/cost + anti‑starvation policy**: Maximizes gain‑per‑cost while enf[3D[K
enforcing periodic updates to slow scopes (anti‑starvation).  

**4. Connections to concepts named in the running abstract**

- The document builds on “operationalizes boredom as a scope‑selection prob[4D[K
problem” and extends it with **local vs. field saturation** notions, distin[6D[K
distinct from the existing **Asymptotic Saturation Theorem** described in A[1D[K
Appendix B (§“Asymptotic Saturation Without Exhaustion”) which addresses re[2D[K
reintegration dynamics rather than task‑portfolio scheduling.  
- Concepts of **EMCG**, **Ft = C(Ht)**, and **progress stability across hor[3D[K
horizons** map directly to the metrics tracked (time‑to‑local saturation, s[1D[K
starvation rates, recovery latencies).  

**5. Unresolved questions or contradictions visible within this chunk**

- The claim that “LocalSat(i,t) does not imply FieldSat(t)” raises the ques[4D[K
question of whether long‑term systemic saturation can still be meaningful d[1D[K
despite individual scopes remaining unsaturated; no further theoretical jus[3D[K
justification is provided.  
- Proposition 2.6’s assertion that progress need not involve POP introduces[10D[K
introduces tension with earlier statements about maintaining unresolved dee[3D[K
deep threads, leaving open how “useful structure” accumulates without event[5D[K
eventual resolution.  

These points reflect the experimental nature of the specification and hint [K
at areas needing empirical validation or further theoretical development.
