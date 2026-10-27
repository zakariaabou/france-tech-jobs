import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from france_tech_jobs.connectors import fetch_source


def response(value):
    return io.BytesIO(json.dumps(value).encode('utf-8'))


class ConnectorTests(unittest.TestCase):
    def test_smartrecruiters_links_to_posting_when_apply_redirect_exists(self):
        source = {'id': 'acme-sr', 'type': 'smartrecruiters', 'company': 'Acme', 'board': 'Acme'}
        listing = {'content': [{'id': '1'}], 'totalFound': 1}
        detail = {'id': '1', 'name': 'Data Engineer', 'location': {'fullLocation': 'Paris, France'}, 'postingUrl': 'https://jobs.smartrecruiters.com/Acme/1-job', 'applyUrl': 'https://jobs.smartrecruiters.com/Acme/1-job?oga=true'}
        with patch('urllib.request.urlopen', side_effect=[response(listing), response(detail)]), patch('time.sleep'):
            result = fetch_source(source)
        self.assertEqual(result[0]['application_url'], 'https://jobs.smartrecruiters.com/Acme/1-job')

    def test_greenhouse_maps_published_job(self):
        source = {'id': 'acme-gh', 'type': 'greenhouse', 'company': 'Acme', 'board': 'acme'}
        payload = {'jobs': [{'id': 2, 'title': 'Data Engineer', 'location': {'name': 'Paris, France'}, 'absolute_url': 'https://example.com/job/2', 'updated_at': '2026-10-01T00:00:00Z', 'content': '<p>Build pipelines</p>'}]}
        with patch('urllib.request.urlopen', return_value=response(payload)) as request:
            result = fetch_source(source)
        self.assertEqual(result[0]['job_id'], '2')
        self.assertEqual(result[0]['source_id'], 'acme-gh')
        self.assertEqual(result[0]['location'], 'Paris, France')
        self.assertEqual(result[0]['application_url'], 'https://example.com/job/2')
        self.assertIn('Build pipelines', result[0]['description'])
        self.assertEqual(result[0]['published_at'], '')  # updated_at is not posted date
        self.assertIn('content=true', request.call_args.args[0].full_url)

    def test_lever_maps_plain_description_and_pagination(self):
        source = {'id': 'acme-lv', 'type': 'lever', 'company': 'Acme', 'board': 'acme'}
        first = [{'id': str(i), 'text': 'Software Engineer', 'categories': {'location': 'Paris, France', 'commitment': 'Full-time'}, 'descriptionPlain': 'Python role', 'hostedUrl': f'https://jobs.lever.co/acme/{i}', 'workplaceType': 'hybrid'} for i in range(100)]
        with patch('urllib.request.urlopen', side_effect=[response(first), response([])]) as request:
            result = fetch_source(source)
        self.assertEqual(len(result), 100)
        self.assertEqual(result[0]['contract'], '')
        self.assertEqual(result[0]['employment_type'], 'Full-time')
        self.assertEqual(result[0]['remote'], 'hybrid')
        self.assertEqual(result[0]['description'], 'Python role')
        self.assertIn('skip=100', request.call_args.args[0].full_url)

    def test_smartrecruiters_fetches_detail_and_paginates(self):
        source = {'id': 'acme-sr', 'type': 'smartrecruiters', 'company': 'Acme', 'board': 'Acme'}
        jobs = [{'id': str(i)} for i in range(100)]
        detail = lambda i: {'id': str(i), 'name': 'ML Engineer', 'location': {'fullLocation': 'Paris, France', 'hybrid': True}, 'postingUrl': f'https://jobs.smartrecruiters.com/Acme/{i}', 'releasedDate': '2026-10-20', 'jobAd': {'sections': {'jobDescription': {'text': '<p>ML</p>'}, 'qualifications': {'text': 'Python'}}}, 'typeOfEmployment': {'label': 'Permanent'}}
        results = [response({'content': jobs, 'totalFound': 101})] + [response(detail(i)) for i in range(100)] + [response({'content': [{'id': '100'}], 'totalFound': 101}), response(detail(100))]
        with patch('urllib.request.urlopen', side_effect=results), patch('time.sleep'):
            result = fetch_source(source)
        self.assertEqual(len(result), 101)
        self.assertEqual(result[-1]['job_id'], '100')
        self.assertEqual(result[0]['remote'], 'hybrid')
        self.assertIn('Python', result[0]['description'])
        self.assertEqual(result[0]['location'], 'Paris, France')
        self.assertEqual(result[0]['contract'], 'Permanent')

    def test_malformed_response_fails_instead_of_silently_removing_jobs(self):
        source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}
        with patch('urllib.request.urlopen', return_value=response({'unexpected': []})):
            with self.assertRaises(ValueError):
                fetch_source(source)

    def test_network_error_is_visible_to_orchestrator(self):
        source = {'id': 'a', 'type': 'lever', 'company': 'A', 'board': 'a'}
        error = HTTPError('https://example.com', 503, 'service down', None, None)
        with patch('urllib.request.urlopen', side_effect=error), patch('time.sleep'):
            with self.assertRaises(HTTPError):
                fetch_source(source)

    def test_unknown_source_type_is_rejected(self):
        with self.assertRaises(ValueError):
            fetch_source({'id': 'a', 'type': 'unknown', 'company': 'A', 'board': 'a'})


