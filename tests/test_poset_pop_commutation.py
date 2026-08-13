import importlib.util
import pathlib
import sys
import unittest


def _load_experiment_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "spherepop" / "28-poset-pop-commutation" / "run.py"
    spec = importlib.util.spec_from_file_location("poset_pop_commutation_run", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PosetPopCommutationExperimentTests(unittest.TestCase):
    def test_equal_content_minimals_commute(self):
        mod = _load_experiment_module()
        base = (
            mod.OptionSpace("alpha", frozenset({"x"})),
            mod.OptionSpace("beta", frozenset({"x"})),
            mod.OptionSpace("gamma", frozenset({"x", "y"})),
        )
        left_then_right = mod.pop_sequence(base, ("alpha", "beta"))
        right_then_left = mod.pop_sequence(base, ("beta", "alpha"))
        self.assertEqual(left_then_right, right_then_left)

    def test_nonminimal_pop_still_rejected(self):
        mod = _load_experiment_module()
        base = (
            mod.OptionSpace("alpha", frozenset({"x"})),
            mod.OptionSpace("beta", frozenset({"x"})),
            mod.OptionSpace("gamma", frozenset({"x", "y"})),
        )
        with self.assertRaises(mod.PosetError):
            mod.pop_minimal(base, "gamma")


if __name__ == "__main__":
    unittest.main()
