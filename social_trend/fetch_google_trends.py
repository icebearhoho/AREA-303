"""
Fetch Google Trends REAL-TIME qua pytrends (KHONG chinh thuc - scrape endpoint noi bo).
- Keo interest_over_time cho danh sach keyword -> ghi de google_trends_clean.parquet
  (cung format: date, keyword, interest, group) -> pipeline con lai chay nhu cu.
- Co retry + sleep chong rate-limit (429). Neu THAT BAI -> GIU nguyen file cu (fallback).

CANH BAO: Google khong co API chinh thuc; pytrends hay bi 429, nhat la tu IP cloud.
Chay tu may/mang ca nhan (IP nha) thi de thanh cong hon.
"""
import sys
import time
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Keyword theo nhom (giu giong dataset hien tai)
KEYWORDS = {
    "beauty":  ["son môi", "serum", "skincare", "toner", "kem chống nắng",
                "kem nền", "cushion", "trị mụn", "nước hoa", "tẩy trang"],
    "fashion": ["áo khoác", "váy", "đầm", "outfit", "thời trang",
                "túi xách", "giày sneaker", "giày cao gót", "áo croptop", "quần ống rộng"],
}
TIMEFRAME = "today 12-m"   # 12 thang gan nhat, granularity tuan
GEO = "VN"
BATCH = 5                  # gioi han toi da cua Google la 5 tu/request
SLEEP_BETWEEN = 15         # giay nghi giua cac batch (tranh 429)

# LUU Y QUAN TRONG: moi batch duoc Google tu chuan hoa DOC LAP ve thang 0-100
# (tu chinh no, khong qua buoc "neo + nhan he so" tu che - buoc do de sai va da
# tung day interest len toi 197, sai voi dinh nghia Google Trends). He qua: KHONG
# the so sanh interest tuyet doi GIUA 2 batch khac nhau, nhung momentum (dieu
# pipeline can) tinh trong cung 1 keyword/batch nen van dung.


def fetch() -> pd.DataFrame:
    from pytrends.request import TrendReq
    py = TrendReq(hl="vi-VN", tz=420)

    grp = {k: g for g, ks in KEYWORDS.items() for k in ks}
    all_kw = list(grp.keys())
    batches = [all_kw[i:i + BATCH] for i in range(0, len(all_kw), BATCH)]

    frames = []
    for bi, batch in enumerate(batches):
        for attempt in range(3):
            try:
                py.build_payload(batch, timeframe=TIMEFRAME, geo=GEO)
                df = py.interest_over_time()
                if df.empty:
                    raise RuntimeError("tra ve rong")
                break
            except Exception as e:
                print(f"  batch {bi+1} thu {attempt+1} loi: {e} -> cho 30s")
                time.sleep(30)
        else:
            raise RuntimeError("Bi chan / khong keo duoc (429?) - giu data cu")
        if "isPartial" in df.columns:
            df = df.drop(columns=["isPartial"])
        frames.append(df)
        print(f"  batch {bi+1}/{len(batches)} OK: {batch}")
        time.sleep(SLEEP_BETWEEN)

    # Ve dang long: date, keyword, interest, group (KHONG ghep scale giua batch)
    rows = []
    for f in frames:
        for kw in f.columns:
            for dt, v in f[kw].items():
                rows.append({"date": pd.Timestamp(dt).normalize(),
                             "keyword": kw, "interest": int(round(max(min(v, 100), 0))),
                             "group": grp.get(kw, "beauty")})
    return pd.DataFrame(rows)


def main() -> None:
    out = config.GOOGLE_TRENDS_PARQUET
    print("Dang keo Google Trends real-time (pytrends)...")
    try:
        live = fetch()
        live.to_parquet(out)
        print(f"OK - da cap nhat REAL-TIME: {out.name} | {live['keyword'].nunique()} kw, "
              f"{live['date'].nunique()} tuan")
    except Exception as e:
        print(f"THAT BAI -> giu nguyen data cu lam fallback. Ly do: {e}")


if __name__ == "__main__":
    main()
