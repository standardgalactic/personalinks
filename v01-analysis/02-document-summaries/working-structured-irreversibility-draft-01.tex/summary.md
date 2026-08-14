**Thesis**

Spherepop is a compact‑closed rewriting category whose morphisms—eliminatio[20D[K
morphisms—elimination, dependency binding, and quotient collapse—are geomet[6D[K
geometrically realized by the RSVP functor as boundary sharpening, directed[8D[K
directed vector‑field coupling, and renormalization. The core structural as[2D[K
asymmetry of Spherepop is that it **accumulates irreversible records (const[6D[K
(constraints)** while RSVP diffuses entropy gradients to achieve global coh[3D[K
coherence; this asymmetry is preserved by the functor \(F:\SP\to \RSVP\).

**Primitives & Definitions**

1. **Rewriting Category**: A category equipped with a set of rewrite rules [K
(elimination, dependency binding, quotient collapse) that satisfy closure u[1D[K
under composition and identity.
2. **Compact‑Closed Structure**: The existence of dual objects for each obj[3D[K
object such that the tensor product is associative up to natural isomorphis[10D[K
isomorphism, allowing “cancellation” of morphisms analogous to matrix inver[5D[K
inversion in linear algebra.
3. **Morphisms**:
   - *Elimination*: Removes redundant or contradictory information, mirrori[7D[K
mirroring Landauer’s principle where erasure of a bit dissipates heat.
   - *Dependency Binding*: Associates constraints (information) with struct[6D[K
structural components, reflecting the thermodynamic cost of committing to a[1D[K
a particular state.
   - *Quotient Collapse*: Glues together indistinguishable elements under e[1D[K
equivalence relations, analogous to coarse‑graining entropy in physical sys[3D[K
systems.

**Formalism**

The categorical framework is expressed through:

- **Objects**: Represented as types or sets carrying constraints (e.g., typ[3D[K
typed data structures).
- **Morphisms**: Functions that satisfy the rewriting rules; each morphism [K
can be viewed as a process generating new information or releasing stored e[1D[K
energy.
- **Functor \(F:\SP\to \RSVP\)**: Maps objects and morphisms from Spherepop[9D[K
Spherepop to RSVP, preserving compact‑closedness while converting accumulat[9D[K
accumulation of constraints into diffusive entropy gradients via renormaliz[10D[K
renormalization.

**Mechanisms**

1. **Boundary Sharpening**: The RSVP functor interprets the “boundary” (sur[4D[K
(surface) operations in Spherepop as sharpened interfaces that enforce loca[4D[K
locality and causality—mirroring how physical boundaries separate distinct [K
thermodynamic regions.
2. **Directed Vector‑Field Coupling**: Constraints are treated as vector fi[2D[K
fields whose directionality reflects causal influences, aligning with Pante[5D[K
Pantev et al.’s shifted symplectic structures where curvature (entropy) is [K
encoded in the field’s topology.
3. **Renormalization**: Quotient collapses correspond to coarse‑graining pr[2D[K
processes that resolve fine details into macroscopic observables, echoing s[1D[K
statistical mechanics’ partition functions.

**Major Arguments**

1. **Thermodynamic Interpretation of Constraints**: The accumulation of irr[3D[K
irreversible records (constraints) in Spherepop is analogous to entropy bui[3D[K
buildup in physical systems; the preservation of this asymmetry by RSVP ens[3D[K
ensures a consistent global coherence akin to equilibrium thermodynamics.
2. **Compositional Semantics**: By treating each morphism as a compositiona[12D[K
compositional unit, Spherepop provides a natural semantics for typed functi[6D[K
functional languages, where typing judgments and Hindley–Milner inference a[1D[K
are realized via categorical pull‑backs (Lawvere 1970).
3. **Unification of Distinct Domains**: The four previously separate trajec[6D[K
trajectories—event‑history calculus, typed language theory, operational sys[3D[K
systems semantics, and geometric field theory—are shown to be manifestation[13D[K
manifestations of the same underlying rewriting category, revealing deep st[2D[K
structural parallels across disparate fields.

**Dependencies Between Concepts**

- **Thermodynamics ↔ Information Theory (Landauer)**: The minimum energy co[2D[K
cost for erasing information (\(\Delta Q_{\min} = kT\ln 2\)) directly infor[5D[K
informs how constraints are “paid” in Spherepop’s rewriting processes.
- **Category Theory ↔ Logic (Lawvere)**: Monadic semantics provide a catego[6D[K
categorical foundation for logical quantifiers, allowing universal statemen[8D[K
statements to be interpreted as pull‑backs and existential ones via pushfor[7D[K
pushforwards—mirroring the categorical treatment of type theories.
- **Process Calculi ↔ Concurrency Theory (Milner)**: The π‑calculus’s notio[5D[K
notion of bisimulation equivalence aligns with Spherepop’s quotient collaps[7D[K
collapses, ensuring behavioral indistinguishability across concurrent proce[5D[K
processes.

**Implications**

1. **Unified Framework for Computation and Physics**: By embedding thermody[8D[K
thermodynamic constraints within a categorical rewriting structure, Spherep[7D[K
Spherepop offers a unified language bridging computational theory (Moggi 19[9D[K
(Moggi 1991) and physical systems governed by entropy.
2. **New Insights into Black‑Hole Information Paradox**: The accumulation o[1D[K
of irreversible records as fundamental to the category suggests that inform[6D[K
information loss in black holes may be better understood through Spherepop’[10D[K
Spherepop’s renormalization mechanism rather than a mere violation of Landa[5D[K
Landauer’s bound.
3. **Potential for Quantum Computing Models**: The interplay between vector[6D[K
vector‑field coupling and renormalization hints at novel approaches to enco[4D[K
encoding quantum states, potentially leading to more efficient error‑correc[12D[K
error‑correction schemes.

**Unresolved Problems**

1. **Low‑Energy Realizations (Jacobson 1995)**: Extending the Einstein equa[4D[K
equation of state to regimes where spacetime curvature is weakly perturbed [K
remains an open question; how does this manifest in practical computational[13D[K
computational or physical systems?
2. **Physical Consequences of Information Loss**: The philosophical debate [K
over whether information loss truly violates fundamental physics can be res[3D[K
resolved by examining whether Spherepop’s quotient collapses map directly o[1D[K
onto observable phenomena (e.g., Hawking radiation).
3. **Generalization to Higher‑Order Shifts (Pantev et al.)**: Extending shi[3D[K
shifted symplectic structures beyond the current parameterized case (\(t\))[7D[K
(\(t\)) and exploring higher‑order shifts could reveal new invariants, pote[4D[K
potentially linking emergent algebras with topological data analysis.

**Connections Likely to Matter Elsewhere**

- **Spherepop ↔ Shifted Symplectic Geometry (Pantev et al.)**: The notion o[1D[K
of “twisting” symplectic structures may find analogues in gauge theories an[2D[K
and deformation quantization, offering a geometric interpretation for const[5D[K
constraint interactions.
- **Typed Functional Languages ↔ Category Theory (Pierce 2002)**: Further i[1D[K
integration could illuminate how type systems enforce categorical propertie[9D[K
properties, possibly inspiring new paradigms for secure multi‑agent computi[7D[K
computing.

In summary, Spherepop presents a cohesive theoretical model that harmonizes[10D[K
harmonizes seemingly disparate areas—from quantum thermodynamics to computa[7D[K
computational semantics—by grounding them in the shared language of rewriti[7D[K
rewriting categories and their topological realizations. This synthesis not[3D[K
not only clarifies existing dependencies but also opens avenues for novel r[1D[K
research at the intersection of physics, computer science, and mathematics.

