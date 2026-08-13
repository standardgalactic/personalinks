**Spherepop – A Formalism for Causal Histories**

**1. Core Syntax**

A *history* in Spherepop is a well‑formed sequence of statements, each bein[4D[K
being one of three kinds:

| Type | Production (grammar) |
|------|-----------------------|
| **Split**   | `split( <object> ) → <object>,<object>` |
| **Merge**   | `merge(<object>,<object>) → <object>` |
| **Direct event transformation** | `<object> → <event> → <object>` |

*Objects* are the regions or “places” that appear on a causal diagram, whil[4D[K
while *events* describe transitions (split/merge) between them.  

The full grammar is

```
<history>        ::= <statement>
                   | <statement> <history>

<statement>      ::= <split>
                   | <merge>
                   | <event-transform>

<object>         ::= ...   (name of a region)
<event>          ::= ...   (label for a transition, e.g., “birth”, “death”)[8D[K
“death”)
```

Thus any history is a linear string such as  

`merge(A,B) → D, split(R) → A,B …`.

**2. Event Graph & Causal Ordering**

When parsed, the statements induce an *event graph* – a directed acyclic gr[2D[K
graph (DAG) where:

- Vertices = objects (regions).  
- Edges = events that move tokens from one vertex to another.

The DAG encodes causal dependencies: if event \(E_i\) precedes \(E_j\), the[3D[K
then \(i\) must occur before \(j\) in any admissible execution.  

**3. Normalization**

Normalization orders the events according to this partial order, producing [K
a *normal form*:

```
(normal-form) ::= ( <event‑word> )
```

The *event word* is the linearized list of events after applying commutatio[10D[K
commutation rules.

**4. Rewriting Rules & Confluence**

Normalization proceeds via a confluent rewriting system defined by two basi[4D[K
basic operations:

1. **Commutation Rule**  
   If two adjacent events \(E_i\) and \(E_j\) are independent \((E_i\parall[13D[K
\((E_i\parallel E_j)\), they may be swapped:  

   \[
   (E_i, E_j) \;\longrightarrow\; (E_j, E_i)
   \]

   Independence is symmetric (if \(i\parallel j\) then \(j\parallel i\)) an[2D[K
and satisfies the *diamond* property: any two independent pairs can be comm[4D[K
commuted independently.

2. **Structural Rules**  
   - A merge `merge(A,B) → D` collapses two incoming edges to a single vert[4D[K
vertex for \(D\).  
   - A split `split(R) → A,B` collapses one outgoing edge from \(R\) into s[1D[K
separate outgoing edges to \(A\) and \(B\).

Applying these rules repeatedly yields the *normal form* (the lexicographic[13D[K
lexicographically smallest word respecting the independence relation).  

**5. Soundness & Completeness**

- **Soundness**: Every well‑typed Spherepop expression corresponds exactly [K
to one normal form; thus two expressions represent the same historical obje[4D[K
object iff their normal forms are identical.
- **Completeness**: The rewriting terminates because the event graph is a D[1D[K
DAG, guaranteeing that every execution can be reduced to its unique normal [K
form.

These properties follow from standard results on confluence and termination[11D[K
termination for trace‑type rewriting systems (see Abramsky 1994; Mazurkiewi[10D[K
Mazurkiewicz 1987).

**6. Connections with Other Formalisms**

| Framework | Mapping to Spherepop |
|-----------|----------------------|
| **Mazurkiewicz Trace Theory** | Event words are equivalence classes of se[2D[K
sequences modulo commutation, identical to the normalized forms obtained by[2D[K
by rewriting. |
| **Petri Nets** | Objects ↔ Places; events ↔ Transitions (split → multiple[8D[K
multiple output places, merge → single input place). A history is a firing [K
sequence in the net’s reachability graph. |
| **String Diagrams** | Objects are wires; morphisms are boxes/nodes (split[6D[K
(split = box with one output wire branching into two, merge = node taking t[1D[K
two inputs and emitting one). Sequential transformations compose by connect[7D[K
connecting output to next input wire. |

These correspondences illustrate Spherepop as a compositional language that[4D[K
that sits at the intersection of algebraic (trace) and geometric (string di[2D[K
diagram) representations of causal processes.

**7. Example**

Consider the simple history:

```
merge(A,B) → D, split(R) → A,B
```

Parsing yields an event graph with vertices {R, A, B, D} and edges R→A, R→B[3D[K
R→B, A→D, B→D.  
Applying commutation (if \(A\parallel B\) we swap `split(R) → B,A`) produce[7D[K
produces the normal form:

```
merge(A,B) → D, split(R) → A,B
```

or after swapping if adjacency allows:  

```
merge(A,B) → D, split(R) → B,A
```

Both are valid because they respect the independence relation.

**8. Decision Procedure**

1. **Parse** the expression into a DAG of events (structural rules).  
2. **Compute a topological sort** (e.g., lexicographic ordering for ties). [K
 
3. **Apply commutation** until no two adjacent events can be swapped withou[6D[K
without violating the sort.  

The resulting event word is unique and serves as the canonical identifier f[1D[K
for that object.

---

*In summary, Spherepop provides an algebraic yet intuitive notation for cau[3D[K
causal histories: parsed into a DAG of independent events, normalized via c[1D[K
confluent commutation rules, yielding a unique normal form that serves as t[1D[K
the identity witness among all syntactically equivalent expressions.*

