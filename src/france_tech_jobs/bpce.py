"""Consume BPCE's open-data snapshot without storing recruiter contact details."""

from datetime import datetime, timedelta, timezone
import hashlib
import json
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

_BASE = "https://bpce.opendatasoft.com/api/explore/v2.1/catalog/datasets/groupe-bpce-offres-emploi"
_MAX_EXPORT = 25 * 1024 * 1024


def _read_json(url, limit, timeout):
    request = Request(url, headers={"User-Agent": "FranceTechJobs/1.0 (open data reader)", "Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        body = response.read(limit + 1)
        if len(body) > limit:
            raise ValueError("BPCE response exceeds size limit")
        length = response.headers.get("Content-Length")
        if length and int(length) != len(body):
            raise ValueError("Incomplete BPCE response")
    return json.loads(body)


def _metadata(payload, now):
    try:
        meta = payload["metas"]["default"]
        count = meta["records_count"]
        processed = datetime.fromisoformat(meta["data_processed"].replace("Z", "+00:00"))
    except (KeyError, AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Invalid BPCE metadata") from exc
    if type(count) is not int or not 0 < count <= 20000 or processed.utcoffset() is None:
        raise ValueError("Invalid BPCE metadata")
    if not now - timedelta(hours=48) <= processed <= now + timedelta(minutes=10):
        raise ValueError("BPCE data is stale or has a future timestamp")
    return count, processed


def fetch_bpce(source, timeout=60, now=None):
    """Fetch one bounded export bracketed by fresh, consistent metadata."""
    instant = datetime.fromisoformat(now) if now else datetime.now(timezone.utc)
    before = _metadata(_read_json(_BASE, 1024 * 1024, timeout), instant)
    entries = _read_json(_BASE + "/exports/json", _MAX_EXPORT, timeout)
    after = _metadata(_read_json(_BASE, 1024 * 1024, timeout), instant)
    if before != after or not isinstance(entries, list) or len(entries) != before[0]:
        raise ValueError("Incomplete or changing BPCE snapshot")
    groups = {}
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("Invalid BPCE job")
        ref, title, url, company = (item.get(key) for key in ("referencenumber", "title", "url", "organization"))
        if not all(isinstance(v, str) and v.strip() for v in (ref, title, url, company)):
            raise ValueError("Incomplete BPCE job")
        parts = urlsplit(url)
        if parts.scheme != "https" or parts.netloc != "recrutement.bpce.fr" or not parts.path.startswith("/job/"):
            raise ValueError("Invalid BPCE job URL")
        key = (ref, url)
        location = ", ".join(str(item.get(k) or "").strip() for k in ("city", "state", "country") if item.get(k))
        if key not in groups:
            identifier = hashlib.sha256((ref + "\n" + url).encode("utf8")).hexdigest()
            groups[key] = {"source_id": source["id"], "job_id": identifier, "company": company, "title": title,
                           "location": location, "description": item.get("description") or "", "contract": item.get("jobtype") or "",
                           "employment_type": "", "published_at": "", "application_url": url, "source_url": url,
                           "remote": item.get("teletravail") or ""}
        else:
            record = groups[key]
            if any((record["title"] != title, record["company"] != company, record["contract"] != (item.get("jobtype") or ""))):
                raise ValueError("Conflicting BPCE duplicate")
            if location and location not in record["location"].split(" | "):
                record["location"] += " | " + location
    return list(groups.values())
