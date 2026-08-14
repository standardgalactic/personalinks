# Spherepop Testing Guide

**Purpose**: Comprehensive testing strategy and guidelines  
**Audience**: Contributors, maintainers, researchers  
**Authority**: Engineering guide (not normative like SPECIFICATIONS.md)

---

## Testing Philosophy

### Three Testing Roles

**Experiments explore** - Generate empirical observations
- Live in `spherepop/NN-*/run.py`
- May discover surprising behavior
- Results inform theory, not specifications
- Failures are valuable data

**Tests verify** - Check implementations match specifications
- Live in `tests/test_*.py`
- Pass/fail based on current specifications
- Regressions are errors
- Failures require investigation

**Specifications prescribe** - Define correct behavior
- Live in `docs/SPECIFICATIONS.md`
- Authority hierarchy: Paper → Spec → Implementation
- Change requires elevated scrutiny
- Ambiguity resolved by paper authors

**Keep these roles distinct.**

---

## Test Categories

### By Stability

**Stable Tests** (default): Verify paper-licensed semantics
```python
def test_refuse_reduces_option_space():
    """REFUSE postcondition: option_space' ⊂ option_space.
    
    Specification: REFUSE → Postcondition 2
    Theory Status: Paper-licensed (Appendix E)
    """
    ...
```

**Experimental Tests**: Verify provisional semantics
```python
@pytest.mark.experimental
def test_bind_existential_quotient():
    """BIND quotient predicate (PROVISIONAL existential semantics).
    
    Specification: BIND → Quotient handling
    Theory Status: Q3 (implementation choice, awaiting clarification)
    """
    ...
```

**Slow Tests**: Performance/property tests
```python
@pytest.mark.slow
def test_benchmark_refuse_10000_options(benchmark):
    """Benchmark REFUSE with |O| = 10,000."""
    ...
```

### By Purpose

**Unit Tests**: Single function/operation
- `test_semantics.py`: Primitive operations
- `test_predicates.py`: BIND predicate logic
- `test_path_utils.py`: Path resolution
- `test_validation.py`: Config validation

**Property Tests**: Hypothesis-based generative
- `test_properties.py`: System-wide properties
  - History monotonicity
  - Replay determinism
  - Observer non-authority

**Regression Tests**: Extracted from experiments
- `test_regressions.py`: 32 tests from experiments 01-29
  - Known-good behaviors
  - Previously-discovered edge cases
  - Cross-corpus references (2120, affliction/infliction)

**Integration Tests**: Multi-operation sequences
- `test_observers.py`: Observer interactions
- `test_properties.py`: Full eval_program sequences

**Performance Tests**: Structural scaling
- `test_performance.py`: T(|h|, |O|, k, b)
  - Marked `@pytest.mark.slow`
  - Run separately with `pytest -m slow --benchmark-only`

---

## Test Structure

### Docstring Format

Every test MUST have a docstring with:

1. **What it tests** (one sentence)
2. **Specification reference** (where behavior is defined)
3. **Theory status** (paper-licensed, provisional, or open)
4. **Paper reference** (if applicable)

**Template**:
```python
def test_operation_property():
    """<What behavior is tested>.
    
    Specification: <Section in SPECIFICATIONS.md>
    Theory Status: <Paper-licensed | Q# | PROVISIONAL>
    Paper Reference: <Appendix X (if applicable)>
    """
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

**Example**:
```python
def test_refuse_nonempty_subset():
    """REFUSE requires nonempty proper subset of option_space.
    
    Specification: REFUSE → Precondition
    Theory Status: Paper-licensed (Appendix E)
    Paper Reference: Appendix E
    """
    cfg = make_config(simple_sphere, {"a", "b", "c"})
    
    # Empty refused set
    with pytest.raises(EvalError, match="nonempty"):
        transition(cfg, RefuseOp(refused=frozenset()))
    
    # Full refused set (would leave empty space)
    with pytest.raises(EvalError, match="empty space"):
        transition(cfg, RefuseOp(refused=frozenset({"a", "b", "c"})))
```

### Arrange-Act-Assert

Structure tests with clear phases:

```python
def test_something():
    # Arrange: Set up test data
    cfg = make_config(...)
    op = PopOp(label="L")
    
    # Act: Perform operation
    result = transition(cfg, op)
    
    # Assert: Verify postconditions
    assert len(result.history) == len(cfg.history) + 1
    assert result.option_space == cfg.option_space
