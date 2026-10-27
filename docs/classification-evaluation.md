# Classification evaluation

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
