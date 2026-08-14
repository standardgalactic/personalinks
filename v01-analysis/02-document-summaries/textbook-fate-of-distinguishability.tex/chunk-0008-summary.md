**Preservation Hierarchy as Fate Regimes**

The EOD preservation hierarchy corresponds to the following nested fate reg[3D[K
regimes:

\[
\persRegime \; \subsetneq \; 
\{(x,y):\fateMap(x,y)\in\operatorname{int}(\admRegion)\}
\; \subsetneq \;
\{(x,y):\fateVol{x,y}>0\}
\; \subsetneq \;
\{(x,y):\repEff(x,y)>0\}
\; \subsetneq \;
\{(x,y):\survRatio(x,y)>0\}
\; \subsetneq \;
\distPairs .
\]

*Proof.* Each containment follows directly from the definitions of the fate[4D[K
fate regimes:

1. **Persistence** (\(\survRatio=1,\repEff>0\)) is contained in admissibly [K
stable regions because persistence implies that no death transitions occur,[6D[K
occur, which is a stricter condition than merely being inside the interior [K
of \(\admRegion\).

2. Admissibly stable regions are contained in fate‑volume‑positive regions [K
since every admissible state belongs to some region with positive reachable[9D[K
reachable volume.

3. Fate‑volume‑positive states lie within memory‑capable (repair) states be[2D[K
because a non‑zero reachability volume guarantees the existence of repair t[1D[K
transitions, ensuring \(\repEff>0\).

4. Memory‑capable states are contained in partially surviving states (\(\su[6D[K
(\(\survRatio>0\)) since any state with positive repair efficiency also has[3D[K
has at least some survival probability.

5. Finally, the full distinction space includes all the above regimes as su[2D[K
subsets, representing every possible reachable fate class.

---

**App Summary**

- **PBT’s persistence**: The fate regime \(\persRegime\) consists of distin[6D[K
distinctions with unit survival ratio (\(\survRatio=1\)) and positive repai[5D[K
repair efficiency (\(\repEff>0\)).  
- **EOD’s admissibility volume**: This is the pushforward fate measure of t[1D[K
the admissible fate region, reflecting how many recoverable distinctions ma[2D[K
map into the interior of \(\admRegion\).  
- **Generative Admissibility Principle (GAP)**: It states that admissibilit[12D[K
admissibility conserves the total reachable volume within \(\admRegion\), i[1D[K
i.e., it acts as a Fate Conservation Law restricted to \(\admRegion\).  
- **EOD’s preservation hierarchy**: Describes a chain of nested fate regime[6D[K
regimes distinguished by their specific fate coordinates (survival ratio, r[1D[K
repair efficiency, etc.), illustrating how more constrained states are subs[4D[K
subsets of broader reachable volumes.

---

**The Rosetta Stone of the Trilogy**

This appendix establishes that the three coordinate systems—PBT, Fate Theor[5D[K
Theory, and EOD—are representations of a single underlying geometric struct[6D[K
structure. By constructing categories \(\catPBT\), \(\catFate\), and \(\cat[6D[K
\(\catEOD\) with appropriate functors between them (see Appendix~A), we dem[3D[K
demonstrate:

1. **Faithfulness** of the PBT‑to‑Fate functor ensures distinct recoverabil[11D[K
recoverability structures map to distinct fate structures.
2. **Fullness** of the Fate‑to‑EOD functor guarantees every ecology morphis[7D[K
morphism arises from an admissible operator, preserving the ecological dyna[4D[K
dynamics.
3. The composite functor maps persistence in \(\catFate\) (unit survival an[2D[K
and repair) to equilibrium distributions (\(\dot{N}=0\)) in \(\catEOD\).
4. Viability (positive reachable volume) corresponds to positive recurrence[10D[K
recurrence of transition rates in \(\catEOD\).

Thus, Fate Theory serves as the hinge connecting the three categories, embo[4D[K
embodying the claim that they are coordinate systems on a common mathematic[10D[K
mathematical object.

