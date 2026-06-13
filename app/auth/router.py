"""Authentication API: signup, login, email verification."""

import logging
import re
import secrets

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import create_access_token, get_current_user, get_password_hash, verify_password
from app.db import get_db
from app.db.models import User
from app.services.email_service import send_verification_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

DISPOSABLE_DOMAINS = frozenset({
    "tempmail.com", "throwaway.email", "guerrillamail.com", "guerrillamail.de",
    "guerrillamail.net", "guerrillamail.org", "mailinator.com", "yopmail.com",
    "10minutemail.com", "trashmail.com", "trashmail.net", "trashmail.me",
    "dispostable.com", "sharklasers.com", "guerrillamailblock.com",
    "grr.la", "discard.email", "maildrop.cc", "mailnesia.com", "tempail.com",
    "temp-mail.org", "temp-mail.io", "fakeinbox.com", "getairmail.com",
    "getnada.com", "mohmal.com", "burnermail.io", "inboxbear.com",
    "mailcatch.com", "mintemail.com", "mytemp.email", "tempr.email",
    "throwam.com", "tmail.ws", "tmpmail.net", "tmpmail.org", "wegwerfmail.de",
    "emailondeck.com", "crazymailing.com", "mailtemp.net", "harakirimail.com",
    "spamgourmet.com", "mailexpire.com", "safetymail.info",
})


def _validate_password(password: str) -> str:
    """Enforce password strength: min 8 chars, 1 uppercase, 1 lowercase, 1 digit."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    return password


def _check_disposable_email(email: str) -> str:
    """Reject sign-ups from known disposable email providers."""
    domain = email.rsplit("@", 1)[-1].lower()
    if domain in DISPOSABLE_DOMAINS:
        raise ValueError("Disposable email addresses are not allowed. Please use a permanent email.")
    return email


class SignupRequest(BaseModel):
    """Signup request body."""

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return _validate_password(v)

    @field_validator("email")
    @classmethod
    def no_disposable_email(cls, v: str) -> str:
        return _check_disposable_email(v)


class LoginRequest(BaseModel):
    """Login request body."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


class UserResponse(BaseModel):
    """User info (no password)."""

    id: str
    email: str
    email_verified: bool = False

    model_config = {"from_attributes": True}


class SignupResponse(BaseModel):
    """Signup response — includes token + verification status."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    email_verified: bool = False
    verification_sent: bool = False


@router.post("/signup", response_model=SignupResponse)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)) -> SignupResponse:
    """Register a new user and send verification email."""
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    verify_token = secrets.token_urlsafe(48)

    user = User(
        email=body.email,
        hashed_password=get_password_hash(body.password),
        email_verified=False,
        email_verify_token=verify_token,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    verification_sent = await send_verification_email(body.email, verify_token)

    token = create_access_token(subject=user.id)
    return SignupResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        email_verified=False,
        verification_sent=verification_sent,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Login and return JWT."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token, user_id=user.id, email=user.email)


@router.get("/verify-email")
async def verify_email(
    token: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Verify email address using the token from the verification link."""
    result = await db.execute(
        select(User).where(User.email_verify_token == token)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification link.")

    if user.email_verified:
        return {"success": True, "message": "Email already verified."}

    user.email_verified = True
    user.email_verify_token = None
    await db.commit()

    logger.info("Email verified for user %s (%s)", user.id, user.email)
    return {"success": True, "message": "Email verified successfully!"}


@router.post("/resend-verification")
async def resend_verification(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Resend verification email for the current user."""
    if user.email_verified:
        return {"success": True, "message": "Email already verified."}

    new_token = secrets.token_urlsafe(48)
    user.email_verify_token = new_token
    await db.commit()

    sent = await send_verification_email(user.email, new_token)
    if not sent:
        raise HTTPException(
            status_code=503,
            detail="Could not send verification email. Please try again later.",
        )
    return {"success": True, "message": "Verification email sent. Check your inbox."}


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)) -> UserResponse:
    """Get current user info."""
    return UserResponse(
        id=user.id,
        email=user.email,
        email_verified=getattr(user, "email_verified", False),
    )
