# Independent audit preparation

On 2026-10-29, a new frame captured 1,854 public posting summaries from Sia,
Scalian, Iliad/Free and Magellan. These four boards are disjoint from the seven
boards in the previous audit. Prior audit job IDs are excluded explicitly.
The capture reads all listing pages rather than the production title-selected
subset, and does not import the production classifier or inspect its predictions.

`evaluation/independent_audit_frame.json` freezes the seed and metadata.
`evaluation/independent_audit_queue.json` contains 28 selected records and
**no labels yet**. The existing `scripts/evaluate_holdout.py` `select()` function
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

Issue #14 remains open. Reviewers must read complete descriptions, assign category
and publish/review/exclude labels without consulting classifier predictions, and
record concise evidence before evaluating or changing classification rules.
The old evaluator uses paraphrased snippets, so it cannot establish full-description
production accuracy; a full-description verification pass and evidence provenance
are still required. This selected four-board sample is not representative of the
French or international job market, and no accuracy figures are claimed.
