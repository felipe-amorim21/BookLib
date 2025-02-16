"""add manual 2

Revision ID: 1315666ab3dd
Revises: bf74fcaf81e8
Create Date: 2025-02-16 09:28:22.537734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1315666ab3dd'
down_revision: Union[str, None] = 'bf74fcaf81e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Criar a tabela 'favorites'
    op.create_table(
        'favorites',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('book_id', sa.Integer(), sa.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['book_id'], ['books.id']),
    )


def downgrade():
    # Reverter a criação da tabela 'favorites'
    op.drop_table('favorites')
