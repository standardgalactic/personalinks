from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from math import exp, log
from statistics import mean, pstdev

EPSILON = 0.05
TIME_STEPS = 80
STARVATION_LIMIT = 12


@dataclass
class ScopeState:
    name: str
    horizon: int
    cost: float
    gain: float
    initial_gain: float
    last_touched: int = -1
    history_events: int = 0
    pop_count: int = 0
    bind_count: int = 0
    refuse_count: int = 0
    collapse_count: int = 0
    local_saturation_steps: int = 0
    active_saturation_start: int | None = None
    recovery_latencies: list[int] = field(default_factory=list)
    gains_over_time: list[float] = field(default_factory=list)


@dataclass(frozen=True)
class CandidateAction:
    scope_index: int
    action: str
    emcg: float
    ratio: float


def make_initial_scopes() -> list[ScopeState]:
    # Horizons are intentionally heterogeneous: minute/day/week/month/year scale proxies.
    base = [
        ("daily-review", 1, 1.0, 0.85),
        ("code-experiment", 3, 1.4, 1.00),
        ("language-seed", 8, 1.1, 0.75),
        ("math-lemma", 21, 1.8, 0.95),
        ("book-manuscript", 55, 2.2, 0.90),
    ]
    return [ScopeState(name=n, horizon=h, cost=c, gain=g, initial_gain=g) for n, h, c, g in base]


def scope_readiness(scope: ScopeState) -> float:
    return min(1.0, scope.history_events / max(1, scope.horizon))


def gaussian_bump(readiness: float, center: float, width: float) -> float:
    return exp(-(((readiness - center) / width) ** 2))


def action_multiplier(action: str, scope: ScopeState) -> float:
    readiness = scope_readiness(scope)
    if action == "BIND":
        # Early-stage shaping dominates; value gradually declines as scope matures.
        return 1.00 - 0.35 * readiness
    if action == "REFUSE":
        # Mid-readiness exclusion window: after initial shaping but before final resolution.
        return 0.40 + 0.15 * readiness + 0.55 * gaussian_bump(readiness, center=0.45, width=0.16)
    if action == "COLLAPSE":
        # Later-readiness compression window: merge distinctions before POP-heavy closure.
        return 0.32 + 0.20 * readiness + 0.60 * gaussian_bump(readiness, center=0.78, width=0.14)
    # POP value rises as local preparatory work accumulates.
    return max(0.25, 0.22 + 0.90 * readiness)


def all_candidates(scopes: Sequence[ScopeState]) -> list[CandidateAction]:
    actions = ["BIND", "REFUSE", "COLLAPSE", "POP"]
    out: list[CandidateAction] = []
    for i, scope in enumerate(scopes):
        for action in actions:
            emcg = max(0.0, scope.gain * action_multiplier(action, scope))
            out.append(CandidateAction(i, action, emcg, emcg / scope.cost))
    return out


def choose_novelty_only(scopes: Sequence[ScopeState], t: int) -> CandidateAction:
    candidates = all_candidates(scopes)

    def novelty_key(c: CandidateAction) -> tuple[int, float]:
        scope = scopes[c.scope_index]
        age = t - scope.last_touched if scope.last_touched >= 0 else t + 1
        return (age, c.emcg)

    best = max(candidates, key=novelty_key)
    return max((c for c in candidates if c.scope_index == best.scope_index), key=lambda c: c.emcg)


def choose_shortest_task_first(scopes: Sequence[ScopeState], _: int) -> CandidateAction:
    min_h = min(scope.horizon for scope in scopes)
    candidates = [c for c in all_candidates(scopes) if scopes[c.scope_index].horizon == min_h]
    return max(candidates, key=lambda c: c.emcg)


def choose_max_emcg(scopes: Sequence[ScopeState], _: int) -> CandidateAction:
    return max(all_candidates(scopes), key=lambda c: c.emcg)


def choose_ratio_antistarvation(scopes: Sequence[ScopeState], t: int) -> CandidateAction:
    candidates = all_candidates(scopes)
    slow_horizon_cutoff = sorted(s.horizon for s in scopes)[-2]
    slow_indices = [i for i, s in enumerate(scopes) if s.horizon >= slow_horizon_cutoff]
    starved = []
    for i in slow_indices:
        scope = scopes[i]
        idle = t - scope.last_touched if scope.last_touched >= 0 else t + 1
        if idle > STARVATION_LIMIT:
            starved.append(i)
    if starved:
        forced = [c for c in candidates if c.scope_index in starved]
        return max(forced, key=lambda c: c.ratio)
    return max(candidates, key=lambda c: c.ratio)


def apply_action(scopes: list[ScopeState], action: CandidateAction, t: int) -> None:
    active = scopes[action.scope_index]
    active.history_events += 1
    active.last_touched = t
    if action.action == "POP":
        active.pop_count += 1
    elif action.action == "BIND":
        active.bind_count += 1
    elif action.action == "REFUSE":
        active.refuse_count += 1
    else:
        active.collapse_count += 1

    # Work on a scope tends to flatten immediate marginal gain (local saturation pressure).
    active.gain = max(0.0, active.gain * 0.72)

    # Untouched scopes recover over time; cross-scope work can also renormalize them.
    for j, scope in enumerate(scopes):
        if j == action.scope_index:
            continue
        horizon_gap = abs(scope.horizon - active.horizon)
        cross_term = 0.012 * log(1.0 + horizon_gap)
        passive_recovery = 0.02 + 0.0009 * scope.horizon
        scope.gain = min(scope.initial_gain * 1.20, scope.gain + passive_recovery + cross_term)


