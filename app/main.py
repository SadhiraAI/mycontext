"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api import (
    chains_router,
    chat_router,
    custom_templates_router,
    evaluate_router,
    execute_router,
    feedback_router,
    keys_router,
    license_router,
    quality_router,
    templates_router,
    transform_router,
)
from app.auth import auth_router
from app.config import get_settings
from app.db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup."""
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Web application for mycontext - browse templates, build chains, execute with your LLM keys",
    lifespan=lifespan,
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url="/api/redoc" if not settings.is_production else None,
)


# --- Middleware (applied bottom-to-top, so order matters) ---

if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[h.strip() for h in settings.allowed_hosts.split(",")],
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add standard security headers to every response."""
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


# Simple in-memory rate limiter for auth endpoints (no extra dependency needed)
_rate_limit_store: dict[str, list[float]] = {}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 10  # requests per window for auth


@app.middleware("http")
async def rate_limit_auth(request: Request, call_next):
    """Rate-limit auth endpoints to prevent brute-force attacks."""
    import time

    if request.url.path in ("/api/auth/login", "/api/auth/signup"):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        hits = _rate_limit_store.get(client_ip, [])
        hits = [t for t in hits if now - t < RATE_LIMIT_WINDOW]
        if len(hits) >= RATE_LIMIT_MAX:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
            )
        hits.append(now)
        _rate_limit_store[client_ip] = hits

    return await call_next(request)


# --- Routers ---

app.include_router(auth_router)
app.include_router(keys_router)
app.include_router(license_router)
app.include_router(templates_router)
app.include_router(custom_templates_router)
app.include_router(chains_router)
app.include_router(transform_router)
app.include_router(quality_router)
app.include_router(execute_router)
app.include_router(chat_router)
app.include_router(evaluate_router)
app.include_router(feedback_router)


@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/health")
async def health():
    """API health check."""
    return {"status": "ok"}
