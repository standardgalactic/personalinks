**Working Example – Collapse on a Finite Option Space**

Let us consider a concrete, small‑size example to illustrate the definition[10D[K
definition and functorial properties of the collapse map \(F:\SP\to\RSVP\) [K
described in the text.  
We will work with three options \(\Omega=\{1,2,3\}\) (so the simplex is \(\[3D[K
\(\Delta(\Omega)\cong[-1,0]\times[-1,0]\times[-1,0]\) after a convenient af[2D[K
affine change of coordinates).

---

### 1. The Setup

| Step | Description |
|------|-------------|
| **Initial state** \(p_0\) | Probability vector \((p_0(1),p_0(2),p_0(3)) =[1D[K
= (0.4,0.3,0.3)\). |
| **Event \(U=\{1\}\)** | Apply the *elimination* generator: keep only outc[4D[K
outcomes in the complement of \(U\) (i.e., \(\{2,3\}\)). The coarse‑grainin[14D[K
coarse‑graining map \(\varphi_\sim(p_0)=p'_0\) is obtained by marginalising[13D[K
marginalising over option 1. |
| **Event \(V=\{2\}\)** | Apply the *elimination* generator again: keep out[3D[K
outcomes in the complement of \(V\) (i.e., \(\{1,3\}\)). Now we coarse‑grai[11D[K
coarse‑grain from state \(p'_0=(0.3,0.7,0)\) to obtain \(p''_0=\varphi_\sim[20D[K
\(p''_0=\varphi_\sim(p'_0)=(0.5,0.5,0)\). |

---

### 2. Realization of Each Collapse

#### (a) First collapse \(\Pop_U\)

*Coarse‑graining map*:  

\[
\varphi_\sim(p)=
\begin{pmatrix}
p(2)\\ p(3)
\end{pmatrix}.
\]

*Fine‑to‑coarse entropy difference*:

\[
\eta_U(p)=SF_{\Omega}(p)-\varphi_\sim^*\!SF_{\Omega/U}(p)
          =-I[p]-(-H_{2,3}[p]).
\]

For \(p_0=(0.4,0.3,0.3)\),

\[
-I[p_0]=-\bigl(0.4\log_2 0.4+0.3\log_2 0.3+0.3\log_2 0.3\bigr)
        \approx 1.5219,
\]
\[
-H_{2,3}[p'_0]=-(0.7\log_2 0.7+0.3\log_2 0.3)\approx 0.8814.
\]

Thus  

\[
\eta_U(p_0)=1.5219-0.8814=0.6405>0,
\]
indicating a positive slack that records the entropy lost by discarding opt[3D[K
option 1.

#### (b) Second collapse \(\Pop_V\) on the resulting state \(p'_0=(0.3,0.7,[16D[K
\(p'_0=(0.3,0.7,0)\)

*Coarse‑graining map*:  

\[
\varphi_\sim(p')=
\begin{pmatrix}
p'(1)\\ p'(3)
\end{pmatrix}.
\]

*Entropy difference*:

\[
\eta_V(p'_0)= -I[p'_0]-(-H_{1,3}[p''])
          =- (0.3\log_2 0.3+0.7\log_2 0.7+0\log_2 0)
           + (0.5\log_2 0.5+0.5\log_2 0.5)
          \approx 0.0619.
\]

The total slack accumulated after both steps is  

\[
\eta_{U}+\eta_V\approx 0.6405+0.0619=0.7024>0,
\]
which reflects the cumulative entropy loss of discarding two distinct event[5D[K
events.

---

### 3. Functoriality in Action

1. **Identity Preservation (Lemma F‑id)**  
   The identity morphism on \((\Omega,\mathcal{A})\) is left unchanged:
   \(F(\operatorname{id})=(\operatorname{id},0)\). This matches the definit[7D[K
definition of a
   functor: the trivial history produces no slack.

2. **Composition Preservation (Lemma F‑comp)**  
   Applying \(\Pop_V\) after \(\Pop_U\) yields:

   \[
   F(\Pop_V\circ\Pop_U)= (F(\Pop_U)\circ F(\Pop_V))
   =((p_1,p_3),\eta_U)\circ((p'_1,p'_3),\eta_V)
   =((p''_0),( \eta_U+\eta_V)),
   \]

   which is exactly the composition of two realizations with additive slack[5D[K
slack,
   as stated in Lemma F‑comp.

3. **Associativity of Slack (Lemma slack‑assoc)**  
   If we instead collapse \(U\cup V\) directly, the resulting map would be [K
a single
   coarse‑graining:

   \[
   \iota_{U\cup V}=(p''_0),\qquad 
   \eta_{U\cup V}= \eta_U+\eta_V,
   \]

   showing that slack composition is associative.

4. **Tensor Compatibility (Lemma F‑tensor)**  
   For the tensor product of two three‑element spaces, \(\Delta(\Omega\time[20D[K
\(\Delta(\Omega\times\Omega')
   =\Delta(\Omega)\times\Delta(\Omega')\). The entropy sum law holds:
   \(SF_{\Omega\times\Omega'}(p)=SF_\Omega(p)+SF_{\Omega'}(p')\), so the fu[2D[K
functor
   respects products as shown in Lemma F‑tensor.

---

### 4. Interpretation

- **Slack as Entropy Loss**: The positive \(\eta\) values record precisely [K
how much Shannon entropy is discarded when we coarsen a probability distrib[7D[K
distribution.
- **Monotonicity of Collapse**: Because every collapse step reduces the sim[3D[K
simplex dimension,
  any further composition cannot increase total slack, reflecting the irrev[5D[K
irreversible
  nature of coarse‑graining in physics (the second law).
- **Functorial Viewpoint**: The map \(F\) is not just a mere set‑to‑set ass[3D[K
assignment; it
  preserves the compositional structure and entropy budget of \(\SP\), maki[4D[K
making it a
  well‑defined symmetric monoidal functor from \(\SP\) into the category of[2D[K
of smooth
  spaces with vector fields (\(\RSVP\)).

---

**Conclusion**

This worked example demonstrates how concrete probabilities are transformed[11D[K
transformed via the collapse map, how slack (entropy loss) accumulates addi[4D[K
additively under composition, and how these properties align with the categ[5D[K
categorical axioms listed in the text. The functorial description thus prov[4D[K
provides a rigorous mathematical framework for understanding coarse‑grainin[14D[K
coarse‑graining processes as irreversible entropy transports.
