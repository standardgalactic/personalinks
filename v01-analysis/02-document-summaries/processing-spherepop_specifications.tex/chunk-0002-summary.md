**Durable Theoretical Information Extracted**

1. **Commit Function (Overlay Authority)**
   - *Definition*: `commit(&mut self, o: Overlay, omega_0: &std::collection[16D[K
&std::collections::HashSet<ObjectId>) -> Result<Vec<LogPos>, ArbiterError>`[14D[K
ArbiterError>`
     - Takes an overlay (`o`) and a set of object identifiers[11D[K
identifiers (`omega_0`).
     - Returns a vector of log positions on success or an `ArbiterError` if[2D[K
if the overlay is stale.
   - *Staleness Check*: If `o.base_len != self.arbiter.len()`, returns `Err[4D[K
`Err(ArbiterError::StaleOverlay)`. This indicates that the overlay has been[4D[K
been modified (e.g., H moved since preview).
   - *Operation*: Calls `self.arbiter.submit(o.pending, omega_0)` analogous[9D[K
analogous to a proposal submission.

2. **Arbiter Interface**
   - The arbiter can submit proposals (`submit`) similar to how `commit` wo[2D[K
works for overlays.
   - Example usage: `arb.submit(Proposal { events: vec![pop(1), pop(2)] }, [K
&omega_0)?;` demonstrates committing events (populating objects 1 and 2) vi[2D[K
via the arbiter.

3. **Observation Rule – Quotient Collapse**
   - Identifying two elements (e.g., `a` and `b`) is achieved by observing [K
under a quotient rule (`collapse("merge_quotient")`), showing that traditio[8D[K
traditional “Merge” is not an independent event type but a projection effec[5D[K
effect.
   - The final refusal of a binding demonstrates **Unlink‑sugar**, where th[2D[K
the original bind remains untouched (Irreversibility, Corollary \ref{cor:ir[21D[K
Corollary \ref{cor:irrev}).

4. **Geometric Semantics**
   - *Primitive Reading*:
     - `Pop` contracts option space (`Ω`) – narrowing possibility.
     - `RefuseOp` marks a region of `Ω` as excluded without contraction.
     - `BindOp` draws an edge between two points but does not merge them.
     - `CollapseOp` projects the entire history onto an observational plane[5D[K
plane `O_c`, with different rules `c` giving distinct projections.

5. **Pipeline Architecture**
   - Strict layering: Parse → Desugar → Typecheck → Evaluate → Interpret.
   - Correctness is guaranteed at the Structured Programming Calculus (SPC)[5D[K
(SPC) level, independent of surface notation.

6. **Example DSL Scene & Lowered Core**
   - *DSL*:
     ```verilog
     @scene {
       sphere f(type: Πx:A.B, body: pop g with x)
       sphere g(type: Πx:A.B, value: <primitive>)
       sphere a(type: A, value: a0)

       pop f with a
       choose 0.5: pop g with a | pop f with a
     }
     ```
   - *Lowered Core*:
     ```verilog
     f = Sphere(x:A. Pop(g, x))
     g = <primitive> : Πx:A.B
     a = a0 : A

     Pop(f, a)
     Choice(0.5, Pop(g, a), Pop(f, a))
     ```
   - Application collapses abstraction boundaries; choice branches probabil[8D[K
probabilistically.

7. **Typing Derivations (Appendix A)**
   - *Application*:
     \[
     \Judgement{\Ctx}{f}{\PiT{x}{A}{B}} \quad \text{and} \quad \Judgement{\[12D[K
\Judgement{\Ctx}{a}{A}
     \]
     ⇒ `⊢ {\Ctx}{Pop(f,a)}{B\Subst a x}`.
   - *Merge*:
     \[
     \Judgement{\Ctx}{t}{A}\wedge \Judgement{\Ctx}{u}{A} \;\Rightarrow\; \J[2D[K
\Judgement{\Ctx}{\Merge(t,u)}{A}
     \]
   - *Choice*:
     \[
     \Judgement{\Ctx}{t}{A}\wedge \Judgement{\Ctx}{u}{A} \;\Rightarrow\; \J[2D[K
\Judgement{\Ctx}{\Choice(p,t,u)}{A}
     \]

8. **Operational Semantics Proofs (Appendix B)**
   - *Preservation*: By induction on typing derivations, β‑reduction preser[6D[K
preserves types.
   - *Progress*: Values are atoms or `\Sphere` forms; `Pop(\Sphere(\cdot),\[21D[K
`Pop(\Sphere(\cdot),\cdot)` reduces; otherwise subterms reduce.
   - *Confluence* (deterministic fragment): β‑reduction is confluent up to [K
standard λ‑calculus arguments adapted for `\Merge`.

9. **Category‑Theoretic Interpretation (Appendix C)**
   - Types as objects, terms `t:A→B` as morphisms (`Sphere`), application a[1D[K
as composition.
   - *\Merge* forms a symmetric, idempotent tensor: `(t\Merge u)\Merge v \e[2D[K
\equiv t\Merge(u\Merge v)`; commutativity and self‑identity hold.
   - *\Choice* aligns with Giry‑style monad: unit returns degenerate choice[6D[K
choice; multiplication marginalizes nested choices.
   - *Topos View*: `\Sphere` scopes interpreted as objects of a site `\Sphe[6D[K
`\SphereCat`; SPC terms act as arrows in the presheaf topos `\ToPos`, expla[5D[K
explaining functorial behavior of abstraction and application.

**Summary**

The fragment captures core operational semantics for overlay authority (`co[4D[K
(`commit`) within a distributed consensus system, demonstrates how “Merge” [K
functions via quotient collapse rather than being an independent event type[4D[K
type, and provides layered geometric interpretations (application as contra[6D[K
contraction, merge as projection). The pipeline design ensures correctness [K
at deeper SPC levels, while the appendices formalize typing derivations, op[2D[K
operational properties (preservation, progress, confluence), and category‑t[10D[K
category‑theoretic perspectives on monoidal structures and topos semantics.

