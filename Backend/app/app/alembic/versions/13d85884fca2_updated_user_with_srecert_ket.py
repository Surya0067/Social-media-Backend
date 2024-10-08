"""updated user with srecert ket

Revision ID: 13d85884fca2
Revises: e8ee29f8970f
Create Date: 2024-09-16 10:23:35.006864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '13d85884fca2'
down_revision: Union[str, None] = 'e8ee29f8970f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('secret_key', sa.String(length=40), nullable=True))
    op.drop_column('user', 'srecert_key')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('srecert_key', mysql.VARCHAR(length=40), nullable=True))
    op.drop_column('user', 'secret_key')
    # ### end Alembic commands ###
