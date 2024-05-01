"""add content to post table

Revision ID: 60dc9e203cf2
Revises: e390312e05be
Create Date: 2024-05-01 10:29:06.306457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60dc9e203cf2'
down_revision: Union[str, None] = 'e390312e05be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
