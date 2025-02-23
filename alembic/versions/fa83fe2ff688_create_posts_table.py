"""create posts table

Revision ID: fa83fe2ff688
Revises: 
Create Date: 2025-02-23 10:58:58.047495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa83fe2ff688'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                             sa.Column('title', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_table('posts')
