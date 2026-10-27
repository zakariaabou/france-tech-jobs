# Stratified classification audit

This audit is separate from the 20 development examples. On 2026-10-27 we
retrieved 412 public postings from seven employer boards (Decathlon Digital,
Algolia, Doctolib, SFEIR, Doctrine, Mendix and Ekimetrics), removed jobs whose
IDs appeared in the development examples, and froze **393 job metadata records**
in `evaluation/holdout_frame.json`. It contains titles, locations, contracts,
source identifiers and links, not complete job descriptions or applicant data.
The frame records the exact board identifiers and excluded development IDs.

The fixed selection uses the seed in that file. For each combination of four
independent title-keyword buckets (data, AI, software/engineering and other)
and two literal-location buckets (France marker and other/unknown), take up
to three records with the smallest SHA-256 of `seed|source_id|job_id`. A
separate title-based junior/confirmed/intermediate oversample adds up to four
records not already selected. The latter returned only four candidates, three
of which were internships. These buckets guide selection; the other/unknown
bucket is not proof that a job is international. The selected IDs and human
labels are in `evaluation/holdout_labels.json`; `select()` replays the ranking
against the saved frame and checks that every selected job has exactly one label.

We examined job titles, locations and brief qualification excerpts, assigned
publish/review/exclude and role-category labels, and stored only short
paraphrases of relevant experience. Empty evidence means that no qualification
was recorded in the audit excerpt, not that no requirement exists anywhere in
the full advert. The offline evaluation measures these frozen excerpts, not a
live classifier run on the full description. URLs and postings can change.
Some category boundaries, such as whether a senior DataOps position counts as
data engineering, are judgment calls.

**Important independence limitation:** initial review of this sample identified
the missing Agentic AI, Software Development Engineer and DataOps title patterns,
and those findings were given to the implementer before the revised classifier
was evaluated. These examples are now development examples, not an independent
holdout for the revised model. The
`c65e8c4` baseline had not been changed in response to these findings, but the
sample itself was selected from only seven known configured boards. The results
are not an independent population estimate; future fixes need a separate held
back, independently labelled evaluation set.

Run `python scripts/evaluate_holdout.py` for the current classifier, or
`python scripts/evaluate_holdout.py --ref c65e8c4` for the baseline; `--ref`
executes code from the specified **trusted local Git revision**. Run
`python -m unittest discover -s tests -p test_holdout.py` to check reproducible
selection and measurement. The evaluator prints a three-way confusion matrix,
category mismatches and Wilson intervals; the intervals describe a tiny
selected sample and cannot be generalized to the market.

| Expected disposition | Baseline: publish / review / exclude | Updated: publish / review / exclude |
| --- | --- | --- |
| Publish (1) | 1 / 0 / 0 | 1 / 0 / 0 |
| Review (4) | 0 / 3 / 1 | 0 / 4 / 0 |
| Exclude (22) | 0 / 0 / 22 | 0 / 0 / 22 |

Both versions have sample publish precision and recall of 1/1; a nominal
95% Wilson interval is approximately 0.207–1.000, and is not a market-wide
confidence interval. The baseline missed an Agentic AI role needing review
and identified three role categories differently from the manual labels. After
the informed title fixes, the category mismatches are zero on these examples.
The DataOps posting is excluded either way because it is senior. Selection
heavily oversamples exclusions and yields only one clearly
publishable job, so these counts cannot establish useful production accuracy.
