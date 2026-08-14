**Formal Grammar of the Spherepop Calculus**

Let  

* \(\mathcal{V}=\{x,y,z,\ldots\}\) be the countable set of variables,  
* \(\mathcal{C}=\{c_1,c_2,\ldots\}\) the constants, and  
* \(\mathcal{O}=\{\operatorname{Sphere},\operatorname{Pop},\operatorname{Me\(\mathcal{O}=\{\operatorname{Sphere},\operatorname{Pop},\operatorname{Merge},\operatorname{Choice},\operatorname{Replay},\operatorname{Refuse},\operge},\operatorname{Choice},\operatorname{Replay},\operatorname{Refuse},\operatorname{Collapse},\operatorname{Bind}\}\) the primitive operators.

The grammar of terms is defined inductively by  

\[
t=
\begin{cases}
x &\text{(variable)}\\[4pt]
c &\text{(constant)}\\[4pt]
\operatorname{Sphere}(x:A.t) &\text{(spherical abstraction)}\\[4pt]
\operatorname{Pop}(t) &\text{(pop a value)}\\[4pt]
\operatorname{Merge}(t,t) &\text{(merge two histories)}\\[4pt]
\operatorname{Choice}(p,t,t) &\text{(probabilistic branching)}\\[4pt]
\operatorname{Replay}(t,t) &\text{(re‑execution of a history)}\\[4pt]
\operatorname{Refuse}(r) &\text{(refusal to commit)}\\[4pt]
\operatorname{Collapse}(t) &\text{(commit irreversible change)}\\[4pt]
\operatorname{Bind}(t,t) &\text{(binding of related histories)}
\end{cases}
\]

**Contexts and Histories**

* Contexts are histories:  

  \[
  \Gamma=
  \begin{cases}
  \emptyset &\text{(empty)}\\
  \Gamma,e,\;e\in\{\operatorname{Open},\operatorname{Pop},\operatorname{Rep\Gamma,e,\;e\in\{\operatorname{Open},\operatorname{Pop},\operatorname{Replay},\operatorname{Merge},\operatorname{Choice},\operatorname{Collapse},\opeay},\operatorname{Merge},\operatorname{Choice},\operatorname{Collapse},\operatorname{Refuse}\}
  \end{cases}
  \]

* A history is a finite sequence:  

  \[
  H=(e_1,e_2,\ldots,e_n).
  \]

**Well‑formedness of Histories**

Every element \(e_i\) respects the dependency order:

\[
e_i\prec e_j\;\Longrightarrow\;i<j,
\]

where “\(\prec\)” denotes the required admissibility condition (no later st[2D[K
step may depend on an earlier unresolved step).

---

### Sphere Definition

A *Sphere* is recursively defined as  

\[
S=(B,I),
\]

* \(B\) – a computational boundary,  
* \(I\) – a finite computation graph.

**Nested‑Sphere Property**

Every interior node of \(I\) belongs to exactly one sphere.  
If spheres overlap, their boundaries are disjoint:

\[
S_i \subset S_j \Longrightarrow \partial S_i \cap \partial S_j = \varnothin[10D[K
\varnothing .
\]

---

### Well‑formed Programs

An admissible program corresponds to a finite directed acyclic graph  

\[
G=(V,E)
\]

together with a sphere assignment  

\[
\sigma : V \rightarrow \mathcal{S},
\]

where spheres form a partial order:

\[
(u,v)\in E \Longrightarrow 
\sigma(u) \subseteq \sigma(v)\;\vee\;
\sigma(v) \subseteq \sigma(u)\;\vee\;
\sigma(u)\parallel\sigma(v),
\]

with “\(\parallel\)” denoting independent computational regions.

---

### Operational Scheduler

The language’s operational semantics **only** act on admissible sphere assi[4D[K
assignments, ensuring that evaluation respects the geometric well‑formednes[14D[K
well‑formedness required by computation. This reflects the core philosophic[11D[K
philosophical principle: computation is fundamentally the irreversible cons[4D[K
construction of computational history through successive opening, interacti[9D[K
interaction, replay, refusal, and dissolution of bounded regions.

