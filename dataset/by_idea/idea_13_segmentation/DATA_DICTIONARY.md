# Idea #13 — Segmentation — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

