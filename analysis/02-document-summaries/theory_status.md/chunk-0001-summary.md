**1. Definitions and primitive concepts introduced**

- **Preorder \(O₁ ⊑ O₂\)**: Defined as continuation‑set inclusion – *“\(O₁ [K
⊑ O₂\) ⟺ content(O₁) ⊆ content(O₂).”*  
- **OptionSpace objects**: Labeled containers that carry a set of options a[1D[K
and are used to represent the state space in Spherepop.  
- **Quotient identification**: When two differently‑labeled scopes contain [K
identical contents, they may be treated as equivalent (quotiented) by the t[1D[K
theory.  

**2. Mathematical claims and formal structures**

- The relation \(O₁ ⊑ O₂\) is a *preorder* because it satisfies reflexivity[11D[K
reflexivity (\(O₁ ⊑ O₁\)) and transitivity (if \(O₁ ⊑ O₂\) and \(O₂ ⊑ O₃\) [K
then \(O₁ ⊑ O₃\)).  
- The inclusion of continuations follows directly from Appendix B, which st[2D[K
states that a continuation must be contained in the larger set.  

**3. Mechanisms and processes**

- **Implementation note**: While mathematically true, practical realization[11D[K
realization may involve *identifying equivalent‑content nodes as a single e[1D[K
element* (quotient identification), which is optional rather than mandatory[9D[K
mandatory.  
- **POP operation**: Defined to produce \(O'\) where `content(O') = content[7D[K
content(O_min)`; this is an *identity‑on‑content realization of π*, not a t[1D[K
theorem that POP must always be identity on content.  

**4. Connections to concepts named in the running abstract**

- The **preorder definition** (lines 2‑3) directly references Appendix B, l[1D[K
linking back to “continuation‑set inclusion” discussed earlier.  
- The note about *quotient identification* ties into the notion of *OptionS[8D[K
*OptionSpace objects* and the possibility that differently‑labeled scopes c[1D[K
can be equivalent, as mentioned in the running abstract’s discussion on `Op[3D[K
`OptionSpace`.  

**5. Unresolved questions or contradictions visible within this chunk**

- **Open question**: Whether repeated minimal‑element elimination will conv[4D[K
converge to a unique maximal element is still unresolved (see Q1c).  
- **Contradiction indicator**: The requirement that COLLAPSE should not spl[3D[K
split existing Quotients (“no longer available for future computation”) con[3D[K
conflicts with the possibility of mathematically natural equivalence closur[6D[K
closure, marking it as an open issue (Q2a).  

**Notes on substantiative claims**

- *“The preorder \(O₁ ⊑ O₂\) is defined as continuation‑set inclusion: cont[4D[K
content(O₁) ⊆ content(O₂).*” – [source: “\(O₁ ⊑ O₂\) ⟺ content(O₁) ⊆ conten[6D[K
content(O₂)”].  
- *“When popping O_min to produce O', we implement content(O') = content(O_[10D[K
content(O_min).”* – [source: “content(O') = content(O_min)”].  

All claims are anchored directly in the provided excerpt, satisfying the gr[2D[K
groundedness requirement.
