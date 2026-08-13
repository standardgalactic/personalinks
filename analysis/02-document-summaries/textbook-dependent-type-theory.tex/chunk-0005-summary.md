**Normalization by Historical Evaluation (NbHE) in the Historical Kernel**

---

### 1. Motivation

Ordinary term‑normalisation answers “*t → v*”.  
Historical normalisation asks for a *pair*:

\[
(H,t)\;\Downarrow\;(H',v),
\]

where **\(H'\)** records exactly how the canonical value **\(v\)** was buil[4D[K
built.
Thus NbHE computes both an observable result and its constructive provenanc[9D[K
provenance.

---

### 2. Historical Semantic Domain

Instead of a plain semantic domain \(\mathcal V\) we work with  

\[
\widehat{\mathcal V}= \mathcal V\times\mathcal H,
\]

with **\(\mathcal H\)** the category of replayable histories (introduced ea[2D[K
earlier).  
Every value now carries:

* an observable term,  
* its construction history,  
* dependency graph, and  
* a replay certificate.

The invariant

\[
\History(\llbracket t\rrbracket_H)=H_t
\]

ensures that the stored history is exactly the one responsible for **\(t\)*[8D[K
**\(t\)**.

---

### 3. Evaluation Function

For an environment **Env** we define  

\[
\llbracket t \rrbracket_H : Env \rightarrow \widehat{\mathcal V},
\]

which *reflexively* records every historical step taken to build the semant[6D[K
semantic
representation of **\(t\)**.

---

### 4. Reflection & Reification

*Reflection*: neutral terms are turned into historical objects:

\[
\uparrow : Ne \rightarrow \widehat{\mathcal V}.
\]

Reification gives canonical syntax while preserving provenance:

\[
\downarrow : \widehat{\mathcal V} \rightarrow Nf,
\qquad
(\downarrow(v),\History(v)).
\]

Thus the kernel outputs a *pair* (normal form + history) rather than just t[1D[K
the
syntax.

---

### 5. Normalisation Procedure

Normalising **\(t\)** with respect to history **\(H\)** proceeds in three p[1D[K
phases:

1. **Evaluate** – compute \(\llbracket t \rrbracket_H\) in the historical s[1D[K
semantic
   domain.
2. **Replay‑aware computation** – perform reduction steps only when they ch[2D[K
change
   the replay graph (i.e., involve a new declaration, bind, collapse, meld,[5D[K
meld,
   or universe). This prevents repeated evaluation of unchanged prefix[6D[K
prefixes.
3. **Reflect & Reify** – apply \(\downarrow\) to obtain canonical syntax wh[2D[K
while keeping
   the original history.

Formally:

\[
\operatorname{Norm}(H,t) = \downarrow\bigl(\llbracket t \rrbracket_H\bigr).[19D[K
\rrbracket_H\bigr).
\]

---

### 6. Historical Sharing & Incremental Normalisation

If **\(t_1\)** and **\(t_2\)** share a historical prefix **\(H_0\)**, we on[2D[K
only need to
evaluate the *new* fragment **\(e\)**:

\[
\operatorname{Norm}(H') = \operatorname{Extend}\bigl(\operatorname{Norm}(H)[49D[K
\operatorname{Extend}\bigl(\operatorname{Norm}(H), e\bigr).
\]

Thus computation depends on novelty rather than repeated evaluation of iden[4D[K
identical
segments.

---

### 7. Replay‑Guided Conversion

Two types **\(A\)** and **\(B\)** are definitionally equal iff:

1. Their normal forms coincide,
2. The histories (including dependency graphs) are replay equivalent, and
3. Their constructions satisfy historical equivalence.

Observable equality alone is insufficient; constructive provenance also dec[3D[K
decides
conversion.

---

### 8. Correctness

**NbHE** satisfies two fundamental correctness properties:

* **Semantic Preservation:** Normalisation preserves observable behaviour.
* **Provenance Consistency:** The returned normal form together with its hi[2D[K
history
  uniquely determines the original term up to definitional equality.

These follow directly from the design of replay (history preservation, incr[4D[K
incrementality,
and reduction only when needed).

---

### 9. Complexity & Caching

Because histories are immutable, replayed prefixes can be cached:

* If **\(H_0\)** has already been normalised, subsequent extensions start f[1D[K
from
  the cached state.
* Normalisation of an extension is linear in the number of new events,
  leading to overall complexity \(O(n)\) where **\(n\)** is the count of ne[2D[K
newly
  introduced events.

---

### 10. Central Role

Normalization by Historical Evaluation exemplifies how replay underpins man[3D[K
many kernel
features:

* **Normalisation** (by evaluation),
* **Type checking** (using history‑aware reduction),
* **Dependency reconstruction**,  
* **Proof verification**,  

and more—mirroring the principle that *history, not context, is the core se[2D[K
semantic
object*.

---

This framework shows how constructive histories replace traditional context[7D[K
contexts,
offering a unified view where normalisation itself becomes a historical ope[3D[K
operation.

