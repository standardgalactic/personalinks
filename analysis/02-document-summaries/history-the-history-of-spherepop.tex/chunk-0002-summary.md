**Spherepop – Core Semantics**

In Spherepop an *expression* is a nested labeling that encodes the current [K
state of knowledge:

```
Expr ::= Value | Sphere
Sphere ::= ( Label : Expr* )
```

A *history* is simply a sequence of events, each of which is one of the fou[3D[K
four primitive actions:

| Event type | Formal signature | Role in semantics |
|------------|------------------|--------------------|
| **Pop**    | pop( Label )     | Removes (abandons) a sphere from the curr[4D[K
current expression. |
| **Collapse** | collapse( Label, Equiv ) | Explicitly identifies two histo[5D[K
histories as equivalent via an equivalence relation `Equiv = { (v₁~v₂), … }[1D[K
}`. This is a *semantic merge* that can be undone only by later events. |
| **Refusal**| refuse( Label, Set ) | Declares a set of future options (the[4D[K
(the predicate “refused”) as unavailable from this point onward. It bounds [K
the option space without removing anything already committed to. |
| **Binding**| bind( Label, Predicate ) | Links a later commitment (label) [K
to a condition expressed by `Predicate = Identifier`. This creates forward [K
constraints that can be revisited or re‑interpreted. |

A *configuration* couples an expression with its authoritative history:

```
Config ::= < Expr , History >
```

Evaluation is the relation `< Config => New Config >` produced by applying [K
**one** event to a configuration.

---

### Key Semantic Themes

1. **Refusal ≠ Undoing**  
   Refusal merely shrinks the set of admissible future events; it does not [K
delete anything already present in the expression or history.

2. **Collapse = Explicit Identification**  
   When histories diverge (they cannot be merged without violating monotoni[8D[K
monotonicity), a *collapse* event makes them equivalent for practical purpo[5D[K
purposes, creating an *implicit merge* that can later be revisited by furth[5D[K
further events.

3. **Regret as a Property of History**  
   A history exhibits *regret* if it becomes strictly more constrained than[4D[K
than another reachable history from the same prefix:
   \[
   O_h \prec O_{h'}
   \]
   Regret is not an error; it signals that irreversible commitments have na[2D[K
narrowed possibilities beyond what could be achieved earlier.

4. **Meaning Arises From Sequences, Not Terminal States**  
   The meaning of a Spherepop system emerges from the *order* and *type* of[2D[K
of events (refusals, bindings, collapses) rather than any single final expr[4D[K
expression or configuration.

---

### Formal Confluence & Divergence

Let \(\mathcal{H}\) be the category of histories. Two histories \(h_1, h_2\[4D[K
h_2\) are **extensionally equivalent at horizon \(k\)** if their induced op[2D[K
option spaces agree up to length‑\(k\) extensions:

\[
h_1 \approx_k h_2 \;\Longleftrightarrow\;
\{\text{length}-k\text{-extensions of }h_1\}
= 
\{\text{length}-k\text{-extensions of }h_2\}.
\]

**Confluence**: A family \(\{h_i\}_{i\in I}\) is confluent if there exists [K
a history \(h_c\) and a collapse policy \(C\) such that for every \(i\),

\[
h_i \cdot C \approx_0 h_c .
\]

Thus confluence does **not** require histories to be identical; it only req[3D[K
requires they can be made equivalent by an explicit act of identification ([1D[K
(the `collapse` event).

**Divergence**: If no such collapse policy exists, the set diverges. This r[1D[K
reflects incompatibility of commitments that cannot be compressed without l[1D[K
losing some admissible futures.

---

### Regret as a Descriptive Property

A history \(h\) exhibits **regret** when there is a reachable prefix \(p\) [K
and histories

\[
h = p \cdot e_1 \dots e_n,\qquad
h' = p \cdot e'_1 \dots e'_m,
\]

with option spaces satisfying

\[
O_h \prec O_{h'} .
\]

Regret is a natural consequence of irreversible commitments; it signals tha[3D[K
that the sequence has become more constrained than an alternative reachable[9D[K
reachable from the same prefix.

---

### Evaluation Model Without Backtracking

In Spherepop:

* **Evaluation** = appending events to a configuration.
* **Correctness** ≠ “no divergence or regret.” It simply means the remainin[8D[K
remaining option space aligns with the agent’s goals.
* **Improvement** occurs by *acting coherently* in light of past commitment[10D[K
commitments, not by undoing them.

Thus Spherepop replaces classical notions of correctness and failure with a[1D[K
a richer view where histories themselves are judged on their capacity to be[2D[K
be merged or regretted rather than merely “being wrong.”

---

### Minimal BNF Grammar for Expressions

```
<Identifier> ::= letter (letter | digit | "_")*
<Value>      ::= <Identifier> | <Number>
<Number>     ::= digit+

<Expr>       ::= <Value>
            | <Sphere>

<Sphere>     ::= "(" <Label> ":" <Expr>* ")"

<Event>      ::= <Pop>
               | <Collapse>
               | <Refusal>
               | <Binding>

<Pop>        ::= "pop" "(" <Label> ")"
<Collapse>  ::= "collapse" "(" <Label> "," <Equiv> ")"
<Refusal>   ::= "refuse" "(" <Label> "," <Set> ")"
<Binding>   ::= "bind" "(" <Label> "," <Predicate> ")"

<Equiv>     ::= "{" <Pair> ("," <Pair>)* "}"
<Pair>      ::= <Value> "~" <Value>

<Set>       ::= "{" <Value> ("," <Value>)* "}"

<Predicate> ::= <Identifier>
```

- **Expressions** are nested spheres that may contain zero or more sub‑expr[8D[K
sub‑expressions.
- **Events** are the only means to change state; they never modify an exist[5D[K
existing expression in place but produce a new configuration via evaluation[10D[K
evaluation.

---

### Bibliography

\begin{thebibliography}{99}

\bibitem{Wittgenstein1953}
L. Wittgenstein.
\emph{Philosophical Investigations}.
Blackwell Publishing, Oxford, 1953.

\bibitem{Church1936}
A. Church.
\emph{An unsolvable problem of elementary number theory}.
American Journal of Mathematics, 58(2):345--363, 1936.

\bibitem{Turing1936}
A. M. Turing.
\emph{On computable numbers, with an application to the Entscheidungsproble[19D[K
Entscheidungsproblem}.
Proceedings of the London Mathematical Society, 42(2):230--265, 1936.

\bibitem{Fant1995}
K. Fant.
\emph{Computer Science Reconsidered: The Challenge of Computers and the Min[3D[K
Mind}.
Addison-Wesley, Reading, MA, 1995.

\bibitem{Needham1997}
T. Needham.
\emph{Visual Complex Analysis}.
Oxford University Press, Oxford, 1997.

\bibitem{Meijer2012}
E. Meijer.
\newblock Your mouse is a database.
In \emph{Proceedings of the ACM SIGMOD International Conference on Manageme[8D[K
Management of Data}, 2012.

\bibitem{Meijer2011}
E. Meijer.
\newblock The duality of computation.
Communications of the ACM, 54(5):41--47, 2011.

\bibitem{MacLane1971}
S. Mac Lane.
\emph{Categories for the Working Mathematician}.
Springer-Verlag, New York, 1971.

\bibitem{Turing1936}
A. M. Turing.
\emph{On computable numbers, with an application to the Entscheidungsproble[19D[K
Entscheidungsproblem}.
Proceedings of the London Mathematical Society, 42(2):230--265, 1936.

\bibitem{Stonebraker2018}
M. Stonebraker and A. Pavlo.
\newblock What goes around comes around.
Communications of the ACM, 61(1):16--18, 2018.

\end{thebibliography}

--- 

*Spherepop’s design deliberately separates *state* (expressions) from *hist[5D[K
*history*, treating histories as first‑class objects that can be merged or [K
regretted. This shift eliminates reliance on backtracking and error handlin[7D[K
handling while preserving a coherent notion of correctness through confluen[8D[K
confluence, divergence, and regret.*

