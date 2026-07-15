# AREA 303 — Backend (FastAPI)

FastAPI service for AREA 303. See repo root `README.md` for the full picture.

## Layout

```
backend/
├── app/
│   ├── api/                 # HTTP layer
│   │   ├── v1/
│   │   │   ├── endpoints/   # one router per feature
│   │   │   └── router.py    # aggregates v1 routers
│   │   └── deps.py          # shared FastAPI dependencies (db, redis, auth)
│   ├── core/                # config, security, responses, exceptions
│   │   │   └── __init__.py  # aggregates v1 routers
│   │   └── deps.py          # shared FastAPI dependencies (db, redis, auth)
│   ├── core/                # config, security, responses, exceptions, sse, rate_limit
│   ├── db/                  # SQLAlchemy session, base, redis client
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # business logic
│   ├── main.py              # FastAPI app factory
│   └── config.py            # pydantic-settings settings
├── alembic/                 # DB migrations (initialized on first run)
│   │   └── genai/           # shared GenAI infra — LLM clients, RAG, cache, prompts
│   ├── main.py              # FastAPI app factory
│   └── config.py            # pydantic-settings settings
├── alembic/                 # DB migrations
├── tests/                   # pytest tests mirror app/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Run locally

```bash
cp .env.example .env
docker compose -f ../docker-compose.yml up -d postgres redis
python -m venv .venv && . .venv/Scripts/Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

OpenAPI docs: <http://localhost:8000/docs>

## GenAI endpoints (fullstack-owned features)

The 4 features owned by the fullstack role live under `/api/v1/`:

| # | Endpoint | Method | Streaming | Notes |
|---|----------|--------|-----------|-------|
| 03 | `/personal-shopper/` | POST | **SSE** | RAG → Gemini/OpenAI, token-by-token |
| 03 | `/personal-shopper/products` | GET  | — | Returns recommended product cards only |
| 09 | `/content-generator/` | POST | — | 3 platform variants + predicted CTR |
| 11 | `/recsys/` | POST | — | Traditional CF or AI reasoning |
| 17 | `/seller-coach/` | POST | — | 5-axis audit + 4-week roadmap |

All endpoints honor `DEMO_MODE=true` (default) — they return
pre-generated fixtures from `app/services/genai/demo_data.py` and
never touch an upstream LLM. This is the project's mandatory safety
net (project plan, Day 8 risk register).

### Examples

```bash
# 03 Personal Shopper — SSE stream
curl -N -X POST http://localhost:8000/api/v1/personal-shopper/ \
  -H 'Content-Type: application/json' \
  -d '{"query": "quà sinh nhật 500k", "top_k": 4, "stream": true}'

# 03 Personal Shopper — product cards only
curl 'http://localhost:8000/api/v1/personal-shopper/products?query=son%20cho%20da%20ng%C4%83m&top_k=3'

# 09 Content Generator — 3 platforms
curl -X POST http://localhost:8000/api/v1/content-generator/ \
  -H 'Content-Type: application/json' \
  -d '{"product_name": "Áo khoác denim unisex", "features": "Denim 12oz, wash nhẹ, free ship"}'

# 11 Recsys — AI reasoning mode
curl -X POST http://localhost:8000/api/v1/recsys/ \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "u-42", "signals": {"skin_type": "dry"}, "top_k": 4}'

# 17 Seller Coach
curl -X POST http://localhost:8000/api/v1/seller-coach/ \
  -H 'Content-Type: application/json' \
  -d '{"seller_id": "shop-001"}'
```

### SSE wire format

The Personal Shopper endpoint emits one `data:` frame per token, then
a final `data:` frame with `{"done": true, "meta": {...}}`:

```
data: {"delta": "Chào", "finish_reason": null}\n\n
data: {"delta": " bạn", "finish_reason": null}\n\n
...
data: {"delta": "", "finish_reason": "stop"}\n\n
data: {"done": true, "last": {...}, "meta": {...}}\n\n
```

Idle connections receive a `: ping\n\n` heartbeat comment every
`SSE_HEARTBEAT_SECONDS` (default 15s) so proxies don't reap them.

### Going live with real LLMs

1. Set `DEMO_MODE=false` in `.env`.
2. Pick a provider in `LLM_PROVIDER` (`gemini` or `openai`).
3. Provide the corresponding API key. Without a key the factory
   falls back to the mock client and logs `llm_client.*.no_key_fallback_mock`.
4. To enable RAG over the Tiki catalog, set:
   ```
   VECTOR_BACKEND=pinecone
   PINECONE_API_KEY=...
   PINECONE_INDEX=area303-tiki-catalog
   ```
   and `pip install pinecone`. With no key the in-memory retriever
   (seeded from `DEMO_CATALOG`) is used.

### Rate limiting

The `RateLimitMiddleware` enforces `RATE_LIMIT_PER_MINUTE` per IP
(default 30). GenAI routes get a dedicated bucket. On exceedance
the response is a standard envelope with `error.code = RATE_LIMITED`
and `Retry-After: 60`. Limits can be tuned per-environment in `.env`.

## Tests

```bash
pytest
ruff check .
mypy app
```

The suite covers:

* `test_envelope.py` — response envelope contract (`{success, data, meta, error}`)
* `test_cache.py` — Redis-backed LLM cache + in-process fallback
* `test_sse.py` — SSE frame encoding + heartbeat
* `test_genai_endpoints.py` — 4 features (envelope shape, demo-mode, SSE)
