"""
Bước 3 — XGBoost Persona Scorer + SHAP Explainability
Idea #13: Customer Segmentation

Mục đích: UMAP + K-Means++ là unsupervised và tốn ~90s để chạy lại trên
toàn bộ data. Với user MỚI (đăng ký hôm nay), ta không muốn chạy lại
UMAP/KMeans mỗi lần. Giải pháp chuẩn: dùng nhãn cluster_id đã có (từ
02_clustering.py) làm target, train một classifier supervised (XGBoost)
để dự đoán persona cho user mới CHỈ TỪ feature hành vi của họ — nhanh,
production-ready, và giải thích được bằng SHAP.

Input : outputs/clustered_users.csv   (từ 02_clustering.py)
Output: models/xgb_persona_classifier.pkl
        models/label_encoder.pkl
        outputs/xgb_classification_report.txt
        figures/shap_summary.png
        figures/feature_importance.png
"""
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import shap

RANDOM_STATE = 42

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
FIG_DIR = ROOT / "figures"
MODEL_DIR = ROOT / "models"
for d in (OUT_DIR, FIG_DIR, MODEL_DIR):
    d.mkdir(exist_ok=True)

DATA_PATH = OUT_DIR / "clustered_users.csv"

# Feature dùng để train classifier — PHẢI là feature có sẵn ngay lúc user
# mới đăng ký / mới tương tác (không dùng umap_x/umap_y vì đó là kết quả
# của UMAP, không tồn tại cho user mới chưa qua bước clustering).
FEATURE_COLS = [
    "log_recency", "seniority_months",
    "log_followers", "log_follows", "log_products_liked",
    "log_products_listed", "log_products_sold", "products_pass_rate",
    "log_products_wished", "log_products_bought",
    "buy_ratio", "wish_to_buy",
    "has_any_app", "has_profile_picture",
]


def main():
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded clustered data: {df.shape}")

    # persona (string) là target dễ diễn giải hơn cluster_id (số)
    le = LabelEncoder()
    y = le.fit_transform(df["persona"])
    X = df[FEATURE_COLS]

    print(f"\nClasses ({len(le.classes_)}): {list(le.classes_)}")
    print(df["persona"].value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"\nTrain: {X_train.shape}, Test: {X_test.shape}")

    # ------------------------------------------------------------------
    # Train XGBoost multi-class classifier
    # ------------------------------------------------------------------
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softprob",
        num_class=len(le.classes_),
        eval_metric="mlogloss",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # ------------------------------------------------------------------
    # Đánh giá
    # ------------------------------------------------------------------
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=le.classes_, digits=3)
    print("\n" + "=" * 70)
    print("CLASSIFICATION REPORT")
    print("=" * 70)
    print(report)

    with open(OUT_DIR / "xgb_classification_report.txt", "w") as f:
        f.write(report)
    print("Saved ->", OUT_DIR / "xgb_classification_report.txt")

    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(pd.DataFrame(cm, index=le.classes_, columns=le.classes_))

    # ------------------------------------------------------------------
    # Feature importance (gain-based, built-in XGBoost)
    # ------------------------------------------------------------------
    importance = pd.Series(model.feature_importances_, index=FEATURE_COLS).sort_values()
    plt.figure(figsize=(8, 6))
    importance.plot(kind="barh", color="#2563eb")
    plt.title("XGBoost Feature Importance — Persona Classifier")
    plt.xlabel("Importance (gain)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "feature_importance.png", dpi=150)
    plt.close()
    print("Saved ->", FIG_DIR / "feature_importance.png")

    # ------------------------------------------------------------------
    # SHAP explainability — giải thích persona theo feature
    # ------------------------------------------------------------------
    print("\nComputing SHAP values (subsample 2000 để nhanh)...")
    sample = X_test.sample(min(2000, len(X_test)), random_state=RANDOM_STATE)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(sample)

    plt.figure()
    # shap_values shape: (n_samples, n_features, n_classes) cho multi-class
    if isinstance(shap_values, list):
        shap.summary_plot(shap_values, sample, class_names=le.classes_, show=False)
    else:
        # multi-class array -> lấy trung bình |shap| trên mọi lớp cho summary tổng quát
        shap.summary_plot(
            np.abs(shap_values).mean(axis=-1) if shap_values.ndim == 3 else shap_values,
            sample, show=False,
        )
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shap_summary.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved ->", FIG_DIR / "shap_summary.png")

    # ------------------------------------------------------------------
    # Lưu model + label encoder để dùng cho scoring real-time
    # ------------------------------------------------------------------
    with open(MODEL_DIR / "xgb_persona_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(MODEL_DIR / "label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
    with open(MODEL_DIR / "feature_columns.json", "w") as f:
        json.dump(FEATURE_COLS, f, indent=2)

    print(f"\nSaved model -> {MODEL_DIR / 'xgb_persona_classifier.pkl'}")
    print(f"Saved label encoder -> {MODEL_DIR / 'label_encoder.pkl'}")
    print(f"Saved feature list -> {MODEL_DIR / 'feature_columns.json'}")
    print("\nDONE.")


def score_new_user(user_features: dict) -> dict:
    """
    Ví dụ hàm dùng để serve real-time: nhận dict feature của 1 user mới
    (đã qua bước feature engineering ở 01_feature_engineering.py) và trả
    về persona dự đoán + xác suất từng lớp.

    Dùng lại trong API/backend, KHÔNG cần chạy UMAP hay KMeans.
    """
    with open(MODEL_DIR / "xgb_persona_classifier.pkl", "rb") as f:
        model = pickle.load(f)
    with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    with open(MODEL_DIR / "feature_columns.json") as f:
        feature_cols = json.load(f)

    x = pd.DataFrame([user_features])[feature_cols]
    pred_class = model.predict(x)[0]
    pred_proba = model.predict_proba(x)[0]

    return {
        "persona": le.inverse_transform([pred_class])[0],
        "probabilities": dict(zip(le.classes_, pred_proba.round(4).tolist())),
    }


if __name__ == "__main__":
    main()
