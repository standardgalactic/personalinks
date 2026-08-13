**Worked Example – Collapse on a Four‑Element Set**

Let us illustrate the concepts of Section 4 with a concrete history in \(\S[4D[K
\(\SP\) that involves four events.  
We take \(\Omega=\{a,b,c,d\}\) and consider three successive perturbations:[14D[K
perturbations:

1. **Eliminate event \(b\)** – this is a *Pop* operation on the set \(\{a,b[7D[K
\(\{a,b,c,d\}\).  
2. **Bind events \(c\) and \(d\)** – a *Bind* (or “merge”) that creates a n[1D[K
new composite object representing the joint occurrence of \(c\) and \(d\). [K
 
3. **Coarse‑grain by equivalence** – we identify all points differing only [K
in which one of \(\{c,d\}\) appears, i.e. \([a,b,c] = [a,b,d]\).

The full history can be written as  

\[
e_2\circ e_1,\qquad 
e_1=\text{Pop}_b,\; e_2=\text{Bind}_{cd}.
\]

---

### 1. Realization of Each Step

| Step | Object in \(\SP\) | Realized object \((p,\eta)\) in \(\RSVP\) (the[4D[K
(the simplex over the set after collapse) |
|------|-------------------|-----------------------------------------------|------|-------------------|----------------------------------------------------------------------------------------|
| **\(e_1 = \text{Pop}_b\)** | Collapse of \(b\) from \(\{a,b,c,d\}\) to a [K
single point representing \(\{a,c,d\}\). | • Fine map: \(\varphi_{e_1} : p([2D[K
p(a,b,c,d)\mapsto p'(a,c,d)=p(a)+p(c)+p(d).\)<br>• Slack: \(\eta_{e_1}(p) =[1D[K
= H(p)-H(\varphi_{e_1}\!\circ\!p)\ge0\) (Shannon entropy decrease). |
| **\(e_2 = \text{Bind}_{cd}\)** | Bind the remaining distinct events \(c,d[5D[K
\(c,d\) inside the already‑collapsed set. | • Fine map: coarse the two comp[4D[K
components of \(\{a,c,d\}\) into a single “composite” point, e.g. \(X=c d\)[3D[K
d\). <br>• Resulting space is \(\{a,X\}\). The fine map sends probabilities[13D[K
probabilities to \(\varphi_{e_2}(p(a,c,d)) = p'(a)+p'(c d)=p(a)+H_{cd}(p(c,[19D[K
d)=p(a)+H_{cd}(p(c,p(d)))\) where \(H_{cd}\) is the binary entropy of a mix[3D[K
mixture. <br>• Slack: \(\eta_{e_2}= H(p)-H(\varphi_{e_2}\!\circ\!p)\). |
| **Combined Collapse** | Apply the two steps sequentially (or as a single [K
generator that does both elimination and binding in one step). | • Composit[8D[K
Composition gives \((\iota_X,\eta_X)+(\iota_b,\eta_b)= (\iota_{X,b},\eta_{X[20D[K
(\iota_{X,b},\eta_{X,b})\) where \(\iota_{X,b}\) is the face inclusion of \[1D[K
\(a,X\) (i.e. the map sending \(p(a,c,d)\mapsto p'(a,X)\)). <br>• Slack add[3D[K
adds: \(\eta = \eta_{e_2}+\eta_{e_1}>0\) because each step removed at least[5D[K
least one degree‑of‑freedom, increasing the slack by the corresponding entr[4D[K
entropy loss. |

---

### 2. Entropy and Slack Interpretation

Suppose we start with a uniform distribution on all four events:

\[
p(a)=p(b)=p(c)=p(d)=\tfrac14 .
\]

* **Step \(e_1\) (Pop \(b\))**  
  - Fine map: \(\varphi_{e_1}(p) = p'(a,c,d)=\tfrac34\) for the point \(a,c[5D[K
\(a,c,d\).  
  - Shannon entropy before and after: \(H(p)=\log4=2\;\text{bits}\), \(H(p'[6D[K
\(H(p')=\log3<2\); thus \(\eta_{e_1}=2-\log3>0\).

* **Step \(e_2\) (Bind \(c,d\))**  
  - After the previous step we have points \([a]\) and \([\,c+d\,]\). The f[1D[K
fine map now collapses a binary variable into a single point; its entropy l[1D[K
loss is roughly \(0.5\) bits per binding operation in this uniform case (bi[3D[K
(binary entropy of mixing two equal‑probability states drops from 1 bit to [K
0.5 bits). Hence \(\eta_{e_2}\approx0.5\).

* **Total Slack**  
  The combined slack is additive:

  \[
  \eta = \eta_{e_1}+\eta_{e_2}= (2-\log3)+0.5\;\text{bits}\approx1.32\;\tex[43D[K
(2-\log3)+0.5\;\text{bits}\approx1.32\;\text{bits}>0 .
  \]

The positive slack signals that the coarse‑grained description has *recorde[8D[K
*recorded* information loss; this is precisely what Axiom \(\mathbf{\text{([23D[K
Axiom \(\mathbf{\text{(Entropy)}}\) of Section 3 guarantees.

---

### 3. Functoriality Checks

| Lemma | What it tells us for our example |
|-------|-----------------------------------|
| **\(F(\mathrm{id}) = (\mathrm{id},0)\)** | The identity history on the se[2D[K
set does nothing; its realized object is unchanged and no slack appears – c[1D[K
consistent with \(\eta=0\). |
| **Composition associativity** | Since \(e_2\) binds after \(e_1\) already[7D[K
already removed one degree of freedom, composing \((e_1,e_2)\) yields a sin[3D[K
single fine map \(\iota_{X,b}\) and slack adds linearly: \((\eta_{e_2}+\eta[18D[K
\((\eta_{e_2}+\eta_{e_1})=\eta_{(e_1\circ e_2)}\) – exactly what the lemma [K
predicts. |
| **Tensor compatibility** | If we tensor our example with a second indepen[7D[K
independent four‑element set, each component contributes its own slack (the[4D[K
(they do not interfere), giving \(\eta_{X,b}+\eta_Y\) for two copies – agai[4D[K
again matching Lemma \(F\text{-tensor}\). |

Thus the functorial properties hold for this concrete history.

---

### 4. Relation to the Structural Asymmetry Theorem

* **Asymmetry (i)–(iii)**  
  - \(\SP\) records *accumulated constraint*: each Pop/Bind step permanentl[10D[K
permanently removes degrees of freedom, so entropy never increases. In our [K
example we observed a net drop from \(2\) bits to less than \(1.5\) bits af[2D[K
after two steps.  
  - \(\RSVP\) (the simplex) can have *redistributed coherence*: the coarse‑[7D[K
coarse‑graining map need not be monotone in Shannon entropy; it can locally[7D[K
locally increase entropy by reshaping probability masses, which is captured[8D[K
captured by the positivity of slack.

* **Non‑equivalence** – Because a smooth vector field that “wiggles’’ withi[5D[K
within the simplex (e.g. \(\partial/\partial p(a) -\partial/\partial p(c d)[2D[K
d)\)) cannot be expressed as any finite sequence of Pop/Bind/Collapses, \(F[3D[K
\(F\) is not full on \(\RSVP\). This mirrors Theorem \(\text{Structural asy[3D[K
asymmetry}\).

---

### 5. Summary

- **Objects** in the example: start with four distinct points; after two op[2D[K
operations we have a single point representing “\(a\) together with either [K
\(c\) or \(d\)”.
- **Slack**: Positive, reflecting that entropy has decreased by removing in[2D[K
information (i.e., degrees of freedom) and also by mixing probabilities dur[3D[K
during binding.  
- The whole process is fully described by the functorial mapping \(F\) defi[4D[K
defined in Section 4, respecting all its lemmas and the structural asymmetr[8D[K
asymmetry highlighted in Theorem \(\text{Structural asymmetry}\).  

This worked example demonstrates how a concrete sequence of perturbations y[1D[K
yields an explicit realization \((p,\eta)\) on the simplex, shows where sla[3D[K
slack originates from entropy loss, and illustrates why \(\SP\) (discrete‑c[11D[K
(discrete‑constraint) and \(\RSVP\) (differential‑entropy transport) are no[2D[K
not equivalent categories.

