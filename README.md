# France Tech Jobs

A France-first collection of **junior, new-graduate and mid-level** technology jobs, with a separate international section. Internships and alternance are excluded.

## Browse jobs

| | Data Engineering | AI Engineering | Software Engineering |
| --- | --- | --- | --- |
| 🇫🇷 France | [Data jobs](jobs/france-data.md) | [AI jobs](jobs/france-ai.md) | [Software jobs](jobs/france-software.md) |
| 🌍 International | [Data jobs](jobs/international-data.md) | [AI jobs](jobs/international-ai.md) | [Software jobs](jobs/international-software.md) |

[Recently added](jobs/recent.md) · [Potential matches — verify requirements](jobs/review.md) · [Suggest a job or employer](CONTRIBUTING.md) · [How jobs are selected](docs/scope.md) · [Sources and coverage](docs/sources.md)

AI Engineering includes machine learning, generative AI, MLOps, NLP and related engineering roles. Jobs may appear in more than one category. Location, contract and remote status are shown only when available; remote eligibility may depend on the employer's restrictions. Apply on the linked employer page.

The separate potential matches page includes active roles where experience or location needs checking. It explains what is uncertain and has views for [France](jobs/review-france.md), [international](jobs/review-international.md) and [unknown locations](jobs/review-unknown.md). Each view shows at most 100 roles by default; maintainers can set `review_limit` from 0 to 1000 in `config/sources.json`. Clearly excluded senior, internship and alternance roles are not included. Always check the employer's requirements and work authorization before applying.

## Subscribe to RSS

Copy a feed link into your preferred RSS reader. Feeds contain confirmed active jobs only; potential matches stay in the review pages.

| Region | Data Engineering | AI Engineering | Software Engineering |
| --- | --- | --- | --- |
| France | [Data RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/france-data.xml) | [AI RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/france-ai.xml) | [Software RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/france-software.xml) |
| International | [Data RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/international-data.xml) | [AI RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/international-ai.xml) | [Software RSS](https://raw.githubusercontent.com/zakariaabou/france-tech-jobs/main/feeds/international-software.xml) |

Each item identifies its source and first observation date. A posting date is included only when the source supplies a timestamp with a time zone. If a source fails, its jobs are temporarily omitted until verified again; closed jobs leave the feed. Feeds do not announce closures. Feed readers differ in how they retain or redisplay older entries.

## Updates and coverage

The project uses a scheduled daily GitHub Actions workflow and can also be updated manually. Each list shows the most recent successful pipeline run in UTC. A source error does not imply its jobs have closed: listings from that source are held as unverified until the source succeeds again. The pages cover the configured employers, not the entire job market. Experience and location rules are intentionally conservative; some relevant roles may be missed. [Read the selection policy](docs/scope.md).

BPCE listings use [Groupe BPCE's open jobs data](https://www.data.gouv.fr/datasets/groupe-bpce-offres-emploi-publiques), published by BPCE - DRH Groupe under the [Open Licence 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf). Classification is performed by this project; the original job posting remains the application reference. See [source details](docs/sources.md) for freshness and coverage limits.

## Run locally

Requires Python 3.11 or newer; there are no third-party runtime dependencies. From the repository root:

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m france_tech_jobs
```

On Windows PowerShell, run `$env:PYTHONPATH = 'src'` first, then run the Python commands. Updating fetches the sources in `config/sources.json`, updates `data/jobs.json` and generates pages in `jobs/` and RSS feeds in `feeds/`. Original descriptions are used for classification and are not stored in the public data file. A run where every source fails leaves the existing output untouched.

The code is under active development; review the [open issues](https://github.com/zakariaabou/france-tech-jobs/issues) for remaining work.
