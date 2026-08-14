**Definitions**

1. **Authority (S)** – The authority is defined as an *append‑only merge of[2D[K
of events*.  
   - *Append‑only* means that each event can be added in sequence without a[1D[K
alteration; no earlier state may be overwritten.  
   - The merge operation concatenates the ordered list of events into a sin[3D[K
single cumulative view.

2. **View (R)** – The view is obtained by *collapsing* the authority throug[6D[K
through replay.  
   - “Collapse” refers to resolving the accumulated commitments expressed i[1D[K
in the event log into a concrete state representation that can be inspected[9D[K
inspected or used for further computation.  

3. **Mutation** – In this context, mutation denotes an *in‑place update* of[2D[K
of data that does not retain the historical trail of previous states (i.e.,[6D[K
(i.e., it erases provenance).  

4. **State Monad \(S \to (A \times S)\)** – The state monad encapsulates a [K
region where computation can read and write a state channel.  
   - *\(A\)* is the value produced by the operation, while *\(*S*\)* carrie[6D[K
carries the updated authority/state forward to subsequent operations.

5. **Continuation‑Passing Style (CPS) \((A \to R) \to R\)** – In CPS the “r[2D[K
“rest of pipeline” is made explicit; control flow proceeds via continuation[12D[K
continuation functions rather than implicit returns, thereby controlling wh[2D[K
where collapse may occur.

**Equations**

- **Authority Definition**:  
  \[
  \text{authority} = \text{append‑only merge of events}
  \]
  This can be formalized as a monotone function \(M : \mathcal{E}^* \to S\)[3D[K
S\) (where \(\mathcal{E}\) is the set of events), satisfying:  
  - **Monotonicity**: If \(e_1, e_2 \in \mathcal{E}\) and order preserves ([1D[K
(\(e_1 < e_2\)), then \(M([e_1,e_2]) = M([e_1]) \cdot M([e_2])\) (i.e., eve[3D[K
events are concatenated in order).  
  - **Idempotence**: Adding an already‑present event does not change the re[2D[K
result, ensuring no overwrite.

- **View Definition**:  
  \[
  \text{view} = \operatorname{collapse}(\text{authority})
  \]
  Collapse is typically a projection function \(C : S \to R\) that selects [K
a representative state from the accumulated authority while preserving nece[4D[K
necessary structural invariants (e.g., functional dependencies).

**Distinctions**

- **Mutation vs. Structured Accumulation**:  
  - *Mutation* changes the underlying data directly, discarding historical [K
information (no trace of prior states).  
  - *Structured accumulation* via the event log preserves provenance; colla[5D[K
collapse merely re‑interprets a sequence as a concrete state without losing[6D[K
losing the ordering.

- **Commitment vs. Collapse**:  
  - *Commitment* is the act of recording an update in the authority (append[7D[K
(append‑only).  
  - *Collapse* resolves these commitments canonically, yielding a usable re[2D[K
representation that may hide some historical details but guarantees consist[7D[K
consistency and recoverability.

**Mechanisms**

1. **Merge Mechanism** – Sequential concatenation of events into a single a[1D[K
authoritative state channel. This is the core operation that ensures eventu[6D[K
eventual consistency across all participants (e.g., in distributed systems [K
or version control).

2. **Collapse Mechanism** – A deterministic reduction step applied to the m[1D[K
merged authority, producing a concrete view \(R\). Collapse respects equiva[6D[K
equivalence relations (often based on functional dependency) so that differ[6D[K
different event sequences yielding identical state are collapsed into a sin[3D[K
single representation.

3. **Control of Collapse** – The discipline is enforced by separating where[5D[K
where collapse occurs:  
   - *When*: After the entire authoritative log has been accumulated, befor[5D[K
before any further mutation can occur without affecting historical traceabi[8D[K
traceability.  
   - *How*: By using monadic or CPS style abstractions that explicitly pass[4D[K
pass the current authority/state as an argument rather than relying on impl[4D[K
implicit return values.

**Arguments**

- The text argues that **state monads and event sourcing are not merely sty[3D[K
stylistic choices**, but structural disciplines required to prevent “collap[7D[K
“collapse from erasing provenance.”  
  - If collapse were allowed before proper abstraction, historical informat[8D[K
information would be lost, violating the invariant that *commitment must re[2D[K
remain replayable*.

- By treating authority as a persistent record (append‑only), subsequent co[2D[K
collapse operations become safe because any future mutation will start from[4D[K
from an immutable base rather than overwriting past states.

**Conjectures**

1. **Compositional Core**: The fragment suggests that all familiar formalis[8D[K
formalisms (λ‑calculus, type theory, monads, CPS) can be seen as particular[10D[K
particular instances of the same structural discipline—*accumulate then col[3D[K
collapse*—when viewed through the lens of Spherepop’s primitive operations.[11D[K
operations.

2. **Universality of the Discipline**: If every computational paradigm ulti[4D[K
ultimately reduces to this invariant pattern, then any formal system can be[2D[K
be interpreted within a unified framework that emphasizes *commitment accum[5D[K
accumulation* and *controlled resolution* rather than syntactic manipulatio[11D[K
manipulation alone.

**Dependencies**

- The authority‑view separation depends on an **append‑only event log**, wh[2D[K
which in turn relies on the ability to order events causally (e.g., timesta[7D[K
timestamps or sequence numbers).  
- Collapse’s deterministic nature presupposes a well‑defined equivalence re[2D[K
relation on states that respects functional dependencies and data integrity[9D[K
integrity constraints.

**Unresolved Questions**

1. *What is the minimal set of axioms required for a consistent merge opera[5D[K
operation in arbitrary computational contexts?* – The fragment does not spe[3D[K
specify formal proof obligations; it merely hints at associativity and idem[4D[K
idempotence, leaving open questions about non‑trivial domains (e.g., concur[6D[K
concurrent systems).

2. *How can mutation be reconciled with the requirement that provenance mus[3D[K
must remain replayable without introducing excessive overhead?* – The text [K
suggests a design principle but does not detail concrete mechanisms for sel[3D[K
selective mutable regions or shadowing techniques.

3. *Is there a principled way to extend this discipline into dependent type[4D[K
type theory or cost semantics while preserving its core invariant?* – This [K
remains an open research area; the fragment serves as a conceptual stepping[8D[K
stepping stone rather than a full formalization.

---

**Summary of Core Ideas**

- **Authority** = append‑only merge → preserves order and history.  
- **View** = collapse by replay → resolves to concrete state while discardi[8D[K
discarding unnecessary historical details.  
- The discipline ensures *commitment accumulation* (merge) followed by *con[4D[K
*controlled collapse* (view), avoiding the loss of provenance that mutation[8D[K
mutation alone can cause.

These concepts underpin the broader argument in Spherepop that computationa[12D[K
computational models are fundamentally about how and when commitments are s[1D[K
stored versus resolved, rather than merely about syntactic transformations.

