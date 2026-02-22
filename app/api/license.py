"""License API: activate enterprise license keys."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_user
from app.db import get_db
from app.db.models import LicenseKey, User

router = APIRouter(prefix="/api/license", tags=["license"])


class ActivateRequest(BaseModel):
    key: str


class ActivateResponse(BaseModel):
    success: bool
    message: str
    enterprise_license: bool


class LicenseStatusResponse(BaseModel):
    enterprise_license: bool
    activated_at: str | None = None


@router.post("/activate", response_model=ActivateResponse)
async def activate_license(
    body: ActivateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ActivateResponse:
    """Redeem a license key to unlock enterprise features."""
    if getattr(user, "enterprise_license", False):
        return ActivateResponse(
            success=True,
            message="Enterprise license is already active on this account.",
            enterprise_license=True,
        )

    key_val = body.key.strip()
    if not key_val:
        raise HTTPException(400, detail="License key is required.")

    result = await db.execute(
        select(LicenseKey).where(LicenseKey.key == key_val)
    )
    license_key = result.scalar_one_or_none()

    if not license_key:
        raise HTTPException(404, detail="Invalid license key.")

    if not license_key.is_valid:
        raise HTTPException(400, detail="This license key has been revoked.")

    if license_key.redeemed_by is not None:
        raise HTTPException(
            400,
            detail="This license key has already been redeemed.",
        )

    license_key.redeemed_by = user.id
    license_key.redeemed_at = datetime.now(UTC)

    await db.execute(
        update(User).where(User.id == user.id).values(enterprise_license=True)
    )

    await db.flush()

    return ActivateResponse(
        success=True,
        message="Enterprise license activated! Access to all 85 patterns.",
        enterprise_license=True,
    )


@router.get("/status", response_model=LicenseStatusResponse)
async def license_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LicenseStatusResponse:
    """Get current license status for the authenticated user."""
    activated_at = None
    if getattr(user, "enterprise_license", False):
        result = await db.execute(
            select(LicenseKey.redeemed_at).where(
                LicenseKey.redeemed_by == user.id
            )
        )
        row = result.first()
        if row and row[0]:
            activated_at = row[0].isoformat()

    return LicenseStatusResponse(
        enterprise_license=getattr(user, "enterprise_license", False),
        activated_at=activated_at,
    )
