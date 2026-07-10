"""
Bước 2 — UMAP (giảm chiều) + K-Means++ (clustering) + đặt tên persona
Idea #13: Customer Segmentation

Input : outputs/features.csv          (từ 01_feature_engineering.py)
Output: outputs/clustered_users.csv   (mỗi user + cluster_id + persona)
        outputs/cluster_profile.csv   (trung bình feature theo cluster)
        outputs/umap_coords.npy       (cache toạ độ UMAP — xoá file này
                                        nếu muốn UMAP chạy lại từ đầu)
        figures/elbow_silhouette.png
        figures/umap_clusters.png

Ghi chú hiệu năng: UMAP trên ~99k dòng mất khoảng 60-120s tuỳ máy.
Kết quả được cache ra outputs/umap_coords.npy để các lần chạy lại sau
(khi chỉ đổi phần đặt tên persona hoặc số cluster) không phải tính lại.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import umap

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
FIG_DIR = ROOT / "figures"
OUT_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)

FEATURES_PATH = OUT_DIR / "features.csv"
UMAP_CACHE = OUT_DIR / "umap_coords.npy"

# Cột dùng để CLUSTER (chỉ numeric hành vi, bỏ ID + cột mô tả country/gender...)
CLUSTER_COLS = [
    "log_recency", "seniority_months",
    "log_followers", "log_follows", "log_products_liked",
    "log_products_listed", "log_products_sold", "products_pass_rate",
    "log_products_wished", "log_products_bought",
    "buy_ratio", "wish_to_buy",
    "has_any_app", "has_profile_picture",
]

# Cột (giá trị gốc, chưa log) dùng để PROFILE / diễn giải cluster cho dễ đọc
PROFILE_COLS = [
    "recency_days", "seniority_months",
    "log_followers", "log_follows", "log_products_liked",
    "log_products_listed", "log_products_sold", "products_pass_rate",
    "log_products_wished", "log_products_bought",
    "buy_ratio", "wish_to_buy", "has_any_app", "is_inactive",
]


def load_features() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES_PATH)
    print(f"Loaded features: {feat.shape}")
    return feat


def run_umap(X_scaled: np.ndarray) -> np.ndarray:
    """Chạy UMAP hoặc load từ cache nếu đã có."""
    if UMAP_CACHE.exists():
        print("Loading cached UMAP coords ->", UMAP_CACHE)
        return np.load(UMAP_CACHE)

    print("Running UMAP (~60-120s tuỳ máy)...")
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        n_components=2,
        metric="euclidean",
        random_state=RANDOM_STATE,
        low_memory=True,
    )
    X_umap = reducer.fit_transform(X_scaled)
    np.save(UMAP_CACHE, X_umap)
    print("UMAP done:", X_umap.shape, "-> cached to", UMAP_CACHE)
    return X_umap


def pick_best_k(X_umap: np.ndarray, k_range=range(2, 9), sample_size=15000):
    """Elbow + Silhouette trên subsample để chọn k (nhanh hơn nhiều so với full data)."""
    search_idx = np.random.choice(len(X_umap), size=min(sample_size, len(X_umap)), replace=False)
    X_search = X_umap[search_idx]

    inertias, sil_scores = [], []
    print(f"\nTesting k in {list(k_range)} on {len(X_search)}-point subsample...")
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=5, random_state=RANDOM_STATE)
        labels = km.fit_predict(X_search)
        inertias.append(km.inertia_)
        sil = silhouette_score(X_search, labels)
        sil_scores.append(sil)
        print(f"  k={k}: inertia={km.inertia_:>12.1f}   silhouette={sil:.4f}")

    # Plot elbow + silhouette
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].plot(list(k_range), inertias, "o-", color="#2563eb")
    axes[0].set_xlabel("Số cluster (k)")
    axes[0].set_ylabel("Inertia")
    axes[0].set_title("Elbow Method")
    axes[0].grid(alpha=0.3)

    axes[1].plot(list(k_range), sil_scores, "o-", color="#16a34a")
    axes[1].set_xlabel("Số cluster (k)")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].set_title("Silhouette Score theo k")
    axes[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "elbow_silhouette.png", dpi=150)
    plt.close(fig)
    print("Saved ->", FIG_DIR / "elbow_silhouette.png")

    best_k = list(k_range)[int(np.argmax(sil_scores))]
    print(f"\n>>> k tốt nhất theo silhouette: k={best_k} (score={max(sil_scores):.4f})")
    return best_k


def name_personas(feat: pd.DataFrame, cluster_profile: pd.DataFrame) -> dict:
    """
    Đặt tên persona rule-based.

    Quan trọng: z-score phải tính trên phân phối USER-LEVEL (98,913 dòng),
    KHÔNG phải trên cluster_profile (chỉ có k=6-8 hàng) — z-score trên
    một bảng vài dòng không có ý nghĩa thống kê và cho kết quả sai lệch.
    """
    global_mean = feat[PROFILE_COLS].mean()
    global_std = feat[PROFILE_COLS].std().replace(0, 1)
    z = (cluster_profile[PROFILE_COLS] - global_mean) / global_std

    names = {}
    for cid, row in z.iterrows():
        # is_inactive là TỶ LỆ 0-1 (mean của cột binary), không phải %
        inactive_rate = cluster_profile.loc[cid, "is_inactive"]
        bought_raw = cluster_profile.loc[cid, "log_products_bought"]
        sold_raw = cluster_profile.loc[cid, "log_products_sold"]
        pass_rate = cluster_profile.loc[cid, "products_pass_rate"]
        seniority_z = row["seniority_months"]
        social_z = (row["log_followers"] + row["log_follows"] + row["log_products_liked"]) / 3

        if inactive_rate >= 0.85:
            name = "Dormant / Ghost Users"
        elif sold_raw > bought_raw and sold_raw > 0.03:
            name = "Sellers (listing & selling activity)"
        elif bought_raw > sold_raw and bought_raw > 0.03:
            name = "Active Buyers"
        elif social_z > 0.8:
            name = "Social Influencers"
        elif seniority_z > 0.3 and inactive_rate < 0.6:
            name = "Loyal Long-term Users"
        elif inactive_rate >= 0.6:
            name = "At-risk / Low-activity Users"
        else:
            name = "Casual / Low-engagement Browsers"
        names[cid] = name
    return names


def plot_clusters(feat: pd.DataFrame, persona_names: dict, best_k: int):
    plt.figure(figsize=(10, 8))
    palette = plt.get_cmap("tab10")
    for cid in sorted(feat["cluster_id"].unique()):
        sub = feat[feat["cluster_id"] == cid]
        sub_plot = sub.sample(min(3000, len(sub)), random_state=RANDOM_STATE)
        plt.scatter(
            sub_plot["umap_x"], sub_plot["umap_y"],
            s=6, alpha=0.5, color=palette(cid % 10),
            label=f"C{cid} · {persona_names[cid]} ({len(sub)})",
        )
    plt.title(
        f"Customer Segmentation — UMAP + K-Means++ (k={best_k} cluster kỹ thuật)\n"
        f"Ghi chú: nhiều cluster có thể cùng persona (xem persona_profile.csv để xem bảng gộp)",
        fontsize=11,
    )
    plt.xlabel("UMAP-1")
    plt.ylabel("UMAP-2")
    plt.legend(markerscale=3, fontsize=8, loc="best")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "umap_clusters.png", dpi=150)
    plt.close()
    print("Saved ->", FIG_DIR / "umap_clusters.png")


def main():
    feat = load_features()

    X_scaled = StandardScaler().fit_transform(feat[CLUSTER_COLS])
    X_umap = run_umap(X_scaled)

    best_k = pick_best_k(X_umap)

    kmeans_final = KMeans(n_clusters=best_k, init="k-means++", n_init=10, random_state=RANDOM_STATE)
    feat["cluster_id"] = kmeans_final.fit_predict(X_umap)
    feat["umap_x"] = X_umap[:, 0]
    feat["umap_y"] = X_umap[:, 1]

    cluster_profile = feat.groupby("cluster_id")[PROFILE_COLS].mean()
    cluster_profile["n_users"] = feat.groupby("cluster_id").size()
    cluster_profile["pct_users"] = (cluster_profile["n_users"] / len(feat) * 100).round(1)
    cluster_profile = cluster_profile.round(2)

    print("\n" + "=" * 100)
    print("CLUSTER PROFILE (trung bình theo cụm)")
    print("=" * 100)
    print(cluster_profile.to_string())

    persona_names = name_personas(feat, cluster_profile)
    feat["persona"] = feat["cluster_id"].map(persona_names)
    cluster_profile["persona"] = cluster_profile.index.map(persona_names)

    print("\n" + "=" * 60)
    print("PERSONA NAMES (theo cluster kỹ thuật gốc)")
    print("=" * 60)
    for cid, name in persona_names.items():
        n = int(cluster_profile.loc[cid, "n_users"])
        pct = cluster_profile.loc[cid, "pct_users"]
        print(f"  Cluster {cid}: {name:<35} ({n:>6} users, {pct}%)")

    # ------------------------------------------------------------------
    # Bảng GỘP theo persona — dùng cho trình bày/báo cáo (business layer).
    # cluster_id vẫn giữ nguyên k=6 (đúng silhouette) cho phân tích kỹ thuật;
    # persona là tầng gộp phía trên khi nhiều cluster cùng ý nghĩa business
    # (vd. 3 cụm Dormant khác nhau về recency/seniority nhưng hành vi ~giống
    # nhau đều được gộp thành 1 persona "Dormant / Ghost Users").
    # ------------------------------------------------------------------
    persona_profile = feat.groupby("persona")[PROFILE_COLS].mean().round(2)
    persona_profile["n_users"] = feat.groupby("persona").size()
    persona_profile["pct_users"] = (persona_profile["n_users"] / len(feat) * 100).round(1)
    persona_profile["n_clusters_merged"] = feat.groupby("persona")["cluster_id"].nunique()
    persona_profile = persona_profile.sort_values("n_users", ascending=False)

    print("\n" + "=" * 100)
    print(f"PERSONA PROFILE (gộp — {persona_profile.shape[0]} persona từ {best_k} cluster kỹ thuật)")
    print("=" * 100)
    print(persona_profile.to_string())

    persona_profile.to_csv(OUT_DIR / "persona_profile.csv")
    print("\nSaved ->", OUT_DIR / "persona_profile.csv")

    cluster_profile.to_csv(OUT_DIR / "cluster_profile.csv")
    feat.to_csv(OUT_DIR / "clustered_users.csv", index=False)
    print(f"\nSaved -> {OUT_DIR / 'clustered_users.csv'} ({feat.shape})")

    plot_clusters(feat, persona_names, best_k)
    print("\nDONE.")


if __name__ == "__main__":
    main()