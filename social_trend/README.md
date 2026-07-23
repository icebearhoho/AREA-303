# Feature #08 — Social Trend Analyzer

Phát hiện **loại sản phẩm đang lên** từ **độ hot tìm kiếm Google Trends** và đưa ra
**gợi ý nhập hàng** cho seller. Tín hiệu xu hướng là dữ liệu tìm kiếm **thật** —
không dùng model dự báo, không mô phỏng, không bịa số.

**Người phụ trách:** Phú · **Track:** NLP / Data

## Kiến trúc

| Lớp | Làm gì | Công nghệ |
|---|---|---|
| **A — Trend Detector** | Đo momentum độ hot tìm kiếm mỗi keyword → keyword đang lên/xuống | Google Trends + momentum score [-100, +100] (KHÔNG Prophet) |
| **B — Inventory Alert** | Keyword search đang lên → nên nhập; đang xuống → nên giảm | Rule thuần theo xu hướng: STOCK UP / MONITOR / REDUCE |
| **Sentiment Engine** | Công cụ độc lập: 1 câu → negative / neutral / positive | XLM-RoBERTa fine-tuned (F1 0.69), fallback TF-IDF + LogReg |
| **Dashboard** | Cảnh báo + biểu đồ interest theo thời gian + ô test sentiment | Streamlit + Plotly |
| **Demo Fallback** | Đóng gói tất cả vào 1 JSON tự chứa | `demo_data.json` |

## Dữ liệu

- **Tầng trend/alert:** `google_trends_clean.parquet` — độ hot tìm kiếm theo tuần
  (53 tuần, 20 keyword beauty + fashion, interest 0-100). Cập nhật **real-time** được
  (xem mục dưới) hoặc dùng file tĩnh có sẵn.
- **Sentiment model:** train trên `tweet_sentiment_clean.parquet` (đa ngôn ngữ).

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Model transformer đặt tại `outputs/xlmr_sentiment/` (tải từ Colab). Nếu không có,
`sentiment.py` tự dùng baseline `outputs/sentiment_baseline_*.pkl`.

## Cập nhật dữ liệu Google Trends real-time (tùy chọn)

Mặc định pipeline chạy trên file tĩnh có sẵn. Muốn kéo dữ liệu mới nhất:

```bash
# Cach 1 (KHUYEN DUNG): SerpApi - on dinh. Can SERPAPI_KEY trong .env
cp .env.example .env            # roi dien SERPAPI_KEY that (lay tai serpapi.com)
python fetch_google_trends_serpapi.py

# Cach 2: pytrends - mien phi nhung KHONG chinh thuc, hay bi Google chan (429)
python fetch_google_trends.py
```
Cả hai ghi đè `google_trends_clean.parquet` đúng format → không cần sửa gì ở pipeline.
Nếu fetch thất bại (rate-limit), script **giữ nguyên file cũ** làm fallback.

> `.env` chứa API key đã được **gitignore** — không bao giờ commit lên repo.

## Pipeline — chạy theo thứ tự (từ thư mục feature)

```bash
python fetch_google_trends_serpapi.py   # (tuy chon) cap nhat data real-time
python trend_google.py                  # momentum moi keyword -> keyword_trends.parquet
python alert_google.py                  # canh bao STOCK UP / MONITOR / REDUCE
python prepare_demo_data.py             # dong goi -> outputs/demo_data.json
streamlit run phase6_dashboard.py       # dashboard
```

## Demo Fallback

Dashboard đọc `outputs/demo_data.json` trước (chip **Demo · JSON**) → **chạy được kể cả
khi thiếu file `.parquet`, thiếu model 1.1GB, hoặc mất mạng**. Ô sentiment: có model thì
chạy live, không thì dùng câu đã cache trong JSON. Xóa `demo_data.json` để về **Live · parquet**.

## Cấu trúc file

```
config.py                        # duong dan tap trung
trend_google.py                  # A: momentum keyword (Google Trends)
alert_google.py                  # B: canh bao STOCK UP / MONITOR / REDUCE
fetch_google_trends_serpapi.py   # real-time qua SerpApi (chinh)
fetch_google_trends.py           # real-time qua pytrends (mien phi, kem on dinh)
sentiment.py                     # predict_sentiment() (cong cu doc lap)
phase2_sentiment_baseline.py     # baseline TF-IDF (fallback cho sentiment)
phase6_dashboard.py              # dashboard Streamlit
prepare_demo_data.py             # demo_data.json
.env.example                     # mau SERPAPI_KEY (copy thanh .env)
.streamlit/config.toml           # theme dark khoa san
outputs/                         # keyword_*, demo_data.json, model xlmr_sentiment
```
