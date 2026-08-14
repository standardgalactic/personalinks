# C004 — Bounded Replay Determinism

- **Status**: COMPUTATIONALLY_SUPPORTED
- **Claim ID**: `prop:replay-determinism`
- **Statement**: For fixed base configuration and program, replay is deterministic within implemented transition semantics.
- **Supporting Experiments**: 13, 24
- **Known Counterexamples**: None in current corpus
- **Scope Conditions**: Assumes deterministic Python runtime and fixed parser semantics.
- **Notes**: Separately tracks replay invariance under safe reorderings (`prop:replay-invariance-bounded-reordering`).
