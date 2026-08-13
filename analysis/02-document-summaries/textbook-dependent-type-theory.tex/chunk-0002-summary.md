Below is an explanation of how the historical kernel’s bidirectional type c[1D[K
checker works, organized according to its intended design and properties:

──────────────────────────────
1. Two Algorithmic Judgments

The core idea behind a bidirectional approach in this context is that we se[2D[K
separate typing into two complementary judgments rather than trying to infe[4D[K
infer types for every expression unconditionally.

• **Synthesis Judgment (→)**  
  \[
  H \vdash t \Rightarrow A
  \]  
  This judgment computes the type \(A\) of an expression \(t\) when it appe[4D[K
appears in a “synthesize” position. It is essentially asking: *Given this t[1D[K
term, what type does it have?* The answer must be accompanied by a proof th[2D[K
that the resulting type can be constructed from the current history \(H\).

• **Checking Judgment (←)**  
  \[
  H \vdash t \Leftarrow A
  \]  
  This judgment verifies whether an expression \(t\) inhabits a given previ[5D[K
previously known type \(A\). It is used in contexts where we already have a[1D[K
a candidate type and need to confirm that the term indeed satisfies it. Lik[3D[K
Like synthesis, this check must also produce a constructive proof of compat[6D[K
compatibility with the history.

These judgments interact: if you can synthesize a type for an expression (→[2D[K
(→), then checking against that synthesized type (←) becomes possible; simi[4D[K
similarly, knowing how to check a given type allows you to infer what type [K
a term should have in other contexts.

──────────────────────────────
2. Mutual Definition and Algorithmic Flow

The synthesis and checking judgments are mutually recursive:

- **From Synthesis → Checking:**  
  If the synthesis judgment succeeds (producing \(A\) with proof of admissi[7D[K
admissibility), then you can “check” that term against this newly derived t[1D[K
type.

- **From Checking → Synthesis:**  
  Conversely, if a checking judgment succeeds, it often implies or enables [K
a synthesis step by providing a concrete example of how to construct the re[2D[K
required type for other similar terms.

This mutual dependency eliminates the need for global inference rules (as m[1D[K
might be used in non-bidirectional systems) and keeps the algorithm determi[7D[K
deterministic. Each decision point can be executed independently with clear[5D[K
clear conditions based on history, ensuring that no undecidable cases arise[5D[K
arise.

──────────────────────────────
3. Historical Provenance

A critical extension of the traditional bidirectional type checker is that [K
every judgment must also validate admissibility within a constructive histo[5D[K
history:

- The synthesis judgment \(H \vdash t \Rightarrow A\) must verify not only [K
that the type \(A\) can be inferred but also that the process leading to it[2D[K
it respects the event algebra (i.e., forward dependency edges are introduce[9D[K
introduced without creating cycles).

- Similarly, the checking judgment \(H \vdash t \Leftarrow A\) must confirm[7D[K
confirm both that the term inhabits the given type and that the constructio[11D[K
construction of this proof is replayable—meaning the history extending up t[1D[K
to this point can be reconstructed from historical events.

By embedding provenance into each step, we guarantee that:

1. **Well‑formedness** – No ill‑formed histories are introduced; every oper[4D[K
operation preserves the internal consistency of the event algebra.
2. **Replayability** – Proofs (or histories) generated during type checking[8D[K
checking can be reconstructed from immutable events, enabling verification [K
and debugging without external proof objects.

──────────────────────────────
4. Implementation Considerations

Because we want a practical kernel that is:

- **Small and Deterministic:**  
  The algorithm should terminate predictably, avoiding non‑terminating sear[4D[K
search spaces.

- **Mechanically Implementable:**  
  Each judgment can be realized as a finite state machine or recursive proc[4D[K
procedure with clear termination proofs (due to the inherent structure of h[1D[K
histories).

The bidirectional checker works by:

1. **Parsing** – Tokenizing input into well‑typed terms.
2. **Synthesis Phase:**  
   - Attempt to synthesize a type for each term using rules that look ahead[5D[K
ahead at possible reductions and their associated events.
3. **Checking Phase:**  
   - When checking against an existing type, verify compatibility with the [K
history; if it fails, backtrack or adjust synthesis accordingly.
4. **Error Handling:**  
   - If neither synthesis nor checking succeeds, report a concrete error al[2D[K
along with the most recent historical event that caused the failure.

──────────────────────────────
5. Summary

In essence, the bidirectional historical type checker leverages:

- Two complementary judgments (synthesis and checking) to separate inferenc[8D[K
inference from verification.
- Mutual recursion between these judgments to maintain logical consistency [K
without global rules.
- Embedding of constructive provenance in every step to ensure that the res[3D[K
resulting histories remain admissible and replayable.

This design mirrors how modern proof assistants operate, providing a robust[6D[K
robust foundation for dependent type theory within the kernel while ensurin[7D[K
ensuring that all operations on terms are traceable back to immutable histo[5D[K
historical events. It also facilitates advanced features like incremental r[1D[K
recompilation and reproducible builds by treating computation as historical[10D[K
historical growth rather than mere state transformation.
  
──────────────────────────────
This structured approach ensures that the kernel remains both practical for[3D[K
for implementation (small, deterministic) and theoretically sound (preservi[9D[K
(preserving well‑formedness via history), paving the way for further develo[6D[K
development in operational semantics, proof verification, and type reconstr[8D[K
reconstruction.

