"""post_votes

Revision ID: 688147a88b8c
Revises: 0362d35b6e5c
Create Date: 2026-03-16 09:20:12.469601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '688147a88b8c'
down_revision: Union[str, Sequence[str], None] = '0362d35b6e5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
