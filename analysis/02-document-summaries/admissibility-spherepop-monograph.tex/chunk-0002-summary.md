**The Spherepop Operators – A Systematic Overview**

---

### 1. Evaluation Region (Definition)

An *evaluation region* is a bounded “bubble” \(B = (U,\partial U,\sigma,\ta[12D[K
U,\sigma,\tau)\) together with:

- **Locally admissible evaluation steps**:  
  - **Pop events** \(\spop{B'}\) for innermost bubbles \(B' \subseteq U\). [K
 
  - **Bind events** \(\sbind{a<b}{B}\) that impose extra constraints on the[3D[K
the bubble’s interior.  
  - **Refuse events** \(\srefuse{B'}\) recording inadmissibility of a poten[5D[K
potential pop.

The region captures the local context (constraints and history) for a subco[5D[K
subcomputation, making evaluation order independent – different sibling‑bub[11D[K
sibling‑bubble popping orders yield the same terminal result because each b[1D[K
bubble’s outcome depends only on its own interior content.

---

### 2. Scope as Physical Boundary

- **Boundary = Scope**: The boundary of a bubble is the physical limit beyo[4D[K
beyond which operations inside cannot affect contents outside (except via p[1D[K
pop results).  
- **Consequence**: Unlike syntactic scope in traditional PL theory, scope h[1D[K
here is a geometric property: variables bound by \(\sbind{a<b}{B}\) are lim[3D[K
limited to interior \(U\) because constraints cannot cross boundaries excep[5D[K
except through the resulting value.

**Proposition – Scope‑Locality Correspondence**

> In Spherepop, the scope of any bind event \(\sbind{a<b}{B}\) is precisely[9D[K
precisely the bubble’s interior \(U\). No operation outside \(B\) can obser[5D[K
observe its constraint effect except via the pop result.

The physical conception makes “scope errors” visually apparent (e.g., a lin[3D[K
line crossing an illegal boundary), unlike syntactic scope violations that [K
require separate analysis.

---

### 3. Dependency as Spatial Nesting

- **Dependency Encoding**: Nested bubbles encode dependency: if \(B_1\) is [K
inside \(B_2\), computation in \(B_2\) cannot proceed until \(B_1\) has bee[3D[K
been popped.  
- **Partial Order from Topology**: The nesting relation defines a partial o[1D[K
order on pop events: \(\spop{B_1} \prec \spop{B_2}\). No explicit dependenc[9D[K
dependency annotations are needed; the geometry itself encodes acyclic depe[4D[K
dependencies.

*Limitation*: Only tree‑structured dependencies (each bubble has at most on[2D[K
one containing bubble) can be expressed. Shared subexpressions require addi[4D[K
additional mechanisms like bind operations to introduce cross‑bubble constr[6D[K
constraints.

---

### 4. Refusal, Collapse, and Admissibility

- **Refuse Operator** \(\srefuse{B}\): Records that a pop was inadmissible [K
due to boundary constraints. It is not an error but a positive historical r[1D[K
record of justified deference.
  
- **Collapse Operator** \(\scollapse{q}\): Identifies histories under equiv[5D[K
equivalence relation \(\sim_q\), preserving structural invariants while com[3D[K
compressing multiple trajectories into classes. Collapse respects admissibi[9D[K
admissibility, ensuring meaningful generalization rather than erasure.

---

### 5. History and Evaluation Chains

A *Spherepop computation history* is a finite ordered sequence of events:

\[
\shist = (e_1,e_2,\ldots,e_n), \quad e_k \in \{\spop{B},\srefuse{B},\scolla[30D[K
\{\spop{B},\srefuse{B},\scollapse{q},\sbind{a<b}{B}\}.
\]

- **Primary Semantic Object**: Histories, not instantaneous values, carry m[1D[K
meaning.  
- **Evaluation Chain**: A subsequence consisting solely of pop events and t[1D[K
the bubbles they resolve traces the reduction path from initial expression [K
to terminal value.

---

### 6. Summary

The Spherepop framework treats computation as a geometric process where:

1. **Evaluation regions** provide local admissibility constraints.
2. **Scope** is realized physically by bubble boundaries, making scope erro[4D[K
errors visible.
3. **Dependency** emerges naturally from nesting, with additional mechanism[9D[K
mechanisms for non‑tree structures.
4. **Refusal** records legitimate inadmissibilities; **Collapse** generaliz[9D[K
generalizes computations while preserving meaning.

This system emphasizes locality and geometry over static syntactic rules, y[1D[K
yielding evaluation order independence and a clear visual/debuggable semant[6D[K
semantics for scope and dependency errors.

