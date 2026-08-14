**Recursive Containment and Deferred Closure**

*Flyxion – A Survey*

---

### A. Formal Definitions Collected

For reference, the principal definitions of the paper are collected here in[2D[K
in order of introduction.

1. **Semantic Bubble (B = (C, E, U))**:  
   - *Contextual binding set C*: Sets of variables or entities that partici[7D[K
participate in a given scope.  
   - *Expectation structure E*: A priori predictions about how the content [K
should be organized.  
   - *Unresolved load scalar U(B)*: Non‑negative measure of remaining uncer[5D[K
uncertainty (e.g., entropy) within the bubble.

2. **Containment Structure Σ = (B, ≺)**:  
   - A finite set of bubbles B equipped with a strict partial order ≺ that [K
defines parent–child relationships.  
   - In the tree case every bubble has at most one immediate parent; in the[3D[K
the DAG (directed acyclic graph) case this restriction is dropped.

3. **Scope Stack Σt = [B₁, …, Bₙ]**: Linearizes the active containment path[4D[K
path such that Bₙ is the currently attended scope.

4. **Semantic Load Functional L(Σ) = ∑_i w_i U(B_i)**:  
   - *wi* = function of distance di (how many hops away), stability si (how[4D[K
(how solid the bubble feels), relevance ri (how pertinent to current concer[6D[K
concerns), and context ci (environmental constraints).

5. **Resolution Operator ρ : B × Σ →ᵗ B′**:  
   - Partially defined; a bubble can be resolved only if all of its descend[7D[K
descendants are closed.

6. **Well‑nestedness at Position i**: Requires U(B_j) = 0 for all B_j ≺ B_i[3D[K
B_i (i.e., the scope stack remains acyclic).

7. **Primitive Operators**  
   - *Open*: Introduces a new bubble into Σ without immediate resolution.  [K

   - *Pop*: Closes the topmost open bubble, potentially modifying parent sc[2D[K
scopes.  
   - *Meldπ*: Merges two bubbles via a specific merging rule π.  
   - *Reframecϕ*: Changes containment relations according to constraints ϕ_[2D[K
ϕ_c (e.g., narrative re‑interpretation).  
   - *Reframeeϕ*: Adjusts expectations E based on new evidence or context ϕ[1D[K
ϕ_e.

8. **Conservative vs. Expansive Reframe**:  
   - *Conservative* reframing keeps the transitive closure ≺∗ unchanged, en[2D[K
ensuring no unnecessary extensions.  
   - *Expansive* reframing extends ≺∗ (adding new parent relations), allowi[6D[K
allowing broader semantic integration.

---

### B. Worked Examples

#### 1. Arithmetic Evaluation

Consider the expression:  

`(3 + (4 × (2 + 1)))`.

Stepwise reduction using recursive containment:

1. **Innermost**: `(2 + 1) = 3`.  
   Stack becomes `[B₁, B₂]` with `U(B₂) = U(4 × 3)`.  
2. **Next Level**: `4 × 3 = 12`.  
   Now stack is `[B₁, B₃]`, where `B₃ = (4 × 3)` has zero unresolved load. [K
 
3. **Outermost**: `3 + 12 = 15`.  

Each arrow corresponds to an admissible Pop operation; the unresolved load [K
monotonically decreases.

#### 2. Narrative Induction

Open a narrative with:

- **B₁** (Frame Story) → interrupt → open **B₂** (Embedded Story) → interru[7D[K
interrupt → open **B₃** (Innermost Anecdote).  

Resolution cascade closes B₃ first, modifies B₂′; then modifies B₁′ and fin[3D[K
finally empties the stack. Semantic load decreases uniformly.

#### 3. Conservative Reframe – Therapeutic Context

- **Scenario**: A client holds a childhood trauma B_trauma as the enclosing[9D[K
enclosing frame for their adult identity B_self.  
- **Therapy Action**: Re‑frame trauma into a contained episode within broad[5D[K
broader developmental narrative B_history.  

Node set remains unchanged; ancestral graph structure is preserved, but cov[3D[K
covering relations redistribute to reflect new semantic constraints.

#### 4. Expansive Reframe – Metaphorical Expansion

- **Domain**: Argument Barg (Barg) acquires an additional parent scope B_wa[4D[K
B_war through metaphor “argument = war.”  
- **Result**: The transitive closure ≺∗ is extended, embedding Barg within [K
a new domain; compatibility checks ensure properties from B_war align with [K
Barg’s existing constraints.

---

### References

1. Henk Barendregt. *The Lambda Calculus: Its Syntax and Semantics*. North‑[6D[K
North‑Holland, 1984.
2. John Baez & Bob Coecke (editors). *Applied Category Theory 2019*. Electr[6D[K
Electronic Notes in Theoretical Computer Science, 2020.
3. Gilles Fauconnier & Mark Turner. *The Way We Think: Conceptual Blending [K
and the Mind’s Hidden Complexities*. Basic Books, 2002.
4. Douglas Hofstadter. *Gödel, Escher, Bach: An Eternal Golden Braid*. Basi[4D[K
Basic Books, 1979.
5. Alicia Juarrero. *Dynamics in Action: Intentional Behavior as a Complex [K
System*. MIT Press, 1999.
6. George Lakoff & Mark Johnson. *Metaphors We Live By*. University of Chic[4D[K
Chicago Press, 1980.

---

*© Flyxion Project – Recursive Containment and Deferred Closure, 2023.*
