**Benchmark Guidelines**

**Do**
- ✓ Test structural scaling: `T(|h|)`, `T(|O|)`, `T(k)`, `T(b)`
- ✓ Use parameterization: `@pytest.mark.parametrize("n", [10, 100, 1000])`
- ✓ Group related benchmarks: `@pytest.mark.benchmark(group="...")`
- ✓ Set generous thresholds (catch catastrophic regressions only)
- ✓ Document expected complexity: “O(n)”, “O(n²)”, “O(b^k)”

**Don’t**
- ✗ Set strict time thresholds (hardware‑dependent)
- ✗ Benchmark trivial operations (noise dominates)
- ✗ Run benchmarks in main test suite (mark `@pytest.mark.slow`)
- ✗ Optimize for benchmarks (optimize for real use cases)

**Run separately**

```bash
# Include experimental only
pytest -m slow --benchmark-only

# Compare to baseline
pytest -m slow --benchmark-compare  # Compare to baseline
```

---

## Experimental Test Markers

### When to Mark Experimental

Mark `@pytest.mark.experimental` when:
- ✓ Testing provisional semantics (Q#, implementation choice awaiting theor[5D[K
theory)
- ✓ Testing unresolved composition (COLLAPSE on quotients)
- ✓ Testing extrapolated behavior (quotient predicate lifting)
- ✓ Research question investigation

**Do NOT mark**
- ✗ Paper‑licensed behavior (even if complex)
- ✗ Infrastructure tests (validation, parsing, formatting)
- ✗ Stable observer behavior

### Example Markings

