import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from france_tech_jobs.connectors import fetch_source
from france_tech_jobs.pipeline import update


def listing(job_id, name):
    return {"id": str(job_id), "name": name}


def detail(job_id, name="Junior Data Engineer"):
    return {"id": str(job_id), "name": name, "postingUrl": f"https://jobs.smartrecruiters.com/Acme/{job_id}",
            "location": {"fullLocation": "Paris, France"}, "typeOfEmployment": {"label": "Permanent"},
            "jobAd": {"sections": {"qualification": {"text": "2 years of experience"}}}}


class SmartRecruitersBudgetTests(unittest.TestCase):
    def setUp(self):
        self.source = {"id": "sr", "type": "smartrecruiters", "company": "Acme", "board": "Acme",
                       "detail_mode": "target_titles", "coverage": "partial", "max_details": 2}

    def fetch(self, pages, details):
        urls = []
        def get(url, timeout):
            urls.append(url)
            if "?limit=" in url:
                return pages.pop(0)
            return details[url.rsplit("/", 1)[-1]]
        with patch("france_tech_jobs.connectors._json", side_effect=get), patch("time.sleep"):
            records = fetch_source(self.source)
        return records, urls

    def test_fetches_detail_only_for_target_titles_within_budget(self):
        page = {"content": [listing(1, "Junior Data Engineer"), listing(2, "Sales associate"),
                            listing(3, "Software Engineer"), listing(4, "Senior Data Engineer")], "totalFound": 4}
        records, urls = self.fetch([page], {"1": detail(1), "3": detail(3, "Software Engineer")})
        self.assertEqual({r["job_id"] for r in records}, {"1", "3"})
        self.assertEqual(len(urls), 3)
        self.assertIn("2 years", records[0]["description"])
        self.assertEqual(records[0]["contract"], "Permanent")

    def test_budget_limits_number_of_details(self):
        page = {"content": [listing(i, "Data Engineer") for i in range(5)], "totalFound": 5}
        records, urls = self.fetch([page], {str(i): detail(i) for i in range(5)})
        self.assertEqual(len(records), 2)
        self.assertEqual(len(urls), 3)

    def test_budget_rotates_between_days(self):
        from datetime import datetime, timezone
        page = {"content": [listing(i, "Data Engineer") for i in range(4)], "totalFound": 4}
        class Clock:
            current = None
            @classmethod
            def now(cls, tz):
                return cls.current
        with patch("france_tech_jobs.connectors.datetime", Clock):
            Clock.current = datetime(2026, 10, 1, tzinfo=timezone.utc)
            first, _ = self.fetch([page], {str(i): detail(i) for i in range(4)})
            Clock.current = datetime(2026, 10, 2, tzinfo=timezone.utc)
            second, _ = self.fetch([page], {str(i): detail(i) for i in range(4)})
        self.assertEqual(len({r['job_id'] for r in first} | {r['job_id'] for r in second}), 4)

    def test_incomplete_title_duplicate_or_invalid_configuration_fails_safely(self):
        for content in ([{"id": "1"}], [listing(1, "Data Engineer"), listing(1, "Data Engineer")]):
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.fetch([{"content": content, "totalFound": len(content)}], {"1": detail(1)})
        for field, value in (("coverage", "complete"), ("max_details", 0), ("max_details", 101)):
            source = dict(self.source, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                fetch_source(source)

    def test_changed_pagination_and_detail_failure_reject_source(self):
        pages = [{"content": [listing(i, "Sales") for i in range(100)], "totalFound": 101},
                 {"content": [listing(100, "Data Engineer")], "totalFound": 102}]
        with self.assertRaises(ValueError):
            self.fetch(pages, {"100": detail(100)})
        with self.assertRaises(ValueError):
            self.fetch([{"content": [listing(1, "Data Engineer")], "totalFound": 1}], {"1": detail(2)})

    def test_selected_unselected_selected_transition_is_never_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [self.source]}), encoding="utf8")
            for day, title, expected in (("2026-10-01", "Junior Data Engineer", "active"),
                                         ("2026-10-02", "Sales associate", "unknown"),
                                         ("2026-10-03", "Junior Data Engineer", "active")):
                page = {"content": [listing(1, title)], "totalFound": 1}
                def get(url, timeout):
                    return page if "?limit=" in url else detail(1)
                with patch("france_tech_jobs.connectors._json", side_effect=get), patch("time.sleep"):
                    update(root, today=day)
                state = json.loads((root / "data/jobs.json").read_text(encoding="utf8"))[0]
                self.assertEqual(state["status"], expected)
                self.assertEqual(state["first_seen"], "2026-10-01")
                self.assertNotIn("closed_since", state)

    def test_previously_closed_job_that_is_listed_but_skipped_becomes_unknown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [self.source]}), encoding="utf8")
            (root / "data").mkdir()
            old = {"source_id": "sr", "job_id": "1", "company": "Acme", "title": "Junior Data Engineer",
                   "application_url": "https://jobs.smartrecruiters.com/Acme/1", "location": "Paris, France",
                   "categories": ["data"], "status": "closed", "closed_since": "2026-09-30", "first_seen": "2026-09-01"}
            (root / "data/jobs.json").write_text(json.dumps([old]), encoding="utf8")
            page = {"content": [listing(1, "Sales associate")], "totalFound": 1}
            with patch("france_tech_jobs.connectors._json", return_value=page), patch("time.sleep"):
                update(root, today="2026-10-01")
            job = json.loads((root / "data/jobs.json").read_text(encoding="utf8"))[0]
            self.assertEqual(job['status'], 'unknown')
            self.assertEqual(job['first_seen'], '2026-09-01')


if __name__ == "__main__":
    unittest.main()
