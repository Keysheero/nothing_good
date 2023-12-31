"""Reborn

Revision ID: 0b2258b5ee40
Revises: 
Create Date: 2023-12-15 18:26:12.014334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b2258b5ee40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_users')),
    sa.UniqueConstraint('chat_id', name=op.f('uq_users_chat_id'))
    )
    op.create_table('channels',
    sa.Column('channel_id', sa.String(length=32), nullable=False),
    sa.Column('user_fk', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_fk'], ['users.user_id'], name=op.f('fk_channels_user_fk_users')),
    sa.PrimaryKeyConstraint('channel_id', name=op.f('pk_channels'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('channels')
    op.drop_table('users')
    # ### end Alembic commands ###
