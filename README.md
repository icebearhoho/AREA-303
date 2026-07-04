# AREA 303 — AI/ML E-Commerce Platform

An AI/ML e-commerce application built for **AREA 303 ("The Buffalo Playground")** —
the AI/ML + Prototype track, e-commerce focus. The platform bundles **17 AI-powered
features** across NLP, time series, computer vision, generative AI, and behavioral AI,
targeting **clothing & accessories and cosmetics/personal care** on Vietnamese
marketplaces (Shopee, Tiki, Lazada).

The goal: give sellers and shoppers a smarter storefront — better search, pricing,
recommendations, review trust, demand planning, and customer insight — grounded in
real Vietnamese e-commerce data.

## The 17 ideas

| Category | Ideas |
|---|---|
| **NLP** | #01 Review Sentiment · #05 Fake Review Detection · #08 Social Trend Analyzer · #09 Content Generator |
| **Time Series** | #02 Dynamic Pricing · #06 Demand Forecasting · #15 Price Sensitivity · #16 Supply-Chain Disruption |
| **Computer Vision** | #07 Visual Search · #12 Virtual Try-On |
| **Generative AI** | #03 Personal Shopper · #11 Recommendation System · #14 Negotiation Chatbot · #17 Seller Intelligence |
| **Behavioral AI** | #04 Churn Prediction · #10 Return Prediction · #13 Customer Segmentation |

Each idea is powered by 1–2 curated datasets and a recommended model. Full
dataset-to-idea mapping and model choices: `model suggestions.xlsx` and
`AREA303_Dataset_Model_Plan.docx`.

## What's in this repository

This repo is the **data foundation** for the platform — the sourcing, cleaning, and
packaging of every dataset the 17 features build on. It is organized so any teammate
(or their AI assistant) can pick up one idea and start modeling immediately.

- **Cleaned, analysis-ready data** in three pipelines — reviews/text, transactions/behavior, catalog/images.
- **Per-idea folders** (`dataset/by_idea/idea_XX_*/`) that bundle each idea's datasets with:
  - **`AI_BRIEF.md`** — a self-contained briefing to paste into an AI assistant (goal, recommended model, decoded data, pitfalls, first steps).
  - **`DATA_DICTIONARY.md`** — every column explained, coded values decoded.
- **`DATA_REPORT.md`** — one-page overview of all datasets.
- Reproducible **download → clean → validate → package** scripts.

> Full pipeline documentation and reproduction steps: **[`dataset/README.md`](dataset/README.md)**.

## Quick start

```bash
pip install -r requirements.txt
# then reproduce the data (see dataset/README.md for the full ordered run):
python download_hf.py && python download_kaggle.py
python clean_pipeline1.py && python clean_pipeline2.py && python clean_pipeline3.py
python finalize_datasets.py && python generate_data_dicts.py && python generate_ai_briefs.py
```

The raw + processed data (~11 GB) is **gitignored** and rebuilt from these scripts —
the repo itself stays lightweight.

## Tech stack

Python · pandas · PyArrow (Parquet) · HuggingFace Hub · Kaggle API.
Modeling (per idea, planned): PhoBERT/ViSoBERT, XGBoost, CLIP + FAISS, Prophet,
Gemini via LangChain, and more — see the plan documents.

## Status

✅ Data foundation complete — all datasets sourced, cleaned, validated, documented,
and packaged per idea. Modeling of the 17 features builds on top of `dataset/by_idea/`.

## Team

Built by a 5-person team for AREA 303. This repository is the **data-processing
workstream**.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style, and the PR process.
