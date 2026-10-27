# Job scope and source policy

## Intended audience and categories

The initial list targets junior, new-graduate and mid-level opportunities,
with jobs located in France presented separately from international jobs.
Internships (stages), apprenticeships (alternance) and senior leadership roles
are out of scope. Multiple category tags can be applied to one opportunity:

- **data**: Data Engineer, Analytics Engineer, Big Data Engineer, ingénieur données.
- **ai**: AI, ML, MLOps, GenAI, LLM, NLP and computer vision engineering.
- **software**: software, backend, frontend, full-stack, mobile and platform engineering.

The classifier uses French and English titles. AI domain tags require AI in
the engineering title: a generic mention of AI in a description may refer to
the employer or a productivity tool, not an AI-engineering role. Being a
product manager who works with engineers is not, by itself, an engineering job.

## Experience and contract policy

- Explicit junior, new-graduate, entry-level or débutant titles are junior;
  mid-level, intermediate, confirmed and confirmé titles are mid-level.
- An explicit experience requirement of 0–2 years is treated as junior,
  and 3–4 years as mid-level. A requirement beginning at 5 years or more
  is excluded as outside this conservative initial scope. All recognized
  requirements are checked, so a later senior requirement is not hidden by an
  earlier number. Explicit references to company history are ignored; the
  wording heuristic is limited and should be reviewed against live examples.
- An open-ended minimum (for example, "2+ years"), an experience range
  crossing those boundaries, conflicting indications, unspecified experience
  or unclear wording is **unknown**. It is not
  published as junior or mid-level without review. This intentionally misses
  some relevant jobs; it avoids inventing qualifications.
- Senior, lead, staff, principal, manager and architect titles are excluded.
  Ordinary references in a description to working with senior colleagues do
  not automatically exclude the posting.
- Internship or alternance titles or contracts are excluded; a description
  that merely mentions mentoring interns does not make the role an internship.
- CDI and CDD can be included if role, seniority and location qualify.
  Freelance positions are also eligible when these conditions are met; the
  contract type must be shown as stated rather than inferred.

These experience boundaries are project defaults, not claims about how every
employer defines junior or mid-level. Manual review and refinement can reduce
false negatives after a pilot.

## Location policy

Explicit France or a recognized French location is placed in France. Explicit
recognized foreign countries or cities are international. A location that
contains both a recognized French and foreign place, or one whose country is
unclear, is unknown and held for review. Remote alone is not a country, and
the job location is not evidence that worldwide applicants are eligible.
Recognized cities and countries are a deliberately limited dictionary, not a
complete geographical database. The original source location is retained.

## Access, attribution and privacy

- Assess each source's documented API, terms of access and reuse, and employer
  constraints before enabling it. A publicly visible endpoint does not itself
  establish unrestricted reuse. Record the source, access status and date of
  assessment; use appropriate rate limits, timeouts and backoff.
- Prefer original employer application links when verified, and retain source
  links and attribution. Publish concise structured facts needed to locate and
  assess a job, not a blanket copy of full job descriptions.
- Do not bypass login walls, access restrictions or bot controls. LinkedIn
  scraping is not included by default; consider it only if authorized access
  and reuse are established. Evaluate Welcome to the Jungle, HelloWork, Apec
  and France Travail individually; availability or permission is not assumed.
- Do not collect candidate data or unnecessary personal contact details from
  listings. Never guess missing salary, experience, remote eligibility or dates.
- Keep a last-successful-check timestamp and treat failed source retrievals as
  unknown. An outage is not evidence that all affected jobs have closed.
