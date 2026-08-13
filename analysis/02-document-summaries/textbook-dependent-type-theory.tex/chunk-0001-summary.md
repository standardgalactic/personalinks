**Historical Substitution – A Constructive Interpretation**

In conventional dependent type theory substitution is treated as a purely s[1D[K
syntactic replacement:

* `t[x:=a]` simply swaps every free occurrence of the variable `x` with the[3D[K
the term `a`.  
* The correctness of this operation rests only on avoiding capture; after t[1D[K
the swap, the provenance of the variables no longer matters.

Spherepop replaces this view by treating substitution as a **historical** ([1D[K
(i.e., constructive) process:

1. **Objects Carry Provenance** – A term is not just a string but a complet[7D[K
completed historical construction embedded in a dependency graph `D(t)` tha[3D[K
that records how it was built.
2. **Substitution as an Operation on Histories** – Replacing one variable b[1D[K
by another therefore transports both the observable syntax and its full con[3D[K
constructive history.

---

### Historical Environments

When we have proven:

* `H ⊢ a : A`

the substitution environment is written as  

\[
\sigma = \{ x_1 ↦ (a_1, H_1), x_2 ↦ (a_2, H_2), … \}
\]

where each substituted object is paired with the history that constructed i[1D[K
it.  
Thus a term `t` together with an environment `\sigma` is denoted:

\[
t[H,x↦a]
\]

rather than the plain `t[x:=a]`.

---

### Definition of Historical Substitution

**Definition (Historical Substitution)**  

Given histories `H₁`, `H₂` such that:

* `H₁ ⊢ a : A`,
* `H₁; Declare(x : A) ⊢ t : B`,

the historical substitution is defined as:

\[
t[H,x↦a] = \text{result of replacing every free } x \text{ in } t
\]

while **extending** the dependency graph `D(t)` with all dependencies requi[5D[K
required to construct `a`.  
Thus substitution never discards provenance; it enriches it.

---

### Dependency Preservation

*Theorem (Dependency Preservation)*  

Let `D(t)` be the dependency graph of `t`. After performing historical subs[4D[K
substitution, the new term’s graph is:

\[
D(t[H,x↦a]) = D(t) \cup D(a),
\]

together with edges introduced by the substitution site.  
Hence substitution always *preserves* (and possibly enlarges) provenance.

---

### Compositionality of Substitutions

Multiple substitutions compose naturally:

If  

\[
\sigma_1 = \{ x ↦ (a, H_a) \},
\qquad
\sigma_2 = \{ y ↦ (b, H_b) \},
\]

then  

\[
t[\sigma_1][\sigma_2] = t[\sigma_2 ∘ \sigma_1],
\]

provided the usual capture‑avoidance conditions hold and their dependency g[1D[K
graphs are compatible.

---

### Substitution & Beta Reduction

*Theorem (Historical β‑Reduction)*  

Ordinary reduction is:

\[
(\lambda x.t)\,a \longrightarrow t[x:=a].
\]

Spherepop interprets it as:

\[
(H, (\lambda x.t)\,a) \longrightarrow (H', t[H,x↦a]),
\]

where `H'` extends `H` by recording the substitution event itself.  
Thus evaluation simultaneously builds a new observable term **and** records[7D[K
records how that term arose historically.

---

### Historical Capture Avoidance

In the conventional system, capture is checked purely by variable names. In[2D[K
In Spherepop:

* Two variables with identical textual names but distinct declaration event[5D[K
events (e.g., `e_x ≠ e_x'`) must be distinguished by their provenance.
* Alpha conversion becomes a **historical renaming** that acts on the under[5D[K
underlying declaration events, naturally supporting hygienic macros, proof [K
replay, distributed construction, and incremental compilation.

---

### Historical Substitution Lemma

*Theorem (Historical Substitution Lemma)*  

If `H ⊢ a : A` and `H; Declare(x : A) ⊢ t : B`, then:

\[
H ⊢ t[H,x↦a] : B[H,x↦a],
\]

and the dependency graph of the resulting derivation is precisely the histo[5D[K
historical composition (union with appropriate edges) of those of `t` and `[1D[K
`a`.

---

**Summary**

By viewing substitution as an operation on **constructive histories**, Sphe[4D[K
Spherepop preserves every piece of provenance that ordinary syntactic subst[5D[K
substitution discards. This enriched notion ensures:

* No accidental loss or merging of distinct construction events.
* A richer semantics for dependent types, where terms carry full contextual[10D[K
contextual narratives.
* Natural extensions to macro hygiene and distributed proof systems, becaus[6D[K
because all variable identities are globally unique by declaration history [K
rather than lexical spelling alone.

