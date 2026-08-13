import importlib.util
import pathlib
import sys
import unittest


def _load_experiment_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "spherepop" / "29-multi-timescale-continuation" / "run.py"
    spec = importlib.util.spec_from_file_location("multi_timescale_run", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MultiTimescaleContinuationTests(unittest.TestCase):
    def test_refuse_and_collapse_are_reachable(self):
        mod = _load_experiment_module()
        policies = [
            ("novelty_only", mod.choose_novelty_only),
            ("shortest_task_first", mod.choose_shortest_task_first),
            ("max_emcg", mod.choose_max_emcg),
            ("emcg_over_cost_antistarvation", mod.choose_ratio_antistarvation),
        ]
        outputs = [mod.simulate(name, chooser) for name, chooser in policies]

        total_refuse = sum(scope["refuse"] for out in outputs for scope in out["scope_stats"])
        total_collapse = sum(scope["collapse"] for out in outputs for scope in out["scope_stats"])

        self.assertGreater(total_refuse, 0)
        self.assertGreater(total_collapse, 0)


if __name__ == "__main__":
    unittest.main()
