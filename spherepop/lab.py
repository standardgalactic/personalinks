from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from spherepop.serialization import CONFIG_SCHEMA_V1, config_from_dict, config_to_dict, to_json
from spherepop.validation import validate_config
from spherepop.views import render_expr


@dataclass(frozen=True)
class ExperimentSpec:
    id: str
    slug: str
    title: str
    experiment_class: str
    proposition: str
    c0: str
    omega: list[str]
    observable: str
    invariant: str
    failure_condition: str
    operations: list[str]
    claims: list[str]
    expected_output_contains: list[str]


@dataclass(frozen=True)
class RunResult:
    spec: ExperimentSpec
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        return self.returncode == 0


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
MANIFEST_PATH = PACKAGE_ROOT / "experiment_manifest.json"
THEORY_CLAIMS_PATH = PACKAGE_ROOT / "theory_claims.json"
LAB_RESULT_SCHEMA_V1 = "spherepop.lab_result.v1"


def _load_manifest() -> list[ExperimentSpec]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    specs: list[ExperimentSpec] = []
    for item in payload["experiments"]:
        specs.append(
            ExperimentSpec(
                id=item["id"],
                slug=item["slug"],
                title=item["title"],
                experiment_class=item["class"],
                proposition=item["proposition"],
                c0=item["c0"],
                omega=list(item["omega"]),
                observable=item["observable"],
                invariant=item["invariant"],
                failure_condition=item["failure_condition"],
                operations=list(item["operations"]),
                claims=list(item["claims"]),
                expected_output_contains=list(item.get("expected_output", {}).get("contains", [])),
            )
        )
    specs.sort(key=lambda spec: spec.id)
    return specs


def _selector_tokens(selector: str) -> list[str]:
    return [token.strip() for token in selector.split(",") if token.strip()]


def _parse_selector(selector: str, known_ids: set[str]) -> list[str]:
    resolved: list[str] = []
    for token in _selector_tokens(selector):
        if ".." in token:
            start, end = token.split("..", 1)
            if not (start.isdigit() and end.isdigit()):
                raise ValueError(f"Invalid range selector: {token}")
            s = int(start)
            e = int(end)
            step = 1 if s <= e else -1
            for value in range(s, e + step, step):
                exp_id = f"{value:02d}"
                if exp_id in known_ids and exp_id not in resolved:
                    resolved.append(exp_id)
            continue
        exp_id = f"{int(token):02d}" if token.isdigit() and len(token) <= 2 else token
        if exp_id not in known_ids:
            raise ValueError(f"Unknown experiment id: {token}")
        if exp_id not in resolved:
            resolved.append(exp_id)
    return resolved


def _select_experiments(specs: list[ExperimentSpec], selector: str | None) -> list[ExperimentSpec]:
    if selector is None:
        return specs
    known = {spec.id for spec in specs}
    ids = _parse_selector(selector, known)
    id_index = {spec.id: spec for spec in specs}
    return [id_index[exp_id] for exp_id in ids]


def _experiment_script(spec: ExperimentSpec) -> Path:
    return PACKAGE_ROOT / f"{spec.id}-{spec.slug}" / "run.py"


