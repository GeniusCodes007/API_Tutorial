"""personal_data

Revision ID: f8efd15ef102
Revises: 
Create Date: 2026-03-16 09:15:14.041162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8efd15ef102'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("personal_data",

                    sa.Column("id",sa.Integer, nullable=False),
                    sa.Column("surname", sa.String, nullable=False),
                    sa.Column("firstname",sa.String, nullable=False),
                    sa.Column("other_names", sa.String, nullable=True),
                    sa.Column("username", sa.String, nullable=False, unique=True),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("is_adult", sa.Boolean, nullable=False, server_default=sa.text("false")),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint("id", name="personal_data_pkey"),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
