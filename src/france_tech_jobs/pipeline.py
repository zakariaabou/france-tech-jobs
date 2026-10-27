"""Track observations without treating source outages as job closures."""

from copy import deepcopy
from datetime import date, datetime, timezone
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit, urlunsplit


def merge_observations(previous, successful, failed, today):
    records = {(j["source_id"], j["job_id"]): deepcopy(j) for j in previous}
    failed = set(failed)
    for job in records.values():
        source = job["source_id"]
        # Older state used last_checked as its only closure timestamp. Capture it
        # before changing status or last_checked; missing/invalid values remain
        # untrusted and are never used to prune the record.
        if job.get("status") == "closed" and "closed_since" not in job:
            job["closed_since"] = job.get("last_checked")
        if source in successful:
            if job.get("status") != "closed" and "closed_since" not in job:
                job["closed_since"] = today
            job["status"] = "closed"
            job["last_checked"] = today
        elif source in failed:
            job["status"] = "unknown"
    for source, observations in successful.items():
        for observation in observations:
            if observation.get("source_id") != source or not observation.get("job_id"):
                raise ValueError(f"Invalid source or job ID in {source}")
            key = (source, observation["job_id"])
            prior = records.get(key, {})
            job = dict(observation)
            job.update(status="active", first_seen=prior.get("first_seen", today), last_seen=today, last_checked=today)
            records[key] = job
    return sorted(records.values(), key=lambda j: (j["source_id"], j["job_id"]))


def retain_records(jobs, today, failed_sources=()):
    """Keep relevant observations and prune confirmed closures after 180 days."""
    today_date = date.fromisoformat(today)
    failed_sources = set(failed_sources)
    retained = []
    for job in jobs:
        # A failed fetch cannot update or reclassify old data, so preserve it.
        if job.get("source_id") in failed_sources:
            retained.append(job)
            continue
        if not set(job.get("categories") or ()).intersection({"data", "ai", "software"}):
            continue
        if job.get("status") == "closed":
            try:
                closed = date.fromisoformat(job.get("closed_since"))
            except (ValueError, TypeError):
                pass  # Never guess an absent or malformed closure date.
            else:
                if (today_date - closed).days >= 180:
                    continue
        retained.append(job)
    return retained


def _url_key(url):
    try:
        parts = urlsplit(url)
        if parts.scheme.lower() not in ("http", "https") or not parts.netloc:
            return None
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), parts.query, ""))
    except ValueError:
        return None


def deduplicate(jobs):
    """Merge only records with the same application URL, preserving source IDs."""
    result, seen = [], {}
    for original in jobs:
        job = deepcopy(original)
        key = _url_key(job.get("application_url", ""))
        if key and key in seen:
            existing = result[seen[key]]
            existing["sources"] = sorted(set(existing["sources"] + [job["source_id"]]))
            existing["categories"] = sorted(set(existing.get("categories", []) + job.get("categories", [])))
        else:
            job["sources"] = [job["source_id"]]
            if key:
                seen[key] = len(result)
            result.append(job)
    return result


def select_review_jobs(jobs, confirmed):
    """Select uncertain active jobs without duplicating confirmed or excluded roles."""
    from .classify import classify

    active = [job for job in jobs if job.get("status") == "active"]
    def excluded(job):
        title_only = classify(job.get("title", ""), "", job.get("location", ""), job.get("contract", ""))
        return job.get("seniority") == "excluded" or title_only["seniority"] == "excluded"

    blocked = {_url_key(job.get("application_url", "")) for job in confirmed}
    blocked.update(_url_key(job.get("application_url", "")) for job in active if excluded(job))
    blocked.discard(None)
    candidates = [job for job in active if not job.get("eligible") and not excluded(job)
                  and bool(set(job.get("categories") or ()) & {"data", "ai", "software"})
                  and (job.get("seniority") == "unknown" or job.get("geography") == "unknown")
                  and _url_key(job.get("application_url", "")) not in blocked]
    return deduplicate(candidates)


def update(root, today=None, fetcher=None, classifier=None):
    """Fetch every configured source, then publish only after a successful fetch."""
    from .classify import classify
    from .connectors import fetch_source
    from .render import render_all

    root = Path(root)
    today = today or datetime.now(timezone.utc).date().isoformat()
    fetcher = fetcher or fetch_source
    classifier = classifier or classify
    config = json.loads((root / "config/sources.json").read_text(encoding="utf8"))
    sources = config["sources"]
    review_limit = config.get("review_limit", 100)
    if type(review_limit) is not int or not 0 <= review_limit <= 1000:
        raise ValueError("review_limit must be an integer between 0 and 1000")
    enabled = [s for s in sources if s.get("enabled", True)]
    ids = [s["id"] for s in enabled]
    if not enabled or len(set(ids)) != len(ids):
        raise ValueError("At least one enabled source with a unique ID is required")
    state_file = root / "data/jobs.json"
    previous = json.loads(state_file.read_text(encoding="utf8")) if state_file.exists() else []
    successful, errors = {}, {}
    for source in enabled:
        source_id = source["id"]
        try:
            records = fetcher(source)
            if not isinstance(records, list):
                raise ValueError("Source returned an invalid job list")
            seen_ids = set()
            for job in records:
                if job.get("source_id") != source_id or not job.get("job_id") or job["job_id"] in seen_ids:
                    raise ValueError("Missing, duplicate or mismatched job ID")
                seen_ids.add(job["job_id"])
                job.update(classifier(job.get("title", ""), job.get("description", ""), job.get("location", ""), job.get("contract", "")))
                # Description is used transiently; avoid republishing full job adverts.
                job.pop("description", None)
            successful[source_id] = records
        except Exception as exc:
            errors[source_id] = f"{type(exc).__name__}: {exc}"
            print(f"Source {source_id} failed: {errors[source_id]}", file=sys.stderr)
    if not successful:
        raise RuntimeError("All sources failed; previous output was retained")
    failed_ids = set(errors) | ({j["source_id"] for j in previous} - set(ids))
    jobs = retain_records(merge_observations(previous, successful, failed_ids, today), today, failed_ids)
    public_jobs = deduplicate([job for job in jobs if job.get("status") == "active" and job.get("eligible")])
    review_jobs = select_review_jobs(jobs, public_jobs)
    outputs = {"data/jobs.json": json.dumps(jobs, ensure_ascii=False, indent=2, sort_keys=True) + "\n", **render_all(public_jobs, today, review_jobs=review_jobs, review_limit=review_limit)}
    for path, content in outputs.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_text(content, encoding="utf8")
        temporary.replace(destination)
    return {"successful": sorted(successful), "failed": sorted(errors), "active": len(public_jobs)}
