"""Generate stable, source-attributed RSS feeds for active eligible jobs."""

from datetime import datetime, timezone
from email.utils import format_datetime
import hashlib
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET


_NAMES = {"data": "Data Engineering", "ai": "AI Engineering", "software": "Software Engineering"}
_REPO = "https://github.com/zakariaabou/france-tech-jobs"


def _clean(value):
    """Drop XML 1.0 forbidden code points from untrusted source text."""
    return "".join(c for c in str(value or "") if ord(c) in (9, 10, 13) or 0x20 <= ord(c) <= 0xD7FF or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF)


def _url(value):
    try:
        parts = urlsplit(_clean(value).strip())
        if parts.scheme.lower() not in ("https", "http") or not parts.netloc:
            return None
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), parts.query, ""))
    except ValueError:
        return None


def _publication_date(value):
    """Use only timestamps that include both a time and explicit time zone."""
    if not isinstance(value, str) or not any(separator in value for separator in ("T", " ")):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            return None
        return format_datetime(parsed.astimezone(timezone.utc), usegmt=True)
    except (ValueError, OverflowError):
        return None


def _rss(jobs, geography, category):
    root = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(root, "channel")
    label = "France" if geography == "france" else "International"
    ET.SubElement(channel, "title").text = f"France Tech Jobs: {label} — {_NAMES[category]}"
    ET.SubElement(channel, "link").text = f"{_REPO}/blob/main/jobs/{geography}-{category}.md"
    ET.SubElement(channel, "description").text = "Confirmed active junior and mid-level opportunities; verify details with the employer."

    by_url = {}
    for job in jobs:
        if job.get("status") != "active" or not job.get("eligible") or job.get("geography") != geography or category not in (job.get("categories") or []):
            continue
        url = _url(job.get("application_url"))
        if not url:
            continue
        sources = {_clean(s) for s in (job.get("sources") or [job.get("source_id")]) if s}
        if url in by_url:
            by_url[url][1].update(sources)
        else:
            by_url[url] = (job, sources)
    ordered = sorted(by_url.items(), key=lambda entry: (str(entry[1][0].get("first_seen") or ""), entry[0]), reverse=True)
    for url, (job, sources) in ordered:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"{_clean(job.get('title')) or 'Unknown role'} — {_clean(job.get('company')) or 'Unknown company'}"
        ET.SubElement(item, "link").text = url
        digest = hashlib.sha256(url.encode("utf8")).hexdigest()
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = "urn:sha256:" + digest
        description = [f"Location: {_clean(job.get('location')) or 'Unknown'}", f"Sources: {', '.join(sorted(sources)) or 'Unknown'}"]
        if job.get("first_seen"):
            description.append(f"First observed: {_clean(job['first_seen'])}")
        ET.SubElement(item, "description").text = " | ".join(description)
        posted = _publication_date(job.get("published_at"))
        if posted:
            ET.SubElement(item, "pubDate").text = posted
    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf8") + "\n"


def generate_feeds(jobs):
    """Return six RSS documents, grouped by geography and job category."""
    return {f"feeds/{region}-{category}.xml": _rss(jobs, region, category)
            for region in ("france", "international") for category in _NAMES}
