import tempfile
import unittest
from pathlib import Path

from france_tech_jobs.__main__ import write_summary


class ReportTests(unittest.TestCase):
    def test_partial_failures_appear_in_workflow_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "summary.md"
            write_summary(path, {"successful": ["good"], "failed": ["unavailable"], "active": 2})
            summary = path.read_text(encoding="utf8")
            self.assertIn("Partial source failure", summary)
            self.assertIn("unavailable", summary)
            self.assertIn("2", summary)
