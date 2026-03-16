"""user_posts

Revision ID: 0362d35b6e5c
Revises: 7aecc0993548
Create Date: 2026-03-16 09:19:42.487506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0362d35b6e5c'
down_revision: Union[str, Sequence[str], None] = '7aecc0993548'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("user_posts",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("postUserId", sa.Integer, nullable=False),
                    sa.Column("username", sa.String, unique=True, nullable=False),
                    sa.Column("email", sa.String, unique=True, nullable=False),
                    sa.Column("postTitle", sa.String, nullable=False),
                    sa.Column("postContent",sa.String, nullable=False, unique=True),
                    sa.Column("up_votes",sa.Integer, nullable=False, server_default='0'),
                    sa.Column("down_votes",sa.Integer, nullable=False, server_default='0'),
                    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.text("now()")),
                    sa.Column("lastUpdatedAt",sa.DateTime, nullable=False, server_default=sa.text("now()")), )



def downgrade() -> None:
    """Downgrade schema."""
    pass
