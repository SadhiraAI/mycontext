# mycontext Web UI

React + Vite frontend for the mycontext web application.

## Run

1. Start the backend (from project root): `uvicorn app.main:app --reload`
2. Start the frontend: `npm run dev`
3. Open http://localhost:5173

API requests to `/api/*` are proxied to the backend.

## Pages

- **Login / Signup** - Auth
- **Dashboard** - Overview and nav
- **Templates** - Browse 85 patterns, build context
- **Chain Builder** - Suggest chain, run orchestration, optionally execute with LLM
- **Settings** - Add/remove encrypted API keys (OpenAI, Anthropic, Google)
- **Custom** - Placeholder for future custom templates CRUD
