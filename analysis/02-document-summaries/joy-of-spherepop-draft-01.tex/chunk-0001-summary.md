**Refusal as a Normative Marker – Not an Authority‑Breaching Operator**

In the abstract event‑history calculus of Spherepop, refusal behaves geomet[6D[K
geometrically like pop because both reduce the space of admissible futures [K
by removing one particular branch at a fixed time point. This is reflected [K
in their equivalent transformation on option‑spaces:

\[
\llbracket \operatorname{refuse}_t \rrbracket
=
\llbracket \operatorname{pop}_t \rrbracket \quad\text{in }\mathcal{O},
\]

so the *mechanics* of history are unchanged. What does change is **why** we[2D[K
we invoke refusal.

### 1. Refusal Lives in the Accounting Layer

Spherepop deliberately isolates normative distinctions (ethical, contractua[10D[K
contractual, or moral reasons) from the kernel’s authoritative state:

- **Kernel layer**: implements a deterministic interpreter over an append‑o[8D[K
append‑only event log; only *causation* matters here.
- **Accounting/View layer**: records supplementary metadata about why event[5D[K
events were chosen. Refusal is recorded there as a “normative tag” attached[8D[K
attached to the offending branch, not as a kernel transition.

Thus refusal never alters the kernel’s state directly; it merely registers [K
an additional attribute that can later be consulted when deciding whether t[1D[K
to enforce the same restriction on new observers (or in replay).

### 2. Non‑Interference Guarantees

Because refusal is recorded outside the kernel, any observer—new or existin[7D[K
existing—can consult this auxiliary history without affecting the determini[9D[K
deterministic execution path already committed:

1. **Early‑joining agents** can see that a branch was refused by checking t[1D[K
the accounting log (e.g., “branch X at timestamp Y was marked ‘refused’ for[3D[K
for ethical violation”), but they cannot retroactively change the kernel st[2D[K
state.
2. **Later observers** may replay the system and encounter the same refusal[7D[K
refusal; the kernel will simply skip that branch, preserving causal consist[7D[K
consistency.

This separation prevents *authority contamination*: normative reasons do no[2D[K
not become irreversible updates to history; they remain as interpretive not[3D[K
notes.

### 3. Preventing “Misuse” of Refusal

If refusal were allowed inside the kernel (i.e., it treated options like po[2D[K
pop does), a malicious or buggy implementation could:

- **Coerce future states** by refusing undesirable outcomes without any ext[3D[K
external audit.
- **Create hidden back‑doors**: an operator could refuse only branches that[4D[K
that later become inconvenient, making history appear consistent while pres[4D[K
preserving undisclosed preferences.

By keeping refusal purely *accounting*—a non‑authoritative annotation—we gu[2D[K
guarantee:

- **Transparency**: anyone can verify why a branch was refused from the eve[3D[K
event log and auxiliary metadata.
- **Replayability**: deterministic replay remains possible because the kern[4D[K
kernel never “rewrites” history; it only chooses to ignore the tagged branc[5D[K
branch.

### 4. Interaction with Collapse

Both collapse and refusal are *quotienting* operations on option‑spaces, bu[2D[K
but their scopes differ:

| Operation | Scope of Effect | Authority |
|-----------|-----------------|-----------|
| **Pop**   | Single future branch at a point in time | Kernel (authoritati[12D[K
(authoritative) |
| **Refuse**| Same geometric effect as pop, *but with an ethical tag* | Acc[3D[K
Accounting layer (non‑authoritative) |
| **Collapse**| Equivocates entire regions of the log based on policy | Ker[3D[K
Kernel (authoritative) |

Because refusal is recorded separately, it can be **reconciled** with colla[5D[K
collapse policies later. If a new policy decides that previously refused br[2D[K
branches should also be collapsed, this decision is made by updating the ke[2D[K
kernel’s transition rules—not by rewriting history.

### 5. Implementation Detail – Tagging Mechanism

In practice, each event carries a small “metadata” field (e.g., `refusalRea[11D[K
`refusalReason = "ethicalViolation"`). When an option is refused:

1. The kernel emits a **RefusalLog** event that points to the offending bra[3D[K
branch ID and stores the reason.
2. No transition rule changes; future observers simply ignore branches tagg[4D[K
tagged as refused.

This design satisfies Spherepop’s principle of *non‑interference*: normativ[8D[K
normative distinctions do not corrupt causal integrity, and they remain mut[3D[K
mutable without breaking determinism.

---

**Bottom Line:** Refusal is treated in Spherepop precisely because it must [K
be recorded externally (in the accounting layer) rather than directly appli[5D[K
applied to kernel state. This placement enforces non‑interference: ethical [K
or contractual reasons stay out of authority’s domain, preserving determini[9D[K
deterministic replayability while allowing transparent auditing and later p[1D[K
policy adjustments.

