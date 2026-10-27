# Pilot verification

On 2026-10-27, a live update fetched all 14 configured employer feeds successfully. The generated catalogue contained 12 eligible listings: ten in France and two international. The France AI Engineering page was empty under the current conservative eligibility rules; this is not a statement about all available AI jobs. The listings and their state can change after this snapshot.

The first pilot includes junior and mid-level software roles, mid-level data roles and international junior software roles. The [classification evaluation](classification-evaluation.md) documents a small manual review of job descriptions, including an AI role withheld for ambiguous experience. The selection rules intentionally omit uncertain experience and geography; a representative precision/recall measurement and broader source coverage remain follow-up work.

Automated tests cover source response completeness, classification, source failures, duplicate URLs, Markdown rendering and job lifecycle transitions. The GitHub workflow must also be verified on the remote repository after deployment; local testing alone does not establish that scheduled updates run successfully.
