"""Drop enterprise license gating (column + license_keys table).

mycontext is now fully open source — all cognitive patterns ship without
license tiers, so the ``users.enterprise_license`` column and the
``license_keys`` table are no longer needed.

Revision ID: b1c2d3e4f5a6
Revises: 9a2f3b4c5d6e
Create Date: 2026-06-13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b1c2d3e4f5a6"
down_revision: str | None = "9a2f3b4c5d6e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Drop the license_keys table first (it has a FK to users).
    op.drop_table("license_keys")
    # SQLite cannot drop a column in place — use batch mode for portability.
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("enterprise_license")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "enterprise_license",
                sa.Boolean(),
                server_default=sa.text("false"),
                nullable=False,
            )
        )
    op.create_table(
        "license_keys",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("key", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("label", sa.String(255), nullable=True),
        sa.Column("is_valid", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("redeemed_by", sa.CHAR(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
    )
