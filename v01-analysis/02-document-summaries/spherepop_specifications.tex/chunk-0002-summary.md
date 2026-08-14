**Durable Theoretical Information Extracted**

1. **Overlay Commit Mechanism (Arbiter Interface)**
   - *Definition*: `commit(&mut self, o: Overlay, omega_0: &std::collection[16D[K
&std::collections::HashSet<ObjectId>) -> Result<Vec<LogPos>, ArbiterError>`[14D[K
ArbiterError>`
     - Takes an overlay object `o` and a set of object identi[6D[K
identifiers `omega_0`.
     - Calls the internal method `self.arbiter.submit(o.pending, omega_0)`.[10D[K
omega_0)`.
   - *Constraint*: If `o.base_len != self.arbiter.len()`, returns[7D[K
returns `Err(ArbiterError::StaleOverlay)` (indicating that the overlay has [K
changed since its preview).
   - *Equation/Dependency*: The operation is only valid when the length of [K
the overlay matches the current state of the arbiter, ensuring consistency [K
between proposal and underlying structure.

2. **Arbiter Submit Call**
   - *Definition*: `arb.submit(Proposal { events: vec![pop(1), pop(2)] }, &[1D[K
&omega_0)?`
     - Submits a proposal containing two `Pop` operations (effectively “con[4D[K
“contracting” objects 1 and 2) along with the identifier set `omega_0`.
   - *Result*: Represents an authoritative commit of events to the history [K
managed by Arbiter.

3. **Quotient Collapse Demonstration**
   - Shows that merging (`Merge`) is not a separate event kind but achieved[8D[K
achieved through observation rules applied to existing binding operations.
   - After invoking `collapse("merge_quotient")`, objects previously identi[6D[K
identified separately (1 and 2) become indistinguishable in the history, il[2D[K
illustrating a projection onto an observational plane.

4. **Unlink Sugar Mechanism**
   - The call `refuse_bind(1, 2, "adjacent", "relation withdrawn")` marks t[1D[K
the binding of 1 and 2 as withdrawn without deleting it.
   - Demonstrates that the original bind remains intact (Irreversibility) w[1D[K
while subsequent observation rules may exclude such a withdrawn relation fr[2D[K
from further projections.

5. **Geometric Semantics**
   - *Pop*: Contraction of option space `Ω`; narrows possibilities.
   - *RefuseOp*: Marks a region in `Ω` as excluded without contraction, ana[3D[K
analogous to removing an area from the set of possible states.
   - *BindOp*: Draws an edge (relationship) between two points without merg[4D[K
merging them; retains distinct identity.
   - *CollapseOp*: Projects the entire history onto a plane `O_c`, where di[2D[K
different projection rules give differing visualizations of the same underl[6D[K
underlying object.

6. **Pipeline Workflow**
   - Sequential stages from DSL input to final field configuration:
     1. **Parse** → AST (Scene)
     2. **Desugar** → SPC Terms
     3. **Typecheck** → Typed Terms in Context `Γ`
     4. **Evaluate** → Normal Forms via β-reduction + stochastic steps
     5. **Interpret** → Field configuration `(Field, Flow, Entropy)`

7. **Typing Derivations**
   - *Application*: If `f` is typed as $\Pi{x}{A}{B}$ and `a` as type $A$, [K
then `Pop(f,a)` yields type $B\Subst{a}{x}$.
   - *Merge*: Two terms of the same type can be merged, producing a term of[2D[K
of that type: `\Judgement{\Ctx}{t}{A}\wedge \Judgement{\Ctx}{u}{A} \To \Jud[4D[K
\Judgement{\Ctx}{\Merge(t,u)}{A}`.
   - *Choice*: Probabilistic branching is expressed as `\Judgement{\Ctx}{t}[20D[K
`\Judgement{\Ctx}{t}{A}\wedge \Judgement{\Ctx}{u}{A} \To \Judgement{\Ctx}{\[18D[K
\Judgement{\Ctx}{\Choice(p,t,u)}{A}`.

8. **Operational Semantics Proofs**
   - *Preservation*: By induction on typing derivations; β-reduction preser[6D[K
preserves type safety, and both Merge and Choice maintain equality of types[5D[K
types.
   - *Progress*: Values are atoms or $\Sphere$-forms; application reduces t[1D[K
to more concrete forms, while probabilistic steps in Choice remain well‑typ[8D[K
well‑typed.

9. **Category-Theoretic Interpretation**
   - Types correspond to objects; term morphisms are generated via the $\Sp[4D[K
$\Sphere$ operation.
   - The monoidal structure of Merge is symmetric and idempotent: `(t\Merge[9D[K
`(t\Merge u)\Merge v \equiv t\Merge(u\Merge v)`, reflecting compositional n[1D[K
nature.
   - Choice aligns with a Giry-style monad, where unit yields degenerate ch[2D[K
choices and multiplication marginalizes nested probabilistic outcomes.

10. **Core Desugaring (DSL → Lowered Core)**
    - Application collapses abstraction boundaries (`f` applied to `a`), wh[2D[K
while Choice introduces probabilistic branching.
    - Typing guarantees that branches agree on type constraints, ensuring e[1D[K
evaluation proceeds via β-reduction and stochastic sampling as defined by t[1D[K
the operational semantics.

**Unresolved Questions/Dependencies**

- The role of Stochastic steps in $\Choice$ is not fully detailed; their im[2D[K
impact on convergence or entropy distribution remains a subject for further[7D[K
further analysis.
- Interaction between Merge (projection) and BindOp (edge creation) when bo[2D[K
both are applied to overlapping sets of objects requires deeper examination[11D[K
examination, especially concerning Irreversibility and the semantics of “wi[3D[K
“withdrawn bindings.”
- The categorial treatment assumes standard λ-calculus adaptation; potentia[8D[K
potential extensions beyond deterministic fragments (e.g., non‑commutative [K
Merge) have not been explored.

