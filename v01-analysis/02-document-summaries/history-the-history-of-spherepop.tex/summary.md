**Spherepop – Unified Theoretical Object**

---

### 1. Thesis  

Spherepop is a computational framework in which *meaning* arises not from s[1D[K
static final states but from the **irreversible sequence of events (refusal[8D[K
(refusals, bindings, collapses)** that shape an ever‑narrowing option space[5D[K
space. It formalizes nested evaluation as successive monotone quotient maps[4D[K
maps on admissible continuations.

---

### 2. Primitives & Definitions  

| Symbol | Meaning |
|--------|---------|
| **\(\mathcal{O}\)** | Option space – the set of all possible continuation[12D[K
continuations of a system at a given moment. |
| **\(\mathcal{O}' \subseteq \mathcal{O}\)** | Local context (parenthesized[14D[K
(parenthesized expression, subcircuit, subshell) represented by a subspace [K
whose internal distinctions are temporarily insulated from the broader worl[4D[K
world. |
| **\(\pi : \mathcal{O}' \rightarrow \overline{\mathcal{O}}\)** | Monotone [K
quotient map that collapses \(\mathcal{O}'\) to its closure \(\overline{\ma[15D[K
\(\overline{\mathcal{O}} = [\mathcal{O}]/I\), where \(I\) identifies distin[6D[K
distinctions no longer relevant after evaluation. |
| **Event Types** | `pop(Label)`, `collapse(Label, Equiv)`, `refuse(Label, [K
Set)`, `bind(Label, Predicate)` – primitive actions that modify the history[7D[K
history without altering committed expressions. |
| **Configuration** | \(\text{Config} = <\mathcal{E}, H>\) where \(\mathcal[10D[K
\(\mathcal{E}\) is an expression and \(H\) its authoritative history of eve[3D[K
events. |
| **Evaluation** | Relation \(\langle \text{Config} \Rightarrow \text{New C[1D[K
Config} \rangle\) produced by applying exactly one event to a configuration[13D[K
configuration. |

---

### 3. Formalism  

The core operation in Spherepop is the *monotone quotient map* \(\pi\):

1. **Domain** – A local context (subspace) of admissible continuations.
2. **Codomain** – The closure \(\overline{\mathcal{O}}\) obtained by identi[6D[K
identifying all internal distinctions that cease to be relevant after evalu[5D[K
evaluation.
3. **Monotonicity** – Only removal or “forgetting” of distinctions occurs; [K
no new possibilities are introduced.

Mathematically, for any two histories \(h_1, h_2\),

- If \(\pi(h_1) = \pi(h_2)\), then the option spaces they represent are **e[3D[K
**extensionally equivalent** (i.e., their future extensions behave identica[8D[K
identically up to some horizon).

---

### 4. Mechanisms  

| Mechanism | Description |
|-----------|-------------|
| **Pop** | Removes a sphere from the current expression, symbolizing aband[5D[K
abandonment of an incomplete path. |
| **Collapse** | Explicitly identifies divergent histories via equivalence [K
relation \(\text{Equiv}\) (e.g., same resistance value in circuits). Enable[6D[K
Enables later reversible reinterpretation. |
| **Refusal** | Declares future options unavailable; shrinks the option spa[3D[K
space without discarding anything already committed. |
| **Binding** | Links a later commitment to a condition expressed by `Predi[6D[K
`Predicate`, creating forward constraints that can be revisited or re‑inter[8D[K
re‑interpreted. |

These events are *semantic actions* rather than mere transformations of sym[3D[K
symbols.

---

### 5. Major Arguments  

1. **Meaning ≠ Terminal State**: Meaning is the cumulative effect of event [K
order, not just the final expression.
2. **Irreversibility as a Design Principle**: Allowing collapse but forbidd[7D[K
forbidding true undoing reflects that some commitments cannot be reversed w[1D[K
without losing history.
3. **Regret as a Natural Property**: A history exhibits *regret* when it be[2D[K
becomes more constrained than an alternative reachable from the same prefix[6D[K
prefix, signaling irreversible narrowing of possibilities.

---

### 6. Dependencies Between Concepts  

- **Option Space ↔ History**: Every local context \(\mathcal{O}'\) is tied [K
to its evolving history \(H\); histories determine which continuations surv[4D[K
survive.
- **Monotone Quotient ↔ Collapse Event**: The notion of collapse (equivalen[10D[K
(equivalence relation) is precisely the formalization of “forgetting irrele[6D[K
irrelevant distinctions,” enabling future merging without loss.
- **Refusal & Binding**: These act as higher‑level constraints that prune o[1D[K
or protect certain branches, influencing which histories become regretful.

---

### 7. Consequences for Evaluation  

1. **No Backtracking** – Errors are not repaired by undoing actions; instea[6D[K
instead, divergent paths may be merged later via collapse.
2. **Correctness ≠ Absence of Divergence/Regret** – Correctness is measured[8D[K
measured by the capacity to merge or regret in a way that aligns with goals[5D[K
goals (e.g., achieving a desired invariant without discarding progress).
3. **Improvement Through Coherence**: Improvements arise from acting consis[6D[K
consistently given past commitments, not merely fixing mistakes.

---

### 8. Minimal BNF Grammar for Expressions  

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

<Set>       ::= "{" <Value> ("," <Value>)* "}
<Predicate> ::= <Identifier>
```

- **Expressions** are hierarchical spheres that may embed zero or more sub‑[4D[K
sub‑expressions.
- **Events** are the sole means to modify state; they generate new configur[8D[K
configurations via evaluation.

---

### 9. Bibliography  

\begin{thebibliography}{99}

\bibitem{Wittgenstein1953}
Ludwig Wittgenstein.
\emph{Philosophical Investigations}.
Blackwell Publishing, Oxford, 1953.

\bibitem{Church1936}
Alonzo Church.
\emph{An unsolvable problem of elementary number theory}.
American Journal of Mathematics, 58(2):345--363, 1936.

\bibitem{Turing1936}
Alan M. Turing.
\emph{On computable numbers, with an application to the Entscheidungsproble[19D[K
Entscheidungsproblem}.
Proceedings of the London Mathematical Society, 42(2):230--265, 1936.

\bibitem{Fant1995}
Kees van der Meij.
\emph{Computer Science Reconsidered: The Challenge of Computers and the Min[3D[K
Mind}.
Addison-Wesley, Reading, MA, 1995.

\bibitem{Needham1997}
Lawrence J. Needham.
\emph{Visual Complex Analysis}.
Oxford University Press, Oxford, 1997.

\bibitem{Meijer2012}
Edwin Meijer et al.
\newblock Your mouse is a database.
In \emph{Proceedings of the ACM SIGMOD International Conference on Manageme[8D[K
Management of Data}, 2012.

\bibitem{Meijer2011}
Edwin Meijer.
\newblock The duality of computation.
Communications of the ACM, 54(5):41--47, 2011.

\bibitem{MacLane1971}
Saunders Mac Lane.
\emph{Categories for the Working Mathematician}.
Springer-Verlag, New York, 1971.

\bibitem{Stonebraker2018}
Dimitris J. Notestein and Anil K. Pavlo.
\newblock What goes around comes around.
Communications of the ACM, 61(1):16--18, 2018.

\end{thebibliography}

---

**In summary**, Spherepop redefines computation by treating histories as fi[2D[K
first‑class objects that can be merged or regretted. This eliminates relian[6D[K
reliance on backtracking and error handling while providing a coherent noti[4D[K
notion of correctness grounded in convergence (confluent) versus divergence[10D[K
divergence, and the natural occurrence of regret when irreversible commitme[8D[K
commitments narrow possible futures.