if __name__ == '__main__':
    unittest.main()

class ConnectorDateAndRateLimitTests(unittest.TestCase):
    def test_rate_limit_is_retried_then_returns_jobs(self):
        source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}
        error = HTTPError('https://example.com', 429, 'rate limited', {'Retry-After': '1'}, None)
        with patch('urllib.request.urlopen', side_effect=[error, response({'jobs': []})]), patch('time.sleep') as sleep:
            self.assertEqual(fetch_source(source), [])
        sleep.assert_called_once_with(1.0)

    def test_duplicate_job_ids_reject_incomplete_source_snapshot(self):
        source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}
        job = {'id': 1, 'title': 'Engineer', 'absolute_url': 'https://example.com'}
        with patch('urllib.request.urlopen', return_value=response({'jobs': [job, job]})):
            with self.assertRaises(ValueError):
                fetch_source(source)

class ConnectorCompletenessTests(unittest.TestCase):
    def test_greenhouse_rejects_truncated_job_list(self):
        source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}
        with patch('urllib.request.urlopen', return_value=response({'jobs': [], 'meta': {'total': 3}})):
            with self.assertRaises(ValueError):
                fetch_source(source)

    def test_greenhouse_rejects_malformed_total(self):
        source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}
        with patch('urllib.request.urlopen', return_value=response({'jobs': [], 'meta': {'total': '0'}})):
            with self.assertRaises(ValueError):
                fetch_source(source)

    def test_smartrecruiters_rejects_inconsistent_page_count(self):
        source = {'id': 'a', 'type': 'smartrecruiters', 'company': 'A', 'board': 'a'}
        item = {'id': '1', 'name': 'Engineer', 'postingUrl': 'https://example.com'}
        with patch('urllib.request.urlopen', side_effect=[response({'content': [{'id': '1'}], 'totalFound': 0}), response(item)]), patch('time.sleep'):
            with self.assertRaises(ValueError):
                fetch_source(source)

    def test_smartrecruiters_rejects_wrong_reported_offset(self):
        source = {'id': 'a', 'type': 'smartrecruiters', 'company': 'A', 'board': 'a'}
        with patch('urllib.request.urlopen', return_value=response({'content': [], 'totalFound': 0, 'offset': 100})):
            with self.assertRaises(ValueError):
                fetch_source(source)

