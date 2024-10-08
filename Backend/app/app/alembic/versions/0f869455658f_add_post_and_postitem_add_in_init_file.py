"""add post and postitem add in init file

Revision ID: 0f869455658f
Revises: 6da76158e9af
Create Date: 2024-09-13 17:17:15.413860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f869455658f'
down_revision: Union[str, None] = '6da76158e9af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('caption', sa.String(length=250), nullable=True),
    sa.Column('post_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=False)
    op.create_table('post_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('post_type', sa.String(length=10), nullable=True),
    sa.Column('post_content', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_item_id'), 'post_item', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_item_id'), table_name='post_item')
    op.drop_table('post_item')
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
