"""schema adjustments"""

revision = "5a94b6347174"
down_revision = "189c1b1f2ba0"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # Allow posts.content to be nullable
    op.alter_column(
        "posts",
        "content",
        existing_type=sa.TEXT(),
        nullable=True,
    )

    # Ensure updated_at is NOT NULL
    op.alter_column(
        "posts",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "users",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )


def downgrade():
    op.alter_column(
        "users",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "posts",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )

    op.alter_column(
        "posts",
        "content",
        existing_type=sa.TEXT(),
        nullable=False,
    )
