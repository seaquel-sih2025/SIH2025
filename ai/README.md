# AI Services (NLP worker + Scrapers)

This folder contains the AI/NLP background worker that consumes hazard reports for analysis and the standalone social-media scrapers used for research/experimentation.

## Components
- NLP worker (production)
  - `worker.py`: Consumes `nlp_queue` from RabbitMQ, analyzes `user_description` with Gemini, and posts verification to the backend at `/api/verifications/nlp`.
  - Config: `config.py` (pydantic BaseSettings) reads from `.env` or environment variables.
  - Dependencies: `requirements.txt` (pika, google-generativeai, pydantic-settings, httpx, etc.).

- Twitter scraper (optional / research)
  - `twitter-scraper/main.py`: Fetches recent tweets via Twitter API v2, filters with a light rule-set + LLM, and stores results in Postgres using `db/models.py` (table `scraped_data`).
  - `twitter-scraper/llm/analyze.py`: Calls Gemini REST API with retry/backoff, returns single-line JSON.
  - `twitter-scraper/db/models.py`: Idempotent, non-destructive table creation and insert helpers.
  - IMPORTANT: `twitter-scraper/config.py` currently contains hard-coded secrets. Do NOT commit real keys; move them to environment variables before sharing or deploying.

- YouTube scraper (optional / research)
  - `youtube-scraper/search_videos.py`, `get_text_data.py`, `analyse_text.py`: Find and analyze videos using Google APIs + Gemini (via LangChain); store alerts in Postgres via `db_utils.py` (table `alerts`).
  - `youtube-scraper/config.py`: Uses `.env` for YouTube/Google API keys and local Postgres settings.

## Environment configuration
Create an `.env` file in this `ai/` folder (see `.env.sample`):

- `GEMINI_API_KEY`: Google Generative AI API key
- `RABBITMQ_URL`: AMQP URL (e.g., `amqp://guest:guest@localhost:5672/`)
- `BACKEND_URL`: Public base URL of your backend (e.g., `http://localhost:8000` or your Render URL)

The NLP worker reads these values via `ai/config.py`.

## Running the NLP worker
- Install dependencies from `ai/requirements.txt` in a virtual environment for Python 3.10+.
- Ensure RabbitMQ is reachable and the backend is running.
- Start the worker: `python ai/worker.py` (or via a process manager).
- Verify queue activity using the backend `/rabbitmq/status` endpoint; `nlp_queue` should show `consumer_count > 0` when the worker is running.

Notes:
- The worker includes retry/backoff for LLM calls and normalizes `hazard_type` values to match backend enums (e.g., `high_waves`, `storm_surge`, `coastal_flooding`, `rip_current`, `coastal_erosion`, `water_discoloration`, `marine_debris`, `tsunami`, `other`).
- If Gemini quota is hit, it falls back to a keyword-based analysis to avoid blocking end-to-end flow.

## Running the scrapers (optional)
These scrapers are not required for core app functionality. If you choose to run them:
- Configure API keys and Postgres connection in their respective `config.py` or `.env` files.
- Initialize their tables (`scraped_data` and `alerts`) using the provided helpers (`create_table()` / `ensure_schema()`).
- Run the scripts manually or on a schedule. Be mindful of API rate limits and costs.

## Security and secrets
- Replace any hard-coded keys in `twitter-scraper/config.py` with environment variables immediately.
- Never commit real API keys to source control. Use `.env` files for local dev and a secrets manager in production.

## Troubleshooting
- Worker not consuming? Check `RABBITMQ_URL` and that the queue `nlp_queue` exists; consult `/rabbitmq/status`.
- 401/403 from Twitter API: Verify your bearer token and app tier.
- Gemini errors: Ensure `GEMINI_API_KEY` is valid and the chosen model is available; the code uses backoff for 429/5xx.
- DB insert issues: Ensure Postgres is reachable and that the scrapers have created their tables; the worker posts results to the backend, not directly to the DB.
