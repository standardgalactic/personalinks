**Appendix A – Incremental Execution**

Many practical systems repeatedly modify only small portions of a computati[9D[K
computation graph. Re‑computing the entire graph would be wasteful; instead[7D[K
instead we **mark only those nodes whose dependencies have changed**, retai[5D[K
retain the histories of unaffected regions, and recompute only the computat[8D[K
computational consequences of the modification. This mechanism naturally su[2D[K
supports interactive programming, graphical editors, continuous simulation,[11D[K
simulation, spreadsheet computation, and reactive user interfaces.

**Incrementality emerges from dependency analysis rather than from speciali[8D[K
specialized programming constructs.**

---

### 1. Overview

* The runtime described here is intentionally minimal:  
  * Maintain a composition graph.  
  * Load operator libraries.  
  * Schedule executable nodes.  
  * Record persistent histories.  
  * Process refusal and collapse events.  
  * Apply graph rewrites when requested.

* Every richer computational phenomenon (typing, theorem proving, compilati[9D[K
compilation, optimization, fuzzy inference, symbolic reasoning, neural comp[4D[K
computation, repair, learning) is realized by supplying different operator [K
libraries and graph transformations rather than enlarging the execution eng[3D[K
engine itself.

* The economy of a small, mathematically uniform runtime follows from treat[5D[K
treating **composition**, not any particular programming language or logica[6D[K
logical system, as the primitive computational operation (the “graph‑first [K
philosophy”).

---

### 2. Incremental Execution Details

1. **Marked Nodes** – When an update occurs, only nodes whose input depende[7D[K
dependencies have changed are flagged for re‑evaluation.  
2. **History Preservation** – Unaffected parts of the graph keep their prev[4D[K
previous histories, ensuring that incremental changes do not erase prior co[2D[K
computational context.  
3. **Re‑evaluation** – Only those portions of the computation that depend o[1D[K
on the modified inputs are recomputed; all other results remain as they wer[3D[K
were previously computed.

This yields a cost‑effective way to maintain consistent state in large, dyn[3D[K
dynamic graphs such as spreadsheets, simulation models, or interactive UIs.[4D[K
UIs.

---

### 3. Relation to Richer Computational Phenomena

The economy of the minimal runtime enables **extension** via operator libra[5D[K
libraries and graph transformations without altering its core semantics:

* Typing → add a type‑checking library.  
* Theorem proving → incorporate proof‑search operators.  
* Compilation → include code‑generation nodes.  
* Optimization → introduce heuristics that prune unnecessary recomputation.[14D[K
recomputation.

Thus, composition remains the **primitive** operation; all other features a[1D[K
are built on top of it.

---

### 4. Towards a Composition‑First Calculus

The operational machinery developed in previous appendices (graphs, operato[7D[K
operator algebras, histories) suggests we can formalize these ideas into a [K
calculus analogous to the lambda calculus or the calculus of constructions [K
**but with composition as its primitive**.

#### 4.1 Primitive Judgments

* The most basic judgment is  

  \[
  H
  \vdash
  G
  \Downarrow
  H',
  \]

  meaning “executing graph \(G\) extends history \(H\) into history \(H'\).[15D[K
history \(H'\).”

* No variables, typing contexts, or logical propositions appear; only graph[5D[K
graphs and histories matter.

#### 4.2 Primitive Rules

1. **Identity** – An empty graph leaves the history unchanged:  

   \[
   \frac{ }{
     H
   \vdash
   \operatorname{Id}
   \Downarrow
   H.
   }
   \]

2. **Composition** – Sequential execution of two graphs \(G_1\) and \(G_2\)[7D[K
\(G_2\):  

   \[
   \frac{
     H
   \vdash
   G_1
   \Downarrow
   H_1
   \qquad
     H_1
   \vdash
   G_2
   \Downarrow
   H_2
   }{
     H
   \vdash
   G_2\circ G_1
   \Downarrow
   H_2.
   }
   \]

* This single rule replaces a large collection of language‑specific evaluat[7D[K
evaluation rules (e.g., function application, pipeline execution).

#### 4.3 Operator Evaluation

If node \(n\) has operator \(f\) and its inputs evaluate to values \(v_1,\d[8D[K
\(v_1,\dots,v_k\), the evaluation rule is  

\[
\frac{
   v
= f(v_1,\ldots ,v_k)
}{
   H
\vdash
   n
\Downarrow
   (H,e),
}
\]

where \(e=(n,f,v)\). The history now records **both** the computation and i[1D[K
its result.

#### 4.4 Refusal

Constraint systems, proof assistants, repair systems, and interactive reaso[5D[K
reasoning often need to reject a continuation:

\[
\frac{
   r
\text{ is a refusal reason}
}{
   H
\vdash
   n
\Downarrow
   (H,\Refuse(r)).
}
\]

* Refusal does not terminate the calculus; subsequent rules may branch, rep[3D[K
repair, or replace the rejected continuation.

#### 4.5 Collapse

When a value \(v\) is already produced and committed:

\[
\frac{
   v
\text{ has been evaluated}
}{
   H
\vdash
   \Collapse(v)
\Downarrow
   (H,\Collapse(v)).
}
\]

* This explicitly separates evaluation from commitment, providing uniform t[1D[K
treatment of speculative execution, interactive computation, symbolic reaso[5D[K
reasoning, and fuzzy evaluation.

---

### 5. Conservativity Principle

An important property: **richer computational systems extend rather than re[2D[K
replace** the primitive rules.  

*Typed systems add typing judgments.*  
*Proof systems add proof judgments.*  
*Dependent type theories add universe judgments.*  

These extensions do **not** alter the operational rules above; they merely [K
constrain which graphs are considered admissible.

Consequently, we have:

> **Theorem (Conservativity).** Every extension of the composition‑first ca[2D[K
calculus obtained by adding descriptive judgments while leaving the operati[7D[K
operational rules unchanged is conservative with respect to execution. Thus[4D[K
Thus richer systems enrich computation without enlarging its primitive sema[4D[K
semantics.

---

### 6. The Composition‑First Thesis

The resulting hierarchy can be summarized as:

\[
\text{composition} \;\Longrightarrow\; \text{graphs} \;\Longrightarrow\; \t[2D[K
\text{histories}
\;\Longrightarrow\; \text{execution}
\;\Longrightarrow\; \text{optimization}
\;\Longrightarrow\; \text{description}
\;\Longrightarrow\; \text{verification}.
\]

*Execution precedes description.* Descriptions (syntax, types, logical syst[4D[K
systems) **constrain** execution but do not generate it.

---

### 7. Bibliography

1. Aho A., Lam M.S., Sethi R., Ullman J.D. – *Compilers: Principles, Techni[6D[K
Techniques, and Tools* (2nd ed.). Addison‑Wesley, 2007.  
2. Baader F., Nipkow T. – *Term Rewriting and All That*. Cambridge Universi[8D[K
University Press, 1998.  
3. Bird R. – *Introduction to Functional Programming Using Haskell*. Prenti[6D[K
Prentice Hall, 1998.  
4. Backus J.P. – “Can Programming Be Liberated from the von Neumann Style?”[7D[K
Style?” ACM SIGPLAN Notices, 21(8):613–641, 1978.  
5. Barendregt H.P. – *The Lambda Calculus: Its Syntax and Semantics*. North[5D[K
North‑Holland, 1984.  
6. Bird R. – *Introduction to Functional Programming Using Haskell*. Prenti[6D[K
Prentice Hall, 1998.  
7. Bondy J.A., Murty U.S.R. – *Graph Theory with Applications*. Macmillan, [K
1976.  
8. Book R.H., Otto F. – *String‑Rewriting Systems*. Springer, 1984.  
9. Cormen T.H., Leiserson C.E., Rivest R.L., Stein C. – *Introduction to Al[2D[K
Algorithms*, 4th ed. MIT Press, 2022.  
10. Cousot P., Cousot R. – “Abstract Interpretation.” Proceedings of the AC[2D[K
ACM Symposium on Principles of Programming Languages, 1977.  
11. Gonthier G. – *Formal Proof — The Four‑Color Theorem*. Notices of the A[1D[K
American Mathematical Society, 55(11):1382–1393, 2008.

---

**End of Appendix A – Incremental Execution**
