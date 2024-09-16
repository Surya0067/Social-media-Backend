"""Updated OTP table in expired time 

Revision ID: a8bfe3faed14
Revises: bc01a87d9b60
Create Date: 2024-09-12 15:01:16.353827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8bfe3faed14'
down_revision: Union[str, None] = 'bc01a87d9b60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('otp', sa.Integer(), nullable=False),
    sa.Column('expired_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otp_id'), 'otp', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_otp_id'), table_name='otp')
    op.drop_table('otp')
    # ### end Alembic commands ###
