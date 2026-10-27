# France Tech Jobs Implementation Plan

**Goal:** Publish an automatically refreshed, France-first catalogue of junior and mid-level data, AI and software jobs.

**Architecture:** Source adapters collect employer postings into a shared record format. Conservative classification, per-source lifecycle tracking and deduplication feed generated Markdown pages; a scheduled GitHub Actions workflow runs the pipeline.

**Tech stack:** Python 3.11+, standard library, unittest and GitHub Actions.

**Scope:** Issues #1–#12 and the agreed conversation scope: exclude internships and alternance, retain unknown data as unknown, and use international listings as a secondary section.

## Work packages

- [ ] Document eligibility and source access; inventory and verify pilot employers.
- [ ] Implement and test source adapters and conservative classification independently.
- [ ] Persist source observations, isolate failures and avoid deleting jobs during outages.
- [ ] Deduplicate conservatively and render categorized GitHub pages from verified records.
- [ ] Add scheduled/manual automation, project documentation and contribution instructions.
- [ ] Run fixture tests and a live source pilot, record limitations and update issues.

## Important failure cases

- A source outage must not imply that all of its jobs have closed.
- Unknown experience, location or remote eligibility must not be presented as known.
- Separate jobs with similar titles must not be merged without strong evidence.
- Markdown and URLs from external data must not break the generated pages.
- A failed run must not overwrite the previous successful output.
