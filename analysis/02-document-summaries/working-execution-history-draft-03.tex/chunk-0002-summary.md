**Event‑Historical Computation**

The core insight of this essay is that computation should be viewed as *the[4D[K
*the irreversible construction and manipulation of histories* rather than a[1D[K
as a state‑transforming process.

1. **History as Accumulated Events**  
   - A history records the sequence of irreducible events (operations) thro[4D[K
through which a system evolves. Each event excludes alternatives, thereby r[1D[K
refining the set of possible future continuations.
   - Computation is then seen as the lawful composition and ordering of the[3D[K
these exclusions.

2. **Primitive Operations**  
   The minimal operational kernel consists of three primitive operations:

   *Extension* – adds new events to an existing history (e.g., appending a [K
commit, logging a state transition).  

   *Merge* – reconciles compatible histories by identifying shared prefixes[8D[K
prefixes and integrating their divergent developments (e.g., Git merge tree[4D[K
trees or CRDT join operations).  

   *Reduction* – collapses longer histories into coarser summaries that ret[3D[K
retain essential constraints for observation (e.g., snapshots in distribute[10D[K
distributed systems).

3. **Ordered Structure**  
   These operations generate an ordered geometry over all possible historie[8D[K
histories:

   - **Ordering by Length**: Longer histories contain more constraints, mak[3D[K
making them stricter limits on future states.
   
   - **Composition of Histories**: Extending a history with another yields [K
a concatenated exclusion set, preserving the order property (if A → B and B[1D[K
B → C then A → C).

4. **Duality of Representation**  
   The paper distinguishes two dual ways to represent histories operational[11D[K
operationally:

   - *State‑Transformation View*: Histories are transformations acting on s[1D[K
states, leading to forward extensions.
   
   - *Observable‑Transformation View*: Histories are transformations acting[6D[K
acting on observables (readable summaries), yielding backward propagation.

   These representations agree empirically but impose different constraints[11D[K
constraints on factorization. Consequently, the algebra of histories is not[3D[K
not strictly self‑dual; the direction of evaluation (forward extension vs. [K
observable propagation) affects lawful intermediate steps.

5. **Implications for Abstraction and Convergence**  
   - **Abstractions**: Reduction mappings compress histories into states or[2D[K
or snapshots while preserving essential causal relationships.
   
   - **Convergence in Distributed Systems**: The append‑only structure ensu[4D[K
ensures monotonic growth, allowing deterministic replay (CRDTs) where event[5D[K
eventual convergence occurs without a global clock.

6. **Physical Analogy**  
   Similar structures appear in physical systems governed by local interact[8D[K
interactions (e.g., Ising models), where each update refines the space of f[1D[K
future possibilities, mirroring computational histories.

**Conclusion**  
Viewing computation through an *event‑historical lens* unifies diverse doma[4D[K
domains—distributed logs, version control, constraint solving, and lattice [K
dynamics—revealing a deep commonality: the progression from simple events t[1D[K
to ordered, reconcilable histories that define system state and behavior. T[1D[K
This perspective aligns computational theory with physical systems where st[2D[K
structure arises from cumulative locally constrained transitions.

