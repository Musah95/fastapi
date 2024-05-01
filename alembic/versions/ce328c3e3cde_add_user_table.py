"""add user table

Revision ID: ce328c3e3cde
Revises: 60dc9e203cf2
Create Date: 2024-05-01 10:37:38.901910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce328c3e3cde'
down_revision: Union[str, None] = '60dc9e203cf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
