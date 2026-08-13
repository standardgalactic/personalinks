from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from spherepop import lab, make_config, parse_sphere
from spherepop.serialization import to_json


class LabManifestTests(unittest.TestCase):
    def test_manifest_covers_all_numbered_experiments(self) -> None:
        specs = lab._load_manifest()
        self.assertEqual(len(specs), 29)
        self.assertEqual(specs[0].id, "01")
        self.assertEqual(specs[-1].id, "29")
        for spec in specs:
            self.assertTrue(spec.proposition)
            self.assertTrue(spec.c0)
            self.assertTrue(spec.omega)
            self.assertTrue(spec.observable)
            self.assertTrue(spec.invariant)
            self.assertTrue(spec.failure_condition)

    def test_selector_range_parsing(self) -> None:
        specs = lab._load_manifest()
        selected = lab._select_experiments(specs, "01..03,07")
        self.assertEqual([spec.id for spec in selected], ["01", "02", "03", "07"])


class LabCommandTests(unittest.TestCase):
    def _run_lab(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "spherepop.lab", *args],
            cwd=str(lab.REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )

    def test_run_single_experiment_json(self) -> None:
        proc = self._run_lab("run", "07", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload[0]["id"], "07")
        self.assertIn("confluent extensional view", payload[0]["stdout"])

    def test_verify_subset(self) -> None:
        proc = self._run_lab("verify", "13", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["failed"], 0)

    def test_theory_map_reports_uncovered_claims(self) -> None:
        proc = self._run_lab("theory-map", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertIn("prop:collapse-composition-transitivity", payload["uncovered_claims"])

    def test_export_creates_portable_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_path = Path(tmpdir) / "result.json"
            proc = self._run_lab("export", "07", "--output", str(artifact_path))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "spherepop.lab_result.v1")
            self.assertEqual(payload["experiment"]["id"], "07")
            self.assertIn("observations", payload["result"])

    def test_inspect_artifact_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_path = Path(tmpdir) / "result.json"
            export_proc = self._run_lab("export", "07", "--output", str(artifact_path))
            self.assertEqual(export_proc.returncode, 0, export_proc.stderr)

            inspect_proc = self._run_lab("inspect", str(artifact_path), "--json")
            self.assertEqual(inspect_proc.returncode, 0, inspect_proc.stderr)
            payload = json.loads(inspect_proc.stdout)
            self.assertEqual(payload["schema"], "spherepop.lab_result.v1")
            self.assertEqual(payload["experiment"]["id"], "07")

    def test_validate_config_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cfg.json"
            cfg = make_config(parse_sphere("(A)"), {"A"})
            cfg_path.write_text(to_json(cfg), encoding="utf-8")
            proc = self._run_lab("validate", str(cfg_path), "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["ok"])

    def test_replay_artifact_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_path = Path(tmpdir) / "result.json"
            export_proc = self._run_lab("export", "13", "--output", str(artifact_path))
            self.assertEqual(export_proc.returncode, 0, export_proc.stderr)

            replay_proc = self._run_lab("replay", str(artifact_path), "--json")
            self.assertEqual(replay_proc.returncode, 0, replay_proc.stderr)
            payload = json.loads(replay_proc.stdout)
            self.assertEqual(payload["experiment"], "13")
            self.assertTrue(payload["success"])


if __name__ == "__main__":
    unittest.main()
