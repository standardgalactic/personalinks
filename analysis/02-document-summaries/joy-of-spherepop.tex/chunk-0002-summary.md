**Abstract Syntax and Denotational Semantics**

A Spherepop program is formally a finite ordered list (AST) of nodes:

\[
\mathsf{AST} = [n_1,\; n_2, \dots , n_k],
\]

where each node $n_i$ is either an **event** or a **declaration**. The orde[4D[K
ordering of the nodes captures temporal succession rather than computation.[12D[K
computation.

---

### Event Nodes

Event nodes encode irreversible operations on option‑spaces:

| Node | Formal Form | Semantic Interpretation |
|------|-------------|------------------------|
| Pop  | $\mathsf{Pop}(t)$ | Restricts future options: $X \;\xrightarrow{\t[17D[K
\;\xrightarrow{\text{pop}}\; X|_{\neg t}$ (exclude target $t$). |
| Refuse | $\mathsf{Refuse}(t)$ | Same geometric exclusion as `Pop`; distin[6D[K
distinguished for ethical/accounting purposes. |
| Bind  | $\mathsf{Bind}(a,b)$ | Introduces precedence: $X \;\xrightarrow{\[16D[K
\;\xrightarrow{\text{bind}}\; X[a \prec b]$ (make $b$ precede $a$). |
| Collapse | $\mathsf{Collapse}(q)$ | Applies a collapse policy $q$: $X \;\[3D[K
\;\xrightarrow{\text{collapse}}\; X/{\sim_q}$ (identify distinctions under [K
$q$). |

No compound event forms exist; each node is atomic and must be interpreted [K
sequentially.

---

### Declaration Nodes

Declarations bind identifiers to expressions in a purely referential enviro[6D[K
environment:

\[
\mathsf{Let}(x,e) \;\longrightarrow\; x := e,
\]

where the expression $e$ is evaluated without affecting semantic state. Dec[3D[K
Declarations are later erased after name resolution, guaranteeing they cann[4D[K
cannot influence option‑spaces.

---

### Semantic Category

Define $\mathcal{O}$ as a category whose:

* **Objects** are (potentially infinite) option‑spaces.
* **Morphisms** $f : X \to Y$ are monotone transformations that:
  * Preserve inclusion ($X \subseteq Y$);
  * Are closed under composition;
  * Possess identity morphisms for each object.

$\mathcal{O}$ is **not a groupoid**: most morphisms lack inverses, embodyin[8D[K
embodying the irreversibility of Spherepop’s semantics.

---

### Interpretation (Denotational Mapping)

Each node maps to a morphism in $\mathcal{O}$:

| Node | Denotation |
|------|------------|
| $\mathsf{Pop}(t)$ | $X \xrightarrow{\text{pop}} X_{\neg t}$ – exclude tar[3D[K
target $t$. |
| $\mathsf{Refuse}(t)$ | Same as `Pop`; distinguished semantically. |
| $\mathsf{Bind}(a,b)$ | $X \xrightarrow{\text{bind}} X[a \prec b]$ – enfor[5D[K
enforce ordering. |
| $\mathsf{Collapse}(q)$ | $X \xrightarrow{\text{collapse}} X/{\sim_q}$ – i[1D[K
identify distinctions via policy $q$. |

**Declarations** map to the identity morphism on $\mathcal{O}$, ensuring th[2D[K
they are purely referential and do not alter semantic state.

---

### Compositional Semantics

The interpretation of an entire AST proceeds by sequential composition:

1. Start with initial option‑space $X_0$.
2. For each node $n_i$:
   * If $n_i$ is a declaration, resolve names (identity on $\mathcal{O}$) a[1D[K
and continue.
   * Otherwise, apply the corresponding morphism from above to obtain $X_{i[5D[K
$X_{i+1}$.

The resulting state $X_k$ represents the settled world produced by the prog[4D[K
program. Because each step is monotone and irreversible, the final space re[2D[K
reflects a cumulative “settled” configuration rather than a recomputed comp[4D[K
computation.

---

**Summary**

- The surface language enforces syntactic irreversibility to guarantee that[4D[K
that programs describe histories, not mutable states.
- Semantically, Spherepop operates in a category $\mathcal{O}$ of monotone [K
transformations on option‑spaces, preserving inclusion and composition but [K
lacking inverses (non‑groupoid).
- Programs are linear ASTs where each node maps directly to a deterministic[13D[K
deterministic morphism, ensuring auditability, reproducibility, and the abs[3D[K
absence of hidden rollback mechanisms.
