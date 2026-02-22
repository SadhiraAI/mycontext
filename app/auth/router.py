"""Authentication API: signup, login."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import create_access_token, get_password_hash, get_current_user, verify_password
from app.db import get_db
from app.db.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SignupRequest(BaseModel):
    """Signup request body."""

    email: EmailStr
    password: str


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
    enterprise_license: bool = False

    model_config = {"from_attributes": True}


@router.post("/signup", response_model=TokenResponse)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Register a new user."""
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=body.email,
        hashed_password=get_password_hash(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token, user_id=user.id, email=user.email)


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


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)) -> UserResponse:
    """Get current user info."""
    return UserResponse(
        id=user.id,
        email=user.email,
        enterprise_license=getattr(user, "enterprise_license", False),
    )
