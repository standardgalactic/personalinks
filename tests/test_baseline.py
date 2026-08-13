"""Tests for benchmark baseline tracking system."""

from __future__ import annotations

import json

import pytest

from spherepop.baseline import (
    DEFAULT_BASELINE_DIR,
    BaselineStore,
    BenchmarkResult,
    extract_structural_params,
    format_comparison_report,
    get_default_store,
)

# ============================================================================
# BenchmarkResult Tests
# ============================================================================


def test_benchmark_result_structural_key():
    """Structural key captures relevant dimensions."""
    result = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
        option_count=100,
        horizon=3,
        branching=2,
    )

    assert result.structural_key() == (10, 100, 3, 2)


def test_benchmark_result_is_structurally_equivalent():
    """Structural equivalence checks name, group, and dimensions."""
    r1 = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
        option_count=100,
    )

    r2 = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
        option_count=100,
        mean_us=500.0,  # Different performance
    )

    r3 = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=20,  # Different structure
        option_count=100,
    )

    assert r1.is_structurally_equivalent(r2)  # Same structure
    assert not r1.is_structurally_equivalent(r3)  # Different structure


def test_benchmark_result_relative_change():
    """Relative change computes ratio of current/baseline."""
    baseline = BenchmarkResult(
        name="test_foo",
        group="group1",
        mean_us=100.0,
    )

    current = BenchmarkResult(
        name="test_foo",
        group="group1",
        mean_us=150.0,  # 1.5x slower
    )

    assert current.relative_change(baseline) == 1.5


def test_benchmark_result_relative_change_requires_structural_equivalence():
    """Cannot compare structurally different benchmarks."""
    baseline = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
    )

    current = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=20,  # Different structure
    )

    with pytest.raises(ValueError, match="structurally different"):
        current.relative_change(baseline)


def test_benchmark_result_regression_severity():
    """Regression severity classification."""
    baseline = BenchmarkResult(name="test", group="g", mean_us=100.0)

    # Improvement: < 0.9x
    improved = BenchmarkResult(name="test", group="g", mean_us=80.0)
    assert improved.regression_severity(baseline) == "improvement"

    # Stable: 0.9x - 1.1x
    stable = BenchmarkResult(name="test", group="g", mean_us=105.0)
    assert stable.regression_severity(baseline) == "stable"

    # Regression: 1.1x - 1.5x
    regressed = BenchmarkResult(name="test", group="g", mean_us=130.0)
    assert regressed.regression_severity(baseline) == "regression"

    # Severe regression: > 1.5x
    severe = BenchmarkResult(name="test", group="g", mean_us=200.0)
    assert severe.regression_severity(baseline) == "severe_regression"


# ============================================================================
# BaselineStore Tests
# ============================================================================


def test_baseline_store_initialization(tmp_path):
    """BaselineStore creates root directory."""
    store_dir = tmp_path / "baselines"
    assert not store_dir.exists()

    BaselineStore(root_dir=store_dir)
    assert store_dir.exists()


def test_baseline_store_save_and_load(tmp_path):
    """Save and load benchmark results."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    result = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
        mean_us=123.45,
        timestamp="2026-08-13T09:00:00",
    )

    store.save_result(result)

    # Load history
    history = store.load_history("group1", "test_foo")
    assert len(history) == 1
    assert history[0].name == "test_foo"
    assert history[0].mean_us == 123.45


def test_baseline_store_append_results(tmp_path):
    """Multiple saves append to history."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    result1 = BenchmarkResult(name="test", group="g", mean_us=100.0, timestamp="T1")
    result2 = BenchmarkResult(name="test", group="g", mean_us=110.0, timestamp="T2")

    store.save_result(result1)
    store.save_result(result2)

    history = store.load_history("g", "test")
    assert len(history) == 2
    assert history[0].timestamp == "T1"
    assert history[1].timestamp == "T2"


def test_baseline_store_get_latest_baseline(tmp_path):
    """Get latest baseline returns most recent."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    result1 = BenchmarkResult(name="test", group="g", mean_us=100.0, timestamp="T1")
    result2 = BenchmarkResult(name="test", group="g", mean_us=110.0, timestamp="T2")
    result3 = BenchmarkResult(name="test", group="g", mean_us=105.0, timestamp="T3")

    store.save_result(result1)
    store.save_result(result2)
    store.save_result(result3)

    latest = store.get_latest_baseline("g", "test")
    assert latest is not None
    assert latest.timestamp == "T3"
    assert latest.mean_us == 105.0


def test_baseline_store_get_latest_baseline_no_history(tmp_path):
    """Get latest baseline returns None when no history."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    latest = store.get_latest_baseline("nonexistent", "test")
    assert latest is None


