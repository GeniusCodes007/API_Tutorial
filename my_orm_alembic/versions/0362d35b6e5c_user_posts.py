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
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
