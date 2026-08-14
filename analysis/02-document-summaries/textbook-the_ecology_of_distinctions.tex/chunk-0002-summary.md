**States as Equivalence Classes of Histories**

Fix a time \(t\). Define an equivalence relation on the history space \(\ma[5D[K
\(\mathcal{H}\) by  

\[
h_1 \sim_t h_2 \;\Longleftrightarrow\; h_1(t)=h_2(t).
\]

The quotient set  

\[
[X] = \{\,[\gamma] : \pi_H(\gamma)=x\,\mid x\in X\}
\]

is the **state space \(X\)**, where each element is an equivalence class of[2D[K
of histories that terminate at the same state.

---

**History Surplus**

For a given state \(x\) and time \(t\),

\[
\Omega_H(x,t)=|\pi_H^{-1}(x)|
\]

counts how many distinct trajectories (histories) end in \(x\).  
If \(\Omega_H(x,t)>1\), the state hides substantial historical structure.

---

**The Law of Historical Compression**

> *Every state description is a compression of a larger history description[11D[K
description. History ontology strictly contains state ontology.*

Formally, for any non‑trivial dynamical system there exist histories \(h_1\[6D[K
\(h_1\neq h_2\) with \(\pi_H(h_1)=\pi_H(h_2)\). Hence the mapping \(\pi_H:\[9D[K
\(\pi_H:\mathcal{H}\to X\) is many‑to‑one:

\[
|\mathcal{H}|>|X|,\qquad X=\pi_H(\mathcal{H})\text{ but }\mathcal{H}\supset[19D[K
}\mathcal{H}\supsetneq X.
\]

Thus state ontology (states) is a strict subset of history ontology (trajec[7D[K
(trajectories).

---

**The Information‑Loss Theorem**

For any non‑injective \(\pi_H\) the entropy satisfies  

\[
H(\mathcal{H}) > H(X).
\]

Indeed, many histories map to the same state, so conditioning on \(X\) disc[4D[K
discards part of the original information.

---

**The Markov Assumption as a Compression Hypothesis**

Define the path‑dependence index  

\[
P_D = I(H_t; x_{t+1}\mid x_t).
\]

A process is **Markovian** iff this index vanishes, i.e., future states dep[3D[K
depend only on the current state:

\[
P(x_{t+1}\mid H_t,x_t)=P(x_{t+1}\mid x_t),
\]

which is precisely the projection from history space onto state space. Henc[4D[K
Hence Markov dynamics can be viewed as a lossless compression when \(P_D=0\[8D[K
\(P_D=0\).

---

These results formalize why, in many dynamical systems, preserving only the[3D[K
the current state discards crucial historical information that could affect[6D[K
affect future behavior.
