"""create votes table"""

revision = "189c1b1f2ba0"
down_revision = "21d1b4a7c423"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "votes",
        sa.Column(
            "post_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("post_id", "user_id"),
    )

    op.create_foreign_key(
        "fk_votes_post_id_posts",
        "votes",
        "posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_votes_user_id_users",
        "votes",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("fk_votes_user_id_users", "votes", type_="foreignkey")
    op.drop_constraint("fk_votes_post_id_posts", "votes", type_="foreignkey")
    op.drop_table("votes")
