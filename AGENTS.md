# AGENTS.md — mycontext-ai

> Root-level instructions for any AI agent working on this repository.

## Project Overview

mycontext-ai is a Python SDK for cognitive templates — reusable prompt
architectures that produce structured Context objects (Guidance + Directive +
Constraints) for any LLM. It ships with 88 cognitive patterns, quality metrics,
multi-template fusion, chain orchestration, and a web application.

## Repository Layout

| Path | What it is |
|------|------------|
| `src/mycontext/` | Python SDK (pip-installable) |
| `app/` | Web app — FastAPI backend + React frontend |
| `website/` | Docusaurus documentation site |
| `docs/` | Research, experiments, notebooks, articles |
| `examples/` | SDK usage examples and orchestration demos |
| `tests/` | pytest test suite |

## Key Conventions

- Python 3.11+, type hints, Pydantic v2
- Linting: `ruff check .` Formatting: `ruff format .`
- Tests: `pytest -v`
- Templates inherit from `Pattern`, must implement `build_context()` and `GENERIC_PROMPT`
- All LLM calls route through LiteLLM

## CRITICAL — LiteLLM (supply chain)

- **Never upgrade or repin `litellm`** in `pyproject.toml` / `uv.lock` unless the **maintainer explicitly asks** in this chat.
- **Compromised releases — never use:** **`1.82.8`**, and **`1.87` / `1.87.x`**.
- The repo pins an exact LiteLLM version on purpose; treat it as **frozen** for routine work.
- Two skill systems exist — SDK SkillRunner demos in `docs/examples/skills/` (for research) vs Cursor Agent skills in `.cursor/skills/` (for development)

## CRITICAL — Enterprise & Deployment Rules

- **Enterprise templates** (`src/mycontext/templates/enterprise/`) are EXCLUDED from PyPI builds — `pyproject.toml` has explicit exclude rules for wheel and sdist. NEVER remove these.
- **Enterprise gating tests** (`tests/unit/test_enterprise_gating.py`) MUST pass before any release.
- **NEVER use "Cursor"** in commit messages, PR titles, or any GitHub-facing text.
- **NEVER commit** `.env`, API keys, PyPI tokens, or credentials.
- **NEVER force-push** to main.
- **Version** lives in TWO places that MUST match: `pyproject.toml` and `src/mycontext/__init__.py`.
- **Manual push only** — always provide git push commands for the user to run; do not auto-push.
- **Full deployment guide**: `docs/DEPLOYMENT_GUIDE.md` — follow it for any release.
- **CI/CD**: `backend.yml` (src/app/tests → Fly.io), `docs.yml` (website → Cloudflare Pages). Research pages excluded from production docs builds.

## When Modifying Templates

1. Read the existing template and its test before editing
2. Preserve the depth parameter behavior (quick/standard/thorough)
3. Keep GENERIC_PROMPT between 600-1200 chars
4. Run `pytest -k <template_name> -v` after changes
5. Constraints must be specific, not vague

## When Modifying the Web App

- Backend endpoints go in `app/api/`, services in `app/services/`
- Protected routes use `Depends(get_current_user)`
- Frontend: React functional components, CSS variables for theming
- Dev: `uvicorn app.main:app --reload` (backend), `cd app/web && npm start` (frontend)

## When Writing Documentation

- Use real mycontext API imports in code examples
- Docusaurus blog frontmatter requires: title, authors, tags
- Research results saved as JSON alongside notebooks
