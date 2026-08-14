**Summary**

The passage presents a formal treatment of probabilistic choice and aggrega[7D[K
aggregation in a functional language that supports both deterministic (choi[5D[K
(choice) and probabilistic behavior. Key points include:

1. **Doom‑Aggregation Law**: For independent hazards \(R_i = \mathrm{Choice[14D[K
\mathrm{Choice}(p_i,\mathsf{Doom},\mathsf{Safe})\), the probability of at l[1D[K
least one “doom” event occurring is  
   \[
   \Pr[T_n=\mathsf{Doom}] = 1 - \prod_{i=1}^n (1-p_i).
   \]  
   This follows from the independence assumption and is used to compute agg[3D[K
aggregated outcomes via a `Merge` operation followed by a logical disjuncti[9D[K
disjunction (`FoldOr`) in SPC.

2. **Translation Properties**:
   - **Typing**: The compositional translation preserves typing derivations[11D[K
derivations, ensuring that types are correctly mapped between source (proba[6D[K
(probabilistic λ‑calculus) and target (structured probabilistic calculus).
   - **Operational**: Source one‑step reductions correspond to steps or equ[3D[K
equalities modulo `Merge` congruence in SPC, preserving the matching probab[6D[K
probabilities for choice.
   - **Adequacy**: Denotations commute with the translation:  
     \[
     \llbracket \mathcal{T}_{\mathrm{prob}\lambda}(e)\rrbracket = \mathcal{[9D[K
\mathcal{T}^\mathcal{E}(\llbracket e \rrbracket),
     \]  
     where `\mathcal{T}^\mathcal{E}` is the induced functor on denotations.[12D[K
denotations. This guarantees that semantic behavior (probability distributi[10D[K
distributions) is preserved.

3. **Translation Lemmas**:
   - **Context Lemma**: If a term \(e\) has type \(\tau\) in STLC, then its[3D[K
its pointwise‑mapped translation retains this typing in SPC.
   - **Substitution Lemma**: Given types and substitutions, the translated [K
term respects substitution properties, ensuring correct handling of variabl[7D[K
variable bindings.

4. **Preservation Corollary**: If a source term reduces under β‑conversion [K
(\(e \to_\beta e'\)), its translation also reduces (`\mathcal{T}_\lambda(e)[24D[K
(`\mathcal{T}_\lambda(e) \to \mathcal{T}_\lambda(e')`) in SPC, confirming t[1D[K
that the translation is reduction‑preserving.

5. **End‑to‑End Worked Example**:
   - A source term using probabilistic choice (e.g., `choice(p, lam x:α.x a[1D[K
a, lam x:α.a x_0)`) translates to an equivalent structure in SPC where each[4D[K
each branch evaluates deterministically (`a` for both branches). The result[6D[K
resulting denotation is the Dirac mass at `a`, matching the operational out[3D[K
outcome.
   - A variant with distinct outcomes (`choice(p,\mathsf{Doom},\mathsf{Safe[37D[K
(`choice(p,\mathsf{Doom},\mathsf{Safe})`) yields a distribution \(p \cdot \[1D[K
\delta_{\mathsf{Doom}} + (1-p) \cdot \delta_{\mathsf{Safe}}\), demonstratin[12D[K
demonstrating how the translation captures probabilistic semantics.

6. **Aggregation via Merge and Choice**:
   - By merging independent hazard terms `R_i` using `Merge` and then foldi[5D[K
folding with logical disjunction (`FoldOr`), one obtains a term `T_n` whose[5D[K
whose denotation is precisely the aggregated probability \(1 - \prod_{i=1}^[12D[K
\prod_{i=1}^n (1-p_i)\). This mirrors the standard formula for the union of[2D[K
of independent Bernoulli trials.

Overall, the document establishes that probabilistic choice and aggregation[11D[K
aggregation can be consistently modeled in SPC using well‑defined translati[9D[K
translation rules, operational semantics, and denotational correspondences.
