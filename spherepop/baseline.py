"""Benchmark baseline tracking for performance regression detection.

Per OVERSOUL directive §9 (PERFORMANCE):
    "Record at minimum dependencies of cost on |h|, |O|, k, b.
     Seek empirical functions T = T(|h|, |O|, k, b)."

This module provides baseline storage, comparison, and regression detection
based on structural variables, not absolute wall-clock times.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BenchmarkResult:
    """Single benchmark measurement.

    Structural variables (what we measure against):
        history_len: |h| - number of operations in history
        option_count: |O| - cardinality of option space
        horizon: k - observational horizon depth
        branching: b - branching factor in structure

    Performance metrics (what we observe):
        mean_us: Mean time in microseconds
        stddev_us: Standard deviation in microseconds
        ops_per_sec: Operations per second (1 / mean)

    Context:
        name: Benchmark function name
        group: Benchmark group (e.g., "pop-depth", "refuse-cardinality")
        timestamp: When measurement was taken
        git_commit: Git commit hash (if available)
        python_version: Python version used
    """

    # Test identification
    name: str
    group: str

    # Structural variables
    history_len: int | None = None
    option_count: int | None = None
    horizon: int | None = None
    branching: int | None = None

    # Performance metrics
    mean_us: float = 0.0
    stddev_us: float = 0.0
    ops_per_sec: float = 0.0

    # Context
    timestamp: str = ""
    git_commit: str = ""
    python_version: str = ""

    def structural_key(self) -> tuple[int | None, ...]:
        """Key for comparing structurally equivalent benchmarks."""
        return (self.history_len, self.option_count, self.horizon, self.branching)

    def is_structurally_equivalent(self, other: BenchmarkResult) -> bool:
        """Check if two benchmarks measure same structural parameters."""
        return (
            self.name == other.name
            and self.group == other.group
            and self.structural_key() == other.structural_key()
        )

    def relative_change(self, baseline: BenchmarkResult) -> float:
        """Compute relative performance change vs baseline.

        Returns:
            Ratio of current/baseline time.
            > 1.0 means slower (regression)
            < 1.0 means faster (improvement)
        """
        if not self.is_structurally_equivalent(baseline):
            raise ValueError(
                f"Cannot compare structurally different benchmarks: "
                f"{self.structural_key()} vs {baseline.structural_key()}"
            )

        if baseline.mean_us == 0:
            return float("inf")

        return self.mean_us / baseline.mean_us

    def regression_severity(self, baseline: BenchmarkResult, threshold: float = 1.5) -> str:
        """Classify regression severity.

        Args:
            baseline: Previous measurement
            threshold: Multiplier for "significant" regression (default 1.5x)

        Returns:
            "improvement" | "stable" | "regression" | "severe_regression"
        """
        ratio = self.relative_change(baseline)

        if ratio < 0.9:
            return "improvement"
        elif ratio < 1.1:
            return "stable"
        elif ratio < threshold:
            return "regression"
        else:
            return "severe_regression"


@dataclass
class BaselineStore:
    """Storage and retrieval of benchmark baselines.

    Baselines stored in JSON format:
        .benchmarks/baselines/{group}/{name}.json

    Each file contains list of historical measurements for that benchmark.
    """

    root_dir: Path

    def __post_init__(self):
        """Ensure baseline directory exists."""
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _baseline_path(self, group: str, name: str) -> Path:
        """Path to baseline file for given benchmark."""
        group_dir = self.root_dir / group
        group_dir.mkdir(parents=True, exist_ok=True)
        return group_dir / f"{name}.json"

    def save_result(self, result: BenchmarkResult) -> None:
        """Append benchmark result to baseline history."""
        path = self._baseline_path(result.group, result.name)

        # Load existing results
        history = []
        if path.exists():
            with open(path) as f:
                history = json.load(f)

        # Append new result
        history.append(asdict(result))

        # Save updated history
        with open(path, "w") as f:
            json.dump(history, f, indent=2)

    def load_history(self, group: str, name: str) -> list[BenchmarkResult]:
        """Load all historical results for given benchmark."""
        path = self._baseline_path(group, name)

        if not path.exists():
            return []

        with open(path) as f:
            data = json.load(f)

        return [BenchmarkResult(**item) for item in data]

    def get_latest_baseline(self, group: str, name: str) -> BenchmarkResult | None:
        """Get most recent baseline for given benchmark."""
        history = self.load_history(group, name)
        return history[-1] if history else None

    def compare_to_baseline(
        self, result: BenchmarkResult, baseline: BenchmarkResult | None = None
    ) -> dict[str, Any]:
        """Compare result to baseline, return detailed comparison.

        Args:
            result: Current benchmark result
            baseline: Baseline to compare against (defaults to latest)

        Returns:
            Dictionary with:
                has_baseline: bool
                ratio: float (current/baseline time)
                severity: str
                delta_us: float (difference in microseconds)
                baseline_timestamp: str
        """
        if baseline is None:
            baseline = self.get_latest_baseline(result.group, result.name)

        if baseline is None:
            return {
                "has_baseline": False,
                "ratio": None,
                "severity": "no_baseline",
                "delta_us": None,
                "baseline_timestamp": None,
            }

        ratio = result.relative_change(baseline)
        severity = result.regression_severity(baseline)
        delta_us = result.mean_us - baseline.mean_us

        return {
            "has_baseline": True,
            "ratio": ratio,
            "severity": severity,
            "delta_us": delta_us,
            "baseline_timestamp": baseline.timestamp,
            "baseline_mean_us": baseline.mean_us,
        }


def extract_structural_params(benchmark_name: str) -> dict[str, int | None]:
    """Extract structural parameters from benchmark name.

    Examples:
        "test_benchmark_pop_depth_10" → {"history_len": None, "option_count": None, ...}
        "test_benchmark_refuse_1000_options" → {"option_count": 1000, ...}
        "test_benchmark_horizon_equivalent_k[3]" → {"horizon": 3, ...}

    This is heuristic pattern matching. Better to explicitly pass params,
    but this provides fallback for existing tests.
    """
    import re

    params = {
        "history_len": None,
        "option_count": None,
        "horizon": None,
        "branching": None,
    }

    # Pattern: "depth_10" → history_len or nesting depth
    if match := re.search(r"depth[_-](\d+)", benchmark_name):
        params["history_len"] = int(match.group(1))

    # Pattern: "1000_options" → option_count
    if match := re.search(r"(\d+)[_-]options", benchmark_name):
        params["option_count"] = int(match.group(1))

    # Pattern: "k[3]" or "k=3" → horizon
    if match := re.search(r"k[\[=](\d+)", benchmark_name):
        params["horizon"] = int(match.group(1))

    # Pattern: "100_ops" → history length
    if match := re.search(r"(\d+)[_-]ops", benchmark_name):
        params["history_len"] = int(match.group(1))

    return params


def format_comparison_report(result: BenchmarkResult, comparison: dict[str, Any]) -> str:
    """Format human-readable comparison report.

    Args:
        result: Current benchmark result
        comparison: Output from compare_to_baseline()

    Returns:
        Formatted multi-line report string
    """
    if not comparison["has_baseline"]:
        return (
            f"[{result.group}/{result.name}]\n"
            f"  No baseline available (first run)\n"
            f"  Current: {result.mean_us:.1f}μs (±{result.stddev_us:.1f}μs)\n"
        )

    ratio = comparison["ratio"]
    severity = comparison["severity"]
    delta = comparison["delta_us"]
    baseline_mean = comparison["baseline_mean_us"]

    severity_symbols = {
        "improvement": "✓",
        "stable": "=",
        "regression": "⚠",
        "severe_regression": "✗",
    }
    symbol = severity_symbols.get(severity, "?")

    ratio_pct = (ratio - 1.0) * 100
    sign = "+" if ratio >= 1.0 else ""

    return (
        f"[{result.group}/{result.name}] {symbol}\n"
        f"  Baseline: {baseline_mean:.1f}μs\n"
        f"  Current:  {result.mean_us:.1f}μs (±{result.stddev_us:.1f}μs)\n"
        f"  Change:   {sign}{ratio_pct:+.1f}% ({sign}{delta:+.1f}μs)\n"
        f"  Status:   {severity}\n"
    )


# Default baseline storage location
DEFAULT_BASELINE_DIR = Path(".benchmarks/baselines")


def get_default_store() -> BaselineStore:
    """Get default baseline store instance."""
    return BaselineStore(root_dir=DEFAULT_BASELINE_DIR)
