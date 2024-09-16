"""add is_active in post table

Revision ID: ceb36fe788cb
Revises: 0c245df07d5c
Create Date: 2024-09-15 15:22:48.126592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ceb36fe788cb'
down_revision: Union[str, None] = '0c245df07d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('image_post_item', 'image_id',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.add_column('post', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'is_active')
    op.alter_column('image_post_item', 'image_id',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
