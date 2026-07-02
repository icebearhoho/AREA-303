# AI Brief — Idea #13: Segmentation

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Cluster customers into personas for targeting.

## Recommended approach
- K-Means++ + UMAP (visualization)
- XGBoost to score new users into a segment

## Datasets for this idea

### `utkarshx27_users_clean.parquet`  —  Fashion marketplace user profiles & engagement.

*98,913 rows · 24 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `identifierHash` | int64 |  | e.g. -7279641312655250028 |
| `type` | large_string |  | e.g. user |
| `country` | large_string |  | e.g. Etats-Unis |
| `language` | large_string | Language of the text. | e.g. en |
| `socialNbFollowers` | int64 |  | e.g. 3 |
| `socialNbFollows` | int64 |  | e.g. 8 |
| `socialProductsLiked` | int64 |  | e.g. 0 |
| `productsListed` | int64 |  | e.g. 0 |
| `productsSold` | int64 |  | e.g. 0 |
| `productsPassRate` | double |  | e.g. 0.0 |
| `productsWished` | int64 |  | e.g. 0 |
| `productsBought` | int64 |  | e.g. 0 |
| `gender` | large_string |  | e.g. F |
| `civilityGenderId` | int64 |  | values: `2`, `1`, `3` |
| `civilityTitle` | large_string |  | e.g. mrs |
| `hasAnyApp` | bool |  | values: `False`, `True` |
| `hasAndroidApp` | bool |  | values: `False`, `True` |
| `hasIosApp` | bool |  | values: `False`, `True` |
| `hasProfilePicture` | bool |  | values: `True`, `False` |
| `daysSinceLastLogin` | int64 |  | e.g. 709 |
| `seniority` | int64 |  | values: `3205`, `3204`, `3203` |
| `seniorityAsMonths` | double |  | e.g. 106.83 |
| `seniorityAsYears` | double |  | e.g. 8.9 |
| `countryCode` | large_string |  | e.g. us |

## How to load
```python
import pandas as pd
utkarshx27_users = pd.read_parquet(r"utkarshx27_users_clean.parquet")   # or pd.read_csv(r"utkarshx27_users_clean.csv")
```

## Watch out for
- utkarshx27_users is per-user; country_agg is a separate aggregate — don't mix
- Standardize features before clustering

## Suggested first steps
1. Use utkarshx27_users features
2. Standardize, reduce with UMAP, cluster K-Means++ (silhouette to pick k)
3. Profile clusters; train a classifier for real-time segment scoring

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
