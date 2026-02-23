"""Add email verification fields to users table.

Revision ID: 9a2f3b4c5d6e
Revises: 824ab1024dff
Create Date: 2026-02-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9a2f3b4c5d6e"
down_revision: str | None = "824ab1024dff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email_verified", sa.Boolean(), nullable=True, server_default=sa.text("false")))
    op.add_column("users", sa.Column("email_verify_token", sa.String(128), nullable=True))
    op.execute("UPDATE users SET email_verified = true")


def downgrade() -> None:
    op.drop_column("users", "email_verify_token")
    op.drop_column("users", "email_verified")
