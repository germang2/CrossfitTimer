"""add penalty and status columns to groups_athletes

Revision ID: 977891d4fd83
Revises: 7c62131d03e8
Create Date: 2026-04-20 21:18:25.316371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '977891d4fd83'
down_revision: Union[str, None] = '7c62131d03e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # get connection
    conn = op.get_bind()
    # inspect columns
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('groups_athletes')]

    with op.batch_alter_table('groups_athletes') as batch_op:
        if 'penalty' not in columns:
            batch_op.add_column(sa.Column('penalty', sa.Integer(), nullable=True, server_default='0'))
        
        if 'status' not in columns:
            batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=True, server_default='1'))


def downgrade() -> None:
    with op.batch_alter_table('groups_athletes') as batch_op:
        batch_op.drop_column('penalty')
        batch_op.drop_column('status')
