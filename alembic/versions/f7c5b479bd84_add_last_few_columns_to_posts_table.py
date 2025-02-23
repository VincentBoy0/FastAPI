"""add last few columns to posts table

Revision ID: f7c5b479bd84
Revises: a3dcfbfb0e14
Create Date: 2025-02-23 16:52:54.399699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7c5b479bd84'
down_revision: Union[str, None] = 'a3dcfbfb0e14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), 
                                     nullable = False, server_default = 'TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), 
                                     nullable = False, server_default = sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
