# Spherepop Documentation Index

**Welcome to the Spherepop documentation.**

Spherepop is a Python implementation of formal configuration transition semantics from "The History of Spherepop" paper.

---

## Documentation Structure

### For Users

**[README.md](../README.md)** - Start here
- Quick start guide
- Installation
- Basic usage examples
- Project overview

**[docs/api/](api/)** - API Reference (generated)
- Module documentation
- Function signatures
- Usage examples
- Generated with `make docs` or `docs/generate.sh`

### For Contributors

**[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development workflow
- How to contribute
- Code standards
- Theory discipline
- Experimental test markers
- Pull request process

**[docs/DEVELOPMENT.md](DEVELOPMENT.md)** - Architecture guide
- Module responsibilities
- Key abstractions
- Design patterns
- Common pitfalls
- Theory→Code mapping

**[docs/TESTING.md](TESTING.md)** - Testing guide
- Testing philosophy (explore/verify/prescribe)
- Test structure and categories
- Property-based testing
- Coverage strategy
- Experimental markers
- Maintenance procedures

### For Theorists

**[THEORY_STATUS.md](../THEORY_STATUS.md)** - **THE AUTHORITY** for paper vs implementation
- Questions Q1-Q8 with definitive answers
- Status categories: ✓ Paper-licensed | → Implementation choice | ? Open | ⊗ Contrary
- What's resolved vs what remains research
- Must be consulted before semantic changes

**[docs/SPECIFICATIONS.md](SPECIFICATIONS.md)** - Normative reference
- Precise definitions of primitives {POP, REFUSE, BIND, COLLAPSE}
- Full pre/post conditions
- Observer contracts (non-authority principle)
- Config invariants
- Continuation relation ⊑
- Testing traceability requirements

**[docs/OVERSOUL_PERFECTION.md](OVERSOUL_PERFECTION.md)** - Epistemic hygiene directive
- Perfection shall not be inferred from absence of violation
- Coverage ≠ completeness, tests pass ≠ semantics correct
- Specified ≠ exhaustive, documented ≠ resolved
- Sparse intervention, boundary maintenance
- Multi-timescale epistemic discipline

**[docs/EXPERIMENT_CATALOG.md](EXPERIMENT_CATALOG.md)** - All 29 experiments documented
- Classification: S (stable) | X (experimental) | Q (research) | I (infrastructure)
- Dependency layers 0→1→2→3
- Theory status and success criteria
- Cross-references to Q1-Q8
- Experiment template

**[docs/RESEARCH_PROGRAM.md](RESEARCH_PROGRAM.md)** - Manifest-driven laboratory workflow
- `python -m spherepop.lab` command surface
- Structured verification (`verify`) and comparison (`compare`)
- Theory-map generation and uncovered-claim reporting
- Conjecture registry integration (`conjectures/`)

**[docs/DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)** - Implementation choice rationale
- 11 DDRs (Design Decision Records)
- Context, decision, rationale, alternatives, consequences
- Status tracking (Accepted | Provisional | Superseded)
- Review criteria for provisional decisions

### For Researchers

**[FUTURE_DIRECTIONS.md](../FUTURE_DIRECTIONS.md)** - Unresolved continuations
- Research directions (Plan B, COLLAPSE composition, history compaction)
- Infrastructure extensions (LLM integration, CLI, optimization)
- Integration patterns
- Anti-patterns documentation
- Stochastic authorship signature protocol (separate project)

---

## Document Authority Hierarchy

```
"The History of Spherepop" (paper)
    ↓
THEORY_STATUS.md (Q1-Q8 interpretations)
    ↓
SPECIFICATIONS.md (normative definitions)
    ↓
Implementation (spherepop/*.py)
```

**Golden Rule**: If paper, theory status, specifications, and code disagree:
1. Paper is authoritative
2. THEORY_STATUS.md clarifies ambiguities
3. SPECIFICATIONS.md defines chosen interpretations
4. Code should match specifications
5. If code doesn't match, code is wrong (unless spec needs updating)

---

## Quick Navigation by Role

### "I want to use Spherepop"
1. [README.md](../README.md) - Installation and quick start
2. [docs/api/](api/) - API reference
3. Examples in `spherepop/NN-*/run.py`

### "I want to contribute"
1. [CONTRIBUTING.md](../CONTRIBUTING.md) - Workflow and standards
2. [docs/DEVELOPMENT.md](DEVELOPMENT.md) - Architecture
3. [docs/TESTING.md](TESTING.md) - Testing guidelines
4. [THEORY_STATUS.md](../THEORY_STATUS.md) - What's open vs resolved

### "I want to understand the theory"
1. "The History of Spherepop" (paper) - Primary source
2. [THEORY_STATUS.md](../THEORY_STATUS.md) - Paper interpretations
3. [docs/SPECIFICATIONS.md](SPECIFICATIONS.md) - Formal definitions
4. [docs/EXPERIMENT_CATALOG.md](EXPERIMENT_CATALOG.md) - Empirical explorations

### "I want to extend or modify Spherepop"
1. [THEORY_STATUS.md](../THEORY_STATUS.md) - What's open
2. [docs/SPECIFICATIONS.md](SPECIFICATIONS.md) - What's specified
3. [docs/DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) - Why choices were made
4. [CONTRIBUTING.md](../CONTRIBUTING.md) - How to propose changes

---

## Documentation Standards

All documentation follows these principles:

### Precision Over Brevity
Be precise. Ambiguity in specifications leads to divergent implementations.

**Good**: "REFUSE requires `∅ ⊂ refused ⊂ option_space` (nonempty proper subset)"
**Bad**: "REFUSE needs some options"

### Theory Status Marking
Mark all claims with theory status:
- ✓ **Paper-licensed**: Explicitly in paper
- → **Implementation choice**: Chosen among valid alternatives
- ? **Open**: Research question, unresolved
- ⊗ **Contrary**: Would violate paper (none should exist)

### Cross-References
Link related documents:
- Specifications → THEORY_STATUS.md Q#
- Tests → SPECIFICATIONS.md sections
- DDRs → Specifications and theory status
- Experiments → Regression tests

### Version History
Every document tracks changes:
```markdown
## Version History
- **2026-08-13**: Initial version
  - What was added
  - Why
```

---

## Maintenance

### When to Update Documentation

**THEORY_STATUS.md**: When paper interpretation changes or questions resolved  
**SPECIFICATIONS.md**: When normative behavior changes  
**DESIGN_DECISIONS.md**: When significant implementation choices made  
**EXPERIMENT_CATALOG.md**: When experiments added or reclassified  
**TESTING.md**: When testing strategy changes  
**DEVELOPMENT.md**: When architecture evolves  
**CONTRIBUTING.md**: When workflow changes

### Documentation Review Checklist

Before committing documentation changes:
- [ ] Authority hierarchy respected (paper → theory → spec → code)
- [ ] Theory status marked (✓ → ? ⊗)
- [ ] Cross-references updated
- [ ] Examples tested (if code samples)
- [ ] Version history entry added
- [ ] Related documents updated (maintain consistency)

---

## Document Relationships

```
README.md ─┬─> CONTRIBUTING.md ─┬─> DEVELOPMENT.md
           │                     ├─> TESTING.md
           │                     └─> THEORY_STATUS.md ─┬─> SPECIFICATIONS.md
           │                                           ├─> EXPERIMENT_CATALOG.md
           │                                           └─> DESIGN_DECISIONS.md
           │
           └─> FUTURE_DIRECTIONS.md

api/ (generated from docstrings in spherepop/*.py)
```

**Key dependencies**:
- SPECIFICATIONS.md depends on THEORY_STATUS.md (must stay consistent)
- TESTING.md references SPECIFICATIONS.md (for traceability)
- EXPERIMENT_CATALOG.md cross-references THEORY_STATUS.md (Q#)
- DESIGN_DECISIONS.md explains choices in SPECIFICATIONS.md

---

## Contributing to Documentation

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Documentation standards
- Markdown formatting
- Code example requirements
- Review process

**Documentation PRs should**:
- Clarify, never obscure
- Add precision, never ambiguity
- Maintain consistency across documents
- Update cross-references
- Follow authority hierarchy

---

## Getting Help

- **Usage questions**: Check README.md and API docs first
- **Theory questions**: See THEORY_STATUS.md and SPECIFICATIONS.md
- **Contributing**: Read CONTRIBUTING.md
- **Bugs**: File issue with minimal reproducer
- **Research questions**: See FUTURE_DIRECTIONS.md

---

## Glossary

**Config**: `(σ, option_space, history, collapse_log)` - complete system state

**Sphere**: Nested structure `(items, label)` where items are Atoms or Spheres

**Atom**: Primitive value, no internal structure

**Quotient**: Equivalence class from COLLAPSE, `{members: FrozenSet[Atom]}`

**Primitives**: The four operations {POP, REFUSE, BIND, COLLAPSE} - **CLOSED**, no 5th primitive

**Observers**: Functions that compute properties, never authorize continuations

**Continuation**: Relation `(σ₁, O₁) ⊑ (σ₂, O₂) ⇔ O₁ ⊇ O₂` (option reduction)

**History**: Sequence of operations `(op₁, op₂, ..., opₙ)` - intensional identity

**Extensional view**: Observable option set, `V(c) → FrozenSet[str]`

**Non-authority**: `V(h) ↛ h` - observers can't modify or authorize

**Admissible**: Operation satisfies preconditions, `admissible(op, c) = can_transition(op, c)`

**Confluent**: Order-independent, `∀π: eval_program(c, π(ops)) = same result`

**Regretful**: Closes future continuations (provisional definition Q6)

**Paper-licensed** (✓): Explicitly stated in "The History of Spherepop"

**Implementation choice** (→): Chosen among alternatives not constrained by paper

**Open** (? ): Research question, genuinely undetermined

**Contrary** (⊗): Would violate paper semantics

---

## Quick Links

### Core Documents
- [README.md](../README.md)
- [THEORY_STATUS.md](../THEORY_STATUS.md) ⭐ **Authority for paper interpretation**
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [FUTURE_DIRECTIONS.md](../FUTURE_DIRECTIONS.md)

### Technical Docs
- [SPECIFICATIONS.md](SPECIFICATIONS.md) ⭐ **Normative reference**
- [DEVELOPMENT.md](DEVELOPMENT.md)
- [TESTING.md](TESTING.md)
- [EXPERIMENT_CATALOG.md](EXPERIMENT_CATALOG.md)
- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)

### Generated
- [API Reference](api/)

---

## Version History

- **2026-08-13**: Initial documentation index
  - Created comprehensive navigation structure
  - Documented authority hierarchy
  - Established maintenance procedures
  - Added glossary and quick links
