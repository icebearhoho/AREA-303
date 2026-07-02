# AI Brief — Idea #04: Customer Churn

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Predict which customers are likely to churn so the team can retain them.

## Recommended approach
- XGBoost + SHAP (explainability)
- Logistic regression baseline

## Datasets for this idea

### `rees46_churn_clean.parquet`  —  REES46 churn-modeling table: 276 engineered behavioral features + churn target.

*112,610 rows · 276 columns*

This table has **276 columns**. The first columns are `row_id`, `user_id`, and the targets `target_event` (0=retained, 1=churned), `target_revenue`, `target_customer_value`. The remaining ~270 are engineered features: each base behavioral metric (click_count, view_count, cart_count, purchase_count, revenue, recency, session/inter-session times, etc.) is aggregated per user as `_mean`, `_sum`, `_min`, `_max`, `_stddev`, `_cv` (coefficient of variation), plus monthly lags (`_lagN`, `_ma3`) and 40+ `view_latent_factor*` / 18 `purchase_latent_factor*` (matrix-factorization embeddings). Use feature selection before modeling.


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
rees46_churn = pd.read_parquet(r"rees46_churn_clean.parquet")   # or pd.read_csv(r"rees46_churn_clean.csv")
utkarshx27_users = pd.read_parquet(r"utkarshx27_users_clean.parquet")   # or pd.read_csv(r"utkarshx27_users_clean.csv")
```

## Watch out for
- Target already balanced — no resampling needed
- 276 pre-engineered features → do feature selection first

## Suggested first steps
1. Train on rees46_churn (target_event); it's already ~32% balanced
2. Feature-select from the 276 features, then SHAP for top churn drivers
3. Cross-check engagement signals from utkarshx27_users

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
