# AREA 303 — Data Processing Pipeline

> This documents the **data-processing workstream**: sourcing, downloading, cleaning,
> validating, and packaging the datasets that feed the 17 candidate ideas.
> Run all commands **from the repository root**. For the project overview, see the
> [top-level README](../README.md).

Product focus: **clothing & accessories + cosmetics/personal care** on Vietnamese
platforms (Shopee, Tiki, Lazada).

## Repo structure

```
.
├── dataset/                      # raw + processed data (data files gitignored — see below)
│   ├── 01_reviews_text/          # raw downloads: NLP sources
│   ├── 02_transactions_behavior/ # raw downloads: time-series + behavioral
│   ├── 03_catalog_images/        # raw downloads: CV + generative
│   ├── 04_live_apis_tools/       # API/tool sources (no static files)
│   ├── processed/                # cleaned, analysis-ready files (.parquet + .csv)
│   └── by_idea/                  # cleaned files grouped one folder per idea (+ AI_BRIEF.md, DATA_DICTIONARY.md)
├── code/                          # all pipeline scripts — local only, not pushed to GitHub
│   ├── download_hf.py            # download datasets from HuggingFace
│   ├── download_kaggle.py        # download datasets from Kaggle
│   ├── clean_pipeline1.py        # cleaning: reviews / text
│   ├── clean_pipeline2.py        # cleaning: transactions / behavior
│   ├── clean_pipeline3.py        # cleaning: catalog / images
│   ├── check_data_quality.py     # per-dataset adequacy/quality report
│   ├── validate_datasets.py      # post-download validation checks
│   ├── finalize_datasets.py      # CSV versions + assembles dataset/by_idea/
│   ├── generate_data_dicts.py    # generates per-idea data dictionaries
│   └── generate_ai_briefs.py     # generates per-idea AI briefs
├── report/                       # write-ups and review docs — local only except CONTRIBUTING.md
│   ├── DATA_REPORT.md            # what each cleaned dataset contains, how to load it
│   ├── data_sources_17_ideas.html # source table: all candidate dataset URLs per idea
│   ├── dataset review v3.xlsx    # dataset usability review (Usable/Questionable/Not Usable)
│   ├── model suggestions.xlsx    # model recommendations per idea
│   ├── AREA303_Dataset_Model_Plan.docx  # full write-up: datasets + models
│   └── CONTRIBUTING.md           # branch/commit/PR guidelines — pushed (needed by the team)
├── HANDOFF.md                    # local-only session/decision log, not pushed to GitHub
└── requirements.txt
```

**Data files under `dataset/` are gitignored.** `.parquet`, `.csv`, `.jsonl`, images, and
archives are excluded — they're large (~11 GB) and fully reproducible from the scripts
below. Small docs that ship *with* each dataset (`_SOURCE.txt`, `_MANIFEST.md`,
`DATA_DICTIONARY.md`, `AI_BRIEF.md`, `USE_THESE.md`) are kept so the structure is
browsable on GitHub without downloading anything.

## Setup

```bash
pip install -r requirements.txt
```

Kaggle downloads require an API token at `~/.kaggle/access_token` (new format) or
`~/.kaggle/kaggle.json` (never commit it — gitignored).

## Reproducing the data pipeline

Run from `code/` (scripts use paths relative to the repo root's `dataset/`), in order:

```bash
cd code
python download_hf.py          # pull HuggingFace-hosted datasets
python download_kaggle.py      # pull Kaggle-hosted datasets
python clean_pipeline1.py      # clean reviews/text sources
python clean_pipeline2.py      # clean transactions/behavior sources
python clean_pipeline3.py      # clean catalog/image sources
python validate_datasets.py    # sanity-check the outputs
python check_data_quality.py   # per-dataset adequacy report
python finalize_datasets.py    # CSV versions + assemble dataset/by_idea/  (~10-14 GB)
python generate_data_dicts.py  # per-idea data dictionaries (decoded columns)
python generate_ai_briefs.py   # per-idea AI briefs
```

## Outputs a teammate cares about

- **`dataset/processed/`** — cleaned `.parquet` (fast) + `.csv` (Excel-friendly) per dataset.
- **`dataset/by_idea/idea_XX_*/`** — everything for one idea in one folder, plus:
  - `AI_BRIEF.md` — paste into an AI assistant for full context on the idea + its data.
  - `DATA_DICTIONARY.md` — every column decoded (e.g. vispam `spam_label` 0/1/2/3).
- **`report/DATA_REPORT.md`** — one-page overview of all cleaned datasets.

## Notes

- Currencies differ: VND (tiki), GBP (kanchana, asos), USD (sephora, retail_sales) — convert before combining.
- Languages differ: Vietnamese, English, multilingual — use an appropriate model.
- Skipped by design: Amazon-Reviews-2023, mkechinov, ChicagoHAI (covered by on-domain sources).
- Descoped: idea #12 Virtual Try-On image data (not feasible in the 1-month timeline).
