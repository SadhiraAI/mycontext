"""SQLAlchemy models for users, API keys, and custom templates."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid.uuid4())


class User(Base):
    """User account for authentication."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    enterprise_license: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    api_keys: Mapped[list["UserAPIKey"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    custom_templates: Mapped[list["CustomTemplate"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class LicenseKey(Base):
    """Pre-generated license keys for enterprise activation."""

    __tablename__ = "license_keys"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=generate_uuid)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_valid: Mapped[bool] = mapped_column(default=True)
    redeemed_by: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    redeemed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class UserAPIKey(Base):
    """Encrypted LLM provider API keys per user."""

    __tablename__ = "user_api_keys"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # openai, anthropic, google
    encrypted_key: Mapped[str] = mapped_column(Text, nullable=False)
    preferred_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="api_keys")

    __table_args__ = ({"sqlite_autoincrement": False},)


class Feedback(Base):
    """User-submitted feedback (bug reports, feature requests, general)."""

    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False)  # bug, feature, general
    message: Mapped[str] = mapped_column(Text, nullable=False)
    page_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CustomTemplate(Base):
    """User-created custom templates (Pattern-like structure stored as JSON)."""

    __tablename__ = "custom_templates"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    guidance: Mapped[str] = mapped_column(Text, nullable=False)  # JSON: {role, rules, style}
    directive_template: Mapped[str] = mapped_column(Text, nullable=False)
    input_schema: Mapped[str] = mapped_column(Text, nullable=False)  # JSON: list of {name, type, default}
    constraints: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON: must_include, must_not_include
    thinking_strategy: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="direct")
    examples: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON: [{input, output}]
    output_schema: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON: [{name, type}]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="custom_templates")
