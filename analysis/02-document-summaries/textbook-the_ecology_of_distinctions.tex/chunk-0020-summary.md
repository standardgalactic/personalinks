Below are concise “summary formulae” that capture the main relations used t[1D[K
throughout the document.

---

### 1. Memory‐Weight Dynamics (Decay)

For memory weights \(w_i(t)\) decaying exponentially,

\[
\frac{dw_i}{dt}= -\lambda_i w_i,\qquad \lambda_i\ge0,
\]

the solution is

\[
w_i(t)=w_i(0)e^{-\lambda_i t}.
\]

The total memory field at time \(t\) and location \(x\) is a weighted sum o[1D[K
of kernel‐center locations:

\[
M(x,t)=\sum_{i} w_i(0)e^{-\lambda_i t}\,K(x,e_i).
\]

---

### 2. Exponential Forgetting Theorem  

If all decay rates satisfy \(\lambda_i\ge\lambda_{\min}>0\),

\[
M(x,t)\le e^{-\lambda_{\min}t}\,M(x,0),
\]

so the field decays at least as fast as a uniform exponential with rate \(\[3D[K
\(\lambda_{\min}\).

---

### 3. Recall Time Bound  

When the initial memory field satisfies \(M(x,0)>\theta\) and all traces de[2D[K
decay at common rate \(\lambda\),

\[
t < \frac{1}{\lambda}\log\!\left(\frac{M(x,0)}{\theta}\right)
\]

ensures that recall persists until the threshold is reached.

---

### 4. Reinforcement Dynamics  

With reinforcement \(r_i(t)\ge0\) (constant), cue exposure adds

\[
\frac{dw_i}{dt}= -\lambda_i w_i + \eta_i r_i,
\]

yielding a steady‑state weight

\[
w_i^* = \frac{\eta_i r_i}{\lambda_i}.
\]

---

### 5. Kernel Memory Representation  

Mapping cue locations to reproducing‑kernel Hilbert space via feature map \[1D[K
\(\Granite\),

\[
K(x,e)=\langle\Granite(x),\Granite(e)\rangle_{\mathcal H_K},
\]

the memory field becomes

\[
M(x,t)=\big\langle\Granite(x),\sum_i w_i(t)\,\Granite(e_i)\big\rangle_{\mat[38D[K
w_i(t)\,\Granite(e_i)\big\rangle_{\mathcal H_K}
      =\langle\Granite(x),m(t)\rangle_{\mathcal H_K},
\]

with the feature‑space memory vector

\[
m(t)=\sum_i w_i(t)\,\Granite(e_i).
\]

Thus recall is linear in kernel space even though it appears nonlinear in o[1D[K
original cue space.

---

### 6. False Recall Region  

Define intended region \(B(r)=\bigcup_i B_i(r)\). The false‑recall (spuriou[8D[K
(spurious) set is

\[
F_\theta(t)=E_\theta(t)\setminus B(r),
\]

and its measure gives the false‑recall rate

\[
\mathrm{FR}(t)=\frac{\mu(F_\theta(t))}{\mu(E_\theta(t))}
               \quad(\text{provided }\mu(E_\theta(t))>0).
\]

---

### 7. Memory Capacity Bound  

If cue space has finite measure \(\mu(X)<\infty\) and each event’s recall n[1D[K
neighborhood \(B_i(r_\theta)\) must stay disjoint, the maximal number of no[2D[K
non‑interfering memories is

\[
N_{\max}\le \frac{\mu(X)}{b_\theta},
\]

where \(b_\theta=\mu(B_i(r_\theta))\) is the measure of a single recall bal[3D[K
ball.

---

### 8. Recoverability–Basin Relation  

For a Gaussian memory trace, recoverability (the fraction of space where we[2D[K
weight exceeds threshold \(\theta\)) scales with the ecphoric radius

\[
r_\theta = \sigma\sqrt{2\log\!\left(\frac{w_i}{\theta}\right)},
\]

so that

\[
\reco(e_i)=\mu(B_i(r_\theta))
\]

increases monotonically with \(r_\theta\) (and thus with \(\sigma\)).

---

These formulae encapsulate the core mathematical relationships presented in[2D[K
in the document, linking dynamics of memory weights to theoretical limits o[1D[K
on recall fidelity and capacity.

