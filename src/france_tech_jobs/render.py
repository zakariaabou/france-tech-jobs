"""Render untrusted listing data as readable GitHub Markdown."""

from datetime import date, timedelta
from html import escape
import re
from urllib.parse import quote, urlsplit

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


def render_all(jobs, updated):
    pages = {}
    for geography, heading in (("france", "France"), ("international", "International")):
        for category, label in _NAMES.items():
            pages[f"jobs/{geography}-{category}.md"] = render_page(jobs, f"{heading}: {label}", updated, category=category, geography=geography)
    pages["jobs/recent.md"] = render_page(jobs, "Recently added", updated, recent=True)
    return pages
