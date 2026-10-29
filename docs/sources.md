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
| [NEXTON](https://careers.smartrecruiters.com/NEXTON) | SmartRecruiters | French technology consultancy / ESN | [Board JSON](https://api.smartrecruiters.com/v1/companies/NEXTON/postings?limit=1) | 167 postings on 2026-10-28; French software, data and machine-learning titles; full fetch completed in about 103 seconds |
| [Sia](https://careers.smartrecruiters.com/Sia) | SmartRecruiters | Consultancy / ESN | [Board JSON](https://api.smartrecruiters.com/v1/companies/Sia/postings?limit=1) | 519 postings; 19 target-title prospects on 2026-10-28 |
| [Scalian](https://careers.smartrecruiters.com/Scalian) | SmartRecruiters | Technology consultancy / ESN | [Board JSON](https://api.smartrecruiters.com/v1/companies/Scalian/postings?limit=1) | 756 postings; 88 target-title prospects on 2026-10-28 |
| [Iliad / Free](https://careers.smartrecruiters.com/Iliad-Free) | SmartRecruiters | Telecommunications / technology employer | [Board JSON](https://api.smartrecruiters.com/v1/companies/Iliad-Free/postings?limit=1) | 285 postings; 6 target-title prospects on 2026-10-28 |
| [Magellan](https://careers.smartrecruiters.com/Magellan) | SmartRecruiters | Technology consultancy | [Board JSON](https://api.smartrecruiters.com/v1/companies/Magellan/postings?limit=1) | 284 postings; 12 target-title prospects on 2026-10-28 |
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
`owner`. The registry records when each endpoint's unauthenticated technical
access was verified; provider documentation describes public access, and
employer-specific aggregation/reuse conditions remain **unverified**;
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

### SmartRecruiters request budget and coverage

For the six configured SmartRecruiters sources, the connector reads up to 50
listing pages (5,000 postings) per board, using 100 postings per page. It then
fetches details for at most 100 selected postings per board per run. These are
limits on logical requests; each may be attempted up to three times on selected
transient errors, so actual HTTP attempts can be higher. Calls are sequential
with a 0.2-second pause after each successful listing or detail request. The
[provider documents](https://developers.smartrecruiters.com/docs/customer-overview)
a 10 requests/second limit and 429 responses; we pause at least 0.2 seconds
between successful calls, use exponential backoff on transient errors, and
honor `Retry-After` up to 30 seconds. If the provider requests a longer delay,
the source fails safely and is tried on the next run. The current 20-second
network timeout is shorter than the provider's recommended 128 seconds and may
therefore mark a slow but available source unverified.

The selection uses the same current category and obvious senior/intern title
rules as the classifier, then fetches full details for experience, contract,
location and the real posting link. The public listing and detail title could
disagree, and unusual titles can be missed; future changes to category rules
must preserve this dependency. Missing titles fail the source instead of being
silently filtered. If candidate counts exceed the detail budget, an ID-sorted
window rotates daily; deferred jobs are unverified, so they may disappear from
published pages until their details are fetched again.

These sources are explicitly partial: omissions are never proof of closure.
An old job that is listed but not checked in detail becomes unknown, even if
previously closed. Unknown history is kept for up to 180 days after a successful partial check
first marks it unverified, with at most 1,000 unknown records per source.
Failed and disabled sources are exempt until a successful refresh. Eviction
is storage cleanup, not a closure claim; see [retention details](data-lifecycle.md).
Changing totals, incorrect page lengths/offsets, duplicate IDs, missing titles,
detail failures and source outages fail safely. Equal totals cannot prove a
stable list if postings are replaced during pagination; partial status avoids
falsely closing omitted jobs but cannot guarantee that every candidate was seen.
The workflow logs total postings, candidates and selected details per board.
The 2026-10-28 Scalian pilot had 756 postings: roughly eight listing requests
and 88 selected details instead of 756 detail requests. Counts change daily.

Sia's [corporate site notice](https://www.sia-partners.com/fr/mentions-legales)
reserves reproduction rights; its application to the separate SmartRecruiters
feed is not established. No affirmative employer-specific reuse authorization
was found for Sia, Scalian, Iliad / Free or Magellan. Public API access alone
does not grant that authorization; the registry records this uncertainty.

## Groupe BPCE open-data employer feed

The [Groupe BPCE public jobs dataset](https://www.data.gouv.fr/datasets/groupe-bpce-offres-emploi-publiques),
created and published by **BPCE - DRH Groupe**, is available under the
[Licence Ouverte / Open Licence 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf).
The publisher expressly permits displaying the data on job platforms and reports
four daily updates. We select only fields needed for the listing; recruiter
names and emails are discarded. Job descriptions are used temporarily for
classification and not stored. The listed URL leads to the employer's own
posting. Dates shown on this project are observation dates, not the dataset's
last modification timestamps. Multiple locations for the same reference and
URL are combined. Classifications are derived by this project.

The connector downloads at most 25 MiB and checks record counts and dataset
version before and after the export. A changed, malformed, incomplete or more
than 48-hour-old snapshot fails safely and existing jobs become unverified.
The project runs daily, so changes may take up to the next successful run to
appear; job availability may change meanwhile. The source portal has announced
its [decommissioning in 2027](https://bpce.opendatasoft.com/explore/assets/groupe-bpce-offres-emploi/),
so the connector may need a replacement. On 2026-10-28 the export contained
1,867 rows, including multiple rows for some roles; counts change over time.

## Job boards requiring further investigation

| Source | Status for this project |
| --- | --- |
| LinkedIn | No automated scraping planned: [LinkedIn prohibits third-party scraping and automated activity](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin). Link to employer originals when available. |
| Welcome to the Jungle | No connector enabled. Its [site terms](https://www.welcometothejungle.com/en/pages/terms) prohibit scraping content, subject to specified exceptions; a separate authorized feed or agreement would be needed for this use. |
| HelloWork | No connector enabled. Its [recruiter terms](https://recruteur.hellowork.com/cgv-abo-lib) describe automated users of the job database as non-legitimate and restrict systematic extraction. Their applicability depends on the service and agreement; investigate an authorized feed or partnership before integration. |
| Apec | No connector enabled. [Apec's site terms](https://www.apec.fr/infos-legales/infos-cgu.html) prohibit automated navigation and capturing content from its site and job database. Obtain suitable authorized access before integrating. |
| France Travail | No connector enabled. [The official API listing](https://www.data.gouv.fr/dataservices/api-offres-demploi) states the job-offers API is not currently exposed while distribution and reuse are reviewed; access inquiries go through France Travail. Recheck before adding. |
| Choisir le service public | No connector enabled. Its [open-licensed weekly dataset](https://www.data.gouv.fr/datasets/les-offres-diffusees-sur-choisir-le-service-public) includes historical postings and no job URL field; its limited RSS feed is not a complete snapshot. Its [site legal notice](https://choisirleservicepublic.gouv.fr/mentions-legales/) limits access to consulting offers and applying; the dataset licence does not establish permission to crawl the website to verify job status. See [issue #18](https://github.com/zakariaabou/france-tech-jobs/issues/18) for remaining work. |
| EURES | No connector enabled. The [official Find a Job terms](https://europa.eu/eures/portal/jv-se/home?lang=en) prohibit extraction and republication through scraping and reserve API data extraction to recognized EURES partners. |
| Adzuna | No connector enabled. [Official API terms](https://developer.adzuna.com/docs/terms_of_service) permit some listing publication, but require a registered API key; licensing and restrictions depend on usage. Account access and conditions for this project are unverified. |
| Remotive | No connector enabled. Its [public API terms](https://remotive.com/remote-jobs/api) require explicit Remotive attribution and a link to each Remotive posting; data is delayed 24 hours and submission to third-party job sites is restricted. Its [general site terms](https://remotive.com/terms-of-use) also contain scraping and redistribution restrictions. The interaction between those terms and this repository's use should be confirmed before integration. |

Other researched boards, such as Sopra Steria and Devoteam on SmartRecruiters,
returned non-empty listings but are not yet enabled. Sopra Steria had 2,062
postings and 154 target-title prospects in the 2026-10-28 pilot, exceeding the
100-detail daily limit; a rotating subset is not comprehensive. Capgemini's tested SmartRecruiters company identifier returned no
postings and has not been enabled. None of these observations proves that an
employer has no jobs on other platforms.
