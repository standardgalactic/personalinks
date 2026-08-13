from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from spherepop import lab, make_config, parse_sphere
from spherepop.lab import ExperimentSpec, RunResult
from spherepop.serialization import CONFIG_SCHEMA_V1, config_to_dict


def _spec(
    exp_id: str,
    *,
    operations: list[str] | None = None,
    claims: list[str] | None = None,
    expected: list[str] | None = None,
) -> ExperimentSpec:
    return ExperimentSpec(
        id=exp_id,
        slug=f"slug-{exp_id}",
        title=f"title-{exp_id}",
        experiment_class="core",
        proposition=f"prop-{exp_id}",
        c0="(A)",
        omega=["POP"],
        observable="obs",
        invariant="inv",
        failure_condition="fail",
        operations=operations or ["POP"],
        claims=claims or ["claim-a"],
        expected_output_contains=expected or [],
    )


def _run(spec: ExperimentSpec, *, rc: int = 0, stdout: str = "", stderr: str = "") -> RunResult:
    return RunResult(
        spec=spec,
        command=["python", "run.py"],
        returncode=rc,
        stdout=stdout,
        stderr=stderr,
    )


def test_selector_parser_covers_range_errors_and_reverse_order() -> None:
    known = {"01", "02", "03"}
    assert lab._parse_selector("03..01", known) == ["03", "02", "01"]
    with pytest.raises(ValueError, match="Invalid range selector"):
        lab._parse_selector("aa..03", known)
    with pytest.raises(ValueError, match="Unknown experiment id"):
        lab._parse_selector("99", known)


def test_run_result_success_property() -> None:
    spec = _spec("01")
    assert _run(spec, rc=0).success is True
    assert _run(spec, rc=1).success is False


def test_run_experiment_uses_subprocess_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    spec = _spec("07")

    class _Proc:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        return _Proc()

    monkeypatch.setattr(lab.subprocess, "run", fake_run)
    result = lab._run_experiment(spec)
    assert result.spec.id == "07"
    assert result.stdout == "ok"


def test_line_observations_and_verify_run() -> None:
    spec = _spec("01", expected=["needle"])
    run = _run(spec, rc=0, stdout="k: v\nneedle\nother: x\nplain")
    report = lab._verify_run(run)
    assert report["ok"] is True
    assert report["observations"] == {"k": "v", "other": "x"}

    failing = _run(spec, rc=0, stdout="k: v")
    missing_report = lab._verify_run(failing)
    assert missing_report["ok"] is False
    assert missing_report["missing_expected_output"] == ["needle"]


