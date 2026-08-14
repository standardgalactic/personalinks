**1. Definitions & Primitive Concepts Introduced**

- *Config*: “`(σ, option_space, history, collapse_log)` – complete system s[1D[K
state.”  
  *[source: "Config": `(σ, option_space, history, collapse_log)` - complete[8D[K
complete system state]*  

- *Sphere*: “Nested structure `(items, label)` where items are Atoms or Sph[3D[K
Spheres.”  
  *[source: "Sphere": Nested structure `(items, label)` where items are Ato[3D[K
Atoms or Spheres]*  

- **Atom**: “Primitive value, no internal structure.”  
  *[source: "Atom": Primitive value, no internal structure]*  

**2. Mathematical Claims & Formal Structures**

- *Primitives* {POP, REFUSE, BIND, COLLAPSE} are described as **CLOSED**, m[1D[K
meaning they cannot be decomposed into further components without loss of i[1D[K
information.  
  *[source: “The four operations {POP, REFUSE, BIND, COLLAPSE} – CLOSED, no[2D[K
no 5th primitive”]*  

- *Quotient*: Defined via equivalence classes from `COLLAPSE`, expressed as[2D[K
as `{members: FrozenSet[Atom]}`.  
  *[source: "Quotient": Equivalence class from COLLAPSE, `{members: FrozenS[7D[K
FrozenSet[Atom]}`]*  

- *Continuation relation* ⊑ is defined by “`σ₁, O₁) ⊑ (σ₂, O₂) ⇔ O₁ ⊇ O₂`” [K
(option reduction).  
  *[source: "Continuation": Relation `(σ₁, O₁) ⊑ (σ₂, O₂) ⇔ O₁ ⊇ O₂"`]*  

- *Non-authority*: Declared as `V(h) ↛ h` – observers cannot modify or auth[4D[K
authorize continuations.  
  *[source: “Non-authority”: `V(h) ↛ h` - observers can't modify or authori[7D[K
authorize]*  

**3. Mechanisms & Processes**

- **Experiment Workflow**: The *Research Program* outlines using the comman[6D[K
command `python -m spherepop.lab` for structured verification (`verify`) an[2D[K
and comparison (`compare`).  
  *[source: “Research Program”: Manifest‑driven laboratory workflow, `verif[6D[K
`verify`/`compare`]*  

- **Design Decision Rationale**: Eleven Design Decision Records (DDR) captu[5D[K
capture context, decision, rationale, alternatives, and consequences. They [K
track status as Accepted / Provisional / Superseded.  
  *[source: “DESIGN_DECISIONS.md”: 11 DDRs with context, decision, rational[8D[K
rationale, alternatives, consequences]*  

- **Authority Hierarchy**: Document authority follows the chain *“The Histo[5D[K
History of Spherepop (paper) → THEORY_STATUS.md (interpretations) → SPECIFI[7D[K
SPECIFICATIONS.md (normative definitions) → Implementation (spherepop/*.py)[16D[K
(spherepop/*.py)”*.  
  *[source: “Document Authority Hierarchy” diagram]*  

**4. Connections to Concepts Named in Running Abstract**

- **README.md**, **CONTRIBUTING.md**, **DEVELOPMENT.md**, and **TESTING.md*[13D[K
**TESTING.md** align with the “For Users”, “For Contributors”, “For Theoris[7D[K
Theorists”, and “For Researchers” sections, respectively, mirroring the run[3D[K
running abstract’s emphasis on usage guides, development workflow, theory s[1D[K
status, and experimental catalogues.  
  *[source: Running abstract description of user/contributor/theoretical do[2D[K
documentation roles]*  

- **THEORY_STATUS.md** serves as the authoritative reference for questions [K
Q1‑Q8, directly linking to unresolved research topics identified in “FUTURE[7D[K
“FUTURE_DIRECTIONS.md”.  
  *[source: “THEORY_STATUS.md” – THE AUTHORITY for paper vs implementation][15D[K
implementation]*  

- **SPECIFICATIONS.md** provides normative definitions of the core primitiv[8D[K
primitives {POP, REFUSE, BIND, COLLAPSE}, matching the running abstract’s n[1D[K
note on precise API and functional contracts.  
  *[source: “SPECIFICATIONS.md” – Normative reference to precise definition[10D[K
definitions of primitives]*  

**5. Unresolved Questions or Contradictions Visible**

- **Open Questions (Status ?)**: Several questions remain unresolved, such [K
as “Research directions (Plan B, COLLAPSE composition, history compaction)”[12D[K
compaction)” and “Infrastructure extensions (LLM integration, CLI, optimiza[8D[K
optimization)”.  
  *[source: “FUTURE_DIRECTIONS.md” – Unresolved continuations]*  

- **Potential Contradictions**: No contradictions are explicitly flagged in[2D[K
in this chunk; however, the note on *Non‑authority* suggests a limitation w[1D[K
where observers cannot enforce continuation logic, implying a design trade‑[6D[K
trade‑off between expressiveness and safety.  
  *[source: “Non-authority”: `V(h) ↛ h` - observers can't modify or authori[7D[K
authorize]*  

These points collectively map out the conceptual landscape of Spherepop as [K
presented in this documentation index.

