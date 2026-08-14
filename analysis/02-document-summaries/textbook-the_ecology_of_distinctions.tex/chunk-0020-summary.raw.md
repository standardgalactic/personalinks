Below are compact “summary‑formula” versions of the key results that appear[6D[K
appear throughout the document.

---

### 1. Memory Decay (Exponential Forgetting)

* **Weight dynamics**  
  \[
  \frac{dw_i}{dt}= -\lambda_i w_i ,\qquad \lambda_i\ge0 .
  \]

* **Solution**  
  \[
  w_i(t)=w_i(0)\,e^{-\lambda_i t}.
  \]

* **Memory field (single cue)**  
  \[
  M(x,t)=\sum_i w_i(0) e^{-\lambda_i t} K(x,e_i).
  \]

**Exponential Forgetting Theorem**

If all decay rates satisfy  

\[
\lambda_i\ge\lambda_{\min}>0,
\]

then for any time \(t\)

\[
M(x,t)\le e^{-\lambda_{\min}t}\,M(x,0).
\]

*Proof sketch*: each term is bounded by \(e^{-\lambda_{\min}t}\) and the su[2D[K
sum of non‑negative weights gives the inequality.

---

### 2. Reinforcement

Adding a constant reinforcement signal  

\[
r_i(t)=r_i\quad(\text{constant}),
\]

the dynamics become  

\[
\frac{dw_i}{dt}= -\lambda_i w_i + \eta_i r_i .
\]

**Solution**

\[
w_i(t)=w_i(0)e^{-\lambda_i t}+ \frac{\eta_i r_i}{\lambda_i}\bigl(1-e^{-\lam[31D[K
r_i}{\lambda_i}\bigl(1-e^{-\lambda_i t}\bigr).
\]

**Reinforced Memory Equilibrium Theorem**

Under constant reinforcement the equilibrium weight is  

\[
w_i^*=\frac{\eta_i r_i}{\lambda_i}.
\]

*(Proof: set \(\partial w_i/\partial t=0\) → \(-\lambda_i w_i+\eta_i r_i=0\[6D[K
r_i=0\).)*

---

### 3. Kernel Representation of Memory

Feature map \(\Granite:X\to\mathcal H_K\) satisfies  

\[
K(x,e)=\langle\Granite(x),\Granite(e)\rangle_{\mathcal H_K}.
\]

Hence the memory field can be written as a linear functional:

\[
M(x,t)=\big\langle\Granite(x),\,m(t)\big\rangle_{\mathcal H_K},
\qquad 
m(t)=\sum_i w_i(t)\,\Granite(e_i).
\]

**Kernel Representation of Memory Proposition**

The memory field is linear in kernel feature space (though nonlinear in ori[3D[K
original cue space).

---

### 4. False Recall

Define intended recall region  

\[
B(r)=\bigcup_i B_i(r),
\]
where \(B_i(r)=\{x:d(x,e_i)<r\}\).  
False‑recall region:

\[
F_\theta(t)=E_\theta(t)\setminus B(r).
\]

*False Recall Rate*

\[
\mathrm{FR}(t)=\frac{\mu(F_\theta(t))}{\mu(E_\theta(t))}
\quad(\text{provided }\mu(E_\theta(t))>0).
\]

---

### 5. Memory Capacity Bound

Assume each memory has a disjoint recall neighborhood of radius \(r_\theta\[11D[K
\(r_\theta\) and cue space measure  

\[
\mu(X)<\infty.
\]

If the ball measure is  

\[
b_\theta=\mu(B_i(r_\theta)),
\]

the maximum number of non‑interfering memories is

\[
N_{\max}\le \frac{\mu(X)}{b_\theta}.
\]

**Noninterference Capacity Bound Theorem**

For unambiguous recall (disjoint ecphoric neighborhoods),

\[
N\le \frac{\mu(X)}{b_\theta}.
\]

*(Proof: the union of \(N\) disjoint balls has measure at most \(Nb_\theta\[12D[K
\(Nb_\theta\), which must be ≤ \(\mu(X)\).)*

---

### 6. Recoverability–Basin Relation (Repair Interpretation)

For a Gaussian trace with weight \(w_i>\theta\),

\[
r_\theta = \sigma\sqrt{2\log\!\bigl(w_i/\theta\bigr)}.
\]

Thus recoverability is proportional to the basin radius:

**Recoverability–Basin Proposition**

For single‑trace Gaussian memory,

\[
\text{recoverability}\propto r_\theta,
\]
i.e. it increases monotonically with \(r_\theta\) (and therefore with \(\si[5D[K
\(\sigma\sqrt{2\log(w_i/\theta)}\)).

*(Proof: the basin of influence under Euclidean distance is monotone in rad[3D[K
radius, so larger ecphoric neighborhoods imply higher recoverability.)*

---

These concise formulae capture the essential mathematical relations derived[7D[K
derived throughout the document and can be used as reference points for fur[3D[K
further analysis or implementation.

