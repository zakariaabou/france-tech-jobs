# Pilot verification

## Updated 20-source pilot

After the classification and source changes, a local update on 2026-10-27
retained active records for all 20 configured employer feeds. The generated
snapshot has nine eligible listings: five in France and four international,
including one French AI role, two data roles and six software roles. It contains
junior, junior–mid and mid-level examples. The [Doctrine confirmed machine
learning role](https://jobs.lever.co/doctrine/6ec36f1e-471a-4cb0-bcc5-6f5d2e7540fd)
appears in the French AI list. The audited Meritis C++ role now has unknown
seniority and is withheld because its two-year requirement is open-ended.
The updated collector links to the SmartRecruiters job page instead of the
one-click application redirect.

The [20-source GitHub manual run](https://github.com/zakariaabou/france-tech-jobs/actions/runs/40561857086)
also completed successfully with all sources available and nine eligible
listings. The manual run below used the earlier 14-source configuration. No
actual scheduled run has been observed yet. Employer-specific reuse terms remain
under review.

## Scope and evidence

This is a point-in-time audit of the `846ad98` pipeline and the catalogue on
2026-10-27, not a guarantee that individual vacancies remain open. The
[manual GitHub Actions run](https://github.com/zakariaabou/france-tech-jobs/actions/runs/40516144644)
completed its tests, fetch and publish steps successfully. Its update log
reported 14 successful source feeds, no failed feeds and 12 eligible listings.
The schedule is configured, but no completed **scheduled** run was available
at the time of this audit; the manual run does not prove that scheduled
execution occurred.

The local snapshot reviewed contained 12 active eligible records with 12
distinct application URLs: three data roles, nine software roles and no AI
roles; ten were in France and two were international. In that snapshot nine
were labeled mid and three junior, with five employers represented. Counts
are an observation from that run, not a measure of the wider market.

## Sample checks

| Posting and link checked | Audit observation |
| --- | --- |
| [Decathlon Data Engineer Confirmed](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4794463101) | France data role, title says confirmed; the direct employer page includes an application form. |
| [SFEIR Data Engineer Confirmé](https://jobs.lever.co/sfeir/978114d0-e5ab-4766-ba14-04332850b0cd/apply) | France data role, title says confirmé; the direct employer application page rendered. |
| [SFEIR Développeur Java confirmé](https://jobs.lever.co/sfeir/9f74e55a-eeaa-4e5a-a980-b0819e125466/apply) | France software role, title says confirmé; the direct employer application page rendered. |
| [Mendix Junior Software Developer](https://jobs.lever.co/mendix/7cbae919-1705-4737-9b0e-a942dd1451b3/apply) | Junior software role in Rotterdam; direct application page rendered. Its description says applicants need a valid Netherlands work permit without sponsorship. |
| [Doctrine Confirmed Machine Learning Engineer](https://jobs.lever.co/doctrine/6ec36f1e-471a-4cb0-bcc5-6f5d2e7540fd/apply) | France AI role in Paris; the employer uses “Confirmed” in the title and asks for significant experience building NLP products, without specifying a number of years. The project treats confirmed as mid-level; the employer does not explicitly define a year range. The direct application page rendered. This was checked separately from the 14-feed snapshot while Doctrine was being added. |
| [Meritis Développeur C++](https://jobs.smartrecruiters.com/Meritis/744000147966164-developpeur-c-h-f-) | France software posting said “à partir de 2 ans d'expérience”: an open-ended minimum. The audited snapshot labeled it junior, which conflicts with the project's policy for open-ended experience. The automated application-link check redirected to SmartRecruiters' one-click page and returned HTTP 403, so the form itself was not verified. |
| [Decathlon AI/ML Engineer](https://job-boards.eu.greenhouse.io/decathlontechnology/jobs/4997303101) | Relevant France AI role; asks for at least three years, without an upper limit. It was held back as unknown under the conservative experience policy. This shows a likely false negative, not evidence that no AI jobs exist. |

The directly rendered pages demonstrate that these sample URLs led to an
employer posting or application form when checked; no application was
submitted. Experience categories are project interpretations, not employer
guarantees. The Decathlon AI role was held back because its experience level
was uncertain; the separately checked Doctrine role was not part of the
14-feed snapshot. Sample links are a convenience selection, not representative
accuracy statistics. See [classification evaluation](classification-evaluation.md)
for the broader classification review.

## Duplicate and failure checks

The 12 active candidates had distinct literal application URLs, so the live
snapshot did not exercise a known cross-source duplicate. The pipeline test
`test_duplicate_url_merges_sources_but_similar_jobs_remain` passes using
fixtures; it checks exact-URL merging and that similarly named roles with
different URLs remain separate. This is not proof that all real duplicate
postings with different URLs are found.

An earlier [manual run](https://github.com/zakariaabou/france-tech-jobs/actions/runs/40514774191)
reported two source timeouts and nevertheless completed; those sources were
held unverified instead of being marked closed. Subsequent code added bounded
retries, and the 14-source manual run above reported no failed feeds. The tests
also cover incomplete source responses and total or partial failures. A source
may fail on a future run, and accessible public endpoints alone do not establish
permission for every type of reuse.

## Remaining launch checks

- Validate the first actual scheduled execution and review its source report.
- Review a qualified France junior data example when one becomes available;
  the current snapshot contains none.
- Continue source-access reviews and a larger, representative accuracy study;
  titles, cities, minimum-experience phrasing and links can all change.
