"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-04 00:00:00.000000
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ideas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_unique_constraint("uq_ideas_slug", "ideas", ["slug"])
    op.create_index("ix_ideas_category", "ideas", ["category"])


def downgrade() -> None:
    op.drop_index("ix_ideas_category", table_name="ideas")
    op.drop_constraint("uq_ideas_slug", "ideas", type_="unique")
    op.drop_table("ideas")
