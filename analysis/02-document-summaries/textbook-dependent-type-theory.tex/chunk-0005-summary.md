**Normalization by Historical Evaluation (NbHE) – Summary**

The historical calculus extends the ordinary Calculus of Constructions by g[1D[K
giving every term a *construction history* together with its observable nor[3D[K
normal form.  This dual output is what we call **Historical Normalization**[15D[K
Normalization**:

---

### Core Idea  

Instead of reducing an expression \(t\) only to a value \(v\), NbHE produce[7D[K
produces a pair  
\[
(\downarrow(v), \History(v)),
\]  
where \(\History(v)\) records the replayable history that generated the nor[3D[K
normal form.  This preserves the invariant

\[
\History(\llbracket t \rrbracket_H)=H_t,
\]

i.e., the recorded history exactly matches the history introduced during th[2D[K
the original derivation.

---

### Semantic Domain  

The semantic domain is enlarged to  
\[
\widehat{\mathcal V}= \mathcal V\times\mathcal H,
\]  
with \(\mathcal H\) being the category of replayable histories (as defined [K
in the replay engine).  Every value now carries both an observable part and[3D[K
and a provenance part.

---

### Evaluation Function  

For any environment \(Env\),

\[
\llbracket t \rrbracket_H : Env \rightarrow \widehat{\mathcal V}
\]

maps neutral terms into this enriched domain.  Neutral terms are first refl[4D[K
reflected (see reflection below) so that the resulting semantic object alre[4D[K
already contains a history.

---

### Reflection  

The operator  
\[
\uparrow: Ne \rightarrow \widehat{\mathcal V}
\]  
converts neutral terms into their historical semantical representation, ini[3D[K
initially carrying only the corresponding declaration event.  Future reduct[6D[K
reductions monotonically extend this history.

---

### Reification  

To obtain canonical syntax,

\[
\downarrow : \widehat{\mathcal V} \rightarrow Nf
\]

projects the semantic object to normal form while preserving its constructi[10D[K
construction history:

\[
\operatorname{Norm}(H,t) = \downarrow(\llbracket t \rrbracket_H).
\]

---

### Evaluation Procedure  

1. **Evaluate** the observable term \(t\) into the historical domain:  
   \(\llbracket t \rrbracket_H\).

2. **Perform replay‑aware semantic computation**: continue reductions only [K
when a new history element appears (i.e., when replay encounters a novel ev[2D[K
event).  This prevents redundant re‑evaluation of shared prefixes.

3. **Reify** the resulting semantical object into canonical syntax, retaini[7D[K
retaining its history:  
   \(\downarrow(\llbracket t \rrbracket_H)\).

---

### Historical Sharing  

If two terms share an earlier replay history \(H_0\),

\[
t_1 = H_0; e_1,\qquad
t_2 = H_0; e_2,
\]

only the new events \(e_1\) and \(e_2\) require semantic evaluation.  All p[1D[K
previously computed parts remain valid because histories are immutable.

---

### Incremental Normalization  

For a derived history \(H' = H; e\),

\[
\operatorname{Norm}(H') = \operatorname{Extend}(\operatorname{Norm}(H), e).[3D[K
e).
\]

Thus the cost of normalization scales linearly with newly introduced events[6D[K
events, not total library size.

---

### Conversion & Correctness  

Conversion between types \(A\) and \(B\) succeeds only if:

1. Their normal forms coincide (observable equality).  
2. Their histories are replay‑equivalent (i.e., they represent the same con[3D[K
constructive derivation).  
3. Dependency graphs satisfy historical equivalence, ensuring that shared s[1D[K
substructures reflect identical provenance.

---

### Correctness Theorem  

If a history \(H\) is accepted by the replay engine, then

\[
\Replay(H) = S,
\]

where \(S\) is the kernel state originally produced by \(H\).  Every typing[6D[K
typing judgment reconstructed during replay is derivable in the declarative[11D[K
declarative historical calculus.

---

### Complexity  

Assuming all previously verified prefixes are cached,

\[
T(n)=O(n),
\]

with respect to the number of new events \(n\), because each step involves [K
only linear graph traversal, dependency verification, and reduction of the [K
newly introduced suffix.

---

**Conclusion**

Normalization by Historical Evaluation integrates constructive provenance d[1D[K
directly into evaluation.  It yields both an observable normal form *and* i[1D[K
its full construction history, enabling precise conversion checking while a[1D[K
avoiding redundant re‑evaluation of shared prefixes and guaranteeing that e[1D[K
every derived expression is fully accounted for in the kernel’s trusted sta[3D[K
state.
