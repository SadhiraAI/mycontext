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

## CLI, Skills export, local MCP, and RaC

- **CLI** (`mycontext` console script, `src/mycontext/cli/`): `mycontext list`, `mycontext run <pattern>`, `mycontext skills export <name|all>`, `mycontext mcp`.
- **Skills export**: emits progressive-disclosure `SKILL.md` packages (Tier-1 name/description, Tier-2 body with pre-authored prompt + SDK scaffold, Tier-3 `references/`). `--plugin` emits a Claude Code / Cowork plugin manifest.
- **Local MCP** (`mycontext mcp`, optional `mcp` extra): a stdio FastMCP server exposing `suggest_patterns`, `transform`, and `score_output`. Local-only, $0.
- **Requirements-as-Code** (`src/mycontext/rac/`): authoring + scoring ONLY. Drafts a `requirements.yaml` (task taxonomy, rubrics, action risk matrix, pre-mortem) from cognitive patterns and scores outputs via `OutputEvaluator`. ANTI-GOAL: never add a RaC compiler, CI gate executor, or HITL/budget runtime here — enforcement is the customer's stack.

## CRITICAL — LiteLLM (supply chain)

- **Never upgrade or repin `litellm`** in `pyproject.toml` / `uv.lock` unless the **maintainer explicitly asks** in this chat.
- **Compromised releases — never use:** **`1.82.8`**, and **`1.87` / `1.87.x`**.
- The repo pins an exact LiteLLM version on purpose; treat it as **frozen** for routine work.
- Two skill systems exist — SDK SkillRunner demos in `docs/examples/skills/` (for research) vs Cursor Agent skills in `.cursor/skills/` (for development)

## CRITICAL — Open Source & Deployment Rules

- **All 88 cognitive patterns are open source** and ship in the PyPI wheel — there are no license tiers. The `templates/free/` and `templates/enterprise/` folders are a TAXONOMY only; both are packaged. Do NOT re-add wheel/sdist excludes or `include_enterprise` gating.
- **License shims**: `mycontext.activate_license` / `deactivate_license` / `is_enterprise_active` are deprecated no-op shims kept for one release; do not build new gating on them.
- **NEVER use "Cursor"** in commit messages, PR titles, or any GitHub-facing text.
- **NEVER commit** `.env`, API keys, PyPI tokens, or credentials.
- **NEVER force-push** to main.
- **Version** lives in TWO places that MUST match: `pyproject.toml` and `src/mycontext/version.py`.
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
