import unittest
from unittest.mock import patch
from io import BytesIO

from france_tech_jobs.bpce import _read_json, fetch_bpce
from france_tech_jobs.connectors import fetch_source


class BPCEConnectorTests(unittest.TestCase):
    def metadata(self, count=1, modified="2026-10-28T12:00:00+00:00"):
        return {"metas": {"default": {"records_count": count, "data_processed": modified}}}

    def job(self, **changes):
        result = {"referencenumber": "123", "title": "Data Engineer", "url": "https://recrutement.bpce.fr/job/data-engineer", "organization": "BPCE IT", "city": "Paris", "country": "France", "state": "Ile-de-France", "description": "2 ans d'expérience", "jobtype": "CDI", "email_recruteur_principal": "private@example.test"}
        result.update(changes)
        return result

    def run_fetch(self, entries, before=None, after=None):
        before = before or self.metadata(len(entries))
        after = after or before
        with patch("france_tech_jobs.bpce._read_json", side_effect=[before, entries, after]):
            return fetch_bpce({"id": "bpce"}, now="2026-10-28T15:00:00+00:00")

    def test_maps_and_omits_personal_data(self):
        record = self.run_fetch([self.job()])[0]
        self.assertEqual(record["company"], "BPCE IT")
        self.assertIn("France", record["location"])
        self.assertEqual(record["contract"], "CDI")
        self.assertEqual(record["source_url"], record["application_url"])
        self.assertNotIn("private@example.test", repr(record))
        self.assertEqual(record["published_at"], "")

    def test_duplicate_locations_are_merged(self):
        records = self.run_fetch([self.job(), self.job(city="Lyon")])
        self.assertEqual(len(records), 1)
        self.assertIn("Paris", records[0]["location"])
        self.assertIn("Lyon", records[0]["location"])

    def test_rejects_stale_incomplete_or_changing_export(self):
        for before, after in [(self.metadata(2), self.metadata(2)), (self.metadata(1, "2026-10-20T12:00:00+00:00"), None), (self.metadata(1), self.metadata(1, "2026-10-28T13:00:00+00:00"))]:
            with self.subTest(before=before, after=after), self.assertRaises(ValueError):
                self.run_fetch([self.job()], before, after)

    def test_rejects_invalid_urls_and_incomplete_records(self):
        for job in (self.job(url="https://example.com/job/123"), self.job(referencenumber=""), self.job(title="")):
            with self.subTest(job=job), self.assertRaises(ValueError):
                self.run_fetch([job])

    def test_dispatches_without_employer_board_identifier(self):
        source = {"id": "bpce", "type": "bpce", "company": "Groupe BPCE"}
        with patch("france_tech_jobs.bpce.fetch_bpce", return_value=[]) as fetch:
            self.assertEqual(fetch_source(source), [])
        fetch.assert_called_once_with(source, timeout=20)

    def test_rejects_oversized_and_truncated_downloads(self):
        class Response(BytesIO):
            headers = {"Content-Length": "20"}

        for body, limit in ((b"[]", 10), (b"[123456789]", 5)):
            with self.subTest(body=body), patch("france_tech_jobs.bpce.urlopen", return_value=Response(body)):
                with self.assertRaises(ValueError):
                    _read_json("https://example.test", limit, 1)


if __name__ == "__main__":
    unittest.main()
