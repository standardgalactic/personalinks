"""Performance benchmarks for Spherepop operations.

These tests measure computational cost as functions of structural variables:
    |h| - history length
    |O| - option space cardinality
    k   - observational horizon
    b   - branching factor

Per OVERSOUL directive §9, benchmarks record T(|h|,|O|,k,b) and M(|h|,|O|,k,b)
rather than absolute wall-clock times. This reveals algorithmic scaling
rather than hardware variance.

Thresholds are generous "sanity checks" to catch catastrophic regressions
(e.g., accidental exponential traversal), not strict performance contracts.

Run separately with: pytest -m slow --benchmark-only
"""

from __future__ import annotations

import pytest

from spherepop import make_config, transition
from spherepop.model import (
    Atom,
    BindOp,
    CollapseOp,
    PopOp,
    RefuseOp,
    Sphere,
)
from spherepop.observers import admissible, equivalent_at, horizon_equivalent
from spherepop.semantics import eval_program

pytestmark = pytest.mark.slow


# ============================================================================
# Fixtures: Synthetic Workloads
# ============================================================================


def make_deeply_nested_sphere(depth: int, label_prefix: str = "L") -> Sphere:
    """Create a sphere nested to specified depth."""
    if depth == 0:
        return Sphere((Atom("x"),), label=f"{label_prefix}0")

    inner = make_deeply_nested_sphere(depth - 1, label_prefix)
    return Sphere((inner,), label=f"{label_prefix}{depth}")


def make_wide_sphere(width: int) -> Sphere:
    """Create a sphere with many immediate children."""
    items = tuple(Atom(f"opt{i}") for i in range(width))
    return Sphere(items, label="root")


def make_large_option_space(size: int) -> frozenset[str]:
    """Create an option space with many options."""
    return frozenset(f"option_{i}" for i in range(size))


# ============================================================================
# POP Benchmarks (depth scaling)
# ============================================================================


@pytest.mark.benchmark(group="pop-depth")
def test_benchmark_pop_depth_10(benchmark):
    """POP on depth-10 nested sphere."""
    sigma = make_deeply_nested_sphere(10)
    cfg = make_config(sigma, {"x"})

    # Benchmark popping the deepest sphere
    result = benchmark(transition, cfg, PopOp(label="L1"))
    assert len(result.history) == 1


@pytest.mark.benchmark(group="pop-depth")
def test_benchmark_pop_depth_20(benchmark):
    """POP on depth-20 nested sphere."""
    sigma = make_deeply_nested_sphere(20)
    cfg = make_config(sigma, {"x"})

    result = benchmark(transition, cfg, PopOp(label="L1"))
    assert len(result.history) == 1


@pytest.mark.benchmark(group="pop-depth")
def test_benchmark_pop_depth_50(benchmark):
    """POP on depth-50 nested sphere.

    Sanity check: Should complete in reasonable time despite depth.
    Path resolution is O(depth) but depth=50 is still tractable.
    """
    sigma = make_deeply_nested_sphere(50)
    cfg = make_config(sigma, {"x"})

    result = benchmark(transition, cfg, PopOp(label="L1"))
    assert len(result.history) == 1


# ============================================================================
# REFUSE Benchmarks (|O| scaling)
# ============================================================================


@pytest.mark.benchmark(group="refuse-cardinality")
def test_benchmark_refuse_100_options(benchmark):
    """REFUSE with |O| = 100."""
    sigma = make_wide_sphere(100)
    options = make_large_option_space(100)
    cfg = make_config(sigma, options)

    # Refuse half the options
    to_refuse = frozenset(f"option_{i}" for i in range(50))
    result = benchmark(transition, cfg, RefuseOp(refused=to_refuse))

    assert len(result.option_space) == 50


@pytest.mark.benchmark(group="refuse-cardinality")
def test_benchmark_refuse_1000_options(benchmark):
    """REFUSE with |O| = 1000.

    This tests frozenset operations at scale.
    """
    sigma = make_wide_sphere(1000)
    options = make_large_option_space(1000)
    cfg = make_config(sigma, options)

    to_refuse = frozenset(f"option_{i}" for i in range(500))
    result = benchmark(transition, cfg, RefuseOp(refused=to_refuse))

    assert len(result.option_space) == 500


@pytest.mark.benchmark(group="refuse-cardinality")
def test_benchmark_refuse_10000_options(benchmark):
    """REFUSE with |O| = 10,000.

    Stress test for large option spaces.
    Sanity threshold: Should complete in <1 second.
    """
    sigma = make_wide_sphere(10000)
    options = make_large_option_space(10000)
    cfg = make_config(sigma, options)

    to_refuse = frozenset(f"option_{i}" for i in range(5000))
    result = benchmark(transition, cfg, RefuseOp(refused=to_refuse))

    assert len(result.option_space) == 5000


# ============================================================================
# BIND Benchmarks (predicate evaluation)
# ============================================================================


@pytest.mark.benchmark(group="bind-predicate")
def test_benchmark_bind_prefix_1000(benchmark):
    """BIND with prefix predicate over 1000 options."""
    sigma = make_wide_sphere(1000)
    options = make_large_option_space(1000)
    cfg = make_config(sigma, options)

    # Bind to options with specific prefix
    result = benchmark(transition, cfg, BindOp(predicate="prefix:option_1"))

    # Should match option_1, option_10-19, option_100-199
    assert len(result.option_space) > 0


