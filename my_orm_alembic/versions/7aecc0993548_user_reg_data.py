"""user_reg_data

Revision ID: 7aecc0993548
Revises: f8efd15ef102
Create Date: 2026-03-16 09:18:04.533693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aecc0993548'
down_revision: Union[str, Sequence[str], None] = 'f8efd15ef102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