```

### Fixtures

**Use fixtures for common setup**:

```python
@pytest.fixture
def simple_sphere():
    """Unlabeled sphere with three atoms."""
    return Sphere((Atom("a"), Atom("b"), Atom("c")), label=None)


@pytest.fixture
def labeled_nested():
    """Nested labeled spheres."""
    inner = Sphere((Atom("x"),), label="inner")
    return Sphere((inner, Atom("y")), label="outer")


def test_with_fixture(simple_sphere):
    cfg = make_config(simple_sphere, {"a", "b"})
    ...
```

**Fixture guidelines**:
- ✓ Fixtures for reusable test data
- ✓ Keep fixtures simple (no complex logic)
- ✗ Don't hide test setup (explicit > implicit)
- ✗ Don't overuse fixtures (prefer inline setup when simple)

---

## Test Coverage

### Current Status

**Coverage: 73.89%** (target: 85% on stable core)

**Exclusions from 85% requirement**:
- `poset.py`: Experimental (Plan B)
- `spherepop/NN-*/`: Experiments (research, not stable)

**Priority gaps** (see `tests/COVERAGE.md`):
1. `semantics.py`: 83% → 90%+ (core primitives)
2. `parser.py`: 82% → 90%+ (convenience parser)
3. `views.py`: 78% → 85%+ (derived views)

### Coverage Strategy

**Good coverage tests**:
- ✓ All success paths (normal operation)
- ✓ All error paths (precondition violations)
- ✓ Boundary conditions (empty, singleton, large)
- ✓ Edge cases discovered in experiments

**Coverage is a measurement, not an objective**:
- ⚠ 100% coverage ≠ complete testing (see `OVERSOUL_PERFECTION.md`)
- ⚠ Coverage shows what's executed, not correctness
- ✓ Uncovered code is definitely not tested
- ✓ Use coverage to find gaps, then write semantic tests

**Perfection inference** (OVERSOUL/PERFECTION-INFERENCE):
```
coverage = 100% ⇏ complete testing
tests pass ⇏ semantics correct
boundary marked ⇏ territory exhausted
```

**Target setting**:
```toml
# pyproject.toml
[tool.coverage.report]
fail_under = 85.0  # Enforced in CI (warning-only initially)
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

---

## Property-Based Testing

### Hypothesis Strategy

Use Hypothesis for system-wide properties:

```python
from hypothesis import given, strategies as st


@st.composite
def valid_configs(draw):
    """Strategy for generating valid Configs."""
    # Simple option space for tractability
    options = draw(
        st.lists(
            st.text(alphabet="abcdefgh", min_size=1, max_size=2),
            min_size=2,
            max_size=5,
            unique=True,
        )
    )
    sigma = Sphere(tuple(Atom(opt) for opt in options), label=None)
    option_set = frozenset(options)
    return make_config(sigma, option_set)


@given(cfg=valid_configs())
def test_property_history_monotone(cfg):
    """History length increases monotonically."""
    initial_len = len(cfg.history)

    # Try all admissible operations
    for op in [RefuseOp(refused=frozenset([next(iter(cfg.option_space))]))]:
        if admissible(op, cfg):
            result = transition(cfg, op)
            assert len(result.history) == initial_len + 1
```

**Property test guidelines**:
- ✓ Test invariants (properties that MUST hold)
- ✓ Use simple generators (complex generators = bugs in test)
- ✓ Shrink examples (Hypothesis finds minimal failing case)
- ✗ Don't test specific values (that's unit tests)
- ✗ Don't assume generated config is "normal" (test resilience)

**Good properties**:
- History monotonicity: `len(h') ≥ len(h)`
- Replay determinism: `eval_program(c, ops) == eval_program(c, ops)`
- Observer non-modification: `observer(c); assert c unchanged`
- Continuation antisymmetry: `c₁ ⊑ c₂ ∧ c₂ ⊑ c₁ ⇒ O₁ = O₂`

---

## Regression Testing

### Extracting Tests from Experiments

When an experiment reveals stable behavior:

