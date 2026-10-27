import json
import tempfile
import unittest
from pathlib import Path

from france_tech_jobs.pipeline import merge_observations, deduplicate, retain_records, update
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

    def test_closure_date_survives_later_checks_and_outage(self):
        previous = [dict(self.job(), status="active", first_seen="2025-01-01", last_seen="2026-01-01")]
        closed = merge_observations(previous, {"one": []}, [], "2026-01-02")
        self.assertEqual(closed[0]["closed_since"], "2026-01-02")
        checked_again = merge_observations(closed, {"one": []}, [], "2026-03-01")
        self.assertEqual(checked_again[0]["closed_since"], "2026-01-02")
        self.assertEqual(checked_again[0]["last_checked"], "2026-03-01")
        outage = merge_observations(checked_again, {}, ["one"], "2026-03-02")
        self.assertEqual(outage[0]["status"], "unknown")
        recovered = merge_observations(outage, {"one": []}, [], "2026-03-03")
        self.assertEqual(recovered[0]["closed_since"], "2026-01-02")
        reopened = merge_observations(recovered, {"one": [self.job()]}, [], "2026-03-04")
        self.assertNotIn("closed_since", reopened[0])

    def test_retention_keeps_relevant_and_unknown_but_prunes_old_closures(self):
        jobs = [
            dict(self.job(job_id="active"), status="active", last_checked="2025-01-01"),
            dict(self.job(job_id="unknown"), status="unknown", closed_since="2025-01-01"),
            dict(self.job(job_id="recent"), status="closed", closed_since="2026-01-02"),
            dict(self.job(job_id="old"), status="closed", closed_since="2026-01-01"),
            dict(self.job(job_id="invalid"), status="closed", closed_since="not-a-date"),
            dict(self.job(job_id="missing"), status="closed"),
            dict(self.job(job_id="unrelated"), status="active", categories=[]),
            dict(self.job(job_id="review"), status="active", seniority="unknown", eligible=False),
        ]
        retained = retain_records(jobs, "2026-06-30")
        self.assertEqual({j["job_id"] for j in retained}, {"active", "unknown", "recent", "invalid", "missing", "review"})

    def test_legacy_closed_records_use_valid_last_checked_conservatively(self):
        old = dict(self.job(job_id="old"), status="closed", last_checked="2025-01-01")
        invalid = dict(self.job(job_id="invalid"), status="closed", last_checked="bad")
        missing = dict(self.job(job_id="missing"), status="closed")
        checked = merge_observations([old, invalid, missing], {"one": []}, [], "2026-06-30")
        self.assertEqual({j["job_id"] for j in retain_records(checked, "2026-06-30")}, {"invalid", "missing"})

    def test_prior_non_target_from_failed_source_is_preserved(self):
        unrelated = dict(self.job("broken", "unrelated"), status="unknown", categories=[])
        self.assertEqual(retain_records([unrelated], "2026-06-30", failed_sources={"broken"}), [unrelated])
        self.assertEqual(retain_records([unrelated], "2026-06-30"), [])

    def test_update_discards_non_target_from_successful_source_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [{"id": "one"}, {"id": "broken"}]}), encoding="utf8")
            (root / "data").mkdir()
            old = dict(self.job("broken", "prior"), categories=[], status="active")
            (root / "data/jobs.json").write_text(json.dumps([old]), encoding="utf8")
            def fetch(source):
                if source["id"] == "broken":
                    raise OSError("offline")
                return [self.job("one", "target"), dict(self.job("one", "other"), title="Sales associate")]
            def classifier(title, *args):
                relevant = title != "Sales associate"
                return {"categories": ["data"] if relevant else [], "seniority": "junior", "geography": "france", "eligible": relevant}
            update(root, "2026-06-30", fetcher=fetch, classifier=classifier)
            state = json.loads((root / "data/jobs.json").read_text(encoding="utf8"))
            self.assertEqual({j["job_id"] for j in state}, {"target", "prior"})
            self.assertEqual(next(j for j in state if j["job_id"] == "prior")["status"], "unknown")

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
