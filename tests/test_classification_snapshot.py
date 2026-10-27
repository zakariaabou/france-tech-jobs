"""Keep the labeled classification audit reproducible."""

import importlib.util
from pathlib import Path
import unittest


class SnapshotAuditTests(unittest.TestCase):
    def test_snapshot_labels_match(self):
        path = Path(__file__).resolve().parents[1] / "scripts/evaluate_classification.py"
        spec = importlib.util.spec_from_file_location("classification_audit", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        samples, matrix, category_errors = module.evaluate()
        self.assertGreaterEqual(len(samples), 20)
        self.assertFalse(category_errors)
        self.assertFalse([(expected, observed, count) for (expected, observed), count in matrix.items() if expected != observed])
