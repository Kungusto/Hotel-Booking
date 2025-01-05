"""init rooms

Revision ID: a5a377cdf166
Revises: b3f69fe382a4
Create Date: 2025-01-04 18:55:19.725258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a5a377cdf166'
down_revision: Union[str, None] = '63ee1df09fb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
