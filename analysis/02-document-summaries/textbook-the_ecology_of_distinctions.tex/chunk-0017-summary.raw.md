**Information‑geometric spaces**

The world we live in can be thought of as a set of “objects’’ (states, even[4D[K
events) whose structure is fixed by two kinds of operations:

1. **Preserved distinctions** – the differences that survive when we look a[1D[K
at the system from some point of view.
2. **Erased distinctions** – the differences that are hidden because they d[1D[K
do not affect our current observation.

These preserved and erased differences give rise to a *metric* (or distance[8D[K
distance) on the space of objects: two states are “close’’ if observing the[3D[K
them yields essentially the same information, i.e., if many of their distin[6D[K
distinguishing features have been suppressed. In this way the geometry of t[1D[K
the space is determined entirely by what we choose to keep and what we choo[4D[K
choose to hide.

---

**Entropy**

Entropy measures **hidden multiplicity beneath a distinction structure**.  [K

If an outcome \(x_i\) occurs with probability \(p_i\), its *surprisal* (or [K
information content) is \(-\log p_i\). The entropy of the whole space is th[2D[K
therefore

\[
H(X)= -\sum_{i=1}^{n} p_i\,\log p_i,
\]

the expected surprisal. Rare events resolve more uncertainty, so they contr[5D[K
contribute larger negative values to the sum and thus raise the total entro[5D[K
entropy.

---

### Uniform Distinction Spaces  

Assume all states are equally likely: \(p_i = 1/n\). Substituting into Shan[4D[K
Shannon’s formula,

\[
H(X)= -n\left(\frac{1}{n}\log\frac{1}{n}\right)= \log n .
\]

**Maximum‑Entropy Principle**

Among all probability distributions on a finite set of size \(n\), entropy [K
is maximized when the distribution is uniform. This follows from maximizing[10D[K
maximizing

\[
H = -\sum_i p_i\log p_i
\]

subject to \(\sum_i p_i = 1\) using Lagrange multipliers, which forces all [K
\(p_i\) equal.

---

### Conditional Entropy  

Observing a variable \(Y\) reduces the hidden multiplicity of another varia[5D[K
variable \(X\). The conditional entropy is

\[
H(X|Y)= H(X,Y)-H(Y),
\]

the amount of uncertainty left after learning \(Y\).

**Lemma:** For any random variables, conditioning never increases entropy.

*Proof:* By definition,

\[
I(X;Y)= H(X)-H(X|Y)\ge 0,
\]

so

\[
H(X|Y)= H(X)-I(X;Y) \le H(X).
\]

---

### Mutual Information  

Mutual information quantifies the shared distinction structure between two [K
variables:

\[
I(X;Y)= H(X)+H(Y)-H(X,Y).
\]

It measures how much one distinction constrains another.

**Theorem (Non‑negativity):** \(I(X;Y)\ge 0\) for all random variables, bec[3D[K
because

\[
I(X;Y)= D_{\mathrm{KL}}(P(X,Y)\| P_X\otimes P_Y) \ge 0.
\]

---

### Relative Entropy and Divergence  

The Kullback–Leibler divergence between distributions \(P\) and \(Q\) is

\[
D_{\mathrm{KL}}(P\|\! Q)=\sum_i P_i\log\frac{P_i}{Q_i}.
\]

It is not a true metric (it need not be symmetric or satisfy the triangle i[1D[K
inequality) but it is fundamental in information theory.

**Theorem (Gibbs Inequality):** For any probability distributions \(P\) and[3D[K
and \(Q\),

\[
D_{\mathrm{KL}}(P\|\! Q)\ge 0,
\]

with equality iff \(P=Q\). This follows from the concavity of \(-x\log x\).[4D[K
x\).

---

### Boltzmann Entropy  

For a macrostate compatible with \(\Omega\) microstates, Boltzmann entropy [K
is

\[
S_B = k_B\log\Omega.
\]

Here “macrostate’’ is a coarse distinction that groups many microscopic con[3D[K
configurations. The term \(\log\Omega\) counts the hidden multiplicity (the[4D[K
(the number of distinct ways to realize the macroscopic description).

---

### Distinction Entropy  

Given a partition \(\{P_1,\dots,P_n\}\) with cell sizes \(m_i = |P_i|\), de[2D[K
define

\[
S_D = \sum_{i=1}^{n} p_i\log m_i .
\]

\(S_D\) measures the average hidden multiplicity in each distinguished cell[4D[K
cell. If every cell is a singleton (\(m_i=1\)), then \(S_D=0\); perfect dis[3D[K
distinguishability means no hidden structure remains.

---

### Entropy Production  

When entropy evolves with time, its production rate is

\[
\sigma = \frac{dS}{dt}.
\]

**Theorem (Second Law of Distinction Dynamics):** If distinctions are lost [K
at a constant rate \(\lambda\) per unit “time”, then the distinction capaci[6D[K
capacity \(D(t)\) decays as \(D(t)= D_0 e^{-\lambda t}\). Defining entropy [K
by \(S = -D\), we have

\[
\frac{dS}{dt}= \lambda D,
\]

which is non‑negative because \(D\ge 0\). Hence progressive distinction ero[3D[K
erosion yields monotonic increase in entropy, embodying the mathematical ex[2D[K
expression of the Second Law.

---

These concepts—entropy as hidden multiplicity, conditional entropy reflecti[8D[K
reflecting information gain, mutual information quantifying shared structur[8D[K
structure, and Boltzmann/ distinction entropy measuring unresolved possibil[8D[K
possibilities—are unified under a geometric view where **the geometry (metr[5D[K
(metric) is determined by which distinctions are preserved versus those tha[3D[K
that are suppressed**. This framework unifies thermodynamics, statistical m[1D[K
mechanics, communication theory, computation, dynamical systems, biology, a[1D[K
and cosmology through the common theme of information‑driven structure.

