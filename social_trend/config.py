"""
Config chung cho Feature #08 - Social Trend Analyzer.
Tap trung moi duong dan o day de cac script khac import lai, khong hard-code lung tung.
"""
from pathlib import Path

# Thu muc goc cua feature (chinh la thu muc chua file config.py nay)
FEATURE_DIR = Path(__file__).resolve().parent

# Thu muc goc cua repo AREA-303 (len 2 cap: features/idea_08.. -> features -> repo)
REPO_ROOT = FEATURE_DIR.parent  # social_trend -> repo root

# Duong dan toi dataset da duoc team data chuan bi san
DATA_DIR = REPO_ROOT / "dataset" / "by_idea" / "idea_08_social_trend"
TWEET_PARQUET = DATA_DIR / "tweet_sentiment_clean.parquet"
TWEET_CSV = DATA_DIR / "tweet_sentiment_clean.csv"

# Sephora reviews CO timestamp that -> dung cho sentiment/brand health (khong bia)
SEPHORA_PARQUET = DATA_DIR / "sephora_reviews_dated_clean.parquet"

# Google Trends: do hot tim kiem theo tuan (tin hieu xu huong that) -> Trend Detector
GOOGLE_TRENDS_PARQUET = DATA_DIR / "google_trends_clean.parquet"

# Thu muc xuat ket qua (bao cao, bieu do, model...) cua feature nay
OUTPUT_DIR = FEATURE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def check_data_exists() -> None:
    """Kiem tra file du lieu ton tai truoc khi chay, bao loi ro rang neu thieu."""
    if not TWEET_PARQUET.exists():
        raise FileNotFoundError(
            f"Khong tim thay file du lieu: {TWEET_PARQUET}\n"
            f"Kiem tra lai xem repo da co dataset/by_idea/idea_08_social_trend/ chua."
        )
