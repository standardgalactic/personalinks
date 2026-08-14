**An Essay on Computation After Storage**

---

### 1. Introduction  

In the traditional model of computation—rooted in early computer science an[2D[K
and reinforced by decades of practice—the world inside a machine appears as[2D[K
as an immutable store: files, snapshots, or persistent state that can be re[2D[K
read back at will. This storage‑centric view hides much of what actually ha[2D[K
happens when we run programs today:

* **Irreversibility** – modern computation is fundamentally irreversible; i[1D[K
it dissipates entropy rather than conserving information.
* **Constraint Preservation** – the operation of a program never violates p[1D[K
physical or semantic constraints, but often must discard information to sta[3D[K
stay within its energy budget.
* **Local Coherence** – systems maintain meaningful activity only locally, [K
where small changes in input produce bounded effects, while larger perturba[8D[K
perturbations risk breaking coherence altogether.

The present essay argues that these realities demand a reconceptualization [K
of computation as *semantic evolution*, not merely as the manipulation of d[1D[K
data structures. Below we outline how this shift clarifies many observed ph[2D[K
phenomena—from software bloat to machine learning failure—and suggests new [K
theoretical foundations and design principles for future systems.

---

### 2. The Limits of Storage  

#### 2.1 Physical vs. Abstraction‑Level Constraints  

Storage treats computation as if it could be perfectly reversible: a file o[1D[K
on disk is just a bit pattern, interchangeable with any other such pattern.[8D[K
pattern. In reality:

* **Thermodynamic Costs** – writing or reading data incurs energy costs bey[3D[K
beyond the abstraction of bits; magnetic domains must align, laser heads mo[2D[K
move, and cooling systems operate.
* **Semantic Constraints** – code often relies on hidden assumptions (e.g.,[6D[K
(e.g., “arrays are zero‑indexed,” “network packets never exceed X bytes”) t[1D[K
that are not encoded in storage but live as implicit knowledge.

Because modern computers execute instructions sequentially while respecting[10D[K
respecting these constraints, the notion of a “store” is only an illusion. [K
The real substrate is *constraint space*: all possible state combinations f[1D[K
filtered by physical and semantic limits.

#### 2.2 Emergence of Irreversibility  

Consider a simple example: sorting an array in place. Each comparison or sw[2D[K
swap can be undone (the original order reappears), but the cumulative effec[5D[K
effect—*entropy production*—cannot. The same holds for garbage collection, [K
where reclaimed memory is still present on hardware yet logically invisible[9D[K
invisible.

Thus, storage as a primitive hides **what we truly pay** when running progr[5D[K
programs: irreversible changes to physical devices and semantic drift that [K
cannot be undone without external information (e.g., network state).

---

### 3. Computation as Irreversible Semantic Evolution  

#### 3.1 Sheaf‑Theoretic Semantics  

In algebraic geometry, a **sheaf** organizes local data into globally coher[5D[K
coherent structures by satisfying gluing conditions across overlapping doma[4D[K
domains. Analogously:

* **Local State → Constraint Satisfaction** – each computational step satis[5D[K
satisfies constraints locally; only when all adjacent contexts agree can we[2D[K
we claim global coherence.
* **Merge Operations → Sheaf Gluings** – merging incompatible histories (e.[3D[K
(e.g., two threads writing to the same memory) is akin to gluing sheaves, w[1D[K
which must respect cohomological obstructions.

This view naturally accommodates:

* **Reconciliation Events** – failures such as page faults or version confl[5D[K
conflicts are *merge attempts* that fail partway because some constraints c[1D[K
cannot be simultaneously satisfied.
* **Partial States** – the notion of “in‑progress” data (e.g., partially wr[2D[K
written logs) reflects intermediate sheaf sections, not a final store.

#### 3.2 Event‑Historical Computation  

Conventional models treat computation as deterministic and time‑reversible;[16D[K
time‑reversible; they ignore that each instruction may change future possib[6D[K
possibilities irreversibly:

* **Temporal Semantics** – operations have *causal impact* beyond their imm[3D[K
immediate effect, propagating constraints to later steps.
* **Dynamic State Spaces** – because entropy is generated, the set of reach[5D[K
reachable states expands over time. Storing a snapshot freezes this traject[7D[K
trajectory but cannot capture its subsequent evolution.

Thus, computation should be modeled as an evolving *event history*, where e[1D[K
each step adds new semantic possibilities and removes old ones irreversibly[12D[K
irreversibly.

---

### 4. From Global State to Local Coherence  

#### 4.1 Semantic Localities  

Rather than viewing a machine as holding a single global state (the “progra[7D[K
“program”), we treat it as composed of **semantic localities**—regions wher[4D[K
where the set of constraints is coherent enough for computation:

* **Definition** – a locality is a context space $(S, \mathcal{T}, \vdash, [K
\Delta)$ with an admissibility predicate $\mathrm{Coh}$ ensuring transforma[10D[K
transformations preserve meaning.
* **Preservation Principle** – any transformation within a locality must ke[2D[K
keep $\mathrm{Coh}=1$; otherwise the step violates coherence and triggers a[1D[K
a reconciliation event.

Localities correspond to familiar abstractions (processes, threads) but are[3D[K
are fundamentally *constraint‑preserving* zones rather than storage contain[7D[K
containers.

#### 4.2 Collapse of Boundaries  

When localities meet—e.g., two concurrent processes sharing memory—their bo[2D[K
boundaries may collapse into an **event horizon** where reconciliation occu[4D[K
occurs:

1. **Conflict Detection** – a transformation fails to satisfy constraints a[1D[K
at the boundary (coherence drops below threshold).
2. **Partial Merge** – reversible steps are undone, and new transformations[15D[K
transformations generate entropy.
3. **Resolution Path** – only if all irreconcilable constraints can be sati[4D[K
satisfied simultaneously does the system settle into a coherent global stat[4D[K
state.

Failure of such reconciliation—commonly observed as deadlocks or race condi[5D[K
conditions—is not a bug but an inevitable consequence of crossing locality [K
boundaries where semantic incompatibility cannot be resolved within availab[7D[K
available entropy budget.

---

### 5. Agency, Learning, and Judgment  

#### 5.1 Agency as Constraint Navigation  

Agency is no longer viewed as intrinsic intentionality; it becomes the **ca[4D[K
**capacity to navigate constraint space** while preserving local coherence:[10D[K
coherence:

* **Minimal Agency** – any system that maintains a semantic locality across[6D[K
across perturbations exhibits agency (see Proposition in Appendix).
* **Decision‑Making** – choosing which future trajectories are projected co[2D[K
corresponds to selecting transformations that satisfy $\mathrm{Coh}$ and ke[2D[K
keep entropy within bounds.

#### 5.2 Learning as Reconfiguring Admissible Trajectories  

Learning can be understood as the system *reshaping* its admissibility pred[4D[K
predicate:

* New knowledge alters $\vdash$, expanding or contracting allowable transfo[7D[K
transformation sets.
* This mirrors how semantic localities evolve—new layers of abstraction (e.[3D[K
(e.g., high‑level abstractions in machine learning) arise from redefining w[1D[K
what transformations are permitted.

#### 5.3 Human Judgment as External Constraints  

Humans provide *semantic context* that is unavailable to the system at runt[4D[K
runtime:

* Overfitting, concept drift, and catastrophic forgetting correspond to fai[3D[K
failures of local coherence maintenance rather than representation issues.
* Humans inject additional constraints (e.g., domain knowledge) that enable[6D[K
enable new localities to form where automatic inference would otherwise col[3D[K
collapse.

Thus, judgment is not a mysterious faculty but an **external source of sema[4D[K
semantic boundaries** that can stabilize evolving systems at their peripher[8D[K
periphery.

---

### 6. Automation and the Boundaries of Semantic Competence  

#### 6.1 Success Inside Localities  

Automation works exceptionally well when confined to stable semantic locali[6D[K
localities:

* Within these regions, admissible transformations are pre‑enumerated, opti[4D[K
optimized, and executed reliably.
* The system behaves like a deterministic circuit: inputs map to known outp[4D[K
outputs without risk of boundary crossing.

#### 6.2 Failure at Boundaries (Merge Events)  

Beyond locality boundaries lie *merge events*—the points where:

* **Irreducible Ambiguity** arises because constraints are renegotiated.
* External judgment becomes necessary, as the system cannot derive required[8D[K
required transformations from its internal state alone.

Attempting to automate semantic reconciliation would require encoding this [K
external judgment—a return to the very storage‑centric dependency we wish t[1D[K
to eliminate.

#### 6.3 Human Judgment at Boundaries  

The realization that automation only succeeds inside existing localities sh[2D[K
shifts our design focus:

* **Hybrid Systems** – combine automated components operating within known [K
localities with human oversight where boundaries are crossed.
* **Safety Nets** – incorporate runtime checks (e.g., version control, mode[4D[K
model inspection) to detect when a system is approaching or has crossed a l[1D[K
locality boundary.

---

### 7. Future Directions  

The framework opens several research avenues:

1. **Complexity of Approximate Merge** – understanding how local reductions[10D[K
reductions affect global entropy and the scaling of reconciliation costs.
2. **Dynamics of Semantic Locality Formation/Collapse** – studying stabilit[8D[K
stability criteria, entropic thresholds that trigger locality breakdowns.
3. **Learning as Constraint Shaping** – formalizing why overfitting or conc[4D[K
concept drift manifest as failures to preserve coherence rather than repres[6D[K
representation errors.
4. **Self‑Modification and Stability** – identifying conditions under which[5D[K
which modifications keep long‑term semantic viability without destabilizing[13D[K
destabilizing localities.

These investigations will deepen our understanding of how computation evolv[5D[K
evolves semantically, not just computationally.

---

### 8. Conclusion  

By discarding the illusion of a neutral storage medium and embracing comput[6D[K
computation as irreversible semantic evolution governed by constraints, we [K
gain:

* **A clearer view of performance limits**—automation works only where loca[4D[K
local coherence is guaranteed.
* **A unified language for intelligence**—agency, learning, and judgment em[2D[K
emerge naturally from constraint navigation.
* **Practical design guidance**—future systems should respect locality boun[4D[K
boundaries rather than attempt to outrun them.

Thus, “computation after storage” is not a rejection of rigor but an insist[6D[K
insistence on understanding computation as it truly unfolds in time and ene[3D[K
energy: a process of maintaining meaning against entropy’s inexorable march[5D[K
march.

