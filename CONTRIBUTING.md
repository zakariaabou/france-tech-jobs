# Contributing

You can [suggest an employer](https://github.com/zakariaabou/france-tech-jobs/issues/new?template=source-suggestion.md) or [report an outdated job](https://github.com/zakariaabou/france-tech-jobs/issues/new?template=stale-job.md). Please include the original employer URL when possible; do not share applicant data.

To add a source, check its terms and whether access and reuse are suitable first. Add the company to `config/sources.json` and document the evidence in `docs/sources.md`. Use a unique source ID, one of the supported connector types and the correct company board identifier. Test with a small live pilot and ensure job URLs lead to actual vacancies. Never add credentials to the repository.

Run the checks from the repository root:

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pip install ruff==0.16.3
python -m ruff check --select E9,F63,F7,F82 src tests
PYTHONPATH=src python -m france_tech_jobs
```

On PowerShell, set `$env:PYTHONPATH = 'src'` before running the Python commands. The second command accesses configured sources and updates the stored data and generated pages.
