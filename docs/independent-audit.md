# Independent audit preparation

On 2026-10-29, a new frame captured 1,854 public posting summaries from Sia,
Scalian, Iliad/Free and Magellan. These four boards are disjoint from the seven
boards in the previous audit. Prior audit job IDs are excluded explicitly.
The capture reads all listing pages rather than the production title-selected
subset, and does not import the production classifier or inspect its predictions.

`evaluation/independent_audit_frame.json` freezes the seed and metadata.
`evaluation/independent_audit_queue.json` contains 28 selected records and
labels assigned by one assistant qualitative reviewer before classifier comparison. The existing `scripts/evaluate_holdout.py` `select()` function
replays the hash-ranked strata and junior/confirmed oversample on this new frame.
Broad independent title keywords define sampling strata, not expected categories.
Each queue entry links to the actual URL returned by the posting-detail API and
records a SHA-256 digest of that detail response. Full descriptions and recruiter
contact details are not stored. Live descriptions can change; a digest mismatch
requires a new review record, not pretending that the original evidence is intact.

`python scripts/prepare_independent_audit.py` documents the capture procedure and
refuses to overwrite an existing frozen frame. Listing counts must agree between
pages, duplicate IDs are rejected, and missing posting links fail capture. Equal
counts do not prove an offset-paginated source was unchanged during collection.

All 28 role descriptions, qualifications and additional conditions were reviewed,
with concise paraphrased evidence recorded before any classifier predictions were
examined. The full response hashes matched for all 28 records. This is an assistant
qualitative review, not independent human adjudication; there is no second reviewer.
Category labels reflect job duties, including data/AI architecture, rather than
merely matching the production title patterns. Infrastructure-only, project
management, analytics-dashboard and non-software industrial roles were excluded.

Run `python scripts/evaluate_independent_audit.py` to fetch and classify the full
source descriptions. It aborts on any source-hash mismatch and writes only expected
and observed labels, hashes and identifiers to `independent_audit_results.json`.
Raw descriptions and recruiter contact details are not published. A source change
can prevent reproduction; do not silently reuse a label for a changed description.

Issue #14 remains open: only one of the 28 cases has a publish label, category
boundaries require second review, and this four-board selection is not representative
of the French or international market. No population accuracy is claimed.

The initial full-description run agreed on 23 exclusions, three review cases,
and one publish case. One review-labelled Java role at Magellan was published:
its qualification states a minimum of four post-study years with no upper bound,
but the wording places the experience noun before the number, which the current
parser misses. Its confirmed-level title then drives publication. Six category
disagreements concern duty-based labels versus title patterns, mostly on roles
already excluded as architects, senior experts or internships. These are
diagnostic counts, not representative precision or recall estimates. Fixes based
on these findings will turn those examples into development evidence.

The initial output is preserved in `independent_audit_baseline_results.json`.
After labels were frozen and compared, the parser was extended to recognize
French/English requirements with the experience noun before the number. Tests
cover open minima, senior requirements, bounded ranges and company-history
text. The same 28 source hashes still matched on the rerun: 23 exclusions,
four review cases and one publish case agreed; six category disagreements remain.
`independent_audit_results.json` records that rerun. The corrected example is
now development evidence, so the improved count is not an independent validation
of the fix. A new positive-rich sample and second-reviewer adjudication remain
necessary before claiming reliable population performance.
