**Entropy and Hidden Multiplicity**

Entropy is a measure of *hidden multiplicity*—the number of unresolved poss[4D[K
possibilities that remain after a distinction has been drawn. In informatio[10D[K
information‑geometric spaces, this “multiplicity” reflects how much additio[7D[K
additional structure (or uncertainty) is still present beneath the apparent[8D[K
apparent ordering imposed by distinctions.

---

### Shannon Entropy

For a finite state space \(X = \{x_1,\dots ,x_n\}\) with probability distri[6D[K
distribution
\(P = (p_1,\dots ,p_n)\), the Shannon entropy is defined as  

\[
H(X)= -\sum_{i=1}^{n} p_i \log p_i .
\]

The term \(-\log p_i\) is called **surprisal**; rare events carry more info[4D[K
information because they resolve greater uncertainty. Hence, entropy measur[6D[K
measures the *expected* number of hidden states compatible with a given obs[3D[K
observation.

---

### Uniform Distinction Spaces

When every state is equally likely (\(p_i = 1/n\)),  

\[
H(X)= -\log (1/n) = \log n .
\]

**Maximum Entropy Principle:**  
Among all probability distributions on an \(n\)‑element set, the uniform di[2D[K
distribution maximizes entropy. This follows from maximizing \(H\) using La[2D[K
Lagrange multipliers under the constraint \(\sum_i p_i = 1\).

---

### Conditional Entropy

Observing additional information can reduce uncertainty:

\[
H(X|Y)= H(X,Y) - H(Y),
\]

where \(H(X|Y)\) is the *conditional entropy*—the remaining hidden multipli[8D[K
multiplicity after conditioning on \(Y\).

**Property:** Conditioning never increases entropy:  

\[
H(X|Y) \le H(X).
\]

---

### Mutual Information

Mutual information quantifies how much knowing one variable constrains anot[4D[K
another:

\[
I(X;Y)= H(X)+H(Y)-H(X,Y),
\]

or equivalently,

\[
I(X;Y)= [#H(X)-H(X|Y)] + [#H(Y)-H(Y|xX)] .
\]

**Non‑negativity:** By the non‑negativity of Kullback–Leibler divergence,  [K


\[
I(X;Y) \ge 0,
\]

with equality iff \(P = Q\).

---

### Relative Entropy (KL Divergence)

For distributions \(P\) and \(Q\),

\[
D_{\mathrm{KL}}(P|Q)=\sum_i P_i \log \frac{P_i}{Q_i}.
\]

Although not a true metric, KL divergence measures distinguishability:

- **Gibbs Inequality:** \(D_{\mathrm{KL}}(P|Q) \ge 0\) (Jensen’s inequality[10D[K
inequality).
- In the infinitesimal limit, it generates the Fisher information metric.

---

### Boltzmann Entropy

For a macrostate with \(\Omega\) compatible microstates,

\[
S_B = k_B \log \Omega .
\]

This is analogous to distinction entropy: the macrostate represents a coars[5D[K
coarse distinction, and each of the \(\Omega\) microstates hides that multi[5D[K
multiplicity.

---

### Distinction Entropy

Given a partition \(\{P_1,\dots ,P_n\}\) with cell sizes \(m_i = |P_i|\), t[1D[K
the *distinction entropy* is  

\[
S_D = \sum_{i=1}^{n} p_i \log m_i .
\]

- If all cells are singletons (\(m_i = 1\)), then \(S_D = 0\) (perfect dist[4D[K
distinguishability).
- Larger cell sizes correspond to higher hidden multiplicity.

---

### Entropy Production

For time‑dependent entropy \(S(t)\), the production rate is  

\[
\sigma = \frac{dS}{dt}.
\]

**Second Law of Distinction Dynamics:**  
If distinctions decay at a constant rate \(\lambda\),

\[
D(t)= D_0 e^{-\lambda t},
\]
where \(D\) is distinction capacity. Entropy, defined as \(-D\), satisfies [K
 

\[
\frac{dS}{dt}= \lambda D \ge 0,
\]

showing that progressive distinction erosion implies monotonic entropy incr[4D[K
increase—a geometric expression of the Second Law.

--- 

These concepts unify thermodynamic entropy with information theory and dyna[4D[K
dynamical systems by viewing entropy as a measure of hidden structure prese[5D[K
preserved by distinctions.

