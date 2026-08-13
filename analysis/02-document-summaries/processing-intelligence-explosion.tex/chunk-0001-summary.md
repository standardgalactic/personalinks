**Parity Invariance Under Stochastic Drift (Lemma \ref{lemma:parity})**

*Proof.*  
Let \(p(t)\) denote the tape pointer after \(t\) steps. By definition of th[2D[K
the \(\mathbf{AmbiBF}\) movement rule, at each step we add a random offset [K
\(\eta_t\) where  

\[
\eta_t \in \{-1,\;+1\},\qquad P(\eta_t = +1)=P(\eta_t = -1)=\tfrac12 .
\]

Since \(\eta_t \equiv 1 \pmod{2}\) in both cases, the parity (even/odd natu[4D[K
nature) of \(p(t)\) changes only by adding an odd number:

\[
p(t+1) = p(t) + \eta_{t} \equiv p(t) + 1 \pmod{2}.
\]

Thus after each step the parity flips deterministically. By induction, star[4D[K
starting from any initial value \(p(0)\),

\[
p(t) \equiv p(0) + t \pmod{2}\qquad\text{for all }t\ge 0 .
\]

Hence the parity of the pointer is completely determined by its step count [K
and the initial parity, independent of the random choices made along the wa[2D[K
way. ∎  

**Corollary [Dead Reckoning]**  
Because \(p(t)\bmod 2\) depends only on whether \(t\) is even or odd (relat[6D[K
(relative to the starting point), a program can always infer its current po[2D[K
pointer parity simply by counting steps, without needing direct access to t[1D[K
the absolute position of the tape. This invariant underlies the “counter en[2D[K
encoding” used in \(\mathbf{AmbiBF}\) semantics: each step advances the poi[3D[K
pointer’s parity, allowing stable counters and loops despite stochastic dri[3D[K
drift.

**Remark on Optimality**  
The lemma demonstrates that parity is *the unique* positional invariant pre[3D[K
preserved by arbitrary symmetric random walks on \(\mathbb{Z}\). All other [K
modular invariants (e.g., modulo‑4 or modulo‑any composite) are destroyed b[1D[K
because the sum of many independent ±1 steps introduces unpredictable odd/e[5D[K
odd/even flips. Consequently, \(\mathbf{AmbiBF}\)’s reliance on parity is n[1D[K
not merely a clever design choice but an optimal strategy for maintaining s[1D[K
structural stability in a fundamentally noisy environment.

