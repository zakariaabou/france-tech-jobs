"""Run with python -m france_tech_jobs from the repository root."""

import json
import os
from pathlib import Path
import sys

from .pipeline import update


def write_summary(path, result):
    status = "Partial source failure" if result["failed"] else "All sources succeeded"
    with Path(path).open("a", encoding="utf8") as handle:
        handle.write(f"## Job update: {status}\n\n")
        handle.write(f"- Active listings: {result['active']}\n")
        handle.write(f"- Successful sources: {', '.join(result['successful']) or 'none'}\n")
        handle.write(f"- Failed sources: {', '.join(result['failed']) or 'none'}\n")


def main():
    try:
        result = update(Path.cwd())
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Update failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        write_summary(os.environ["GITHUB_STEP_SUMMARY"], result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
