**Productive Incompletion – A Computational View**

1. **What Is “Incompletion”?**  
   An artifact *a* (e.g., a painting, a proof page, an unfinished book) is [K
said to be in an *incompletion state* \(I(a)\) when its current configurati[11D[K
configuration \(c(a)\) differs from the intended final form \(\pi(a)\) by m[1D[K
more than a small threshold \(\delta\). Formally,

   \[
   d(c(a),\pi(a)) > \delta,
   \]

   where *d* is a distance metric over “configuration space.” The artifact’[9D[K
artifact’s value therefore lies in its persistent, visible gap.

2. **Recruitment Potential**  
   The computational role of that gap is captured by the *recruitment poten[5D[K
potential*  

   \[
   \rho(a) = \text{Visibility}(a)\times\text{Salience}(I(a))\times\text{Pro[62D[K
\text{Visibility}(a)\times\text{Salience}(I(a))\times\text{Proximity}(a,\te\text{Visibility}(a)\times\text{Salience}(I(a))\times\text{Proimity}(a,\text{traffic}),
   \]

   meaning an unfinished item stays cognitively “alive” because it is (i) v[1D[K
visible, (ii) carries unresolved weight, and (iii) frequently encountered i[1D[K
in ordinary movement.

3. **Zeigarnik Effect Extended**  
   The classic Zeigarnik effect shows that interrupted tasks are remembered[10D[K
remembered better than completed ones. Extending this:

   - Let \(\Lambda(a)\) be the total cognitive load imposed by *a*:
   
     \[
     \Lambda(a)=\Lambda_{\text{explicit}}(a)+\Lambda_{\text{implicit}}(a).
     \]

   - For a completed artifact, \(\Lambda_{\text{explicit}}\approx0\) and \([2D[K
\(\Lambda_{\text{implicit}}\) decays quickly.  
   - For an unfinished one, both components remain substantial for longer:

     \[
     P_{\text{engage}}(a,t)=P_0 e^{-t/\tau_{\text{incomplete}}},
     \]

     where \(\tau_{\text{incomplete}}\gg\tau_{\text{complete}}\). Thus unfi[4D[K
unfinished artifacts continuously recruit attention.

4. **Suspended Execution**  
   Scientific and mathematical work often involves *suspended processes*: a[1D[K
a proof page left open, a sketch of an argument still to be filled in. When[4D[K
When such artifacts are present,

   \[
   \text{State}(P,t+\Delta t)\approx\text{State}(P,t)\oplus\text{Context}(A[48D[K
t)\approx\text{State}(P,t)\oplus\text{Context}(A_{\text{suspend}}),
   \]

   meaning the process is not lost but automatically “resumed” by encounter[9D[K
encountering its surrounding context. This mirrors how an OS preserves a ru[2D[K
running process’s registers and memory until it can be re‑started.

5. **Order vs. Clutter**  
   The notion that visual disorder indicates computational richness challen[7D[K
challenges conventional tidy‑up advice:

   - Define *process density*  

     \[
     \Pi(E)=\sum_{a\in E}\mathbf{1}_{I(a>0)}\cdot\rho(a),
     \]

     the weighted sum of all unfinished states. High \(\Pi\) reflects many [K
suspended executions, while low \(\Pi\) may strip away needed context for r[1D[K
resuming complex work.

   - **Theorem (Optimal Incompletion):** For an environment \(E\) supportin[9D[K
supporting \(N\) concurrent projects,

     \[
     \Pi^*(E)=\arg\max_{\Pi}\Bigl[\sum_{i=1}^{N}\text{Progress}_i(\Pi)-\tex[70D[K
\Pi^*(E)=\arg\max_{\Pi}\Bigl[\sum_{i=1}^{N}\text{Progress}_i(\Pi)-\text{Dis\Pi^*(E)=\arg\max_{\Pi}\Bigl[\sum_{i=1}^{N}\text{Progress}_i(\Pi)-\tex{Distraction}(\Pi)\Bigr],
     \]

     where progress is facilitated by suspended execution states, and distr[5D[K
distraction arises when too many threads are collapsed. An optimal environm[8D[K
environment retains a non‑zero level of incompletion.

---

**Key Takeaway:** Incomplete artifacts act as “hooks” that keep relevant id[2D[K
ideas alive, allowing continuous mental work without the need for deliberat[9D[K
deliberate scheduling. This makes productive incompletion not just a by‑pro[6D[K
by‑product but an essential design principle for environments supporting co[2D[K
complex thought.

