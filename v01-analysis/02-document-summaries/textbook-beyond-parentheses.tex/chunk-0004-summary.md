Below is a detailed explanation of the formal grammar and semantic structur[8D[K
structure described in the Spherepop Calculus section. This breakdown clari[5D[K
clarifies how terms are constructed, how contexts (histories) are formed, a[1D[K
and what rules govern their evaluation.

---

### Formal Grammar

The calculus defines its syntax using three main types:

1. **Variables**  
   \[
   \mathcal{V} = \{x,y,z,\ldots\}
   \]  
   These represent the basic symbols used in terms.

2. **Constants**  
   \[
   \mathcal{C} = \{c_1,c_2,\ldots\}
   \]  
   Constants are predefined values that can appear directly in terms.

3. **Primitive Operators**  
   \[
   \mathcal{O} =
   \{\operatorname{Sphere}, \operatorname{Pop}, \operatorname{Merge},
    \operatorname{Choice}, \operatorname{Replay}, \operatorname{Refuse},
    \operatorname{Collapse}, \operatorname{Bind}\}
   \]  
   These operators define the operations that can be applied to terms.

#### Term Construction

Terms are built inductively using:

\[
t
=
\begin{cases}
x & (\text{variable})\\[4pt]
c & (\text{constant})\\[4pt]
\operatorname{Sphere}(x:A.t) & (\text{sphere construction})\\[4pt]
\operatorname{Pop}(t) & (\text{pop operation})\\[4pt]
\operatorname{Merge}(t,t) & (\text{merge of histories})\\[4pt]
\operatorname{Choice}(p,t,t) & (\text{conditional branching})\\[4pt]
\operatorname{Replay}(t,t) & (\text{replaying a history})\\[4pt]
\operatorname{Refuse}(r) & (\text{refusal of a branch})\\[4pt]
\operatorname{Collapse}(t) & (\text{irreversible commit})\\[4pt]
\operatorname{Bind}(t,t). & (\text{binding two histories})
\end{cases}
\]

#### Contexts (Histories)

Contexts are ordered lists of historical operations:

\[
\Gamma =
\emptyset \mid \Gamma,e,
\]  

where \( e \in \{\operatorname{Open}, \operatorname{Pop}, \operatorname{Rep[17D[K
\operatorname{Replay},
\operatorname{Merge}, \operatorname{Choice}, \operatorname{Collapse},
\operatorname{Refuse}\} \).

A **History** is a finite sequence:

\[
H = (e_1,e_2,\ldots,e_n).
\]

The dependency order \( \prec \) ensures that operations in a history are
processed topologically, meaning if \( e_i \prec e_j \), then \( i < j \).

### Well‑formed Histories

Histories must satisfy:

\[
e_i \prec e_j \Longrightarrow i < j,
\]

ensuring chronological integrity. Additionally, nested spheres have disjoin[7D[K
disjoint
boundaries:

\[
S_i \subset S_j \Longrightarrow \partial S_i \cap \partial S_j = \varnothin[10D[K
\varnothing.
\]

### Sphere Definition

A **Sphere** is defined as:

\[
S = (B, I),
\]

where \( B \) is a computational boundary and \( I \) is a finite computati[9D[K
computation
graph. Interior nodes belong to exactly one sphere, ensuring clear separati[8D[K
separation of
computational regions.

### Dependency Graph

Every admissible program corresponds to a directed acyclic graph:

\[
G = (V,E)
\]  

with a **Sphere Assignment** \( \sigma : V \rightarrow \mathcal{S} \) such [K
that:

\[
(u,v) \in E \Longrightarrow 
\sigma(u) \subseteq \sigma(v) \vee \sigma(v) \subseteq \sigma(u) \vee
\sigma(u) \parallel \sigma(v).
\]

This ensures that dependencies are respected, and spheres may be independen[10D[K
independent.

### Operational Semantics

The operational semantics dictate how the language behaves:

- The parser generates a rooted forest of computational regions.
- The scheduler acts only on **admissible sphere assignments**, ensuring th[2D[K
that
  operations respect dependency constraints.

---

These components together define the core structure of the Spherepop Calcul[6D[K
Calculus,
emphasizing historical construction and geometric well‑formedness as centra[6D[K
central to
computation. If you need further elaboration on any specific rule or compon[6D[K
component,
feel free to ask!

