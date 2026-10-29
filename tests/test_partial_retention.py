import unittest
import json
import tempfile
from pathlib import Path
from france_tech_jobs.pipeline import merge_observations, retain_records, update


class PartialRetentionTests(unittest.TestCase):
    def job(self, id='1', **values):
        return dict(source_id='partial', job_id=id, categories=['data'], status='unknown', **values)

    def test_unknown_age_is_not_a_closure_and_does_not_reset(self):
        old = self.job(first_seen='2025-01-01')
        first = merge_observations([old], {'partial': []}, [], '2026-01-01', {'partial'})
        again = merge_observations(first, {'partial': []}, [], '2026-06-30', {'partial'})
        self.assertEqual(again[0]['unknown_since'], '2026-01-01')
        self.assertEqual(again[0]['status'], 'unknown')
        self.assertEqual(retain_records(again, '2026-06-30', partial_sources={'partial'}), [])
        self.assertEqual(len(retain_records(again, '2026-06-29', partial_sources={'partial'})), 1)

    def test_failed_source_is_preserved_even_beyond_limits(self):
        jobs = [self.job(str(i), unknown_since='2020-01-01') for i in range(1001)]
        self.assertEqual(retain_records(jobs, '2026-01-01', {'partial'}, {'partial'}), jobs)

    def test_unknown_history_is_capped_deterministically(self):
        jobs = [self.job(str(i), unknown_since='invalid') for i in range(1005)]
        kept = retain_records(jobs, '2026-01-01', partial_sources={'partial'})
        self.assertEqual(len(kept), 1000)
        self.assertEqual({j['job_id'] for j in kept}, {j['job_id'] for j in retain_records(list(reversed(jobs)), '2026-01-01', partial_sources={'partial'})})

    def test_recovery_clears_unknown_clock_and_keeps_first_seen(self):
        old = self.job(unknown_since='2026-01-01', first_seen='2025-01-01')
        fresh = dict(old)
        fresh.pop('unknown_since')
        recovered = merge_observations([old], {'partial': [fresh]}, [], '2026-02-01', {'partial'})
        self.assertNotIn('unknown_since', recovered[0])
        self.assertEqual(recovered[0]['first_seen'], '2025-01-01')
        self.assertEqual(recovered[0]['status'], 'active')

    def test_future_and_missing_dates_not_aged_out(self):
        jobs = [self.job('future', unknown_since='2027-01-01'), self.job('missing')]
        self.assertEqual(retain_records(jobs, '2026-01-01', partial_sources={'partial'}), jobs)

    def test_pipeline_eviction_and_later_reappearance_start_new_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'config').mkdir()
            (root / 'data').mkdir()
            (root / 'config/sources.json').write_text(json.dumps({'sources': [{'id': 'partial', 'coverage': 'partial'}]}), encoding='utf8')
            old = self.job(unknown_since='2026-01-01', first_seen='2025-01-01', title='Junior Data Engineer', company='Example', location='Paris, France', application_url='https://example.test/job/1')
            state = root / 'data/jobs.json'
            state.write_text(json.dumps([old]), encoding='utf8')
            update(root, '2026-06-30', fetcher=lambda source: [])
            self.assertEqual(json.loads(state.read_text(encoding='utf8')), [])
            self.assertNotIn('Junior Data Engineer', (root / 'feeds/france-data.xml').read_text(encoding='utf8'))
            fresh = {k: v for k, v in old.items() if k not in ('unknown_since', 'first_seen', 'status')}
            update(root, '2026-07-01', fetcher=lambda source: [fresh])
            recovered = json.loads(state.read_text(encoding='utf8'))[0]
            self.assertEqual(recovered['first_seen'], '2026-07-01')
            self.assertEqual(recovered['status'], 'active')
