"""
Bước 1 — Feature Engineering
Idea #13: Customer Segmentation (Fashion marketplace users)

Input : data/utkarshx27_users_clean.csv  (98,913 users x 24 cols)
Output: outputs/features.csv (feature đã chọn, chưa scale)
        outputs/features_summary.txt

Logic:
- Đây là dữ liệu USER PROFILE + ENGAGEMENT của 1 sàn marketplace thời trang
  (kiểu Vestiaire Collective / Vinted) chứ không phải transaction log,
  nên KHÔNG có RFM cổ điển (Recency/Frequency/Monetary theo đơn hàng).
  Ta thay bằng "Engagement RFM":
    R (Recency)   -> daysSinceLastLogin (đảo dấu: càng nhỏ càng active)
    F (Frequency) -> seniorityAsMonths, socialNbFollows... (mức độ gắn bó)
    M (Monetary proxy) -> productsBought, productsSold (hành vi mua/bán thật)
- Dữ liệu rất lệch (long-tail): 78% user gần như không hoạt động,
  outlier cực đoan ở daysSinceLastLogin (max ~737,028 ngày -> lỗi log).
  => Cap outlier theo percentile 99, sau đó log1p toàn bộ biến đếm.
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # customer_segmentation/
RAW_PATH = ROOT / "data" / "utkarshx27_users_clean.csv"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / "features.csv"

df = pd.read_csv(RAW_PATH)
print(f"Loaded raw data: {df.shape}")

# ----------------------------------------------------------------------
# 1. Loại cột không dùng cho clustering (ID, hằng số, hoặc bị lệch quá mức)
# ----------------------------------------------------------------------
# - identifierHash: chỉ để join lại sau, không phải feature
# - type: hằng số 100% "user" -> vô nghĩa
# - civilityTitle: trùng thông tin với gender/civilityGenderId
# - seniority (đơn vị lạ, không rõ nghĩa) -> đã có seniorityAsMonths/Years thay thế
# - country / countryCode / language: quá nhiều category (>100 quốc gia),
#   để riêng cho phân tích mô tả cluster sau này, KHÔNG đưa vào clustering
#   (one-hot 100+ cột sẽ làm loãng distance metric của K-Means)
id_col = "identifierHash"
descriptive_cols = ["country", "countryCode", "language", "gender", "civilityTitle"]

# ----------------------------------------------------------------------
# 2. Xử lý outlier cực đoan: daysSinceLastLogin có giá trị lỗi (737,028 ngày ~ 2000 năm)
#    Cap tại percentile 99 để tránh outlier "ăn" hết variance khi scale.
# ----------------------------------------------------------------------
cap_cols = [
    "socialNbFollowers", "socialNbFollows", "socialProductsLiked",
    "productsListed", "productsSold", "productsWished", "productsBought",
    "daysSinceLastLogin",
]
for c in cap_cols:
    cap = df[c].quantile(0.99)
    n_capped = (df[c] > cap).sum()
    df[c] = df[c].clip(upper=cap)
    print(f"  cap {c:<22} at p99={cap:>10.1f}  -> {n_capped} values capped")

# productsPassRate đã là % (0-100), giữ nguyên nhưng clip về [0,100] cho chắc
df["productsPassRate"] = df["productsPassRate"].clip(0, 100)

# ----------------------------------------------------------------------
# 3. Feature engineering — nhóm "Engagement RFM" + tỉ lệ hành vi
# ----------------------------------------------------------------------
feat = pd.DataFrame(index=df.index)
feat[id_col] = df[id_col]

# --- Recency: đảo dấu daysSinceLastLogin thành "độ tươi mới" (log để nén đuôi dài) ---
feat["recency_days"] = df["daysSinceLastLogin"]
feat["log_recency"] = np.log1p(df["daysSinceLastLogin"])

# --- Tenure (gắn bó lâu dài với platform) ---
feat["seniority_months"] = df["seniorityAsMonths"]

# --- Social engagement ---
feat["log_followers"] = np.log1p(df["socialNbFollowers"])
feat["log_follows"] = np.log1p(df["socialNbFollows"])
feat["log_products_liked"] = np.log1p(df["socialProductsLiked"])

# --- Seller-side behavior ---
feat["log_products_listed"] = np.log1p(df["productsListed"])
feat["log_products_sold"] = np.log1p(df["productsSold"])
feat["products_pass_rate"] = df["productsPassRate"]  # % sp bị từ chối khi bán

# --- Buyer-side behavior ---
feat["log_products_wished"] = np.log1p(df["productsWished"])
feat["log_products_bought"] = np.log1p(df["productsBought"])

# --- Tỉ lệ hành vi mua vs bán (ai chủ yếu là buyer, ai là seller/cả hai) ---
total_activity = df["productsBought"] + df["productsSold"] + 1e-6
feat["buy_ratio"] = df["productsBought"] / total_activity  # gần 1 = buyer, gần 0 = seller

# --- Chỉ số "wishlist-to-buy conversion" (mức độ chuyển đổi ý định thành hành động) ---
feat["wish_to_buy"] = df["productsBought"] / (df["productsWished"] + 1)

# --- App usage (mobile-first user hay không) ---
feat["has_any_app"] = df["hasAnyApp"].astype(int)
feat["has_profile_picture"] = df["hasProfilePicture"].astype(int)

# --- Tổng mức độ hoạt động (dùng để lọc user hoàn toàn inactive nếu cần) ---
feat["total_activity_raw"] = (
    df["productsBought"] + df["productsSold"] + df["productsWished"] + df["socialProductsLiked"]
)
feat["is_inactive"] = (feat["total_activity_raw"] == 0).astype(int)

# ----------------------------------------------------------------------
# 4. Giữ lại cột mô tả (để profiling cluster sau, KHÔNG dùng để cluster)
# ----------------------------------------------------------------------
for c in descriptive_cols:
    feat[c] = df[c]

print(f"\nFeature set shape: {feat.shape}")
print(f"Inactive users (0 mọi hành vi mua/bán/wish/like): {feat['is_inactive'].sum()} "
      f"({feat['is_inactive'].mean()*100:.1f}%)")

feat.to_csv(OUT_PATH, index=False)
print(f"\nSaved -> {OUT_PATH}")

with open(OUT_DIR / "features_summary.txt", "w") as f:
    f.write("FEATURE ENGINEERING SUMMARY\n")
    f.write("=" * 60 + "\n")
    f.write(f"Raw shape: {df.shape}\n")
    f.write(f"Feature shape: {feat.shape}\n")
    f.write(f"Inactive users: {feat['is_inactive'].sum()} ({feat['is_inactive'].mean()*100:.1f}%)\n\n")
    f.write(feat.describe().T.to_string())
print(f"Saved -> {OUT_DIR / 'features_summary.txt'}")
