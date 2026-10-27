"""Read public employer job-board postings into a common record format.

A source raises on incomplete/invalid responses so callers never interpret a failed
fetch as an empty board. No candidate data or credentials are requested.
"""
import html
from html.parser import HTMLParser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request


class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def _plain(value):
    if not isinstance(value, str):
        return ''
    parser = _TextParser()
    parser.feed(html.unescape(value))
    return ' '.join(' '.join(parser.parts).split())


def _json(url, timeout):
    request = urllib.request.Request(url, headers={'User-Agent': 'FranceTechJobs/1.0 (public careers listing)', 'Accept': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
            delay = 2 ** attempt
            if exc.code == 429:
                try:
                    delay = float(exc.headers.get('Retry-After', '1')) if exc.headers else 1.0
                except (TypeError, ValueError):
                    delay = 1.0
            time.sleep(min(max(delay, 0.0), 10.0))
        except urllib.error.URLError as exc:
            if not isinstance(exc.reason, TimeoutError) or attempt == 2:
                raise
            time.sleep(2 ** attempt)
        except TimeoutError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError('Unreachable retry state')


def _required_record(item, source, title, url):
    if not isinstance(item, dict) or item.get('id') is None or not title or not url:
        raise ValueError(f"Incomplete posting from {source['id']}")
    return {
        'source_id': str(source['id']), 'job_id': str(item['id']),
        'company': str(source['company']), 'title': str(title), 'location': '',
        'description': '', 'contract': '', 'employment_type': '', 'published_at': '',
        'application_url': str(url), 'source_url': str(url), 'remote': '',
    }


def _label(value):
    if isinstance(value, dict):
        return str(value.get('label') or '')
    return str(value or '')


def _employment(value):
    """Keep work schedule distinct from an explicitly stated contract type."""
    value = _label(value).strip()
    if not value:
        return '', ''
    schedule = re.search(r'\b(?:full[ -]?time|part[ -]?time|temps\s+(?:plein|partiel|complet))\b', value, re.I)
    contract = re.search(r'\b(?:cdi|cdd|permanent|fixed[ -]?term|temporary|temporaire|contract|contrat|freelance|internship|alternance|apprenticeship)\b', value, re.I)
    return (value if contract else '', value if schedule else '')


def _greenhouse(source, board, timeout):
    payload = _json(f'https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true', timeout)
    if not isinstance(payload, dict) or not isinstance(payload.get('jobs'), list):
        raise ValueError('Invalid Greenhouse jobs response')
    meta = payload.get('meta', {})
    if not isinstance(meta, dict):
        raise ValueError('Invalid Greenhouse response metadata')
    if 'total' in meta:
        total = meta['total']
        if type(total) is not int or total < 0 or total != len(payload['jobs']):
            raise ValueError('Incomplete Greenhouse jobs response')
    records = []
    for job in payload['jobs']:
        if not isinstance(job, dict):
            raise ValueError('Invalid Greenhouse job')
        url = job.get('absolute_url')
        result = _required_record(job, source, job.get('title'), url)
        result['location'] = (job.get('location') or {}).get('name', '') or ''
        result['description'] = _plain(job.get('content'))
        # Greenhouse updated_at is not a publication date.
        result['published_at'] = job.get('first_published') or ''
        records.append(result)
    return records


def _lever(source, board, timeout):
    region = source.get('region', 'global')
    if region not in ('global', 'eu'):
        raise ValueError('Invalid Lever region')
    host = 'api.eu.lever.co' if region == 'eu' else 'api.lever.co'
    records = []
    for page in range(1000):
        skip = page * 100
        payload = _json(f'https://{host}/v0/postings/{board}?mode=json&skip={skip}&limit=100', timeout)
        if not isinstance(payload, list):
            raise ValueError('Invalid Lever postings response')
        for job in payload:
            if not isinstance(job, dict):
                raise ValueError('Invalid Lever posting')
            url = job.get('hostedUrl') or job.get('applyUrl')
            result = _required_record(job, source, job.get('text'), url)
            categories = job.get('categories') or {}
            if not isinstance(categories, dict):
                raise ValueError('Invalid Lever categories')
            result['location'] = categories.get('location') or ''
            result['contract'], result['employment_type'] = _employment(categories.get('commitment'))
            description = [job.get('descriptionPlain') or _plain(job.get('description'))]
            for section in job.get('lists') or []:
                if isinstance(section, dict):
                    description.append(_plain(section.get('content')))
            description.append(job.get('additionalPlain') or '')
            result['description'] = ' '.join(part for part in description if part)
            result['remote'] = job.get('workplaceType') or ''
            result['application_url'] = job.get('applyUrl') or url
            records.append(result)
        if len(payload) < 100:
            return records
    raise ValueError('Lever page limit exceeded')


def _smartrecruiters(source, board, timeout):
    base = f'https://api.smartrecruiters.com/v1/companies/{board}/postings'
    records = []
    expected_total = None
    for page in range(1000):
        offset = page * 100
        payload = _json(f'{base}?limit=100&offset={offset}', timeout)
        if not isinstance(payload, dict) or not isinstance(payload.get('content'), list):
            raise ValueError('Invalid SmartRecruiters postings response')
        content = payload['content']
        total = payload.get('totalFound')
        if type(total) is not int or total < 0:
            raise ValueError('Invalid SmartRecruiters totalFound')
        if 'offset' in payload and (type(payload['offset']) is not int or payload['offset'] != offset):
            raise ValueError('Invalid SmartRecruiters page offset')
        if expected_total is None:
            expected_total = total
        elif total != expected_total:
            raise ValueError('SmartRecruiters total changed during fetch')
        if len(content) != min(100, max(total - offset, 0)):
            raise ValueError('Incomplete SmartRecruiters page')
        for job in content:
            if not isinstance(job, dict) or not job.get('id'):
                raise ValueError('Invalid SmartRecruiters posting')
            job_id = urllib.parse.quote(str(job['id']), safe='')
            detail = _json(f'{base}/{job_id}', timeout)
            if not isinstance(detail, dict) or str(detail.get('id', '')) != str(job['id']):
                raise ValueError('Invalid SmartRecruiters posting detail')
            url = detail.get('postingUrl') or detail.get('applyUrl')
            result = _required_record(detail, source, detail.get('name'), url)
            location = detail.get('location') or {}
            if not isinstance(location, dict):
                raise ValueError('Invalid SmartRecruiters location')
            result['location'] = location.get('fullLocation') or ', '.join(str(location.get(k) or '') for k in ('city', 'region', 'country') if location.get(k))
            if location.get('hybrid') is True:
                result['remote'] = 'hybrid'
            elif location.get('remote') is True:
                result['remote'] = 'remote'
            result['contract'], result['employment_type'] = _employment(detail.get('typeOfEmployment'))
            for custom in detail.get('customField') or []:
                if isinstance(custom, dict) and str(custom.get('fieldLabel', '')).lower() in ('contract type', 'type de contrat'):
                    contract, schedule = _employment(custom.get('valueLabel'))
                    result['contract'] = contract or result['contract']
                    result['employment_type'] = schedule or result['employment_type']
            sections = (detail.get('jobAd') or {}).get('sections') or {}
            if not isinstance(sections, dict):
                raise ValueError('Invalid SmartRecruiters description')
            result['description'] = ' '.join(_plain(section.get('text')) for section in sections.values() if isinstance(section, dict)).strip()
            result['published_at'] = detail.get('releasedDate') or ''
            result['application_url'] = detail.get('applyUrl') or url
            records.append(result)
            time.sleep(0.1)
        if offset + len(content) >= total:
            return records
        if len(content) < 100:
            raise ValueError('Incomplete SmartRecruiters page')
    raise ValueError('SmartRecruiters page limit exceeded')


def fetch_source(source: dict, timeout: float = 20) -> list[dict]:
    """Fetch all public listings for one configured company or raise on failure."""
    if not isinstance(source, dict) or any(not source.get(k) for k in ('id', 'type', 'company', 'board')):
        raise ValueError('Source requires id, type, company and board')
    if timeout <= 0:
        raise ValueError('Timeout must be positive')
    board = urllib.parse.quote(str(source['board']), safe='')
    handlers = {'greenhouse': _greenhouse, 'lever': _lever, 'smartrecruiters': _smartrecruiters}
    if source['type'] not in handlers:
        raise ValueError(f"Unsupported source type: {source['type']}")
    records = handlers[source['type']](source, board, timeout)
    ids = [item['job_id'] for item in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source job IDs: snapshot may be incomplete')
    return records
