# Idea #04 — Customer Churn — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

