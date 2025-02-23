"""add user table

Revision ID: ea64e86aa413
Revises: 6f652e4c2376
Create Date: 2025-02-23 11:52:40.326959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea64e86aa413'
down_revision: Union[str, None] = '6f652e4c2376'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('email', sa.String(), nullable = False),
        sa.Column('password', sa.String(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True), 
                  server_default = sa.text('now()'), 
                  nullable = False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
