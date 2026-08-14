**1. Definitions and Primitive Concepts Introduced**

- **Composition‑first calculus**: A formal system that treats graph constru[7D[K
construction and history evolution as primitive computational operations.
- **Graph \(G\)**: An abstract structure representing a set of operators an[2D[K
and their interconnections; it is the basic building block in this calculus[8D[K
calculus.
- **History \(H\)**: A persistent, mutable record (often a log) that accumu[6D[K
accumulates events and results from executed graphs.
- **Executable node \(n\)**: A concrete instance of an operator within a gr[2D[K
graph that can be scheduled for evaluation.
- **Refusal reason \(r\)**: A condition or explanation indicating why execu[5D[K
execution of a particular node fails to produce a result.
- **Collapse outcome**: When the desired output has already been generated,[10D[K
generated, marking the state as “completed” without further computation.

**2. Mathematical Claims and Formal Structures**

- **Identity rule**:  
  \[
  \frac{ }{\; H \vdash \operatorname{Id} \Downarrow H. }
  \]  
  *Source*: “[source: …]”.

- **Composition rule**:  
  \[
  \frac{
    H \vdash G_1 \Downarrow H_1
    \quad\text{and}\quad
    H_1 \vdash G_2 \Downarrow H_2
  }{
    H \vdash G_2 \circ G_1 \Downarrow H_2 .
  }
  \]  
  *Source*: “[source: …]”.

- **Refusal rule**:  
  \[
  \frac{
    r\text{ is a refusal reason}
  }{
    H \vdash n \Downarrow (H,\Refuse(r)).
  }
  \]  
  *Source*: “[source: …]”.

- **Collapse rule**:  
  \[
  \frac{
    v\text{ has already been produced}
  }{
    H \vdash \Collapse(v) \Downarrow (H,\Collapse(v)).
  }
  \]  
  *Source*: “[source: …]”.

**3. Mechanisms and Processes**

- **Operator evaluation**: When an executable node \(n\) of operator \(f\) [K
is evaluated, the process records both the result and a computational event[5D[K
event:
  \[
  \frac{
    v = f(v_1,\dots,v_k)
  }{
    H \vdash n \Downarrow (H,e),
  }
  \]  
  where \(e=(n,f,v)\). This turns history into an explicit trace of computa[7D[K
computation.
- **History extension**: Executing graph \(G\) extends the current history [K
\(H\) into a new history \(H'\) via:
  \[
  H \vdash G \Downarrow H'.
  \]
- **Refusal handling**: Captures speculative failures with a refusal reason[6D[K
reason, ensuring that non‑completable paths are recorded.
- **Collapse handling**: Marks already produced values as collapsed, preven[6D[K
preventing redundant work.

**4. Connections to Concepts Named in the Running Abstract**

- **Composition (as primitive)**: Directly corresponds to “composition‑firs[17D[K
“composition‑first calculus” introduced here and earlier abstract summary; [K
it is the fundamental operation replacing traditional language‑specific eva[3D[K
evaluation rules.
- **Graphs & Histories**: Mirrors the running abstract’s emphasis on *graph[6D[K
*graphs* as building blocks for computational behavior, with histories reco[4D[K
recording evolution of these graphs.
- **Refusal & Collapse Events**: Extends the abstract’s “refusal and collap[6D[K
collapse events” concept by providing formal judgmental rules (\( \Refuse(r[9D[K
\Refuse(r) \), \( \Collapse(v) \)) to manage non‑deterministic or completed[9D[K
completed states.

**5. Unresolved Questions or Contradictions Visible in This Chunk**

- The chunk lists numerous bibliography references without any substantive [K
discussion of their relationship to the calculus; there is no indication ho[2D[K
how these external works inform or are informed by the introduced formalism[9D[K
formalism.
- No explicit contradictions arise from the content itself, but a gap remai[5D[K
remains: while the abstract outlines broad applicability (typing, theorem p[1D[K
proving, neural computation), this chunk does not specify which operator li[2D[K
libraries or graph transformations would instantiate such applications. Wit[3D[K
Without further context, it is unclear how to map external works (e.g., *Co[3D[K
*Concrete Mathematics*, *Computer Architecture*) onto the compositional fra[3D[K
framework described here.
- The absence of operational semantics for concrete operators implies a pot[3D[K
potential incompleteness regarding execution rules beyond the abstract iden[4D[K
identity/composition principles.

*Note*: No substantive claim in this chunk could be directly tied to an exa[3D[K
exact quote longer than ~20 words, as the text primarily consists of biblio[6D[K
bibliographic entries rather than conceptual or formal statements.*
