"""empty message

Revision ID: c6133edc1b45
Revises: d4ba34f31b6f
Create Date: 2025-08-15 19:35:48.661785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6133edc1b45'
down_revision: Union[str, Sequence[str], None] = 'd4ba34f31b6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
