**Historical Substitution – A Constructive Interpretation**

In conventional dependent type theory substitution (β‑reduction) is treated[7D[K
treated as a purely syntactic replacement:

\[
t[x:=a]\;\text{means replace every free }x\text{ by }a,
\]

and correctness depends only on avoiding variable capture.  In the Spherepo[8D[K
Spherepop kernel, however, substitution is *historical*: it replaces not ju[2D[K
just symbols but whole constructive constructions and records their provena[7D[K
provenance.

---

### Historical Environments

When a term \(t\) has already been proved to inhabit a type (e.g.,  

\[
H \vdash a : A,
\]

where \(H\) is the current history), we introduce a **historical environmen[10D[K
environment**  

\[
\sigma = \{ x_1 \mapsto (a_1,H_1),\; x_2 \mapsto (a_2,H_2),\ldots\},
\]

which pairs each variable with the *history* that constructed its value.  S[1D[K
Substitution is therefore written as  

\[
t[H,x\mapsto a],
\]

indicating “substitute \(a\) for \(x\) **within history** \(H\).”

---

### Definition of Historical Substitution

Let  

1. \(H \vdash a : A\) – the object \(a\) is already constructed in some his[3D[K
history \(H\), and  
2. \(H;\operatorname{Declare}(x:A) \vdash t : B\) – we intend to replace fr[2D[K
free occurrences of \(x\) by \(a\) inside term \(t\).

Then **historical substitution** is defined as:

> Replace every free occurrence of \(x\) with \(a\) *and* extend the depend[6D[K
dependency graph of \(t\) so that it now includes all dependencies required[8D[K
required for constructing \(a\).

Formally:

\[
t[H,x\mapsto a] \;=\;
\text{the term obtained by ordinary substitution, but together with history[7D[K
history } H.
\]

---

### Dependency Preservation

The resulting object inherits the richer provenance captured in its depende[7D[K
dependency graph.  Let  

\(D(t)\) be the set of dependencies built into \(t\) before substitution.  [K

After applying \(\sigma = (x \mapsto a)\),

\[
D(t[H,x\mapsto a]) = D(t) \cup D(a),
\]

plus any new edges introduced by the substitution itself (e.g., edges from [K
the substitution site to the proof steps that built \(a\)).  Thus **no prov[4D[K
provenance is ever lost**; it is merely expanded.

---

### Compositionality

Multiple substitutions compose naturally.  If  

\[
\sigma_1 = \{ x \mapsto a, H_a\},\qquad
\sigma_2 = \{ y \mapsto b, H_b\},
\]

then

\[
t[\sigma_1][\sigma_2] \;=\; t[\sigma_2\circ\sigma_1],
\]

provided the substitution sites do not conflict (standard capture‑avoidance[17D[K
capture‑avoidance).  This preserves both semantic correctness and historica[9D[K
historical integrity.

---

### Substitution vs. Beta Reduction

The ordinary reduction rule is  

\[
(\lambda x.t)\,a \;\longrightarrow\; t[x:=a].
\]

In Spherepop we record this as a *historical* event:

\[
(H,\;(\lambda x.t)a) \;\longrightarrow\; (H',\;t[H,x\mapsto a]),
\]

where \(H'\) is the history extended by the substitution.  Thus evaluation [K
simultaneously builds a new observable term **and** a permanent historical [K
record of how that term arose.

---

### Historical Capture Avoidance

Traditional α‑conversion renames bound variables symbolically, but in Spher[5D[K
Spherepop we also rename their *historical identity* because two variables [K
may share the same name yet originate from different declaration events \(e[3D[K
\(e_x \neq e_{x'}\).  Consequently, substitution respects not only syntacti[8D[K
syntactic capture rules but also distinct provenance.  This natural extensi[7D[K
extension supports hygienic macros, proof replay, distributed proof constru[7D[K
construction, and incremental compilation.

---

### Historical Substitution Lemma

If  

\[
H \vdash a : A
\]

and  

\[
H;\operatorname{Declare}(x:A) \vdash t : B,
\]

then after substitution we have  

\[
H \vdash t[H,x\mapsto a] : B[H,x\mapsto a],
\]

and the dependency graph of the resulting derivation is exactly the histori[7D[K
historical composition (union with edges to \(a\)’s construction history). [K
 This lemma shows that the familiar substitution properties survive unchang[7D[K
unchanged in the constructive setting.

---

**In Summary**

Historical substitution reframes β‑reduction as a *constructive* process: i[1D[K
it replaces terms while preserving and extending their entire provenance.  [K
Every new term carries with it a full dependency graph, enabling richer rea[3D[K
reasoning about proofs (e.g., capture avoidance based on historical identit[7D[K
identity) without sacrificing the familiar computational behavior of depend[6D[K
dependent type theory.
