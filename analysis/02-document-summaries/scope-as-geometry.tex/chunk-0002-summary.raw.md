**1. Primitive concepts introduced in this chunk**

- **Replay**: A deterministic “rewind” operation that walks through a speci[5D[K
specific historical path, allowing observers to verify or debug the state o[1D[K
of the system at any prior point.
- **Speculative branch**: A non‑authoritative extension of the history that[4D[K
that does not affect future decisions; it is kept visible for inspection bu[2D[K
but ignored in replayed histories.
- **Commit (speculative outcome)**: An explicit event such as “event: decis[5D[K
decision X adopted” that ties a speculative path to an irreversible action,[7D[K
action, preserving traceability.

**2. Mathematical claims / formal structures**

- Determinism of history‑first systems applies only to the *replay* of a gi[2D[K
given past trajectory; selecting which future branch to commit does **not**[7D[K
**not** violate deterministic replay.
- The system’s operational semantics can be modeled as an extension of type[4D[K
typed lambda calculus: `Sphere(α → β)` corresponds to introducing an irreve[6D[K
irreversible event (term application), and `Pop(β → γ)` allows deterministi[12D[K
deterministic reconstruction/replay of the preceding history.

**3. Mechanisms / processes**

1. **Replay mechanism** – Enables late‑joining participants to “rewind” ana[3D[K
analysis, verifying past states without altering the immutable record.
2. **Speculative branching mechanism** – Creates visible but non‑authoritat[14D[K
non‑authoritative histories; they remain for inspection yet are excluded fr[2D[K
from replayed outcomes, preserving causality.
3. **Commitment process** – When a speculative outcome is accepted (e.g., “[1D[K
“decision X adopted”), it becomes an explicit event, linking the branch to [K
an irreversible change.

**4. Connections to concepts in the running abstract**

- The idea that *meaning* or state changes are recorded as events aligns wi[2D[K
with Appendix A’s claim that semantics arise solely from events.
- Replay and speculative branches echo Appendix C’s description of “replay [K
enables late‑joining observers” and “speculative branches … remain visible [K
for inspection but ignored in replayed histories.”
- The emphasis on traceability mirrors the limitation noted in Appendix D: [K
Spherepop does not seek to optimize for all use cases nor claim to solve al[2D[K
alignment/governance, because preserving history is essential.

**5. Unresolved questions / contradictions**

- **Open question:** How do speculative branches evolve over time without c[1D[K
creating hidden mutations? The chunk asserts determinism of replay but offe[4D[K
offers no mechanism for resolving conflicts between multiple commits.
- **Potential contradiction:** If a later event re‑records an earlier decis[5D[K
decision, does this constitute a “hidden mutation” that violates the princi[6D[K
principle of traceability?
- Both issues remain unresolved; the fragment does not propose solutions or[2D[K
or acknowledge trade‑offs.

---

**Extracted quotations (as requested):**

1. *“Branching therefore does not undermine determinism.”* – [source: "Bran[5D[K
"Branching therefore does not undermine determinism."]

2. *“Determinism applies to replay of a given history, not to the selection[9D[K
selection of which history to commit.”* – [source: “Determinism applies to [K
replay of a given history, not to the selection of which history to commit.[7D[K
commit.”]

