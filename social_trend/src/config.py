"""
Config chung cho feature Social Trend (#08). Tap trung moi duong dan.
Layout: <repo>/social_trend/src/config.py
"""
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent          # social_trend/src
FEATURE_DIR = SRC_DIR.parent                        # social_trend
REPO_ROOT = FEATURE_DIR.parent                      # repo root

# Du lieu da xu ly (gitignore theo policy repo) - dat o dataset/by_idea/
DATA_DIR = REPO_ROOT / "dataset" / "by_idea" / "idea_08_social_trend"
SEPHORA_PARQUET = DATA_DIR / "sephora_reviews_dated_clean.parquet"
TWEET_PARQUET = DATA_DIR / "tweet_sentiment_clean.parquet"

# Ket qua cua feature
OUTPUT_DIR = FEATURE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def check_data_exists() -> None:
    """Bao loi ro rang neu thieu file du lieu (data gitignore, tai/tao lai theo README)."""
    if not SEPHORA_PARQUET.exists():
        raise FileNotFoundError(
            f"Khong tim thay: {SEPHORA_PARQUET}\n"
            f"Data bi gitignore theo policy repo. Xem README de biet nguon Sephora."
        )
