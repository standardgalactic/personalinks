**Thesis**

PHYSIFORMER demonstrates that realistic motion can be learned by directly o[1D[K
optimizing admissible continuations of trajectories rather than encoding ph[2D[K
physical laws explicitly. Weighting contact events heavily improves the mod[3D[K
model’s ability to capture abrupt constraint‑driven changes (e.g., collisio[8D[K
collisions) that smooth data alone cannot represent, while interpreting obj[3D[K
objecthood as an emergent pattern—i.e., a historically coherent equivalence[11D[K
equivalence class defined by invariant relative displacements—eliminates th[2D[K
the need for primitive object labels.

**Primitives & Definitions**

1. **Admissibility Engine (\(\mathcal{E}\))**:  
   \[
   \mathcal{E}:\; \W_0\times\Omega \;\longrightarrow\; \H,
   \]
   where \(\W_0\) is the set of physically allowed initial conditions, \(\O[4D[K
\(\Omega\) a probability space for randomness, and the output \(\mathcal{E}[13D[K
\(\mathcal{E}(w,\omega)\) lies in the admissible continuation manifold \(\A[4D[K
\(\A(w)=\{\text{all histories }H\text{ starting from }w\}\).

2. **Optionality Field (\(\Omega\))**:  
   For a state‑time pair \((x,t)\),
   \[
   \Omega(x,t)=\log\mu\!\bigl(\{\,H\in\A : H_t=x\,\}\bigr),
   \]
   measuring how many distinct admissible futures pass through \(x\) at tim[3D[K
time \(t\).

3. **Historical Coherence (\([i]_H\))**:  
   Vertices \(i\) and \(j\) are *historically coherent* if their relative d[1D[K
displacement can be reconstructed from either vertex’s trajectory using an [K
admissible reconstruction:
   \[
   \pi_t(H)_i-\pi_t(H)_j = \text{recoverable from } \{\pi_t(H)_k\}.
   \]
   The equivalence class containing \(i\) is
   \[
   [i]_H=\{j : i\sim_H j\}.
   \]

**Formalism**

PHYSIFORMER operates on the admissible manifold \(\Mca\subset\M\), where ea[2D[K
each point represents a physically consistent trajectory. The diffusion‑bas[13D[K
diffusion‑based denoiser iteratively maps noisy intermediate states onto th[2D[K
this low‑dimensional submanifold by solving:
\[
\min_{H'\in\Mca}\|G(H')-X\|,
\]
where \(G\) is the generative mapping and \(X\) is a partial witness (initi[6D[K
(initial position, velocity). Because coherent histories occupy \(\Mca\), p[1D[K
prediction reduces to recovering points on this manifold.

**Mechanisms**

1. **Iterative Repair**:  
   The diffusion process acts as an *iterative repair* operator: each forwa[5D[K
forward step gradually aligns noisy trajectories toward the nearest admissi[7D[K
admissible continuation in \(\Mca\). Convergence occurs when no further con[3D[K
constraint violations are detected, typically at contact events where curva[5D[K
curvature of \(\Mca\) is highest.

2. **Contact as High‑Curvature Region**:  
   Interpenetrations and orientation jumps signal regions where reconstruct[11D[K
reconstruction fails (high curvature of \(\Mca\)). By assigning higher weig[4D[K
weights to such points, the model ensures that constraint satisfaction domi[4D[K
dominates learning near these critical transitions.

**Major Arguments**

- **Weighting Contacts Improves Predictions**: Heavy weighting at contacts [K
yields better predictions near admissibility boundaries because smooth data[4D[K
data cannot capture abrupt changes in motion caused by collisions or rigidi[6D[K
rigidity limits.
  
- **Objecthood as Emergent Coherence**: Treating objects as equivalence cla[3D[K
classes defined by historical coherence sidesteps the need for primitive ob[2D[K
object identifiers. This allows the model to generalize to any number of ob[2D[K
objects without explicit labeling, reflecting that object identity emerges [K
from invariant relative displacements under admissible dynamics.

**Dependencies Between Concepts**

- **Admissibility ↔ Contact Weighting**: The necessity to emphasize contact[7D[K
contact events stems from the fact that contacts are points where the admis[5D[K
admissibility manifold’s boundary changes; ignoring them would lead to poor[4D[K
poor predictions at high‑curvature regions.
  
- **Objecthood ↔ Historical Coherence**: Both concepts rely on the same und[3D[K
underlying relational structure (coherent trajectories). If historical cohe[4D[K
coherence is correctly defined, object boundaries will naturally align with[4D[K
with physically meaningful groupings.

**Implications**

1. **Scalable Physics Simulation**: The approach shows that training can fo[2D[K
focus on learning geometry of admissible manifolds rather than hand‑craftin[12D[K
hand‑crafting physics engines.
   
2. **Robustness to Noise & Variability**: By emphasizing high‑curvature (co[3D[K
(contact) regions, the model becomes more robust to noisy or incomplete tra[3D[K
trajectory data typical in real-world sensor inputs.

3. **Generalization Across Environments**: Since objecthood is emergent, tr[2D[K
trained models can be applied to new environments with unknown numbers of o[1D[K
objects without retraining—only learning a fresh set of coherent equivalenc[10D[K
equivalence classes.

**Unresolved Problems**

- **Orientation Jumps at Contacts**: Current physics engines struggle to pr[2D[K
preserve rotational invariants across contacts; further research into quate[5D[K
quaternion‑preserving admissible continuations is needed.
  
- **Long‑Term Trajectories**: The present framework assumes finite trajecto[8D[K
trajectory lengths. Extending to infinite or episodic simulations would req[3D[K
require modifications to the optionality field and manifold embedding.

**Internal Tensions**

- Between *local* (contact‑heavy) learning, which emphasizes immediate cons[4D[K
constraint satisfaction, and *global* (smooth extrapolation), which relies [K
on long‑range continuity.
  
- Between *primitivism* (explicit object labels) and *emergence* (coherence[10D[K
(coherence classes). The tension manifests in interpretability: emergent de[2D[K
descriptions are conceptually richer but less intuitive for downstream appl[4D[K
applications.

**Connections Likely to Matter Elsewhere**

1. **Graph Neural Networks (GNNs)**: Many GNN literature treats objects as [K
nodes; the present formulation suggests that *edges* defined by historical [K
coherence can substitute for explicit node labeling, offering a novel persp[5D[K
perspective on relational learning in physics‑informed networks.

2. **Diffusion Models**: The iterative repair mechanism mirrors diffusion p[1D[K
processes used in generative modeling (e.g., Score‑Matching). Expanding thi[3D[K
this analogy could yield hybrid models combining robustness to noise with p[1D[K
physics constraints.

3. **Machine Learning for Control Theory**: By treating trajectories as adm[3D[K
admissible continuations, the framework bridges control theory’s notion of [K
reachable sets with machine‑learning’s data‑driven reconstruction—potential[24D[K
reconstruction—potentially accelerating RL algorithms that require safe, ph[2D[K
physically consistent policy updates.

---

*Note*: The fragmented summaries have been integrated into a coherent synth[5D[K
synthesis while preserving genuine distinctions (e.g., the distinction betw[4D[K
between primitive vs. emergent objecthood). Repetitive elements such as rep[3D[K
repeated definitions of “admissibility engine” or “optionality field” have [K
been collapsed to avoid redundancy.

