"""API key management: encrypted storage, CRUD, active provider selection."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user
from app.db import get_db
from app.db.encryption import decrypt_api_key, encrypt_api_key
from app.db.models import User, UserAPIKey

router = APIRouter(prefix="/api/keys", tags=["keys"])

VALID_PROVIDERS = {"openai", "anthropic", "google"}


class AddKeyRequest(BaseModel):
    """Add API key request."""

    provider: str
    api_key: str
    preferred_model: str | None = None


class UpdateModelRequest(BaseModel):
    """Update preferred model for a provider."""

    model: str


class KeyResponse(BaseModel):
    """Key metadata (never returns actual key)."""

    provider: str
    preferred_model: str | None = None
    is_active: bool = False
    created_at: str


class ActiveProviderResponse(BaseModel):
    """The user's currently active provider + model."""

    provider: str | None = None
    model: str | None = None
    has_key: bool = False


@router.get("", response_model=list[KeyResponse])
async def list_keys(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[KeyResponse]:
    """List user's stored providers (never returns keys)."""
    result = await db.execute(
        select(UserAPIKey).where(UserAPIKey.user_id == user.id)
    )
    keys = result.scalars().all()
    return [
        KeyResponse(
            provider=k.provider,
            preferred_model=k.preferred_model,
            is_active=k.is_active,
            created_at=k.created_at.isoformat(),
        )
        for k in keys
    ]


@router.get("/active", response_model=ActiveProviderResponse)
async def get_active_provider(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ActiveProviderResponse:
    """Return the user's active provider and model."""
    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user.id,
            UserAPIKey.is_active.is_(True),
        )
    )
    active = result.scalar_one_or_none()
    if not active:
        return ActiveProviderResponse()
    return ActiveProviderResponse(
        provider=active.provider,
        model=active.preferred_model,
        has_key=True,
    )


@router.post("", response_model=KeyResponse)
async def add_key(
    body: AddKeyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KeyResponse:
    """Add or replace API key for a provider. First key auto-activates."""
    provider = body.provider.lower()
    if provider not in VALID_PROVIDERS:
        raise HTTPException(400, detail=f"Provider must be one of: {VALID_PROVIDERS}")

    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user.id,
            UserAPIKey.provider == provider,
        )
    )
    existing = result.scalar_one_or_none()
    encrypted = encrypt_api_key(body.api_key)

    # Check if user has any keys at all (for auto-activate)
    all_keys = await db.execute(
        select(UserAPIKey).where(UserAPIKey.user_id == user.id)
    )
    has_any = len(all_keys.scalars().all()) > 0

    if existing:
        existing.encrypted_key = encrypted
        if body.preferred_model is not None:
            existing.preferred_model = body.preferred_model
        await db.commit()
        await db.refresh(existing)
        return KeyResponse(
            provider=provider,
            preferred_model=existing.preferred_model,
            is_active=existing.is_active,
            created_at=existing.created_at.isoformat(),
        )

    new_key = UserAPIKey(
        user_id=user.id,
        provider=provider,
        encrypted_key=encrypted,
        preferred_model=body.preferred_model,
        is_active=not has_any,  # auto-activate first key
    )
    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)
    return KeyResponse(
        provider=provider,
        preferred_model=new_key.preferred_model,
        is_active=new_key.is_active,
        created_at=new_key.created_at.isoformat(),
    )


@router.put("/{provider}/activate", response_model=KeyResponse)
async def activate_provider(
    provider: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KeyResponse:
    """Set a provider as the active one (deactivates all others)."""
    provider = provider.lower()

    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user.id,
            UserAPIKey.provider == provider,
        )
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(404, detail=f"No key stored for {provider}")

    # Deactivate all keys for this user
    await db.execute(
        update(UserAPIKey)
        .where(UserAPIKey.user_id == user.id)
        .values(is_active=False)
    )
    # Activate the target
    target.is_active = True
    await db.commit()
    await db.refresh(target)
    return KeyResponse(
        provider=target.provider,
        preferred_model=target.preferred_model,
        is_active=True,
        created_at=target.created_at.isoformat(),
    )


@router.put("/{provider}/model", response_model=KeyResponse)
async def update_model(
    provider: str,
    body: UpdateModelRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KeyResponse:
    """Update the preferred model for a provider."""
    provider = provider.lower()
    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user.id,
            UserAPIKey.provider == provider,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, detail=f"No key stored for {provider}")

    row.preferred_model = body.model
    await db.commit()
    await db.refresh(row)
    return KeyResponse(
        provider=row.provider,
        preferred_model=row.preferred_model,
        is_active=row.is_active,
        created_at=row.created_at.isoformat(),
    )


@router.delete("/{provider}")
async def delete_key(
    provider: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Remove API key for a provider."""
    provider = provider.lower()
    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user.id,
            UserAPIKey.provider == provider,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, detail="Key not found")
    was_active = row.is_active
    await db.delete(row)

    # If deleted key was active, activate another if available
    if was_active:
        remaining = await db.execute(
            select(UserAPIKey).where(UserAPIKey.user_id == user.id)
        )
        next_key = remaining.scalars().first()
        if next_key:
            next_key.is_active = True

    await db.commit()
    return {"status": "deleted", "provider": provider}


async def get_decrypted_key_for_user(db: AsyncSession, user_id: str, provider: str) -> str | None:
    """Get decrypted API key for a user and provider. Used by execute service."""
    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user_id,
            UserAPIKey.provider == provider,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        return None
    return decrypt_api_key(row.encrypted_key)


async def get_active_provider_for_user(db: AsyncSession, user_id: str) -> dict:
    """Get active provider + model + decrypted key for a user."""
    result = await db.execute(
        select(UserAPIKey).where(
            UserAPIKey.user_id == user_id,
            UserAPIKey.is_active.is_(True),
        )
    )
    active = result.scalar_one_or_none()
    if not active:
        return {"provider": None, "model": None, "api_key": None}
    return {
        "provider": active.provider,
        "model": active.preferred_model,
        "api_key": decrypt_api_key(active.encrypted_key),
    }