def test_baseline_store_compare_to_baseline_no_baseline(tmp_path):
    """Comparison without baseline reports no_baseline."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    result = BenchmarkResult(name="test", group="g", mean_us=100.0)
    comparison = store.compare_to_baseline(result)

    assert not comparison["has_baseline"]
    assert comparison["severity"] == "no_baseline"
    assert comparison["ratio"] is None


def test_baseline_store_compare_to_baseline_with_baseline(tmp_path):
    """Comparison with baseline computes ratio and severity."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    baseline = BenchmarkResult(name="test", group="g", mean_us=100.0, timestamp="T1")
    store.save_result(baseline)

    current = BenchmarkResult(name="test", group="g", mean_us=150.0, timestamp="T2")
    comparison = store.compare_to_baseline(current)

    assert comparison["has_baseline"]
    assert comparison["ratio"] == 1.5
    assert comparison["severity"] == "severe_regression"  # 1.5x = severe
    assert comparison["delta_us"] == 50.0
    assert comparison["baseline_timestamp"] == "T1"


def test_baseline_store_explicit_baseline(tmp_path):
    """Can compare against explicit baseline, not just latest."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    baseline1 = BenchmarkResult(name="test", group="g", mean_us=100.0, timestamp="T1")
    baseline2 = BenchmarkResult(name="test", group="g", mean_us=200.0, timestamp="T2")

    store.save_result(baseline1)
    store.save_result(baseline2)

    current = BenchmarkResult(name="test", group="g", mean_us=150.0, timestamp="T3")

    # Compare to explicit baseline1 (not latest)
    comparison = store.compare_to_baseline(current, baseline=baseline1)
    assert comparison["ratio"] == 1.5  # 150/100
    assert comparison["baseline_timestamp"] == "T1"


# ============================================================================
# Utility Function Tests
# ============================================================================


def test_extract_structural_params_depth():
    """Extract depth parameter from benchmark name."""
    params = extract_structural_params("test_benchmark_pop_depth_20")
    assert params["history_len"] == 20


def test_extract_structural_params_options():
    """Extract option count from benchmark name."""
    params = extract_structural_params("test_benchmark_refuse_1000_options")
    assert params["option_count"] == 1000


def test_extract_structural_params_horizon():
    """Extract horizon parameter from benchmark name."""
    params = extract_structural_params("test_benchmark_horizon_equivalent_k[3]")
    assert params["horizon"] == 3


def test_extract_structural_params_ops():
    """Extract operation count from benchmark name."""
    params = extract_structural_params("test_benchmark_eval_program_100_ops")
    assert params["history_len"] == 100


def test_extract_structural_params_multiple():
    """Extract multiple parameters."""
    params = extract_structural_params("test_refuse_1000_options_depth_50")
    assert params["option_count"] == 1000
    assert params["history_len"] == 50


def test_format_comparison_report_no_baseline():
    """Format report when no baseline available."""
    result = BenchmarkResult(
        name="test_foo",
        group="group1",
        mean_us=123.45,
        stddev_us=5.67,
    )

    comparison = {"has_baseline": False}
    report = format_comparison_report(result, comparison)

    assert "No baseline" in report
    assert "123" in report  # Flexible for rounding (123.4 or 123.5)


def test_format_comparison_report_with_baseline():
    """Format report with baseline comparison."""
    result = BenchmarkResult(
        name="test_foo",
        group="group1",
        mean_us=150.0,
        stddev_us=10.0,
    )

    comparison = {
        "has_baseline": True,
        "ratio": 1.5,
        "severity": "regression",
        "delta_us": 50.0,
        "baseline_mean_us": 100.0,
    }

    report = format_comparison_report(result, comparison)

    assert "100.0μs" in report  # Baseline
    assert "150.0μs" in report  # Current
    assert "+50%" in report or "50.0%" in report  # Change percentage
    assert "regression" in report


def test_format_comparison_report_improvement():
    """Format report for performance improvement."""
    result = BenchmarkResult(name="test", group="g", mean_us=80.0, stddev_us=5.0)

    comparison = {
        "has_baseline": True,
        "ratio": 0.8,
        "severity": "improvement",
        "delta_us": -20.0,
        "baseline_mean_us": 100.0,
    }

    report = format_comparison_report(result, comparison)

    assert "✓" in report
    assert "improvement" in report
    assert "-20%" in report or "20.0%" in report


def test_format_comparison_report_severe_regression():
    """Format report for severe regression."""
    result = BenchmarkResult(name="test", group="g", mean_us=200.0, stddev_us=10.0)

    comparison = {
        "has_baseline": True,
        "ratio": 2.0,
        "severity": "severe_regression",
        "delta_us": 100.0,
        "baseline_mean_us": 100.0,
    }

    report = format_comparison_report(result, comparison)

    assert "✗" in report
    assert "severe_regression" in report


def test_get_default_store():
    """Default store uses expected directory."""
    store = get_default_store()
    assert store.root_dir == DEFAULT_BASELINE_DIR


def test_baseline_store_json_format(tmp_path):
    """Baseline files are valid JSON."""
    store = BaselineStore(root_dir=tmp_path / "baselines")

    result = BenchmarkResult(
        name="test_foo",
        group="group1",
        history_len=10,
        mean_us=123.45,
        timestamp="2026-08-13T09:00:00",
    )

    store.save_result(result)

    # Check JSON file directly
    baseline_path = tmp_path / "baselines" / "group1" / "test_foo.json"
    assert baseline_path.exists()

    with open(baseline_path) as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "test_foo"
    assert data[0]["mean_us"] == 123.45
