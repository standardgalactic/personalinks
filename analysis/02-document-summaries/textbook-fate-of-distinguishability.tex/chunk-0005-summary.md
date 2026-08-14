**Entropy as Fate Contraction**

*Definition.*  
For a system Σ evolving under admissible (generative) dynamics, **fate entr[4D[K
entropy** is defined as the time‑derivative of its fate volume:

\[
\boxed{\;\fateEnt(t)= -\frac{d}{dt}\,\fateVol_{\Sigma}(t)\;}
\]

where \(\fateVol_{\Sigma}(t)\) denotes the volume (measure) of all admissib[8D[K
admissible future fate profiles reachable from Σ’s present state at time *t[2D[K
*t*.  

- **Positive entropy (\(\fateEnt(t)>0\))** → the system is losing accessibl[9D[K
accessible futures; its range of possible outcomes is contracting.  
- **Zero entropy (\(\fateEnt(t)=0\))** → fate volume remains constant; all [K
reachable futures are preserved (neutral or reversible dynamics).  
- **Negative entropy (\(\fateEnt(t)<0\))** → the system gains accessible fu[2D[K
futures; its future space is expanding.

---

### Entropy–Reachability Theorem

The rate of loss of futures can be expressed as a volume deficit between re[2D[K
reachable fate sets over an infinitesimal interval:

\[
\boxed{\;\fateEnt(t)\,\varepsilon \approx 
        \Vol\!\bigl(\fateReach_{\Sigma}(t)
               \setminus
               \fateReach_{\Sigma}(t+\varepsilon)\bigr),\;}
\]

where \(\varepsilon>0\) is a small time step. For sufficiently tiny \(\vare[7D[K
\(\varepsilon\),

\[
\frac{\Vol(\fateReach_{\Sigma}(t))-\Vol(\fateReach_{\Sigma}(t+\varepsilon))\frac{\Vol(\fateReach_{\Sigma}(t))-\Vol(\fateReach_{\Sigma}(t+\varepsilon))}
     {\varepsilon}
   = -\frac{d}{dt}\,\fateVol_{\Sigma},
\]

so \(\fateEnt(t)\cdot\varepsilon\) equals the volume of fate profiles that [K
disappear between *t* and *t + ε*.  

---

### The Second Law as Fate Contraction

The **Second Law of Thermodynamics** is a direct consequence of the monoton[7D[K
monotonic decrease (or non‑increase) of fate entropy in isolated systems:

1. **Isolated Systems:** No external energy can be supplied to change \(\fa[5D[K
\(\fateVol_{\Sigma}\) except via admissible operators, which preserve or in[2D[K
increase \(\fateEnt\).  
2. **Irreversibility:** In irreversible processes (e.g., heat flow from hot[3D[K
hot to cold reservoir), the reachable fate volume shrinks (\(\dot{\fateVol}[17D[K
(\(\dot{\fateVol}<0\)), giving a positive \(\fateEnt\) and thus an overall [K
entropy increase.

Consequently, in thermodynamics we state: *entropy never decreases* because[7D[K
because it measures the irreversible contraction of accessible futures.  

---

### Unifying Entropy Formulations

- **Physical (thermodynamic) entropy** ↔ loss of macroscopic future states [K
via heat diffusion.  
- **Information/Statistical entropy** ↔ loss of distinguishable microstates[11D[K
microstates, again reflected by a reduction in \(\fateVol\).  

Both arise from the same underlying geometric principle: *entropy is fundam[6D[K
fundamentally the rate at which fate volume contracts*. This unifies the tr[2D[K
treatment across PBT (Poincaré‑Brouwer theorem) and EOD (Ecology of Distinc[7D[K
Distinctions), providing a single, unified definition grounded in fate geom[4D[K
geometry rather than abstract concepts like disorder or missing information[11D[K
information.