def _run_experiment(spec: ExperimentSpec) -> RunResult:
    script = _experiment_script(spec)
    command = [sys.executable, str(script)]
    proc = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        check=False,
    )
    return RunResult(
        spec=spec,
        command=command,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _line_observations(stdout: str) -> dict[str, str]:
    observed: dict[str, str] = {}
    for raw in stdout.splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        observed[key.strip()] = value.strip()
    return observed


def _verify_run(run: RunResult) -> dict[str, object]:
    checks = run.spec.expected_output_contains
    missing = [snippet for snippet in checks if snippet not in run.stdout]
    ok = run.success and not missing
    return {
        "experiment": run.spec.id,
        "slug": run.spec.slug,
        "ok": ok,
        "returncode": run.returncode,
        "missing_expected_output": missing,
        "observations": _line_observations(run.stdout),
        "invariant": run.spec.invariant,
        "failure_condition": run.spec.failure_condition,
    }


def _json_print(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _write_json_file(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _read_json_file(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file '{path}': {exc.msg}") from exc


def _extract_config_payload(stdout: str) -> dict[str, object] | None:
    """Extract optional embedded Config JSON from experiment stdout.

    Convention: experiments may emit a line prefixed by `config_json:`.
    """
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line.startswith("config_json:"):
            continue
        _, json_payload = line.split(":", 1)
        cfg = config_from_dict(json.loads(json_payload.strip()))
        return config_to_dict(cfg)
    return None


def _lab_artifact(spec: ExperimentSpec, run: RunResult) -> dict[str, object]:
    config_payload = _extract_config_payload(run.stdout)
    return {
        "schema": LAB_RESULT_SCHEMA_V1,
        "generated_at": datetime.now(UTC).isoformat(),
        "experiment": {
            "id": spec.id,
            "slug": spec.slug,
            "title": spec.title,
            "class": spec.experiment_class,
            "proposition": spec.proposition,
            "operations": spec.operations,
            "claims": spec.claims,
        },
        "result": {
            "success": run.success,
            "returncode": run.returncode,
            "command": run.command,
            "stdout": run.stdout,
            "stderr": run.stderr,
            "observations": _line_observations(run.stdout),
        },
        "config_schema": CONFIG_SCHEMA_V1,
        "config": config_payload,
    }


def _cmd_list(args: argparse.Namespace) -> int:
    specs = _load_manifest()
    if args.operation:
        op = args.operation.upper()
        specs = [spec for spec in specs if op in spec.operations]
    payload = [
        {
            "id": spec.id,
            "slug": spec.slug,
            "class": spec.experiment_class,
            "title": spec.title,
            "operations": spec.operations,
            "claims": spec.claims,
        }
        for spec in specs
    ]
    if args.json:
        _json_print(payload)
        return 0
    for item in payload:
        ops = ",".join(item["operations"])
        print(f"{item['id']} [{item['class']}] {item['slug']} :: {item['title']} :: ops={ops}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    specs = _select_experiments(_load_manifest(), args.selector)
    runs = [_run_experiment(spec) for spec in specs]
    payload = [
        {
            "id": run.spec.id,
            "slug": run.spec.slug,
            "success": run.success,
            "returncode": run.returncode,
            "stdout": run.stdout,
            "stderr": run.stderr,
        }
        for run in runs
    ]
    if args.json:
        _json_print(payload)
    else:
        for run in runs:
            print(f"=== {run.spec.id}-{run.spec.slug} ===")
            print(run.stdout.rstrip())
            if run.stderr.strip():
                print("--- stderr ---")
                print(run.stderr.rstrip())
    return 0 if all(run.success for run in runs) else 1


def _cmd_verify(args: argparse.Namespace) -> int:
    specs = _select_experiments(_load_manifest(), args.selector)
    reports = [_verify_run(_run_experiment(spec)) for spec in specs]
    passed = sum(1 for report in reports if report["ok"])
    payload = {
        "total": len(reports),
        "passed": passed,
        "failed": len(reports) - passed,
        "reports": reports,
    }
    if args.json:
        _json_print(payload)
    else:
        for report in reports:
            status = "PASS" if report["ok"] else "FAIL"
            print(f"[{status}] {report['experiment']}-{report['slug']}")
            if report["missing_expected_output"]:
                print(f"  missing: {report['missing_expected_output']}")
        print(f"summary: {passed}/{len(reports)} passed")
    return 0 if payload["failed"] == 0 else 1


def _cmd_compare(args: argparse.Namespace) -> int:
    specs = _load_manifest()
    selected = _select_experiments(specs, f"{args.left},{args.right}")
    if len(selected) != 2:
        raise ValueError("compare expects exactly two experiment ids")
    left, right = selected
    run_left = _run_experiment(left)
    run_right = _run_experiment(right)
    payload = {
        "left": {
            "id": left.id,
            "slug": left.slug,
            "proposition": left.proposition,
            "operations": left.operations,
            "claims": left.claims,
            "observations": _line_observations(run_left.stdout),
            "success": run_left.success,
        },
        "right": {
            "id": right.id,
            "slug": right.slug,
            "proposition": right.proposition,
            "operations": right.operations,
            "claims": right.claims,
            "observations": _line_observations(run_right.stdout),
            "success": run_right.success,
        },
        "shared_operations": sorted(set(left.operations) & set(right.operations)),
        "shared_claims": sorted(set(left.claims) & set(right.claims)),
    }
    if args.json:
        _json_print(payload)
    else:
        print(f"left : {left.id}-{left.slug} :: {left.proposition}")
        print(f"right: {right.id}-{right.slug} :: {right.proposition}")
        print(f"shared operations: {', '.join(payload['shared_operations']) or '(none)'}")
        print(f"shared claims: {', '.join(payload['shared_claims']) or '(none)'}")
    return 0 if run_left.success and run_right.success else 1


def _cmd_theory_map(args: argparse.Namespace) -> int:
    specs = _load_manifest()
    operations = ["POP", "REFUSE", "BIND", "COLLAPSE", "HISTORY", "REPLAY", "OBSERVER"]
    rows: list[dict[str, object]] = []
    for spec in specs:
        rows.append(
            {
                "id": spec.id,
                "slug": spec.slug,
                **{op: ("✓" if op in spec.operations else "·") for op in operations},
            }
        )

    claims_payload = json.loads(THEORY_CLAIMS_PATH.read_text(encoding="utf-8"))
    claim_to_experiments: dict[str, list[str]] = {
        claim["id"]: [] for claim in claims_payload["claims"]
    }
    for spec in specs:
        for claim in spec.claims:
            claim_to_experiments.setdefault(claim, []).append(spec.id)

    uncovered = [claim_id for claim_id, ids in claim_to_experiments.items() if not ids]
    payload = {
        "operations": operations,
        "matrix": rows,
        "claim_coverage": claim_to_experiments,
        "uncovered_claims": uncovered,
    }
    if args.json:
        _json_print(payload)
        return 0

    header = "ID  " + "  ".join(f"{op[:4]:<4}" for op in operations) + "  slug"
    print(header)
    for row in rows:
        cols = "  ".join(f"{row[op]:<4}" for op in operations)
        print(f"{row['id']}  {cols}  {row['slug']}")
    print("\nUncovered claims:")
    if uncovered:
        for claim in uncovered:
            print(f"- {claim}")
    else:
        print("- (none)")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    specs = _select_experiments(_load_manifest(), args.experiment)
    if len(specs) != 1:
        raise ValueError("export expects exactly one experiment id")
    spec = specs[0]
    run = _run_experiment(spec)
    artifact = _lab_artifact(spec, run)
    output_path = Path(args.output)
    _write_json_file(output_path, artifact)
    if args.json:
        _json_print(artifact)
    else:
        print(f"exported {spec.id}-{spec.slug} → {output_path}")
        print(f"schema: {LAB_RESULT_SCHEMA_V1}")
    return 0 if run.success else 1


def _cmd_inspect(args: argparse.Namespace) -> int:
    payload = _read_json_file(Path(args.path))
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON payload must be an object")

    schema = payload.get("schema")
    if schema == CONFIG_SCHEMA_V1:
        cfg = config_from_dict(payload)
        summary = {
            "schema": CONFIG_SCHEMA_V1,
            "history_length": len(cfg.history),
            "option_space_size": len(cfg.option_space),
            "sigma": render_expr(cfg.sigma),
        }
    elif schema == LAB_RESULT_SCHEMA_V1:
        experiment = payload.get("experiment")
        result = payload.get("result")
        if not isinstance(experiment, dict) or not isinstance(result, dict):
            raise ValueError("Artifact must contain object fields 'experiment' and 'result'")
        config_payload = payload.get("config")
        config_summary: dict[str, object] | None = None
        if isinstance(config_payload, dict):
            cfg = config_from_dict(config_payload)
            config_summary = {
                "history_length": len(cfg.history),
                "option_space_size": len(cfg.option_space),
                "sigma": render_expr(cfg.sigma),
            }
        summary = {
            "schema": LAB_RESULT_SCHEMA_V1,
            "experiment": {"id": experiment.get("id"), "slug": experiment.get("slug")},
            "success": result.get("success"),
            "returncode": result.get("returncode"),
            "observation_keys": sorted(_line_observations(str(result.get("stdout", ""))).keys()),
            "has_config": isinstance(config_payload, dict),
            "config": config_summary,
        }
    else:
        raise ValueError(f"Unsupported payload schema: {schema!r}")

    if args.json:
        _json_print(summary)
    else:
        for key, value in summary.items():
            print(f"{key}: {value}")
    return 0


def _cmd_validate_artifact_payload(payload: dict[str, object]) -> tuple[list[str], list[str]]:
    structural_errors: list[str] = []
    semantic_violations: list[str] = []

    if payload.get("schema") != LAB_RESULT_SCHEMA_V1:
        structural_errors.append(f"Artifact schema must be '{LAB_RESULT_SCHEMA_V1}'")

    experiment = payload.get("experiment")
    result = payload.get("result")
    if not isinstance(experiment, dict):
        structural_errors.append("Artifact field 'experiment' must be an object")
    if not isinstance(result, dict):
        structural_errors.append("Artifact field 'result' must be an object")

    config_payload = payload.get("config")
    if config_payload is not None:
        if not isinstance(config_payload, dict):
            structural_errors.append("Artifact field 'config' must be an object or null")
        else:
            try:
                cfg = config_from_dict(config_payload)
            except ValueError as exc:
                structural_errors.append(f"Embedded config malformed: {exc}")
            else:
                semantic_violations.extend(validate_config(cfg))

    return structural_errors, semantic_violations


def _cmd_validate(args: argparse.Namespace) -> int:
    payload = _read_json_file(Path(args.path))
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON payload must be an object")

    schema = payload.get("schema")
    if schema == CONFIG_SCHEMA_V1:
        cfg = config_from_dict(payload)
        structural_errors: list[str] = []
        semantic_violations = validate_config(cfg)
    elif schema == LAB_RESULT_SCHEMA_V1:
        structural_errors, semantic_violations = _cmd_validate_artifact_payload(payload)
    else:
        raise ValueError(f"Unsupported payload schema: {schema!r}")

    report = {
        "schema": schema,
        "structural_errors": structural_errors,
        "semantic_violations": semantic_violations,
        "ok": not structural_errors and not semantic_violations,
    }

    if args.json:
        _json_print(report)
    else:
        if structural_errors:
            print("structural errors:")
            for item in structural_errors:
                print(f"- {item}")
        if semantic_violations:
            print("semantic violations:")
            for item in semantic_violations:
                print(f"- {item}")
        if not structural_errors and not semantic_violations:
            print("ok")

    return 0 if report["ok"] else 1


def _cmd_replay(args: argparse.Namespace) -> int:
    payload = _read_json_file(Path(args.path))
    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON payload must be an object")

    schema = payload.get("schema")
    if schema == CONFIG_SCHEMA_V1:
        cfg = config_from_dict(payload)
        if args.json:
            print(to_json(cfg))
        else:
            print(f"sigma: {render_expr(cfg.sigma)}")
            print(f"history length: {len(cfg.history)}")
            print(f"option space size: {len(cfg.option_space)}")
        return 0

    if schema == LAB_RESULT_SCHEMA_V1:
        experiment = payload.get("experiment")
        if not isinstance(experiment, dict):
            raise ValueError("Artifact field 'experiment' must be an object")
        exp_id = experiment.get("id")
        if not isinstance(exp_id, str):
            raise ValueError("Artifact experiment id must be a string")
        specs = _select_experiments(_load_manifest(), exp_id)
        if len(specs) != 1:
            raise ValueError("Artifact references unknown or ambiguous experiment id")
        run = _run_experiment(specs[0])
        replay_payload = {
            "experiment": exp_id,
            "success": run.success,
            "returncode": run.returncode,
            "stdout": run.stdout,
            "stderr": run.stderr,
            "observations": _line_observations(run.stdout),
        }
        if args.json:
            _json_print(replay_payload)
        else:
            print(run.stdout.rstrip())
            if run.stderr.strip():
                print("--- stderr ---")
                print(run.stderr.rstrip())
        return 0 if run.success else 1

    raise ValueError(f"Unsupported payload schema: {schema!r}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m spherepop.lab", description="Spherepop experiment laboratory runner"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List experiments from manifest")
    list_cmd.add_argument("--operation", help="Filter by operation tag, e.g. COLLAPSE")
    list_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    list_cmd.set_defaults(handler=_cmd_list)

    run_cmd = sub.add_parser("run", help="Run one or many experiments")
    run_cmd.add_argument("selector", nargs="?", help="Examples: 07, 01..29, 03,07,10")
    run_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    run_cmd.set_defaults(handler=_cmd_run)

    verify_cmd = sub.add_parser("verify", help="Run experiments and assert manifest invariants")
    verify_cmd.add_argument("selector", nargs="?", help="Examples: 07, 01..29, 03,07,10")
    verify_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    verify_cmd.set_defaults(handler=_cmd_verify)

    compare_cmd = sub.add_parser("compare", help="Compare two experiments")
    compare_cmd.add_argument("left", help="Left experiment id")
    compare_cmd.add_argument("right", help="Right experiment id")
    compare_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    compare_cmd.set_defaults(handler=_cmd_compare)

    map_cmd = sub.add_parser("theory-map", help="Generate operation/claim coverage map")
    map_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    map_cmd.set_defaults(handler=_cmd_theory_map)

    export_cmd = sub.add_parser("export", help="Export one experiment result as portable artifact")
    export_cmd.add_argument("experiment", help="Experiment id, e.g. 07")
    export_cmd.add_argument("--output", required=True, help="Output JSON artifact path")
    export_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    export_cmd.set_defaults(handler=_cmd_export)

    inspect_cmd = sub.add_parser("inspect", help="Inspect a Config/artifact JSON file")
    inspect_cmd.add_argument("path", help="Path to JSON file")
    inspect_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    inspect_cmd.set_defaults(handler=_cmd_inspect)

    validate_cmd = sub.add_parser("validate", help="Validate structure and semantics of JSON file")
    validate_cmd.add_argument("path", help="Path to JSON file")
    validate_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    validate_cmd.set_defaults(handler=_cmd_validate)

    replay_cmd = sub.add_parser("replay", help="Replay a Config/artifact JSON file")
    replay_cmd.add_argument("path", help="Path to JSON file")
    replay_cmd.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    replay_cmd.set_defaults(handler=_cmd_replay)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
