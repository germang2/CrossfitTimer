"""create column tasks_completed

Revision ID: 7c62131d03e8
Revises: 
Create Date: 2024-09-23 21:42:18.687577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c62131d03e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Creates column tasks_completed in groups_athletes
    """
    op.add_column('groups_athletes', sa.Column('tasks_completed', sa.Integer, nullable=True))


def downgrade() -> None:
    """
    Rollback changes
    """
    op.drop_column('groups_athletes', 'tasks_completed')
