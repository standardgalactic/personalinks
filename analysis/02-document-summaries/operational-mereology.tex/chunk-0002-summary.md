**Extracted Durable Theoretical Information**

---

### 1. Operational Semantics of Event Rules  

| Rule | Formal Presentation (small‑step) | Purpose / Effect |
|------|----------------------------------|------------------|
| **POP** (non‑member) | \(\displaystyle\frac{x\notin H}{⟨\texttt{POP}(x)\;[21D[K
H}{⟨\texttt{POP}(x)\;P,\;\langle H,\preceq,L,\approx,M\rangle⟩\to ⟨P,\langl[9D[K
⟨P,\langle H\cup\{x\},\preceq,L,\approx,M\rangle⟩}\) | Adds an element *x* [K
to the heap **H** (i.e., it becomes a handle). The transition is idempotent[10D[K
idempotent for members: if \(x\in H\) then POP is either an error or no‑op.[6D[K
no‑op. |
| **POP – Idempotent Variant** | \(\displaystyle\frac{x\in H}{⟨\texttt{POP}[16D[K
H}{⟨\texttt{POP}(x)\;P,\Sigma⟩\to ⟨P,\Sigma⟩}\) | Captures the “no‑op” case[4D[K
case (e.g., for engineering semantics). |
| **MERGE** | \(\displaystyle\frac{x,y\in H}{⟨\texttt{MERGE}(x,y)\;P,\Sigma[33D[K
H}{⟨\texttt{MERGE}(x,y)\;P,\Sigma⟩\to ⟨P,\Sigma[\preceq:=\preceq\cup\{(rep_[37D[K
⟨P,\Sigma[\preceq:=\preceq\cup\{(rep_\Sigma(x),rep_\Sigma(y))\}]⟩}\) | Reco[4D[K
Records a directed containment edge between the representatives of *x* and [K
*y*. |
| **LINK** | \(\displaystyle\frac{x,y\in H}{⟨\texttt{LINK}(x,y,\ell)\;P,\Si[34D[K
H}{⟨\texttt{LINK}(x,y,\ell)\;P,\Sigma⟩\to ⟨P,\Sigma[L:=L\cup\{(rep_\Sigma(x[33D[K
⟨P,\Sigma[L:=L\cup\{(rep_\Sigma(x),rep_\Sigma(y),\ell)\}]⟩}\) | Associates [K
a label **ℓ** (link relation) between the two representatives. |
| **COLLAPSE** | \(\displaystyle\frac{x,y\in H}{⟨\texttt{COLLAPSE}(x,y)\;P,[30D[K
H}{⟨\texttt{COLLAPSE}(x,y)\;P,\Sigma⟩\to ⟨P,\mathsf{collapse}(\Sigma,x,y)⟩}[34D[K
⟨P,\mathsf{collapse}(\Sigma,x,y)⟩}\) <br> *Definition of collapse*:<br>\[
\approx' = \mathsf{cl}(\approx\cup\{(x,y)\}),\quad<br>
\preceq' = \mathsf{norm}_{rep_{\Sigma'}}(\preceq),\quad<br>
L' = \mathsf{norm}_{rep_{\Sigma'}}(L),\quad<br>
M' = \mathsf{norm}_{rep_{\Sigma'}}(M)
\] <br>Result: \(\mathsf{collapse}(\Sigma,x,y)=⟨H,\preceq',L',\approx',M'⟩\[60D[K
\(\mathsf{collapse}(\Sigma,x,y)=⟨H,\preceq',L',\approx',M'⟩\). | Explicitly[10D[K
Explicitly rewrites *x* and *y* as identified entities (identity‑as‑event).[20D[K
(identity‑as‑event). |
| **META** | \(\displaystyle\frac{\tau\text{ well‑formed in }\Sigma}{⟨\text[15D[K
}\Sigma}{⟨\texttt{META}(\tau,k,v)\;P,\Sigma⟩\to ⟨P,\Sigma[M:=M\cup\{(rep_\S[27D[K
⟨P,\Sigma[M:=M\cup\{(rep_\Sigma(\tau),k)\mapsto v}]⟩}\) | Updates metadata [K
without altering the heap or relations. |

*Key points*:  
- **POP** is the only rule that mutates *H*. All other rules touch only rel[3D[K
relations (`≈`, `L`) and/or metadata (`M`).  
- **MERGE**, **LINK**, and **COLLAPSE** formalize how handles become relate[6D[K
related (containment, labeling, identification).  

---

### 2. Temporal Parthood (Induced Containment Relation)

For a prefix of events \(P_{\leq t}=e_1\cdots e_t\) define the replayed sta[3D[K
state:

\[
⟨P_{\leq t},\Sigma_0⟩ \to^{*} ⟨\varepsilon,\Sigma_t⟩,
\]

where \(\Sigma_0 = \langle\emptyset,\preceq,L,\approx,M\rangle\) is the emp[3D[K
empty initial state.

**Time‑indexed parthood**

\[
x\leq_t y \quad\text{iff}\quad rep_{\Sigma_t}(x)\text{ reaches }rep_{\Sigma[12D[K
}rep_{\Sigma_t}(y)\text{ via }{\preceq}_t^{*}.
\]

Interpretation: *Parthood is a historical fact witnessed by replay*, i.e., [K
it depends on the chronological order of events.

---

### 3. Safety Properties Induced by the Semantics  

| Lemma / Property | Statement | Proof Sketch |
|------------------|-----------|--------------|
| **Existence by Construction** | If \(x\in H_t\) in \(\Sigma_t\), then the[3D[K
there exists an index \(i\leq t\) with event \(e_i=\texttt{POP}(x)\). | Onl[3D[K
Only rule POP adds elements to *H*; membership implies a prior POP. |
| **No Predicate‑Generated Objects** | No derivation step introduces a new [K
handle except via POP. | Inspection of all transition rules shows only POP [K
mutates *H*. |
| **Explicit Identity** | If \(rep_{\Sigma_t}(x)=rep_{\Sigma_t}(y)\) and \([2D[K
\(x\neq y\), then some COLLAPSE event relating the equivalence classes occu[4D[K
occurred at or before time \(t\). | Identification occurs solely through mo[2D[K
modifications of \(\approx\) (via COLLAPSE); other rules do not change repr[4D[K
representatives. |

---

### 4. Theorems on Determinism & Replay Equivalence  

**Determinism (Theorem)**  
Fix a deterministic representative‑selection policy for `rep`. For any conf[4D[K
configuration \(⟨P,\Sigma⟩\), there exists at most one \(\langle P',\Sigma'[10D[K
P',\Sigma'\rangle\) such that the transition holds.

*Proof*: Each rule matches only the head constructor of the event sequence [K
and prescribes a unique state update. The only non‑determinism is in repres[6D[K
representative choice during `COLLAPSE`; with a fixed deterministic policy,[7D[K
policy, the update is unique.

**Replay Equivalence (Theorem)**  
If two programs share the same prefix \(P_{\leq t}\), replaying that prefix[6D[K
prefix from the same initial state yields the identical final state \(\Sigm[7D[K
\(\Sigma_t\).

*Proof*: By determinism, evaluation proceeds via the same unique transition[10D[K
transition sequence for both programs.

---

### 5. Philosophical Foundations  

- **Ontology as Induction**: Ontological commitments arise only by replayin[8D[K
replaying events; nothing is assumed a priori in an empty state.  
- **Historical Parthood**: Parthood is not static but time‑indexed, reflect[7D[K
reflecting the “historical fact” view of relationships.  
- **Identity as Event**: `COLLAPSE` makes identity explicit (labels become [K
identified) and preserves the history through the collapse function \(\math[7D[K
\(\mathsf{collapse}\).  

---

### 6. Bibliographic Context  

The fragment references foundational works in set theory, logic, and catego[6D[K
category theory:

- Zermelo (1908) – early axiomatic foundations of set theory.  
- Fraenkel (1922) – contributions to the axiomatization of mathematics.  
- Goodman (1951, 1960s) – seminal work on mereology (“the calculus of indiv[5D[K
individuals”).  
- Varzi (2005), Lawvere & Schanuel (1997) – modern categorical approaches t[1D[K
to ontology and perception.  

These references support the claim that the presented semantics aligns with[4D[K
with established philosophical and logical traditions concerning identity, [K
containment, and time.

---

**Summary**

The fragment presents a deterministic small‑step operational semantics for [K
a system of event rules (`POP`, `MERGE`, `LINK`, `COLLAPSE`, `META`) applie[6D[K
applied to a state consisting of a heap **H**, partial order **≤**, labelin[7D[K
labeling relation **L**, equivalence relation **≈**, and metadata **M**. Ke[2D[K
Key theoretical outcomes include:

- Unique, deterministic evolution of system states.
- Parthood being defined by reachability in replayed (time‑indexed) paths.
- Identity expressed explicitly via `COLLAPSE`, preserving historical conte[5D[K
context.

These elements together form a coherent framework for reasoning about dynam[5D[K
dynamic systems where objects emerge and merge through observable events.

