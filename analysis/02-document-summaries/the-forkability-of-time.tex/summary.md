**Summary**

Spherepop’s design is built on a handful of mathematical principles that to[2D[K
together guarantee *causal sovereignty*:

| Principle | What it guarantees |
|-----------|--------------------|
| **Deterministic `eval`** | The world‑state function `eval(H)` is pure: fo[2D[K
for any two correct implementations the result on a given history does not [K
change. This makes semantic state invariant under migration across differen[8D[K
different code bases. |
| **Replay equivalence** | Two histories are replay‑equivalent only when th[2D[K
they are identical (`H = H'`). Because canonical encoding forces each histo[5D[K
history to be uniquely represented, there is no “interpretive margin” where[5D[K
where two distinct histories could define the same world. |
| **World identity across arbiters** | If Arbiter A exports history `H_A` a[1D[K
and Arbiter B accepts history `H_B`, then `H_A = H_B`. No translation, norm[4D[K
normalization, or reinterpretation is allowed; causal continuity is defined[7D[K
defined strictly by syntactic equality of histories. |
| **Migration as an isomorphism** | Migration between arbiters is modeled a[1D[K
as a morphism in the category **Hist**, where objects are histories and arr[3D[K
arrows are prefix extensions. An exit operation leaves the history unchange[8D[K
unchanged (`id_H`) but swaps the sequencing authority, showing that migrati[7D[K
migration only changes governance, not ontology. |
| **Fork semantics & geometry of time** | The set of all finite histories `[1D[K
`𝓗` with the prefix order forms a rooted tree. A *fork* occurs at a node `H[2D[K
`H` when two distinct extensions exist (`H·e` and `H·e'` with `e≠e'`). Fork[4D[K
Forking is not inconsistency; it reflects causal divergence (different futu[4D[K
futures from the same past). |
| **Arbiter authority as path selection** | An arbiter does not create the [K
tree but selects a path through it. The selector function `S : 𝓗 → 𝓗` picks[5D[K
picks one successor of each history, satisfying `H ⊂ S(H)`. Authority is th[2D[K
thus “choosing a branch,” not defining all possibilities. |
| **Forkability of time** | Time remains forkable as long as no arbiter can[3D[K
can permanently collapse the tree into an irreversible trunk. Any history a[1D[K
and any of its successors may become authoritative under another arbiter, p[1D[K
preserving the public manifold nature of causality. |
| **Exit as path rebinding** | When a world changes governance (e.g., exiti[5D[K
exiting to Arbiter B), the underlying historical path stays fixed; only the[3D[K
the selector function is replaced (`S_A` → `S_B`). This preserves the geome[5D[K
geometry of time while altering political control. |

### Why These Principles Matter

1. **Elimination of Covert Sovereignty**  
   By tying world identity strictly to history equality, Spherepop prevents[8D[K
prevents any institution from redefining past events merely by preserving c[1D[K
current surface state. Institutions may *witness* reality but cannot rewrit[6D[K
rewrite it.

2. **Public vs. Private Time**  
   Traditional platforms treat time as a private line owned by an arbiter ([1D[K
(e.g., TikTok’s recommendation engine). In Spherepop, time is a public bran[4D[K
branching manifold where every agent can traverse the same historical tree,[5D[K
tree, making causality a commons rather than a proprietary artifact.

3. **Topological Nature of Causality**  
   Forkability is not metaphorical; it is an actual geometric property of c[1D[K
causal space. The prefix‑order tree captures divergent futures without coll[4D[K
collapsing them into a single linear timeline.

### Implications for Design

- **No “Versioning” Hacks**: Because replay equivalence reduces to syntacti[8D[K
syntactic equality, there is no room for hidden version mismatches that cou[3D[K
could be exploited.
- **Transparent Migration**: Migration protocols must preserve the exact hi[2D[K
historical prefix; any deviation (e.g., selective pruning or canonicalizati[14D[K
canonicalization) would violate world‑identity across arbiters.
- **Governance Changes Do Not Alter Ontology**: Exits only change who gets [K
to select successors, leaving the underlying history untouched—ensuring tha[3D[K
that “replaying” a state always yields the same semantic result.

In essence, Spherepop’s formalism turns time into a *public geometry* where[5D[K
where every participant can walk the same branches of past events, guarante[8D[K
guaranteeing that no single entity can rewrite reality without breaking cau[3D[K
causal sovereignty. This is both a logical necessity and a practical design[6D[K
design goal for systems built on immutable history.

