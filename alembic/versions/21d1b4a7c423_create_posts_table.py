"""create posts table"""

revision = "21d1b4a7c423"
down_revision = "7169e56b796a"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "posts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_foreign_key(
        "fk_posts_owner_id_users",
        "posts",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_index(
        "ix_posts_owner_id",
        "posts",
        ["owner_id"],
    )


def downgrade():
    op.drop_index("ix_posts_owner_id", table_name="posts")
    op.drop_constraint("fk_posts_owner_id_users", "posts", type_="foreignkey")
    op.drop_table("posts")