1. **Identify the insight**: What specific behavior was observed?
2. **Check theory status**: Paper-licensed, provisional, or open?
3. **Write focused test**: Test the insight, not entire experiment
4. **Add to test_regressions.py**: Group by theme
5. **Mark appropriately**: Experimental if provisional

**Example extraction**:

Experiment 20 (intensional-extensional-equivalence) reveals:
```python
# Experiment observation:
# Two histories can produce same extensional view

# Extracted regression test:
def test_regression_intensional_vs_extensional():
    """Extensional equality doesn't imply intensional identity.
    
    # 2120
    
    Specification: Observer non-authority
    Theory Status: Paper-licensed (Q5)
    Cross-corpus: affliction/infliction, unidimary 2120
    """
    # Two paths to same state
    cfg1 = make_config(...)
    cfg1 = transition(cfg1, RefuseOp(...))
    
    cfg2 = make_config(...)
    cfg2 = transition(cfg2, BindOp(...))
    
    # Same observable view
    assert extensional_view(cfg1) == extensional_view(cfg2)
    
    # Different histories
    assert cfg1.history != cfg2.history
    
    # Configs are distinct (intensional identity)
    assert cfg1 != cfg2  # May require custom __eq__
```

### Regression Test Organization

Group by theme, not chronologically:

```python
# test_regressions.py

# ============================================================================
# History and Identity
# ============================================================================


def test_regression_history_monotonicity(): ...
def test_regression_intensional_vs_extensional(): ...
def test_regression_replay_determinism(): ...


# ============================================================================
# Quotient Behavior
# ============================================================================


def test_regression_quotient_equality(): ...
def test_regression_quotient_representative_independence(): ...


# ============================================================================
# Observer Non-Authority
# ============================================================================


def test_regression_observer_non_authority(): ...
def test_regression_three_observers_agree(): ...
```

---

## Error Testing

### Testing Preconditions

Every operation precondition MUST have a test:

```python
def test_refuse_precondition_nonempty():
    """REFUSE requires refused ≠ ∅."""
    cfg = make_config(...)
    with pytest.raises(EvalError, match="nonempty"):
        transition(cfg, RefuseOp(refused=frozenset()))


def test_refuse_precondition_proper_subset():
    """REFUSE requires refused ⊂ option_space (proper subset)."""
    cfg = make_config(simple_sphere, {"a", "b"})
    with pytest.raises(EvalError, match="empty space"):
        transition(cfg, RefuseOp(refused=frozenset({"a", "b"})))


def test_refuse_precondition_subset():
    """REFUSE requires refused ⊆ option_space."""
    cfg = make_config(simple_sphere, {"a", "b"})
    with pytest.raises(EvalError, match="subset"):
        transition(cfg, RefuseOp(refused=frozenset({"a", "b", "x"})))
```

### Error Message Quality

Test error messages are actionable:

```python
def test_error_message_actionable():
    """Error messages explain what's wrong and what was expected."""
    cfg = make_config(simple_sphere, {"a", "b"})
    
    with pytest.raises(EvalError) as exc_info:
        transition(cfg, RefuseOp(refused=frozenset({"x"})))
    
    error_msg = str(exc_info.value)
    assert "subset" in error_msg  # What's wrong
    assert "available" in error_msg  # Context
    assert "{a, b}" in error_msg or "a" in error_msg  # Actual options
```

---

## Performance Testing

### Benchmark Structure

```python
@pytest.mark.benchmark(group="refuse-cardinality")
def test_benchmark_refuse_1000_options(benchmark):
    """REFUSE with |O| = 1000.
    
    Measures: Time as function of option space cardinality
    Structural: T(|O|) scaling
    Threshold: ~250μs (sanity check, not strict contract)
    """
    sigma = make_wide_sphere(1000)
    options = make_large_option_space(1000)
    cfg = make_config(sigma, options)
    
    to_refuse = frozenset(f"option_{i}" for i in range(500))
    result = benchmark(transition, cfg, RefuseOp(refused=to_refuse))
    
    assert len(result.option_space) == 500
```

### Benchmark Guidelines

**Do**:
- ✓ Test structural scaling: T(|h|), T(|O|), T(k), T(b)
- ✓ Use parameterization: `@pytest.mark.parametrize("n", [10, 100, 1000])`
- ✓ Group related benchmarks: `@pytest.mark.benchmark(group="...")`
- ✓ Set generous thresholds (catch catastrophic regressions only)
- ✓ Document expected complexity: "O(n)", "O(n²)", "O(b^k)"

