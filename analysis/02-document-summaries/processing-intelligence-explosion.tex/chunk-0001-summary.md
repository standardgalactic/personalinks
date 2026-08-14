**Parity Invariance Under Stochastic Drift**

**Lemma [Parity Preservation] (labelled as \ref{lemma:parity})**  
Let \(p(t) \in \mathbb{Z}\) be the tape pointer evolving under the AmbiBF m[1D[K
movement rule:

\[
p(t+1)=p(t)+\eta_t,\qquad 
\eta_t\in\{-1,+1\},\;\text{with equal probability}.
\]

Then the parity \(p(t)\bmod 2\) is deterministic given the initial value \([2D[K
\(p(0)\):

\[
p(t)\bmod 2 = (p(0)+t)\bmod 2 \quad\text{for all } t\ge 0.
\]

**Proof**  
Because each step adds either +1 or ‑1, we have  

\[
\eta_t \equiv 1 \pmod{2}
\]

in both cases. Hence  

\[
p(t+1) = p(t)+\eta_t \equiv p(t)+1 \pmod{2}.
\]

By induction on \(t\),

\[
p(0)\bmod 2,\; p(1)\bmod 2=p(0)+1\bmod 2,\;
p(2)\bmod 2=p(0)+2\bmod 2=\dots
\]

Thus  

\[
p(t)\bmod 2 = (p(0)+t)\bmod 2 \quad\forall t.
\tag{*}
\]  

**Corollary [Dead Reckoning]**  
A program executing on AmbiBF can always determine the current parity of th[2D[K
the tape pointer by counting steps, even without knowing its absolute posit[5D[K
position. This invariant underpins counter encoding in the original languag[7D[K
language specification.

**Remark** – The lemma shows that *parity is the unique positional invarian[8D[K
invariant preserved under arbitrary symmetric random walks on \(\mathbb{Z}\[13D[K
\(\mathbb{Z}\)*: all other modular invariants are erased by stochastic drif[4D[K
drift. Consequently, AmbiBF’s design deliberately exploits this property to[2D[K
to achieve reliable computation from unreliable primitives (see von Neumann[11D[K
von Neumann 1956; Cover & Thomas 2006 for analogous results).
