# Classification evaluation

## Reproducible stratified snapshot: 2026-10-27

The file `evaluation/classification_snapshot.json` contains 20 manually selected,
manually labelled snapshots linked to the original postings. Selection deliberately
spans France and international locations; data, AI and software titles; junior,
mid-level and junior-to-mid roles; internships, senior roles and unrelated jobs;
and uncertain experience. It draws on Doctrine, Decathlon Digital, SFEIR, Meritis,
Ekimetrics and Mendix. This is a **stratified convenience sample**, not a random,
representative sample of the French or international market. Labels and classifier
changes were developed using some of the same examples, so it is not a holdout.

To avoid republishing full advertisements, each fixture includes the title,
location, contract, and a minimal paraphrase of relevant experience evidence. An
empty evidence field means no experience detail was included in this snapshot,
not that none appeared anywhere in the original posting. The test evaluates those
fixed inputs, not today's postings or full descriptions. The source may have
changed or closed since review.

Run `python scripts/evaluate_classification.py` for the current version or
`python scripts/evaluate_classification.py --ref 846ad98` for the baseline.
`--ref` executes the classifier from the specified trusted local Git revision.
The script prints a three-way expected-versus-observed matrix, sample publish
precision and recall, and role-category mismatches. `python -m unittest discover
-s tests -p test_classification_snapshot.py -v` checks the fixed labels offline.

| Manually labelled | Baseline observed publish / review / exclude | Updated observed publish / review / exclude |
| --- | --- | --- |
| Publish (7) | 6 / 0 / 1 | 7 / 0 / 0 |
| Review (6) | 1 / 5 / 0 | 0 / 6 / 0 |
| Exclude (7) | 0 / 0 / 7 | 0 / 0 / 7 |

For this deliberately selected snapshot, publish precision and recall both
changed from 6/7 to 7/7; category mismatches changed from 3 to 0. These numbers
describe only these fixed excerpts and do **not** estimate production precision,
recall, or the overall market. The baseline missed a hyphenated front-end role
and classified a French open-ended minimum as junior; AI platform and AI software
titles also lacked AI tags. Regression tests cover these cases, including French
“à partir de” requirements and longer English qualification wording.

Explicit junior/intermediate titles and bounded ranges entirely within the
junior-to-mid bands (for example 2–4 years) are labelled `junior-mid` and
eligible. An open-ended minimum, a range including five years, or conflicting
independent requirements remains unknown or excluded according to the evidence.
The sample and earlier regression tests were used to build this version; a
larger, randomly selected and independently labelled holdout remains necessary
to measure generalization.

## Method and limits

On 2026-10-27, we retrieved current public postings from Decathlon Digital
(Greenhouse), SFEIR, Ekimetrics and Mendix (Lever) and manually examined this
convenience sample. The table records the classifier output using the full
posting description, not the shorter regression-test excerpts. Links are
direct employer postings; content and availability can change. These employers
are examples for evaluation, not a claim that all are configured as sources.

We use three expected dispositions: **publish** when the role explicitly looks
junior or confirmed and relevant; **exclude** for clear senior, internship or
non-engineering examples; **review** where seniority is not clear enough for
publication under this project's conservative policy. Labels are manual
judgments of the supplied evidence, not employer-verified ground truth.

## Live sample, after fixes

| Posting | Evidence / expected disposition | Observed result |
| --- | --- | --- |
| [Decathlon Data Engineer Confirmed](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4794463101) | Confirmed data engineering, France; publish mid | Data, mid, France; eligible |
| [SFEIR Data Engineer Confirmé(e)](https://jobs.lever.co/sfeir/978114d0-e5ab-4766-ba14-04332850b0cd) | Confirmé, Lille; using GenAI to aid workflows does not make the role an AI engineer; publish mid | Data only, mid, France; eligible |
| [SFEIR Développeur Java confirmé(e)](https://jobs.lever.co/sfeir/9f74e55a-eeaa-4e5a-a980-b0819e125466) | Confirmé software development, Lille; publish mid | Software, mid, France; eligible |
| [Ekimetrics Junior Software Engineer](https://jobs.lever.co/ekimetrics/d741727e-f25f-452a-8e40-e6d04c3395ea) | Junior software, Hong Kong; six-month role is not an internship; publish | Software, junior, international; eligible |
| [Mendix Junior Software Developer](https://jobs.lever.co/mendix/7cbae919-1705-4737-9b0e-a942dd1451b3) | Junior software, Rotterdam; publish | Software, junior, international; eligible |
| [Decathlon Senior AI Engineer](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4846614101) | Senior title; exclude | AI, excluded; ineligible |
| [Decathlon Product Manager internship](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4895914101) | Internship and non-engineering; exclude | No category, excluded; ineligible |
| [Decathlon Data Product Manager](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4977048101) | Product management is not an engineering role; exclude | No category; ineligible |
| [Decathlon AI/ML Engineer](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4997303101) | Relevant France role, requires at least 3 years with no upper limit; review | AI, unknown, France; ineligible |
| [SFEIR Data Engineer, Luxembourg](https://jobs.lever.co/sfeir/837d6ed4-db91-4417-9b2d-4c441fbbf3bc) | Relevant international role; marketing phrase “deviens un expert” does not establish level; review | Data, unknown, international; ineligible |
| [SFEIR GenAI Engineer, Niort](https://jobs.lever.co/sfeir/bd2baf72-ba52-4168-9a89-d2a8c179741b) | Relevant France role; experience level not explicit; review | AI, unknown, France; ineligible |

The 11 selected examples matched these manual dispositions after the changes:
5 publish, 3 exclude and 3 review. This is **not** a population precision or
recall estimate: the sample is small, intentionally selected, and includes no
random sample of employer boards. The three review cases demonstrate likely
recall loss, especially for open-ended minimum experience requirements.

## Changes informed by live observations

- Recognize English **confirmed** as a mid-level indicator, in addition to
  French **confirmé**. The Decathlon role was previously held as unknown.
- Require AI to be part of an engineering title rather than inferring an AI
  role from generic description mentions. The SFEIR data role was previously
  tagged as both data and AI because it mentions using AI in its workflow.
- Treat “expert” as senior when it describes the title itself, rather than
  treating an unrelated promotional phrase as a seniority declaration.
- Recognize Niort, Rotterdam and Hong Kong as location signals. They were
  previously unknown in the cited examples.

`tests/test_classify.py` contains small paraphrased fixtures exercising these
patterns and separate tests for edge cases such as internships, ambiguous
experience and conflicting candidate requirements. The fixtures are not live
postings and should not be presented as current vacancies.

## Known limitations and follow-up

- Open-ended requirements such as “at least 3 years” are withheld even when
  an employer may consider the role mid-level. This is a deliberate precision
  versus recall trade-off and needs a product decision or a review queue.
- Many genuine jobs do not state seniority or have uncommon job titles; they
  are withheld rather than guessed. A title may not describe all duties, so
  title-based AI tagging can miss relevant jobs.
- City matching is incomplete and does not resolve ambiguous place names or
  remote work authorization. Do not infer worldwide eligibility from remote.
- Full descriptions can contain employer marketing or multiple qualifications;
  the experience parser uses heuristics and cannot guarantee correct attribution.
- Follow-up should use a larger, representative, independently labelled sample
  with a documented sampling method, confusion matrix and separate precision
  and recall measurements; include junior roles in France and international
  roles across sources. Re-evaluate as listings and sources change.
