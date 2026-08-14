**Experiment Catalog – Overview**

| # | Experiment ID | Class | Layer | Theory Status* | Purpose / Question |[1D[K
|
|---|----------------|-------|-------|----------------|-------------------||---|----------------|-------|-------|----------------|--------------------|
| 01 | `01` | **S** | 0 | Paper‑licensed (normative) | Defines the primitiv[8D[K
primitive *Sphere* and its construction rules. |
| 02 | `02` | **S** | 0 | Paper‑licensed | Describes how to compose *Operat[7D[K
*Operations* from primitives. |
| 03 | `03` | **S** | 0 | Paper‑licensed | Specifies immutable property *is[3D[K
*isMember* for members of a Sphere. |
| 04 | `04` | **S** | 0 | Paper‑licensed | Introduces the notion of *Histor[7D[K
*History* as a trace of applied Operations. |
| 05 | `05` | **S** | 0 | Paper‑licensed | States that each Operation is a [K
deterministic function on History. |
| 06 | `06` | **S** | 0 | Paper‑licensed | Provides the canonical ordering [K
for *Observables* (labels, counts). |
| 07 | `07` | **S** | 1 | Paper‑licensed | Tests that an *Observer* correct[7D[K
correctly reports current values of Observables. |
| 08 | `08` | **S** | 1 | Paper‑licensed | Verifies Observer non‑authority:[14D[K
non‑authority: observers cannot infer hidden state or recompute histories. [K
|
| 09 | `09` | **S** | 1 | Paper‑licensed | Checks that the same *Observer* [K
yields identical reports across concurrent runs. |
| 10 | `10` | **S** | 1 | Paper‑licensed (experimental) | Validates that Ob[2D[K
Observer equality does not imply History identity. |
| 11 | `11` | **S** | 1 | Paper‑licensed (experimental) | Ensures *represen[9D[K
*representative()* returns an arbitrary member but always a valid view. |
| 12 | `12` | **S** | 0 | Paper‑licensed literal implementation | Full gram[4D[K
grammar for primitive expressions; round‑trip parsing verified. |
| 13 | `13` | **Q** | 3 | Paper‑licensed core principle (FUTURE_DIRECTIONS)[19D[K
(FUTURE_DIRECTIONS) | Explores multi‑timescale continuation policies and th[2D[K
their stability guarantees. |
| 14 | `14-labels` | **S** | 0 | Paper‑licensed | Defines label semantics f[1D[K
for Observables; ensures consistent labeling across layers. |
| 14 | `14-check` | **S** | 2 | Research question (→) | Verifies that the O[1D[K
Observer non‑authority principle holds under various policy families. |
| 15 | `15` | **Q** | 2 | Research question (expensive) | Tests horizon‑equ[11D[K
horizon‑equivalence for k = 1,2,… up to a configurable limit; checks O(|ops[6D[K
O(|ops|^k). |
| 16 | `16` | **Q** | 2 | Research question (highly experimental) | Investi[7D[K
Investigates whether certain policy families are *confluent* under all poss[4D[K
possible histories. |
| 17 | `17` | **S** | 1 | Paper‑licensed | Confirms that REFUSE followed by[2D[K
by BIND yields the same effect as BIND then REFUSE for disjoint options onl[3D[K
only. |
| 18 | `18` | **S** | 1 | Implementation choice (Q7) | Validates *equivalen[10D[K
*equivalent_at* with prefix matching: first k operations must match regardl[7D[K
regardless of later differences. |
| 19 | `19` | **S** | 1 | Paper‑licensed core principle | Demonstrates that[4D[K
that Quotient({a,b}) == Quotient({b,a}); representative is arbitrary for id[2D[K
identity testing only. |
| 20 | `20-intensional-extensional-equivalence` | **S** | 3 | Paper‑license[13D[K
Paper‑licensed core principle (Q5) | Shows two distinct histories can have [K
identical extensional views but different internal states. |
| 21 | `21-refuse-bind-commute` | **S** | 2 | Research question (→) | Deter[5D[K
Determines when REFUSE and BIND commute; tests overlapping option sets wher[4D[K
where they diverge. |
| 22 | `22-confluence-policy-family` | **Q** | 2 | Research question | Clas[4D[K
Classifies policy families that guarantee confluence; reports empirical inv[3D[K
invariants for future theory work. |
| 23 | `23-regret-accumulation` | **X** | 2 | Dependent on Q6 (research) | [K
Measures regret accumulation over sequences; tests “recovery” of lost oppor[5D[K
opportunities experimentally. |
| 24 | `24-replay-invariance-reordering` | **S** | 3 | Paper‑licensed deter[5D[K
deterministic principle | Verifies that replaying a history yields exactly [K
the original configuration, irrespective of permutation order. |
| 25 | `25-observer-non-authority` | **S** | 3 | Paper‑licensed core princi[6D[K
principle (OVERSOUL §4) | Confirms Observer non‑authority: observers cannot[6D[K
cannot modify configs nor be used as authority for config identity. |
| 26 | `26-horizon-equivalence` | **Q** | 2 | Research question (expensive)[11D[K
(expensive) | Computes k‑step horizon equivalence; tests O(|ops|^k) complex[7D[K
complexity and correctness of reachable sets. |

\* **Theory Status**  
- **Paper‑licensed**: Normative, derived directly from the formal specifica[9D[K
specification and approved for inclusion in the official spec.  
- **→ (Provisional)**: Requires additional theoretical work or community co[2D[K
consensus before full licensing.  
- **Research / Experimental**: Intended only as exploratory; results are no[2D[K
not considered final specifications.

---

### How to Add a New Experiment

1. **Classify**  
   - Determine whether it is *S* (specification), *X* (experimental researc[7D[K
research), *Q* (question requiring further theory), or *I* (implementation [K
detail).  

2. **Document Purpose**  
   - Write a single‑sentence statement of the question you are trying to an[2D[K
answer.  

3. **Check Theory Status**  
   - If it is novel, mark as **Research**; if it will be part of the formal[6D[K
formal spec once resolved, mark **→ (Provisional)**.  

4. **Update Catalog Entry**  
   - Add a new row following the template shown above and ensure the *Purpo[6D[K
*Purpose* column reflects the question.  

5. **Cross‑Reference**  
   - Link to relevant sections in `THEORY_STATUS.md` for provisional experi[6D[K
experiments, or to existing spec items for licensed ones.  

6. **Add Tests (if applicable)**  
   - For each new experiment, write corresponding regression tests and plac[4D[K
place them under appropriate test modules (`test_properties.py`, `test_regr[10D[K
`test_regressions.py`, etc.).  

---

### Maintaining the Catalog

- **Re‑run when specifications change** – any update to a licensed experime[8D[K
experiment requires updating its *Purpose* and possibly moving it out of Re[2D[K
Research.  
- **Do not re‑run for research outcomes** – experimental results should be [K
documented in separate `README.md` files, not as formal success criteria.  [K


---

### Cross‑References

| Reference | Purpose |
|-----------|---------|
| `SPECIFICATIONS.md` | Holds the authoritative normative definitions (S ex[2D[K
experiments). |
| `THEORY_STATUS.md` | Tracks which questions are still open or require fur[3D[K
further proof (Q/X experiments). |
| `CONTRIBUTING.md` | Guidelines for proposing new experiments and ensuring[8D[K
ensuring proper classification. |
| `test_regressions.py` | Contains extracted regression tests derived from [K
S‑experiments; used for CI validation. |

---

**Last Updated:** 2026‑08‑13 – this catalog reflects the current set of exp[3D[K
experiments as defined in the OVERSOUL documentation hierarchy.

