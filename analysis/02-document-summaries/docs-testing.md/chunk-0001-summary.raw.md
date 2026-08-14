**Benchmark Example**

```python
# Benchmark the transition operation with a medium-sized configuration.
# We expect to see ~500 distinct options in the resulting option space.

from spherepop.transition import transition
from spherepop.refuse import RefuseOp

def benchmark_transition(cfg, refused=to_refuse):
    # Perform the transition and capture the result.
    result = transition(cfg, ops=[RefuseOp(refused=refused)])
    
    # Verify that we obtain an option space of roughly 500 entries.
    assert len(result.option_space) == 500
```

**Explanation**

- **Purpose**: The benchmark checks structural scaling—specifically the siz[3D[K
size (`|O|`) of the resulting `option_space` after applying a refuse operat[6D[K
operation.
- **Assertion**: We expect the length of `result.option_space` to be exactl[6D[K
exactly 500, serving as an empirical check for scalability with moderate‑si[11D[K
moderate‑size configurations.
- **Placement in CI**: This benchmark should run alongside other stability [K
tests and trigger only if it fails (e.g., `len(...) != 500`), ensuring that[4D[K
that any regression in the number of options is caught early.

--- 

**Testing Checklist**

| Category | Item |
|----------|------|
| **New Features** | ✅ Unit tests for all success paths <br>✅ Unit tests [K
for all error paths <br>✅ Integration test for typical usage <br>✅ Proper[6D[K
Property test if invariant exists <br>✅ Actionable error messages <br>✅ D[1D[K
Docstrings include *Specification:* and *Theory Status:* |
| **Bug Fixes** | ✅ Regression test reproduces the bug <br>✅ Fix makes re[2D[K
regression test pass <br>✅ No other tests are broken <br>✅ Root cause ide[3D[K
identified (not just symptom) <br>✅ Specification updated if behavior clar[4D[K
clarified <br>✅ Design Decision Record created if design decision changed [K
|
| **Refactoring** | ✅ All existing tests still pass <br>✅ Coverage unchan[6D[K
unchanged or improved <br>✅ No semantic changes (behavior identical) <br>✅[K
 Performance benchmarks unchanged (no regression) <br>✅ Updated docstrings[10D[K
docstrings for interface changes |

--- 

**Common Pitfalls & Solutions**

| Pitfall | Description | Fix |
|---------|-------------|-----|
| **Testing Implementation, Not Specification** | Verifying internal implem[6D[K
implementation details instead of the intended semantics. | Replace with a [K
test that checks the *expected* outcome (e.g., `admissible()` returns `Fals[5D[K
`False` for REFUSE with empty set). |
| **Circular Tests** | Testing multiple related properties in one suite cau[3D[K
causing dependency issues. | Split into independent tests; avoid asserting [K
multiple unrelated conditions within the same test case. |
| **Flaky Tests** | Failures due to timing, randomness, or shared resources[9D[K
resources. | Add explicit seeding for random generators (`@given(..., seed=[5D[K
seed=123)`), use temporary directories (`tmp_path`), and run with `--random[9D[K
`--random-order`. |
| **Overfitting to Implementation** | Writing tests that depend on the curr[4D[K
current code structure rather than intended behavior. | Refactor tests to a[1D[K
assert high‑level invariants (e.g., immutability) instead of implementation[14D[K
implementation details. |
| **Ignoring Experimental Markers** | Treating provisional or unstable feat[4D[K
features as stable. | Keep `@pytest.mark.experimental` for work-in-progress[16D[K
work-in-progress and review it regularly; mark resolved experiments with a [K
proper status change. |

--- 

**Test Coverage by Module**

| Module | Current Coverage | Priority | Target |
|--------|------------------|----------|--------|
| `model.py` | 100% | ✓ Complete | - |
| `semantics.py` | 83% | High | 90%+ |
| `observers.py` | 96% | ✓ Good | 95%+ |
| `views.py` | 78% | Medium | 85%+ |
| `grammar.py` | 97% | ✓ Good | 95%+ |
| `parser.py` | 82% | Medium | 90%+ |
| `predicates.py` | 94% | ✓ Good | 90%+ |
| `path_utils.py` | 92% | ✓ Good | 90%+ |
| `validation.py` | 88% | Good | 85%+ |
| `poset.py` (excluded) | 81% | — | — |

**Prioritization**

1. **Core primitives** (`semantics.py`) – highest priority due to foundatio[9D[K
foundational behavior.
2. **Parsers** (`parser.py`, `grammar.py`) – medium priority, ensuring corr[4D[K
correct syntax interpretation.
3. **Infrastructure** (`validation.py`, `views.py`) – medium priority for r[1D[K
reliability and usability.

--- 

**Continuous Integration (CI) Workflow**

*`.github/workflows/test.yml`*

```yaml
name: Test & Coverage

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{matrix.python-version}}
        uses: actions/setup-python@v5
        with:
          python-version: ${{{matrix.python-version}}}
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: pytest --cov=spherepop
      - name: Upload coverage report to Codecov
        if: github.ref == 'main'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

*`.github/workflows/lint.yml`*

```yaml
name: Lint

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: pip install ruff mypy
      - run: ruff lint
      - run: ruff format --check
      - run: mypy spherepop --strict
```

**Branch Protection Rules (suggested)**

- Require **lint** and **type‑checking** passes.
- Require **tests** to pass.
- Enforce a minimum coverage of **85 %** on the stable core modules (`model[7D[K
(`model.py`, `semantics.py`).
- Allow experimental test failures initially, but require them to be resolv[6D[K
resolved before merging.

--- 

**Version History**

| Date | Version | Change |
|------|---------|--------|
| 2026‑08‑13 | v0.1 | Initial testing guide and documentation; includes ben[3D[K
benchmark example, coverage table, CI workflow definitions, and common pitf[4D[K
pitfalls. |

---

*End of Document.*

