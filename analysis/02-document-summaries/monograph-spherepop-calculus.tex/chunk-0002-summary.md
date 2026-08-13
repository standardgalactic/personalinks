**Summary**

The document outlines a compositional translation from a probabilistic λ‑ca[4D[K
λ‑calculus (with internal choice) to a static‑probabilistic calculus (SPC).[6D[K
(SPC). Key points include:

1. **Typing Preservation** – The pointwise‑mapped translations preserve typ[3D[K
typing derivations in the target language SPC.

2. **Operational Equivalence** – One‑step reductions in source terms map di[2D[K
directly to corresponding steps or equalities modulo Merge congruence, pres[4D[K
preserving the probabilities of choice events.

3. **Adequacy (Denotational)** – For monadic formulations, denotations comm[4D[K
commute with translation:
   \[
   \llbracket \mathcal{T}_{\mathrm{prob}\lambda}(e) \rrbracket = 
   \mathcal{T}^\mathcal{E}(\llbracket e \rrbracket),
   \]
   where \(\mathcal{T}^\mathcal{E}\) is the induced functor on denotations.[12D[K
denotations.

4. **Compositional Translation** – The translation maps:
   - Variables unchanged,
   - Abstractions to a *Sphere* construction (encapsulating arguments in SP[2D[K
SPC),
   - Applications using *Pop* to destructure and apply.

5. **Worked Example**  
   - **Source Term**: `choice(p, (λx→α.x)a, (λx→α.a)x₀)` typed with base ty[2D[K
type α.
   - **Translated Form**: `\mathrm{Choice}(p,\ \mathrm{Pop}(\mathrm{Sphere}[28D[K
\mathrm{Pop}(\mathrm{Sphere}(x{:}\alpha.\,x),\ a),\ \mathrm{Pop}(\mathrm{Sp[23D[K
\mathrm{Pop}(\mathrm{Sphere}(x{:}\alpha.\,a),\ x₀))`.
   - **Operational Trace**: Branches collapse to the constant `a`, yielding[8D[K
yielding a final value of type α.
   - **Denotational Result (Option B)**:  
     \[
     \llbracket \mathrm{Choice}(p,t,u) \rrbracket = p\cdot\delta_{\llbracke[23D[K
p\cdot\delta_{\llbracket t\rbracket} + (1-p)\cdot\delta_{\llbracket u\rbrac[7D[K
u\rbracket},
     \]
     which reduces to a Dirac mass at `a` because both branches denote the [K
same object.

6. **Variant with Distinct Outcomes** – For outcomes `{Safe, Doom}`:
   - Translated term remains `\mathrm{Choice}(p,\mathsf{Doom},\mathsf{Safe}[46D[K
`\mathrm{Choice}(p,\mathsf{Doom},\mathsf{Safe})`.
   - Probability of doom after \(n\) independent hazards is  
     \[
     1-\prod_{i=1}^{n}(1-p_i),
     \]
     matching the pushforward of a product distribution through Boolean dis[3D[K
disjunction.

7. **Aggregation via Merge and Choice** – For independent hazards \(R_i\), [K
merging them into `T_n = \mathrm{FoldOr}(\mathrm{Merge}(R_1,\dots,R_n))` yi[2D[K
yields the probability above, confirming that denotational semantics align [K
with operational expectations under independence (Independent‑Channels Lemm[4D[K
Lemma).

Overall, the translation is sound and fully compositional, preserving both [K
typing and probabilistic behavior across reductions.

