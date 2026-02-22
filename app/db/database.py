"""Database connection and session management."""

import ssl
from collections.abc import AsyncGenerator
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()


def _prepare_async_url(url: str) -> tuple[str, dict]:
    """Strip query params asyncpg doesn't understand; return (clean_url, connect_args)."""
    connect_args: dict = {}
    if url.startswith("postgresql"):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        sslmode = params.pop("sslmode", [None])[0]
        params.pop("channel_binding", None)
        if sslmode and sslmode != "disable":
            connect_args["ssl"] = ssl.create_default_context()
        url = urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in params.items()})))
    return url, connect_args


_db_url, _connect_args = _prepare_async_url(settings.database_url)

engine = create_async_engine(
    _db_url,
    echo=settings.debug,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI that yields a DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create all tables (dev convenience; production uses Alembic migrations)."""
    if not settings.is_production:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
