# AREA 303

Data pipeline and model planning for **AREA 303 ("The Buffalo Playground")** — AI/ML + Prototype track, e-commerce focus. Product focus: **clothing & accessories + cosmetics/personal care** on Vietnamese platforms (Shopee, Tiki, Lazada).

This repo covers the **data processing** workstream: sourcing, downloading, cleaning, and validating the datasets that feed 17 candidate product ideas (NLP, time series, computer vision, generative AI, behavioral AI).

## Repo structure

```
.
├── dataset/                      # raw + processed data (gitignored — see below)
│   ├── 01_reviews_text/          # raw downloads: NLP sources
│   ├── 02_transactions_behavior/ # raw downloads: time-series + behavioral
│   ├── 03_catalog_images/        # raw downloads: CV + generative
│   ├── 04_live_apis_tools/       # API/tool sources (no static files)
│   ├── processed/                # cleaned, analysis-ready files (.parquet + .csv)
│   └── by_idea/                  # cleaned files grouped one folder per idea
├── download_hf.py                # download datasets from HuggingFace
├── download_kaggle.py            # download datasets from Kaggle
├── clean_pipeline1.py            # cleaning: reviews / text
├── clean_pipeline2.py            # cleaning: transactions / behavior
├── clean_pipeline3.py            # cleaning: catalog / images
├── check_data_quality.py         # per-dataset adequacy/quality report
├── validate_datasets.py          # post-download validation checks
├── finalize_datasets.py          # assembles dataset/by_idea/ from processed/
├── generate_data_dicts.py        # generates data dictionaries
├── generate_ai_briefs.py         # generates per-idea AI briefs
├── DATA_REPORT.md                # what each cleaned dataset contains, how to load it
├── context_handoff.md            # project/team context for onboarding (human or AI)
├── data_sources_17_ideas.html    # source table: all candidate dataset URLs per idea
├── dataset review v3.xlsx        # dataset usability review (Usable/Questionable/Not Usable)
├── model suggestions.xlsx        # model recommendations per idea
├── AREA303_Dataset_Model_Plan.docx  # full write-up: datasets + models
└── requirements.txt
```

**`dataset/` is mostly gitignored.** Raw and processed data files (`.parquet`, `.csv`, images, archives) are excluded — they're large (~11 GB) and fully reproducible from the scripts below. Small documentation that ships *with* each dataset (`README.md`, `_SOURCE.txt`) is kept so the structure is browsable on GitHub without downloading anything.

## Setup

```bash
pip install -r requirements.txt
```

Kaggle downloads require a `kaggle.json` API token in `~/.kaggle/` (never commit this file — it's gitignored).

## Reproducing the data pipeline

```bash
python download_hf.py          # pull HuggingFace-hosted datasets
python download_kaggle.py      # pull Kaggle-hosted datasets
python clean_pipeline1.py      # clean reviews/text sources
python clean_pipeline2.py      # clean transactions/behavior sources
python clean_pipeline3.py      # clean catalog/image sources
python validate_datasets.py    # sanity-check the outputs
python check_data_quality.py   # per-dataset adequacy report
python finalize_datasets.py    # assemble dataset/by_idea/
```

See **`DATA_REPORT.md`** for what each cleaned file contains (rows, columns, which idea it feeds, how to load it), and **`context_handoff.md`** for the full project background.

## The 17 ideas

| Category | Ideas |
|---|---|
| NLP | #01 Review Sentiment, #05 Fake Review Detection, #08 Social Trends, #09 Content Generator |
| Time Series | #02 Dynamic Pricing, #06 Demand Forecasting, #15 Price Sensitivity, #16 Supply Chain |
| Computer Vision | #07 Visual Search, #12 Virtual Try-On |
| Generative AI | #03 Personal Shopper, #11 RecSys, #14 Negotiation Chatbot, #17 Seller Intelligence |
| Behavioral AI | #04 Churn Prediction, #10 Return Prediction, #13 Segmentation |

Full dataset-to-idea mapping and model recommendations: `model suggestions.xlsx` / `AREA303_Dataset_Model_Plan.docx`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style, and the PR process.