class EmploymentTypeTests(unittest.TestCase):
    def test_smartrecruiters_full_time_is_schedule_and_cdi_is_contract(self):
        source = {'id': 'a', 'type': 'smartrecruiters', 'company': 'A', 'board': 'a'}
        detail = {'id': '1', 'name': 'Engineer', 'postingUrl': 'https://example.com', 'typeOfEmployment': {'label': 'Full-time'}, 'customField': [{'fieldLabel': 'Type de contrat', 'valueLabel': 'CDI'}]}
        with patch('urllib.request.urlopen', side_effect=[response({'content': [{'id': '1'}], 'totalFound': 1}), response(detail)]), patch('time.sleep'):
            job = fetch_source(source)[0]
        self.assertEqual(job['employment_type'], 'Full-time')
        self.assertEqual(job['contract'], 'CDI')

    def test_smartrecruiters_full_time_does_not_imply_contract(self):
        source = {'id': 'a', 'type': 'smartrecruiters', 'company': 'A', 'board': 'a'}
        detail = {'id': '1', 'name': 'Engineer', 'postingUrl': 'https://example.com', 'typeOfEmployment': {'label': 'Full-time'}}
        with patch('urllib.request.urlopen', side_effect=[response({'content': [{'id': '1'}], 'totalFound': 1}), response(detail)]), patch('time.sleep'):
            job = fetch_source(source)[0]
        self.assertEqual(job['employment_type'], 'Full-time')
        self.assertEqual(job['contract'], '')

    def test_lever_full_time_is_schedule_not_contract(self):
        source = {'id': 'a', 'type': 'lever', 'company': 'A', 'board': 'a'}
        item = {'id': '1', 'text': 'Engineer', 'hostedUrl': 'https://example.com', 'categories': {'commitment': 'Full-time'}}
        with patch('urllib.request.urlopen', return_value=response([item])):
            job = fetch_source(source)[0]
        self.assertEqual(job['employment_type'], 'Full-time')
        self.assertEqual(job['contract'], '')

    def test_lever_cdi_is_contract_not_schedule(self):
        source = {'id': 'a', 'type': 'lever', 'company': 'A', 'board': 'a'}
        item = {'id': '1', 'text': 'Engineer', 'hostedUrl': 'https://example.com', 'categories': {'commitment': 'CDI'}}
        with patch('urllib.request.urlopen', return_value=response([item])):
            job = fetch_source(source)[0]
        self.assertEqual(job['contract'], 'CDI')
        self.assertEqual(job['employment_type'], '')

class ConnectorTransientRetryTests(unittest.TestCase):
    def setUp(self):
        self.source = {'id': 'a', 'type': 'greenhouse', 'company': 'A', 'board': 'a'}

    def test_timeout_then_success_retries_with_backoff(self):
        with patch('urllib.request.urlopen', side_effect=[TimeoutError('read timed out'), response({'jobs': []})]) as request, patch('time.sleep') as sleep:
            self.assertEqual(fetch_source(self.source), [])
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_urlerror_timeout_then_success_is_retried(self):
        from urllib.error import URLError
        with patch('urllib.request.urlopen', side_effect=[URLError(TimeoutError('timed out')), response({'jobs': []})]) as request, patch('time.sleep'):
            self.assertEqual(fetch_source(self.source), [])
        self.assertEqual(request.call_count, 2)

    def test_transient_http_failure_recovers_after_backoff(self):
        for code in (500, 502, 503, 504):
            with self.subTest(code=code):
                error = HTTPError('https://example.com', code, 'server error', None, None)
                with patch('urllib.request.urlopen', side_effect=[error, response({'jobs': []})]) as request, patch('time.sleep'):
                    self.assertEqual(fetch_source(self.source), [])
                self.assertEqual(request.call_count, 2)

    def test_exhausted_timeout_reraises_after_three_attempts(self):
        with patch('urllib.request.urlopen', side_effect=TimeoutError('read timed out')) as request, patch('time.sleep') as sleep:
            with self.assertRaises(TimeoutError):
                fetch_source(self.source)
        self.assertEqual(request.call_count, 3)
        self.assertEqual([x.args[0] for x in sleep.call_args_list], [1, 2])

    def test_permanent_http_error_is_not_retried(self):
        error = HTTPError('https://example.com', 404, 'not found', None, None)
        with patch('urllib.request.urlopen', side_effect=error) as request, patch('time.sleep') as sleep:
            with self.assertRaises(HTTPError):
                fetch_source(self.source)
        self.assertEqual(request.call_count, 1)
        sleep.assert_not_called()

    def test_non_timeout_urlerror_is_not_retried(self):
        from urllib.error import URLError
        error = URLError('name resolution failed')
        with patch('urllib.request.urlopen', side_effect=error) as request, patch('time.sleep') as sleep:
            with self.assertRaises(URLError):
                fetch_source(self.source)
        self.assertEqual(request.call_count, 1)
        sleep.assert_not_called()
