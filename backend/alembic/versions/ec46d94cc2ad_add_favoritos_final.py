"""add favoritos final

Revision ID: ec46d94cc2ad
Revises: 1315666ab3dd
Create Date: 2025-02-16 09:59:30.623081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec46d94cc2ad'
down_revision: Union[str, None] = '1315666ab3dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='favorites_book_id_fkey'),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='favorites_book_id_fkey1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favorites_user_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favorites_user_id_fkey1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey')
    )
    # ### end Alembic commands ###
