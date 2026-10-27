import json
import tempfile
import unittest
from pathlib import Path

from france_tech_jobs.pipeline import merge_observations, deduplicate, update
from france_tech_jobs.render import render_page


class PipelineTests(unittest.TestCase):
    def job(self, source="one", job_id="1", url="https://example.com/job/1"):
        return {"source_id": source, "job_id": job_id, "company": "Acme", "title": "Junior Data Engineer", "location": "Paris, France", "application_url": url, "categories": ["data"], "seniority": "junior", "geography": "france", "eligible": True}

    def test_failed_source_is_unknown_not_closed(self):
        previous = [dict(self.job(), status="active", first_seen="2026-01-01", last_seen="2026-01-01", last_checked="2026-01-01")]
        result = merge_observations(previous, {}, ["one"], "2026-01-02")
        self.assertEqual(result[0]["status"], "unknown")
        self.assertEqual(result[0]["last_seen"], "2026-01-01")
        self.assertEqual(result[0]["last_checked"], "2026-01-01")

    def test_missing_from_successful_complete_feed_is_closed(self):
        previous = [dict(self.job(), status="active", first_seen="2026-01-01", last_seen="2026-01-01")]
        result = merge_observations(previous, {"one": []}, [], "2026-01-02")
        self.assertEqual(result[0]["status"], "closed")
        self.assertEqual(result[0]["last_checked"], "2026-01-02")

    def test_reappearing_job_retains_first_seen(self):
        previous = [dict(self.job(), status="closed", first_seen="2026-01-01", last_seen="2026-01-01")]
        result = merge_observations(previous, {"one": [self.job()]}, [], "2026-01-03")
        self.assertEqual((result[0]["status"], result[0]["first_seen"], result[0]["last_seen"]), ("active", "2026-01-01", "2026-01-03"))

    def test_duplicate_url_merges_sources_but_similar_jobs_remain(self):
        jobs = [self.job(), self.job("two", "2"), self.job("two", "3", "https://example.com/job/3")]
        result = deduplicate(jobs)
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result[0]["sources"]), {"one", "two"})

    def test_render_escapes_fields_and_excludes_unknown_status(self):
        active = dict(self.job(), company="A | B", status="active")
        stale = dict(self.job("two", "2"), status="unknown")
        page = render_page([active, stale], "France", "2026-01-02", category="data", geography="france")
        self.assertIn(r"A \| B", page)
        self.assertEqual(page.count("Junior Data Engineer"), 1)
        self.assertIn("2026-01-02", page)

    def test_render_escapes_markdown_formatting_in_external_fields(self):
        active = dict(self.job(), title="`Junior *Data* Engineer`", status="active")
        page = render_page([active], "France", "2026-01-02", category="data", geography="france")
        self.assertIn(r"\`Junior \*Data\* Engineer\`", page)

    def test_schedule_is_separate_from_contract(self):
        active = dict(self.job(), contract="", employment_type="Full-time", status="active")
        page = render_page([active], "France", "2026-01-02", category="data", geography="france")
        self.assertIn("| Contract | Schedule |", page)
        self.assertIn("| Unknown | Full-time |", page)

    def test_all_failed_sources_preserve_existing_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [{"id": "one", "enabled": True}]}), encoding="utf8")
            (root / "data").mkdir()
            state = root / "data/jobs.json"
            state.write_text("[]", encoding="utf8")
            def fail(source):
                raise OSError("offline")
            with self.assertRaises(RuntimeError):
                update(root, "2026-01-02", fetcher=fail)
            self.assertEqual(state.read_text(encoding="utf8"), "[]")

    def test_partial_failure_preserves_other_source_and_publishes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [{"id": "one", "enabled": True}, {"id": "two", "enabled": True}]}), encoding="utf8")
            (root / "data").mkdir()
            (root / "data/jobs.json").write_text(json.dumps([dict(self.job("two"), status="active", first_seen="2026-01-01", last_seen="2026-01-01")]), encoding="utf8")
            def fetch(source):
                if source["id"] == "two":
                    raise OSError("offline")
                return [self.job("one")]
            classifier = lambda *args: {"categories": ["data"], "seniority": "junior", "geography": "france", "eligible": True}
            report = update(root, "2026-01-02", fetcher=fetch, classifier=classifier)
            state = json.loads((root / "data/jobs.json").read_text(encoding="utf8"))
            self.assertEqual({j["source_id"]: j["status"] for j in state}, {"one": "active", "two": "unknown"})
            self.assertEqual(report["failed"], ["two"])
            self.assertTrue((root / "jobs/france-data.md").exists())


if __name__ == "__main__":
    unittest.main()
