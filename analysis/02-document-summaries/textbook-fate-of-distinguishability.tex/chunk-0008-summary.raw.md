**Appendix E – The Fate‑Regime Hierarchy**

---

### 1.  Definition of the hierarchy

For any admissible ecology $(\fateClasses,\transRate,\admRegion)$ we define[6D[K
define a *nested* collection of fate regimes:

\[
\begin{aligned}
\PersRegime &:=\{(x,y):\survRatio(x,y)=1,\;\repEff(x,y)>0\}\\[2mm]
AdmVol      &=\{(x,y): \fateMap(x,y)\in\operatorname{int}(\admRegion)\}\\
FatePos     &=\{(x,y): \fateVol{x,y}>0\}\\
MemCap      &=\{(x,y):\repEff(x,y)>0\}\\
PartSurv    &=\{(x,y):\survRatio(x,y)>0\}\\
DistPairs   &:=\text{the full distinction space }(\distPairs).
\end{aligned}
\]

Here  

* **Persistence** ($\PersRegime$) corresponds to *perfect survival* and non[3D[K
non‑trivial repair (i.e. a positive feedback loop that prevents decay).  
* **Admissibility volume** ($AdmVol$) consists of states that lie strictly [K
inside the allowed fate region, guaranteeing compliance with system constra[7D[K
constraints.  
* **Fate‑volume positivity** ($FatePos$) guarantees that each class can be [K
reached from an initial state (the transition rate matrix has positive entr[4D[K
entries in at least one direction).  
* **Memory capability** ($MemCap$) reflects that repair mechanisms operate [K
within the population, ensuring that even a small fraction of repaired dist[4D[K
distinctions survives.  
* **Partial survival** ($PartSurv$) captures any surviving fraction above z[1D[K
zero; it is weaker than full persistence but still non‑trivial.

The inclusion order follows directly from the definitions:

\[
\PersRegime \subsetneq AdmVol \subsetneq FatePos 
\subsetneq MemCap \subsetneq PartSurv \subsetneq DistPairs .
\]

---

### 2.  Proven containment

Each implication is a consequence of how the associated quantities are defi[4D[K
defined.

1. **Persistence ⇒ admissibility**:  
   If $\survRatio=1$ and $\repEff>0$, then by definition $\fateMap(x,y)$ mu[2D[K
must lie in the interior (or at least on the boundary) of $\admRegion$, oth[3D[K
otherwise repair could not be sustained without violating the ecological co[2D[K
constraints.

2. **Admissibility ⇒ fate‑volume positive**:  
   A state inside the admissible region necessarily has a non‑zero reachabi[8D[K
reachability measure, i.e., there exists some transition path that places i[1D[K
it in $\operatorname{int}(\admRegion)$, guaranteeing $\fateVol(x,y)>0$.

3. **Fate‑volume positive ⇒ memory capability**:  
   A class with positive volume can be reached from any other point; theref[6D[K
therefore at least one repair interaction (hence a non‑zero $\repEff$) must[4D[K
must exist for some distinctions within the class, ensuring $MemCap$ holds.[6D[K
holds.

4. **Memory capability ⇒ partial survival**:  
   Because repair is present, even after all possible decay has occurred th[2D[K
there remains a positive fraction of survivors (the surviving cells are tho[3D[K
those that have undergone at least one repair event). Thus $\survRatio>0$ f[1D[K
for many points.

5. **Partial survival ⇒ the whole distinction space**:  
   By definition every point $(x,y)$ in the full distinction space either s[1D[K
survives partially or disappears; consequently the entire set $DistPairs$ i[1D[K
is contained within the regime of partial survival.

---

### 3.  Interpretation

- The hierarchy provides a *semantic ladder* for interpreting ecological ou[2D[K
outcomes: from perfectly persistent (e.g., stable populations), through str[3D[K
strictly admissible dynamics, to merely surviving groups.
- Each level adds an additional structural requirement that isolates sub‑po[6D[K
sub‑populations with distinct dynamical properties (stable vs. fluctuating [K
behavior).
- This ordering is invariant under any similarity transformation of the tra[3D[K
transition matrix; only the relative position within the hierarchy changes.[8D[K
changes.

---

**End of Appendix E – Fate‑Regime Hierarchy**

