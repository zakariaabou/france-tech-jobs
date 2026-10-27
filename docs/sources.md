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
| [Doctrine](https://jobs.lever.co/doctrine) | Lever | French legal AI product | [Board JSON](https://api.lever.co/v0/postings/doctrine?mode=json&limit=100) | 38 postings; [confirmed ML/NLP role in Paris](https://jobs.lever.co/doctrine/6ec36f1e-471a-4cb0-bcc5-6f5d2e7540fd) and [confirmed software role](https://jobs.lever.co/doctrine/ed05d3b6-53be-4af9-9abd-e89574dca94b), both eligible under the current rules |
| [Odaseva](https://jobs.lever.co/odaseva) | Lever | French data security software product | [Board JSON](https://api.lever.co/v0/postings/odaseva?mode=json&limit=100) | 16 postings; [junior frontend role in Paris](https://jobs.lever.co/odaseva/5fa5b26d-a0f2-4135-9559-e63feb2213f1); its stated experience requirement should be checked before classification |
| [Algolia](https://job-boards.greenhouse.io/algolia) | Greenhouse | International AI/search product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/algolia/jobs?content=true) | 26 postings; France and international technology roles |
| [Doctolib](https://job-boards.greenhouse.io/Doctolib) | Greenhouse | French health technology product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/Doctolib/jobs?content=true) | 150 postings; includes French software and AI roles, many senior or internships |
| [Shift Technology](https://job-boards.greenhouse.io/shifttechnology) | Greenhouse | French AI/insurance software product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/shifttechnology/jobs?content=true) | 18 postings; French AI roles, some outside target experience scope |
| [Mirakl Labs](https://job-boards.greenhouse.io/mirakllabs) | Greenhouse | French commerce software product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/mirakllabs/jobs?content=true) | 30 postings; French software and AI roles, many senior or internships |
| [Pigment](https://jobs.lever.co/pigment) | Lever | French planning software | [Board JSON](https://api.lever.co/v0/postings/pigment?mode=json&limit=100) | 100 postings in first page; [junior backend](https://jobs.lever.co/pigment/dad6777e-77e7-4885-b8cc-751ad141df6a) and [data engineer](https://jobs.lever.co/pigment/0aede960-d9cd-45c1-92e4-82e3cb3b2ae2) in Paris |
| [Scaleway](https://jobs.lever.co/scaleway) | Lever | French cloud infrastructure provider | [Board JSON](https://api.lever.co/v0/postings/scaleway?mode=json&limit=100) | 30 postings in first page; [backend software role in Paris](https://jobs.lever.co/scaleway/ad74cfd6-edb5-4ea7-a998-52cf8945112b) |
| [VO2 Group](https://jobs.lever.co/vo2-group) | Lever | French technology consultancy | [Board JSON](https://api.lever.co/v0/postings/vo2-group?mode=json&limit=100) | 42 postings in first page; [AI engineer role in Paris](https://jobs.lever.co/vo2-group/5325c5b9-0e1d-44f0-8e09-0f226cba2d8b) |
| [Malt](https://jobs.lever.co/malt) | Lever | French freelance marketplace | [Board JSON](https://api.lever.co/v0/postings/malt?mode=json&limit=100) | 26 postings in first page; [engineering role in Paris](https://jobs.lever.co/malt/977db4c4-b876-40db-b36e-71a9ad93a78e), senior and excluded by current scope |
| [Outsight](https://jobs.lever.co/outsight) | Lever | French spatial analytics product | [Board JSON](https://api.lever.co/v0/postings/outsight?mode=json&limit=100) | 13 postings in first page; [algorithm engineer in Paris](https://jobs.lever.co/outsight/9006eaa9-9c8e-4c2d-8dd3-1e08e6065243) |
| [Perion Network](https://job-boards.greenhouse.io/perionnetworkltd) | Greenhouse | International advertising technology product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/perionnetworkltd/jobs?content=true) | 6 postings; [machine-learning role in Paris](https://job-boards.greenhouse.io/perionnetworkltd/jobs/4699316006) |
| [Beacon Biosignals](https://job-boards.greenhouse.io/beaconbiosignals) | Greenhouse | International neurotechnology product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/beaconbiosignals/jobs?content=true) | 27 postings; [senior algorithm role in Paris](https://job-boards.greenhouse.io/beaconbiosignals/jobs/4361222009), excluded by current scope |
| [Teads](https://job-boards.greenhouse.io/teads1) | Greenhouse | International advertising technology product | [Board JSON](https://boards-api.greenhouse.io/v1/boards/teads1/jobs?content=true) | 59 postings; [engineering role in Montpellier](https://job-boards.eu.greenhouse.io/teads1/jobs/4673150101), senior and excluded by current scope |

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
its current access and applicable reuse requirements. Each record also stores
`access_status`, `access_verified_at`, `reuse_status`, `country_scope`, and
`owner`. For all current records the endpoint's unauthenticated technical
access was verified on 2026-10-27, provider documentation describes public
access, and employer-specific aggregation/reuse conditions remain **unverified**;
those fields are evidence and a review queue, not a grant of permission. Source
locations are checked per posting, and a country hint is never treated as
verified location. The owner is the project maintainer; community contributors
may propose changes through GitHub issues.

Public accessibility is a technical observation, not an authorization or legal
conclusion about every form of reuse. Keep attribution and links to the
original posting, collect only information needed for the job listing, and
review provider and employer conditions. Identify the project through an
appropriate user agent, use conservative request rates and back off on errors.
Avoid collecting recruiter or applicant personal information.

The [employer terms audit](employer-terms-audit.md) records source-specific
policies and their scope. Reuse authorization for the individual employer feeds
remains unverified; provider API availability is not blanket clearance.

Provider evidence: [Lever's Postings API](https://github.com/lever/postings-api)
describes its published jobs and explicitly says they may be scraped by third
parties; [Greenhouse's Job Board API](https://docs.greenhouse.io/job-board.html#authentication)
documents unauthenticated GET endpoints; [SmartRecruiters' Posting API](https://developers.smartrecruiters.com/docs/posting-api)
documents access to public postings and its [endpoints](https://developers.smartrecruiters.com/docs/endpoints)
describe listing and detail requests. Public access or a provider statement
does not by itself establish an individual employer's redistribution terms.

For the 28-source snapshot, a normal complete update makes nine Greenhouse GETs,
at least 18 Lever GETs plus extra pages, and roughly 139 Meritis SmartRecruiters
GETs (two listing pages plus 137 details). Actual counts vary with feed size and
retryable errors; these are planning estimates, not rate limits or hard caps.
The connector throttles SmartRecruiters detail fetches to about 10 per second
and backs off/retries selected errors. Large SmartRecruiters boards are **not**
enabled without further request budgeting; filtered snapshots must never be
treated as complete snapshots for closure detection.

## Job boards requiring further investigation

| Source | Status for this project |
| --- | --- |
| LinkedIn | No automated scraping planned: [LinkedIn prohibits third-party scraping and automated activity](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin). Link to employer originals when available. |
| Welcome to the Jungle | No connector enabled. Its [site terms](https://www.welcometothejungle.com/en/pages/terms) prohibit scraping content, subject to specified exceptions; a separate authorized feed or agreement would be needed for this use. |
| HelloWork | No connector enabled. Its [recruiter terms](https://recruteur.hellowork.com/cgv-abo-lib) describe automated users of the job database as non-legitimate and restrict systematic extraction. Their applicability depends on the service and agreement; investigate an authorized feed or partnership before integration. |
| Apec | No connector enabled. [Apec's site terms](https://www.apec.fr/infos-legales/infos-cgu.html) prohibit automated navigation and capturing content from its site and job database. Obtain suitable authorized access before integrating. |
| France Travail | No connector enabled. [The official API listing](https://www.data.gouv.fr/dataservices/api-offres-demploi) states the job-offers API is not currently exposed while distribution and reuse are reviewed; access inquiries go through France Travail. Recheck before adding. |
| Choisir le service public | No connector enabled. Its [open-licensed weekly dataset](https://www.data.gouv.fr/datasets/les-offres-diffusees-sur-choisir-le-service-public) includes historical postings and no job URL field; its limited RSS feed is not a complete snapshot. See [issue #18](https://github.com/zakariaabou/france-tech-jobs/issues/18) for the work needed to verify links and handle incremental updates safely. |
| EURES | No connector enabled. The [official Find a Job terms](https://europa.eu/eures/portal/jv-se/home?lang=en) prohibit extraction and republication through scraping and reserve API data extraction to recognized EURES partners. |
| Adzuna | No connector enabled. [Official API terms](https://developer.adzuna.com/docs/terms_of_service) permit some listing publication, but require a registered API key; licensing and restrictions depend on usage. Account access and conditions for this project are unverified. |
| Remotive | No connector enabled. Its [public API terms](https://remotive.com/remote-jobs/api) require explicit Remotive attribution and a link to each Remotive posting; data is delayed 24 hours and submission to third-party job sites is restricted. Its [general site terms](https://remotive.com/terms-of-use) also contain scraping and redistribution restrictions. The interaction between those terms and this repository's use should be confirmed before integration. |

Other researched boards, such as Sopra Steria and Devoteam on SmartRecruiters,
returned non-empty listings but are substantially larger; they are not yet in
the pilot because an unfiltered detail request per posting would be costly.
They should be reassessed once bounded filtering and request budgets are in
place. Capgemini's tested SmartRecruiters company identifier returned no
postings and has not been enabled. None of these observations proves that an
employer has no jobs on other platforms.
