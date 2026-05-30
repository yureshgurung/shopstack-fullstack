"""add email column

Revision ID: 0d0ef60269a0
Revises: 
Create Date: 2026-05-29 06:51:00.836230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d0ef60269a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('users', 'email')
