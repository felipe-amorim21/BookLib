"""Create books and reviews tables

Revision ID: e976ba8d16fe
Revises: 8df0b2333329
Create Date: 2024-12-01 15:32:21.142999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e976ba8d16fe'
down_revision: Union[str, None] = '8df0b2333329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
