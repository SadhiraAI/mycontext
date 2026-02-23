# mycontext — Developer Deployment & Operations Guide

> Last updated: February 2026

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Environments](#2-environments)
3. [Accounts & Dashboards](#3-accounts--dashboards)
4. [Local Development](#4-local-development)
5. [CI/CD Pipeline](#5-cicd-pipeline)
6. [Production Infrastructure](#6-production-infrastructure)
7. [Database & Migrations](#7-database--migrations)
8. [Domain & DNS Setup](#8-domain--dns-setup)
9. [Secrets Management](#9-secrets-management)
10. [Frontend Deployment](#10-frontend-deployment)
11. [Deploying Code Changes](#11-deploying-code-changes)
12. [License Key Management](#12-license-key-management)
13. [Monitoring & Debugging](#13-monitoring--debugging)
14. [Common Issues & Fixes](#14-common-issues--fixes)
15. [Future Enhancements](#15-future-enhancements)

---

## 1. Architecture Overview

```
┌─────────────────────────┐     ┌─────────────────────────┐
│   Frontend (React/Vite) │     │   Backend (FastAPI)      │
│   Cloudflare Pages      │────▶│   Fly.io                 │
│   mycontext.sadhiraai.com│     │   api.sadhiraai.com      │
└─────────────────────────┘     └────────┬────────────────┘
                                         │
                                         ▼
                                ┌─────────────────────┐
                                │  PostgreSQL (Neon)   │
                                │  Managed, serverless │
                                └─────────────────────┘
```

**What each service does:**

| Service | Purpose | Cost |
|---------|---------|------|
| **Fly.io** | Hosts the FastAPI backend in a Docker container. Auto-sleeps when idle. | Free tier (256MB RAM) |
| **Neon** | Managed PostgreSQL database (serverless, auto-scales to zero). | Free tier (0.5GB) |
| **Cloudflare Pages** | Hosts the React frontend as a static site with global CDN. | Free tier |
| **Cloudflare DNS** | Manages DNS records for `sadhiraai.com` and subdomains. | Free |
| **GitHub Actions** | CI/CD pipeline — lints, tests, and deploys on every push to `main`. | Free for public/private repos |

**Domain structure:**

| Domain | Points to | Purpose |
|--------|-----------|---------|
| `sadhiraai.com` | Company website | Parent domain |
| `mycontext.sadhiraai.com` | Cloudflare Pages | Frontend app |
| `api.sadhiraai.com` | Fly.io (`sadhiraai-api.fly.dev`) | Backend API |

---

## 2. Environments

### Development (local machine)

- **Database:** SQLite (`mycontext.db`, auto-created)
- **Backend:** `uvicorn app.main:app --reload` on `http://localhost:8000`
- **Frontend:** `npm run dev` on `http://localhost:5173`
- **SDK:** Editable install (`pip install -e ".[dev]"`) — all templates available
- **Config:** `.env` file or defaults in `app/config.py`

### Docker Development (local, closer to production)

- **Database:** PostgreSQL via Docker Compose
- **Backend + DB:** `docker compose up`
- **Uses:** `docker-compose.yml` with hot-reload via volume mounts

### Production

- **Database:** Neon PostgreSQL (cloud, `postgresql+asyncpg://...`)
- **Backend:** Fly.io Docker container (built from `Dockerfile`)
- **Frontend:** Cloudflare Pages (built from `app/web/`)
- **Config:** Environment variables set via `fly secrets`
- **Deploys:** Automatic via GitHub Actions on push to `main`

---

## 3. Accounts & Dashboards

You need accounts on these services. Bookmark these dashboards:

| Service | Dashboard URL | What you do there |
|---------|--------------|-------------------|
| **GitHub** | https://github.com/SadhiraAI/mycontext | Code, pull requests, Actions (CI/CD) |
| **Fly.io** | https://fly.io/dashboard | Backend hosting, logs, secrets, scaling |
| **Neon** | https://console.neon.tech | Database, connection strings, SQL editor |
| **Cloudflare** | https://dash.cloudflare.com | DNS records, Pages deployments, analytics |
| **Google/Squarespace** | https://domains.squarespace.com | Domain registrar (nameservers point to Cloudflare) |

**GitHub Actions** (CI/CD pipeline): https://github.com/SadhiraAI/mycontext/actions

**GitHub Secrets** (deploy tokens): https://github.com/SadhiraAI/mycontext/settings/secrets/actions

---

## 4. Local Development

### First-time setup

```bash
# Clone the repo
git clone https://github.com/SadhiraAI/mycontext.git
cd mycontext

# Install Python dependencies (editable mode for SDK development)
pip install -e ".[dev]"
pip install -r app/requirements.txt

# Start the backend (uses SQLite by default)
uvicorn app.main:app --reload --port 8000

# In another terminal, start the frontend
cd app/web
npm install
npm run dev
```

The app is now running at `http://localhost:5173` (frontend) and `http://localhost:8000` (API).

### Docker Compose (PostgreSQL locally)

```bash
docker compose up
```

This starts the backend + a local PostgreSQL database. Useful for testing database-specific behavior before deploying.

### Running tests

```bash
# Lint
ruff check .

# Unit tests
pytest tests/unit/ -v --tb=short

# Both (what CI runs)
ruff check . && pytest tests/unit/ -v --tb=short
```

### Environment variables (local)

Create a `.env` file in the project root (never commit this):

```
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=any-string-for-dev
ENCRYPTION_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
```

See `.env.production.example` for all available variables.

---

## 5. CI/CD Pipeline

**What:** GitHub Actions (`.github/workflows/backend.yml`)

**Trigger:** Every push to `main` and every pull request.

**Pipeline steps:**

```
Push to main
    │
    ▼
┌─────────────────┐
│  1. Checkout     │
│  2. Python 3.12  │
│  3. pip install   │
│  4. ruff check .  │  ◀── Lint (code style, imports, type hints)
│  5. pytest        │  ◀── Unit tests (210+ tests)
└────────┬────────┘
         │ (only on push to main, not PRs)
         ▼
┌─────────────────┐
│  6. Deploy to    │
│     Fly.io       │  ◀── Builds Docker image, pushes, restarts machines
└─────────────────┘
```

**Key points:**
- PRs only run lint + tests (no deploy)
- Pushes to `main` run lint + tests + deploy
- Deploy uses `FLY_API_TOKEN` secret from GitHub repo settings
- Deploy builds the Docker image remotely on Fly.io's servers

**If CI fails:**
1. Go to https://github.com/SadhiraAI/mycontext/actions
2. Click the failed run
3. Read the error in the failing step
4. Fix locally, push again

---

## 6. Production Infrastructure

### Fly.io (Backend Hosting)

**What we did:** Containerized the FastAPI app with Docker and deployed to Fly.io.

**Config file:** `fly.toml`

```toml
app = 'sadhiraai-api'
primary_region = 'iad'           # US East

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = 'stop'    # Sleep when no traffic (saves money)
  auto_start_machines = true     # Wake on incoming request
  min_machines_running = 0       # Can scale to zero

[[vm]]
  memory = '256mb'               # Minimum viable RAM
  cpu_kind = 'shared'
  cpus = 1
```

**Useful Fly.io commands:**

```bash
# Check app status
fly status -a sadhiraai-api

# View logs (live streaming)
fly logs -a sadhiraai-api

# View logs (snapshot, no streaming)
fly logs -a sadhiraai-api -n

# SSH into the running container
fly ssh console -a sadhiraai-api

# List secrets (values are hidden)
fly secrets list -a sadhiraai-api

# Set a secret (restarts machines)
fly secrets set KEY="value" -a sadhiraai-api

# Manual deploy (bypasses CI)
fly deploy --remote-only

# Check SSL certificate status
fly certs show api.sadhiraai.com -a sadhiraai-api

# Scale memory if needed
fly scale memory 512 -a sadhiraai-api
```

### Dockerfile

The `Dockerfile` builds the production image:

1. Starts from `python:3.12-slim`
2. Installs system deps (`gcc`, `libpq-dev` for PostgreSQL)
3. Installs Python deps from `app/requirements.txt`
4. Copies application code (`app/`, `src/`, `alembic.ini`)
5. Installs the mycontext SDK (with enterprise templates included via `sed` workaround)
6. Runs uvicorn on port 8000

**Important:** The `pyproject.toml` excludes enterprise templates for public PyPI releases. The `Dockerfile` uses `sed` to remove that exclusion so enterprise templates are included in your private deployment. Enterprise template usage is still gated by license keys at runtime.

---

## 7. Database & Migrations

### Neon PostgreSQL (Production)

**Dashboard:** https://console.neon.tech

**Connection string format:**
```
postgresql+asyncpg://USER:PASSWORD@ENDPOINT/DATABASE?sslmode=require
```

**Important:** The `DATABASE_URL` secret on Fly.io must use `postgresql+asyncpg://` prefix (not plain `postgresql://`) and must NOT include `channel_binding=require` (asyncpg doesn't support it).

### Alembic Migrations

Alembic manages database schema changes. Migration files live in `app/alembic/versions/`.

**How Alembic works:**
- `alembic/env.py` reads the database URL from `app/config.py`
- Converts `asyncpg` URL to `psycopg2` for sync operations
- Strips incompatible query params for psycopg2

**Run migrations on production:**

```bash
fly ssh console -a sadhiraai-api
cd /app
alembic upgrade head
exit
```

**Create a new migration (after changing models):**

```bash
# Locally, with your dev database
alembic revision --autogenerate -m "describe the change"

# Review the generated file in app/alembic/versions/
# Then commit and push — CI deploys the new code
# Then SSH into Fly.io and run: alembic upgrade head
```

**Database tables:**

| Table | Purpose |
|-------|---------|
| `users` | User accounts (email, hashed password, enterprise flag) |
| `license_keys` | Enterprise license keys (generated, redeemed) |
| `user_api_keys` | Encrypted LLM API keys (OpenAI, Anthropic, etc.) |
| `feedback` | User feedback submissions |
| `custom_templates` | User-created custom templates |

---

## 8. Domain & DNS Setup

**Registrar:** Google Domains (transferred to Squarespace)
**DNS Provider:** Cloudflare (nameservers changed from Google to Cloudflare)

### Cloudflare DNS Records

| Type | Name | Target | Proxy | Purpose |
|------|------|--------|-------|---------|
| CNAME | `api` | `sadhiraai-api.fly.dev` | DNS only (grey) | Backend API |
| CNAME | `mycontext` | `mycontext.pages.dev` | Proxied (orange) | Frontend app |
| MX | `sadhiraai.com` | `smtp.google.com` | DNS only | Email (Google Workspace) |

**Key rules:**
- `api.sadhiraai.com` must be **DNS only** (grey cloud) — Fly.io manages its own SSL certificate
- `mycontext.sadhiraai.com` should be **Proxied** (orange cloud) — Cloudflare handles SSL for Pages

### SSL Certificates

- **api.sadhiraai.com:** Let's Encrypt certificate managed by Fly.io (`fly certs add api.sadhiraai.com`)
- **mycontext.sadhiraai.com:** Cloudflare universal SSL (automatic with Pages custom domain)

---

## 9. Secrets Management

Production secrets are stored as **Fly.io secrets** (encrypted, injected as environment variables at runtime).

### Current secrets

| Secret | Purpose | How to generate |
|--------|---------|-----------------|
| `ENVIRONMENT` | Set to `production` | `fly secrets set ENVIRONMENT=production` |
| `DATABASE_URL` | Neon PostgreSQL connection string | Copy from Neon dashboard, change prefix to `postgresql+asyncpg://` |
| `SECRET_KEY` | JWT signing key (must be strong) | `openssl rand -hex 32` |
| `ENCRYPTION_KEY` | Fernet key for encrypting user API keys | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| `CORS_ORIGINS` | Allowed frontend origins | Comma-separated URLs |

### GitHub Secrets

| Secret | Purpose |
|--------|---------|
| `FLY_API_TOKEN` | Allows GitHub Actions to deploy to Fly.io |

Generate with: `fly tokens create deploy -a sadhiraai-api`

Set at: https://github.com/SadhiraAI/mycontext/settings/secrets/actions

---

## 10. Frontend Deployment

**Platform:** Cloudflare Pages
**Dashboard:** https://dash.cloudflare.com → Workers & Pages → mycontext

### Build configuration

| Setting | Value |
|---------|-------|
| Framework preset | None |
| Build command | `cd app/web && npm install && npm run build` |
| Build output directory | `app/web/dist` |
| Root directory | `/` (repo root) |

### Environment variables (Cloudflare Pages)

| Variable | Value | Set where |
|----------|-------|-----------|
| `VITE_API_URL` | `https://api.sadhiraai.com/api` | Pages → Settings → Environment variables |

**Important:** Vite bakes `VITE_*` variables at **build time**, not runtime. After changing an env var, you must trigger a new deployment (Deployments → Retry deployment).

### Custom domain

Set up at: Pages project → Custom domains → `mycontext.sadhiraai.com`

### Redeploying frontend

Frontend redeploys automatically when you push to `main` (Cloudflare Pages watches the GitHub repo). To manually redeploy:
1. Go to Pages dashboard → Deployments
2. Click `...` on the latest deployment → Retry deployment

---

## 11. Deploying Code Changes

### Standard workflow (recommended)

```bash
# 1. Make changes locally
# 2. Test locally
ruff check .
pytest tests/unit/ -v --tb=short

# 3. Commit and push
git add -A
git commit -m "Describe what changed and why"
git push

# 4. GitHub Actions automatically:
#    - Runs lint + tests
#    - If passing AND on main branch, deploys to Fly.io

# 5. If you changed database models:
fly ssh console -a sadhiraai-api
cd /app && alembic upgrade head
exit
```

### Emergency manual deploy (skip CI)

```bash
fly deploy --remote-only
```

### Updating Fly.io secrets

```bash
fly secrets set KEY="value" -a sadhiraai-api
# This automatically restarts all machines
```

---

## 12. License Key Management

Enterprise features are gated by license keys stored in the `license_keys` database table.

### Generate keys (production)

```bash
# SSH into the production container
fly ssh console -a sadhiraai-api

# Generate a license key
cd /app
python -c "
import secrets, uuid
key = 'MC-ENT-' + secrets.token_hex(16).upper()
print(f'License key: {key}')
"
```

**Note:** The current `scripts/manage_licenses.py` uses SQLite and is meant for local dev. For production, you'll need to write a PostgreSQL-compatible version or manage keys directly via SQL through Neon's SQL editor.

### Grant enterprise access via Neon SQL Editor

```sql
-- Insert a new license key
INSERT INTO license_keys (id, key, label, is_valid, created_at)
VALUES (gen_random_uuid()::text, 'MC-ENT-YOUR-KEY-HERE', 'customer-name', true, now());

-- Check existing keys
SELECT key, label, is_valid, redeemed_by, created_at FROM license_keys;
```

---

## 13. Monitoring & Debugging

### Backend logs

```bash
# Live logs
fly logs -a sadhiraai-api

# Snapshot (no streaming)
fly logs -a sadhiraai-api -n
```

### App status

```bash
fly status -a sadhiraai-api
```

### Database queries (Neon)

Use the SQL Editor at https://console.neon.tech to run queries directly.

### Frontend errors

Open browser DevTools (F12) → Console tab to see JavaScript errors.

### Web Analytics

Cloudflare Web Analytics is embedded in the frontend (`index.html`). View at:
Cloudflare Dashboard → your site → Analytics & logs → Web Analytics

---

## 14. Common Issues & Fixes

### "Failed to fetch" in the frontend

**Cause:** CORS blocking API requests.
**Fix:** Ensure `CORS_ORIGINS` includes `https://mycontext.sadhiraai.com`:
```bash
fly secrets set CORS_ORIGINS="https://mycontext.sadhiraai.com,https://mycontext.pages.dev,http://localhost:5173,http://localhost:5174" -a sadhiraai-api
```

### "sslmode parameter" / asyncpg connection error

**Cause:** `DATABASE_URL` has parameters asyncpg doesn't understand.
**Fix:** Use this format (no `channel_binding`):
```
postgresql+asyncpg://user:pass@host/db?sslmode=require
```

### "Invalid host header"

**Cause:** `TrustedHostMiddleware` rejecting the domain.
**Fix:** Add the domain to `allowed_hosts` in `app/config.py`.

### "cannot import name 'enterprise'"

**Cause:** Enterprise templates excluded from wheel build.
**Fix:** The `Dockerfile` uses `sed` to include them. If rebuilding locally, use `pip install -e .` (editable install includes everything).

### CI lint failures

**Fix:** Run `ruff check --fix .` locally, then commit.

### CI test failures

**Fix:** Run `pytest tests/unit/ -v --tb=short` locally to reproduce, fix, commit.

### DNS not working

**Check:** Cloudflare DNS records are correct (see Section 8).
**Wait:** DNS propagation can take up to 24 hours after nameserver changes.

### Fly.io deploy auth error

**Cause:** `FLY_API_TOKEN` expired or not set.
**Fix:** Generate a new one: `fly tokens create deploy -a sadhiraai-api` and update GitHub Secrets.

---

## 15. Future Enhancements

Planned features (see `docs/POST_LAUNCH_TODO.md`):

| Feature | Tech | Priority |
|---------|------|----------|
| Multi-Factor Auth (MFA) | `pyotp` + QR codes | High |
| Payment Portal | Stripe integration | High |
| Error Tracking | Sentry | Medium |
| Email Notifications | Resend | Medium |
| Production License Manager | PostgreSQL-compatible CLI | Medium |

### Adding a new feature (workflow)

1. Create a branch: `git checkout -b feature/my-feature`
2. Develop and test locally
3. Run `ruff check .` and `pytest tests/unit/` to verify
4. Push and create a PR: `git push -u origin feature/my-feature`
5. PR triggers lint + tests (no deploy)
6. After review, merge to `main`
7. Merge triggers lint + tests + deploy to production
8. If database changes: SSH into Fly.io and run `alembic upgrade head`

### Adding a new database table

1. Add the model in `app/db/models.py`
2. Import it in `app/db/__init__.py`
3. Import it in `app/alembic/env.py` (so Alembic sees it)
4. Generate migration: `alembic revision --autogenerate -m "add my_table"`
5. Review the generated file in `app/alembic/versions/`
6. Test locally: `alembic upgrade head`
7. Commit, push, wait for deploy
8. Run on production: `fly ssh console` → `alembic upgrade head`
