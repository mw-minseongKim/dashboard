"""create item table

Revision ID: 5e46aa0fdc96
Revises: a04b47239556
Create Date: 2026-02-19 16:14:35.415481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5e46aa0fdc96'
down_revision: Union[str, Sequence[str], None] = 'a04b47239556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'items',
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('items_pkey')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('items')
