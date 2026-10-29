"""Freeze a new audit frame and an UNLABELLED review queue; never infer labels."""

from pathlib import Path
import hashlib
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from france_tech_jobs.connectors import _json
from evaluate_holdout import select


def main():
    destination = ROOT / "evaluation/independent_audit_frame.json"
    if destination.exists():
        raise SystemExit("Frozen frame already exists; do not overwrite an audit sample")
    sources = [("sia", "Sia"), ("scalian", "Scalian"), ("iliad-free", "Iliad-Free"), ("magellan", "Magellan")]
    prior = json.loads((ROOT / "evaluation/holdout_frame.json").read_text(encoding="utf8"))
    excluded = {str(row["job_id"]) for row in prior["rows"]}
    rows = []
    for source_id, board in sources:
        total = None
        seen = set()
        for offset in range(0, 5000, 100):
            payload = _json(f"https://api.smartrecruiters.com/v1/companies/{board}/postings?limit=100&offset={offset}", 20)
            current = payload["totalFound"]
            if total is not None and total != current:
                raise ValueError("Moving snapshot; retry capture later")
            total = current
            content = payload["content"]
            if len(content) != min(100, max(total-offset, 0)):
                raise ValueError("Truncated listing")
            for item in content:
                identifier = str(item["id"])
                if identifier in seen:
                    raise ValueError("Duplicate listing ID")
                seen.add(identifier)
                if identifier in excluded:
                    continue
                title = item["name"]
                lower = title.casefold()
                role = "data" if re.search(r"data|donn[eé]es|analytics", lower) else "ai" if re.search(r"\b(?:ai|ia|ml|nlp)\b|machine learning|mlops|intelligence artificielle", lower) else "software" if re.search(r"software|logiciel|engineer|ing[eé]nieur|d[eé]veloppe|developer", lower) else "other"
                location = (item.get("location") or {}).get("fullLocation") or ""
                rows.append({"source_id": source_id, "board": board, "job_id": identifier, "title": title,
                             "location": location, "contract": "", "role_bucket": role,
                             "geography_bucket": "france_marker" if re.search(r"\bFrance\b", location, re.I) else "other_or_unknown"})
            time.sleep(0.2)
            if offset + len(content) >= total:
                break
        else:
            raise ValueError("Listing limit exceeded")
    frame = {"seed": "independent-audit-2026-10-29-v1", "captured_on": "2026-10-29", "rows": rows,
             "status": "unlabelled; no accuracy claim", "excluded_prior_ids": sorted(excluded)}
    selected = select(frame)
    queue = []
    for row in selected:
        detail = _json(f"https://api.smartrecruiters.com/v1/companies/{row['board']}/postings/{row['job_id']}", 20)
        if str(detail.get("id")) != row["job_id"]:
            raise ValueError("Detail ID mismatch")
        url = detail.get("postingUrl")
        if not url:
            raise ValueError("Missing actual posting URL")
        queue.append({**row, "source_url": url, "detail_sha256": hashlib.sha256(json.dumps(detail, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                      "expected_categories": None, "expected_disposition": None, "evidence": None,
                      "review_status": "pending full-description review"})
        time.sleep(0.2)
    destination.write_text(json.dumps(frame, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    (ROOT / "evaluation/independent_audit_queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    print(f"Frozen {len(rows)} metadata records; {len(queue)} pending labels")


if __name__ == "__main__":
    main()