**Don't**:
- ✗ Set strict time thresholds (hardware-dependent)
- ✗ Benchmark trivial operations (noise dominates)
- ✗ Run benchmarks in main test suite (mark `@pytest.mark.slow`)
- ✗ Optimize for benchmarks (optimize for real use cases)

**Run separately**:
```bash
pytest -m slow --benchmark-only
pytest -m slow --benchmark-compare  # Compare to baseline
```

---

## Experimental Test Markers

### When to Mark Experimental

Mark `@pytest.mark.experimental` when:
- ✓ Testing provisional semantics (Q#, implementation choice awaiting theory)
- ✓ Testing unresolved composition (COLLAPSE on quotients)
- ✓ Testing extrapolated behavior (quotient predicate lifting)
- ✓ Research question investigation

**Do NOT mark**:
- ✗ Paper-licensed behavior (even if complex)
- ✗ Infrastructure tests (validation, parsing, formatting)
- ✗ Stable observer behavior

### Example Markings

```python
# NOT experimental - paper-licensed
def test_refuse_removes_options():
    """REFUSE reduces option space (Appendix E)."""
    ...


# EXPERIMENTAL - provisional quotient predicate semantics (Q3)
@pytest.mark.experimental
def test_bind_quotient_existential():
    """BIND uses existential semantics on quotients (PROVISIONAL)."""
    ...


# NOT experimental - infrastructure
def test_validate_detects_invalid_option():
    """Validation identifies options not in sigma."""
    ...


# EXPERIMENTAL - unresolved COLLAPSE composition (Q2b)
@pytest.mark.experimental
def test_collapse_composition():
    """COLLAPSE on quotients (unresolved, currently errors)."""
    with pytest.raises(EvalError):
        ...
```

### Running Experimental Tests

```bash
# Include experimental (default)
pytest

# Exclude experimental
pytest -m "not experimental"

# Only experimental
pytest -m experimental
```

---

## Test Maintenance

### When Specifications Change

If `SPECIFICATIONS.md` changes:

1. **Identify affected tests**: Grep for specification section name
2. **Review theory status**: Did Q# get resolved?
3. **Update test assertions**: Match new specification
4. **Update docstrings**: Update Specification: reference
5. **Reclassify markers**: Remove `experimental` if now stable
6. **Run full suite**: Ensure no regressions

### When Theory Questions Resolved

If `THEORY_STATUS.md` Q# changes from ? or → to ✓:

1. **Find experimental tests**: `pytest -m experimental --co -q | grep test_name`
2. **Review against paper**: Does implementation match?
3. **Update if needed**: Adjust implementation and tests
4. **Remove experimental markers**: Tests are now stable
5. **Update docstrings**: Change Theory Status line
6. **Update DESIGN_DECISIONS.md**: Mark DDR as Superseded if applicable

### When Experiments Complete

After running experiment NN:

1. **Document in EXPERIMENT_CATALOG.md**: Add entry
2. **Extract regressions**: Stable behaviors → `test_regressions.py`
3. **Mark theory status**: S, X, Q, or I classification
4. **File research questions**: Open questions → THEORY_STATUS.md or FUTURE_DIRECTIONS.md
5. **Don't force conclusions**: Research ≠ specification

---

## Testing Checklist

### For New Features

- [ ] Unit tests for all success paths
- [ ] Unit tests for all error paths
- [ ] Integration test for typical usage
- [ ] Property test if invariant exists
- [ ] Error messages are actionable
- [ ] Docstrings have Specification: and Theory Status:
- [ ] Marked `@pytest.mark.experimental` if provisional
- [ ] Updated SPECIFICATIONS.md if adding semantics
- [ ] Updated THEORY_STATUS.md if resolving question
- [ ] Coverage ≥ 85% on stable core

### For Bug Fixes

- [ ] Regression test reproduces bug
- [ ] Fix makes regression test pass
- [ ] No other tests regressed
- [ ] Root cause identified (not just symptom)
- [ ] Specification updated if behavior clarified
- [ ] DDR created if design decision changed

### For Refactoring

- [ ] All existing tests still pass
- [ ] Coverage unchanged or improved
- [ ] No semantic changes (behavior identical)
- [ ] Performance benchmarks unchanged (no regression)
- [ ] Updated docstrings if interfaces changed

---

## Common Testing Pitfalls

### Pitfall 1: Testing Implementation, Not Specification

**Bad**:
```python
def test_refuse_uses_frozenset_difference():
    """REFUSE implementation uses frozenset.__sub__."""
    # Tests implementation detail, not behavior
```

**Good**:
```python
def test_refuse_removes_specified_options():
    """REFUSE postcondition: option_space' = option_space \ refused."""
    # Tests specified behavior
```

### Pitfall 2: Circular Tests

**Bad**:
```python
def test_admissible_matches_transition():
    """admissible() returns same as transition() success."""
    for op in operations:
        assert admissible(op, cfg) == can_transition(op, cfg)
```

**Problem**: `can_transition` likely implemented as `try: transition(); return True`.

**Good**:
```python
def test_admissible_detects_empty_refuse():
    """admissible() returns False for REFUSE with empty set."""
    cfg = make_config(...)
    assert not admissible(RefuseOp(refused=frozenset()), cfg)
```

### Pitfall 3: Flaky Tests

**Causes**:
- Random without seed
- Time-dependent assertions
- Filesystem race conditions
- Test order dependencies

**Solutions**:
- Use `@given` with Hypothesis (reproducible seeds)
- Mock time/random with fixtures
- Use temp directories (pytest's `tmp_path`)
- Make tests independent (`--random-order` should pass)

### Pitfall 4: Overfitting to Implementation

**Bad**:
```python
def test_pop_clones_items_list():
    """POP clones items list to avoid mutation."""
    # Over-specifies implementation
```

**Good**:
```python
def test_pop_doesnt_mutate_original():
    """POP returns new Config, doesn't mutate original."""
    original_history = cfg.history
    result = transition(cfg, PopOp(...))
    assert cfg.history is original_history  # Immutability
```

### Pitfall 5: Ignoring Experimental Markers

**Problem**: Treating experimental tests as stable

**Solution**:
- Always mark provisional semantics as `@pytest.mark.experimental`
- Document why it's experimental in docstring
- Review and remove markers when theory resolves
- Consider CI strategy (fail on experimental failures or just warn?)

---

## Test Coverage by Module

| Module | Coverage | Priority | Target |
|--------|----------|----------|--------|
| `model.py` | 100% | ✓ Complete | - |
| `semantics.py` | 83% | High | 90%+ |
| `observers.py` | 96% | ✓ Good | 95%+ |
| `views.py` | 78% | Medium | 85%+ |
| `grammar.py` | 97% | ✓ Good | 95%+ |
| `parser.py` | 82% | Medium | 90%+ |
| `predicates.py` | 94% | ✓ Good | 90%+ |
| `path_utils.py` | 92% | ✓ Good | 90%+ |
| `validation.py` | 88% | Good | 85%+ |
| `poset.py` | 81% | Excluded | - |

**Prioritization**:
1. Core primitives (`semantics.py`) - highest priority
2. Parsers (`parser.py`, `grammar.py`) - medium priority
3. Infrastructure (`validation.py`, `views.py`) - medium priority
4. Experimental (`poset.py`) - excluded from requirement

---

## Continuous Integration

### GitHub Actions Workflows

**.github/workflows/test.yml**:
```yaml
- Python 3.12, 3.13 matrix
- Run all tests: pytest tests/
- Coverage report: pytest --cov=spherepop
- Fail if coverage < 85% on stable core (warning initially)
- Upload to Codecov
```

**.github/workflows/lint.yml**:
```yaml
- Ruff lint
- Ruff format check
- Mypy type check (strict mode)
```

**Branch protection** (recommended):
- Require: lint passing
- Require: tests passing
- Require: coverage ≥ 85% (after gaps filled)
- Allow: experimental test failures? (TBD)

---

## Version History

- **2026-08-13**: Initial testing guide
  - Documented testing philosophy (explore/verify/prescribe)
  - Established test categories and structure
  - Provided comprehensive examples
  - Cross-referenced SPECIFICATIONS.md and THEORY_STATUS.md