def update_saturation_bookkeeping(scopes: list[ScopeState], t: int) -> None:
    for scope in scopes:
        local_max = max(
            scope.gain * action_multiplier(a, scope) for a in ["BIND", "REFUSE", "COLLAPSE", "POP"]
        )
        scope.gains_over_time.append(local_max)
        if local_max <= EPSILON:
            scope.local_saturation_steps += 1
            if scope.active_saturation_start is None:
                scope.active_saturation_start = t
        else:
            if scope.active_saturation_start is not None:
                scope.recovery_latencies.append(t - scope.active_saturation_start)
                scope.active_saturation_start = None


def field_saturated(scopes: Sequence[ScopeState]) -> bool:
    return max(c.emcg for c in all_candidates(scopes)) <= EPSILON


def simulate(
    policy_name: str, chooser: Callable[[Sequence[ScopeState], int], CandidateAction]
) -> dict[str, object]:
    scopes = make_initial_scopes()
    field_saturation_steps = 0

    for t in range(TIME_STEPS):
        update_saturation_bookkeeping(scopes, t)
        if field_saturated(scopes):
            field_saturation_steps += 1
        choice = chooser(scopes, t)
        apply_action(scopes, choice, t)

    # close any open saturation episodes at horizon end
    for scope in scopes:
        if scope.active_saturation_start is not None:
            scope.recovery_latencies.append(TIME_STEPS - scope.active_saturation_start)
            scope.active_saturation_start = None

    slow_horizon_cutoff = sorted(s.horizon for s in scopes)[-2]
    slow_scopes = [s for s in scopes if s.horizon >= slow_horizon_cutoff]
    starved_slow = 0
    for scope in slow_scopes:
        expected_min = TIME_STEPS / max(1, scope.horizon)
        if scope.history_events < max(2, int(0.5 * expected_min)):
            starved_slow += 1

    all_gains = [g for scope in scopes for g in scope.gains_over_time]
    stability = 0.0
    if all_gains:
        m = mean(all_gains)
        stability = 0.0 if m == 0 else 1.0 - (pstdev(all_gains) / m)

    return {
        "policy": policy_name,
        "time_to_first_local_saturation": min(
            (
                next((i for i, g in enumerate(scope.gains_over_time) if g <= EPSILON), TIME_STEPS)
                for scope in scopes
            ),
            default=TIME_STEPS,
        ),
        "time_in_field_saturation": field_saturation_steps,
        "mean_recovery_latency_after_switch": round(
            mean([lat for s in scopes for lat in s.recovery_latencies]), 3
        )
        if any(s.recovery_latencies for s in scopes)
        else None,
        "long_horizon_starvation_rate": round(starved_slow / max(1, len(slow_scopes)), 3),
        "compression_progress_stability": round(stability, 3),
        "scope_stats": [
            {
                "scope": s.name,
                "horizon": s.horizon,
                "history_events": s.history_events,
                "pop": s.pop_count,
                "bind": s.bind_count,
                "refuse": s.refuse_count,
                "collapse": s.collapse_count,
                "local_saturation_steps": s.local_saturation_steps,
                "recoveries": len(s.recovery_latencies),
            }
            for s in scopes
        ],
    }


def render_report(results: Iterable[dict[str, object]]) -> None:
    print("POLICY SUMMARY")
    print("=" * 80)
    for result in results:
        print(f"policy: {result['policy']}")
        print(f"  time_to_first_local_saturation: {result['time_to_first_local_saturation']}")
        print(f"  time_in_field_saturation:       {result['time_in_field_saturation']}")
        print(f"  mean_recovery_latency:          {result['mean_recovery_latency_after_switch']}")
        print(f"  long_horizon_starvation_rate:   {result['long_horizon_starvation_rate']}")
        print(f"  compression_progress_stability: {result['compression_progress_stability']}")
        print("  per-scope:")
        for scope in result["scope_stats"]:
            print(
                "    "
                f"{scope['scope']} (tau={scope['horizon']}): "
                f"events={scope['history_events']}, "
                f"POP={scope['pop']}, BIND={scope['bind']}, REFUSE={scope['refuse']}, COLLAPSE={scope['collapse']}, "
                f"sat_steps={scope['local_saturation_steps']}, recoveries={scope['recoveries']}"
            )
        print("-" * 80)


if __name__ == "__main__":
    policies: list[tuple[str, Callable[[Sequence[ScopeState], int], CandidateAction]]] = [
        ("novelty_only", choose_novelty_only),
        ("shortest_task_first", choose_shortest_task_first),
        ("max_emcg", choose_max_emcg),
        ("emcg_over_cost_antistarvation", choose_ratio_antistarvation),
    ]
    outputs = [simulate(name, chooser) for name, chooser in policies]
    render_report(outputs)
