import unittest
import json
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

from france_tech_jobs.feeds import generate_feeds
from france_tech_jobs.pipeline import update


def job(**overrides):
    item = {
        "source_id": "source-a", "sources": ["source-a"], "job_id": "1",
        "company": "A & B", "title": "Data <Engineer>\x01", "location": "Paris, France",
        "categories": ["data"], "geography": "france", "status": "active",
        "eligible": True, "first_seen": "2026-10-01", "published_at": "",
        "application_url": "https://example.com/job/1?x=1&y=2",
    }
    item.update(overrides)
    return item


class FeedTests(unittest.TestCase):
    def parse(self, jobs, geography="france", category="data"):
        return ET.fromstring(generate_feeds(jobs)[f"feeds/{geography}-{category}.xml"])

    def test_xml_is_valid_escapes_and_omits_unknown_publication_date(self):
        root = self.parse([job()])
        item = root.find("./channel/item")
        self.assertEqual(item.findtext("title"), "Data <Engineer> — A & B")
        self.assertEqual(item.findtext("link"), "https://example.com/job/1?x=1&y=2")
        self.assertIsNone(item.find("pubDate"))
        self.assertIn("source-a", item.findtext("description"))
        self.assertIn("First observed: 2026-10-01", item.findtext("description"))

    def test_known_timestamp_is_converted_to_utc_without_guessing_date_only(self):
        jobs = [job(published_at="2026-10-01T12:30:00+02:00"), job(job_id="2", application_url="https://example.com/2", published_at="2026-10-01")]
        items = self.parse(jobs).findall("./channel/item")
        timestamps = {i.findtext("link"): i.findtext("pubDate") for i in items}
        self.assertEqual(timestamps["https://example.com/job/1?x=1&y=2"], "Thu, 01 Oct 2026 10:30:00 GMT")
        self.assertIsNone(timestamps["https://example.com/2"])

    def test_duplicate_url_has_one_stable_guid_across_source_outage(self):
        first = job()
        duplicate = job(source_id="source-b", sources=["source-b"], job_id="2")
        item = self.parse([first, duplicate]).findall("./channel/item")
        self.assertEqual(len(item), 1)
        self.assertIn("source-a", item[0].findtext("description"))
        self.assertIn("source-b", item[0].findtext("description"))
        same_job = self.parse([duplicate]).find("./channel/item/guid").text
        self.assertEqual(item[0].find("guid").text, same_job)
        self.assertEqual(item[0].find("guid").attrib["isPermaLink"], "false")

    def test_only_active_eligible_jobs_in_correct_category_and_region(self):
        jobs = [job(), job(job_id="2", application_url="https://example.com/2", status="unknown"), job(job_id="3", application_url="https://example.com/3", status="closed"), job(job_id="4", application_url="https://example.com/4", eligible=False), job(job_id="5", application_url="javascript:alert(1)"), job(job_id="6", application_url="https://example.com/6", geography="international")]
        self.assertEqual(len(self.parse(jobs).findall("./channel/item")), 1)
        self.assertEqual(len(self.parse(jobs, "international").findall("./channel/item")), 1)
        self.assertEqual(len(generate_feeds(jobs)), 6)

    def test_pipeline_recovery_keeps_feed_identity_and_never_notifies_closure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config/sources.json").write_text(json.dumps({"sources": [{"id": "source-a"}, {"id": "source-b"}]}), encoding="utf8")
            classifier = lambda *args: {"categories": ["data"], "seniority": "junior", "geography": "france", "eligible": True}
            def good(source):
                return [job()] if source["id"] == "source-a" else []
            def outage(source):
                if source["id"] == "source-a":
                    raise OSError("offline")
                return []
            update(root, "2026-10-01", fetcher=good, classifier=classifier)
            path = root / "feeds/france-data.xml"
            first_guid = ET.fromstring(path.read_text(encoding="utf8")).find("./channel/item/guid").text
            update(root, "2026-10-02", fetcher=outage, classifier=classifier)
            self.assertEqual(ET.fromstring(path.read_text(encoding="utf8")).findall("./channel/item"), [])
            update(root, "2026-10-03", fetcher=good, classifier=classifier)
            restored_guid = ET.fromstring(path.read_text(encoding="utf8")).find("./channel/item/guid").text
            self.assertEqual(first_guid, restored_guid)


if __name__ == "__main__":
    unittest.main()
