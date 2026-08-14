**Definitions**

1. **Admissibility Engine (Definition)**  
   For a domain \(\W\) an *admissibility engine* \(\mathcal{E}\) is a map  [K


   \[
   \mathcal{E}:\; \W_0\times\Omega \;\longrightarrow\; \H,
   \]

   where \(\W_0\) denotes the space of admissible initial conditions,  
   \(\Omega\) a probability space for randomness, and the output
   \(\mathcal{E}(w,\omega)\) lies in the set of *admissible continuations* [K
 

   \[
   \A(w)=\{\text{all physically allowed histories starting from }w\}.
   \]

2. **Optionality Field (Definition)**  
   Let a reference measure \(\mu\) be defined on the admissibility manifold[8D[K
manifold
   \(\H\). The *optionality field* is  

   \[
   \Omega:\mathcal{S}\times[0,T]\to[0,\infty),\qquad 
   \Omega(x,t)=\log\mu\!\bigl(\{\,H\in\A : H_t=x\,\}\bigr),
   \]

   measuring how many distinct admissible futures pass through a given
   state \(x\) at time \(t\).

**Equations & Distinctions**

- **Admissibility Constraint (Proposition)**  
  If stronger physical constraints \(\Granite'\) imply weaker constraints
  \(\Granite\) (\(\Phi' \supset \Granite\)), then for any state‑time pair  [K


  \[
  \Omega'(x,t)\le\Omega(x,t).
  \]

  This follows because a larger admissible set (more constraints) reduces
  the logarithmic measure of histories through that point.

- **Objecthood vs. State**  
  *Objecthood* is defined by historical coherence (\([i]_H\) for history \([10D[K
history \(H\)),
  not by primitive labels such as “cube” or “bunny”. A model trained on
  admissibility learns to identify the underlying coherent continuation,
  explaining why a cube and a teapot (different geometric objects) are trea[4D[K
treated
  identically.

**Mechanisms**

1. **Iterative Repair (PHYSIFORMER)**  
   The diffusion‑based denoiser acts as an *iterative repair* operator on t[1D[K
the
   manifold \(\Mca\) of admissible trajectories: each forward step graduall[8D[K
gradually
   aligns noisy intermediate states toward a physically consistent path,
   converging when no further violations exist.

2. **Persistence → Recoverability → Repairability**  
   The core principle is that coherent histories occupy a low‑dimensional
   submanifold \(\Mca\) of the ambient space; thus prediction reduces to
   recovering a point on this manifold from partial witnesses (initial
   positions and velocities).

3. **Contact as High‑Curvature Region**  
   Interpenetrations, orientation jumps at contacts indicate where
   reconstruction fails—these are precisely the high‑curvature patches of
   \(\Mca\) that require stronger constraint satisfaction.

**Key Insights & Limitations**

- The architecture implicitly demonstrates that *prediction need not rely o[1D[K
on
  explicit law encoding*; learning to repair admissible trajectories suffic[6D[K
suffices.
- Current limitations (e.g., orientation discontinuities, fixed trajectory [K
length)
  highlight where the manifold’s curvature becomes intractable and suggest [K
future
  work toward more expressive physics encodings.

**References**

1. Chen, Y., Lan, Y., & Vedaldi, A. *PHYSIFORMER*: Learning to Simulate Mec[3D[K
Mechanics
   in World Space (arXiv:2606.27364, 2026).

2. Battaglia, P. W., Pascanu, R., Lai, M., Rezende, D. J., & Kavukcuoglu,
   K. *Interaction Networks for Learning about Objects, Relations and Physi[5D[K
Physics*
   (NeurIPS 2016).

3. Pfaff, T., Fortunato, M., Sanchez‑Gonzalez, A., & Battaglia, P.
   *Learning Mesh-Based Simulation with Graph Networks* (ICML 2021).

4. Sanchez‑Gonzalez, A., Godwin, J., Pfaff, T., Ying, R., Leskovec,
   J., & Battaglia, P. *Learning to Simulate Complex Physics with Graph
   Networks* (ICLR 2020).

5. Shao, Y., & Xie, S. *Scalable Diffusion Models with Transformers*
   (NeurIPS 2022).

6. Lipman, Y., Chen, R. T. Q., Ben‑Hamu, H., Nickel, M., & Le,
   M. *Flow Matching for Generative Modeling* (arXiv:2210.02747, 2022).

7. Ho, J., Jain, A., & Abbeel, P. *Denoising Diffusion Probabilistic
   Models* (NeurIPS 2020).

8. Todorov, E., Erez, T., & Tassa, Y. *MuJoCo*: A Physics Engine for Model‑[6D[K
Model‑Based Control*
   (ICRA 2012).

9. Allen, K. R., Rubanova, Y., Lopez‑Guevara, T., Whitney,
   W., Sanchez‑Gonzalez, A., Battaglia, P., & Pfaff, T.
   *Learning Rigid Dynamics with Face Interaction Graph Networks* (arXiv:22[9D[K
(arXiv:2212.03574,
   2022).

10. Kabsch, W. *A Solution for the Best Rotation to Relate Two Sets of Vect[4D[K
Vectors*
    (Acta Crystallographica 32B, 1976).

