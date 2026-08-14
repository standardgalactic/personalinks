**Capacity as Observational Resolution**

The distinguishability capacity  

\[
\capObs{X}\;=\;\log\bigl|\operatorname{quotient}_{\obs}\bigr|
\]

from Chapter 2 quantifies how many operationally distinct
categories the observation family \(\obs\) can create in \(X\).
Equivalently, it is the maximum number of bits needed to label a
state uniquely within the equivalence classes defined by \(\obs\);
a larger capacity means finer observational resolution.

---

**Partition Lattice as a Dynamic Framework**

The quotient‑partition lattice (the set of all equivalence
classes under \(\sim_{\obs}\)) naturally encodes which distinctions
remain observable after a transformation.  However, this static
lattice is inadequate for describing dynamic processes because:

1. **Collapsing Distinctions** – Transformations can merge
   previously distinct classes, moving the system to a finer
   partition (downward movement).  
2. **Creating New Distinctions** – Some transformations may split an
   equivalence class into separate ones (upward movement), raising
   capacity temporarily.  
3. **Lateral Movements** – Transport or damage can shift systems
   between adjacent partitions without changing the overall
   resolution, reflecting repair or transport dynamics.

These movements are precisely what require a dynamic description,
leading to Part II’s operator framework where operators act on the
capacity as a conserved potential rather than merely permuting
the partition itself.

---

**Capacity as a Conserved Potential**

In this static picture, capacity plays the role of an invariant
potential: it is unchanged by any admissible transformation that
preserves distinguishability.  Operators (e.g., time‑evolution,
repair operations) can change the *state* within each class but do
not alter \(\capObs{X}\).  This invariance underlies why capacity
provides a meaningful measure of information content across dynamics.

---

**Bridge to Operator Algebra**

The static partition geometry is formally connected to operator
algebra by recognizing that every transformation can be viewed as an
operator acting on the space of partitions.  In Part II, we will:

* Define **dynamical operators** \(U\) such that  
  \(\partial^{\!U}\) (the induced partition mapping) maps each class
  to another while preserving capacity.
* Show how **repair operators** act upward in the lattice,
  increasing capacity temporarily before returning to a lower state.
* Use **transport operators** to model lateral moves, illustrating that
  observable transitions need not be monotonic.

Thus, capacity serves as a conserved invariant upon which all dynamic
operators operate, guiding the transition from static partition theory
to the full operator framework of Part II.

