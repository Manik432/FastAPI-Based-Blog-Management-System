"""add content column to posts table

Revision ID: 02f27f27a19a
Revises: a634b6079579
Create Date: 2025-08-10 19:52:08.614799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02f27f27a19a'
down_revision: Union[str, Sequence[str], None] = 'a634b6079579'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
