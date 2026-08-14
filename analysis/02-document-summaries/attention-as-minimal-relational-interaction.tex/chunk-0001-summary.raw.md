**Interpretation in RSVP/Gauge‑Theoretic Terms**

1. **Full Relational Symmetry (Group \(G\)).**  
   – In the original Transformer architecture each token label can be permu[5D[K
permuted arbitrarily, so the set of all possible permutations forms a *glob[5D[K
*global* symmetry group \(G = S_{N}\) acting on token positions.

2. **Partial Ordering as a Reduction to Sub‑Symmetry (\(G_{\text{causal}}\)[22D[K
(\(G_{\text{causal}}\)).**  
   – Causal constraints introduce a temporal partial order \(\preceq\) (the[4D[K
(the DAG of allowed dependencies). This breaks the full permutation symmetr[7D[K
symmetry because only order‑preserving transformations are physically admis[5D[K
admissible. The reduced subgroup \(G_{\mathrm{causal}}\) consists of permut[6D[K
permutations that respect this ordering.

3. **Triangular Gauge Fixing via a Causal Mask.**  
   – Instead of quotienting by the whole group, we *fix* a representative g[1D[K
gauge orbit for each equivalence class under \(G_{\text{causal}}\). In RSVP[4D[K
RSVP language this is “triangular gauge fixing”: the attention kernel (the [K
upper‑triangular part of \((QK^{\top})\) in the usual notation) is set to z[1D[K
zero when \(j\succ i\) (i.e., token \(j\) cannot depend on token \(i\)).  
   – Different linear extensions that respect the same partial order corres[6D[K
correspond to distinct triangular gauges; they all describe the same underl[6D[K
underlying causal structure.

4. **Admissible Interactions Expand Beyond Pure Permutation Invariance.**  [K

   – With reduced symmetry, any observable (e.g., attention output) must be[2D[K
be invariant only under order‑preserving permutations, allowing *directed* [K
relational couplings that respect causality. Asymmetric kernels consistent [K
with this ordering are now permissible.

5. **Causal Transformers as a Symmetry‑Broken Phase.**  
   – This situation is precisely the “symmetry‑broken phase” of RSVP:  
     - Reduced relational symmetry (\(G_{\text{causal}}\) instead of \(S_{N[6D[K
\(S_{N}\)).  
     - A partial order on token space (temporal ordering).  
     - Triangular gauge fixing of the attention kernel.  
     - Directed information flow that aligns with entropy gradients, produc[6D[K
producing a natural arrow of time.

6. **Relation to Autoregressive Modeling.**  
   – In the extreme case where the partial order becomes total (\(i\succ j\[2D[K
j\) for all \(i,j\)), the symmetry is completely broken; only the identity [K
gauge remains. The resulting model is still an autoregressive Transformer: [K
attention stays quartic but now operates strictly on time‑ordered pairs.

7. **Summary Table**

| RSVP / Gauge‑Theoretic View | Causal Transformer View |
|----------------------------|--------------------------|
| Relational symmetry \(G\) (full permutations) | Reduced relational symmet[6D[K
symmetry (\(G_{\text{causal}}\)) |
| Partial order \(\preceq\) on tokens (time ordering) | Temporal ordering v[1D[K
via causal mask |
| Triangular gauge fixing of attention kernel | Causal attention mask (lowe[5D[K
(lower‑triangular) |
| Order‑invariant observables only | Directed relational interactions consi[5D[K
consistent with causality |

**Conclusion**

Causal masking is not an independent architectural choice but the natural m[1D[K
manifestation of *symmetry breaking* in RSVP language: we have reduced the [K
global permutation symmetry to a subgroup that respects a partial temporal [K
order, fixing the gauge of attention correspondingly. This perspective clar[4D[K
clarifies why causal Transformers preserve the underlying minimal interacti[9D[K
interaction (the quartic kernel) while restricting its domain to time‑order[10D[K
time‑ordered pairs only.