def test_json_io_helpers(tmp_path: Path) -> None:
    path = tmp_path / "a" / "payload.json"
    payload = {"x": 1}
    lab._write_json_file(path, payload)
    assert lab._read_json_file(path) == payload

    bad = tmp_path / "bad.json"
    bad.write_text("{bad", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON file"):
        lab._read_json_file(bad)


def test_extract_config_payload() -> None:
    cfg = make_config(parse_sphere("(A)"), {"A"})
    encoded = json.dumps(config_to_dict(cfg))
    out = f"prefix\nconfig_json:{encoded}\nend"
    extracted = lab._extract_config_payload(out)
    assert extracted is not None
    assert extracted["schema"] == CONFIG_SCHEMA_V1
    assert lab._extract_config_payload("no config line") is None


def test_cmd_list_json_and_text(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    specs = [_spec("01", operations=["POP"]), _spec("02", operations=["BIND"])]
    monkeypatch.setattr(lab, "_load_manifest", lambda: specs)

    code = lab._cmd_list(argparse.Namespace(operation="pop", json=True))
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in payload] == ["01"]

    code = lab._cmd_list(argparse.Namespace(operation=None, json=False))
    assert code == 0
    printed = capsys.readouterr().out
    assert "01 [core] slug-01" in printed
    assert "02 [core] slug-02" in printed


def test_cmd_run_json_and_text(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    specs = [_spec("01"), _spec("02")]
    runs = [
        _run(specs[0], rc=0, stdout="ok-1\n", stderr=""),
        _run(specs[1], rc=1, stdout="ok-2\n", stderr="boom\n"),
    ]
    monkeypatch.setattr(lab, "_load_manifest", lambda: specs)
    monkeypatch.setattr(lab, "_select_experiments", lambda s, selector: s)
    monkeypatch.setattr(
        lab, "_run_experiment", lambda spec: runs[0] if spec.id == "01" else runs[1]
    )

    code = lab._cmd_run(argparse.Namespace(selector=None, json=True))
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in payload] == ["01", "02"]

    code = lab._cmd_run(argparse.Namespace(selector=None, json=False))
    assert code == 1
    printed = capsys.readouterr().out
    assert "=== 01-slug-01 ===" in printed
    assert "--- stderr ---" in printed


def test_cmd_verify_json_and_text(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    specs = [_spec("01"), _spec("02")]
    reports = {
        "01": {"experiment": "01", "slug": "slug-01", "ok": True, "missing_expected_output": []},
        "02": {
            "experiment": "02",
            "slug": "slug-02",
            "ok": False,
            "missing_expected_output": ["needle"],
        },
    }
    monkeypatch.setattr(lab, "_load_manifest", lambda: specs)
    monkeypatch.setattr(lab, "_select_experiments", lambda s, selector: s)
    monkeypatch.setattr(lab, "_run_experiment", lambda spec: _run(spec))
    monkeypatch.setattr(lab, "_verify_run", lambda run: reports[run.spec.id])

    code = lab._cmd_verify(argparse.Namespace(selector=None, json=True))
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed"] == 1

    code = lab._cmd_verify(argparse.Namespace(selector=None, json=False))
    assert code == 1
    printed = capsys.readouterr().out
    assert "[PASS] 01-slug-01" in printed
    assert "[FAIL] 02-slug-02" in printed
    assert "missing: ['needle']" in printed


def test_cmd_compare_success_and_shape_errors(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    left = _spec("01", operations=["POP"], claims=["c1"])
    right = _spec("02", operations=["POP", "BIND"], claims=["c2"])

    monkeypatch.setattr(lab, "_load_manifest", lambda: [left, right])
    monkeypatch.setattr(
        lab,
        "_select_experiments",
        lambda specs, selector: [left, right] if selector == "01,02" else [left],
    )
    monkeypatch.setattr(
        lab,
        "_run_experiment",
        lambda spec: _run(spec, rc=0 if spec.id == "01" else 1, stdout="k: v"),
    )

    with pytest.raises(ValueError, match="exactly two"):
        lab._cmd_compare(argparse.Namespace(left="01", right="03", json=True))

    code = lab._cmd_compare(argparse.Namespace(left="01", right="02", json=True))
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["shared_operations"] == ["POP"]

    code = lab._cmd_compare(argparse.Namespace(left="01", right="02", json=False))
    assert code == 1
    printed = capsys.readouterr().out
    assert "shared claims: (none)" in printed


def test_cmd_theory_map_json_and_text(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    specs = [
        _spec("01", operations=["POP"], claims=["claim-covered"]),
        _spec("02", operations=["BIND"], claims=["claim-covered"]),
    ]
    claims_path = tmp_path / "claims.json"
    claims_path.write_text(
        json.dumps({"claims": [{"id": "claim-covered"}, {"id": "claim-uncovered"}]})
    )

    monkeypatch.setattr(lab, "_load_manifest", lambda: specs)
    monkeypatch.setattr(lab, "THEORY_CLAIMS_PATH", claims_path)

    code = lab._cmd_theory_map(argparse.Namespace(json=True))
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["uncovered_claims"] == ["claim-uncovered"]

    # Cover "(none)" output branch.
    claims_path.write_text(json.dumps({"claims": [{"id": "claim-covered"}]}))
    code = lab._cmd_theory_map(argparse.Namespace(json=False))
    assert code == 0
    printed = capsys.readouterr().out
    assert "Uncovered claims:" in printed
    assert "- (none)" in printed


def test_cmd_export_and_inspect_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = _spec("07")
    run = _run(spec, rc=0, stdout="k: v", stderr="")
    monkeypatch.setattr(lab, "_load_manifest", lambda: [spec])
    monkeypatch.setattr(lab, "_select_experiments", lambda specs, selector: specs)
    monkeypatch.setattr(lab, "_run_experiment", lambda _: run)

    output_path = tmp_path / "artifact.json"
    code = lab._cmd_export(argparse.Namespace(experiment="07", output=str(output_path), json=True))
    assert code == 0
    artifact = json.loads(capsys.readouterr().out)
    assert artifact["schema"] == lab.LAB_RESULT_SCHEMA_V1
    assert output_path.exists()

    with pytest.raises(ValueError, match="exactly one"):
        monkeypatch.setattr(lab, "_select_experiments", lambda specs, selector: [])
        lab._cmd_export(argparse.Namespace(experiment="07", output=str(output_path), json=True))

    cfg = make_config(parse_sphere("(A)"), {"A"})
    cfg_summary_payload = config_to_dict(cfg)
    monkeypatch.setattr(lab, "_read_json_file", lambda _: cfg_summary_payload)
    code = lab._cmd_inspect(argparse.Namespace(path=str(output_path), json=True))
    assert code == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["schema"] == CONFIG_SCHEMA_V1

    artifact_payload = {
        "schema": lab.LAB_RESULT_SCHEMA_V1,
        "experiment": {"id": "07", "slug": "slug-07"},
        "result": {"success": True, "returncode": 0, "stdout": "obs: yes"},
        "config": cfg_summary_payload,
    }
    monkeypatch.setattr(lab, "_read_json_file", lambda _: artifact_payload)
    code = lab._cmd_inspect(argparse.Namespace(path=str(output_path), json=False))
    assert code == 0
    printed = capsys.readouterr().out
    assert "schema: spherepop.lab_result.v1" in printed

    monkeypatch.setattr(lab, "_read_json_file", lambda _: [])
    with pytest.raises(ValueError, match="Top-level JSON payload must be an object"):
        lab._cmd_inspect(argparse.Namespace(path=str(output_path), json=True))

    monkeypatch.setattr(lab, "_read_json_file", lambda _: {"schema": "unknown"})
    with pytest.raises(ValueError, match="Unsupported payload schema"):
        lab._cmd_inspect(argparse.Namespace(path=str(output_path), json=True))


def test_validate_artifact_payload_and_cmd_validate(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg = make_config(parse_sphere("(A)"), {"A"})
    cfg_dict = config_to_dict(cfg)
    cfg_dict["history"] = [{"kind": "POP", "history_index": 9, "path": [], "label": None}]

    payload = {
        "schema": lab.LAB_RESULT_SCHEMA_V1,
        "experiment": {"id": "07"},
        "result": {"success": True},
        "config": cfg_dict,
    }
    structural, semantic = lab._cmd_validate_artifact_payload(payload)
    assert structural == []
    assert semantic

    malformed = {"schema": "bad", "experiment": 1, "result": 2, "config": []}
    structural2, semantic2 = lab._cmd_validate_artifact_payload(malformed)  # type: ignore[arg-type]
    assert structural2
    assert semantic2 == []

    bad_config_payload = {
        "schema": lab.LAB_RESULT_SCHEMA_V1,
        "experiment": {},
        "result": {},
        "config": {"schema": CONFIG_SCHEMA_V1, "sigma": {"kind": "sphere", "items": "bad"}},
    }
    structural3, _ = lab._cmd_validate_artifact_payload(bad_config_payload)
    assert any("Embedded config malformed" in item for item in structural3)

    monkeypatch.setattr(lab, "_read_json_file", lambda _: cfg_dict)
    code = lab._cmd_validate(argparse.Namespace(path="x", json=False))
    assert code == 1
    assert "semantic violations:" in capsys.readouterr().out

    monkeypatch.setattr(lab, "_read_json_file", lambda _: config_to_dict(cfg))
    code = lab._cmd_validate(argparse.Namespace(path="x", json=False))
    assert code == 0
    assert capsys.readouterr().out.strip() == "ok"

    monkeypatch.setattr(lab, "_read_json_file", lambda _: payload)
    code = lab._cmd_validate(argparse.Namespace(path="x", json=True))
    assert code == 1
    report = json.loads(capsys.readouterr().out)
    assert report["schema"] == lab.LAB_RESULT_SCHEMA_V1

    monkeypatch.setattr(lab, "_read_json_file", lambda _: {"schema": "bad"})
    with pytest.raises(ValueError, match="Unsupported payload schema"):
        lab._cmd_validate(argparse.Namespace(path="x", json=True))


def test_cmd_replay_config_and_artifact_paths(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg = make_config(parse_sphere("(A)"), {"A"})
    cfg_dict = config_to_dict(cfg)

    monkeypatch.setattr(lab, "_read_json_file", lambda _: cfg_dict)
    code = lab._cmd_replay(argparse.Namespace(path="x", json=True))
    assert code == 0
    replayed_cfg = json.loads(capsys.readouterr().out)
    assert replayed_cfg["schema"] == CONFIG_SCHEMA_V1

    monkeypatch.setattr(lab, "_read_json_file", lambda _: cfg_dict)
    code = lab._cmd_replay(argparse.Namespace(path="x", json=False))
    assert code == 0
    text = capsys.readouterr().out
    assert "sigma:" in text
    assert "history length:" in text

    spec = _spec("07")
    monkeypatch.setattr(lab, "_load_manifest", lambda: [spec])
    monkeypatch.setattr(lab, "_select_experiments", lambda specs, selector: specs)
    monkeypatch.setattr(
        lab, "_run_experiment", lambda _: _run(spec, rc=1, stdout="run-out", stderr="run-err")
    )
    artifact_payload = {"schema": lab.LAB_RESULT_SCHEMA_V1, "experiment": {"id": "07"}}
    monkeypatch.setattr(lab, "_read_json_file", lambda _: artifact_payload)
    code = lab._cmd_replay(argparse.Namespace(path="x", json=False))
    assert code == 1
    replay_text = capsys.readouterr().out
    assert "run-out" in replay_text
    assert "--- stderr ---" in replay_text

    monkeypatch.setattr(lab, "_read_json_file", lambda _: artifact_payload)
    code = lab._cmd_replay(argparse.Namespace(path="x", json=True))
    assert code == 1
    replay_payload = json.loads(capsys.readouterr().out)
    assert replay_payload["experiment"] == "07"

    monkeypatch.setattr(lab, "_read_json_file", lambda _: [])
    with pytest.raises(ValueError, match="Top-level JSON payload must be an object"):
        lab._cmd_replay(argparse.Namespace(path="x", json=True))

    monkeypatch.setattr(
        lab, "_read_json_file", lambda _: {"schema": lab.LAB_RESULT_SCHEMA_V1, "experiment": []}
    )
    with pytest.raises(ValueError, match="must be an object"):
        lab._cmd_replay(argparse.Namespace(path="x", json=True))

    monkeypatch.setattr(
        lab,
        "_read_json_file",
        lambda _: {"schema": lab.LAB_RESULT_SCHEMA_V1, "experiment": {"id": 7}},
    )
    with pytest.raises(ValueError, match="must be a string"):
        lab._cmd_replay(argparse.Namespace(path="x", json=True))

    monkeypatch.setattr(
        lab,
        "_read_json_file",
        lambda _: {"schema": lab.LAB_RESULT_SCHEMA_V1, "experiment": {"id": "07"}},
    )
    monkeypatch.setattr(lab, "_select_experiments", lambda specs, selector: [])
    with pytest.raises(ValueError, match="unknown or ambiguous"):
        lab._cmd_replay(argparse.Namespace(path="x", json=True))

    monkeypatch.setattr(lab, "_read_json_file", lambda _: {"schema": "unknown"})
    with pytest.raises(ValueError, match="Unsupported payload schema"):
        lab._cmd_replay(argparse.Namespace(path="x", json=True))


def test_build_parser_and_main_error_path(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    parser = lab.build_parser()
    args = parser.parse_args(["list"])
    assert callable(args.handler)
    assert args.command == "list"

    class _FakeParser:
        def parse_args(self, argv: list[str] | None) -> argparse.Namespace:
            def _handler(_args: argparse.Namespace) -> int:
                raise ValueError("boom")

            return argparse.Namespace(handler=_handler)

    monkeypatch.setattr(lab, "build_parser", lambda: _FakeParser())
    code = lab.main(["list"])
    assert code == 2
    assert "error: boom" in capsys.readouterr().err
