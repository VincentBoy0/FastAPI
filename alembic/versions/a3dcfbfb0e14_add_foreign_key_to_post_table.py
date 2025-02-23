"""add foreign key to post table

Revision ID: a3dcfbfb0e14
Revises: ea64e86aa413
Create Date: 2025-02-23 16:41:31.231486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3dcfbfb0e14'
down_revision: Union[str, None] = 'ea64e86aa413'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key(
        'posts_users_fk', 
        source_table = 'posts', local_cols = ['owner_id'],
        referent_table = 'users', remote_cols = ['id'], ondelete = "CASCADE"
    )

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name = 'posts')
    op.drop_column('posts', 'owner_id')
