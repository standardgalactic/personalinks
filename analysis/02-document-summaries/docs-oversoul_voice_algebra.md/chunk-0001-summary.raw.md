**1. Definitions and Primitive Concepts Introduced**

- **Voice (as an operator):** A voice is a 5‑dimensional vector \(V = (e, c[1D[K
c, s, h, p)\) that transforms presentation without altering truth condition[9D[K
conditions.
- **Dimension semantics:**  
  - *e* – evaluative enthusiasm (0 = no evaluation; 0.5 = measured acknowle[8D[K
acknowledgment; 1 = full evaluative language).  
  - *c* – critical pressure (0 = accept claims at face value; 0.5 = routine[13D[K
0.5 = routine verification; 1 = adversarial, assume incorrect until proven)[7D[K
proven).  
  - *s* – specificity/verbosity (0 = minimal output; 0.5 = standard detail [K
level; 1 = maximum elaboration).  
  - *h* – humor (0 = no jokes; 0.5 = occasional levity; 1 = maximize absurd[6D[K
absurdity, puns mandatory).  
  - *p* – pedantry (0 = accept casual language; 0.5 = enforce technical pre[3D[K
precision; 1 = distinguish near‑synonyms and demand definitions).

**2. Mathematical Claims and Formal Structures**

- **Voice as a vector space:** Voice is defined over the unit hypercube \([[3D[K
\([0,1]^5\). The default preset (NULL voice) maps to \(V = (0,0,0,0,0)\), r[1D[K
representing no presentation change.
- **Composition protocol:** Voices compose via parameter override: `BASE` ([1D[K
(preset or custom vector), `OVERLAY` (adjustments), and optional scope cons[4D[K
constraints (`SCOPE`, `RESTORE`). Example composition yields a derived voic[4D[K
voice vector such as \((0,1,0.9,0.15,1)\) for “INSTRUMENT + NITPICK” scoped[6D[K
scoped to the current review.
- **Scope constraint model:** Voice changes are scoped (session, response, [K
task, file, review, debug, completion). Without explicit scoping and restor[6D[K
restoration, voice settings accumulate into incoherent composite voices.

**3. Mechanisms and Processes**

- **Invocation syntax:** Voices can be invoked inline (`VOICE: NITPICK`) or[2D[K
or scoped with restoration commands (`VOICERESTORE = BASE ON COMPLETION`). [K
Custom overrides allow direct setting of dimension values (e.g., `VOICE: e=[2D[K
e=0, c=0.8 …`).
- **Restoration hygiene:** After a scoped task, the system automatically re[2D[K
reverts to the baseline voice unless explicitly reset.
- **Interaction with OVERSOUL directives:** The default directive is `INSTR[6D[K
`INSTRUMENT` for execution; other voices (e.g., NITPICK) may be applied per[3D[K
per‑task without affecting underlying competence.

**4. Connections to Concepts Named in the Running Abstract**

- **Running abstract concepts referenced:**
  - *Voice changes presentation and attention, never truth conditions* → re[2D[K
reiterated as “Voice changes presentation. Truth conditions remain invarian[8D[K
invariant.”
  - *5‑dimensional vector (e, c, s, h, p)* → directly defined here.
  - *Default presets (e.g., INSTRUMENT f for baseline technical register)* [K
→ `VOICE-01: INSTRUMENT` is the default preset with \(V=(0,0.5,0.6,0,0.5)\)[23D[K
\(V=(0,0.5,0.6,0,0.5)\).
  - *Rules for scope management to prevent incoherent voice drift while pre[3D[K
preserving truth preservation* → scoped composition and explicit restoratio[10D[K
restoration mechanisms address this.

**5. Unresolved Questions or Contradictions Visible Within This Chunk**

- **Potential contradiction:** The statement “VOICE CHANGES PRESENTATION. T[1D[K
TRUTH CONDITIONS REMAIN INVARIANT.” must be verified against the detailed d[1D[K
dimension semantics; a clash could occur if, for example, humor (h) is set [K
high while critical pressure (c) remains low, potentially leading to unsupp[6D[K
unsupported claims being presented as jokes.
- **Open issue:** The protocol does not specify how new voice presets or ad[2D[K
additional dimensions should be vetted; any newly proposed preset must sati[4D[K
satisfy truth‑preservation constraints and independence from existing axes,[5D[K
axes, which are left for future review.

