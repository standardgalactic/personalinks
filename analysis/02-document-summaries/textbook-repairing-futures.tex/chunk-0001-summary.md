**Contact‑Event Weighting in Trajectory Diffusion**

1. **Why weight contact events heavily?**  
   - Contact points (edges where two vertices meet) define instantaneous ch[2D[K
changes in geometry—rigidity constraints are enforced at those moments.  
   - In trajectory data the admissibility boundary is sharp around contacts[8D[K
contacts: a tiny violation of rigidity or momentum near a contact can be ea[2D[K
easily mis‑interpreted as smooth noise elsewhere.  
   - Because the physics (e.g., elasticity) lives primarily at these intera[6D[K
interaction sites, learning from them provides strong signals about what *i[2D[K
*is* physically allowed versus what is not.

2. **Implication for diffusion models**  
   - Treating all events equally would treat a small deviation in free‑flow[9D[K
free‑flow segments as equally informative to correcting a violation that co[2D[K
could cause catastrophic error (e.g., unrealistic deformation).  
   - By giving contact events higher weight, the model can focus its repair[6D[K
repair operations on the regions where the most critical admissibility rule[4D[K
rules are enforced—rigidity and momentum constraints.

3. **Consequences**  
   - The resulting denoising operation becomes more robust to realistic phy[3D[K
physical perturbations (elastic stress, velocity drift) because it learns t[1D[K
to “undo” violations precisely at points where they matter most.  
   - This aligns the learning objective with the actual structure of admiss[6D[K
admissible trajectories rather than an abstract noise model.

---

**Admissibility‑Structured Perturbation**

1. **Definition Recap**  
   \[
   \mathcal{P}_\sigma(H) \text{ perturbs } H \in \A(w) \text{ by violating [K
a chosen class (rigidity, momentum, temporal continuity) controlled by }\si[4D[K
}\sigma>0,
   \]
   while \(\mathcal{P}_0(H)=H\) for any history.

2. **Training Objective**  
   \[
   \mathcal{L}_{\text{repair}}(\theta)=\mathbb{E}_{H\in\A(w),\,\sigma}\bigl\mathcal{L}_{\text{repair}}(\theta)=\mathbb{E}_{H\in\A(w),\,\sigma}\bigl\| x_\theta(\mathcal{P}_\sigma(H),\sigma)-H\bigr\|^2,
   \]
   where \(x_\theta\) is trained to map perturbed trajectories back onto th[2D[K
the admissible manifold.

3. **Why this formulation?**  
   - The objective directly mirrors the physical repair process (e.g., rest[4D[K
restoring rigidity, momentum) rather than merely “denoising” coordinates in[2D[K
in an abstract sense.  
   - It ensures that learned features correspond to physically meaningful c[1D[K
constraints, making the model’s predictions more interpretable and reliable[8D[K
reliable for trajectory data.

---

**Repair‑Equivalence Theorem**

1. **Statement**  
   If \(\{\mathcal{P}_\sigma\}\) satisfies: *for every admissible history \[1D[K
\(H\) and sufficiently small \(\sigma\), \(\mathcal{P}_\sigma(H)\) has a un[2D[K
unique projection onto \(\A(w)\) equal to \(H\)*, then the minimizer of \(\[3D[K
\(\mathcal{L}_{\text{repair}}\) acts as a repair operator, and iterating  
   \[
   H_{k+1}=x_\theta(\mathcal{P}_\sigma(H_k),\sigma_k)
   \]
   converges to an element of \(\A(w)\) as \(\sigma_k\to0\).

2. **Proof Sketch**  
   - The projection condition guarantees that the perturbed trajectory lies[4D[K
lies in a neighborhood where the target \(H\) is uniquely recoverable.  
   - Minimizing the squared loss forces \(x_\theta^*\) to map any admissibl[9D[K
admissible history back exactly onto itself, i.e., it learns the identity m[1D[K
mapping on the manifold.  
   - The decreasing \(\sigma_k\) ensures that each iteration reduces the pe[2D[K
perturbation magnitude, guaranteeing convergence via contraction of the pro[3D[K
projection operator.

3. **Interpretation**  
   - This theorem shows that Gaussian‑noise diffusion and admissibility‑str[17D[K
admissibility‑structured diffusion are mathematically equivalent in terms o[1D[K
of their repair property: both lead to a unique target once noise is suffic[6D[K
sufficiently attenuated.

---

**Objecthood as Emergent Coherence**

1. **Historical Coherence Definition**  
   For a trajectory \(H\), vertices \(i\) and \(j\) are historically cohere[6D[K
coherent (\(i\simeq_H j\)) if the relative displacement \(\pi_t(H)_i-\pi_t([19D[K
\(\pi_t(H)_i-\pi_t(H)_j\) can be reconstructed from either vertex’s traject[7D[K
trajectory alone using an admissible reconstruction family.

2. **Proposition**  
   The relation \(\sim_H\) is reflexive, symmetric, and transitive; thus it[2D[K
it partitions the vertex set into equivalence classes (objects).

3. **Implication**  
   - Object identity emerges as a relational property of *coherence* rather[6D[K
rather than being imposed as an intrinsic label.  
   - A rigid body corresponds to vertices whose relative displacements are [K
constant across time; an elastic body is a coherence class where displaceme[10D[K
displacements vary but remain reconstructible via the deformation field.

4. **PHYSIFORMER’s Attention Mechanism**  
   - By using factorized attention over time, space, and these emergent cla[3D[K
classes (instead of pre‑defined object IDs), PHYSIFORMER learns to attend a[1D[K
across vertices that belong to the same coherence class.  
   - This design naturally generalizes: when new objects appear in unseen c[1D[K
configurations, the model identifies them as novel coherence classes based [K
on invariant relative motions.

5. **Philosophical Insight**  
   - Objecthood is not a primitive entity but an *emergent pattern* of pers[4D[K
persistent coherence that can be discovered from trajectory data alone. Thi[3D[K
This aligns with physical intuition (rigidity defines object identity) and [K
supports the model’s ability to handle arbitrary numbers of objects without[7D[K
without explicit counting.

---

**Summary**

- **Contact events are weighted heavily** because they mark where fundament[9D[K
fundamental admissibility constraints (rigidity, momentum) are enforced; ne[2D[K
neglecting them would risk misinterpreting noise as acceptable behavior.
- **Admissibility‑structured diffusion** provides a principled way to pertu[5D[K
perturb trajectories so that the learned denoiser directly repairs physical[8D[K
physically meaningful violations rather than abstract coordinate corruption[10D[K
corruption.
- The **repair‑equivalence theorem** demonstrates mathematically that such [K
structured diffusion converges exactly like standard Gaussian diffusion, pr[2D[K
preserving convergence guarantees while aligning learning with physical rea[3D[K
reality.
- **Objecthood emerges from historical coherence**: vertices that share inv[3D[K
invariant relative displacements form objects without needing a priori obje[4D[K
object identifiers. This emergent property enables scalable generalization [K
to unseen object counts and reflects the true nature of physical continuity[10D[K
continuity in trajectories.

These insights collectively justify why contact events, rigidity/momentum‑p[19D[K
rigidity/momentum‑preserving perturbations, and the emergence of coherence [K
classes are central to robust trajectory prediction models like PHYSIFORMER[11D[K
PHYSIFORMER.
