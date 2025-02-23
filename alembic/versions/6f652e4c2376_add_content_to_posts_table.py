"""add content to posts table

Revision ID: 6f652e4c2376
Revises: fa83fe2ff688
Create Date: 2025-02-23 11:46:15.737099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f652e4c2376'
down_revision: Union[str, None] = 'fa83fe2ff688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
