**Spherepop – A Geometric Formalism for Concurrency, Evaluation Order Indep[5D[K
Independence, and Scope**

---

### 1. Core Concepts  

#### **Evaluation Region (Bubble)**
- A *bubble* \(B=(U,\partial U,\sigma,\tau)\) is a bounded region with:
  - **Interior** \(U\) – the set of locally admissible evaluation steps.
  - **Boundary** \(\partial U\) – where pop, bind, and refuse events can af[2D[K
affect the interior.
- The *evaluation region* records:
  - **Pop events** \(\spop{B'}\): innermost bubbles that may be popped.
  - **Bind events** \(\sbind{a<b}{B}\): introduce constraints on \(U\)’s co[2D[K
content.
  - **Refuse events** \(\srefuse{B'}\): record inadmissibility of a pop ste[3D[K
step.

#### **Scope as Physical Boundary**
- The bubble’s boundary is the *physical limit* for evaluation effects:
  - Anything inside can be directly influenced by operations/events within [K
it.
  - Nothing outside can affect the interior except via the *pop result* (th[3D[K
(the value returned when a bubble pops).

**Proposition:**  
The scope of any bind event \(\sbind{a<b}{B}\) is exactly the interior \(U\[4D[K
\(U\) of its containing bubble \(B\). No operation outside \(B\) can observ[6D[K
observe constraints introduced by binds except through the pop result.

---

### 2. Dependency Encoding  

- **Spatial Nesting:**  
  If a bubble \(B_1\) is nested inside another \(B_2\), then:
  \[
    \spop{B_1} \prec \spop{B_2}
  \]
  This encodes tree‑structured dependencies. Computation cannot proceed pas[3D[K
past a pop event that requires the result of an inner bubble.

- **Directed Acyclic Graph (DAG) Limitation:**  
  Pure nesting supports only tree structures; shared subexpressions require[7D[K
require bind operations to create cross‑bubble constraints, effectively gen[3D[K
generalizing variable binding in functional languages.

---

### 3. Evaluation Order Independence  

Because evaluation events inside one bubble cannot affect sibling bubbles d[1D[K
directly:

\[
\text{Result of the containing bubble is independent of sibling pop order.}[7D[K
order.}
\]

This mirrors the confluence theorem for reduction systems: different evalua[6D[K
evaluation orders yield the same terminal result, as each bubble’s outcome [K
depends solely on its own interior and boundary conditions.

---

### 4. Spherepop Operators  

| Operator | Meaning |
|----------|---------|
| **Pop \(\spop{B}\)** | Reduces an innermost pop‑eligible bubble to its va[2D[K
value; records the event in history. |
| **Refuse \(\srefuse{B'}\)** | Records that a proposed reduction is curren[6D[K
currently inadmissible (constraints not satisfied). Not a failure but a del[3D[K
deliberate deference, analogous to epistemically responsible thinking. |
| **Collapse \(\scollapse{q}\)** | Identifies histories equivalent under re[2D[K
relation \(q\) while preserving structural invariants; used for generalizat[11D[K
generalization and compression of computation paths. |

**Conditions for Collapse:**  
- Must preserve admissibility (no information about prohibited reductions i[1D[K
is lost).
- Factorization condition: observable functions satisfy \(f = \bar{f} \circ[5D[K
\circ \scollapse{q}\), ensuring the quotient respects semantics.

---

### 5. Semantic Objects  

#### **History**
- A finite ordered sequence of evaluation events:
  \[
    \shist = (e_1, e_2, \ldots, e_n) \quad\text{with } e_k \in \{\spop{B}, [K
\srefuse{B}, \scollapse{q}, \sbind{a<b}{B}\}
  \]
- **Primary semantic object** – the domain over which the action functional[10D[K
functional \(S[\shist]\) is defined.

#### **Evaluation Chain**
- A subsequence of a history consisting only of pop events and resolved bub[3D[K
bubbles.
- Traces the reduction from initial expression to terminal value, recording[9D[K
recording ordering and produced values.

---

### 6. Conclusions  

Spherepop uses geometric constraints (bubbles with boundaries) to give a *p[2D[K
*physical* meaning to scope, dependency, and evaluation order. By treating [K
histories—rather than instantaneous values—as fundamental objects, it achie[5D[K
achieves:

1. **Evaluation Order Independence:** Different orders of sibling evaluatio[9D[K
evaluations produce the same result.
2. **Explicit Scope Representation:** Boundaries cleanly separate dependent[9D[K
dependent from independent scopes.
3. **Structured Dependency Capture:** Spatial nesting directly encodes DAG‑[4D[K
DAG‑structured dependencies without extra annotations.

This framework bridges conventional programming language semantics with a s[1D[K
spatial, geometric intuition for concurrency and evaluation order, offering[8D[K
offering both conceptual clarity and formal rigor.
