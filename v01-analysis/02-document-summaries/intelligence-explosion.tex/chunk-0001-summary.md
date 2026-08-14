**Parity Invariance Under Stochastic Drift**

*Lemma*: Let \(p(t) \in \mathbb{Z}\) be the tape pointer evolving under the[3D[K
the AmbiBF movement rule: at each step, \(p(t+1)=p(t)+\eta_t\) where \(\eta[6D[K
\(\eta_t \in \{-1,+1\}\) with equal probability. Then the parity \(p(t)\bmo[10D[K
\(p(t)\bmod 2\) is deterministic given \(p(0)\): \(p(t)\bmod 2 = (p(0)+t)\b[10D[K
(p(0)+t)\bmod 2\) for all \(t\).

*Proof*: Since \(\eta_t \in \{-1,+1\}\), we have \(\eta_t \equiv 1 \pmod{2}[8D[K
\pmod{2}\) in both cases. Therefore, \(p(t+1) \equiv p(t)+1 \pmod{2}\) at e[1D[K
every step, regardless of the random outcome. By induction, \(p(t) \equiv p[1D[K
p(0)+t \pmod{2}\).

*Corollary*: A program executing on AmbiBF can always determine the current[7D[K
current parity of the tape pointer by counting steps, even with no access t[1D[K
to the pointer's absolute position. This is the foundational invariant on w[1D[K
which the counter encoding described in the original language specification[13D[K
specification rests.

*Remark*: The lemma shows that parity is the unique positional invariant pr[2D[K
preserved under arbitrary symmetric random walks on \(\mathbb{Z}\): all oth[3D[K
other modular invariants are destroyed by stochastic drift. The AmbiBF enco[4D[K
encoding strategy is therefore not merely clever but optimal given the subs[4D[K
substrate's constraints.

