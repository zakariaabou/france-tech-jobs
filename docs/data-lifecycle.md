# Job data and lifecycle

Each source provides a complete snapshot of its public postings. A job is identified by the pair `(source_id, job_id)`; neither a title nor a company name is a stable identifier. `data/jobs.json` is the persistent state shared between runs. Each record retains the source ID, source job ID, company, title, original location, contract, working schedule and work-mode text if provided, publication date if provided, source and application URLs, category tags, experience classification, geographic section and eligibility. Missing values remain blank or `unknown`. A full-time schedule is not assumed to be a CDI.

The pipeline uses three separate observation dates, all in UTC: `first_seen` is when the source ID was first observed; `last_seen` is when that job most recently appeared in a complete successful snapshot; `last_checked` is when its source was last successfully checked. They are not substitutes for `published_at`.

- **active:** present in the most recent successful complete snapshot for its source.
- **closed:** absent from a successful complete snapshot; not shown in current lists.
- **unknown:** its source failed or was disabled, so its current state cannot be confirmed; not shown in current lists.

When a source fails, previously stored observations remain in the state file and are marked unknown, not closed. If every source fails, no state or page is overwritten. When a job reappears, its original `first_seen` is retained. Only active jobs with eligible experience, role and geography are published. Classification uses descriptions transiently; complete descriptions are not persisted.

The output merges records only when their full application URLs match, preserving contributing source identifiers. Similar titles alone are not enough to prove two openings are the same. Geographic classification uses the posting's actual location, never the employer's home country or an inferred remote-work eligibility. See [scope](scope.md) for the selection policy.
