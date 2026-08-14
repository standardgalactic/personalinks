**Appendix E – The Fate‑Regime Hierarchy**

---

### 1. Definition of the hierarchy  

For any admissible ecology \((\fateClasses,\transRate,\admRegion)\) we defi[4D[K
define a *nested* collection of fate regimes:

\[
\begin{aligned}
\PersRegime &:=\{(x,y):\survRatio(x,y)=1,\;\repEff(x,y)>0\\
AdmVol      &=\{(x,y): \fateMap(x,y)\in\operatorname{int}(\admRegion)\\
FatePos     &=\{(x,y): \fateVol{x,y}>0\\
MemCap      &=\{(x,y):\repEff(x,y)>0\\
PartSurv    &=\{(x,y):\survRatio(x,y)>0\\
DistPairs   &:=\text{the full distinction space }(\distPairs).
\end{aligned}
\]

Here  

* **Persistence** (\(\PersRegime\)) corresponds to *perfect survival* and n[1D[K
non‑trivial repair (i.e. a positive feedback loop that prevents decay).  
* **Admissibility volume** (\(AdmVol\)) consists of states that lie strictl[7D[K
strictly inside the allowed fate region, guaranteeing compliance with syste[5D[K
system constraints.  
* **Fate‑volume positivity** (\(FatePos\)) guarantees that each class can b[1D[K
be reached from an initial state (the transition rate matrix has positive e[1D[K
entries in at least one direction).  
* **Memory capability** (\(MemCap\)) reflects that repair mechanisms operat[6D[K
operate within the population, ensuring a non‑zero \(\repEff\) for some dis[3D[K
distinctions.  
* **Partial survival** (\(PartSurv\)) captures any surviving fraction above[5D[K
above zero; it is weaker than full persistence but still non‑trivial.

The inclusion order follows directly from the definitions:

\[
\PersRegime \subsetneq AdmVol \subsetneq FatePos 
\subsetneq MemCap \subsetneq PartSurv \subsetneq DistPairs .
\]

---

### 2. Proven containment  

Each implication is a consequence of how the associated quantities are defi[4D[K
defined.

1. **Persistence ⇒ admissibility**:  
   If \(\survRatio=1\) and \(\repEff>0\), then by definition \(\fateMap(x,y[14D[K
\(\fateMap(x,y)\) must lie in the interior (or at least on the boundary) of[2D[K
of \(\admRegion\); otherwise repair could not be sustained without violatin[8D[K
violating ecological constraints.

2. **Admissibility ⇒ fate‑volume positive**:  
   A state inside the admissible region necessarily has a non‑zero reachabi[8D[K
reachability measure, i.e., there exists some transition path that places i[1D[K
it in \(\operatorname{int}(\admRegion)\), guaranteeing \(\fateVol(x,y)>0\).[20D[K
\(\fateVol(x,y)>0\).

3. **Fate‑volume positive ⇒ memory capability**:  
   A class with positive volume can be reached from any other point; theref[6D[K
therefore at least one repair interaction (hence a non‑zero \(\repEff\)) mu[2D[K
must exist for some distinctions within the class, ensuring \(MemCap\) hold[4D[K
holds.

4. **Memory capability ⇒ partial survival**:  
   Because repair is present, even after all possible decay has occurred th[2D[K
there remains a positive fraction of survivors (the surviving cells are tho[3D[K
those that have undergone at least one repair event). Thus \(\survRatio>0\)[16D[K
\(\survRatio>0\) for many points.

5. **Partial survival ⇒ the whole distinction space**:  
   By definition every point \((x,y)\) in the full distinction space either[6D[K
either survives partially or disappears; consequently the entire set \(Dist[6D[K
\(DistPairs\) is contained within the regime of partial survival.

---

### 3. Interpretation  

- The hierarchy provides a *semantic ladder* for interpreting ecological ou[2D[K
outcomes: from perfectly persistent (e.g., stable populations), through str[3D[K
strictly admissible dynamics, to merely surviving groups.  
- Each level adds an additional structural requirement that isolates sub‑po[6D[K
sub‑populations with distinct dynamical properties (stable vs. fluctuating [K
behavior).  
- This ordering is invariant under any similarity transformation of the tra[3D[K
transition matrix; only the relative position within the hierarchy changes.[8D[K
changes.

**End of Appendix E – Fate‑Regime Hierarchy**
