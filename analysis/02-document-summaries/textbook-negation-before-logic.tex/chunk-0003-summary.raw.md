**Summary of Key Concepts**

1. **Memory Distortion Decay (Exponential Forgetting)**
   - The decay law for memory distortion is  
     \[
     \mathcal D_t = \mathcal D_0 e^{-2\lambda t}.
     \]
   - This result follows from the integration of a squared differential ine[3D[K
inequality, showing that distortions shrink exponentially over time.

2. **Ecphory Retrieval**
   - An *ecphory operator* maps an internal state to external data:  
     \[
     \mathcal E_t : \mathcal H \rightarrow X.
     \]
   - Retrieval success is determined by a threshold \( \theta > 0\):  
     \[
     \mathcal E_t(h) = x \quad \text{iff} \quad |h - E(x)| < \theta.
     \]

3. **Retrieval Error**
   - The error measure for retrieval is the distance between reconstructed [K
and original states:  
     \[
     \varepsilon_t(x) = d_R\bigl(x, \mathcal E_t(E(x))\bigr).
     \]
   - Perfect ecphory (retrieval without error) yields \( \varepsilon_t(x)=0[18D[K
\varepsilon_t(x)=0\).

4. **Orientation Persistence**
   - Orientation is persistent if the orientation field remains unchanged: [K
 
     \[
     \omega_t = \omega_0.
     \]
   - Under this condition, negation distortion also remains invariant.

5. **Delayed Verification Dynamics**
   - The verification state \(V_t\) is defined via a consistency functional[10D[K
functional:  
     \[
     V_t(x) = \chi(P, M_t(x)).
     \]
   - Verification latency \( \tau \) satisfies a lower bound when distortio[9D[K
distortion persists:
     \[
     \tau \ge c\Delta_0,
     \]
     where \(c>0\) is a constant. This indicates that verification requires[8D[K
requires time proportional to the initial distortion.

6. **Distortion Persistence Spectrum**
   - Modes with eigenvalues \(|\lambda_n| = 1\) lead to permanent distortio[9D[K
distortion persistence.
   - The spectrum separates into:
     - *Persistence Spectrum*: \(\sigma_P = \{\lambda_n\}\) where modes do [K
not decay.
     - *Distortion Spectrum*: \(\Sigma_D = \{\lambda_n : \phi_n \text{ cont[4D[K
contributes to } D_N\}\).

7. **Recoverability Geometry**
   - The recoverability radius is defined as:  
     \[
     \rho(x) = \sup\{r : B_r(x) \text{ is reconstructible}\}.
     \]
   - Persistence capacity is the integral of the recoverability radius over[4D[K
over the domain:
     \[
     \Phi_P = \int_X \rho(x)\, d\mu(x).
     \]
   - If \( \Phi_P < D_N^{\max} \), all negation distortions are recoverable[11D[K
recoverable.

8. **Delayed Verification Theorem**
   - Given distortion \(D_N(x) > 0\) and orientation preservation (\(\omega[9D[K
(\(\omega_t = \omega_0\)), the theorem states:
     \[
     \Delta_t(x) = D_N(x),
     \]
     and verification latency satisfies  
     \[
     \tau(x) \ge cD_N(x).
     \]
   - This shows that delayed-verification effects stem from persistent geom[4D[K
geometric distortion, not repeated syntactic computation.

9. **Persistence Principle**
   - Memory preserves distortions of reachability geometry rather than prop[4D[K
propositions.
   - Negation-induced displacement persists when orientation structure is p[1D[K
preserved, making the persistence of verification cost equivalent to geomet[6D[K
geometric distortion persistence.

10. **Admissibility Geometry (NPI Licensing)**
    - On a Riemannian manifold \((M,g)\), an admissibility field \(A\) maps[4D[K
maps points to \([0,1]\).
    - The *admissible region* is  
      \[
      \mathcal A = \{x : A(x) > 0\},
      \]
      with the fully admissible subset being  
      \[
      \mathcal A_1 = \{x : A(x) = 1\}.
      \]

    - Licensing domains are defined as:
      - *Licensing Domain*: \(L = \{x : A(x)=1, \omega(x)<0\}\).
      - *Positive Domain*: \(P = \{x : A(x)=1, \omega(x)>0\}\).
      - *Neutral Boundary*: \(B = \{x : A(x)=1, \omega(x)=0\}\).

    - Thus,
      \[
      \mathcal A_1 = P \cup B \cup L.
      \]

11. **NPI Probe Functions**
    - An NPI is represented by a probe function \(\Pi: M \rightarrow \{0,1\[6D[K
\{0,1\}\).
    - Licensing condition for a point \(x\) is:
      \[
      \Pi(x) = 1 \text{ and } x \in L.
      \]
    - The probe function is the characteristic of the licensing region.

12. **Geometric Licensing Criterion**
    - An NPI is licensed at \(x\) iff:
      \[
      A(x)=1 \quad \text{and} \quad \omega(x)<0.
      \]

13. **Connected Licensing Components**
    - A *licensing component* is a connected subset of \(L\).
    - The theorem states that every point in a licensing component licenses[8D[K
licenses NPIs, reflecting the local nature of licensing.

14. **Boundary Geometry**
    - Admissibility curvature is defined as:
      \[
      \kappa_A = \nabla\cdot\left(\frac{\nabla A}{|\nabla A|}\right),
      \]
      capturing how orientation field variations influence admissibility.

These concepts together form a framework for understanding memory dynamics,[9D[K
dynamics, retrieval processes, and the geometric underpinnings of logical l[1D[K
licensing in cognitive systems.

