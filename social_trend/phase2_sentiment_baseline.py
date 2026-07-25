import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

import config

# ===== KHOI 1: Load data =====
config.check_data_exists()
df = pd.read_parquet(config.TWEET_PARQUET)
print("Load OK:", df.shape)

# ===== KHOI 2: Tach 3 tap theo cot split co san (KHONG tu chia lai) =====
train_df = df[df["split"] == "train"]
val_df   = df[df["split"] == "validation"]
test_df  = df[df["split"] == "test"]
print("Train:", len(train_df), "| Val:", len(val_df), "| Test:", len(test_df))

# ===== KHOI 3: TF-IDF (bien chu thanh so) =====
# fit_transform CHI goi tren train; val/test chi transform (khong cho model nhin truoc)
vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
X_train = vectorizer.fit_transform(train_df["text"])
X_val   = vectorizer.transform(val_df["text"])
X_test  = vectorizer.transform(test_df["text"])

y_train = train_df["label"]
y_val   = val_df["label"]
y_test  = test_df["label"]
print("TF-IDF xong. So tu vung:", len(vectorizer.vocabulary_))

# ===== KHOI 4: Train model =====
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train, y_train)
print("Train xong.")

# ===== KHOI 5: Danh gia tren VALIDATION (de tune) =====
val_pred = model.predict(X_val)
print("\n=== VALIDATION ===")
print(classification_report(y_val, val_pred, target_names=["negative", "neutral", "positive"]))

# ===== KHOI 6: Danh gia tren TEST (chi chay 1 lan cuoi) =====
test_pred = model.predict(X_test)
print("=== TEST (chi chay 1 lan) ===")
print(classification_report(y_test, test_pred, target_names=["negative", "neutral", "positive"]))
print("Confusion matrix:")
print(confusion_matrix(y_test, test_pred))

# ===== KHOI 7: Luu model + vectorizer de Phase 4/6 dung lai =====
joblib.dump(model, config.OUTPUT_DIR / "sentiment_baseline_model.pkl")
joblib.dump(vectorizer, config.OUTPUT_DIR / "sentiment_vectorizer.pkl")
print("\nDa luu model + vectorizer vao outputs/")
