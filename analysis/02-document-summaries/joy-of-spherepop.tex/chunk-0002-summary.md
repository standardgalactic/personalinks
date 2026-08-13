**Abstract Syntax and Denotational Semantics**

A Spherepop program (Π) is formally a finite ordered list of nodes:

\[
\mathsf{AST} = [n_1,n_2,\dots ,n_k].
\]

Each node `ni` belongs to one of two primitive families:

| Type | Form | Semantic Role |
|------|------|----------------|
| **Event** | `Pop(t)`, `Refuse(t)`, `Bind(a,b)`, `Collapse(q)` | Irreversi[9D[K
Irreversible modifications to the option‑space (see Section 4). |
| **Declaration** | `Let(x,e)` | Purely referential binding; erased after n[1D[K
name resolution. |

---

### 1. Option‑Space Category

Let \(\mathcal{O}\) be the category whose:

* **Objects** are all possible option‑spaces (collections of viable futures[7D[K
futures), and  
* **Morphisms** are monotone maps that preserve inclusion, i.e., for any `f[2D[K
`f : X → Y` we have  

  \[
  f(A) ⊆ f(B) \text{ whenever } A ⊆ B.
  \]

Key properties:

* **Composition** is defined pointwise (`(g∘f)(x)=g(f(x))`) and yields anot[4D[K
another morphism.  
* **Identity** for an object `X` is the inclusion into itself, `id_X : X → [K
X`.  
* No morphisms have inverses; most are not bijections—this encodes *irrever[8D[K
*irreversibility*.

---

### 2. Interpretation (Functor)

Define a functor \(\llbracket·\rrbracket : \mathsf{AST} \to \mathcal{O}\) b[1D[K
by mapping each node:

| Node | Functorial Meaning |
|------|---------------------|
| `Pop(t)` or `Refuse(t)` | \(P_t : X → X \setminus t\) (exclude target `t`[3D[K
`t`). |
| `Bind(a,b)` | \(B_{a\prec b} : X → X[a \prec b]\) (make `b` precede `a`).[5D[K
`a`). |
| `Collapse(q)` | \(C_q : X → X/{\sim_q}\) (identify all elements related b[1D[K
by policy `q`). |

The interpretation of a declaration node is the identity morphism:

\[
\llbracket Let(x,e)\rrbracket = \text{id}_X .
\]

---

### 3. Compositionality

Given two programs Π₁ = `[n₁,…,n_m]` and Π₂ = `[n_{m+1},…,n_k]`, their comb[4D[K
combined semantic effect is the sequential composition of morphisms:

\[
\llbracket \Pi_1;\Pi_2 \rrbracket = (\llbracket\Pi_2\rrbracket) \circ (\llb[5D[K
(\llbracket\Pi_1\rrbracket).
\]

Because each morphism in \(\mathcal{O}\) is monotone and composition respec[6D[K
respects the ordering of options, every Spherepop program defines a *well‑d[7D[K
*well‑defined* transformation on option‑spaces without ambiguity.

---

### 4. Determinism & Auditability

Since the syntax admits **only linear histories**, evaluation order is fixe[4D[K
fixed:

1. Process nodes strictly left‑to‑right.
2. Each node applied yields exactly one morphism (no branching or backtrack[9D[K
backtracking).

Consequently, a program’s semantic interpretation is deterministic given an[2D[K
an initial option‑space `X₀`. Replaying the same AST always produces the sa[2D[K
same transformation, enabling verification and reproducibility—essential fo[2D[K
for formal reasoning about irreversible commitments.

---

### 5. Minimal Semantics

The abstract syntax deliberately omits:

* Blocks/loops,
* Conditional or branching control structures,
* Implicit updates (e.g., “reassignment”).

All semantic effects appear explicitly as nodes. This design eliminates hid[3D[K
hidden state, aligns with the philosophical claim that meaning arises only [K
from *made irreversible* choices.

---

### 6. Extension Points

Any higher‑level language built on Spherepop must translate its constructs [K
into a linear sequence of primitive AST nodes (`Pop`, `Refuse`, `Bind`, `Co[3D[K
`Collapse`, and pure declarations). Such extensions preserve linearity, thu[3D[K
thus preserving the core guarantees of irreversibility, determinism, and au[2D[K
auditability.

---

**Summary**

The abstract syntax models programs as immutable histories—linear sequences[9D[K
sequences of irreversible events that transform option‑spaces in a well‑def[8D[K
well‑defined monotone way. The semantics are captured by the category \(\ma[5D[K
\(\mathcal{O}\) with its natural interpretation functor, guaranteeing that [K
every Spherepop program is a deterministic transformation without hidden re[2D[K
revision paths or rollback mechanisms. This formalism underlies the philoso[7D[K
philosophical commitments: irreversibility, auditability, and the notion th[2D[K
that “meaning” is paid for rather than predicted.