```python
# NOT experimental - paper‑licensed
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
4. **Update docstrings**: Add Specification: reference line and Theory Stat[4D[K
Status comment
5. **Reclassify markers**: Remove `experimental` if now stable (or add back[4D[K
back)
6. **Run full suite**: Ensure no regressions

### When Theory Questions Resolved

If `THEORY_STATUS.md` marks Q# as ✓:

1. **Find experimental tests**: `pytest -m experimental --co -q | grep test[4D[K
test_name`
2. **Review against paper**: Does implementation match?
3. **Update if needed**: Adjust implementation and tests
4. **Remove experimental markers**: Tests are now stable
5. **Update docstrings**: Change Theory Status line to ✓
6. **Update DESIGN_DECISIONS.md**: Mark DDR as Superseded if applicable

### When Experiments Complete

After running experiment NN:

1. **Document in EXPERIMENT_CATALOG.md**: Add entry with description, outco[5D[K
outcome, and links
2. **Extract regressions**: Stable behaviors → `test_regressions.py`
3. **Mark theory status**: S (stable), X (excluded), Q (questionable), I (i[2D[K
(incomplete)
4. **File research questions**: Open questions → THEORY_STATUS.md or FUTURE[6D[K
FUTURE_DIRECTIONS.md
5. **Don’t force conclusions**: Research ≠ specification

---

## Testing Checklist

### For New Features

- [ ] Unit tests for all success paths  
- [ ] Unit tests for all error paths  
- [ ] Integration test for typical usage  
- [ ] Property test if invariant exists  
- [ ] Error messages are actionable  
- [ ] Docstrings have **Specification:** and **Theory Status:** comments  
- [ ] Marked `@pytest.mark.experimental` if provisional  
- [ ] Updated **SPECIFICATIONS.md** if adding semantics  
- [ ] Updated **THEORY_STATUS.md** if resolving question  
- [ ] Coverage ≥ 85 % on stable core

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

**Bad**
```python
def test_refuse_uses_frozenset_difference():
    """REFUSE implementation uses frozenset.__sub__."""
    # Tests implementation detail, not behavior
```

**Good**
```python
def test_refuse_removes_specified_options():
    """REFUSE postcondition: option_space' = option_space \ refused.
        This ensures the invariant defined by the specification holds regardles[9D[K
    regardless of internal representation."""
    assert set(refused).issubset(option_space) and not any(op in option_space for op in refused)
```

### Pitfall 2: Circular Tests

**Bad**
```python
def test_admissible_matches_transition():
    """admissible() returns same as transition() success.
        This tests both sides of the equivalence but creates a circular depende[7D[K
    dependency."""
    for op in operations:
        assert admissible(op, cfg) == can_transition(op, cfg)
```

**Problem**: `can_transition` likely implemented as `try: transition(); ret[3D[K
return True`.

**Good**
```python
def test_admissible_detects_empty_refuse():
    """admissible() returns False for REFUSE with empty set.
        This isolates the specific failure mode without relying on other behavi[6D[K
    behavior."""
    cfg = make_config(...)
    assert not admissible(RefuseOp(refused=frozenset()), cfg)
```

### Pitfall 3: Flaky Tests

**Causes**
- Random testing without a seed
- Time‑dependent assertions (e.g., waiting for network responses)
- Filesystem race conditions or test order dependencies  
- Uncontrolled environments (temporary files, global state)

**Solutions**
- Use `@given` with **Hypothesis** (reproducible seeds) to exhaustively exp[3D[K
explore inputs
- Mock time/randomness via fixtures so that deterministic results are alway[5D[K
always produced
- Use temporary directories (`pytest's tmp_path`) to avoid shared‑state fla[3D[K
flakiness  
- Run tests with `--random-order` to surface order dependencies early

### Pitfall 4: Overfitting to Implementation

**Bad**
```python
def test_pop_clones_items_list():
    """POP clones items list to avoid mutation.
        This over‑specifies the implementation detail and becomes a regression [K
    target."""
```

**Good**
```python
def test_pop_doesnt_mutate_original():
    """POP returns a new Config, not mutating the original state.
        The invariant is about the system’s behavior, not its internal represen[8D[K
    representation."""
    original_history = cfg.history
    result = transition(cfg, PopOp(...))
    assert cfg.history is original_history  # Immutability guarantee
```

### Pitfall 5: Ignoring Experimental Markers

**Problem**: Treating experimental tests as stable can cause false‑positive[14D[K
false‑positive regression warnings.

**Solution**
- Always mark provisional semantics or research questions with `@pytest.mar[12D[K
`@pytest.mark.experimental`
- Include a brief comment in the docstring explaining why it is experimenta[11D[K
experimental (e.g., “provisional quotient predicate semantics – awaiting fo[2D[K
formal proof”)
- Review and remove markers when theory resolves
- Consider CI strategy: fail on experimental failures for critical modules,[8D[K
modules, otherwise treat them as warnings

---

## Test Coverage by Module

| Module | Coverage | Priority | Target |
|--------|----------|----------|--------|
| `model.py` | 100% | ✓ Complete | - |
| `semantics.py` | 83% | High | ≥ 90%+ |
| `observers.py` | 96% | ✓ Good | ≥ 95%+ |
| `views.py` | 78% | Medium | ≥ 85%+ |
| `grammar.py` | 97% | ✓ Good | ≥ 95%+ |
| `parser.py` | 82% | Medium | ≥ 90%+ |
| `predicates.py` | 94% | ✓ Good | ≥ 90%+ |
| `path_utils.py` | 92% | ✓ Good | ≥ 90%+ |
| `validation.py` | 88% | Good | ≥ 85%+ |
| `appendix_g.py` | 63% | Excluded | - |
| `poset.py` | 81% | Excluded | - |

**Prioritization**
1. Core primitives (`semantics.py`) – highest priority  
2. Parsers (`parser.py`, `grammar.py`) – medium priority  
3. Infrastructure (`validation.py`, `views.py`) – medium priority  
4. Experimental (`poset.py`) – excluded from requirement  
5. Legacy (`appendix_g.py`) – not part of the stable API  

---

### Summary

- Follow **benchmark guidelines** for performance testing.
- Use experimental marks wisely and update specs/theory as needed.
- Maintain high test coverage, especially in core semantics modules.
- Avoid implementation‑specific assertions; focus on behavior defined by sp[2D[K
specifications.

