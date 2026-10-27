# Source inventory and access notes

This is a small pilot inventory, not comprehensive coverage of France. The
enabled records in `config/sources.json` select public employer job boards;
they do not prove that all jobs on a board are in scope. Classification must
still check job family, experience, contract and location, and must never use
an employer's home country as proof of a posting's location.

## Pilot inventory

On 2026-10-27, unauthenticated HTTP GETs to the following public listing
endpoints returned HTTP 200 and non-empty JSON. Counts and openings are a
snapshot, not a guarantee of current availability. Country hints are null
because company boards can contain listings in more than one country.

| Employer | Type | Category | Public listing endpoint | Snapshot |
| --- | --- | --- | --- | --- |
| [Decathlon Digital](https://job-boards.greenhouse.io/decathlontechnology) | Greenhouse | End client, retail/technology | [Board JSON](https://boards-api.greenhouse.io/v1/boards/decathlontechnology/jobs) | 74 postings |
| [SFEIR](https://jobs.lever.co/sfeir) | Lever | ESN / technology consultancy | [Board JSON](https://api.lever.co/v0/postings/sfeir?mode=json) | Non-empty |
| [Meritis](https://careers.smartrecruiters.com/Meritis) | SmartRecruiters | IT consultancy / ESN | [Board JSON](https://api.smartrecruiters.com/v1/companies/Meritis/postings?limit=1) | 137 postings total |
| [INFINIT](https://jobs.lever.co/infinit) | Lever | Fintech product | [Board JSON](https://api.lever.co/v0/postings/infinit?mode=json&limit=100) | 7 postings in first page; [software role in Paris](https://jobs.lever.co/infinit/bb2b0d9e-dc5c-49a3-904b-ee0750e65ae1) |
| [Beamy](https://jobs.lever.co/Beamy) | Lever | SaaS product | [Board JSON](https://api.lever.co/v0/postings/Beamy?mode=json&limit=100) | 13 postings in first page; [AI role in Paris](https://jobs.lever.co/Beamy/5defdfbe-8ec1-4279-94d7-279c840c2c29) |
| [Winamax](https://jobs.lever.co/winamax) | Lever | Gaming product | [Board JSON](https://api.lever.co/v0/postings/winamax?mode=json&limit=100) | 27 postings in first page; [backend role in Paris](https://jobs.lever.co/winamax/77f38084-073c-4f6c-bdbe-b5ebab701642) |
| [Agicap](https://jobs.lever.co/agicap) | Lever | Fintech product | [Board JSON](https://api.lever.co/v0/postings/agicap?mode=json&limit=100) | 24 postings in first page; [AI software role in Lyon](https://jobs.lever.co/agicap/8f6a3de6-0956-4a7d-8f0a-ddf363b5b153) |
| [Swile](https://jobs.lever.co/swile) | Lever | HR/fintech product | [Board JSON](https://api.lever.co/v0/postings/swile?mode=json&limit=100) | 31 postings in first page; [data role in Paris](https://jobs.lever.co/swile/2883d123-bbd8-4cce-93b3-04b8e387bca8) |
| [Theodo](https://jobs.lever.co/theodo) | Lever | IT consultancy | [Board JSON](https://api.lever.co/v0/postings/theodo?mode=json&limit=100) | 100 postings in first page; [AI software role in Paris](https://jobs.lever.co/theodo/9a2863cd-96b8-49f6-b17e-0de2a266917e) |
| [Kpler](https://jobs.lever.co/kpler) | Lever | International data product | [Board JSON](https://api.lever.co/v0/postings/kpler?mode=json&limit=100) | 100 postings in first page; [ML role in Paris](https://jobs.lever.co/kpler/10105b9b-ed9c-4ebe-8f3b-76b18edeccb8) |
| [MARGO](https://jobs.lever.co/margo-group) | Lever | IT consultancy | [Board JSON](https://api.lever.co/v0/postings/margo-group?mode=json&limit=100) | 67 postings in first page; [AI role in Paris](https://jobs.lever.co/margo-group/722035eb-386a-4875-aa60-20ef0fdf9a24) |
| [Datadog](https://job-boards.greenhouse.io/datadog) | Greenhouse | International cloud software product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/datadog/jobs) | 429 postings; [AI role in Paris](https://careers.datadoghq.com/detail/7194969/?gh_jid=7194969) |
| [Ekimetrics](https://jobs.lever.co/ekimetrics) | Lever | International data/AI consultancy | [Board JSON](https://api.lever.co/v0/postings/ekimetrics?mode=json&limit=100) | 32 postings in first page; [junior software role in Hong Kong](https://jobs.lever.co/ekimetrics/d741727e-f25f-452a-8e40-e6d04c3395ea) |
| [Mendix](https://jobs.lever.co/mendix) | Lever | International software product | [Board JSON](https://api.lever.co/v0/postings/mendix?mode=json&limit=100) | 44 postings in first page; [junior software role in Rotterdam](https://jobs.lever.co/mendix/7cbae919-1705-4737-9b0e-a942dd1451b3) |

Examples on these boards: [Decathlon Data Engineer in France](https://job-boards.greenhouse.io/decathlontechnology/jobs/4794463101),
[SFEIR Data Engineer in Strasbourg](https://jobs.lever.co/sfeir/256e267c-525f-49b4-8400-781ad1b8d6bb), and
[Meritis Data Engineer GCP](https://jobs.smartrecruiters.com/Meritis/744000110352885-data-engineer-gcp-h-f-).
Examples illustrate source relevance only; they are not validated as junior or
mid-level, and may close at any time.

Lever snapshots above are counts from a request capped at 100 results, not
necessarily totals. Where the first page contains 100 entries, the connector
must paginate to discover later results. Datadog and Kpler have international
listings as well as French ones; location must be assessed per posting.

`id` identifies the source stably, `type` selects the connector, `board` is the
employer's board identifier, `careers_url` is the public employer board, and
`enabled` controls collection. Add a source only after checking the exact board,
its current access and applicable reuse requirements. Any country hint must be
treated as a hint, not as verified job location. The pilot owner is the project
maintainer; community contributors may propose changes through GitHub issues.

Public accessibility is a technical observation, not an authorization or legal
conclusion about every form of reuse. Keep attribution and links to the
original posting, collect only information needed for the job listing, and
review provider and employer conditions. Identify the project through an
appropriate user agent, use conservative request rates and back off on errors.
Avoid collecting recruiter or applicant personal information.

The [Lever Postings API](https://github.com/lever/postings-api) documents
published jobs and pagination. [SmartRecruiters' public posting API](https://developers.smartrecruiters.com/docs/endpoints)
documents the listing and detail endpoints. Detail requests on large boards
are potentially expensive; start with this small pilot and do not turn on large
employer boards without checking request volume and rate limits.

## Job boards requiring further investigation

| Source | Status for this project |
| --- | --- |
| LinkedIn | No automated scraping planned: [LinkedIn prohibits third-party scraping and automated activity](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin). Link to employer originals when available. |
| Welcome to the Jungle | No connector enabled. Investigate a suitable authorized feed, partnership and conditions for reuse. |
| HelloWork | No connector enabled. Investigate a suitable authorized feed, partnership and conditions for reuse. |
| Apec | No connector enabled. Investigate available access, partnership and conditions for reuse. |
| France Travail | No connector enabled. [The official API listing](https://www.data.gouv.fr/dataservices/api-offres-demploi) states the job-offers API is not currently exposed while distribution and reuse are reviewed; access inquiries go through France Travail. Recheck before adding. |

Other researched boards, such as Sopra Steria and Devoteam on SmartRecruiters,
returned non-empty listings but are substantially larger; they are not yet in
the pilot because an unfiltered detail request per posting would be costly.
They should be reassessed once bounded filtering and request budgets are in
place. Capgemini's tested SmartRecruiters company identifier returned no
postings and has not been enabled. None of these observations proves that an
employer has no jobs on other platforms.