@pytest.mark.benchmark(group="bind-predicate")
def test_benchmark_bind_contains_large(benchmark):
    """BIND with contains predicate on large space."""
    sigma = make_wide_sphere(1000)
    options = make_large_option_space(1000)
    cfg = make_config(sigma, options)

    result = benchmark(transition, cfg, BindOp(predicate="contains:5"))
    assert len(result.option_space) > 0


# ============================================================================
# COLLAPSE Benchmarks (quotient construction)
# ============================================================================


@pytest.mark.benchmark(group="collapse-classes")
def test_benchmark_collapse_10_classes(benchmark):
    """COLLAPSE creating 10 equivalence classes."""
    options = make_large_option_space(100)
    cfg = make_config(make_wide_sphere(100), options)

    # Create 10 classes of 10 members each
    classes = tuple(frozenset(f"option_{i * 10 + j}" for j in range(10)) for i in range(10))

    result = benchmark(transition, cfg, CollapseOp(classes=classes))
    assert len(result.option_space) == 10  # 10 quotients


@pytest.mark.benchmark(group="collapse-classes")
def test_benchmark_collapse_100_classes(benchmark):
    """COLLAPSE creating 100 equivalence classes."""
    options = make_large_option_space(1000)
    cfg = make_config(make_wide_sphere(1000), options)

    # Create 100 classes of 10 members each
    classes = tuple(frozenset(f"option_{i * 10 + j}" for j in range(10)) for i in range(100))

    result = benchmark(transition, cfg, CollapseOp(classes=classes))
    assert len(result.option_space) == 100


# ============================================================================
# eval_program Benchmarks (|h| scaling)
# ============================================================================


@pytest.mark.benchmark(group="eval-program")
def test_benchmark_eval_program_10_ops(benchmark):
    """Execute 10 operations sequentially."""
    cfg = make_config(make_wide_sphere(20), make_large_option_space(20))

    ops = [RefuseOp(refused=frozenset([f"option_{i}"])) for i in range(10)]

    result = benchmark(eval_program, cfg, ops)
    assert len(result.history) == 10


@pytest.mark.benchmark(group="eval-program")
def test_benchmark_eval_program_100_ops(benchmark):
    """Execute 100 operations sequentially.

    Tests history accumulation cost T(|h|).
    """
    cfg = make_config(make_wide_sphere(150), make_large_option_space(150))

    ops = [RefuseOp(refused=frozenset([f"option_{i}"])) for i in range(100)]

    result = benchmark(eval_program, cfg, ops)
    assert len(result.history) == 100


# ============================================================================
# Observer Benchmarks
# ============================================================================


@pytest.mark.benchmark(group="observers")
def test_benchmark_admissible_check(benchmark):
    """Benchmark admissible() predicate checking."""
    cfg = make_config(make_wide_sphere(100), make_large_option_space(100))
    op = RefuseOp(refused=frozenset(["option_50"]))

    result = benchmark(admissible, op, cfg)
    assert result is True


@pytest.mark.benchmark(group="observers")
def test_benchmark_equivalent_at_depth_3(benchmark):
    """Benchmark equivalent_at with k=3."""
    cfg = make_config(make_wide_sphere(10), make_large_option_space(10))

    ops1 = [RefuseOp(refused=frozenset([f"option_{i}"])) for i in range(5)]
    ops2 = [RefuseOp(refused=frozenset([f"option_{i}"])) for i in range(5)]

    result = benchmark(equivalent_at, cfg, ops1, ops2, 3)
    assert isinstance(result, bool)


# ============================================================================
# Horizon Equivalence (k scaling) - Most Expensive
# ============================================================================


@pytest.mark.benchmark(group="horizon-equivalence")
@pytest.mark.parametrize("k", [2, 3, 4])
def test_benchmark_horizon_equivalent_k(benchmark, k):
    """Benchmark horizon_equivalent for varying k.

    This is the most expensive observer - it explores full reachable sets.
    Cost scales exponentially with k but is bounded by candidate_ops.
    """
    cfg1 = make_config(make_wide_sphere(5), make_large_option_space(5))
    cfg2 = make_config(make_wide_sphere(5), make_large_option_space(5))

    # Small candidate set to keep tractable
    candidate_ops = [RefuseOp(refused=frozenset([f"option_{i}"])) for i in range(3)]

    result = benchmark(horizon_equivalent, cfg1, cfg2, candidate_ops, k)
    assert isinstance(result, bool)


# ============================================================================
# Structural Complexity Benchmarks
# ============================================================================


@pytest.mark.benchmark(group="structural")
def test_benchmark_complex_history(benchmark):
    """Benchmark with complex history: mix of all operations."""
    cfg = make_config(make_wide_sphere(100), make_large_option_space(100))

    ops = [
        RefuseOp(refused=frozenset(["option_0", "option_1"])),
        BindOp(predicate="prefix:option_"),  # Keep all option_* (no-op filter)
        CollapseOp(classes=(frozenset(["option_10", "option_11"]),)),
        RefuseOp(refused=frozenset(["option_2", "option_3"])),
        BindOp(predicate="ALL"),  # Keep all
    ]

    result = benchmark(eval_program, cfg, ops)
    assert len(result.history) == 5


# ============================================================================
# Summary Reporter
# ============================================================================


def test_benchmark_summary():
    """Informational test explaining benchmark usage.

    Run benchmarks with:
        pytest -m slow --benchmark-only

    Compare runs:
        pytest -m slow --benchmark-autosave
        pytest -m slow --benchmark-compare

    Generate report:
        pytest -m slow --benchmark-only --benchmark-json=benchmark.json
    """
    pass
