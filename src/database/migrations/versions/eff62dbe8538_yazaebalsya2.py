"""YaZaebalsya2

Revision ID: eff62dbe8538
Revises: bc32e14c14ee
Create Date: 2023-10-31 21:45:47.154081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eff62dbe8538'
down_revision: Union[str, None] = 'bc32e14c14ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channels',
    sa.Column('channel_id', sa.String(length=32), nullable=False),
    sa.Column('user_fk', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_fk'], ['users.user_id'], name=op.f('fk_channels_user_fk_users')),
    sa.PrimaryKeyConstraint('channel_id', name=op.f('pk_channels'))
    )
    op.create_unique_constraint(op.f('uq_users_chat_id'), 'users', ['chat_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_chat_id'), 'users', type_='unique')
    op.drop_table('channels')
    # ### end Alembic commands ###
