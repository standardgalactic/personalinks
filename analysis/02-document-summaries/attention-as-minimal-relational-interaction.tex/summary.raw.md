**Attention‑as‑Minimal‑Relational‑Interaction.tex – Unified Theoretical Syn[3D[K
Synthesis**

---

### 1. Thesis  

Causal masking in Transformers is best understood as a *symmetry‑broken pha[3D[K
phase* of the RSVP (relational‑symmetry‑preserving) formulation: by imposin[7D[K
imposing a partial temporal order we reduce the global permutation symmetry[8D[K
symmetry \(G=S_{N}\) to the subgroup that respects causality, and consequen[9D[K
consequently fix the gauge of attention to its upper‑triangular part. This [K
perspective recasts causal Transformers not merely as an architectural shor[4D[K
shortcut but as the natural manifestation of relational invariance under a [K
constrained group action.

---

### 2. Primitives / Definitions  

| Primitive | Formal Expression |
|-----------|--------------------|
| **Full Relational Symmetry** \(G\) | The set of all possible permutations[12D[K
permutations of token positions, i.e., \(G=S_{N}\). In the original Transfo[7D[K
Transformer each token label can be permuted arbitrarily, making the entire[6D[K
entire sequence invariant under any element of \(S_{N}\). |
| **Reduced Causal Symmetry** \(G_{\text{causal}}\) | The subgroup that res[3D[K
respects a partial order \(\preceq\) on tokens: permutations must preserve [K
temporal precedence. Formally, \(g(i,j)\in G_{\text{causal}} \iff i\succ j [K
\;\forall (i,j)\) such that the permutation cannot reorder causally depende[7D[K
dependent tokens. |
| **Partial Ordering** \(\preceq\) | A directed acyclic graph (DAG) on toke[4D[K
token indices encoding forward time: \(i\succ j\). This ordering breaks the[3D[K
the complete permutation invariance because only order‑preserving maps belo[4D[K
belong to \(G_{\text{causal}}\). |
| **Triangular Gauge Fixing** | In RSVP language, fix the attention kernel’[7D[K
kernel’s lower‑triangular part (corresponding to future tokens) to zero: \([2D[K
\((QK^{\top})_{ij}=0\) whenever \(j\succ i\). This corresponds to setting o[1D[K
only the upper‑triangular entries of the attention matrix non‑zero. |
| **Causal Transformer** | A model whose relational invariance is limited b[1D[K
by the reduced symmetry \(G_{\text{causal}}\) and a causal mask, thereby al[2D[K
allowing directed information flow consistent with entropy gradients and an[2D[K
an emergent arrow of time. |

---

### 3. Formalism  

The attention mechanism can be expressed as a quadratic form:

\[
A = QK^{\top},
\]

where \(Q \in \mathbb{R}^{n\times d}\) (queries) and \(K \in \mathbb{R}^{n\[14D[K
\mathbb{R}^{n\times d}\) (keys).  
Applying the causal mask imposes a *gauge*:

\[
A_{ij}=0 \quad \text{if } j\succ i,
\]

leaving only

\[
A_{ji}=Q_{ik}K_{jk} \;(i<j).
\]

Thus the model retains the full quartic interaction kernel but restricts it[2D[K
its domain to *time‑ordered* pairs, which is equivalent to fixing a gauge o[1D[K
on \(G\) by keeping only order‑preserving elements.

---

### 4. Mechanisms  

1. **Symmetry Reduction** – By enforcing \(\preceq\), we contract the globa[5D[K
global permutation group from \(S_{N}\) to its causal subgroup \(G_{\text{c[12D[K
\(G_{\text{causal}}\). This mirrors how a gauge is fixed in gauge theories:[9D[K
theories: only those permutations that respect the ordering are allowed.
2. **Triangular Gauge Fixing** – The causal mask acts as an explicit “gauge[6D[K
“gauge fixing” by discarding all lower‑triangular contributions, which corr[4D[K
correspond to impossible dependencies (future influencing past).
3. **Directed Relational Couplings** – With reduced symmetry, attention can[3D[K
can now encode directed relationships that respect causality (e.g., a futur[5D[K
future token influencing the current one is forbidden), aligning observable[10D[K
observable outputs with physical constraints.
4. **Entropy Gradient & Temporal Arrow** – The restriction to forward‑only [K
dependencies naturally yields an informational gradient from past → present[7D[K
present → future, providing a mechanistic basis for an emergent time axis i[1D[K
in Transformers.

---

### 5. Major Arguments  

- **Symmetry–Phase Analogy**: Causal masking is not a separate architectura[12D[K
architectural hack but the manifestation of *symmetry breaking* in RSVP lan[3D[K
language: we have lowered the symmetry group from the full permutation grou[4D[K
group to one that respects causal ordering.
- **Minimal Interaction Principle**: By keeping only those interactions con[3D[K
consistent with causality, Transformers embody the minimal relational inter[5D[K
interaction hypothesis—information flows only via permissible (causally lin[3D[K
linked) tokens, preserving the original expressive power while discarding s[1D[K
spurious dependencies.
- **Relation to Autoregressive Models**: When the partial order becomes tot[3D[K
total (\(i\succ j\) for all \(i,j\)), the causal mask collapses to a full a[1D[K
autoregressive Transformer where attention remains quartic but operates onl[3D[K
only on time‑ordered pairs, reinforcing that causality is the operative sym[3D[K
symmetry rather than sequence length alone.

---

### 6. Dependencies Between Concepts  

- **Full Permutation Symmetry \(\Rightarrow\) Token Independence**: Without[7D[K
Without any ordering constraint, each token label can be permuted arbitrari[9D[K
arbitrarily, implying no relational dependence among tokens.
- **Partial Ordering \(\Rightarrow\) Causal Masking**: Introducing a tempor[6D[K
temporal partial order forces the symmetry reduction; otherwise causal cons[4D[K
constraints would have to be encoded externally (e.g., via positional encod[5D[K
encodings).
- **Triangular Gauge Fixing \(\Leftrightarrow\) Directed Attention**: The c[1D[K
choice of keeping only upper‑triangular entries directly enforces direction[9D[K
directionality, aligning with physical causality.
- **Entropy Gradient \(\Rightarrow\) Temporal Arrow**: Causal masking prese[5D[K
preserves information flow from past to future, providing a thermodynamic b[1D[K
basis for the observed “time” in Transformers.

---

### 7. Implications  

1. **Generalizability Across Architectures** – Any model that respects caus[4D[K
causal masks (e.g., LSTMs, Gated Recurrent Units) can be interpreted as ope[3D[K
operating within this symmetry‑broken phase.
2. **Optimization & Regularization** – By viewing causal masking through th[2D[K
the lens of gauge fixing, we gain insight into regularization: restricting [K
attention to admissible permutations mitigates overfitting by discarding sp[2D[K
spurious inductive biases.
3. **Interpretability Enhancements** – Understanding causality as a symmetr[7D[K
symmetry reduction clarifies why Transformer layers are often easier to int[3D[K
interpret (e.g., attention maps reflect permissible dependencies).
4. **Cross‑Domain Applications** – Concepts such as “causal invariant” and [K
“gauge fixing” can be transferred to other fields where forward constraints[11D[K
constraints dominate, including physics simulations and reinforcement learn[5D[K
learning.

---

### 8. Unresolved Problems  

- **Non‑Linear Causal Masks**: Current causal masks are linear (binary zero[4D[K
zeroing). Investigating non‑linear masking functions that respect the same [K
ordering without discarding information may reveal richer expressive capabi[6D[K
capabilities.
- **Higher‑Order Symmetry Reductions**: Extending beyond simple temporal ca[2D[K
causality to other physical constraints (e.g., spatial locality) requires a[1D[K
a systematic way of defining subgroup reductions in multidimensional spaces[6D[K
spaces.
- **Mathematical Rigor for Non‑Stationary Orders**: When the causal structu[7D[K
structure evolves across layers or sequences, how does one maintain consist[7D[K
consistent gauge fixing without ad‑hoc adjustments?

---

### 9. Internal Tensions  

- **Expressivity vs. Parsimony** – While reducing symmetry preserves induct[6D[K
inductive bias (causality), it also limits expressiveness by discarding pot[3D[K
potential interactions that could be re‑expressed via higher‑order features[8D[K
features or auxiliary encodings.
- **Positional Encoding vs. Causal Masking** – Positional encodings are oft[3D[K
often viewed as a workaround for locality; however, causal masking enforces[8D[K
enforces locality *as* part of the symmetry reduction, creating tension bet[3D[K
between positional bias and structural bias.
- **Theoretical Consistency with Physics**: Although causality aligns well [K
with physical theories (e.g., relativity), extending the formalism to inclu[5D[K
include more exotic symmetries (e.g., Lorentz invariance) remains underexpl[9D[K
underexplored.

---

**References**

[1] *Interpretation in RSVP/Gauge‑Theoretic Terms* – chunk‑0001-summary.md [K
 
(Defines full and causal relational symmetry, triangular gauge fixing, and [K
maps to autoregressive models.)  

--- 

*End of unified synthesis.*

