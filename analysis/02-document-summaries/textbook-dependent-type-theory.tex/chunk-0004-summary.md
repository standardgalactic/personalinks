**Principal Structural Properties of the Historical Calculus**

1. **Well‑Formedness** – A history \(H\) is well formed when it satisfies:
   - *Typing*: every event obeys its typing rule,
   - *Acyclicity & Monotonicity*: each dependency points to an earlier even[4D[K
event,
   - *Replayability*: all derived facts can be replayed,
   - *Justification of Collapses*: any collapse is justified by replay equi[4D[K
equivalence,
   - *Compatibility of Melds*: meld operations preserve the type‑theoretic [K
structure,
   - *Cumulative Hierarchy for Universes*: universe assignments respect the[3D[K
the cumulative hierarchy.

2. **Historical Weakening** – If a history \(H\) proves \(t:A\), appending [K
an independent event does not alter this proof:
   \[
   (H;e)\vdash t:A.
   \]
   The additional information merely enlarges future construction space wit[3D[K
without breaking existing derivations.

3. **Historical Substitution** – Substitution remains valid and is enriched[8D[K
enriched with provenance:
   - If \(H\vdash a:A\) and \(H,x:A\vdash t:B\), then  
     \[
     H\vdash t[x:=a]:B[x:=a],
     \]
     where the construction history of the substituted term records the mer[3D[K
merged dependency graph of both original terms.

4. **Historical Preservation** – Type preservation is extended:
   - If \(H\vdash t:A\) and a reduction occurs (\((H,t)\to(H',u)\)), then  [K

     \[
     H'\vdash u:A.
     \]
   This ensures that evaluation does not change the type of a well‑typed ex[2D[K
expression while also tracking provenance.

5. **Historical Progress** – Every closed term has a deterministic progress[8D[K
progression:
   - Either it is a value, or there exists an event \(H',u\) such that  
     \[
     (\varepsilon,t)\to(H',u).
     \]
   The resulting configuration includes the newly generated history.

6. **Replay Determinism** – Replay of a history is unique:
   - If two replay sequences lead to different histories, they must be iden[4D[K
identical; otherwise, non‑deterministic choices would violate well‑formedne[13D[K
well‑formedness.
   This guarantees reproducibility in theorem verification.

7. **Historical Confluence** – Evaluation order does not affect observable [K
results:
   - For a term \(t\) with reductions \((H,t)\to(H_1,u_1)\) and \((H,t)\to([11D[K
\((H,t)\to(H_2,u_2)\), there exists an intermediate history \((H_3,v)\) suc[3D[K
such that both paths converge to the same final term.

8. **Historical Strong Normalization** – Every well‑typed proof term normal[6D[K
normalizes:
   - Any replay terminates in a historical normal form, ensuring no infinit[7D[K
infinite computation is hidden within the reconstruction process.

9. **Historical Canonicity** – Closed inhabitants of inductive types reduce[6D[K
reduce canonically:
   - For \(n:\mathsf{Nat}\), replay terminates with either \(\mathsf{Zero}\[16D[K
\(\mathsf{Zero}\) or \(\mathsf{Succ}(m)\), and the entire history consists [K
only of admissible constructor applications.

10. **Uniqueness of Universes** – The hierarchy remains predicative:
    - No replayable history constructs a universe satisfying \(\Type:\Type\[14D[K
\(\Type:\Type\); cyclic dependencies are forbidden, preserving logical cons[4D[K
consistency.

These properties collectively ensure that the historical calculus not only [K
retains the core guarantees of dependent type theory—such as preservation a[1D[K
and normalization—but also enriches each theorem with rigorous provenance i[1D[K
information. This strengthens verification frameworks by making every step [K
traceable and reproducible while maintaining the foundational soundness exp[3D[K
expected from a dependently typed proof kernel.
