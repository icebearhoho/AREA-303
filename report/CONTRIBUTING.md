# Contributing

Guidelines for the AREA 303 team (5 members) working in this repo.

## Branches

- `main` is always in a working state — no direct pushes.
- Branch off `main` per task: `<type>/<short-description>`
  - `data/add-tiki-pipeline`
  - `fix/sephora-null-handling`
  - `docs/update-data-report`
  - Types: `data`, `feat`, `fix`, `docs`, `chore`

## Commits

Keep commits scoped and use a short imperative summary:

```
clean_pipeline2: dedupe rees46 churn rows
```

## Pull requests

1. Open a PR from your branch into `main` using the PR template.
2. Fill in what changed and how it was tested/verified (e.g. re-ran `validate_datasets.py`).
3. Request review from at least one teammate before merging.
4. Squash-merge once approved; delete the branch after merge.

## Data changes

- Never commit files under `dataset/` except the small doc files (`README.md`, `_SOURCE.txt`) that already ship with each source — see `.gitignore`.
- If a cleaning script's output schema changes, update `DATA_REPORT.md` in the same PR.
- Run `validate_datasets.py` and `check_data_quality.py` before opening a PR that touches a `clean_pipeline*.py` script.

## Reporting issues

Use the issue templates (bug report / feature or task request) so the rest of the team has enough context to pick it up.
