"""Check sample provenance and metric behaviour, not a perfect score."""

import importlib.util
import json
from pathlib import Path
import unittest


class HoldoutTest(unittest.TestCase):
    def test_frozen_selection_has_distinct_labels_and_no_development_ids(self):
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location("holdout", root / "scripts/evaluate_holdout.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        selected, matrix, _ = module.evaluate()
        frame = json.loads((root / "evaluation/holdout_frame.json").read_text(encoding="utf8"))
        self.assertEqual(len(selected), 27)
        self.assertEqual(sum(matrix.values()), 27)
        self.assertEqual(len({(row["source_id"], row["job_id"]) for row in selected}), 27)
        self.assertFalse(set(frame["excluded_development_ids"]) & {row["job_id"] for row in selected})
        self.assertIsNone(module.wilson(0, 0))
        lower, upper = module.wilson(1, 1)
        self.assertAlmostEqual(lower, 0.2065, places=3)
        self.assertAlmostEqual(upper, 1.0)
