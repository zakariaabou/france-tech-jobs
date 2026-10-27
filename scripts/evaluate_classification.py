"""Evaluate manually labelled, paraphrased job snapshots; no live requests."""

from collections import Counter
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from france_tech_jobs.classify import classify


def evaluate(classifier=classify):
    samples = json.loads((ROOT / "evaluation/classification_snapshot.json").read_text(encoding="utf8"))
    matrix = Counter()
    category_errors = []
    for sample in samples:
        result = classifier(sample["title"], sample["evidence"], sample["location"], sample["contract"])
        observed = "publish" if result["eligible"] else "exclude" if result["seniority"] == "excluded" or not result["categories"] else "review"
        matrix[(sample["expected"], observed)] += 1
        if result["categories"] != sample["expected_categories"]:
            category_errors.append(sample["url"])
    return samples, matrix, category_errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", help="Evaluate the classifier saved at this trusted local Git revision")
    args = parser.parse_args()
    classifier = classify
    if args.ref:
        source = subprocess.check_output(["git", "show", f"{args.ref}:src/france_tech_jobs/classify.py"], cwd=ROOT, text=True, encoding="utf8")
        namespace = {"__name__": "classification_reference"}
        exec(compile(source, "classification_reference", "exec"), namespace)
        classifier = namespace["classify"]
    samples, matrix, category_errors = evaluate(classifier)
    labels = ("publish", "review", "exclude")
    print(f"Manually selected paraphrased snapshots: {len(samples)}")
    print("Expected rows / observed columns: " + ", ".join(labels))
    for expected in labels:
        print(f"{expected}: " + ", ".join(str(matrix[(expected, observed)]) for observed in labels))
    tp = matrix[("publish", "publish")]
    published = sum(matrix[(expected, "publish")] for expected in labels)
    expected_publish = sum(matrix[("publish", observed)] for observed in labels)
    print(f"Sample publish precision: {tp}/{published}; sample publish recall: {tp}/{expected_publish}")
    print(f"Category mismatches: {len(category_errors)}")
    for url in category_errors:
        print(url)


if __name__ == "__main__":
    main()
