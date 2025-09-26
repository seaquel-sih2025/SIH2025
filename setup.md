# Setup Guide (Local Development)

This document explains how to set up and run every component in the SIH2025 monorepo on your local machine.

It covers prerequisites, environment configuration, installation steps, how to start each service (backend, workers, web app, mobile app, AI worker), database setup/migrations, RabbitMQ queues, and troubleshooting.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Repository Layout](#repository-layout)
- [Environment Variables](#environment-variables)
  - [Backend `.env` template](#backend-env-template)
  - [Web App `.env.local` template](#web-app-envlocal-template)
  - [Mobile App `.env` template](#mobile-app-env-template)
  - [AI Worker `.env` template](#ai-worker-env-template)
- [Initial Setup](#initial-setup)
  - [Backend setup](#backend-setup)
  - [Database setup](#database-setup)
  - [RabbitMQ setup](#rabbitmq-setup)
  - [Web App setup](#web-app-setup)
  - [Mobile App setup](#mobile-app-setup)
  - [AI Worker setup](#ai-worker-setup)
- [Running Services](#running-services)
  - [Backend API](#backend-api)
  - [Coordinator Worker](#coordinator-worker)
  - [Weather Verification Worker](#weather-verification-worker)
  - [Peer Notification Worker](#peer-notification-worker)
  - [AI NLP Worker](#ai-nlp-worker)
  - [Web Dashboard](#web-dashboard)
  - [Mobile App](#mobile-app)
- [Database & Migrations](#database--migrations)
- [Messaging (RabbitMQ) Queues](#messaging-rabbitmq-queues)
- [Verification & Health Checks](#verification--health-checks)
- [Common Developer Workflow](#common-developer-workflow)
- [Troubleshooting](#troubleshooting)
- [Appendix: Architecture Diagram](#appendix-architecture-diagram)

---

## Prerequisites

Install the following on your machine:

- Python 3.11+
- Node.js 18+ and npm
- Flutter SDK (with Android Studio/Xcode toolchains)
- PostgreSQL 14+ with PostGIS extension enabled
- RabbitMQ server
- AWS S3 bucket and credentials (for uploads)
- WeatherAPI.com API key
- Google Gemini API key
- (Optional) Firebase project credentials for push notifications

---

## Repository Layout

```
SIH2025/
├── backend/
│   ├── app/
│   │   ├── api/                  # Routers: auth, users, reports, verifications, feed, notifications
│   │   ├── core/                 # Settings/security
│   │   ├── db/                   # SQLAlchemy models, session/engine
│   │   ├── models/               # Pydantic models
│   │   ├── services/             # S3, RabbitMQ, confidence, verification tracker
│   │   └── main.py               # FastAPI app
│   ├── create_tables.py          # Fresh/migrate/reset helpers
│   ├── worker.py                 # Coordinator worker (fan-out)
│   ├── weather_worker.py         # Weather verification worker
│   └── peer_notif_worker.py      # Peer notification worker
├── frontend/
│   ├── web_app/                  # React + Vite dashboard
│   └── mobile_app/               # Flutter app (Recent Reports + SOS button)
└── ai/
    ├── worker.py                 # Gemini-based NLP worker
    └── config.py                 # AI worker settings (env-driven)
```

---

## Environment Variables

Create the following files and fill in your secrets. Do not commit these files.

### Backend `.env` template
Create `backend/.env`:

```
# Core Services
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/DBNAME
SYNC_DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DBNAME
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# JWT
SECRET_KEY=replace_with_strong_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET_NAME=...
AWS_S3_REGION=ap-south-1

# External APIs
WEATHERAPI_KEY=...
GEMINI_API_KEY=...

# Backend URL (used by workers)
BACKEND_URL=http://127.0.0.1:8000

# Firebase (optional)
FIREBASE_PROJECT_ID=...
FIREBASE_PRIVATE_KEY_ID=...
FIREBASE_PRIVATE_KEY=... # replace \n with real newlines when loading
FIREBASE_CLIENT_EMAIL=...
FIREBASE_CLIENT_ID=...
FIREBASE_AUTH_URI=...
FIREBASE_TOKEN_URI=...
```

### Web App `.env.local` template
Create `frontend/web_app/.env.local`:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Mobile App `.env` template
Create `frontend/mobile_app/.env`:

```
# Android emulator loopback to host
API_BASE_URL=http://10.0.2.2:8000
# For real device on same LAN, use http://<your_host_ip>:8000
```

### AI Worker `.env` template
Create `ai/.env`:

```
GEMINI_API_KEY=...
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
BACKEND_URL=http://127.0.0.1:8000
```

---

## Initial Setup

### Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
# Create backend/.env as above
```

### Database setup

1) Start PostgreSQL and create (or choose) a database.
2) Enable PostGIS in your database:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

3) Apply schema: see [Database & Migrations](#database--migrations).

### RabbitMQ setup

- Start RabbitMQ locally (default: `amqp://guest:guest@localhost:5672/`).
- Update `RABBITMQ_URL` in your `.env` files if your host/port differs.

### Web App setup

```bash
cd frontend/web_app
npm install
# Create .env.local as above
```

### Mobile App setup

```bash
cd frontend/mobile_app
flutter pub get
# Create .env as above
```

### AI Worker setup

```bash
cd ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Create ai/.env as above
```

---

## Running Services

Open a separate terminal for each service below.

### Backend API
From `backend/`:

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- Health check: `GET /` returns `{ "status": "active" }`.

### Coordinator Worker
From `backend/`:

```bash
python worker.py
```

- Consumes `report_processing_queue`.
- Persists initial report & media, then dispatches to `nlp_queue`, `weather_queue`, `peer_notification_queue`.

### Weather Verification Worker
From `backend/`:

```bash
python weather_worker.py
```

- Consumes `weather_queue`.
- Calls WeatherAPI.com, analyzes match, and POSTs to `POST /api/verifications/weather`.

### Peer Notification Worker
From `backend/`:

```bash
python peer_notif_worker.py
```

- Consumes `peer_notification_queue`.
- POSTs to `POST /api/notifications/peer`.

### AI NLP Worker
From `ai/`:

```bash
python worker.py
```

- Consumes `nlp_queue`.
- Analyzes descriptions with Gemini (fallback analysis when needed).
- POSTs to backend NLP verification endpoint: `POST /api/verifications/nlp`.

### Web Dashboard
From `frontend/web_app/`:

```bash
npm run dev
```

- Runs on http://localhost:5173
- Uses `VITE_API_BASE_URL` to reach the backend.

### Mobile App
From `frontend/mobile_app/`:

```bash
flutter run
```

- For Android emulator, use `API_BASE_URL=http://10.0.2.2:8000`.
- For a physical device on the same LAN, use `http://<your_host_ip>:8000`.
- The home screen includes a Recent Reports section and an SOS emergency button (ready for backend integration).

---

## Database & Migrations

Use `backend/create_tables.py` for schema operations.

- Fresh (drop & recreate tables):

```bash
cd backend
python create_tables.py fresh
```

- Migrate (executes SQL in `backend/migrations/add_user_profile_fields.sql` if present):

```bash
python create_tables.py migrate
```

- Reset (fresh + migrate):

```bash
python create_tables.py reset
```

Tables defined in `backend/app/db/models.py` include:
- `users`
- `reports` (with `Geography(POINT, 4326)`)
- `media`
- `verifications`
- `notifications`

With enums for hazard types, statuses, urgency, sentiment, media types, sources, etc.

---

## Messaging (RabbitMQ) Queues

- `report_processing_queue`: initial report ingestion (fan-out trigger)
- `nlp_queue`: AI NLP analysis jobs
- `weather_queue`: weather verification jobs
- `peer_notification_queue`: peer alert jobs

The RabbitMQ connection URL is configured via `RABBITMQ_URL` in `.env` files.

---

## Verification & Health Checks

- Backend root: `GET http://127.0.0.1:8000/` → `{ "status": "active" }`
- OpenAPI docs: `http://127.0.0.1:8000/docs`
- Web app: `http://localhost:5173`
- Mobile app: verify API calls reach the backend (emulator vs device base URL)
- Workers: check each worker terminal for queue consumption logs and POST success messages

---

## Common Developer Workflow

1. Start Postgres, ensure PostGIS is enabled.
2. Start RabbitMQ.
3. Launch the backend (and apply schema if needed).
4. Start required workers in separate terminals.
5. Run the web app (and/or mobile app) pointing to your backend.
6. Submit a report from the app → verify:
   - Coordinator persists records and dispatches fan-out.
   - NLP, Weather, and Peer workers consume respective queues and POST results.
   - Backend receives verification/notification results.

---

## Troubleshooting

- Backend won’t start: confirm `backend/.env`, DB connectivity, and RabbitMQ availability.
- PostGIS errors: run `CREATE EXTENSION postgis;` in your database.
- Android emulator cannot reach backend: use `http://10.0.2.2:8000`.
- CORS issues on web: confirm `VITE_API_BASE_URL` and backend CORS (backend allows all in dev).
- RabbitMQ connection errors: validate `RABBITMQ_URL` and server status/port.
- AWS S3 upload issues: verify bucket name, region, keys, and IAM permissions (`s3:PutObject`, `s3:GetObject`).
- Weather verification fails: check `WEATHERAPI_KEY` and API rate limits.
- Gemini errors: ensure `GEMINI_API_KEY` is valid; AI worker uses a keyword-based fallback.

---

## Appendix: Architecture Diagram

```mermaid
flowchart LR
  Mobile[Flutter Mobile App] -->|HTTP| API[(FastAPI Backend)]
  Web[React Web App] -->|HTTP| API
  API -->|PostgreSQL + PostGIS| DB[(Database)]
  API -->|Publish| RMQ[(RabbitMQ)]
  RMQ -->|report_processing_queue| Coord[Coordinator Worker]
  Coord -->|nlp_queue| AI[AI NLP Worker]
  Coord -->|weather_queue| Weather[Weather Worker]
  Coord -->|peer_notification_queue| Peer[Peer Notification Worker]
  AI -->|POST /api/verifications/nlp| API
  Weather -->|POST /api/verifications/weather| API
  Peer -->|POST /api/notifications/peer| API
  API -->|S3| Storage[(AWS S3)]
```
