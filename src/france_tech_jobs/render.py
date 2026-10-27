"""Render untrusted listing data as readable GitHub Markdown."""

from datetime import date, timedelta
from html import escape
import re
from urllib.parse import quote, urlsplit

from .classify import classify

_NAMES = {"data": "Data Engineering", "ai": "AI Engineering", "software": "Software Engineering"}


def _cell(value):
    text = str(value or "Unknown").replace("\r", " ").replace("\n", " ")
    return re.sub(r"([\\`*_{}\[\]~|])", r"\\\1", escape(text, quote=False))


def _link(url):
    try:
        parsed = urlsplit(url or "")
        if parsed.scheme.lower() not in ("https", "http") or not parsed.netloc:
            return "Unavailable"
        return "[Apply](" + quote(url, safe=":/?#@!$&'*+,;=%-._~") + ")"
    except ValueError:
        return "Unavailable"


def render_page(jobs, title, updated, category=None, geography=None, recent=False):
    lines = [f"# {_cell(title)}", "", f"Last pipeline run: {updated} (UTC). Only currently confirmed listings are shown.", "", "[Home](../README.md)", "", "| Company | Role | Location | Experience | Contract | Schedule | Work mode | Posted | Apply |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    cutoff = (date.fromisoformat(updated) - timedelta(days=7)).isoformat()
    selected = [j for j in jobs if j.get("status") == "active" and j.get("eligible") and (not category or category in j.get("categories", [])) and (not geography or j.get("geography") == geography) and (not recent or j.get("first_seen", "") >= cutoff)]
    selected.sort(key=lambda j: (j.get("first_seen", ""), j.get("company", ""), j.get("title", "")), reverse=True)
    for job in selected:
        fields = [job.get("company"), job.get("title"), job.get("location"), job.get("seniority"), job.get("contract"), job.get("employment_type"), job.get("remote"), (job.get("published_at") or "")[:10]]
        lines.append("| " + " | ".join([*map(_cell, fields), _link(job.get("application_url"))]) + " |")
    if not selected:
        lines.extend(["", "No matching jobs are currently available."])
    lines.append("")
    return "\n".join(lines)


def render_review_page(jobs, updated, limit=100, region=None):
    """Render uncertain, currently active candidates without assigning missing facts."""
    selected = []
    for job in jobs:
        seniority = job.get("seniority") or "unknown"
        geography = job.get("geography") or "unknown"
        if region and geography != region:
            continue
        if job.get("status") != "active" or job.get("eligible") or seniority not in {"unknown", "junior", "junior-mid", "mid"}:
            continue
        if not set(job.get("categories") or []).intersection(_NAMES):
            continue
        if seniority != "unknown" and geography != "unknown":
            continue
        # Guard against inconsistent inputs with an explicit senior/intern title or contract.
        if classify(job.get("title") or "", "", job.get("location") or "", job.get("contract") or "")["seniority"] == "excluded":
            continue
        selected.append(job)

    # Newest candidates first within a France-first, international, unknown order.
    selected.sort(key=lambda job: (job.get("first_seen") or "", job.get("company") or "", job.get("title") or ""), reverse=True)
    selected.sort(key=lambda job: {"france": 0, "international": 1}.get(job.get("geography"), 2))
    shown = selected[:max(0, limit)]
    scope = "France appears first, followed by international and unknown locations." if not region else f"Region: {region}."
    lines = [
        "# Potential matches — verify requirements", "",
        f"Last pipeline run: {updated} (UTC). These active listings require review; eligibility and work authorization are not confirmed.", "",
        f"Showing {len(shown)} of {len(selected)} candidates (limit: {max(0, limit)}). {scope}", "",
        "[Home](../README.md)", "",
        "[All](review.md) · [France](review-france.md) · [International](review-international.md) · [Location unknown](review-unknown.md)", "",
        "| Company | Role | Categories | Location | Experience | Review reason | Sources | Apply |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for job in shown:
        reasons = []
        if (job.get("seniority") or "unknown") == "unknown":
            reasons.append("Experience level not confirmed")
        if (job.get("geography") or "unknown") == "unknown":
            reasons.append("Location not confirmed")
        categories = ", ".join(_NAMES[name] for name in _NAMES if name in (job.get("categories") or []))
        sources = ", ".join(str(source) for source in (job.get("sources") or [job.get("source_id")]) if source)
        fields = [job.get("company"), job.get("title"), categories, job.get("location"), job.get("seniority"), "; ".join(reasons), sources]
        lines.append("| " + " | ".join([*map(_cell, fields), _link(job.get("application_url"))]) + " |")
    if not shown:
        lines.extend(["", "No potential matches currently need review."])
    lines.append("")
    return "\n".join(lines)


def render_all(jobs, updated, review_jobs=None, review_limit=100):
    pages = {}
    for geography, heading in (("france", "France"), ("international", "International")):
        for category, label in _NAMES.items():
            pages[f"jobs/{geography}-{category}.md"] = render_page(jobs, f"{heading}: {label}", updated, category=category, geography=geography)
    pages["jobs/recent.md"] = render_page(jobs, "Recently added", updated, recent=True)
    pages["jobs/review.md"] = render_review_page(review_jobs or [], updated, limit=review_limit)
    for region in ("france", "international", "unknown"):
        pages[f"jobs/review-{region}.md"] = render_review_page(review_jobs or [], updated, limit=review_limit, region=region)
    return pages
