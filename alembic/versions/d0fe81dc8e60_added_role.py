"""Added role

Revision ID: d0fe81dc8e60
Revises: 5c29976a36e3
Create Date: 2024-12-20 01:56:22.159300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'd0fe81dc8e60'
down_revision = '5c29976a36e3'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Check if the 'role' column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'role' not in [column['name'] for column in inspector.get_columns('users')]:
        op.add_column('users', sa.Column('role', sa.String(length=255), nullable=False, server_default='viewer'))

def downgrade() -> None:
    # Check if the 'role' column exists before dropping it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'role' in [column['name'] for column in inspector.get_columns('users')]:
        op.drop_column('users', 'role')
