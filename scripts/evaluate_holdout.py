"""Evaluate a frozen, manually labelled source sample without fetching adverts."""

from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from france_tech_jobs.classify import classify


def select(frame):
    """Replay the declared hash ranking from the frozen public-metadata frame."""
    seed = frame["seed"]
    rows = frame["rows"]

    def rank(row):
        return hashlib.sha256(f"{seed}|{row['source_id']}|{row['job_id']}".encode()).hexdigest()

    selected = []
    for role in ("data", "ai", "software", "other"):
        for geography in ("france_marker", "other_or_unknown"):
            pool = [r for r in rows if r["role_bucket"] == role and r["geography_bucket"] == geography]
            selected.extend(sorted(pool, key=rank)[:3])
    existing = {(r["source_id"], r["job_id"]) for r in selected}
    extras = [r for r in rows if (r["source_id"], r["job_id"]) not in existing
              and re.search(r"junior|débutant|debutant|confirmé|confirmed|intermediate", r["title"], re.I)
              and re.search(r"engineer|developer|développeur|ingénieur", r["title"], re.I)]
    selected.extend(sorted(extras, key=rank)[:4])
    return selected


def wilson(successes, total):
    """95% Wilson interval for the observed fraction, not population inference."""
    if not total:
        return None
    z = 1.959963984540054
    proportion = successes / total
    scale = 1 + z * z / total
    midpoint = (proportion + z * z / (2 * total)) / scale
    half = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / scale
    return midpoint - half, midpoint + half


def evaluate(classifier=classify):
    frame = json.loads((ROOT / "evaluation/holdout_frame.json").read_text(encoding="utf8"))
    labels = json.loads((ROOT / "evaluation/holdout_labels.json").read_text(encoding="utf8"))
    by_key = {(x["source_id"], x["job_id"]): x for x in labels}
    selected = select(frame)
    if len(by_key) != len(labels) or set(by_key) != {(r["source_id"], r["job_id"]) for r in selected}:
        raise ValueError("Frozen selection and independent labels do not match")
    matrix = Counter()
    category_errors = []
    for row in selected:
        label = by_key[(row["source_id"], row["job_id"])]
        result = classifier(row["title"], label["evidence"], row["location"], row["contract"])
        observed = "publish" if result["eligible"] else "exclude" if result["seniority"] == "excluded" or not result["categories"] else "review"
        matrix[label["expected_disposition"], observed] += 1
        if set(result["categories"]) != set(label["expected_categories"]):
            category_errors.append((row["source_url"], label["expected_categories"], result["categories"]))
    return selected, matrix, category_errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", help="Evaluate classifier from this trusted local Git revision")
    args = parser.parse_args()
    classifier = classify
    if args.ref:
        source = subprocess.check_output(["git", "show", f"{args.ref}:src/france_tech_jobs/classify.py"], cwd=ROOT, text=True, encoding="utf8")
        namespace = {"__name__": "trusted_classification_reference"}
        exec(compile(source, "trusted_classification_reference", "exec"), namespace)
        classifier = namespace["classify"]
    selected, matrix, category_errors = evaluate(classifier)
    labels = ("publish", "review", "exclude")
    print(f"Frozen stratified sample: {len(selected)}")
    print("Expected rows / observed columns: " + ", ".join(labels))
    for expected in labels:
        print(expected + ": " + ", ".join(str(matrix[expected, observed]) for observed in labels))
    tp = matrix["publish", "publish"]
    published = sum(matrix[expected, "publish"] for expected in labels)
    expected = sum(matrix["publish", observed] for observed in labels)
    for name, denominator in (("sample precision", published), ("sample recall", expected)):
        interval = wilson(tp, denominator)
        suffix = f"; 95% Wilson {interval[0]:.3f}–{interval[1]:.3f}" if interval else "; undefined"
        print(f"{name}: {tp}/{denominator}{suffix}")
    print(f"Category mismatches: {len(category_errors)}")
    for url, expected, observed in category_errors:
        print(f"{url} expected={expected}, observed={observed}")


if __name__ == "__main__":
    main()
