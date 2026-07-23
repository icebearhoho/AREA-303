"""
Fetch Google Trends REAL-TIME qua SerpApi (dich vu tra phi, on dinh hon pytrends).
Ghi de google_trends_clean.parquet theo dung format cu (date, keyword, interest, group)
-> KHONG can sua trend_google.py / alert_google.py / dashboard.

Can SERPAPI_KEY trong file .env (khong commit len Git).
"""
import os
import sys
import time
import requests
import pandas as pd
from dotenv import load_dotenv
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

load_dotenv(config.FEATURE_DIR / ".env")
API_KEY = os.getenv("SERPAPI_KEY")

KEYWORDS = {
    "beauty":  ["son môi", "serum", "skincare", "toner", "kem chống nắng",
                "kem nền", "cushion", "trị mụn", "nước hoa", "tẩy trang"],
    "fashion": ["áo khoác", "váy", "đầm", "outfit", "thời trang",
                "túi xách", "giày sneaker", "giày cao gót", "áo croptop", "quần ống rộng"],
}
GEO = "VN"
DATE_RANGE = "today 12-m"
ENDPOINT = "https://serpapi.com/search"
SLEEP_BETWEEN = 1.5   # SerpApi co ha tang rieng, khong can cho lau nhu pytrends


def fetch_one(keyword: str, group: str) -> pd.DataFrame:
    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": GEO,
        "date": DATE_RANGE,
        "data_type": "TIMESERIES",
        "api_key": API_KEY,
    }
    r = requests.get(ENDPOINT, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"SerpApi loi: {data['error']}")

    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    if not timeline:
        raise RuntimeError("timeline_data rong")

    rows = []
    for pt in timeline:
        ts = int(pt["timestamp"])
        val = pt["values"][0]["extracted_value"]
        rows.append({"date": pd.Timestamp(ts, unit="s").normalize(),
                     "keyword": keyword, "interest": int(max(min(val, 100), 0)),
                     "group": group})
    return pd.DataFrame(rows)


def main() -> None:
    if not API_KEY:
        print("LOI: khong tim thay SERPAPI_KEY trong .env")
        return

    print(f"API key: {API_KEY[:8]}... (da nap tu .env)")
    print("Dang test 1 keyword truoc khi keo full 20 keyword...")

    # ---- TEST 1 keyword truoc, khong ton quota neu loi cau hinh ----
    test_kw, test_grp = "serum", "beauty"
    try:
        df_test = fetch_one(test_kw, test_grp)
        print(f"TEST OK: '{test_kw}' -> {len(df_test)} tuan, "
              f"interest {df_test['interest'].min()}-{df_test['interest'].max()}")
    except Exception as e:
        print(f"TEST THAT BAI: {e}")
        print("Dung lai, KHONG keo full 20 keyword. Kiem tra API key / quota.")
        return

    # ---- Keo full 20 keyword ----
    print("\nDang keo toan bo 20 keyword...")
    frames = [df_test]
    all_kw = [(k, g) for g, ks in KEYWORDS.items() for k in ks if k != test_kw]
    ok, fail = 1, 0
    for kw, grp in all_kw:
        try:
            frames.append(fetch_one(kw, grp))
            ok += 1
            print(f"  [{ok+fail}/20] OK: {kw}")
        except Exception as e:
            fail += 1
            print(f"  [{ok+fail}/20] LOI: {kw} -> {e}")
        time.sleep(SLEEP_BETWEEN)

    if fail > 0:
        print(f"\nCANH BAO: {fail}/20 keyword loi. Data se THIEU cac keyword nay.")

    live = pd.concat(frames, ignore_index=True)
    out = config.GOOGLE_TRENDS_PARQUET
    live.to_parquet(out)
    print(f"\nOK - da cap nhat: {out.name} | {live['keyword'].nunique()} keyword, "
          f"{live['date'].nunique()} tuan | interest {live['interest'].min()}-{live['interest'].max()}")


if __name__ == "__main__":
    main()
