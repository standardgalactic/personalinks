# Spherepop

**A formal calculus of configuration transitions under historical constraint.**

Spherepop implements the four primitive operations from "The History of Spherepop" as an executable micro-lab. Configurations evolve through an immutable history, where each transition appends exactly one event:

```
(σ, h) → (σ', h · e)
```

The calculus is closed over four primitives:

- **POP**: Remove a nested scope, promoting its contents
- **REFUSE**: Contract the option space by eliminating unwanted choices  
- **BIND**: Filter options through a stated predicate
- **COLLAPSE**: Identify previously distinct options into equivalence classes

## Core Principle

> Spherepop treats **history as primary identity**. Two configurations may exhibit identical extensional views while remaining intensionally distinct — the trajectory matters, not merely what it presently looks like.

## Quick Start

```bash
# Install
pip install -e .

# Run tests
pytest

# Try an experiment
python spherepop/03-pop/run.py
```

## Installation

**Requirements:** Python 3.12+

```bash
git clone https://github.com/standardgalactic/personalinks.git
cd personalinks
pip install -e ".[dev]"
```

## Example Usage

```python
from spherepop import make_config, parse_sphere, transition
from spherepop.model import RefuseOp, CollapseOp

# Create initial configuration
cfg = make_config(
    parse_sphere("(root: a b c)"),
    {"a", "b", "c"}
)

# Refuse unwanted options
cfg = transition(cfg, RefuseOp(refused=frozenset({"c"})))

# Collapse remaining options into equivalence class
cfg = transition(cfg, CollapseOp(classes=(frozenset({"a", "b"}),)))

# History records the full trajectory
print(f"Events: {len(cfg.history)}")  # 2
```

## Architecture

**Stable Core** (`spherepop/`):
- `model.py` — Data structures for Config, Operations, Events
- `semantics.py` — The four primitive transitions
- `observers.py` — Read-only analysis (confluence, regret, admissibility)
- `views.py` — Presentation functions (extensional, history rendering)
- `grammar.py` — Appendix G concrete syntax parser
- `predicates.py` — BIND predicate DSL
- `path_utils.py` — Sphere tree navigation
- `validation.py` — Advisory configuration invariant checking

**Experiments** (`spherepop/NN-*/`):
- 29 numbered experiments exploring confluence, divergence, regret, horizon equivalence, and intensional vs extensional identity

**Research** (`spherepop/poset.py`):
- Plan B: Labeled option-space preorder (Appendix B semantics, not yet integrated)

## Documentation

- [**THEORY_STATUS.md**](./THEORY_STATUS.md) — What's paper-licensed vs implementation choice vs open
- [**CONTRIBUTING.md**](./CONTRIBUTING.md) — Development workflow and theory discipline
- [**docs/DEVELOPMENT.md**](./docs/DEVELOPMENT.md) — Architecture guide
- [**tests/COVERAGE.md**](./tests/COVERAGE.md) — Test coverage gaps and action plan
- **API Documentation**: Generate with `./docs/generate.sh`

## Testing

```bash
# Full suite (159 tests)
pytest

# With coverage
pytest --cov=spherepop

# Property tests only
pytest -m experimental

# Fast tests (exclude slow benchmarks)
pytest -m "not slow"
```

**Test Categories:**
- Unit tests for each module
- Property-based tests (Hypothesis)
- Regression tests from experiments 01-29
- Integration tests for operation sequences
- Validation tests for structural invariants

## Theory Discipline

Spherepop maintains strict separation between:

- **Paper-licensed semantics** — Explicitly stated in the appendices
- **Implementation choices** — Selected from valid alternatives (documented as such)
- **Open questions** — Genuinely underdetermined by current theory
- **Experimental** — Plan B, collapse composition, horizon equivalence details

See `THEORY_STATUS.md` for the complete status of questions Q1-Q8.

> **Prime directive:** Don't turn an unanswered semantic question into an implementation default and then later mistake the default for Spherepop theory.

## Current Status

- **Tests:** 159 passing (unit, property, regression, validation)
- **Coverage:** 73.89% (on path to 85% target)
- **Type safety:** mypy strict mode
- **Supported:** Python 3.12, 3.13

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development workflow
- Pre-commit hooks setup
- How to add tests for provisional semantics
- When to mark tests with `@pytest.mark.experimental`

## License

MIT

## Citation

```bibtex
@software{spherepop2026,
  title={Spherepop: A micro-lab for configuration transition calculi},
  author={Standard Galactic},
  year={2026},
  url={https://github.com/standardgalactic/personalinks}
}
```

---

**Status:** Active research. The four primitives are stable. Plan B (labeled preorder) and collapse composition remain experimental.
