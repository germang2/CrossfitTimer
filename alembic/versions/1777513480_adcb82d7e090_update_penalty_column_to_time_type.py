"""update penalty column to time type

Revision ID: adcb82d7e090
Revises: 977891d4fd83
Create Date: 2026-04-29 20:44:40.185743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adcb82d7e090'
down_revision: Union[str, None] = '977891d4fd83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('groups_athletes') as batch_op:
        batch_op.drop_column('penalty')
        batch_op.add_column(sa.Column('penalty', sa.Time(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('groups_athletes') as batch_op:
        batch_op.drop_column('penalty')
        batch_op.add_column(sa.Column('penalty', sa.Integer(), nullable=True, server_default='0'))
